import abc
import enum


class Order(enum.Enum):
    LITTLE = "little"
    BIG = "big"


class Unit(enum.Enum):
    BYTES = enum.auto()
    HEX = enum.auto()
    BIN = enum.auto()
    INT = enum.auto()


class BaseField(abc.ABC):
    """Base field for the field structure."""
    BIT_LENGTH = 8
    BIT_ORDER = Order.BIG.value
    SIGNED = False
    REPR_UNIT = Unit.HEX

    def __repr__(self) -> str:
        """Please provide a more friendly representation of the field.

        Returns:
            A pretty representation of the field.
        """
        output = f"{self.__class__.__name__}: "
        if self.REPR_UNIT == Unit.BYTES:
            output += f"{self.to_bytes()}"
        elif self.REPR_UNIT == Unit.HEX:
            output += f"{self.to_hex(prefix=True)}"
        elif self.REPR_UNIT == Unit.BIN:
            output += f"{self.to_bin(prefix=True)}"
        elif self.REPR_UNIT == Unit.INT:
            output += f"{self.to_int()}"
        else:
            raise ValueError(f"Unknown {self.REPR_UNIT=}")
        return output

    @classmethod
    def byte_length(cls) -> int:
        return (cls.BIT_LENGTH + 7) // 8

    @classmethod
    @abc.abstractmethod
    def from_bytes(cls, field_bytes: bytes):
        """Create the field object from bytes.

        Args:
            field_bytes: The field to parse.

        Returns:
            The class object created from the raw bytes.
        """
        return cls()

    @classmethod
    def from_hex(cls, field_hex: str):
        """Parse the field from a hex format.

        Args:
            field_hex: The field to parse.

        Returns:
            The class object created from the raw hex string.
        """
        if len(field_hex) % 2:
            raise ValueError("Hex string must be even number of chars.")
        if field_hex.startswith("0x"):
            field_hex = field_hex[2:]
        return cls.from_bytes(bytes.fromhex(field_hex, ))

    @classmethod
    def from_bin(cls, field_bin: str):
        """Parse the field from a binary format.

        Args:
            field_bin: The field to parse.

        Returns:
            The class object created from the raw binary string.
        """
        if field_bin.startswith("0b"):
            field_bin = field_bin[2:]
        return cls.from_bytes(int(field_bin, 2).to_bytes((len(field_bin) + 7) // 8, byteorder=cls.BIT_ORDER, signed=cls.SIGNED))

    @classmethod
    def from_int(cls, field_int: int):
        return cls.from_bytes(field_int.to_bytes((cls.BIT_LENGTH + 7) // 8, byteorder=cls.BIT_ORDER, signed=cls.SIGNED))

    @abc.abstractmethod
    def to_bytes(self) -> bytes:
        """Converts the field to bytes.

        Returns:
            The field as bytes.
        """
        return b""

    def to_hex(self, prefix: bool = False) -> str:
        """Return the raw field as a hex representation.

        Args:
            prefix: Indicates if the hex string should have a "0x" prefix.

        Returns:
            The field as hex.
        """
        if prefix:
            return f"0x{self.to_bytes().hex().upper()}"
        return self.to_bytes().hex().upper()

    def to_bin(self, prefix: bool = False) -> str:
        """Return the raw field as a binary representation.

        Args:
            prefix: Indicates if the bits should have a "0b" prefix.

        Returns:
            The field as bits.
        """
        field_bytes = self.to_bytes()
        if prefix:
            return f"0b{format(int.from_bytes(field_bytes, byteorder=self.BIT_ORDER, signed=self.SIGNED), f'0{len(field_bytes)*8}b')}"
        return format(int.from_bytes(field_bytes, byteorder=self.BIT_ORDER, signed=self.SIGNED), f"0{len(field_bytes)*8}b")

    def to_int(self) -> int:
        """ Converts the field to an integer.

        Returns:
            An integer representation of the field
        """
        return int.from_bytes(self.to_bytes(), byteorder=self.BIT_ORDER, signed=self.SIGNED)


class LengthField(BaseField):
    REPR_UNIT = Unit.INT

    def __init__(self, length: int):
        if length >= 2**(self.BIT_LENGTH):
            raise ValueError(f"Length is too large, max allowed is {2**(self.BIT_LENGTH)-1}: {length=}")
        self.length = length

    @classmethod
    def from_bytes(cls, length_bytes: bytes):
        """Create the field object from bytes.

        Args:
            field_bytes: The field to parse.

        Returns:
            The class object created from the raw bytes.
        """
        return cls(int.from_bytes(length_bytes, byteorder=cls.BIT_ORDER, signed=cls.SIGNED))

    def to_bytes(self) -> bytes:
        """Converts the field to bytes.

        Returns:
            The field as bytes.
        """
        return bytes((self.length,))
