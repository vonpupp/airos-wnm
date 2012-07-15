#!/usr/bin/python                                                                                                                        
import argparse
from ConfigParser import ConfigParser
import pexpect

def main(args):
    url = args.url
    user, host = url.split('@', 1)

    cfg_file = 'ssh.cfg'
    cfg = ConfigParser()
    cfg.read(cfg_file)
    passwd = cfg.get(user, host)

    child = pexpect.spawn('ssh {0}'.format(url))
    child.expect('password:')
    child.sendline(passwd)
    child.interact()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run ssh through pexpect')
    parser.add_argument('url')
    args = parser.parse_args()
    main(args)
