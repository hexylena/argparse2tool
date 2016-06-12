#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'gainloss']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Identify targeted genes with copy number gain or loss.

inputs:


- id: filename
  type: string

  description: Processed sample coverage data file (*.cnr), the output
                of the 'fix' sub-command.
  inputBinding:
    position: 1


- id: segment
  type: ["null", string]
  description: Segmentation calls (.cns), the output of the 'segment' command).
  inputBinding:
    position: 2
    prefix: --segment 

- id: threshold
  type: ["null", float]
  default: 0.2
  description: Copy number change threshold to report a gene gain/loss.
                [Default - %(default)s]
  inputBinding:
    position: 3
    prefix: --threshold 

- id: min_probes
  type: ["null", int]
  default: 3
  description: Minimum number of covered probes to report a gain/loss.
                [Default - %(default)d]
  inputBinding:
    position: 4
    prefix: --min-probes 

- id: drop_low_coverage
  type: ["null", boolean]
  default: True
  description: Drop very-low-coverage bins before segmentation to avoid
                false-positive deletions in poor-quality tumor samples.
  inputBinding:
    position: 5
    prefix: --drop-low-coverage 

- id: male_reference
  type: ["null", boolean]
  default: True
  description: Assume inputs are already corrected against a male
                reference (i.e. female samples will have +1 log-coverage of
                chrX; otherwise male samples would have -1 chrX).
  inputBinding:
    position: 6
    prefix: --male-reference 

- id: output
  type: ["null", string]
  description: Output table file name.
  inputBinding:
    position: 7
    prefix: --output 
outputs:
    []
