import proto_frame.core as pf_core


class LorawanFrame(pf_core.BaseFrame):
    """Base frame for the frame structure."""

    def __init__(self, payload: bytes):
        self.payload = payload

    @classmethod
    def from_bytes(cls, frame_bytes: bytes):
        return cls(frame_bytes)

    def to_bytes(self) -> bytes:
        return self.payload
