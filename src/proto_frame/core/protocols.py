from typing import Iterable, Optional


class BaseProtocol:
    """Base protocol structure as a collection of frames.

    Attributes:
        frames: The frames that compose the protocol.
    """

    def __init__(self, frames: Iterable):
        self.frames = list(frames)

    def __repr__(self):
        """Represents the protocol and its frames.

        Returns:
            A human readable represenation of the protocol.
        """
        return "\n\t".join(
            [
                self.__class__.__name__,
            ]
            + [frame.__repr__().replace("\n", "\n\t") for frame in self.frames]
        )

    def to_bytes(self, layer: Optional[int] = None) -> bytes:
        """Return the raw frame as bytes.

        Args:
            layer: The protocol layer to return as bytes. None will select the lowest layer.

        Returns:
            The protocol as bytes given the layer tier.
        """
        if layer is None:
            layer = len(self.frames)-1
        if layer < 0:
            raise ValueError(f"layer cannot be negative. Got {layer=}")
        if layer >= len(self.frames):
            raise ValueError(f"layer cannot be higher or equal to the number of frames. Got {layer=}")
        return self.frames[layer].to_bytes()

    def to_hex(self, layer: Optional[int] = None, prefix: bool = False) -> str:
        """Return the raw frame as a hex representation.

        Args:
            prefix: Indicates if the hex string should have a "0x" prefix.

        Returns:
            The protocol as hex given the layer tier.
        """
        if prefix:
            return f"0x{self.to_bytes(layer).hex().upper()}"
        return self.to_bytes(layer).hex().upper()

    def to_bin(self, layer: Optional[int] = None, prefix: bool = False) -> str:
        """Return the raw frame as a binary representation.

        Args:
            prefix: Indicates if the bits should have a "0b" prefix.

        Returns:
            The protocol as bits given the layer tier.
        """
        frame_bytes = self.to_bytes(layer)
        if prefix:
            return f"0b{format(int.from_bytes(frame_bytes, byteorder='big'), f'0{len(frame_bytes)*8}b')}"
        return format(int.from_bytes(frame_bytes, byteorder="big"), f"0{len(frame_bytes)*8}b")
