#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------
#
# Script for different odoo 7.0+ development environments.
# Based on odoo/odoo.py.
#
# wget -O- https://raw.githubusercontent.com/soltic-ar/odoo/master/odoo.py | python
#
#----------------------------------------------------------
import os
import re
import sys
import subprocess
import yaml

def printf(f,*l):
    print "odoo-dev: " + f % l

def run(*l):
    if isinstance(l[0], list):
        l = l[0]
    printf("running %s", " ".join(l))
    subprocess.check_call(l)

#--------------------------------------
# Environment
#--------------------------------------

def get_currentenv():
    try:
        f = open('.conf', 'r')
        return f.readline()
    except:
        pass

def load_dataenv():
    try:
        f = get_currentenv()
        stream = open(f, "r")
        return yaml.load(stream)
    except:
        pass

def cmd_current(args=[]):
    printf("current '%s'", get_currentenv())

def cmd_set(args=[]):
    if len(args)==1:
        if os.path.isfile('./%s'%args[0]):
            try:
                f = open('.conf', "w")
                f.write(args[0])
                f.close()
                cmd_checkout()
                printf("current is now '%s'", args[0])
            except:
                print "Unexpected error:", sys.exc_info()[0]
        else:
            printf("The %s environment does not exist!"%args[0])
    return True

dataenv=load_dataenv()

#--------------------------------------
# Versioning
#--------------------------------------

def cmd_init(args=[]):
    rootdir=os.getcwd()
    for rep in dataenv['repository']:
        printf('-'*40)
        try:
            run('git', 'clone', rep['url'], rep['folder'])
            os.chdir("%s/%s"%(rootdir,rep['folder']))
            run('git', 'checkout', rep['branch'])
            os.chdir("../")
        except:
            pass

def cmd_pull(args=[]):
    cmd_current()
    rootdir=os.getcwd()
    for rep in dataenv['repository']:
        printf(rep['folder']+'-'*(40-len(rep['folder'])))
        try:
            os.chdir("%s/%s"%(rootdir,rep['folder']))
            run('git', 'pull', 'origin', '%s'%rep['branch'])
        except:
            pass

def cmd_log(args=[]):
    cmd_current()
    rootdir=os.getcwd()
    for rep in dataenv['repository']:
        printf(rep['folder']+'-'*(40-len(rep['folder'])))
        try:
            os.chdir("%s/%s"%(rootdir,rep['folder']))
            run(['git', 'log', '-1']+args)
        except:
            pass

def cmd_checkout(args=[]):
    rootdir=os.getcwd()
    dataenv= load_dataenv()
    for rep in dataenv['repository']:
        printf(rep['folder']+'-'*(40-len(rep['folder'])))
        try:
            os.chdir("%s/%s"%(rootdir,rep['folder']))
            run('git', 'checkout', '%s'%rep['branch'])
        except:
            pass

#--------------------------------------
# Odoo
#--------------------------------------

def cmd_server(args=[]):
    cmd_current()
    addons=[]
    for rep in dataenv['repository']:
        try:
            addons.append(rep['folder-addons'])
        except:
            addons.append(rep['folder'])
    try:
        if os.path.isfile('./odoo/odoo.py'):
            run(['./odoo/odoo.py', 'server', '--addons-path=%s'%",".join(addons)] + args)
        else: 
            # old version
            run(['./odoo/openerp-server', '--addons-path=%s'%",".join(addons)] + args)
    except:
        pass    

def cmd_help():
    print "usage: odoo.py <command> [<args>]"
    print "Commands:"
    print "   environment:"
    print "    set <sample>        Sets an environment"
    print "    current             Shows the current environment"
    print "   versioning:"
    print "    init                Initializes current environment downloading repositories"
    print "    pull                Upgrade repositories current environment"
    print "    log [<args>]        Shows log. Supports own arguments 'git log'"
    print "   odoo:"
    print "    server [<args>]     Starts odoo server. Supports own arguments odoo server"

def main():
    # regsitry of commands
    g = globals()
    cmds = dict([(i[4:],g[i]) for i in g if i.startswith('cmd_')])
    if len(sys.argv) >1 and sys.argv[1] in cmds:
        cmds[sys.argv[1]]( sys.argv[2:] )    
    else:
        cmd_help()

if __name__ == "__main__":
    main()

