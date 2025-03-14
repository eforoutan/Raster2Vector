cwlVersion: v1.2
class: CommandLineTool
 
hints:
  DockerRequirement:
    dockerPull: "eforoutan/ras2vec:latest"
  NetworkAccess:
    networkAccess: true
 
inputs:

  input_raster:
    type: File
    inputBinding:
      position: 1
 
  rounding_precision:
    type: string
    inputBinding:
      position: 2
 
outputs:
  output_geojson:
    type: File
    outputBinding:
      glob: "vectorized_output.geojson"
 
  output_csv:
    type: File
    outputBinding:
      glob: "vectorized_output.csv"