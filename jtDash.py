from dash import Dash, html, dash_table

from jt_reader import load_jt
from jt_reader.lsg.lsgNode import LSGNode
from jt_reader.properties import LateLoadedPropertyAtom
from jt_reader.load_jt import toc_entries_to_df
from jt_reader.logging_config import configure_logging
import argparse
import logging
logger=logging.getLogger(__name__)

global PATH

app = Dash(__name__)

def get_tree(node: LSGNode):
    global PATH
    def flatten_node(n):
        return list(load_jt.flatten_lsg_nodes([n]))[0]

    def node_str(n):
        flat_node = flatten_node(n)
        return f'{flat_node["object id"]}: {flat_node["object type name"]}'

    # node_attr: attributes for current node
    if len(node.attributes) == 0:
        node_attr = html.Div()
    else:
        node_attr = html.Details([
            html.Summary(
                children=["Node Attributes"],
                style={'font-size': '11pt'}
            ),
            *[
                html.Div(
                    [
                        node_str(n),
                        html.Div(
                            flatten_node(n)["val"],
                            style={'font-weight': 'normal'}
                        )
                    ],
                    style={'font-weight': 'bold', 'font-size': '11pt'}
                )
                for n in node.attributes
            ],
        ])

    # node_props: properties for current node
    if len(node.properties) == 0:
        node_props = html.Div()
    else:
        # load late loaded properties
        props = node.properties.copy()
        late_loaded = filter(lambda k: isinstance(node.properties[k], LateLoadedPropertyAtom), node.properties.keys())
        for k in late_loaded:
            ll_segment_id = node.properties[k].segment_id
            ll_entry = list(filter(lambda entry: entry.guid == ll_segment_id, toc))
            if len(ll_entry) > 0:
                ll_entry = ll_entry[0]
                ll_data = load_jt.read_segment(PATH, ll_entry.offset)
                if ll_entry.type == load_jt.DATA_SEGMENT_TYPES[3]:
                    # add metadata properties to node properties
                    del props[k]
                    for k_n in ll_data.data[0].properties.keys():
                        props[k+'_'+k_n] = ll_data.data[0].properties[k_n]
        node.properties = props
        node_props = html.Details([
            html.Summary(
                children=["Node Properties"],
                style={'font-size': '11pt'}
            ),
            dash_table.DataTable(
                data=[{"key": str(k), "val": str(v)} for (k, v) in node.properties.items()],
                style_cell={'textAlign': 'left'}
            ),
        ])

        # build current node in lsg-tree and call function recursively for children
    tree = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        node_str(node),
                        style={'font-size': '12pt', 'font-weight': 'bold'}
                    ),
                    html.Details([
                        html.Summary(
                            children=["Node Value"],
                            style={'font-size': '11pt'}
                        ),
                        html.Div(
                            flatten_node(node)["val"],
                            style={'font-size': '11pt'}
                        )
                    ]),
                    node_attr,
                    node_props,
                    html.Div(
                        [get_tree(c) for c in node.child_nodes],
                        style={'padding-left': f'4em', 'border-left': '2px dashed'}
                    ),
                ],
            )
        ],
        style={'font-family': 'monospace'}
    )
    return tree




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Load a jt file")
    parser.add_argument('version', metavar='v', type=int, nargs='?', help='version to load', default=10)
    parser.add_argument('--debug', action="store_true")
    args = parser.parse_args()
    configure_logging(args.debug)
    logger.info("Started")
    logger.debug("showing debug information")

    global PATH
    if args.version == 9:
        PATH = load_jt.PATH_9
    else:
        PATH = load_jt.PATH_10

    toc = load_jt.read_table_of_contents(PATH)
    toc_df = toc_entries_to_df(toc).sort_values(by="Offset")
    lsg = load_jt.read_segment(PATH, toc_df.iloc[0].Offset)

    app.layout = html.Div([
    html.H1(children='.jt Reader', style={'textAlign': 'center'}),
    html.H3(children='Table of Contents', style={'textAlign': 'center'}),
    dash_table.DataTable(
        id="datatable-toc",
        data=toc_df.to_dict('records'),
        style_cell={'textAlign': 'left'}
    ),
    html.H3(children='Logical Scene Graph - Nodes', style={'textAlign': 'center'}),
    get_tree(lsg.rootNode),
    html.H3(children='Logical Scene Graph - Properties', style={'textAlign': 'center'}),

    ], style={'font-family': 'monospace'})
    app.run(debug=args.debug)
