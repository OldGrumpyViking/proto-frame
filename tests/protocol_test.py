from proto_frame.core.frames import LengthFrame, SimpleFrame
from proto_frame.core.protocols import BaseProtocol


class TestProtocol:
    def setup(self):
        self.payload = bytes(range(10))
        self.frame1 = SimpleFrame.from_bytes(self.payload)
        self.frame2 = LengthFrame(self.frame1)
        self.frame3 = LengthFrame(self.frame2)
        self.protocol = BaseProtocol((self.frame1, self.frame2, self.frame3))
        self.raw = bytes((11, 10)) + self.payload

    def test_to_bytes(self):
        print("protocol:", self.protocol.to_bytes().hex())
        print("test_vector:", self.raw.hex())
        assert self.protocol.to_bytes() == self.raw
        # assert 0

    def test_repr(self):
        print(self.protocol)
        assert str(self.protocol)
        # assert 0

    def test_from_bytes(self):
        protocol = BaseProtocol.from_bytes(self.raw, (LengthFrame, ("payload", LengthFrame), ("payload", SimpleFrame)))
        print(protocol)
        assert protocol.to_bytes() == self.raw
        # assert 0
