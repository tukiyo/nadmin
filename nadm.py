#!/usr/bin/env python 

import os
import sys

dir = '/etc/nagios3/conf.d/'
version = "0.9"

def _list():
  """List hosts"""
  for f in os.listdir(dir) :
    if 'nagios' in f : continue
    print f
def _print_header():
  print("nadm v" + version + ": nagios admin")

def _help(emsg=""):
  if emsg != "" : print( "Error: "+emsg)
  print("\tlist\t\tlist hosts")
  print("\tadd [host] [ipaddress] \tadd a host and ipaddress to ping")
  print("\tdel [host]\tdelete a host")
  sys.exit(1)

def _is_exist_host(fname) :
  if os.path.isfile(fname): return True
  return False

def _add(host, ipaddr):
  fname = dir+"/" + host + ".cfg"
  if _is_exist_host(fname) : 
    print("Error: host already exist")
    sys.exit(1)
  fp = open(fname, 'w')
  fp.write("define host{\n")
  fp.write("use       generic-host\n")
  fp.write("  host_name " + host + "\n")
  fp.write("  alias " + host + "\n")
  fp.write("  address " + ipaddr + "\n")
  fp.write("}\n")

#define service{
#  use       generic-service
#  host_name KCT_HyundeaHS_Life
#  service_description Alive
#3  check_command check-host-alive
#}
  fp.close()
  print("Done, please restart nagios")
  sys.exit()

def _del(host):
  fname = dir+"/" + host + ".cfg"
  if not _is_exist_host(fname) :
    print("Error: host not found")
    sys.exit(1)
  # are you sure?
  os.unlink(fname)
  sys.exit()

if __name__ == '__main__' :
  _print_header()
  if len(sys.argv) == 1 : _help()
  elif sys.argv[1] == 'list' : _list()
  elif sys.argv[1] == 'add' and len(sys.argv) != 4 : _help("more arguments for add command")
  elif sys.argv[1] == 'add' : _add(sys.argv[2], sys.argv[3])
  elif sys.argv[1] == 'del' and len(sys.argv) != 3 : _help("more argements for del command")
  elif sys.argv[1] == 'del' : _del(sys.argv[2])

