# consul to nginx service discovery
This directory contains various scripts to help with service discovery in a consul cluster.

## generate_nginx_config.py
This script will query consul for all services and then generate a nginx configuration file that will proxy to the services.

### Usage
```bash
python generate_nginx_config.py
```

## update_nginx_config.sh
This script will update the nginx configuration file and then reload nginx.


## Usage
```bash
sudo ./update_nginx_config.sh
```

## Why do we do this?
We use consul to register services, and then we use nginx to proxy to those services. 
** This avoids CORS issues and allows us to use the same domain for all of our services. **



