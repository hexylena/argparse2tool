#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3.dev2"

class: CommandLineTool
baseCommand: ["python"]

requirements:
  - $import: envvar-global.cwl
  - $import: linux-sort-docker.cwl
  - class: InlineJavascriptRequirement

description: |
  Toy program to search inverted index and print out each line the term appears

inputs:


- id: mainfile
  type: File
  inputBinding:
    position: 1

- id: term
  type: string
  inputBinding:
    position: 2

- id: search.py
  type: File
  default:
    class: File
    path: search.py
  inputBinding:
    position: 0


outputs:
  []