#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'segmetrics']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Compute segment-level metrics from bin-level log2 ratios.

inputs:


- id: cnarray
  type: string

  description: Bin-level copy ratio data file (*.cnn, *.cnr).
  inputBinding:
    position: 1


- id: segments
  type: string

  description: Segmentation data file (*.cns, output of the 'segment' command).
  inputBinding:
    position: 2
    prefix: --segments 

- id: drop_low_coverage
  type: ["null", boolean]
  default: True
  description: Drop very-low-coverage bins before segmentation to avoid
                false-positive deletions in poor-quality tumor samples.
  inputBinding:
    position: 3
    prefix: --drop-low-coverage 

- id: output
  type: ["null", string]
  description: Output table file name.
  inputBinding:
    position: 4
    prefix: --output 

- id: stdev
  type: ["null", boolean]
  default: True
  description: Standard deviation.
  inputBinding:
    position: 5
    prefix: --stdev 

- id: mad
  type: ["null", boolean]
  default: True
  description: Median absolute deviation (standardized).
  inputBinding:
    position: 6
    prefix: --mad 

- id: iqr
  type: ["null", boolean]
  default: True
  description: Inter-quartile range.
  inputBinding:
    position: 7
    prefix: --iqr 

- id: bivar
  type: ["null", boolean]
  default: True
  description: Tukey's biweight midvariance.
  inputBinding:
    position: 8
    prefix: --bivar 

- id: ci
  type: ["null", boolean]
  default: True
  description: Confidence interval (by bootstrap).
  inputBinding:
    position: 9
    prefix: --ci 

- id: pi
  type: ["null", boolean]
  default: True
  description: Prediction interval.
  inputBinding:
    position: 10
    prefix: --pi 

- id: alpha
  type: ["null", float]
  default: 0.05
  description: Level to estimate confidence and prediction intervals;
                use with --ci and --pi. [Default - %(default)s]
  inputBinding:
    position: 11
    prefix: --alpha 

- id: bootstrap
  type: ["null", int]
  default: 100
  description: Number of bootstrap iterations to estimate confidence interval;
                use with --ci. [Default - %(default)d]
  inputBinding:
    position: 12
    prefix: --bootstrap 
outputs:
    []
