#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'export', 'theta']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Convert segments to THetA2 input file format (*.input).

inputs:


- id: tumor_segment
  type: string

  description: Tumor-sample segmentation file from CNVkit (.cns).
  inputBinding:
    position: 1


- id: normal_reference
  type: ["null", string]
  description: Reference copy number profile (.cnn), or normal-sample bin-level
                log2 copy ratios (.cnr). [DEPRECATED]
  inputBinding:
    position: 2


- id: reference
  type: ["null", string]
  description: Reference copy number profile (.cnn), or normal-sample bin-level
                log2 copy ratios (.cnr). Use if the tumor_segment input file
                does not contain a "weight" column.
  inputBinding:
    position: 3
    prefix: --reference 

- id: vcf
  type: ["null", string]
  description: VCF file containing SNVs observed in both the tumor and normal
                samples. Tumor sample ID should match the `tumor_segment`
                filename or be specified with -i/--sample-id.
  inputBinding:
    position: 4
    prefix: --vcf 

- id: sample_id
  type: ["null", string]
  description: Specify the name of the tumor sample in the VCF (given with
                -v/--vcf). [Default - taken the tumor_segment file name]
  inputBinding:
    position: 5
    prefix: --sample-id 

- id: normal_id
  type: ["null", string]
  description: Corresponding normal sample ID in the input VCF.
  inputBinding:
    position: 6
    prefix: --normal-id 

- id: min_depth
  type: ["null", int]
  default: 20
  description: Minimum read depth for a SNP in the VCF to be counted.
                [Default - %(default)s]
  inputBinding:
    position: 7
    prefix: --min-depth 

- id: output
  type: ["null", string]
  description: Output file name.
  inputBinding:
    position: 8
    prefix: --output 
outputs:
    []
