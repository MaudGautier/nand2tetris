from typing import Optional
from hack_command import HackCommand, HackACommand, HackCCommand

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

    """ Private methods """

    def __init__(self, file_name: FileName):
        self.file_name = file_name
        self.commands = self.__get_commands()
        self.current_command_index = -1
        self.current_command = None

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
            # TODO: Label

        return commands

    """ Public methods """

    def has_more_commands(self) -> bool:
        if self.current_command_index < len(self.commands) - 1:
            return True
        return False

    def advance(self):
        self.current_command_index += 1
        self.current_command = self.commands[self.current_command_index]
