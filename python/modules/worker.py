import subprocess
import re
from rich.console import Console

class Worker:
    def __init__(self):
        self.console = Console()
        self.global_vars = {}
        self.state = None

    def __execute_command(self, command, local_vars):
        all_vars = {**self.global_vars, **local_vars}
        original_command = command

        for var in sorted(all_vars.keys(), key=lambda x: -len(x)):
            value = all_vars[var]
            command = command.replace(f"${var}", value)
        
        self.console.print(f"Command: {command}", style="bold cyan")

        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout.strip()
        except KeyboardInterrupt:
            self.console.print("\n[bold red]Execution interrupted by user (Ctrl+C). What would you like to do next?[/bold red]")
            self.state = {'command': original_command, 'local_vars': local_vars}
            self._handle_interrupt()
            return None

    def _handle_interrupt(self):
        while True:
            choice = input("Press 'y' to continue or 'q' to return to the main menu: ").strip().lower()
            if choice == 'y':
                self.console.print("[bold green]Resuming the task...[/bold green]")
                return
            elif choice == 'q':
                self.console.print("[bold red]Returning to the main menu...[/bold red]")
                raise KeyboardInterrupt
            else:
                self.console.print("[bold yellow]Invalid choice. Please press 'y' to continue or 'q' to return to the main menu.[/bold yellow]")

    def __match_condition(self, pattern, result):
        return bool(re.search(pattern, result))

    def process_workflow(self, workflow):
        self.__collect_global_variables(workflow)
        for step in workflow['steps']:
            try:
                self.__execute_step(step)
            except KeyboardInterrupt:
                self.console.print("[bold red]Workflow execution interrupted.[/bold red]")

    def __collect_global_variables(self, workflow):
        all_commands = [step['command'] for step in workflow['steps']]
        for step in workflow['steps']:
            for block in ['ifSuccess', 'ifFail']:
                if block in step:
                    substeps = step[block] if isinstance(step[block], list) else [step[block]]
                    all_commands.extend([s['command'] for s in substeps])

        variables = set(re.findall(r"\$[A-Z][A-Z0-9_]*", " ".join(all_commands)))
        for var in variables:
            var_name = var[1:]
            value = input(f"Enter a value for global variable {var}: ")
            self.global_vars[var_name] = value

    def __extract_local_variables(self, command):
        matches = re.findall(r"\$[a-z][a-z0-9_]*", command)
        local_vars = {}
        for var in matches:
            var_name = var[1:]
            value = input(f"Enter a value for local variable {var}: ")
            local_vars[var_name] = value
        return local_vars

    def __execute_step(self, step, indent=""):
        self.console.print(f"{indent}Executing step: {step['name']}", style="bold yellow")

        local_vars = self.__extract_local_variables(step['command'])
        result = self.__execute_command(step['command'], local_vars)
        if result is None:
            return

        self.console.print(f"{indent}Result: {result}", style="italic")

        if 'match' in step:
            if self.__match_condition(step['match'], result):
                self.console.print(f"{indent}[✔] Condition met for step: {step['name']}", style="bold green")
                if 'ifSuccess' in step:
                    self.__execute_substeps(step['ifSuccess'], indent + "↳")
            else:
                self.console.print(f"{indent}[✘] Condition failed for step: {step['name']}", style="bold red")
                if 'ifFail' in step:
                    self.__execute_substeps(step['ifFail'], indent + "↳")
        else:
            self.console.print(f"{indent}No match condition for step: {step['name']}.", style="dim")
            if 'ifFail' in step:
                self.__execute_substeps(step['ifFail'], indent + "↳")

    def __execute_substeps(self, substeps, indent="↳"):
        if isinstance(substeps, list):
            for substep in substeps:
                self.__execute_step(substep, indent)
        elif isinstance(substeps, dict):
            self.__execute_step(substeps, indent)
