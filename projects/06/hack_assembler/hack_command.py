from hack_code_converter import HackCodeConverter
from hack_types import RawContent, CommandType, CommandContent, CComp, CDest, CJump, BinaryCode

# Constants
COMMENT_SYMBOL = "//"
JUMP_SEPARATOR = ";"
DEST_SEPARATOR = "="


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
        if self.content.startswith("@"):
            return "A"
        return "C"

    """ Public methods """

    def is_valid(self) -> bool:
        return self.content != ""

    def is_a_command(self) -> bool:
        return self.type == "A"

    def is_c_command(self) -> bool:
        return self.type == "C"

    def convert_to_binary(self):
        pass


class HackACommand(HackCommand):
    """ Hack A-command
    """

    """ Private methods """

    def __get_value(self):
        if not self.content.startswith("@"):
            raise ValueError(f"A-command '{self.content}' does not start with '@' !")

        value = self.content[1:]
        if value.isdigit():
            return int(value)

        raise ValueError("A command case not digit is not handled yet")  # TODO: Handle cases where not digit

    """ Public methods """

    def convert_to_binary(self) -> BinaryCode:
        value = self.__get_value()
        opcode = "0"
        return opcode + format(value, '015b')  # Only keep 15 bits in addition to opcode


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

    def convert_to_binary(self) -> BinaryCode:
        opcode = "1"
        filling_bits = "11"

        code = HackCodeConverter()
        comp = code.convert_comp(self.comp)
        dest = code.convert_dest(self.dest)
        jump = code.convert_jump(self.jump)

        return opcode + filling_bits + comp + dest + jump
