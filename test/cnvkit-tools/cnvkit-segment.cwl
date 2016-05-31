#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'segment']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Infer copy number segments from the given coverage table.

inputs:


- id: filename
  type: string

  description: Bin-level log2 ratios (.cnr file), as produced by 'fix'.
  inputBinding:
    position: 1


- id: output
  type: ["null", string]
  description: Output table file name (CNR-like table of segments, .cns).
  inputBinding:
    position: 2
    prefix: --output 

- id: dataframe
  type: ["null", string]
  description: File name to save the raw R dataframe emitted by CBS or
                Fused Lasso. (Useful for debugging.)
  inputBinding:
    position: 3
    prefix: --dataframe 

- id: method
  type:
  - "null"
  - type: enum
    symbols: ['cbs', 'haar', 'flasso']
  default: cbs
  description: Segmentation method (CBS, HaarSeg, or Fused Lasso).
                [Default - %(default)s]
  inputBinding:
    position: 4
    prefix: --method 

- id: threshold
  type: ["null", float]
  description: Significance threshold (p-value or FDR, depending on method) to
                accept breakpoints during segmentation.
  inputBinding:
    position: 5
    prefix: --threshold 

- id: vcf
  type: ["null", string]
  description: VCF file name containing variants for segmentation by allele
                frequencies.
  inputBinding:
    position: 6
    prefix: --vcf 

- id: drop_low_coverage
  type: ["null", boolean]
  default: True
  description: Drop very-low-coverage bins before segmentation to avoid
                false-positive deletions in poor-quality tumor samples.
  inputBinding:
    position: 7
    prefix: --drop-low-coverage 

- id: drop_outliers
  type: ["null", float]
  default: 10
  description: Drop outlier bins more than this many multiples of the 95th
                quantile away from the average within a rolling window.
                Set to 0 for no outlier filtering.
                [Default - %(default)g]
  inputBinding:
    position: 8
    prefix: --drop-outliers 

- id: rlibpath
  type: ["null", string]
  description: Path to an alternative site-library to use for R packages.
  inputBinding:
    position: 9
    prefix: --rlibpath 
outputs:
    []
