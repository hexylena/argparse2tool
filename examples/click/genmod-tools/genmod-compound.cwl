#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2cwl ver. 0.3.0
# To generate again: $ genmod --generate_cwl_tool
# Help: $ genmod --help_arg2cwl

cwlVersion: "cwl:v1.0"

class: CommandLineTool
baseCommand: ['genmod', 'compound']

description: |
  Score compound variants in a vcf file based on their rank score.

inputs:
  
  variant_file:
    type: File
  
    description: <vcf_file> or -
    inputBinding:
      position: 1

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

  processes:
    type: ["null", int]
    default: 4
    description: Define how many processes that should be use for annotation.
    inputBinding:
      prefix: --processes 

  temp_dir:
    type: ["null", string]
    description: Path to tempdir
    inputBinding:
      prefix: --temp_dir 

  vep:
    type: ["null", boolean]
    default: False
    description: If variants are annotated with the Variant Effect Predictor.
    inputBinding:
      prefix: --vep 


outputs:

  outfile_out:
    type: File
  
    description: Specify the path to a file where results should be stored.
    outputBinding:
      glob: $(inputs.outfile.path)
