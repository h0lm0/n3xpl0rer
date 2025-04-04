import subprocess
import re
from rich.console import Console

class Worker:
    def __init__(self):
        self.console = Console()

    def __execute_command(self, command):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout

    def __match_condition(self, pattern, result):
        return re.search(pattern, result) is not None

    def process_workflow(self, workflow):
        for step in workflow['steps']:
            self.console.print(f"Executing step: {step['name']}", style="bold yellow")
            result = self.__execute_command(step['command'])
            self.console.print(f"Result: {result}", style="italic")

            if self.__match_condition(step['match'], result):
                self.console.print("Condition met, executing ifSuccess", style="bold green")
                self.__execute_commands(step['ifSuccess'])
            else:
                self.console.print("Condition failed, executing ifFail", style="bold red")
                if 'ifFail' in step:
                    self.__execute_commands(step['ifFail'])

    def __execute_commands(self, commands):
        if isinstance(commands, list):
            for command_info in commands:
                self.console.print(f"Executing command: {command_info['name']}", style="bold yellow")
                result = self.__execute_command(command_info['command'])
                self.console.print(f"Result: {result}", style="italic")
        else:
            self.console.print(f"Executing command: {commands['name']}", style="bold yellow")
            result = self.__execute_command(commands['command'])
            self.console.print(f"Result: {result}", style="italic")
