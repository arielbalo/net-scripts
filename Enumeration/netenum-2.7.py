import socket
import subprocess
import argparse

parser = argparse.ArgumentParser("netenum.py")
parser.add_argument("-r", "--range", help="IP range to scan (Ex. '192.168.0.0/24')", type=str)
parser.add_argument("-ip", "--ipaddress", help="IP address to port scan (Ex. '192.168.0.100')", type=str)
parser.add_argument("-t", "--timeout", help="Timeout in seconds (Default: 2)", type=int, default=2)
parser.add_argument("-v", "--verbose", help="Show all the process", action='store_true')
args = parser.parse_args()


def ping_sweep(subnet, verbose=False, timeout=2):
    for ip in scan_subnet(subnet):
        try:
            response = subprocess.check_output(
                ["ping", "-c", "1", "-W", str(timeout), ip],
                stderr=subprocess.STDOUT,
            )
            if u"1 packets transmitted, 1 received" in response.decode("utf-8"):
                print("{} is up".format(ip))
        except subprocess.CalledProcessError as e:
            if verbose:
                print("{} is down".format(ip))
            continue
        except (KeyboardInterrupt):
            print("\nExiting...\n")
            exit(1)


def scan_subnet(subnet):
    ip_host, ip_mask = subnet.split("/")
    network = ip_host.split('.')
    cant_hosts = 2**(32-int(ip_mask))
    network_range = []
    for i in range(cant_hosts):
        if i == 0:
            continue
        network[-1] = str(i)
        network_range.append('.'.join(network))
    return network_range

def get_open_ports(ip, verbose=False):
    ports = 65535
    open_ports = []
    for port in range(ports):
        if verbose:
            print("Testing the port {}/tcp".format(port))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            print("Port {}/tcp open".format(port))
            open_ports.append(port)
    #return open_ports

if __name__ == "__main__":
    verbose = args.verbose
    timeout = args.timeout

    if args.range:
        ping_sweep(args.range, verbose, timeout)
    elif args.ipaddress:
        get_open_ports(args.ipaddress, verbose)
    else:
        print(parser.print_help())
