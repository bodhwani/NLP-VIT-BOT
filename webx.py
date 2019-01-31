import subprocess

print ("training nlu")
return_code1 = subprocess.call("python -m rasa_nlu.train -c nlu_config.yml --data data/nlu -o models --fixed_model_name nlu --project current --verbose", shell=True)

print ("training core")
return_code2 = subprocess.call("python -m rasa_core.train -d domain.yml -s data/stories -o models/current/dialogue -c policies.yml", shell=True)


print ("executing")
return_code3 = subprocess.call("python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --enable_api", shell=True)
