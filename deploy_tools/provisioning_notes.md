Provisioning a new site
=====================================================================

## Should install:

* nginx
* python3
* git
* pip

e.g.,, on Ubuntu:

	sudo apt-get install nginx git python3 python3-pip

## Nginx virtualenv server setting

* see nginx.template.conf
* replace SITENAME with, e.g., staging.my-domain.com

## Upstart work

* see gunicorn-upstart.template.service
* replace SITENAME with, e.g., staging.my-domain.com

## Folder structure:
Assume we have a user account at /home/username

/home/username
└──sites
    └──SITENAME
	├──database
	├──source
	├──static
	└──venv


