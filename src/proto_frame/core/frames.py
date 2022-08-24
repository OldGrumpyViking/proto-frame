import abc
from typing import Union

from proto_frame.core.fields import make_field, Unit, BaseField


class FrameParseError(Exception):
    """ Thrown when one of the from_unit methods fail to parse the input."""


class BaseFrame(abc.ABC):
    """Base frame for the frame structure."""
    FIELDS = ()

    def __repr__(self) -> str:
        output = [f"{self.__class__.__name__}: ({self.to_bytes().hex().upper()})", ]
        for field in self.FIELDS:
            value = self.__dict__[field]
            if isinstance(value, bytes):
                output.append(f"{field}: 0x{value.hex().upper()}")
            elif isinstance(value, str):
                output.append(f"{field}: {value}")
            elif isinstance(value, BaseFrame):
                output.append(f"{field}: <^{value.__class__.__name__}>")
            elif isinstance(value, BaseField):
                output.append(f"{str(value)}")
            else:
                raise NotImplementedError(f"Unknown type of {field=}: {type(value)=}")
        return "\n\t".join(output)

    def __len__(self):
        return len(self.to_bytes())

    @classmethod
    @abc.abstractmethod
    def from_bytes(cls, frame_bytes: bytes):
        """Create the frame object from bytes.

        Args:
            frame_bytes: The frame to parse.

        Returns:
            The class object created from the raw bytes.
        """
        return cls()

    @classmethod
    def from_hex(cls, frame_hex: str):
        """Parse the frame from a hex format.

        Args:
            frame_hex: The frame to parse.

        Returns:
            The class object created from the raw hex string.
        """
        if len(frame_hex) % 2:
            raise ValueError("Hex string must be even number of chars.")
        if frame_hex.startswith("0x"):
            frame_hex = frame_hex[2:]
        return cls.from_bytes(bytes.fromhex(frame_hex))

    @classmethod
    def from_bin(cls, frame_bin: str):
        """Parse the frame from a binary format.

        Args:
            frame_bin: The frame to parse.

        Returns:
            The class object created from the raw binary string.
        """
        if frame_bin.startswith("0b"):
            frame_bin = frame_bin[2:]
        return cls.from_bytes(int(frame_bin, 2).to_bytes((len(frame_bin) + 7) // 8, byteorder="big"))

    def to_bytes(self) -> bytes:
        """Converts the frame to bytes.

        Returns:
            The frame as bytes.
        """
        output = b""
        for field in self.FIELDS:
            value = self.__dict__[field]
            if isinstance(value, bytes):
                output += value
            elif isinstance(value, BaseFrame):
                output += value.to_bytes()
            elif isinstance(value, BaseField):
                output += value.as_unit(Unit.BYTES)
            else:
                raise NotImplementedError(f"Unknown type of {field=}: {type(value)=}")
        return output

    def to_hex(self, prefix: bool = False) -> str:
        """Return the raw frame as a hex representation.

        Args:
            prefix: Indicates if the hex string should have a "0x" prefix.

        Returns:
            The frame as hex.
        """
        if prefix:
            return f"0x{self.to_bytes().hex().upper()}"
        return self.to_bytes().hex().upper()

    def to_bin(self, prefix: bool = False) -> str:
        """Return the raw frame as a binary representation.

        Args:
            prefix: Indicates if the bits should have a "0b" prefix.

        Returns:
            The frame as bits.
        """
        frame_bytes = self.to_bytes()
        if prefix:
            return f"0b{format(int.from_bytes(frame_bytes, byteorder='big'), f'0{len(frame_bytes)*8}b')}"
        return format(int.from_bytes(frame_bytes, byteorder="big"), f"0{len(frame_bytes)*8}b")


class SimpleFrame(BaseFrame):
    FIELDS = ("payload", )

    def __init__(self, payload: Union[bytes, BaseFrame]):
        self.payload = payload

    @classmethod
    def from_bytes(cls, frame_bytes: bytes):
        return cls(frame_bytes)


class LengthFrame(BaseFrame):
    FIELDS = ("length_field", "payload", )
    LEN_FIELD = make_field("length", Unit.INT, repr_unit=Unit.INT)

    def __init__(self, payload: Union[bytes, BaseFrame]):
        self.payload = payload
        self.length_field = self.LEN_FIELD(self.payload.__len__)

    @classmethod
    def from_bytes(cls, frame_bytes: bytes):
        length_field = cls.LEN_FIELD(frame_bytes[:cls.LEN_FIELD.BYTE_LEN], Unit.BYTES)
        payload = frame_bytes[cls.LEN_FIELD.BYTE_LEN:]
        if length_field.value != len(payload):
            raise FrameParseError(f"Length and Payload length do not match: {length_field.value=} {len(payload)=}")
        return cls(payload)
