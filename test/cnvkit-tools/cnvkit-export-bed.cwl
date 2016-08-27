#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'export', 'bed']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Convert segments to BED format.
  
      Input is a segmentation file (.cns) where, preferably, log2 ratios have
      already been adjusted to integer absolute values using the 'call' command.
      

inputs:


- id: segments
  type:
    type: array
    items: string

  description: Segmented copy ratio data files (*.cns), the output of the
                'segment' or 'call' sub-commands.
  inputBinding:
    position: 1


- id: sample_id
  type: ["null", string]
  description: Identifier to write in the 4th column of the BED file.
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

- id: show
  type:
  - "null"
  - type: enum
    symbols: ['ploidy', 'variant', 'all']
  default: ploidy
  description: Which segmented regions to show -
                'all' = all segment regions;
                'variant' = CNA regions with non-neutral copy number;
                'ploidy' = CNA regions with non-default ploidy.
                [Default - %(default)s]
  inputBinding:
    position: 5
    prefix: --show 

- id: show_all
  type: ["null", boolean]
  default: True
  description: Write all segmented regions.
                [DEPRECATED; use "--show all" instead]
  inputBinding:
    position: 6
    prefix: --show-all 

- id: male_reference
  type: ["null", boolean]
  default: True
  description: Was a male reference used?  If so, expect half ploidy on
                chrX and chrY; otherwise, only chrY has half ploidy.  In CNVkit,
                if a male reference was used, the "neutral" copy number (ploidy)
                of chrX is 1; chrY is haploid for either gender reference.
  inputBinding:
    position: 7
    prefix: --male-reference 

- id: output
  type: ["null", string]
  description: Output file name.
  inputBinding:
    position: 8
    prefix: --output 
outputs:
    []
