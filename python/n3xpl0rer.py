from rich.console import Console
from rich.prompt import Prompt
from modules.workflower import Workflower
from modules.worker import Worker

class N3xpl0rer:
    def __init__(self):
        self.console = Console()
        self.menu_options = ["Display Workflow", "Run Workflow", "Exit"]

    def display_menu(self):
        self.console.print("n3xpl0rer", style="bold green")
        for idx, option in enumerate(self.menu_options, start=1):
            self.console.print(f"{idx}. {option}")

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
      try:
        workflow_path = input("Enter the path to the workflow JSON file: ")
        workflower = Workflower(workflow_path)
        workflow = workflower.load_workflow()
        self.console.print(f"Workflow Name: {workflow['name']}", style="bold blue")
        for step in workflow['steps']:
            self.console.print(f"- {step['name']}", style="bold yellow")
      except FileNotFoundError as e:
        self.console.print(f"Workflow {workflow_path} not found", style="red")

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
    app = N3xpl0rer()
    app.run()
