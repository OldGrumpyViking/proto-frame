import proto_frame.core as pf_core


class Frame(pf_core.BaseFrame):
    def __init__(self, payload: bytes):
        self.payload = payload

    @classmethod
    def from_bytes(cls, frame_bytes: bytes):
        return cls(frame_bytes)

    def to_bytes(self) -> bytes:
        return self.payload


class TestFrame:
    def test_bytes(self):
        res = bytes(range(10))
        tst_frame = Frame.from_bytes(res)
        assert tst_frame.to_bytes() == res
