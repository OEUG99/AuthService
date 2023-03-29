import jinja2
import requests

DOCKER_HOST_IP = "localhost"
CONSUL_BASE_URL = f"http://{DOCKER_HOST_IP}:8500"
CONSUL_LIST_SERVICES_URL = f"{CONSUL_BASE_URL}/v1/catalog/services"

nginx_template = ('''
events {
    worker_connections 1024;
}

http {
    resolver 172.17.0.2;

    {% for service_name, services in all_services.items() if service_name != 'consul' %}
    upstream {{ service_name }} {
        {% for service in services %}
        server {{ service.ServiceAddress }}:{{ service.ServicePort }};
        {% endfor %}
    }
    
    upstream consul {
        
        server ''' + DOCKER_HOST_IP + (''':8500;
        
    }
    
    upstream react {
        server ''' + DOCKER_HOST_IP + ''':3000;
    }
    {% endfor %}

    server {
        listen 8081;

        {% for service_name, services in all_services.items() if service_name != 'consul' %}
        location ~ ^/api/{{ service_name }}/(.*)$ {
            proxy_pass http://{{ service_name }}/$1;
        }
        {% endfor %}


        location / {
            proxy_pass http://react;
        }
        
        location ~ ^/api/consul/(.*)$ {
            proxy_pass http://consul/$1;
        }
        
        # ... add any additions below if needed - ...
        
    }
}
'''))


def get_all_services():
    response = requests.get(CONSUL_LIST_SERVICES_URL)
    response.raise_for_status()
    services = response.json()

    all_services = {}
    for service_name in services:
        service_url = f"{CONSUL_BASE_URL}/v1/catalog/service/{service_name}"
        service_response = requests.get(service_url)
        service_response.raise_for_status()
        all_services[service_name] = service_response.json()

    return all_services


def generate_nginx_config(all_services):
    template = jinja2.Template(nginx_template, autoescape=True)
    config = template.render(all_services=all_services)
    with open("ngnix_dev.conf", "w") as f:
        f.write(config)


def main():
    all_services = get_all_services()
    generate_nginx_config(all_services)


if __name__ == "__main__":
    main()