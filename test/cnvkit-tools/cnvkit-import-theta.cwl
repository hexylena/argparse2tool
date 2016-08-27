#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'import-theta']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Convert THetA output to a BED-like, CNVkit-like tabular format.
  
      Equivalently, use the THetA results file to convert CNVkit .cns segments to
      integer copy number calls.
      

inputs:


- id: tumor_cns
  type: string


  inputBinding:
    position: 1


- id: theta_results
  type: string


  inputBinding:
    position: 2


- id: ploidy
  type: ["null", int]
  default: 2
  description: Ploidy of normal cells. [Default - %(default)d]
  inputBinding:
    position: 3
    prefix: --ploidy 

- id: output_dir
  type: ["null", string]
  default: .
  description: Output directory name.
  inputBinding:
    position: 4
    prefix: --output-dir 
outputs:
    []
