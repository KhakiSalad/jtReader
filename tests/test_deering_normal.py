import pytest

from jt_reader.codec.deeringNormal import DeeringNormalLookupTable


@pytest.fixture
def lookup_table():
    return DeeringNormalLookupTable()


def test_lookup_table_init(lookup_table):
    print(lookup_table)
    lookup_table.lookup_theta_psi(25, 3, 8)
