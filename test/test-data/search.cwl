- id: search
  class: CommandLineTool
  baseCommand: python
  requirements:
    - class: InlineJavascriptRequirement
  inputs:
    - id: file
      type: File
      inputBinding:
        position: 1
      secondaryFiles:
        - ".idx1"
        - "^.idx2"
        - '$(self.path+".idx3")'
        - '$({"path": self.path+".idx4", "class": "File"})'
        - '${ return self.path+".idx5"; }'
    - id: search.py
      type: File
      default:
        class: File
        path: search.py
      inputBinding:
        position: 0
    - id: term
      type: string
      inputBinding:
        position: 2
  outputs:
    - id: result
      type: File
      outputBinding:
        glob: result.txt
  stdout: result.txt