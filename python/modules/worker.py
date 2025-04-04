import subprocess
import re
from rich.console import Console

class Worker:
    def __init__(self):
        self.console = Console()
        self.global_vars = {}

    def __replace_variables(self, text, local_vars):
        all_vars = {**self.global_vars, **local_vars}
        def replacer(match):
            var_name = match.group(0)[1:]  # remove the $
            return all_vars.get(var_name, match.group(0))  # keep original if not found
        return re.sub(r"\$[a-zA-Z_][a-zA-Z0-9_]*", replacer, text)

    def __execute_command(self, command, local_vars):
        final_command = self.__replace_variables(command, local_vars)
        self.console.print(f"[bold white]Running:[/bold white] {final_command}", style="dim")
        result = subprocess.run(final_command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()

    def __match_condition(self, pattern, result, local_vars):
        if pattern:
            pattern = self.__replace_variables(pattern, local_vars)
            return bool(re.search(pattern, result))
        return False

    def process_workflow(self, workflow):
        self.__collect_global_variables(workflow)
        for step in workflow['steps']:
            self.__execute_step(step)

    def __collect_global_variables(self, workflow):
        all_commands = []
        for step in workflow['steps']:
            all_commands.append(step.get('command', ''))
            for block in ['ifSuccess', 'ifFail']:
                if block in step:
                    substeps = step[block] if isinstance(step[block], list) else [step[block]]
                    all_commands.extend([s.get('command', '') for s in substeps])

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
            if var_name not in local_vars:
                value = input(f"Enter a value for local variable {var}: ")
                local_vars[var_name] = value
        return local_vars

    def __execute_step(self, step):
        self.console.print(f"\n[bold yellow]Executing step:[/bold yellow] {step['name']}")

        local_vars = self.__extract_local_variables(step['command'])
        result = self.__execute_command(step['command'], local_vars)
        self.console.print(f"[italic]Result:[/italic] {result}")

        if self.__match_condition(step.get('match', ''), result, local_vars):
            self.console.print(f"[✔] Condition met for step: {step['name']}", style="bold green")
            if 'ifSuccess' in step:
                self.__execute_substeps(step['ifSuccess'])
        else:
            self.console.print(f"[✘] Condition failed for step: {step['name']}", style="bold red")
            if 'ifFail' in step:
                self.__execute_substeps(step['ifFail'])

    def __execute_substeps(self, substeps):
        if isinstance(substeps, list):
            for substep in substeps:
                self.__execute_step(substep)
        elif isinstance(substeps, dict):
            self.__execute_step(substeps)
