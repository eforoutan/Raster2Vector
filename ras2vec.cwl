class: CommandLineTool
hints:
  NetworkAccess:
    networkAccess: true
  DockerRequirement:
    dockerPull: eforoutan/ras2vec:latest
inputs:
  input_raster:
    type: File
    inputBinding:
      position: 1
  rounding_precision:
    type: string
    inputBinding:
      position: 2
  geojson_file_name:
    type: string
    default: default.json
    inputBinding:
      position: 3
  csv_file_name:
    type: string
    default: default.csv
    inputBinding:
      position: 4
outputs:
  output_csv:
    type: File
    outputBinding:
      glob: "$(inputs.csv_file_name)"
  output_geojson:
    type: File
    outputBinding:
      glob: "$(inputs.geojson_file_name)"
cwlVersion: v1.2
