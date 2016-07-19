#!/usr/bin/env cwl-runner

cwlVersion: "cwl:draft-3"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'version']

requirements:
  - class: InlineJavascriptRequirement

description: |
  Display this program's version.

inputs:

outputs:
    []
