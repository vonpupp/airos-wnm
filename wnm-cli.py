#!/usr/bin/python
__version__ = "1.0"
__author__ = "Albert De La Fuente (vonpupp@gmail.com)"
__copyright__ = "(C) 2012 Albert De La Fuente. GNU GPL 3."

import argparse

import pexpect
import sys
import pxssh
import getpass
from collections import namedtuple
from time import sleep

import lib.ssh_session as sshlib
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
        Row = namedtuple('Row',['FILE', 'ESSID', 'CHANNEL', 'BSSID', 'KEY'])
        data = []
        for item in sorted(self.wnm.networks):
            network = self.wnm.networks[item]
            data = data + [Row(network.varsfile, network.essid, network.channel,
                               network.bssid, network.key)]
        pprinttable(data)

    def printnetworks(self):
        print("%s %s %s %s" % ("ESSID", "CHANNEL", "BSSID", "KEY"))
        for item in sorted(self.wnm.networks):
            network = self.wnm.networks[item]
            print("%s %s %s %s" % (network.essid, network.channel,
                  network.bssid, network.key))

def main(args):
    #config_file = os.environ['HOME'] + '/.airos-wnm/config'

    cli = WNMCLIModel()
    if cli.wnm.loadconfig() == -1:
        print('Please fill the file properties %s' % configfilename)
        print('Quiting...')
        exit(0)
    else:
        if not args.connect:
            cli.wnm.loadnetworks()
            cli.pretyprintnetworks()
            exit(0)
        else:
            if cli.wnm.networkexists(args.connect) == None:
                print("File / network '%s' doesn't seems to exists on the repo" %
                      args.connect)
                print('Quiting...')
                exit(0)
            else:
                print("Creating temporary script to '%s'..." % wnm.tmpscriptfilename)
                cli.wnm.composescript(args.connect, wnm.tmpscriptfilename)
                print("Uploading '%s' script to the device..." % wnm.tmpscriptfilename)
                s = sshlib.ssh_session(cli.wnm.user, cli.wnm.host, cli.wnm.passwd)
                s.scp(wnm.tmpscriptfilename, wnm.tmpscriptfilename)
                cli.wnm.printsessionout()
                #print("Executing '%s' remote script on the device..." % wnm.tmpscriptfilename)
                print("Connecting to '%s'..." % args.connect)
                s = sshlib.ssh_session(cli.wnm.user, cli.wnm.host, cli.wnm.passwd)
                s.ssh('sh ' + wnm.tmpscriptfilename)
                cli.wnm.printsessionout()
                sleep(5)
                print("Connected to '%s'... [most probably :p]" % args.connect)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "AirOS CLI Wireless Network Manager")
    #parser.add_argument("filename")
    parser.add_argument("--connect", help="connect to a network within the repository")
    args = parser.parse_args()
    main(args)
