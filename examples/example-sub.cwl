#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool
# To generate again: $ example-sub.py --generate_cwl_tool
# Help: $ example --help_arg2cwl

cwlVersion: v1.0

class: CommandLineTool
baseCommand: ['example-sub.py', 'foo']

doc: |
  None

inputs:
  
  keyword:
    type:
      type: array
      items: string

    doc: action keyword
    inputBinding:
      position: 1

  integers:
    type:
      type: array
      items: int

    doc: an integer for the accumulator
    inputBinding:
      position: 2

  foo:
    type: ["null", string]
    doc: foo help
    inputBinding:
      prefix: --foo 

  bar:
    type:
    - "null"
    - type: array
      items: string

    default: [1, 2, 3]
    doc: BAR!
    inputBinding:
      prefix: --bar 

  true:
    type: ["null", boolean]
    default: False
    doc: Store a true
    inputBinding:
      prefix: --true 


outputs:
    []

#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool
# To generate again: $ example-sub.py --generate_cwl_tool
# Help: $ example --help_arg2cwl

cwlVersion: v1.0

class: CommandLineTool
baseCommand: ['example-sub.py', 'bar']

doc: |
  None

inputs:
  
  false:
    type: ["null", boolean]
    default: True
    doc: Store a false
    inputBinding:
      prefix: --false 

  append:
    type:
    - "null"
    - type: array
      items: string

    doc: Append a value
    inputBinding:
      prefix: --append 

  nargs2:
    type:
    - "null"
    - type: array
      items: string

    doc: nargs2
    inputBinding:
      prefix: --nargs2 

  mode:
    type:
    - "null"
    - type: enum
      symbols: ['rock', 'paper', 'scissors']
    default: scissors

    inputBinding:
      prefix: --mode 


outputs:
    []

