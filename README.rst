.. image:: https://img.shields.io/pypi/v/skeleton.svg
   :target: `PyPI link`_

.. image:: https://img.shields.io/pypi/pyversions/skeleton.svg
   :target: `PyPI link`_

.. _PyPI link: https://pypi.org/project/skeleton

.. image:: https://github.com/jaraco/skeleton/workflows/tests/badge.svg
   :target: https://github.com/jaraco/skeleton/actions?query=workflow%3A%22tests%22
   :alt: tests

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

.. .. image:: https://readthedocs.org/projects/skeleton/badge/?version=latest
..    :target: https://skeleton.readthedocs.io/en/latest/?badge=latest

Provides functions to interact with NAT-PMP gateways implementing version 0
of the NAT-PMP draft specification.

Forked from `py-natpmp <https://github.com/yimingliu/py-natpmp>`_ by
Yiming Liu. See `this blog <http://blog.yimingliu.com/2008/01/07/nat-pmp-client-library-for-python>`_
for more background.

Introduction
============

py-natpmp is a NAT-PMP (Network Address Translation Port Mapping Protocol) library and testing client in Python. The client allows you to set up dynamic port mappings on NAT-PMP compatible routers. Thus this is a means for dynamic NAT traversal with routers that talk NAT-PMP. In practical terms, this is basically limited to the newer Apple AirPort base stations and the AirPort Express, which have support for this protocol.

In any case, this library puts a thin layer of Python abstraction over the NAT-PMP protocol, version 0, as specified by the NAT-PMP draft standard.

Library
=======

The library provides a set of high-level and low-level functions to interact via the NAT-PMP protocol. The functions map_port and get_public_address provide the two high-level functions offered by NAT-PMP. Responses are stored as Python objects.

Client
======

To use the client, grab it and the above library. Make sure you have the library in the same directory as the client script or otherwise on your Python instance’s sys.path. Invoke the client on the command-line (Terminal.app) as ``python -m natpmp [-u] [-l lifetime] [-g gateway_addr] public_port private_port``.

For example:

``python -m natpmp -u -l 1800 60009 60009``
Create a mapping for the public UDP port 60009 to the private UDP port 60009 for 1,800 seconds (30 minutes)

``python -m natpmp 60010 60010``
Create a mapping for the public TCP port 60010 to the private TCP port 60010

``python -m natpmp -g 10.0.1.1 60011 60022``
Explicitly instruct the gateway router 10.0.1.1 to create the TCP mapping from 60010 to 60022

Remember to turn off your firewall for those ports that you map.

Caveats
=======

This is an incomplete implementation of the specification.  When the router reboots, all dynamic mappings are lost.  The specification provides for notification packets to be sent by the router to each client when this happens.  There is no support in this library and client to monitor for such notifications, nor does it implement a daemon process to do so.  The specification recommends queuing requests – that is, all NAT-PMP interactions should happen serially.  This simple library does not queue requests – if you abuse it with multithreading, it will send those requests in parallel and possibly overwhelm the router.

The library will attempt to auto-detect your NAT gateway. This is done via a popen to netstat on BSDs/Darwin and ip on Linux. This is likely to fail miserably, depending on how standard the output is. In the library, a keyword argument is provided to override the default and specify your own gateway address. In the client, use the -g switch to manually specify your gateway.
