#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'breaks']

requirements:
  - class: InlineJavascriptRequirement

description: |
  List the targeted genes in which a copy number breakpoint occurs.

inputs:


- id: filename
  type: string

  description: Processed sample coverage data file (*.cnr), the output
                of the 'fix' sub-command.
  inputBinding:
    position: 1


- id: segment
  type: string

  description: Segmentation calls (.cns), the output of the 'segment' command).
  inputBinding:
    position: 2


- id: min_probes
  type: ["null", int]
  default: 1
  description: Minimum number of within-gene probes on both sides of a
                breakpoint to report it. [Default - %(default)d]
  inputBinding:
    position: 3
    prefix: --min-probes 

- id: output
  type: ["null", string]
  description: Output table file name.
  inputBinding:
    position: 4
    prefix: --output 
outputs:
    []
