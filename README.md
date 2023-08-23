# tenants-config

## About

This repository contains AppStudio configuration for Redhat users.
Each directory in `cluster/${CLUSTER}` maps to namespace on $CLUSTER/

## Making Changes

After making changes, run `build-manifests.sh` and commit the `auto-generated`
directory (in addition to your changes).

Change from the `auto-generated` directory will get automatically deployed.
