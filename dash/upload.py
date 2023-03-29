import requests
import glob
import os
from fhirclient.models.parameters import Parameters, ParametersParameter #https://github.com/smart-on-fhir/client-py

def generate_import_parameters(import_folder, profile, resource, mode):
    param_resource = Parameters()

    param_resource_type = ParametersParameter()
    param_resource_type.name= 'resourceType'
    param_resource_type.valueCode = resource

    param_url = {}
    param_url['name'] = 'url'
    param_url['valueUrl'] = f'{import_folder}/{profile}'
    print(param_url['valueUrl'])
    param_mode = ParametersParameter()
    param_mode.name= 'mode'
    param_mode.valueCode = mode

    param_source = ParametersParameter()
    param_source.name = 'source'
    param_source.part = [param_resource_type, param_url, param_mode]
    param_resource.parameter = [param_source]
    
    return param_resource.as_json()

def post_import_ndjson(server, param):
    url = f'{server}/$import'

    resp = requests.post(url,  json = param, headers={"Content-Type": "application/fhir+json"} )
    return resp 


## Get all files in the import folder
import_folder = '/usr/share/staging/fhir' 
server = 'http://pathling:8080/fhir'

# Specify the folder path and pattern for the files you want to list
file_pattern = '*.ndjson'

# Construct the full pattern with folder path and file pattern
full_pattern = os.path.join(import_folder, file_pattern)

# Get the list of all files matching the pattern
files = glob.glob(full_pattern)

# Extract the file names from the file paths
file_names = [os.path.basename(file_path) for file_path in files]

# Get the resource type from the file name
resources = [file_name.split('.')[0] for file_name in file_names]

mode = 'merge' # overwrite for fresh load (but not really since need to merge Observations not overwrite)

for resource, file in zip(resources, file_names):
    param = generate_import_parameters('file://' + import_folder, file, resource, mode)
    resp = post_import_ndjson(server, param)
    print(f"{resource}: {resp.json()['issue'][0]['diagnostics']}")

print('Everything imported OK')