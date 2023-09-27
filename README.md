# tenants-config

## About

This repository contains AppStudio configuration for Redhat users.
Each directory in `cluster/${CLUSTER}/${WORKSPACE_TYPE}` maps to namespace on $CLUSTER/

Tenants directories can contain sub directories, but only the top level kustomization directory
will get build. It means that only resources referenced in the top level kustomization file will
be included in the built tenant directory (thus you won't see any sub directories in the tenants
directory in the auto-generated directory).

## Making Changes

After making changes, run `build-manifests.sh` and commit the `auto-generated`
directory (in addition to your changes).

Change from the `auto-generated` directory will get automatically deployed.
