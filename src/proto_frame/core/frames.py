import abc


class BaseFrame(abc.ABC):
    """Base frame for the frame structure."""

    def __repr__(self):
        """Please provide a more friendly representation of the frame.
        
        Returns:
            A pretty representation of the frame.
        """
        return f"{self.__class__.__name__}: {self.to_hex(prefix=True)}"

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
        """ Parse the frame from a hex format.
        
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
        """ Parse the frame from a binary format.
        
        Args:
            frame_bin: The frame to parse.

        Returns:
            The class object created from the raw binary string.
        """
        if frame_bin.startswith("0b"):
            frame_bin = frame_bin[2:]
        return cls.from_bytes(int(frame_bin, 2).to_bytes((len(frame_bin) + 7) // 8, byteorder="big"))

    @abc.abstractmethod
    def to_bytes(self) -> bytes:
        """ Converts the frame to bytes.

        Returns:
            The frame as bytes.
        """
        return b""

    def to_hex(self, prefix: bool = False) -> str:
        """Return the raw frame as a hex representation

        Args:
            prefix: Indicates if the hex string should have a "0x" prefix.

        Returns:
            The frame as hex.
        
        """
        if prefix:
            return f"0x{self.to_bytes().hex().upper()}"
        return self.to_bytes().hex().upper()

    def to_bin(self, prefix: bool = False) -> str:
        """Return the raw frame as a binary representation

        Args:
            prefix: Indicates if the bits should have a "0b" prefix.

        Returns:
            The frame as bits.
        
        """
        frame_bytes = self.to_bytes()
        if prefix:
            return f"0b{format(int.from_bytes(frame_bytes, byteorder='big'), f'0{len(frame_bytes)*8}b')}"
        return format(int.from_bytes(frame_bytes, byteorder="big"), f"0{len(frame_bytes)*8}b")
