#!/usr/bin/env python

import os
import sys
import json
import subprocess

# if no arguments provided, test if engine is supported on local system
if len(sys.argv) == 1:
    # Python engine is always supported since its required to run liveset itself
    sys.exit(0)

# check for correct number of arguments
if len(sys.argv) < 4:
    print(f"ERROR: run.py: insufficient arguments Usage <scenario_file> <params_json> <output_dir>")
    sys.exit(1)
# scenario is the first argument
scenario_file = sys.argv[1]
if not os.path.exists(scenario_file):
    print(f"ERROR: run.py: could not find scenario file ({scenario_file})")
    sys.exit(1)  
# params.json is the second argument
params_json = sys.argv[2]
params_dict = {}
if not os.path.exists(params_json):
    print(f"ERROR: run.py: file ({params_json}) does not exist")
    sys.exit(1)
try:
    with open(params_json, 'r') as f:
        params_dict = json.load(f)
except json.JSONDecodeError:
    print(f"ERROR: run.py: input json ({params_json}) containts invalid JSON format")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: run.py: input json ({params_json}) unknown error in loading data: {e}")
    sys.exit(1)
args = []
for key, value in params_dict.items():
    args.append(f"--{key}={value}")
# output dir for dataset is the third argument
output_dir = sys.argv[3]
if not os.path.isdir(output_dir):
    print(f"ERROR: run.py: could not find output dir ({output_dir})")
    sys.exit(1)    
# run command
command = ['python', scenario_file]
command += args
print(f"run.py: running command: {command}")
sys.stdout.flush()
sys.stderr.flush()
result = subprocess.run(command, cwd=output_dir, text=True)
sys.stdout.flush()
sys.stderr.flush()
sys.exit(result)