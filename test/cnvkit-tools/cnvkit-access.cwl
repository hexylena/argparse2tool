#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'access']

requirements:
  - class: InlineJavascriptRequirement

description: |
  List the locations of accessible sequence regions in a FASTA file.

inputs:


- id: fa_fname
  type: string

  description: Genome FASTA file name
  inputBinding:
    position: 1


- id: min_gap_size
  type: ["null", int]
  default: 5000
  description: Minimum gap size between accessible sequence
                regions.  Regions separated by less than this distance will
                be joined together. [Default - %(default)s]
  inputBinding:
    position: 2
    prefix: --min-gap-size 

- id: exclude
  type:
  - "null"
  - type: array
    items: string

  description: Additional regions to exclude, in BED format. Can be
                used multiple times.
  inputBinding:
    position: 3
    prefix: --exclude 

- id: output
  type: ["null", File]
  description: Output file name
  inputBinding:
    position: 4
    prefix: --output 
outputs:
- id: output_out
  type: File
  description: Output file name
  outputBinding:
    glob: $(inputs.output.path)
