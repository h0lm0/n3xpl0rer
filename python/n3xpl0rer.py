from rich.console import Console
from rich.prompt import Prompt
from modules.workflower import Workflower
from modules.worker import Worker

class n3xpl0rer:
    def __init__(self):
        self.console = Console()
        self.menu_options = ["Display Workflow", "Run Workflow", "Exit"]

    def display_menu(self):
        ascii_art = r"""
[bold green]

👾 n̲3̲x̲p̲l̲0̲r̲e̲r̲ 👾

[/bold green]
        """
        self.console.print(ascii_art)

        for idx, option in enumerate(self.menu_options, start=1):
            self.console.print(f"[bold cyan]{idx}[/bold cyan]. {option}")
        self.console.print("\n" + "=" * 40)


    def run(self):
        while True:
            self.display_menu()
            choice = Prompt.ask("Select an option", choices=[str(i) for i in range(1, len(self.menu_options) + 1)])

            if choice == "1":
                self.display_workflow()
            elif choice == "2":
                self.run_workflow()
            elif choice == "3":
                self.console.print("Exiting...", style="bold red")
                break

    def display_workflow(self):
        workflow_path = input("Enter the path to the workflow JSON file: ")
        workflower = Workflower(workflow_path)
        workflower.display_workflow()

    def run_workflow(self):
      try:
        workflow_path = input("Enter the path to the workflow JSON file: ")
        workflower = Workflower(workflow_path)
        worker = Worker()
        workflow = workflower.load_workflow()
        self.console.print(f"Loaded workflow: {workflow['name']}", style="bold blue")
        worker.process_workflow(workflow)
      except FileNotFoundError as e:
        self.console.print(f"Workflow {workflow_path} not found", style="red")

if __name__ == "__main__":
    app = n3xpl0rer()
    app.run()
