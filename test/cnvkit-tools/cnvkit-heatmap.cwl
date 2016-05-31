#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'heatmap']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Plot copy number for multiple samples as a heatmap.

inputs:


- id: filenames
  type:
    type: array
    items: string

  description: Sample coverages as raw probes (.cnr) or segments (.cns).
  inputBinding:
    position: 1


- id: chromosome
  type: ["null", string]
  description: Chromosome (e.g. 'chr1') or chromosomal range (e.g.
                'chr1 -2333000-2444000') to display. If a range is given,
                all targeted genes in this range will be shown, unless
                '--gene'/'-g' is already given.
  inputBinding:
    position: 2
    prefix: --chromosome 

- id: desaturate
  type: ["null", boolean]
  default: True
  description: Tweak color saturation to focus on significant changes.
  inputBinding:
    position: 3
    prefix: --desaturate 

- id: output
  type: ["null", string]
  description: Output PDF file name.
  inputBinding:
    position: 4
    prefix: --output 
outputs:
    []
