#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3.dev2"

class: CommandLineTool
baseCommand: ["python"]

requirements:
  - $import: envvar-global.cwl
  - $import: linux-sort-docker.cwl
  - class: InlineJavascriptRequirement

description: |
  Generate inverted index of word to line

inputs:


- id: mainfile
  type: File
  inputBinding:
    position: 1

- id: index.py
  type: File
  default:
    class: File
    path: index.py
  inputBinding:
    position: 0


outputs:
  []