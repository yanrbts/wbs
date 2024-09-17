import json
import netaddr
import requests
from netaddr import iprange_to_cidrs, IPNetwork

def generate_ip_range(ip_range):
    """
    IP range to CIDR and IPNetwork type

    Args:
        ip_range: IP range

    Returns:
        an array with CIDRs
    """
    if "/" in ip_range:
        return [ip.format() for ip in [cidr for cidr in IPNetwork(ip_range)]]
    else:
        ips = []
        for generator_ip_range in [
            cidr.iter_hosts() for cidr in iprange_to_cidrs(*ip_range.rsplit("-"))
        ]:
            for ip in generator_ip_range:
                ips.append(ip.format())
        return ips