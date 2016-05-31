#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'reference']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Compile a coverage reference from the given files (normal samples).

inputs:


- id: references
  type:
  - "null"
  - type: array
    items: string

  description: Normal-sample target or antitarget .cnn files, or the
                directory that contains them.
  inputBinding:
    position: 1


- id: fasta
  type: ["null", string]
  description: Reference genome, FASTA format (e.g. UCSC hg19.fa)
  inputBinding:
    position: 2
    prefix: --fasta 

- id: targets
  type: ["null", string]
  description: Target intervals (.bed or .list)
  inputBinding:
    position: 3
    prefix: --targets 

- id: antitargets
  type: ["null", string]
  description: Antitarget intervals (.bed or .list)
  inputBinding:
    position: 4
    prefix: --antitargets 

- id: male_reference
  type: ["null", boolean]
  default: True
  description: Create a male reference - shift female samples' chrX
                log-coverage by -1, so the reference chrX average is -1.
                Otherwise, shift male samples' chrX by +1, so the reference chrX
                average is 0.
  inputBinding:
    position: 5
    prefix: --male-reference 

- id: do_gc
  type: ["null", boolean]
  description: Skip GC correction.
  inputBinding:
    position: 6
    prefix: --no-gc 

- id: do_edge
  type: ["null", boolean]
  description: Skip edge-effect correction.
  inputBinding:
    position: 7
    prefix: --no-edge 

- id: do_rmask
  type: ["null", boolean]
  description: Skip RepeatMasker correction.
  inputBinding:
    position: 8
    prefix: --no-rmask 

- id: output
  type: ["null", string]
  description: Output file name.
  inputBinding:
    position: 9
    prefix: --output 
outputs:
    []
