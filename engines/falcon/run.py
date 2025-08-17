# falcon/run.py requires env variables to be setup first:
# Set Falcon cloud token:
# export FALCON_CLOUD_TOKEN=<token>
# On Linux, set Falcon dir:
# export FALCON_DIR=<falconsim_dir>

import os
import sys
import platform
import json
import subprocess
import shutil
import time
import threading
import platform

end_logging = False

def logging(file):
    print(f"Monitoring falcon log file: {file}")
    seek_offset = 0
    while True:
        if end_logging:
            break
        if not os.path.exists(file):
            time.sleep(1)
            continue
        log_file = open(file, "r")
        log_file.seek(seek_offset, 0)
        line = log_file.readline()       
        if not line:
            log_file.close()
            time.sleep(1)
            continue
        seek_offset += len(line) 
        line = line.strip()        
        if line.find('LogDuPython:') >= 0:
            print(line)

# if no arguments provided, test if engine is supported on local system
if len(sys.argv) == 1:
    os_name = platform.system()
    if os_name != "Windows":
        print(f"ERROR: run.py: only supported on Windows")
        sys.exit(1)
    try:
        command = ['DuSim', '-RenderOffScreen', '-timeout=1']
        subprocess.run(command, text=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: run.py: executing command: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"ERROR: run.py: command not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: run.py: an unexpected error occurred: {e}")
        sys.exit(1)
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
current_platform = platform.platform()
dusim_cmd = None
if "Windows" in current_platform:
    log_dir = os.path.join(str(os.getenv('homedrive') + os.getenv('homepath')), 'AppData\\Local\\Falcon\\Logs')
    dusim_cmd = 'DuSim.exe'
else:
    log_dir = os.path.join(str(os.getenv('HOME')), '.config/Epic/Falcon/Logs')
    dusim_cmd = 'Falcon.sh'
print(f"scenario_file: {scenario_file}")
print(f"params_json: {params_json}")
print(f"log_dir: {log_dir}")
shutil.copy(params_json, log_dir)
# output dir for dataset is the third argument
output_dir = sys.argv[3]
print(f"output_dir: {output_dir}")
if not os.path.isdir(output_dir):
    print(f"ERROR: run.py: could not find output dir ({output_dir})")
    sys.exit(1)
if "Linux" in current_platform:
    # dir with Falcon binary, needs to be cwd for linux
    cmd_dir = os.getenv("FALCON_DIR")
    print(f"cd {cmd_dir}")
    os.chdir(cmd_dir)
print(f"cmd_dir: {cmd_dir}")
playerrole = 'Fixedbase_BP_C_0'
if 'playerrole' in params_dict:
    playerrole = params_dict['playerrole']
token = os.environ.get('FALCON_CLOUD_TOKEN')
if not token:
    print(f"ERROR: run.py: token must be defined")
    sys.exit(1)
# run command
command = [dusim_cmd,  
           str('-scenario=' + scenario_file),
           str('-playerrole=' + playerrole),   
           str('-token=' + token),
           '-RenderOffScreen', 
           '-log=falcon.log']
print(f"run.py: running command: {command}")
log_file = os.path.join(log_dir, 'falcon.log')
print(f"log_file: {log_file}")
thread = threading.Thread(target=logging, args=(log_file,))
thread.start()
try:
    sys.stdout.flush()
    sys.stderr.flush()
    falcon_env = os.environ.copy()
    falcon_env['output_dir'] = output_dir
    falcon_env['log_dir'] = log_dir
    result = subprocess.run(command, cwd=cmd_dir, text=True, env=falcon_env)
    sys.stdout.flush()
    sys.stderr.flush()
except subprocess.CalledProcessError as e:
    print(f"ERROR: run.py: executing command: {e}")
    end_logging = True
    sys.exit(1)
except FileNotFoundError as e:
    print(f"ERROR: run.py: command not found: {e}")
    end_logging = True
    sys.exit(1)
except Exception as e:
    print(f"ERROR: run.py: an unexpected error occurred: {e}")
    end_logging = True
    sys.exit(1)
end_logging = True
if os.path.exists(log_file):
    if os.path.exists(os.path.join(output_dir, "falcon.log")):
        os.remove(os.path.join(output_dir, "falcon.log"))
    shutil.move(log_file, output_dir)
sys.exit(0)
