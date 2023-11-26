from hack_parser import HackParser, FileName
from hack_symbol_table import HackSymbolTable


class HackAssembler:
    """ Hack Assembler

    Assembles an assembly file (written in symbolic machine language) into a binary machine code.
    Does so by orchestrating the parsing of the input file and conversion of each command into binary code.
    """
    file_name: FileName

    """ Private methods """

    def __init__(self, file_name: FileName):
        self.file_name = file_name

    def __compute_output_file_name(self):
        return self.file_name.replace(".asm", '.hack')

    @staticmethod
    def __first_scan(parser: HackParser, symbols: HackSymbolTable):
        """ On the first scan, the symbol table is initiated and labels are recorded in the table.
        """

        while parser.has_more_commands():
            parser.advance_first_scan()
            command = parser.current_CandL
            if command.is_label():
                symbols.add_entry(symbol=command.get_symbol(), address=parser.current_command_index + 1)

    @staticmethod
    def __second_scan(output_file_name: str, parser: HackParser, symbols: HackSymbolTable):
        parser.restart()
        with open(output_file_name, "w") as output_file:
            while parser.has_more_commands():
                parser.advance()
                binary_code = parser.current_command.convert_to_binary(symbols)
                output_file.write(binary_code + "\n")

    """ Public methods """

    def assemble(self):
        parser = HackParser(file_name=self.file_name)
        symbols = HackSymbolTable()
        output_file_name = self.__compute_output_file_name()

        self.__first_scan(parser=parser, symbols=symbols)
        self.__second_scan(output_file_name=output_file_name, parser=parser, symbols=symbols)

        print(f"Finished assembling. Result is in file '{output_file_name}'")
