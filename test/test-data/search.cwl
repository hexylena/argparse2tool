#!/usr/bin/env cwl-runner
# This tool description was formed automatically by argparse2tool ver. 0.2.5
# To form again: $ python --generate_cwl_tool
# Help: $ python --help_arg2cwl

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['python']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Toy program to search inverted index and print out each line the term appears

inputs:
  
- id: search.py
  type: File
  default:
    class: File
    path: search.py
  inputBinding:
    position: 0


- id: mainfile
  type: File

  description: Text file to be indexed
  inputBinding:
    position: 1

- id: term
  type: string

  description: Term for search
  inputBinding:
    position: 2

outputs:
    []
