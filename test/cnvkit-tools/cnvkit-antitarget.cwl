#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'antitarget']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Derive a background/antitarget BED file from a target BED file.

inputs:


- id: interval
  type: string

  description: BED or interval file listing the targeted regions.
  inputBinding:
    position: 1


- id: access
  type: ["null", string]
  description: Regions of accessible sequence on chromosomes (.bed), as
                output by genome2access.py.
  inputBinding:
    position: 2
    prefix: --access 

- id: avg_size
  type: ["null", int]
  default: 100000
  description: Average size of antitarget bins (results are approximate).
                [Default - %(default)s]
  inputBinding:
    position: 3
    prefix: --avg-size 

- id: min_size
  type: ["null", int]
  description: Minimum size of antitarget bins (smaller regions are dropped).
                [Default - 1/16 avg size, calculated]
  inputBinding:
    position: 4
    prefix: --min-size 

- id: output
  type: ["null", string]
  description: Output file name.
  inputBinding:
    position: 5
    prefix: --output 
outputs:
    []
