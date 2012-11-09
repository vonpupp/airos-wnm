#!/usr/bin/python

from ConfigParser import ConfigParser
import os
import codecs

configfilename = '~/.airos-wnm/config'

class NetworkModel:
    """ The Network model abstraction
    Attributes:
        - user, host, passwd, repo: string
    """
    bssid = ''
    essid = ''
    channel = ''
    key = ''
    varsfile = ''
    
    def __init__(self):#, bssid, essid, channel):
        #self.bssid = bssid
        #self.essid = essid
        #self.channel = channel
        pass
        
    def fetchvariable(self, variable):
        result = None
        if self.varsfile:
            f = codecs.open(self.varsfile, encoding='utf-8', mode='r')
            for line in f:
                if '=' in line:
                    fvariable = line.split('=')[0]
                    fvalue = line.split('=')[1]
                    if fvariable.strip() == variable:
                        result = fvalue.strip()
        return result

class WNMModel:
    """ The Wireless Network Manager model abstraction
    Attributes:
        - user, host, passwd, repo: string
        - networks: dict
    """
    user = ''
    host = ''
    passwd = ''
    repo = ''
    networks = {}
    
    def __init__(self):
        pass
    
    def loadconfig(self):
        """ Loads the configuration file
        """
        configfile = os.path.expanduser(configfilename)
        section = "config"
        config = ConfigParser()
        if os.path.isfile(configfile):
            config.read(configfile)
            self.user = config.get(section, "user")
            self.host = config.get(section, "host")
            self.passwd = config.get(section, "pass")
            self.repo = config.get(section, "repo")
            result = 1
        else:
            #config = ConfigParser.RawConfigParser()
            config.add_section(section)
            config.set(section, 'user', 'root')
            config.set(section, 'host', '192.168.1.1')
            config.set(section, 'pass', 'password')
            config.set(section, 'repo', '/home/user/wireless-repo')
            configfileh = open(configfile, 'wb')
            config.write(configfileh)
            result = -1
        return result
    
    def loadnetworks(self):
        """ Fills the networks dict with the networks from the vars files
        Returns:
            - Number of loaded networks
        """
        networks = {}
        result = 0
        #if self.path == ""
        for dirname, dirnames, filenames in os.walk(self.repo):
            for filename in filenames:
                if filename.endswith('.vars'):
                    result += 1
                    network = NetworkModel()
                    network.varsfile = os.path.join(dirname, filename)
                    network.bssid = network.fetchvariable('BSSID')
                    network.essid = network.fetchvariable('ESSID')
                    network.channel = network.fetchvariable('CH')
                    network.key = network.fetchvariable('KEY')
                    if network.key:
                        self.networks[network.varsfile] = network
                    else:
                        del network
                    
                    #wffile = self.fixpath(wffile, self.replacepath, self.prependpath)
                    
        return result
    
    def connect():
        pass