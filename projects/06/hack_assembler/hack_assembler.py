from hack_parser import HackParser, FileName


class HackAssembler:
    """ Hack Assembler

    Assembles an assembly file (written in symbolic machine language) into a binary machine code.
    Does so by orchestrating the parsing of the input file and conversion of each command into binary code.
    """
    file_name: FileName

    def __init__(self, file_name: FileName):
        self.file_name = file_name

    def __compute_output_file_name(self):
        return self.file_name.replace(".asm", '.hack')

    def assemble(self):
        parser = HackParser(file_name=self.file_name)
        output_file_name = self.__compute_output_file_name()
        with open(output_file_name, "w") as output_file:
            while parser.has_more_commands():
                parser.advance()
                binary_code = parser.current_command.convert_to_binary()
                output_file.write(binary_code + "\n")
        print(f"Finished assembling. Result is in file '{output_file_name}'")
