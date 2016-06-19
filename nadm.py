#!/usr/bin/env python 
import os
import sys 
dir = '/etc/nagios3/conf.d'
#------------------------------------------------------
def _help(emsg=""):
  if emsg != "" : print( "Error: "+emsg)
  print("usage: "+sys.argv[0]+" group host ip")
  _list()
  sys.exit(1)

def _list():
  for f in os.listdir(dir) :
      if not '_nagios2.cfg' in f:
          print "\t"+dir +"/"+ f

def _add(group, host, ip):
  _write(_define_host(group, host, ip), dir+"/host_" + group + ".cfg")
  _write(_define_chek(group, host, ip), dir+"/host_" + group + "_check.cfg")
  _list()

def _define_host(group, host, ip):
  txt = "# "+host+" ("+ip+")\n"
  txt+= "define host{\n"
  txt+= "    use        generic-host\n"
  txt+= "    host_name  " + group + "-" + host + "\n"
  txt+= "    alias      " + host + "\n"
  txt+= "    address    " + ip + "\n"
  txt+= "#   check_command \treturn-ok\n"
  txt+= "    }\n\n"
  return txt

# see: /usr/lib/nagios/plugins/
def _define_chek(group, host, ip):
  txt = "## "+host+"("+ip+")\n"
  txt+= "#define service{\n"
  txt+= "#    service_description Alive\n"
  txt+= "#    host_name           " + group + "-" + host + "\n"
  txt+= "#    use                 generic-service\n"
  txt+= "#    check_command       check-host-alive\n"
  txt+= "#    }\n\n"
  return txt

def _write(txt, fname):
  fp = open(fname, 'a+')
  fp.write(txt)
  fp.close()
#------------------------------------------------------
if __name__ == '__main__' :
  if len(sys.argv) == 1 : _help()
  elif len(sys.argv) != 4 : _help("more arguments for add command")
  _add(sys.argv[1], sys.argv[2], sys.argv[3])
  print("check: nagios3 -v /etc/nagios3/nagios.cfg && service nagios3 restart")
