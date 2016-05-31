#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'fix']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Combine target and antitarget coverages and correct for biases.
  
      Adjust raw coverage data according to the given reference, correct potential
      biases and re-center.
      

inputs:


- id: target
  type: string

  description: Target coverage file (.targetcoverage.cnn).
  inputBinding:
    position: 1


- id: antitarget
  type: string

  description: Antitarget coverage file (.antitargetcoverage.cnn).
  inputBinding:
    position: 2


- id: reference
  type: string

  description: Reference coverage (.cnn).
  inputBinding:
    position: 3


- id: do_gc
  type: ["null", boolean]
  description: Skip GC correction.
  inputBinding:
    position: 4
    prefix: --no-gc 

- id: do_edge
  type: ["null", boolean]
  description: Skip edge-effect correction.
  inputBinding:
    position: 5
    prefix: --no-edge 

- id: do_rmask
  type: ["null", boolean]
  description: Skip RepeatMasker correction.
  inputBinding:
    position: 6
    prefix: --no-rmask 

- id: output
  type: ["null", string]
  description: Output file name.
  inputBinding:
    position: 7
    prefix: --output 
outputs:
    []
