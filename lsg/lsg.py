import logging
import struct
import sys
from dataclasses import dataclass

from jt_reader.lsg import PartitionNodeElement, MetaDataNodeElement, PartNodeElement, RangeLODNodeElement, \
    GroupNodeElement, TriStripSetShapeNodeElement, MaterialAttributeElement
from jt_reader.lsg.elementHeader import ElementHeader
from jt_reader.lsg.lsgNode import LSGNode
from jt_reader.properties import LateLoadedPropertyAtom, FloatingPointPropertyAtom, StringPropertyAtom
from jt_reader.lsg.types import JtVersion

logger = logging.getLogger(__name__)

@dataclass
class LSG:
    """
    Class representing data contained in the LSG data segment of a .jt-file.
    """
    SEGMENT_TYPE_ID = 1
    nodes: dict[int, LSGNode]
    props: dict
    property_table: list

    rootNode: LSGNode

    def __init__(self, nodes: dict, props: dict, property_table: list):
        self.nodes = nodes
        self.props = props
        self.property_table = property_table
        self._build_lsg()
        self._set_node_properties()

    def _build_lsg(self):
        self.rootNode = self.nodes[0]
        for k_n in self.nodes.keys():
            node = self.nodes[k_n]
            node.child_nodes = [self.nodes[c] for c in node.child_node_object_id]
            node.attributes = [self.nodes[a] for a in node.attr_object_id]
            node.properties = {}

    def _set_node_properties(self):
        for row in self.property_table:
            object_id = row["object id"]
            key_id = row["key property atom"]
            val_id = row["value property atom"]
            key = self.props[key_id].val
            val = self.props[val_id].val
            self.nodes[object_id].properties[key] = val

    def ascii_lsg_tree(self):
        def string_for_node(node: LSGNode, depth=0, max_depth=sys.maxsize):
            node_str = "  " + depth * "|     " + "|-- " + f"{str(node)}"
            if len(node.child_node_object_id) == 0 or depth > max_depth:
                return node_str
            child_str = [string_for_node(c, depth + 1) for c in node.child_nodes]
            child_str = "".join((f"{cs}" for cs in child_str))
            return f"{node_str}\n" + child_str

        return string_for_node(self.rootNode)


def read_lsg_nodes(ds_bytes, version=JtVersion.V9d5) -> dict:
    element_idx = 0
    end_of_elements = False
    nodes = {}
    while ds_bytes.remaining() > 0 and not end_of_elements:
        e_header = ElementHeader.from_bytes(ds_bytes)
        # save offset/ read head position to realign after element read
        read_head = ds_bytes.offset
        print(f'node {element_idx} has type {e_header.object_type_id}')
        if e_header.object_type_id == PartitionNodeElement.TYPE_ID:
            start = ds_bytes.offset
            node_data = PartitionNodeElement.from_bytes(ds_bytes, header=e_header, version=version)
            end = ds_bytes.offset
            remaining = (end - start) - e_header.length
            if remaining > 0:
                print(f"{remaining} bytes left for node, reading and discarding")
                ds_bytes.read(remaining)
        elif e_header.object_type_id == MetaDataNodeElement.TYPE_ID:
            node_data = MetaDataNodeElement.from_bytes(ds_bytes, header=e_header, version=version)
        elif e_header.object_type_id == PartNodeElement.TYPE_ID:
            node_data = PartNodeElement.from_bytes(ds_bytes, header=e_header)
        elif e_header.object_type_id == RangeLODNodeElement.TYPE_ID:
            node_data = RangeLODNodeElement.from_bytes(ds_bytes, header=e_header)
        elif e_header.object_type_id == GroupNodeElement.TYPE_ID:
            node_data = GroupNodeElement.from_bytes(ds_bytes, header=e_header)
        elif e_header.object_type_id == TriStripSetShapeNodeElement.TYPE_ID:
            node_data = TriStripSetShapeNodeElement.from_bytes(ds_bytes, header=e_header)
        elif e_header.object_type_id == MaterialAttributeElement.TYPE_ID:
            node_data = MaterialAttributeElement.from_bytes(ds_bytes, header=e_header)
        elif e_header.object_type_id == ElementHeader.END_OF_ELEMENTS:
            print("End of Elements reached")
            end_of_elements = True
            node_data = None
        else:
            print(f'Found unsupported element type {e_header.object_type_id} while reading LSG segment')
            # ds_bytes.read(e_header.length - 21)
            node_data = None
        if node_data is not None: 
            nodes[e_header.object_id] = node_data
        element_idx += 1
        #realign read position to mitigate propagation of offset errors between elements
        ds_bytes.offset = read_head
        ds_bytes.read(e_header.length - 21)
    return nodes


def read_lsg_props(ds_bytes) -> dict:
    end_of_elements = False
    props = {}
    while ds_bytes.remaining() > 0 and not end_of_elements:
        e_header = ElementHeader.from_bytes(ds_bytes)
        prop = None
        # print(f'node {element_idx} has type {e_header.object_type_id}')
        if e_header.object_type_id == LateLoadedPropertyAtom.TYPE_ID:
            prop = LateLoadedPropertyAtom.from_bytes(ds_bytes, header=e_header)
        elif e_header.object_type_id == FloatingPointPropertyAtom.TYPE_ID:
            prop = FloatingPointPropertyAtom.from_bytes(ds_bytes, header=e_header)
        elif e_header.object_type_id == StringPropertyAtom.TYPE_ID:
            prop = StringPropertyAtom.from_bytes(ds_bytes, header=e_header)
        elif e_header.object_type_id == ElementHeader.END_OF_ELEMENTS:
            # print("End of Elements reached")
            end_of_elements = True
        else:
            print(f'element type {e_header.object_type_id} not implemented')
            break
        props[e_header.object_id] = prop
    return props


def read_property_table(ds_bytes) -> list:
    pt_version_number, element_property_table_count = struct.unpack("<hi", ds_bytes.read(6))
    logger.debug(f'{pt_version_number=}, {element_property_table_count=}')
    property_table = []
    i = 1
    while ds_bytes.remaining() >= 12:  # and i < element_property_table_count:
        element_object_id = struct.unpack("i", ds_bytes.read(4))[0]
        has_keys = True
        while has_keys:
            key_property_atom_bytes = ds_bytes.read(4)
            if key_property_atom_bytes == b'':
                has_keys = False
            else:
                key_property_atom = struct.unpack("i", key_property_atom_bytes)[0]
                if key_property_atom == 0:
                    has_keys = False
                else:
                    val_property_atom = struct.unpack("i", ds_bytes.read(4))[0]
                    property_table.append({
                        "object id": element_object_id,
                        "key property atom": key_property_atom,
                        "value property atom": val_property_atom
                    })
        i += 1
    return property_table


def read_lsg_segment(ds_bytes, version=JtVersion.V9d5):
    # read data
    nodes = read_lsg_nodes(ds_bytes, version=version)
    props = read_lsg_props(ds_bytes)
    property_table = read_property_table(ds_bytes)
    lsg = LSG(nodes, props, property_table)
    return lsg
