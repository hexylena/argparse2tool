#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'gender']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Guess samples' gender from the relative coverage of chromosome X.

inputs:


- id: targets
  type:
    type: array
    items: string

  description: Copy number or copy ratio files (*.cnn, *.cnr).
  inputBinding:
    position: 1


- id: male_reference
  type: ["null", boolean]
  default: True
  description: Assume inputs are already normalized to a male reference
                (i.e. female samples will have +1 log-coverage of chrX;
                otherwise male samples would have -1 chrX).
  inputBinding:
    position: 2
    prefix: --male-reference 

- id: output
  type: ["null", string]
  description: Output table file name.
  inputBinding:
    position: 3
    prefix: --output 
outputs:
    []
