#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'export', 'vcf']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Convert segments to VCF format.
  
      Input is a segmentation file (.cns) where, preferably, log2 ratios have
      already been adjusted to integer absolute values using the 'call' command.
      

inputs:


- id: segments
  type: string

  description: Segmented copy ratio data file (*.cns), the output of the
                'segment' or 'call' sub-commands.
  inputBinding:
    position: 1


- id: sample_id
  type: ["null", string]
  description: Sample name to write in the genotype field of the output VCF file.
                [Default - use the sample ID, taken from the file name]
  inputBinding:
    position: 2
    prefix: --sample-id 

- id: ploidy
  type: ["null", int]
  default: 2
  description: Ploidy of the sample cells. [Default - %(default)d]
  inputBinding:
    position: 3
    prefix: --ploidy 

- id: gender
  type:
  - "null"
  - type: enum
    symbols: ['m', 'male', 'Male', 'f', 'female', 'Female']
  description: Specify the sample's gender as male or female. (Otherwise
                guessed from chrX copy number).
  inputBinding:
    position: 4
    prefix: --gender 

- id: male_reference
  type: ["null", boolean]
  default: True
  description: Was a male reference used?  If so, expect half ploidy on
                chrX and chrY; otherwise, only chrY has half ploidy.  In CNVkit,
                if a male reference was used, the "neutral" copy number (ploidy)
                of chrX is 1; chrY is haploid for either gender reference.
  inputBinding:
    position: 5
    prefix: --male-reference 

- id: output
  type: ["null", string]
  description: Output file name.
  inputBinding:
    position: 6
    prefix: --output 
outputs:
    []
