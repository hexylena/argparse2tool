#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'export', 'nexus-basic']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Convert bin-level log2 ratios to Nexus Copy Number "basic" format.

inputs:


- id: filename
  type: string

  description: Log2 copy ratio data file (*.cnr), the output of the 'fix'
                sub-command.
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
