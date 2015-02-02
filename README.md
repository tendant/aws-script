# aws-script
AWS  python/boto scripts

## Delete launch configuration

    python autoscaling/delete-old-launch-configuration.py REGION PATTERN

Delete launch oldest launch configuration which name matches given
PATTERN in given REGION, keep at least recent 25 launch configurations
