#!/usr/bin/python                                                                                                                        
import argparse
from ConfigParser import ConfigParser
import pexpect
import sys
import pxssh
import getpass
import ssh_session
import os
#import libssh2

def main(args):
    #url = args.url
    #user, host = url.split('@', 1)

    #cfg_file = os.environ['HOME'] + '/.airos-wnm/config'
    cfg_file = os.path.expanduser('~/.airos-wnm/config')
    cfg = ConfigParser()
    cfg.read(cfg_file)
    user = cfg.get("config", "user")
    host = cfg.get("config", "host")
    passwd = cfg.get("config", "pass")
    #passwd = cfg.get(user, host)

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


    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.connect((host, 22))
    #
    #session = libssh2.Session()
    #session.startup(sock)
    #session.userauth_password(user, passwd)
    #
    #channel = session.channel()
    #channel.execute('touch test')
    #
    #print channel.read(1024)


    script = open("connect.sh", "r")
    s = ssh_session.ssh_session(user, host, passwd)
    s.scp("connect.sh", "connect.sh")
    s = ssh_session.ssh_session(user, host, passwd)
    s.ssh("./connect.sh")
    
    
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
    parser = argparse.ArgumentParser(description='Run ssh through pexpect')
    #parser.add_argument('url')
    args = parser.parse_args()
    main(args)
