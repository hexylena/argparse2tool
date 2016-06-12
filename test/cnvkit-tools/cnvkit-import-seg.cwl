#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'import-seg']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Convert a SEG file to CNVkit .cns files.

inputs:


- id: segfile
  type: string

  description: Input file in SEG format. May contain multiple samples.
  inputBinding:
    position: 1


- id: chromosomes
  type: ["null", string]
  description: Mapping of chromosome indexes to names. Syntax -
                "from1 -to1,from2 -to2". Or use "human" for the preset -
                "23 -X,24 -Y,25 -M".
  inputBinding:
    position: 2
    prefix: --chromosomes 

- id: prefix
  type: ["null", string]
  description: Prefix to add to chromosome names (e.g 'chr' to rename '8' in
                the SEG file to 'chr8' in the output).
  inputBinding:
    position: 3
    prefix: --prefix 

- id: from_log10
  type: ["null", boolean]
  default: True
  description: Convert base-10 logarithm values in the input to base-2 logs.
  inputBinding:
    position: 4
    prefix: --from-log10 

- id: output_dir
  type: ["null", string]
  default: .
  description: Output directory name.
  inputBinding:
    position: 5
    prefix: --output-dir 
outputs:
    []
