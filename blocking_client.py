import datetime, optparse, socket


def parse_args():
    parser = optparse.OptionParser()

    _, addresses = parser.parse_args()

    if not addresses:
        print parser.format_help()
        parser.exit()

    def parse_address(addr):
        if ':' not in addr:
            host = '127.0.0.1'
            port = addr
        else:
            host, port = addr.split(':', 1)

        if not port.isdigit():
            parser.error('Ports must be integers.')

        return host, int(port)

    return map(parse_address, addresses)


def get_poetry(address):
    """Download a piece of poetry from the given address."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)

    poem = ''

    while True:

        # This is the 'blocking' call in this synchronous program.
        # The recv() method will block for an indeterminate period
        # of time waiting for bytes to be received from the server.

        data = sock.recv(1024)

        if not data:
            sock.close()
            break

        poem += data

    return poem


def format_address(address):
    host, port = address
    return '%s:%s' % (host or '127.0.0.1', port)


def main():
    addresses = parse_args()

    elapsed = datetime.timedelta()

    for i, address in enumerate(addresses):
        addr_fmt = format_address(address)

        print 'Task %d: get poetry from: %s' % (i + 1, addr_fmt)

        start = datetime.datetime.now()

        # Each execution of 'get_poetry' corresponds to the
        # execution of one synchronous task in Figure 1 here:
        # http://krondo.com/?p=1209#figure1

        poem = get_poetry(address)

        time = datetime.datetime.now() - start

        msg = 'Task %d: got %d bytes of poetry from %s in %s'
        print  msg % (i + 1, len(poem), addr_fmt, time)

        elapsed += time

    print 'Got %d poems in %s' % (len(addresses), elapsed)


if __name__ == '__main__':
    main()