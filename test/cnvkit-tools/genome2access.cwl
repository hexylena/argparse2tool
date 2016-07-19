#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3.dev2"

class: CommandLineTool
baseCommand: ["python"]

requirements:
  - class: InlineJavascriptRequirement

description: |
  List the locations of accessible sequence regions in a FASTA file.
  
  Inaccessible regions, e.g. telomeres and centromeres, are masked out with N in
  the reference genome sequence; this script scans those to identify the
  coordinates of the accessible regions (those between the long spans of N's).
  
  DEPRECATED -- use "cnvkit.py access" instead.
  

inputs:

- id: fa_fname
  type: string
  description: Genome FASTA file name
  inputBinding:
    position: 1

- id: min_gap_size
  type: int
  default: 5000
  description: Minimum gap size between accessible sequence
                regions.  Regions separated by less than this distance will
                be joined together. [Default- %(default)s]
  inputBinding:
    position: 2

- id: exclude
  type: 
    type: array
    items: string
  description: Additional regions to exclude, in BED format. Can be
                used multiple times.
  inputBinding:
    position: 3

- id: output
  type: File
  description: Output file name
  inputBinding:
    position: 4
- id: genome2access.py
  type: File
  default:
    class: File
    path: genome2access.py
  inputBinding:
    position: 0

outputs:
- id: output_out
  type: File
  description: Output file name
  outputBinding:
    glob: $(inputs.output.path)
