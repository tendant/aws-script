# aws-script
Python scripts for managing AWS service using boto.

## Delete launch configuration

    python autoscaling/delete-old-launch-configuration.py REGION PATTERN

Delete k oldest launch configuration which name matches given PATTERN
in given REGION, keep at least recent 25 launch configurations
