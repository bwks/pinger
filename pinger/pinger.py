import sys
if not sys.version_info >= (3, 4):
    sys.exit('Pinger requires Python 3.4 or greater')

import ipaddress
import argparse
import json
import subprocess

from multiprocessing.pool import ThreadPool


def validate_network(network):
    try:
        ipaddress.ip_network(network)
        return True
    except ValueError as e:
        print(e)
        sys.exit(1)


def get_host_list(network):
    if validate_network(network):
        subnet = ipaddress.ip_network(network)
        if subnet.num_addresses == 1:
            return [str(subnet.network_address)]
        else:
            return [str(host) for host in subnet.hosts()]


def pinger(host, verbose=True):
    out = subprocess.getoutput('ping -c 1 -w 2 {0}'.format(host))
    status = 'UP' if '1 received' in out else 'DOWN'
    if verbose:
        print('{0} -- {1}'.format(host, status))
    return {host: status}


def json_to_file(file_name, dict_list):
    with open(file_name, 'w') as outfile:
        data = {k: v for d in dict_list for k, v in d.get().items()}
        json.dump(data, outfile)


def worker(network, pool_size=256, file_name='', verbose=False):
    pool_size = pool_size
    host_list = get_host_list(network)
    pool = ThreadPool(pool_size)
    results = []
    hosts_up = 0
    hosts_down = 0
    for host in host_list:
        result = pool.apply_async(pinger, (host, verbose))
        results.append(result)
        if result[host] == 'UP':
            hosts_up += 1
        else:
            hosts_down += 1

    pool.close()
    pool.join()

    hashes = '#' * 25
    print('{0} Results {0}'.format(hashes))
    print('Total Hosts: {0} | Hosts up: {1} | Hosts down: {2}'.format(
        hosts_up + hosts_down, hosts_up, hosts_down)
    )

    if file_name:
        json_to_file(file_name, results)


def main():
    parser = argparse.ArgumentParser(description='Super fast ping')
    parser.add_argument('network', help='subnet to ping eg: 10.1.1.0/24')
    parser.add_argument('-p', '--pool-size', help='Number of concurrent hosts to ping', nargs='?', default=256, type=int)
    parser.add_argument('-f', '--file-name', help='Name of output file', type=str)
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    args = parser.parse_args()

    worker(args.network, args.pool_size, args.file_name, args.verbose)


if __name__ == '__main__':
    main()
