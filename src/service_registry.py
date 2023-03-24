import json
import os
import requests


def register_service(consul_host, consul_port, service_name, service_port, service_ip, service_tags,
                     health_check_endpoint):
    # similar to the flask_consulate library, but allows for easier use with containers
    # todo: move to a separate repo and support as a library for re-usability across other python based micro services.

    url = f'http://{consul_host}:{consul_port}/v1/agent/service/register'

    service_definition = {
        "ID": f"{service_name}-{service_ip}-{service_port}",
        "Name": service_name,
        "Tags": service_tags,
        "Address": service_ip,
        "Port": int(service_port),
        "Check": {
            "HTTP": f"http://{service_ip}:{service_port}/{health_check_endpoint}",
            "Interval": "10s"
        }
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.put(url, data=json.dumps(service_definition), headers=headers)

    if response.status_code == 200:
        print(f'Service {service_name} registered with Consul!')
    else:
        print(f'Error registering service: {response.text}')


servicePort = os.environ.get('SERVICE_PORT')
serviceIP = os.environ.get('SERVICE_IP') or requests.get('https://checkip.amazonaws.com').text.strip()
register_service('consul',
                 8500,
                 'Authentication',
                 servicePort,
                 serviceIP,
                 ['register', 'login', 'validate'],
                 'health')