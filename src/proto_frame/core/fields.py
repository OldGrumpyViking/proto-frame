import enum
import abc


class Order(enum.Enum):
    LITTLE = "little"
    BIG = "big"


class Unit(enum.Enum):
    BYTES = enum.auto()
    HEX = enum.auto()
    BIN = enum.auto()
    INT = enum.auto()


class BaseField(abc.ABC):
    pass


def make_field(name: str, value_unit=Unit.BYTES, bit_len=8, bit_order=Order.BIG, signed=False, repr_unit=Unit.HEX):
    class Field(BaseField):
        NAME = name
        VALUE_UNIT = value_unit
        BIT_LEN = bit_len
        BYTE_LEN = (bit_len + 7) // 8
        BIT_ORDER = bit_order
        SIGNED = signed
        REPR_UNIT = repr_unit

        def __init__(self, value, unit=value_unit):
            if callable(value):
                self._value = value
                self._callable_unit = unit
            else:
                self._value = self._transform_unit(value, unit, self.VALUE_UNIT)
                self._callable_unit = None
            self.verify_bit_size(self._value)

        def __repr__(self) -> str:
            return f"{self.__class__.__name__}-{self.NAME}: {self.as_unit(self.REPR_UNIT, prefix=True)}"

        @staticmethod
        def _transform_unit(value, from_unit, to_unit):
            if from_unit == to_unit:
                return value
            # Always transform to bytes
            if from_unit != Unit.BYTES:
                if from_unit == Unit.HEX:
                    value = bytes.fromhex(value)
                elif from_unit == Unit.BIN:
                    value = int(value, 2).to_bytes(Field.BYTE_LEN, byteorder=Field.BIT_ORDER.value, signed=Field.SIGNED)
                elif from_unit == Unit.INT:
                    value = value.to_bytes(Field.BYTE_LEN, byteorder=Field.BIT_ORDER.value, signed=Field.SIGNED)
                else:
                    raise NotImplementedError(f"Unit unknwon: {from_unit=}")
            # Convert bytes to the desired unit
            if to_unit != Unit.BYTES:
                if to_unit == Unit.HEX:
                    value = value.hex().upper()
                elif to_unit == Unit.BIN:
                    value = format(int.from_bytes(value, byteorder=Field.BIT_ORDER.value, signed=Field.SIGNED), f"0{len(value)*8}b")
                elif to_unit == Unit.INT:
                    value = int.from_bytes(value, byteorder=Field.BIT_ORDER.value, signed=Field.SIGNED)
                else:
                    raise NotImplementedError(f"Unit unknwon: {to_unit=}")
            return value

        def verify_bit_size(self, value):
            if callable(value):
                value = self._transform_unit(value(), self._callable_unit, Unit.INT)
            else:
                value = self._transform_unit(value, self.VALUE_UNIT, Unit.INT)
            if self.SIGNED:
                if not (-2**self.BIT_LEN //2) <= value < (2**self.BIT_LEN // 2):
                    raise ValueError(f"{value=} not within {self.BIT_LEN=}")
            else:
                if not 0 <= value < 2**self.BIT_LEN:
                    raise ValueError(f"{value=} not within {self.BIT_LEN=}")

        @property
        def value(self):
            if callable(self._value):
                return self._transform_unit(self._value(), self._callable_unit, self.VALUE_UNIT)
            return self._value

        def as_unit(self, unit: Unit, prefix=False):
            if callable(self._value):
                value = self._transform_unit(self._value(), self._callable_unit, unit)
            else:
                value = self._transform_unit(self._value, self.VALUE_UNIT, unit)
            if prefix:
                if unit == Unit.HEX:
                    value = f"0x{value}"
                if unit == Unit.BIN:
                    value = f"0b{value}"
            return value
    return Field

if __name__ == "__main__":
    MyField = make_field("length", Unit.INT, repr_unit=Unit.INT)
    a = MyField(10, Unit.INT)
    print(a)
    b = MyField(10)
    print(b)
    print(a.as_unit(Unit.HEX, prefix=True))
    print(a.value)
    # c = MyField(300)
    d = [1,2,3]
    e = MyField(d.__len__)
    print(d, e)
    d.append(4)
    print(d, e)
