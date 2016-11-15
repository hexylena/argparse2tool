#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool ver. 0.3.0
# To generate again: $ genmod --generate_cwl_tool
# Help: $ genmod --help_arg2cwl

cwlVersion: "cwl:v1.0"

class: CommandLineTool
baseCommand: ['genmod', 'annotate']

description: |
  Annotate vcf variants.
  
  Annotate variants with a number of different sources.
  Please use --help for more info.

inputs:
  
  variant_file:
    type: File
  
    description: <vcf_file> or -
    inputBinding:
      position: 1

  annotate_regions:
    type: ["null", boolean]
    default: False
    description: Increase output verbosity.
    inputBinding:
      prefix: --annotate_regions 

  cadd_file:
    type: ["null", string]
    description: Specify the path to a bgzipped cadd file (with index) with variant scores. This command can be used multiple times if multiple cadd files.
    inputBinding:
      prefix: --cadd_file 

  thousand_g:
    type: ["null", string]
    description: Specify the path to a bgzipped vcf file (with index) with 1000g variants
    inputBinding:
      prefix: --thousand_g 

  exac:
    type: ["null", string]
    description: Specify the path to a bgzipped vcf file (with index) with exac variants.
    inputBinding:
      prefix: --exac 

  cosmic:
    type: ["null", string]
    description: Specify the path to a bgzipped vcf file (with index) with COSMIC variants.
    inputBinding:
      prefix: --cosmic 

  max_af:
    type: ["null", boolean]
    default: False
    description: If the MAX AF should be annotated
    inputBinding:
      prefix: --max_af 

  spidex:
    type: ["null", string]
    description: Specify the path to a bgzipped tsv file (with index) with spidex information.
    inputBinding:
      prefix: --spidex 

  annotation_dir:
    type: ["null", string]
    default: /usr/local/lib/python2.7/dist-packages/genmod/annotations
    description: Specify the path to the directory where the annotation databases are. Default is the gene pred files that comes with the distribution.
    inputBinding:
      prefix: --annotation_dir 

  cadd_raw:
    type: ["null", boolean]
    default: False
    description: If the raw cadd scores should be annotated.
    inputBinding:
      prefix: --cadd_raw 

  processes:
    type: ["null", int]
    default: 4
    description: Define how many processes that should be use for annotation.
    inputBinding:
      prefix: --processes 

  outfile:
    type: ["null", File]
    description: Specify the path to a file where results should be stored.
    inputBinding:
      prefix: --outfile 

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


outputs:

  outfile_out:
    type: File
  
    description: Specify the path to a file where results should be stored.
    outputBinding:
      glob: $(inputs.outfile.path)
