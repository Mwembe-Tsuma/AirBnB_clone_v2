#!/usr/bin/env bash
# This script sets up web servers for the deployment fo web_static.

# ----------------------------------------------------------------------
# This section configures a webserver with nginx, adds basic html page,
# adds custome http header X-Serve-By with the value of the hostname

# Update the package repository
sudo apt update

# Install Nginx
sudo apt install -y nginx

# Start Nginx
sudo service nginx start

# Create an index.html file with "Hello World!"
echo "Hello World!" | sudo tee /var/www/html/index.html

# Configure redirection for /redirect_me
# shellcheck disable=SC1004
sudo sed -i '/server_name _;/a \
        location /redirect_me {\n\
                rewrite ^/redirect_me https://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;\n\
        }\n' /etc/nginx/sites-available/default

# Create a custom 404 HTML page
echo "Ceci n'est pas une page" | sudo tee /var/www/html/custom_404.html

# Modify the Nginx configuration to use the custom 404 page
# shellcheck disable=SC1004
sudo sed -i '/server_name _;/a \
        error_page 404 /custom_404.html;\n\
        location = /custom_404.html {\n\
                internal;\n\
        }\n' /etc/nginx/sites-available/default

# Configure custom HTTP response header
sudo echo 'add_header X-Served-By $hostname;' | sudo tee /etc/nginx/conf.d/0-custom-header.conf

#------------------------------------------------------ end of section

sudo mkdir -p /data/web_static/releases/test/

sudo mkdir -p /data/web_static/shared

sudo echo 'fake html file' | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu: /data/

# shellcheck disable=SC1004
sudo sed -i '/server_name _;/a \
	     location = /hbnb_static {\n\
		     alias data//web_static/current;\n\
	     }\n' /etc/nginx/sites-available/default

sudo service nginx restart
