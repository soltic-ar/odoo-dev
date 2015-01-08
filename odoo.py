#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------
#
# Script for different odoo 7.0+ development environments.
# Based on github.com/odoo/odoo/odoo.py.
#
# wget https://raw.githubusercontent.com/soltic-ar/odoo-dev/master/odoo.py
# 
#----------------------------------------------------------
import os
import sys
import subprocess
from ConfigParser import SafeConfigParser

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

def get_current():
    try:
        f = open('.conf', 'r')
        return (f.readline()).strip()
    except:
        print "Unexpected error:", sys.exc_info()[1]

def set_current(args=[]):
    if len(args)==1:
        if os.path.isfile('./%s'%args[0]):
            if get_current()!=args[0]:
                try:
                    f = open('.conf', "w")
                    f.write(args[0])
                    f.close()
                    printf("current is now '%s'", get_current())
                    return True
                except:
                    print "Unexpected error:", sys.exc_info()[1]
        else:
            print "The %s file does not exist!"%args[0]
    return False

def cmd_current(args=[]):
    printf("current '%s'", get_current())

rootdir = os.getcwd()
parser = SafeConfigParser()
parser.read(get_current())
addons_dev = [section_name for section_name in parser.sections() if section_name!='options']

#--------------------------------------
# Versioning
#--------------------------------------

def cmd_init(args=[]):

    # read new current
    os.chdir(rootdir)
    new_parser = SafeConfigParser()
    new_parser.read(args[0])
    new_addons_dev = [section_name for section_name in new_parser.sections() if section_name!='options']

    for rep in new_addons_dev:
        printf(rep+'-'*(40-len(rep)))
        try:
            run('git', 'clone', new_parser.get(rep, 'url'), rep)
        except:
            pass

    cmd_checkout(args)

def cmd_pull(args=[]):
    for rep in addons_dev:
        printf(rep+'-'*(40-len(rep)))
        try:
            os.chdir("%s/%s"%(rootdir,rep))
            run('git', 'pull', 'origin', '%s'%parser.get(rep, 'branch'))
        except:
            print "Unexpected error:", sys.exc_info()[1]

def cmd_log(args=[]):
    for rep in addons_dev:
        printf(rep+'-'*(40-len(rep)))
        try:
            os.chdir("%s/%s"%(rootdir,rep))
            run(['git', 'log', '-1']+args)
        except:
            print "Unexpected error:", sys.exc_info()[1]

def cmd_status(args=[]):
    for rep in addons_dev:
        printf(rep+'-'*(40-len(rep)))
        try:
            os.chdir("%s/%s"%(rootdir,rep))
            run('git', 'status')
        except:
            print "Unexpected error:", sys.exc_info()[1]

def cmd_branch(args=[]):
    for rep in addons_dev:
        printf(rep+'-'*(40-len(rep)))
        try:
            os.chdir("%s/%s"%(rootdir,rep))
            run('git', 'branch')
        except:
            print "Unexpected error:", sys.exc_info()[1]

def cmd_checkout(args=[]):
    current = get_current()
    if not set_current(args):
        return False

    printf("Save local changes...")
    for rep in addons_dev:
        try:
            printf(rep+'-'*(40-len(rep)))
            os.chdir("%s/%s"%(rootdir,rep))
            msg='stash_%s(%s)'%(current, (subprocess.check_output(["git branch | grep '*'"], shell=True)).strip()[2:])
            run('git', 'stash', 'save', msg)
        except:
            print "Unexpected error:", sys.exc_info()[1]

    # read new current
    os.chdir(rootdir)
    current = get_current()
    new_parser = SafeConfigParser()
    new_parser.read(current)
    new_addons_dev = [section_name for section_name in new_parser.sections() if section_name!='options']

    printf("Checkout and restore local changes...")
    for rep in new_addons_dev:
        try:
            printf(rep+'-'*(40-len(rep)))
            os.chdir("%s/%s"%(rootdir,rep))
            run('git', 'checkout', '%s'%new_parser.get(rep, 'branch'))
        except:
            print "Unexpected error:", sys.exc_info()[1]
        # apply stash if exist
        try:
            msg='stash_%s(%s)'%(current, new_parser.get(rep, 'branch'))
            find=subprocess.check_output(["git stash list | grep '%s'"%msg], shell=True)
            stash=find[:(find.find('}:'))+1]
            run('git', 'stash', 'apply', stash)
            run('git', 'stash', 'drop', stash)
        except:
            pass

#--------------------------------------
# Odoo
#--------------------------------------

def cmd_server(args=[]):
    # Path to libreoffice (required for aeroo)
    # TODO: Detect and automatically load.
    check = os.environ['PYTHONPATH'] if os.environ.has_key('PYTHONPATH') else ''
    if parser.has_option('options', 'office_path') and not check.find(parser.get('options', 'office_path'))>0:
        printf("WARNING! office_path not found in PYTHONPATH (required for Aeroo). Run: 'export PYTHONPATH=$PYTHONPATH:%s'."%parser.get('options', 'office_path'))
        return False

    try:
        if os.path.isfile('./odoo/odoo.py'):
            run(['./odoo/odoo.py', 'server', '--config=%s'%get_current()] + args)
        else: 
            # old version
            run(['./odoo/openerp-server', '--config=%s'%get_current()] + args)
    except:
        pass    

def cmd_scaffold(args=[]):
    try:
        if os.path.isfile('./odoo/odoo.py'):
            run(['./odoo/odoo.py', 'scaffold'] + args)
    except:
        pass    

def cmd_help(args=[]):
    print "usage: odoo.py <command> [<args>]"
    print "Commands:"
    print "   environment:"
    print "    init <sample>       Initializes <sample> environment downloading repositories"
    print "    current             Shows the current environment"
    print "    checkout <sample>   Change to <sample> environment"
    print "   versioning:"
    print "    pull                Upgrade repositories current environment"
    print "    status              Shows status repositories current environment"
    print "    log [<args>]        Shows log. Supports own arguments 'git log'"
    print "   odoo:"
    print "    server [<args>]     Starts odoo server. Supports own arguments odoo server"
    print "    scaffold [<args>]   Generates a base module for development. Supports own arguments odoo scaffold (only for version 8.0+)"

def main():
    # regsitry of commands
    g = globals()
    cmds = dict([(i[4:],g[i]) for i in g if i.startswith('cmd_')])
    if len(sys.argv) >1 and sys.argv[1] in cmds:     
        if sys.argv[1:][0]!='current': 
            cmd_current()
        cmds[sys.argv[1]]( sys.argv[2:] )    
    else:
        cmd_help()

if __name__ == "__main__":
    main()
