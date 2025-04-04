# <img src="assets/n3xpl0rer.png" width="200" alt="n3xpl0rer logo"> 

**What's this?**

n3xpl0rer is a simple tool designed to automate reconnaissance tasks during penetration tests or security assessments.

The idea behind this project is to allow users to create custom workflows, which n3xpl0rer will execute automatically to streamline the recon process. By defining steps in a workflow, you can speed up your reconnaissance efforts without manually running each tool.

## Installation

wip, bientôt

## Usage

Create your workflows in `workflows` folder.

```bash
cd python
python n3xpl0rer.py
```

## Workflows list

- w1.json: web enum tasks
  - next version: web enum + exploit tasks
- todo w2.json: windows environment enum tasks (cme + impacket)

## Next improvements

- Python version
  - concurrent step (property in json that specify if the step can be concurrent or not)
- Nim version
  - python to nim because it's cool but complex
