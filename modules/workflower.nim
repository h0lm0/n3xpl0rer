import yaml

type
  Workflow* = object
    name: string
    steps: seq[string]

proc loadWorkflow*(filename: string): Workflow =
  let content = readFile(filename)
  result = loadAs[Workflow](content)

proc displayWorkflow*(workflow: Workflow) =
  echo "workflow name: ", workflow.name
  echo "setps: "
  for step in workflow.steps:
    echo "  - ", step
