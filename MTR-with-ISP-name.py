#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Jash Lee"
__copyright__ = "Jun 3, 2015"
__credits__ = ["Site Reliability Engineers"]
__license__ = "BSD"
__version__ = "0.1"
__maintainer__ = "Jash Lee"
__email__ = "s905060@gmail.com"
__status__ = "Alpha"

import os
import sys
import socket
import requests

class MTR:
    def __init__(self):
        self.HOST = sys.argv[1]
        self.IP = socket.gethostbyname(self.HOST)
        self.HOSTNAME = socket.gethostname()
        self.FILE = "/tmp/MTR"
        self.CMD = 'mtr -n -i 0.1 -c 5 -r -w －4 ' + self.IP + ' > ' + self.FILE
        self.privateIP = ["10.", "172.16.", "172.31.", "192.168."]
        self.apiURL = "https://www.telize.com/geoip/" # Free GEO IP API

    def GetIp(self, ip):
        url = self.apiURL + ip
        response = requests.get(url)
        data = response.json()
        return data['country'], data['isp']

    def runMTR(self):
        os.system(self.CMD)
        with open(self.FILE, 'r') as fp: # Open tmp file
            for line in fp.readlines()[1:]: # Read line by line
                strings = line.strip() # Get the entire line and get rid of white space (head and tail)
                for ip in line.strip().split()[1:2]: # Get the ip address from the line
                    if ip == '???':
                        x = 'Forbid ICMP detect '
                        print strings + '    ' + x
                    elif ip == '`|--':
                        del ip
                    elif ip == '|--':
                        del ip
                    elif ip.startswith(tuple(self.privateIP)): # Check if it is private Ip
                        print strings + '    ' + 'internet IP'
                    else:
                        source = []
                        if "HOST" in strings: # Print First Line
                            print strings + '    ' + "ISP"
                        else:
                            prefix = str(line.strip().split()[0:1]) # Count white space, beautify
                            space = ' ' * (len(prefix) - 7 ) # Magic number 7
                            country, isp = self.GetIp(ip)
                            print strings + '    ' + country + " / " + isp
                            try:
                                source = socket.gethostbyaddr(ip) # Try resolve the DNS name from IP
                                print space + "|--> " + source[0]
                            except:
                                pass
        os.remove(self.FILE)

if __name__ == '__main__':
    main = MTR()
    main.runMTR()
