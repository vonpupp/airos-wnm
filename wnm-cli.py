#!/usr/bin/python                                                                                                                        
import argparse

import pexpect
import sys
import pxssh
import getpass
import ssh_session
from collections import namedtuple

import model.wnmmodel as wnm
#import libssh2

def pprinttable(rows):
    if len(rows) > 1:
        headers = rows[0]._fields
        lens = []
        for i in range(len(rows[0])):
            lens.append(len(max([x[i] for x in rows] + [headers[i]],key=lambda x:len(str(x)))))
        formats = []
        hformats = []
        for i in range(len(rows[0])):
            if isinstance(rows[0][i], int):
                formats.append("%%%dd" % lens[i])
            else:
                formats.append("%%-%ds" % lens[i])
            hformats.append("%%-%ds" % lens[i])
        pattern = " | ".join(formats)
        hpattern = " | ".join(hformats)
        separator = "-+-".join(['-' * n for n in lens])
        print hpattern % tuple(headers)
        print separator
        for line in rows:
            print pattern % tuple(line)
    elif len(rows) == 1:
        row = rows[0]
        hwidth = len(max(row._fields,key=lambda x: len(x)))
        for i in range(len(row)):
            print "%*s = %s" % (hwidth,row._fields[i],row[i])

class WNMCLIModel:
    """ The CLI model abstraction
    Attributes:
        - file: string
    """
    wnm = None
    host = ''
    passwd = ''
    repo = ''
    
    def __init__(self):
        self.wnm = wnm.WNMModel()

    def pretyprintnetworks(self):
        Row = namedtuple('Row',['BSSID', 'CHANNEL', 'ESSID', 'KEY'])
        data = []
        for item in sorted(self.wnm.networks):
            network = self.wnm.networks[item]
            data = data + [Row(network.bssid, network.channel, network.essid, network.key)]
        pprinttable(data)

    def printnetworks(self):
        print("%s %s %s %s" % ("BSSID", "CHANNEL", "ESSID", "KEY"))
        for item in sorted(self.wnm.networks):
            network = self.wnm.networks[item]
            print("%s %s %s %s" % (network.bssid, network.channel,
                  network.essid, network.key))

def main(args):
    #config_file = os.environ['HOME'] + '/.airos-wnm/config'

    cli = WNMCLIModel()
    if cli.wnm.loadconfig() == -1:
        print('please fill the file properties %s' % configfilename)
        print('quiting...')
        exit(0)
    else:
        if not args.connect:
            cli.wnm.loadnetworks()
            cli.pretyprintnetworks()
            print('I will list the networks')
            exit(0)
        else:
            print('connecting to %s' % args.connect)
            s = ssh_session.ssh_session(user, host, passwd)
            s.scp("wep-connect.sh", "wep-connect.sh")
            s = ssh_session.ssh_session(user, host, passwd)
            s.ssh("./wep-connect.sh")
    #filename = args.filename
    #varsf = repo + "/" + filename + ".vars"

    #child = pexpect.spawn('ssh {0}'.format(url))
    #child.expect('password:')
    #child.sendline(passwd)
    #child.interact()
    
    #user = "root"
    #try:
    #    host = sys.argv[1]
    #except IndexError:
    #    print "Must have host name or ip address"
    #    sys.exit(1)

    

#    script = open("connect.sh", "r")

    
    
    #for line in script:
    #    line = line.split("\n")[0]
    #    if line != "":
    #        print "executing: %s" % line
    #        s = ssh_session.ssh_session(user, host, passwd)
    #        s.ssh(line)

    #s = pxssh.pxssh()
    #if not s.login(host, user, passwd):
    #    print "SSH session failed on login."
    #    print str(s)
    #else:
    #    print "SSH session login successful"
    #    s.sendline ('ls -l')
    #    s.prompt()         # match the prompt
    #    print s.before     # print everything before the prompt.
    #    s.logout()


    
    #passwd = "yourpasswd"
    #try:
    #s = pxssh.pxssh()
    #s.force_passwd = True
    #s.login (host, user, passwd)#, login_timeout = 20)
    #s.sendline("ls -la") # run a command
    #s.prompt() # match the prompt
    ##print s.before(), s.after
    #s.interact()
    #except pxssh.ExceptionPxssh, e:
    #    print "pxssh failed on login."
    #    print str(e)
    #except OSError:
    #    print "End session to " + user + "@" + host


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Wireless network connection manager")
    #parser.add_argument("filename")
    parser.add_argument("--connect", help="connect to a network on the repository")
    args = parser.parse_args()
    main(args)
