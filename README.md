AirOS CLI Wireless Network Manager
==================================

This a simple CLI version of a wireless network connection manager 
which works over ssh for an Ubiquiti AirOS Nanostation 2 device 
(not the MiMo version)

Networks
--------

Networks are stored in a single directory (repository), each network is
represented as a very simple (ba)sh file containing some variables:

Example: (filename: /home/albert/wireless-repo/wireless1.vars)

    #!/bin/bash
    BSSID=xx:yy:zz:xx:yy:zz     # MAC address
    ESSID="Wireless AP 01"      # Network name
    KEY=1111                    # Network key

Config file
-----------

The config file is stored in: ~/.airos-wnm/config.

Example: (filename: ~/.airos-wnm/config)

    [config]
    user = root
    host = 192.168.0.1
    pass = your-admin-password
    repo = /home/albert/wireless-repo

Usage
-----

The tool is very minimalistic, designed for easy use.

### Commands

### No arguments

It will list available networks (files within the repository)

Input example:

    $ python wnm-cli.py
    
Output example:

    FILE           | ESSID                  | CHANNEL | BSSID             | KEY       
    ---------------+------------------------+---------+-------------------+-----------
    wireless1.vars | "Wireless AP 01"       | 6       | xx:yy:zz:xx:yy:zz | 1111
    wireless2.vars | "Wireless AP 02"       | 11      | xx:yy:zz:xx:yy:zz | 2222
    wireless3.vars | "Wireless AP 03"       | 6       | xx:yy:zz:xx:yy:zz | 3333

### Connect to a wireless2 network

Input example:

    $ python wnm-cli.py --connect wireless2
    
Output example:

    Creating temporary script to 'connect.sh'...
    Uploading 'connect.sh' script to the device...
    root@192.168.0.1's password:
    
    connect.sh                                    100%  822     0.8KB/s   00:00    
    
    <class 'pexpect.EOF'>
    
    Connecting to 'wireless2'...
    root@192.168.0.1's password:
    
    Connection to 192.168.0.1 closed by remote host.
    
    <class 'pexpect.EOF'>
    
    Connected to 'wireless2'... [most probably :p]