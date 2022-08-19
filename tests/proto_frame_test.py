import importlib.metadata

from proto_frame.core import _version


def test_version():
    """Tests that the different ways of getting the version of the package is working."""
    assert importlib.metadata.version("proto_frame") == _version.__version__
