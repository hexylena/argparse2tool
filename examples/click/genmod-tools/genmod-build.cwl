#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool ver. 0.3.0
# To generate again: $ genmod --generate_cwl_tool
# Help: $ genmod --help_arg2cwl

cwlVersion: "cwl:v1.0"

class: CommandLineTool
baseCommand: ['genmod', 'build']

description: |
  Build a new annotation database
  
  Build an annotation database from an annotation file.

inputs:
  
  annotation_file:
    type: string
  
    description: ANNOTATION_FILE
    inputBinding:
      position: 1

  outdir:
    type: ["null", string]
    description: Specify the path to a folder where the annotation files should be stored.
    inputBinding:
      prefix: --outdir 

  annotation_type:
    type:
    - "null"
    - type: enum
      symbols: []
    default: gene_pred
    description: Specify the format of the annotation file.
    inputBinding:
      prefix: --annotation_type 

  splice_padding:
    type: ["null", int]
    default: 2
    description: Specify the the number of bases that the exons should be padded with. Default is 2 bases.
    inputBinding:
      prefix: --splice_padding 

  verbose:
    type:
    - "null"
    - type: array
      items: string
  
    default: 0
    description: Increase output verbosity.
    inputBinding:
      prefix: --verbose 


outputs:
    []
