#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'coverage']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Calculate coverage in the given regions from BAM read depths.

inputs:


- id: bam_file
  type: string

  description: Mapped sequence reads (.bam)
  inputBinding:
    position: 1


- id: interval
  type: string

  description: Intervals (.bed or .list)
  inputBinding:
    position: 2


- id: count
  type: ["null", boolean]
  default: True
  description: Get read depths by counting read midpoints within each bin.
                (An alternative algorithm).
  inputBinding:
    position: 3
    prefix: --count 

- id: min_mapq
  type: ["null", int]
  description: Minimum mapping quality score (phred scale 0-60) to count a read
                for coverage depth.  [Default - %(default)s]
  inputBinding:
    position: 4
    prefix: --min-mapq 

- id: output
  type: ["null", string]
  description: Output file name.
  inputBinding:
    position: 5
    prefix: --output 
outputs:
    []
