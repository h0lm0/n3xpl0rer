import json, options

type
  Step* = ref object
    name*: string
    command*: string
    match*: Option[string]
    ifSuccess*: Option[Step]
    ifFail*: Option[Step]

  Workflow* = object
    name*: string
    steps*: seq[Step]

proc loadWorkflow*(filename: string): Workflow =
  var wf: Workflow
  let content = readFile(filename)
  let jsonData = parseJson(content)

  wf.name = jsonData["name"].getStr()
  for stepJson in jsonData["steps"].getElems():
    var step = Step(
      name: stepJson["name"].getStr(),
      command: stepJson["command"].getStr(),
      match: if stepJson.hasKey("match") and not stepJson["match"].isNil: some(stepJson["match"].getStr()) else: none(string),
      ifSuccess: none(Step),
      ifFail: none(Step)
    )
    
    if stepJson.hasKey("ifSuccess") and not stepJson["ifSuccess"].isNil:
      step.ifSuccess = some(Step(name: stepJson["ifSuccess"].getStr()))
    if stepJson.hasKey("ifFail") and not stepJson["ifFail"].isNil:
      step.ifFail = some(Step(name: stepJson["ifFail"].getStr()))
    
    wf.steps.add(step)
  
  return wf

proc displayWorkflow*(workflow: Workflow) =
  echo "name: ", workflow.name
  echo "steps: "
  for step in workflow.steps:
    echo "> ", step.name
    echo "  command: ", step.command
    if step.match.isSome:
      echo "  match: ", step.match.get()
    if step.ifSuccess.isSome:
      echo "  ifSuccess: ", step.ifSuccess.get().name
    if step.ifFail.isSome:
      echo "  ifFail: ", step.ifFail.get().name
