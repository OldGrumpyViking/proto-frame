from proto_frame.core.frames import SimpleFrame


class TestFrame:
    def test_bytes(self):
        res = bytes(range(10))
        tst_frame = SimpleFrame.from_bytes(res)
        assert tst_frame.to_bytes() == res
