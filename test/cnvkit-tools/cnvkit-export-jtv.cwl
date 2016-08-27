#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'export', 'jtv']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Convert log2 ratios to Java TreeView's native format.

inputs:


- id: filenames
  type:
    type: array
    items: string

  description: Log2 copy ratio data file(s) (*.cnr), the output of the
                    'fix' sub-command.
  inputBinding:
    position: 1


- id: output
  type: ["null", string]
  description: Output file name.
  inputBinding:
    position: 2
    prefix: --output 
outputs:
    []
