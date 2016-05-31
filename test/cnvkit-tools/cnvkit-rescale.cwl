#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'rescale']

requirements:
  - class: InlineJavascriptRequirement

description: |
  [DEPRECATED] Rescale segment copy ratios given known purity and ploidy.
  
      Instead, use the command "call -m none".
      

inputs:


- id: filename
  type: string

  description: Copy ratios (.cnr or .cns).
  inputBinding:
    position: 1


- id: center
  type:
  - "null"
  - type: enum
    symbols: ['mean', 'median', 'mode', 'biweight']
  description: Re-center the log2 ratio values using this estimate of the
                center or average value.
  inputBinding:
    position: 2
    prefix: --center 

- id: ploidy
  type: ["null", int]
  default: 2
  description: Ploidy of the sample cells. [Default - %(default)d]
  inputBinding:
    position: 3
    prefix: --ploidy 

- id: purity
  type: ["null", float]
  description: Estimated tumor cell fraction, a.k.a. purity or cellularity.
  inputBinding:
    position: 4
    prefix: --purity 

- id: gender
  type:
  - "null"
  - type: enum
    symbols: ['m', 'male', 'Male', 'f', 'female', 'Female']
  description: Specify the sample's gender as male or female. (Otherwise
                guessed from chrX copy number).
  inputBinding:
    position: 5
    prefix: --gender 

- id: male_reference
  type: ["null", boolean]
  default: True
  description: Was a male reference used?  If so, expect half ploidy on
                chrX and chrY; otherwise, only chrY has half ploidy.  In CNVkit,
                if a male reference was used, the "neutral" copy number (ploidy)
                of chrX is 1; chrY is haploid for either gender reference.
  inputBinding:
    position: 6
    prefix: --male-reference 

- id: output
  type: ["null", string]
  description: Output table file name (CNR-like table of segments, .cns).
  inputBinding:
    position: 7
    prefix: --output 
outputs:
    []
