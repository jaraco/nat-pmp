Provides functions to interact with NAT-PMP gateways implementing version 0
of the NAT-PMP draft specification.

Forked from `py-natpmp <https://github.com/yimingliu/py-natpmp>`_ by
Yiming Liu.


Introduction
============

NAT-PMP (Network Address Translation Port Mapping Protocol) implements
the `NAT-PMP protocol <https://en.wikipedia.org/wiki/NAT_Port_Mapping_Protocol>`_
developed by Apple as a Python library and client. Use the client to manage
port mappings on any NAT-PMP compatible router, typically limited to Apple
AirPort base stations.

Installation
============

NAT-PMP is published to PyPI. Use your favorite installer to install the package
for Python 2 or Python 3.

    pip install NAT-PMP


Library
=======

The library provides a set of high-level and low-level functions to interact
via the NAT-PMP protocol. The functions map_port and get_public_address
provide the two high-level functions offered by NAT-PMP. Responses are
stored as Python objects.


Client
======

NAT-PMP provides a command-line client. After installing the package,
the client should be installed as a console script ``natpmp-client``. If
that script does not appear on the command line, it may also be invoked
with ``python -m natpmp.client``.

Invoke the command with ``--help`` to get the usage, for example::

    $ natpmp-client --help
    usage: natpmp-client [-h] [-u] [-l LIFETIME] [-g GATEWAY]
                         public_port private_port

    positional arguments:
      public_port
      private_port

    optional arguments:
      -h, --help            show this help message and exit
      -u, --udp
      -l LIFETIME, --lifetime LIFETIME
                            lifetime in seconds
      -g GATEWAY, --gateway GATEWAY
                            gateway IP address

Example Usage
-------------

Create a TCP mapping for the public port 60010 to the private port 60010::

    natpmp-client 60010 60010

Create a UDP mapping for the public port 60009 to the private port 60009
for 1,800 seconds (30 minutes)::

    natpmp-client -u -l 1800 60009 60009

Explicitly instruct the gateway router 10.0.1.1 to create the TCP mapping
from 60010 to 60022::

    natpmp-client -g 10.0.1.1 60011 60022

Remember to turn off your firewall for those ports that you map.

Caveats
=======

This is an incomplete implementation of the specification.  When the router reboots, all dynamic mappings are lost.  The specification provides for notification packets to be sent by the router to each client when this happens.  There is no support in this library and client to monitor for such notifications, nor does it implement a daemon process to do so.  The specification recommends queuing requests – that is, all NAT-PMP interactions should happen serially.  This simple library does not queue requests – if you abuse it with multithreading, it will send those requests in parallel and possibly overwhelm the router.

The library will attempt to auto-detect your NAT gateway. This is done via a popen to netstat on BSDs/Darwin and ip on Linux. This is likely to fail miserably, depending on how standard the output is. In the library, a keyword argument is provided to override the default and specify your own gateway address. In the client, use the -g switch to manually specify your gateway.
