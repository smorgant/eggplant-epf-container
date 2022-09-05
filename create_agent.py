#!/usr/bin/python3
import os, sys, requests, json, logging

print("Python Script starting")

response = requests.request("GETT", "http://169.254.170.2/v2/metadata/", headers=headers, data=payload)

response = json.loads(response.text)

os.system("echo '" + response , "'")

#Confirm that they all exist first before moving forward
if 'URL' not in os.environ:
        sys.exit("URL Env variable missing")

if 'WS' not in os.environ:
        sys.exit("WS Env variable missing")

if 'CLIENT_ID' not in os.environ:
        sys.exit("CLIENT_ID Env variable missing")

if 'CLIENT_SECRET' not in os.environ:
        sys.exit("CLIENT_SECRET Env variable missing")

if 'EXECUTION_ID' not in os.environ:
        sys.exit("EXECUTION_ID Env variable missing")

if 'LICENSER_HOST' not in os.environ:
        sys.exit("LICENSER_HOST Env variable missing")

# Print all the Env Variables to be used
logging.info(os.environ.get('URL'))
logging.info(os.environ.get('WS'))
logging.info(os.environ.get('CLIENT_ID'))
logging.info(os.environ.get('CLIENT_SECRET'))
logging.info(os.environ.get('EXECUTION_ID'))
logging.info(os.environ.get('LICENSER_HOST'))

#Create the AGENT Namte from the execution ID
agent_name = "EPFEXECUTION" + str(os.environ.get('EXECUTION_ID'))

#Create a Request to get the DAI token
url = os.environ.get('URL') + "/auth/realms/eggplant/protocol/openid-connect/token"
payload='grant_type=client_credentials&client_id=' + os.environ.get('CLIENT_ID') + '&client_secret=' + os.environ.get('CLIENT_SECRET')
headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload)

response = json.loads(response.text)
token = response['access_token']
#print(response['access_token'])

#Get the list of all current Agents
url = os.environ.get('URL') + "/ai/agents"

payload={}
headers = {
        'Authorization': 'Bearer ' + token
}

response = requests.request("GET", url, headers=headers, data=payload)

agents = json.loads(response.text)

for agent in agents:
        if agent['name'] == agent_name:
                sys.exit(1)
                print("Agent ID still exist")


#Create a new agent
url = os.environ.get('URL') + "/ai/agents"

payload = json.dumps({
  "name": agent_name,
  "recordpath": "",
  "suite": "/eggplant/Suites"
})
headers = {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

agent = json.loads(response.text)
agent_id = agent['id']

#get the ini file
url = os.environ.get('URL') + "/ai/agents/generate_secrets"

payload = json.dumps({
  "agent_id": agent_id,
  "host_url": os.environ.get('URL')
})
headers = {
       'Authorization': 'Bearer ' + token,
       'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

if response.status_code == 200:
        f = open("/eggplant/" + agent_name + ".ini", "w")
        f.write(response.text)
        f.close()
        print(agent_name)

        os.system("/usr/local/bin/runscript -driveport 5400 -dai-base-url " + os.environ.get('URL') + " -dai-broker-url " + os.environ.get('WS') + "/mq/fedrive -dai-environment-name " + agent_name + " -dai-environment-mode RUN -dai-suite-root /eggplant/Suites/ -BonjourDiscoveryEnabled 0 -dai-ini-file /eggplant/" + agent_name + ".ini -dai-execution-environment-id " + str(agent_id) + " -RedirectOutputToFile Yes -GSBackend libgnustep-back-headless -driveOutputFile /eggplant/output.log -LicenserHost " + os.environ.get('LICENSER_HOST'))

else:
        print(0)
