import socket
import subprocess
import argparse
import concurrent.futures

parser = argparse.ArgumentParser("netenum.py")
parser.add_argument("-r", "--range", help="IP range to scan (Ex. '192.168.0.0/24')", type=str)
parser.add_argument("-ip", "--ipaddress", help="IP address to port scan (Ex. '192.168.0.100')", type=str)
parser.add_argument("-t", "--timeout", help="Timeout in seconds (Default: 2)", type=int, default=2)
parser.add_argument("-v", "--verbose", help="Show all the process", action='store_true')
args = parser.parse_args()

def ping_sweep(ip, verbose=False):
    try:
        response = subprocess.check_output(
            ["ping", "-c", "1", "-W", str(timeout), ip],
            stderr=subprocess.STDOUT,
            timeout=1,
        )
        if "1 packets transmitted, 1 received" in response.decode():
            print(f"{ip} is up")
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        if verbose:
            print(f"{ip} is down")
        pass
    except KeyboardInterrupt:
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

def get_open_ports(ip, port, verbose):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    if result == 0:
        print("Port {}/tcp open".format(port))
    elif verbose:
        print("Port {}/tcp close".format(port))

if __name__ == "__main__":
    ports = 65535
    verbose = args.verbose
    timeout = args.timeout
    
    if args.range:
        with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
            for result in executor.map(ping_sweep, scan_subnet(args.range)):
                pass
    elif args.ipaddress:
        with concurrent.futures.ThreadPoolExecutor(max_workers=150) as executor:
            for port in list(range(ports)):
                executor.submit(get_open_ports, args.ipaddress, port, verbose)
                pass
    else:
        print(parser.print_help())
