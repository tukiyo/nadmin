#!/usr/bin/env python 
import os
import sys 
dir = '/etc/nagios3/conf.d'
dir = '.'
#------------------------------------------------------
def help(emsg):
    print(emsg)
    print("usage: {} group host ip").format(sys.argv[0])
    list()

def list():
    for f in os.listdir(dir) :
        if '.cfg' in f and '_nagios2' not in f:
            print "\t{dir}/{file}".format(dir=dir,file=f)

def add(group, host, ip):
    write(define_host(group, host, ip)
        ,"{dir}/host_{group}.cfg".format(dir=dir, group=group))
    write(define_chek(group, host, ip)
        ,"{dir}/host_{group}_check.cfg".format(dir=dir, group=group))
    list()

def define_host(group, host, ip):
    form = """# {host} ({ip})"
define host{{
    use        generic-host
    host_name  {group}-{host}
    alias      {host}
    address    {ip}
#   check_command return-ok
    }}
"""
    text = form.format(group=group, host=host, ip=ip)
    return text

# see: /usr/lib/nagios/plugins/
def define_chek(group, host, ip):
    form = """## {host} ({ip})
#define service{{
#    service_description Alive
#    host_name           {group}-{host}
#    use                 generic-service
#    check_command       check-host-alive
#    }}
"""
    text = form.format(group=group, host=host, ip=ip)
    return text

def write(txt, fname):
    fp = open(fname, 'a+')
    fp.write(txt)
    fp.close()
#------------------------------------------------------
if __name__ == '__main__' :
    if len(sys.argv) != 4:
        help('[ERROR] specify argument is wrong.')
        sys.exit(1)

    add(sys.argv[1], sys.argv[2], sys.argv[3])
    print("check: nagios3 -v /etc/nagios3/nagios.cfg && service nagios3 restart")
