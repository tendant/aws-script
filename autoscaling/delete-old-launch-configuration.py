#!/usr/bin/env python

import re
import sys
import boto.ec2.autoscale
from boto.ec2.autoscale import LaunchConfiguration

def main(REGION, pattern):
    print('Checking new launch configuration in the "{0}" region.'.format(REGION))
    asConnection = boto.ec2.autoscale.connect_to_region(REGION)

    lc = asConnection.get_all_launch_configurations(max_records=100)
    print('Total number of launch configuration: {0}'.format(len(lc)))
    target_lc = find_target_lc(lc, pattern)
    print('Number of launch configuration for pattern ("{0}"): {1}'.format(pattern, len(target_lc)))
    delete_oldest_k_lc(asConnection, target_lc, 10)

def delete_lc (conn, lc):
    print('Deleting launch configuration: {0}'.format(lc.name))
    conn.delete_launch_configuration(lc.name)

def find_target_lc (lc, pattern):
    target_lc = filter(lambda x: re.search(pattern, x.name), lc)
    return target_lc

def delete_oldest_k_lc (conn, lc, k):
    """Delete oldest k launch configuration which matches given pattern, keep at least recent 10 launch configuration"""
    min_items = 25;
    num_to_be_deleted = min(k, len(lc) - min_items);
    if (num_to_be_deleted < 1):
        print('Nothing to delete, count of launch configuration: {0}'.format(len(lc)))
        return None
    else:
        sorted_lc = sorted(lc, key=lambda lc: lc.created_time)
        to_be_deleted_lc = sorted_lc[:num_to_be_deleted]
        print('Number of launch configuration to be deleted: {0}'.format(len(to_be_deleted_lc)))
        map(lambda x: delete_lc(conn, x), to_be_deleted_lc)
        return None
    
if __name__ == "__main__":
    if (len(sys.argv) != 3):
        exit('Usage: {0} region pattern'.format(sys.argv[0]))
    else:
        main(sys.argv[1], sys.argv[2])
