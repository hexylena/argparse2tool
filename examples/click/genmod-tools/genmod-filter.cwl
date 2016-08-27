#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2cwl ver. 0.3.0
# To generate again: $ genmod --generate_cwl_tool
# Help: $ genmod --help_arg2cwl

cwlVersion: "cwl:v1.0"

class: CommandLineTool
baseCommand: ['genmod', 'filter']

description: |
  Filter vcf variants.
  
  Filter variants based on their annotation

inputs:
  
  variant_file:
    type: File
  
    description: <vcf_file> or -
    inputBinding:
      position: 1

  annotation:
    type: ["null", string]
    default: 1000GAF
    description: Specify the info annotation to search for. Default 1000GAF
    inputBinding:
      prefix: --annotation 

  threshold:
    type: ["null", float]
    default: 0.05
    description: Threshold for filter variants. Default 0.05
    inputBinding:
      prefix: --threshold 

  discard:
    type: ["null", boolean]
    default: False
    description: If variants without the annotation should be discarded
    inputBinding:
      prefix: --discard 

  greater:
    type: ["null", boolean]
    default: False
    description: If greater than threshold should be used instead of less thatn threshold.
    inputBinding:
      prefix: --greater 

  silent:
    type: ["null", boolean]
    default: False
    description: Do not print the variants.
    inputBinding:
      prefix: --silent 

  outfile:
    type: ["null", File]
    description: Specify the path to a file where results should be stored.
    inputBinding:
      prefix: --outfile 


outputs:

  outfile_out:
    type: File
  
    description: Specify the path to a file where results should be stored.
    outputBinding:
      glob: $(inputs.outfile.path)
