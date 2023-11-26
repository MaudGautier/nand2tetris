from hack_code_converter import HackCodeConverter
from hack_types import RawContent, CommandType, CommandContent, CComp, CDest, CJump, BinaryCode, Symbol
from hack_symbol_table import HackSymbolTable

# Constants
COMMENT_SYMBOL = "//"
JUMP_SEPARATOR = ";"
DEST_SEPARATOR = "="
A_COMMAND_IDENTIFIER = "@"
LABEL_DECLARATION_IDENTIFIER = "("


class HackCommand:
    """ Hack Command

    Provides utility methods to deal with commands (C-command, A-command, label) and convert them to binary code
    """
    content: CommandContent
    type: CommandType

    """ Private methods """

    def __init__(self, raw_content: RawContent):
        self.content = self.__clean(raw_content)
        self.type = self.__get_command_type()

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.content}', type={self.type})"

    def __clean(self, raw_content: str) -> CommandContent:
        return self.__strip_comment(raw_content).strip()

    @staticmethod
    def __strip_comment(raw_content: str) -> CommandContent:
        comment_start = raw_content.find(COMMENT_SYMBOL)
        if comment_start == -1:
            return raw_content

        return raw_content[:comment_start]

    def __get_command_type(self) -> CommandType:
        if self.content.startswith(A_COMMAND_IDENTIFIER):
            return "A"

        if self.content.startswith(LABEL_DECLARATION_IDENTIFIER):
            return "L"

        return "C"

    """ Public methods """

    def is_valid(self) -> bool:
        return self.content != ""

    def is_a_command(self) -> bool:
        return self.type == "A"

    def is_c_command(self) -> bool:
        return self.type == "C"

    def is_label(self) -> bool:
        return self.type == "L"

    def convert_to_binary(self, symbols: HackSymbolTable):
        pass

    def get_symbol(self):
        pass


class HackACommand(HackCommand):
    """ Hack A-command
    """

    """ Private methods """

    def __get_value(self) -> int or str:
        value = self.content[1:]

        # Constant
        if value.isdigit():
            return int(value)

        # Symbol (label or previously declared variable)
        return value

    @staticmethod
    def __format_binary_code(value: int or str):
        # Only keep 15 bits in addition to opcode
        opcode = "0"
        return opcode + format(value, '015b')

    """ Public methods """

    def convert_to_binary(self, symbols: HackSymbolTable) -> BinaryCode:
        value = self.__get_value()

        # Case constant
        if isinstance(value, int):
            return self.__format_binary_code(value)

        # Case symbol (variable or label)
        address = symbols.get_entry(str(value))
        return self.__format_binary_code(address)

    def get_symbol(self) -> Symbol:
        return str(self.__get_value())


class HackCCommand(HackCommand):
    """ Hack C-command
    """
    comp: CComp
    dest: CDest
    jump: CJump

    """ Private methods """

    def __init__(self, raw_content: RawContent):
        super().__init__(raw_content=raw_content)
        self.comp = self.__get_comp()
        self.dest = self.__get_dest()
        self.jump = self.__get_jump()

    def __get_comp(self) -> CComp:
        dest_comp_fields = self.content.partition(JUMP_SEPARATOR)[0]
        if DEST_SEPARATOR in dest_comp_fields:
            return dest_comp_fields.partition(DEST_SEPARATOR)[2]
        return dest_comp_fields

    def __get_dest(self) -> CDest:
        dest_comp_fields = self.content.partition(JUMP_SEPARATOR)[0]
        if DEST_SEPARATOR in dest_comp_fields:
            return dest_comp_fields.partition(DEST_SEPARATOR)[0]
        return None

    def __get_jump(self) -> CJump:
        jump_field = self.content.partition(JUMP_SEPARATOR)[2]
        return jump_field if jump_field else None

    """ Public methods """

    def convert_to_binary(self, _: HackSymbolTable) -> BinaryCode:
        opcode = "1"
        filling_bits = "11"

        code = HackCodeConverter()
        comp = code.convert_comp(self.comp)
        dest = code.convert_dest(self.dest)
        jump = code.convert_jump(self.jump)

        return opcode + filling_bits + comp + dest + jump

    def get_symbol(self):
        # Should never happen
        raise ValueError("No symbol associated to a C-Command !!")


class HackLabel(HackCommand):
    """ Hack Label
    """

    """ Public methods """

    def get_symbol(self) -> Symbol:
        return str(self.content[1:-1])
