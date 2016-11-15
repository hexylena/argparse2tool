#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool ver. 0.3.0
# To generate again: $ genmod --generate_cwl_tool
# Help: $ genmod --help_arg2cwl

cwlVersion: "cwl:v1.0"

class: CommandLineTool
baseCommand: ['genmod', 'sort']

description: |
  Sort a VCF file based on rank score.

inputs:
  
  variant_file:
    type: File
  
    description: <vcf_file> or -
    inputBinding:
      position: 1

  outfile:
    type: ["null", File]
    description: Specify the path to a file where results should be stored.
    inputBinding:
      prefix: --outfile 

  family_id:
    type: ["null", string]
    description: Specify the family id for sorting.
    inputBinding:
      prefix: --family_id 

  silent:
    type: ["null", boolean]
    default: False
    description: Do not print the variants.
    inputBinding:
      prefix: --silent 

  temp_dir:
    type: ["null", string]
    description: Path to tempdir
    inputBinding:
      prefix: --temp_dir 

  position:
    type: ["null", boolean]
    default: False
    description: If variants should be sorted by position.
    inputBinding:
      prefix: --position 


outputs:

  outfile_out:
    type: File
  
    description: Specify the path to a file where results should be stored.
    outputBinding:
      glob: $(inputs.outfile.path)
