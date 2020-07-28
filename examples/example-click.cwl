#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool ver. 0.4.8
# To generate again: $ example-click.py --generate_cwl_tool
# Help: $ example --help_arg2cwl

cwlVersion: v1.0

class: CommandLineTool
baseCommand: ['example-click.py']

doc: |
  Simple program that greets NAME for a total of COUNT times.

inputs:
  
  count:
    type: ["null", int]
    default: 1
    doc: Number of greetings.
    inputBinding:
      prefix: --count 

  name:
    type: ["null", string]
    doc: The person to greet.
    inputBinding:
      prefix: --name 


outputs:
    []

