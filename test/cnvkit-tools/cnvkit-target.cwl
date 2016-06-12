#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'target']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Transform bait intervals into targets more suitable for CNVkit.

inputs:


- id: interval
  type: string

  description: BED or interval file listing the targeted regions.
  inputBinding:
    position: 1


- id: annotate
  type: ["null", string]
  description: UCSC refFlat.txt or ensFlat.txt file for the reference genome.
                Pull gene names from this file and assign them to the target
                regions.
  inputBinding:
    position: 2
    prefix: --annotate 

- id: short_names
  type: ["null", boolean]
  default: True
  description: Reduce multi-accession bait labels to be short and consistent.
  inputBinding:
    position: 3
    prefix: --short-names 

- id: split
  type: ["null", boolean]
  default: True
  description: Split large tiled intervals into smaller, consecutive targets.
  inputBinding:
    position: 4
    prefix: --split 

- id: avg_size
  type: ["null", int]
  default: 266.6666666666667
  description: Average size of split target bins (results are approximate).
                [Default - %(default)s]
  inputBinding:
    position: 5
    prefix: --avg-size 

- id: output
  type: ["null", string]
  description: Output file name.
  inputBinding:
    position: 6
    prefix: --output 
outputs:
    []
