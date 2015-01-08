# odoo-dev

Script for different odoo 7.0+ development environments using configuration file odoo own.
Based on github.com/odoo/odoo/odoo.py

## Dependencies

* git
* postgres
* Packages required by Odoo:
```
sudo apt-get install graphviz ghostscript postgresql-client
python-dateutil python-feedparser python-gdata
python-ldap python-libxslt1 python-lxml python-mako
python-openid python-psycopg2 python-pybabel python-pychart
python-pydot python-pyparsing python-reportlab python-simplejson
python-tz python-vatnumber python-vobject python-webdav
python-werkzeug python-xlwt python-yaml python-imaging
python-matplotlib python-decorator python-requests python-passlib
```

https://doc.odoo.com/7.0/install/linux/server/#installing-the-required-packages

## How to use

### Download script

```
mkdir odoo-dev
cd odoo-dev
wget https://raw.githubusercontent.com/soltic-ar/odoo-dev/master/odoo.py
```

### Create a environment **sample**

1- Create *sample.conf* file with the definition of the repositories:

```
;---------------------------------------
; Odoo configuration
;---------------------------------------

[options]

addons_path = addons-mycompany,addons-other
log_level = debug

;---------------------------------------
; Addons repositories configuration
;---------------------------------------

[odoo]
url = https://github.com/odoo/odoo.git
branch = 8.0

[addons-mycompany]
url = git@github.com:mycompany/myrepo.git
branch = 8.0

[addons-other]
url = git@github.com:mycompany/other.git
branch = 8.0

```

Where:

* url: The repository url
* branch: The branch of work

2- Initialize repositories

`./odoo.py init sample.conf`
 
### Development

Start the odoo server

`./odoo.py server`

Update modules

`./odoo.py server --update=all --database=DBNAME`

> View other commands in [odoo command line options](https://doc.odoo.com/trunk/server/01_getting_started/#command-line-options)

Pull repositories

`./odoo.py pull`

Show current environment

`./odoo.py current`

Change of environment

`./odoo.py checkout another.conf`

