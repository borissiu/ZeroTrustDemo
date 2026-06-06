import zt_mcp_lifecycle_json as zt_mcp_json
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def decode_mcp_response(response):
    current_event = None
    current_data = []
    decoded_events = []

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith("event:"):
                current_event = decoded_line[6:].strip()
            elif decoded_line.startswith("data:"):
                current_data.append(decoded_line[5:].strip())
        else:
            if current_data:
                full_data = "\n".join(current_data)
                data = json.loads(full_data)
                current_event = None
                current_data = []
    return data

def connect_direct(url, user=None, password=None, proxy=None):
    session = requests.Session()
    session.verify = False

    session.headers.update({'Accept': 'application/json, text/event-stream'})
    r = session.post(url, json=zt_mcp_json.initialize, timeout=5, stream=True)
    if 'mcp-session-id' in r.headers:
        session.headers.update({'mcp-session-id': r.headers['mcp-session-id']})
    r = session.post(url, json=zt_mcp_json.initialize_ack, timeout=5, stream=True)
    r = session.post(url, json=zt_mcp_json.tools_list, timeout=5)
    r = decode_mcp_response(r)
    return(r)

def connect_viaF5(url, user=None, password=None, proxy=None):
    session = requests.Session()
    session.verify = False
    if proxy != None:
        fwdProxy = {}
        fwdProxy["http"] = "http://" + user + ":" + password + "@" + proxy
        fwdProxy["https"] = "http://" + user + ":" + password + "@" + proxy
        session.proxies = fwdProxy

    session.headers.update({'Accept': 'application/json, text/event-stream'})
    r = session.post(url, json=zt_mcp_json.initialize, timeout=5, stream=True)
    if 'X-Frame-Options' in r.headers:
        if r.headers['X-Frame-Options'] == 'DENY':
            print("Blocked by Zero Trust Policy!")
            data = '{"result": {"tools": [{"name": "Blocked by Zero Trust Policy!"}]}}'
            return(json.loads(data))
    if 'mcp-session-id' in r.headers:
        session.headers.update({'mcp-session-id': r.headers['mcp-session-id']})
    r = session.post(url, json=zt_mcp_json.initialize_ack, timeout=5, stream=True)
    r = session.post(url, json=zt_mcp_json.tools_list, timeout=5)
    r = decode_mcp_response(r)
    return(r)

def checkPolicy():
    mgmtSession = requests.Session()
    mgmtSession.verify = False
    mgmtSession.headers.update({'Content-Type': 'application/json'})
    body = { "username": "fake-user", "password": "fake-password", "loginProviderName": "tmos" }
    r = mgmtSession.post("https://fake-ip/mgmt/shared/authn/login", json=body, timeout=5)
    token=r.json()['token']['token']
    r = mgmtSession.get("https://fake-ip/mgmt/tm/sys/url-db/url-category/ZeroTrust_Block", headers={'X-F5-Auth-Token': token}, timeout=5)
    ZeroTrust_Block = r.json()['urls']
    return r.json()['urls']

def updatePolicy(urls_policy):
    mgmtSession = requests.Session()
    mgmtSession.verify = False
    mgmtSession.headers.update({'Content-Type': 'application/json'})
    body = { "username": "fake-user", "password": "fake-password", "loginProviderName": "tmos" }
    r = mgmtSession.post("https://fake-ip/mgmt/shared/authn/login", json=body, timeout=5)
    token=r.json()['token']['token']
    r = mgmtSession.patch("https://fake-ip/mgmt/tm/sys/url-db/url-category/ZeroTrust_Block", headers={'X-F5-Auth-Token': token}, json=urls_policy, timeout=5)

