#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'export', 'seg']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Convert segments to SEG format.
  
      Compatible with IGV and GenePattern.
      

inputs:


- id: filenames
  type:
    type: array
    items: string

  description: Segmented copy ratio data file(s) (*.cns), the output of the
                'segment' sub-command.
  inputBinding:
    position: 1


- id: output
  type: ["null", string]
  description: Output file name.
  inputBinding:
    position: 2
    prefix: --output 
outputs:
    []
