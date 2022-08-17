import importlib.metadata

import proto_frame.core as pf_core
import proto_frame.lorawan as pf_lorawan


def test_version():
    """Tests that the different ways of getting the version of the package is working."""
    assert importlib.metadata.version("proto_frame") == pf_core.__version__
    assert importlib.metadata.version("proto_frame") == pf_lorawan.__version__
