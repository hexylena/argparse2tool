#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'export', 'nexus-ogt']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Convert log2 ratios and b-allele freqs to Nexus "Custom-OGT" format.

inputs:


- id: filename
  type: string

  description: Log2 copy ratio data file (*.cnr), the output of the 'fix'
                sub-command.
  inputBinding:
    position: 1


- id: vcf
  type: string

  description: VCF of SNVs for the same sample, to calculate b-allele
                frequencies.
  inputBinding:
    position: 2


- id: sample_id
  type: ["null", string]
  description: Specify the name of the sample in the VCF to use to extract
                b-allele frequencies.
  inputBinding:
    position: 3
    prefix: --sample-id 

- id: min_variant_depth
  type: ["null", int]
  default: 20
  description: Minimum read depth for a SNV to be included in the b-allele
                frequency calculation. [Default - %(default)s]
  inputBinding:
    position: 4
    prefix: --min-variant-depth 

- id: min_weight
  type: ["null", float]
  description: Minimum weight (between 0 and 1) for a bin to be included in
                the output. [Default - %(default)s]
  inputBinding:
    position: 5
    prefix: --min-weight 

- id: output
  type: ["null", string]
  description: Output file name.
  inputBinding:
    position: 6
    prefix: --output 
outputs:
    []
