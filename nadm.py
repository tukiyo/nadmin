#!/usr/bin/env python 
import os
import sys 
dir = '/etc/nagios3/conf.d'
dir = '.'
#------------------------------------------------------
def help(emsg=""):
  if emsg != "" : print( "Error: "+emsg)
  print("usage: "+sys.argv[0]+" group host ip")
  list()
  sys.exit(1)

def list():
  for f in os.listdir(dir) :
      if not '_nagios2.cfg' in f:
          print "\t"+dir +"/"+ f

def add(group, host, ip):
  write(define_host(group, host, ip), dir+"/host_" + group + ".cfg")
  write(define_chek(group, host, ip), dir+"/host_" + group + "_check.cfg")
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
  if len(sys.argv) == 1 : help()
  elif len(sys.argv) != 4 : help("more arguments for add command")
  add(sys.argv[1], sys.argv[2], sys.argv[3])
  print("check: nagios3 -v /etc/nagios3/nagios.cfg && service nagios3 restart")
