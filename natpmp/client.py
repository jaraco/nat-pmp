import argparse

import natpmp


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('public_port')
    parser.add_argument('private_port')
    parser.add_argument(
        '-u',
        '--udp',
        dest='protocol',
        default=natpmp.NATPMP_PROTOCOL_TCP,
        action='store_const',
        const=natpmp.NATPMP_PROTOCOL_UDP,
    )
    parser.add_argument(
        '--lifetime', type=int, default=3600,
        help='lifetime in seconds')
    parser.add_argument('--gateway', help='gateway IP address')
    return parser.parse_args()


def main():
    args = get_args()
    res = natpmp.map_port(
        args.protocol,
        args.public_port,
        args.private_port,
        args.lifetime,
        gateway_ip=args.gateway or natpmp.get_gateway_addr(),
    )
    print(res)


if __name__ == "__main__":
    main()
