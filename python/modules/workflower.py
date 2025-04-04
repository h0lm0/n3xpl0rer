from rich.console import Console
import json

class Workflower:
    def __init__(self, file_path):
        self.file_path = file_path
        self.console = Console()

    def load_workflow(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def display_workflow(self):
        try:
            workflow = self.load_workflow()
            self.console.print(f"\n[bold cyan]Workflow Name:[/bold cyan] {workflow['name']}")
            self.console.print("[bold magenta]Steps:[/bold magenta]")

            for idx, step in enumerate(workflow['steps'], start=1):
                self.console.print(f"\n  [bold yellow]Step {idx}: {step['name']}[/bold yellow]")
                self.console.print(f"    [bold white]Command:[/bold white] {step['command']}")
                self.console.print(f"    [bold white]Match Condition:[/bold white] {step.get('match', 'None')}")

                if 'ifSuccess' in step:
                    self.console.print("    [green]→ On Success:[/green]")
                    self.__display_substeps(step['ifSuccess'], level=2)

                if 'ifFail' in step:
                    self.console.print("    [red]→ On Failure:[/red]")
                    self.__display_substeps(step['ifFail'], level=2)

        except FileNotFoundError:
            self.console.print(f"[red]Error:[/red] Workflow {self.file_path} not found.")

    def __display_substeps(self, substeps, level=2):
        indent = " " * (level * 4)

        if isinstance(substeps, list):
            for substep in substeps:
                self.console.print(f"{indent}- [bold yellow]{substep['name']}[/bold yellow]")
                self.console.print(f"{indent}  [bold white]Command:[/bold white] {substep['command']}")
        elif isinstance(substeps, dict):
            self.console.print(f"{indent}- [bold yellow]{substeps['name']}[/bold yellow]")
            self.console.print(f"{indent}  [bold white]Command:[/bold white] {substeps['command']}")
