from typing import Optional
from hack_command import HackCommand, HackACommand, HackCCommand, HackLabel

# Types
FileName = str


class HackParser:
    """ Hack File Parser

    Provides methods to parse all commands of a file
    """
    file_name: FileName
    commands: list[HackCommand]
    current_command_index: int
    current_command: Optional[HackCommand]
    commands_and_label_declarations: list[HackCommand]
    current_CandL_index: int
    current_CandL: Optional[HackCommand]

    """ Private methods """

    def __init__(self, file_name: FileName):
        self.file_name = file_name
        self.commands = self.__get_commands()
        self.commands_and_label_declarations = self.__get_valid_lines()
        self.restart()

    def __get_commands(self) -> list[HackCommand]:
        with open(self.file_name, "r") as file:
            lines = file.readlines()

        commands: list[HackCommand] = []
        for line in lines:
            command = HackCommand(line)
            if not command.is_valid():
                continue
            if command.is_a_command():
                commands.append(HackACommand(line))
            elif command.is_c_command():
                commands.append(HackCCommand(line))
            elif command.is_label():
                pass  # Do not add labels to list of commands

        return commands

    def __get_valid_lines(self) -> list[HackCommand]:
        with open(self.file_name, "r") as file:
            lines = file.readlines()

        commands: list[HackCommand] = []
        for line in lines:
            command = HackCommand(line)
            if not command.is_valid():
                continue
            if command.is_a_command():
                commands.append(HackACommand(line))
            elif command.is_c_command():
                commands.append(HackCCommand(line))
            elif command.is_label():
                commands.append(HackLabel(line))

        return commands

    """ Public methods """

    def has_more_commands(self) -> bool:
        if self.current_command_index < len(self.commands) - 1:
            return True
        return False

    def advance(self):
        self.current_command_index += 1
        self.current_command = self.commands[self.current_command_index]

    def advance_first_scan(self):
        self.current_CandL_index += 1
        self.current_CandL = self.commands_and_label_declarations[self.current_CandL_index]
        if not self.current_CandL.is_label():
            self.advance()

    def restart(self):
        self.current_command_index = -1
        self.current_command = None
        self.current_CandL_index = -1
        self.current_CandL = None
