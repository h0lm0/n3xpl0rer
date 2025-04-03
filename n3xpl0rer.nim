import terminal, strutils
import modules/workflower

proc recon() =
  setForegroundColor(fgGreen)
  echo "Recon: Not implemented"
  resetAttributes()
  echo "Press Enter to continue..."
  discard readLine(stdin)

proc showMenu() =
  while true:
    eraseScreen(stdout)
    setForegroundColor(fgCyan)
    echo "============================="
    echo "          n3xpl0rer          "
    echo "============================="
    resetAttributes()
    echo "[1] Recon"
    echo "[2] Load a Workflow"
    echo "[3] Exit"
    setForegroundColor(fgCyan)
    echo "============================="
    resetAttributes()
    stdout.write("Select an option: ")
    let choice = readLine(stdin).strip()

    case choice
    of "1":
      recon()
    of "2":
      stdout.write("Enter the YAML file name in the 'workflows' folder: ")
      let filename = readLine(stdin).strip()
      let filepath = "workflows/" & filename
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
