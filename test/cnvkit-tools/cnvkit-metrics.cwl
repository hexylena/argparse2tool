#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'metrics']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Compute coverage deviations and other metrics for self-evaluation.
      

inputs:


- id: cnarrays
  type:
    type: array
    items: string

  description: One or more bin-level coverage data files (*.cnn, *.cnr).
  inputBinding:
    position: 1


- id: segments
  type:
    type: array
    items: string

  description: One or more segmentation data files (*.cns, output of the
                'segment' command).  If more than one file is given, the number
                must match the coverage data files, in which case the input
                files will be paired together in the given order. Otherwise, the
                same segments will be used for all coverage files.
  inputBinding:
    position: 2
    prefix: --segments 

- id: output
  type: ["null", string]
  description: Output table file name.
  inputBinding:
    position: 3
    prefix: --output 
outputs:
    []
