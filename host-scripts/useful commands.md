# Docker Commands that are useful:
## finding the IP address of a container:
* docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' Service_name
