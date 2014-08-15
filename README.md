# odoo-dev

Script for different odoo 7.0+ development environments.
Based on odoo/odoo.py.

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

## How to use

### Download script

```
mkdir odoo-dev
cd odoo-dev
wget https://raw.githubusercontent.com/soltic-ar/odoo-dev/master/odoo.py
```

### Create a environment **sample**

1- Create *sample.yml* file with the definition of the repositories:

```
repository:

  # The odoo repository
  - 
    url: https://github.com/odoo/odoo.git
    folder: odoo
    branch: master
    folder-addons: odoo/openerp/addons,odoo/addons

  # Other modules repositories 
  -
    url: git@github.com:mycompany/myrepo.git
    folder: addons-mycompany
    branch: master
  -
    url: https://my-company.com/repos/other.git
    folder: addons-other
    branch: master
    folder-addons: addons-other/addons
```

Where:

* url: The repository url
* folder: The destination directory
* branch: The branch of work
* folder-addons (optional): To be added to the addons-path odoo (If not specified takes the *folder* attribute)

2- Assign *sample.yml* as the current environment: 
    
`./odoo.py set sample.yml`

3- Initialize repositories

`./odoo.py init`
 
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

`./odoo.py set another.yml`

