from hack_types import Symbol, Address

# Types
SymbolTable = dict[Symbol, Address]


class HackSymbolTable:
    """ Hack Symbol table

    Contains Symbol tables and values
    """
    symbol_table: SymbolTable
    free_memory_address = 16

    """ Private methods """

    def __init__(self):
        self.symbol_table = {
            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SCREEN": 16384,
            "KBD": 24576,
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4
        }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.symbol_table})"

    """ Public methods """

    def add_entry(self, symbol: Symbol, address: Address) -> None:
        if symbol in self.symbol_table:
            # Should never happen
            raise ValueError(f"Symbol {symbol} is already in table. We should not have gone in this function!")
        self.symbol_table[symbol] = address

    def get_entry(self, symbol: Symbol) -> Address:
        # If already in table => return the corresponding address
        if symbol in self.symbol_table:
            return self.symbol_table[symbol]

        # Otherwise, allocate new address, add it to table and return it
        address_allocated = self.free_memory_address
        self.add_entry(symbol, address_allocated)
        self.free_memory_address += 1
        return address_allocated
