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
    current_command_without_labels_index: int

    """ Private methods """

    def __init__(self, file_name: FileName, is_first_scan: bool = True):
        self.file_name = file_name
        self.commands = self.__get_commands(include_labels=is_first_scan)
        self.current_command_index = -1
        self.current_command = None
        self.current_command_without_labels_index = -1

    def __get_commands(self, include_labels: bool = False) -> list[HackCommand]:
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
            elif include_labels and command.is_label():
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
        if not self.current_command.is_label():
            self.current_command_without_labels_index += 1

    def restart(self):
        self.__init__(file_name=self.file_name, is_first_scan=False)
