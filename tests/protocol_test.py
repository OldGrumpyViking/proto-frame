from proto_frame.core.frames import SimpleFrame, LengthFrame
from proto_frame.core.protocols import BaseProtocol


class TestProtocol:
    def setup(self):
        self.payload = bytes(range(10))
        self.frame1 = SimpleFrame.from_bytes(self.payload)
        self.frame2 = LengthFrame(self.frame1)
        self.frame3 = LengthFrame(self.frame2)
        self.protocol = BaseProtocol((self.frame1, self.frame2, self.frame3))

    def test_bytes(self):
        print("protocol:", self.protocol.to_bytes().hex())
        print("test_vector:", (bytes((10, 11)) + self.payload).hex())
        assert self.protocol.to_bytes() == bytes((11, 10)) + self.payload

    def test_repr(self):
        print(self.protocol)
        assert str(self.protocol)
