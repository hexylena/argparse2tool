#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'diagram']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Draw copy number (log2 coverages, CBS calls) on chromosomes as a diagram.
  
      If both the raw probes and segments are given, show them side-by-side on
      each chromosome (segments on the left side, probes on the right side).
      

inputs:


- id: filename
  type: ["null", string]
  description: Processed coverage data file (*.cnr), the output of the
                'fix' sub-command.
  inputBinding:
    position: 1


- id: segment
  type: ["null", string]
  description: Segmentation calls (.cns), the output of the 'segment' command.
  inputBinding:
    position: 2
    prefix: --segment 

- id: threshold
  type: ["null", float]
  default: 0.5
  description: Copy number change threshold to label genes.
                [Default - %(default)s]
  inputBinding:
    position: 3
    prefix: --threshold 

- id: min_probes
  type: ["null", int]
  default: 3
  description: Minimum number of covered probes to label a gene.
                [Default - %(default)d]
  inputBinding:
    position: 4
    prefix: --min-probes 

- id: male_reference
  type: ["null", boolean]
  default: True
  description: Assume inputs are already corrected against a male
                reference (i.e. female samples will have +1 log-CNR of
                chrX; otherwise male samples would have -1 chrX).
  inputBinding:
    position: 5
    prefix: --male-reference 

- id: output
  type: ["null", string]
  description: Output PDF file name.
  inputBinding:
    position: 6
    prefix: --output 
outputs:
    []
