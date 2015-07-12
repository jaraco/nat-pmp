#!/usr/bin/env python
# Yiming Liu
# A NAT-PMP client implementation using NATPMP.py

import getopt, sys

import natpmp

def main():
    if len(sys.argv) < 3:
        print("usage: natpmp-client.py [-u] [-l lifetime] [-g gateway_addr] public_port private_port")
        sys.exit(-1)

    opts, args = getopt.getopt(sys.argv[1:], "ul:g:")
    public_port = int(args[0])
    private_port = int(args[1])
    protocol = natpmp.NATPMP_PROTOCOL_TCP
    lifetime = 3600
    gateway = None

    for opt in opts:
        name, val = opt
        if name == "-u":
            protocol = natpmp.NATPMP_PROTOCOL_UDP
        elif name == "-l":
            lifetime = int(val)
        elif name == "-g":
            gateway = val

    if not gateway:
        gateway = natpmp.get_gateway_addr()
    print natpmp.map_port(protocol, public_port, private_port, lifetime, gateway_ip=gateway)

if __name__=="__main__":
    main()
