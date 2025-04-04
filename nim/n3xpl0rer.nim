import terminal, strutils
import modules/workflower
import modules/worker

proc showMenu() =
  while true:
    setForegroundColor(fgCyan)
    echo "============================="
    echo "          n3xpl0rer          "
    echo "============================="
    resetAttributes()
    echo "[1] Recon"
    echo "[2] Load a Workflow"
    echo "[3] Run a Workflow"
    echo "[4] Exit"
    setForegroundColor(fgCyan)
    echo "============================="
    resetAttributes()
    stdout.write("Select an option: ")
    let choice = readLine(stdin).strip()

    case choice
    of "1":
      echo "Recon: Not implemented"
    of "2":
      stdout.write("Enter the JSON file name in the 'workflows' folder: ")
      let filename = readLine(stdin).strip()
      let filepath = "../workflows/" & filename
      try:
        let workflow = workflower.loadWorkflow(filepath)
        workflower.displayWorkflow(workflow)
      except CatchableError as e:
        setForegroundColor(fgRed)
        echo "Error loading the workflow: ", e.msg
        resetAttributes()
      echo "Press Enter to continue..."
      discard readLine(stdin)
    of "3":
      stdout.write("Enter the JSON file name in the 'workflows' folder: ")
      let filename = readLine(stdin).strip()
      let filepath = "../workflows/" & filename
      stdout.write("Enter the target host: ")
      let host = readLine(stdin).strip()
      try:
        let workflow = workflower.loadWorkflow(filepath)
        worker.runWorkflow(workflow, host)
      except CatchableError as e:
        setForegroundColor(fgRed)
        echo "Error executing the workflow: ", e.msg
        resetAttributes()
      echo "Press Enter to continue..."
      discard readLine(stdin)
    of "4":
      setForegroundColor(fgYellow)
      echo "Exiting..."
      resetAttributes()
      quit(0)
    else:
      setForegroundColor(fgRed)
      echo "Invalid option. Please select a valid option."
      resetAttributes()
      echo "Press Enter to continue..."
      discard readLine(stdin)

when isMainModule:
  showMenu()
