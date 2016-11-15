#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2tool ver. 0.3.0
# To generate again: $ cnvkit.py batch -go --generate_cwl_tool
# Help: $ cnvkit.py batch  --help_arg2cwl

cwlVersion: "cwl:v1.0"

class: CommandLineTool
baseCommand: ['cnvkit.py', 'batch']

description: |
  Run the complete CNVkit pipeline on one or more BAM files.

inputs:
  
  bam_files:
    type:
    - "null"
    - type: array
      items: string
  
    description: Mapped sequence reads (.bam)
    inputBinding:
      position: 1

  male_reference:
    type: ["null", boolean]
    default: False
    description: Use or assume a male reference (i.e. female samples will have +1 log-CNR of chrX; otherwise male samples would have -1 chrX).
    inputBinding:
      prefix: --male-reference 

  count_reads:
    type: ["null", boolean]
    default: False
    description: Get read depths by counting read midpoints within each bin. (An alternative algorithm).
    inputBinding:
      prefix: --count-reads 

  processes:
    type: ["null", int]
    default: 1
    description: Number of subprocesses used to running each of the BAM files in parallel. Give 0 or a negative value to use the maximum number of available CPUs. [Default - process each BAM in serial]
    inputBinding:
      prefix: --processes 

  rlibpath:
    type: ["null", str]
    description: Path to an alternative site-library to use for R packages.
    inputBinding:
      prefix: --rlibpath 

  normal:
    type:
    - "null"
    - type: array
      items: string
  
    description: Normal samples (.bam) to construct the pooled reference. If this option is used but no files are given, a "flat" reference will be built.
    inputBinding:
      prefix: --normal 

  fasta:
    type: ["null", str]
    description: Reference genome, FASTA format (e.g. UCSC hg19.fa)
    inputBinding:
      prefix: --fasta 

  targets:
    type: ["null", str]
    description: Target intervals (.bed or .list)
    inputBinding:
      prefix: --targets 

  antitargets:
    type: ["null", str]
    description: Antitarget intervals (.bed or .list)
    inputBinding:
      prefix: --antitargets 

  annotate:
    type: ["null", str]
    description: UCSC refFlat.txt or ensFlat.txt file for the reference genome. Pull gene names from this file and assign them to the target regions.
    inputBinding:
      prefix: --annotate 

  short_names:
    type: ["null", boolean]
    default: False
    description: Reduce multi-accession bait labels to be short and consistent.
    inputBinding:
      prefix: --short-names 

  split:
    type: ["null", boolean]
    default: False
    description: Split large tiled intervals into smaller, consecutive targets.
    inputBinding:
      prefix: --split 

  target_avg_size:
    type: ["null", int]
    description: Average size of split target bins (results are approximate).
    inputBinding:
      prefix: --target-avg-size 

  access:
    type: ["null", str]
    description: Regions of accessible sequence on chromosomes (.bed), as output by the 'access' command.
    inputBinding:
      prefix: --access 

  antitarget_avg_size:
    type: ["null", int]
    description: Average size of antitarget bins (results are approximate).
    inputBinding:
      prefix: --antitarget-avg-size 

  antitarget_min_size:
    type: ["null", int]
    description: Minimum size of antitarget bins (smaller regions are dropped).
    inputBinding:
      prefix: --antitarget-min-size 

  output_reference:
    type: ["null", str]
    description: Output filename/path for the new reference file being created. (If given, ignores the -o/--output-dir option and will write the file to the given path. Otherwise, "reference.cnn" will be created in the current directory or specified output directory.) 
    inputBinding:
      prefix: --output-reference 

  reference:
    type: ["null", str]
    description: Copy number reference file (.cnn).
    inputBinding:
      prefix: --reference 

  output_dir:
    type: ["null", str]
    default: .
    description: Output directory.
    inputBinding:
      prefix: --output-dir 

  scatter:
    type: ["null", boolean]
    default: False
    description: Create a whole-genome copy ratio profile as a PDF scatter plot.
    inputBinding:
      prefix: --scatter 

  diagram:
    type: ["null", boolean]
    default: False
    description: Create a diagram of copy ratios on chromosomes as a PDF.
    inputBinding:
      prefix: --diagram 


outputs:

  output_reference_out:
    type: File
  
    description: Output filename/path for the new reference file being created. (If given, ignores the -o/--output-dir option and will write the file to the given path. Otherwise, "reference.cnn" will be created in the current directory or specified output directory.) 
    outputBinding:
      glob: $(inputs.output_reference.path)

  output_dir_out:
    type: File
    default: . 
    description: Output directory.
    outputBinding:
      glob: $(inputs.output_dir.path)
