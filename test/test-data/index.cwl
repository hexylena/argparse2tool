cwlVersion: cwl:draft-3
class: CommandLineTool
baseCommand: python
requirements:
- class: CreateFileRequirement
  fileDef:
    - filename: input.txt
      fileContent: $(inputs.file)

inputs:
- id: file
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
- id: result
  type: File
  outputBinding:
    glob: input.txt
  secondaryFiles:
    - ".idx1"
    - "^.idx2"