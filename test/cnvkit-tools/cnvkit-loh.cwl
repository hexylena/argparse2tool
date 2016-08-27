#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'loh']

requirements:
  - class: InlineJavascriptRequirement

description: |
  [DEPRECATED] Plot allelic frequencies at each variant position in a VCF file.
  
      Divergence from 0.5 indicates loss of heterozygosity in a tumor sample.
  
      Instead, use the command "scatter -v".
      

inputs:


- id: variants
  type: string

  description: Sample variants in VCF format.
  inputBinding:
    position: 1


- id: segment
  type: ["null", string]
  description: Segmentation calls (.cns), the output of the 'segment' command.
  inputBinding:
    position: 2
    prefix: --segment 

- id: min_depth
  type: ["null", int]
  default: 20
  description: Minimum read depth for a variant to be displayed.
                [Default - %(default)s]
  inputBinding:
    position: 3
    prefix: --min-depth 

- id: sample_id
  type: ["null", string]
  description: Sample name to use for LOH calculations from the input VCF.
  inputBinding:
    position: 4
    prefix: --sample-id 

- id: normal_id
  type: ["null", string]
  description: Corresponding normal sample ID in the input VCF.
  inputBinding:
    position: 5
    prefix: --normal-id 

- id: trend
  type: ["null", boolean]
  default: True
  description: Draw a smoothed local trendline on the scatter plot.
  inputBinding:
    position: 6
    prefix: --trend 

- id: output
  type: ["null", string]
  description: Output PDF file name.
  inputBinding:
    position: 7
    prefix: --output 
outputs:
    []
