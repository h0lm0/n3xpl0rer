import osproc, re
import workflower
import std/strutils
import options
import os

proc findCommandPath(command: string): string =
  let path = findExe(command)
  if path.len == 0:
    echo "[ERROR] Command not found: ", command
    return ""
  return path

proc executeStep*(step: Step, host: string) =
  echo "[WORKER] Executing: ", step.command
  var parts = step.command.split(" ")
  let exePath = findCommandPath(parts[0])

  if exePath.len == 0:
    echo "[ERROR] Skipping step: ", step.name
    return

  let cmd = exePath & " " & parts[1..^1].join(" ")
  let finalCmd = cmd.replace("$host", host)
  let output = execProcess(finalCmd, options = {poStdErrToStdOut})

  echo output
  
  if step.match.isSome() and output.match(re(step.match.get())):
    echo "[WORKER] Match found: ", step.match.get()
    if step.ifSuccess.isSome:
      executeStep(step.ifSuccess.get(), host)
  else:
    if step.ifFail.isSome:
      executeStep(step.ifFail.get(), host)

proc runWorkflow*(workflow: Workflow, host: string) =
  echo "[WORKER] Running workflow: ", workflow.name
  for step in workflow.steps:
    executeStep(step, host)
