#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool ver. 0.3.0
# To generate again: $ genmod --generate_cwl_tool
# Help: $ genmod --help_arg2cwl

cwlVersion: "cwl:v1.0"

class: CommandLineTool
baseCommand: ['genmod', 'score']

description: |
  Score variants in a vcf file using a Weighted Sum Model.
  
  The specific scores should be defined in a config file, see examples on 
  github.

inputs:
  
  variant_file:
    type: File
  
    description: <vcf_file> or -
    inputBinding:
      position: 1

  family_id:
    type: ["null", string]
    default: 1
  
    inputBinding:
      prefix: --family_id 

  family_file:
    type: ["null", File]
  
    inputBinding:
      prefix: --family_file 

  family_type:
    type:
    - "null"
    - type: enum
      symbols: []
    default: ped
    description: If the analysis use one of the known setups, please specify which one.
    inputBinding:
      prefix: --family_type 

  silent:
    type: ["null", boolean]
    default: False
    description: Do not print the variants.
    inputBinding:
      prefix: --silent 

  skip_plugin_check:
    type: ["null", boolean]
    default: False
    description: If continue even if plugins does not exist in vcf.
    inputBinding:
      prefix: --skip_plugin_check 

  rank_results:
    type: ["null", boolean]
    default: False
    description: Add a info field that shows how the different categories contribute to the rank score.
    inputBinding:
      prefix: --rank_results 

  outfile:
    type: ["null", File]
    description: Specify the path to a file where results should be stored.
    inputBinding:
      prefix: --outfile 

  score_config:
    type: ["null", string]
    description: The plug-in config file(.ini)
    inputBinding:
      prefix: --score_config 


outputs:

  outfile_out:
    type: File
  
    description: Specify the path to a file where results should be stored.
    outputBinding:
      glob: $(inputs.outfile.path)
