#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool ver. 0.3.0
# To generate again: $ genmod --generate_cwl_tool
# Help: $ genmod --help_arg2cwl

cwlVersion: "cwl:v1.0"

class: CommandLineTool
baseCommand: ['genmod', 'models']

description: |
  Annotate genetic models for vcf variants. 
  
  Checks what patterns of inheritance that are followed in a VCF file.
  The analysis is family based so each family that are specified in the family
  file and exists in the variant file will get it's own annotation.

inputs:
  
  variant_file:
    type: File
  
    description: <vcf_file> or -
    inputBinding:
      position: 1

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

  reduced_penetrance:
    type: ["null", File]
    description: File with gene ids that have reduced penetrance.
    inputBinding:
      prefix: --reduced_penetrance 

  vep:
    type: ["null", boolean]
    default: False
    description: If variants are annotated with the Variant Effect Predictor.
    inputBinding:
      prefix: --vep 

  phased:
    type: ["null", boolean]
    default: False
    description: If data is phased use this flag.
    inputBinding:
      prefix: --phased 

  strict:
    type: ["null", boolean]
    default: False
    description: If strict model annotations should be used(see documentation).
    inputBinding:
      prefix: --strict 

  processes:
    type: ["null", int]
    default: 4
    description: Define how many processes that should be use for annotation.
    inputBinding:
      prefix: --processes 

  silent:
    type: ["null", boolean]
    default: False
    description: Do not print the variants.
    inputBinding:
      prefix: --silent 

  whole_gene:
    type: ["null", boolean]
    default: False
    description: If compounds should be checked over the whole gene.
    inputBinding:
      prefix: --whole_gene 

  keyword:
    type: ["null", string]
    default: Annotation
    description: What annotation keyword that should be used when searching for features.
    inputBinding:
      prefix: --keyword 

  outfile:
    type: ["null", File]
    description: Specify the path to a file where results should be stored.
    inputBinding:
      prefix: --outfile 

  temp_dir:
    type: ["null", string]
    description: Path to tempdir
    inputBinding:
      prefix: --temp_dir 


outputs:

  outfile_out:
    type: File
  
    description: Specify the path to a file where results should be stored.
    outputBinding:
      glob: $(inputs.outfile.path)
