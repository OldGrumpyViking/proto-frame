from proto_frame.core import BaseProtocol
from tests.frame_test import Frame


class TestProtocol:
    def setup(self):
        self.frame1_b = bytes(range(0, 10))
        self.frame1 = Frame.from_bytes(self.frame1_b)
        self.frame2_b = bytes(range(10, 20))
        self.frame2 = Frame.from_bytes(self.frame2_b)
        self.frame3_b = bytes(range(20, 30))
        self.frame3 = Frame.from_bytes(self.frame3_b)
        self.protocol = BaseProtocol((self.frame1, self.frame2, self.frame3))

    def test_bytes(self):
        assert self.protocol.to_bytes() == self.frame1_b + self.frame2_b + self.frame3_b

    def test_repr(self):
        print(self.protocol)
        assert str(self.protocol)
