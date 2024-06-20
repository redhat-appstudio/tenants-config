# Assisted installer

Each folder represents a different release process / product.

* New branches that represents a release (e.g. release-v2.10) should be defined in `$product/apps/$branch/`
  * There should be one RPA per release
  * Each RP should target the associated RPA (to have the right product_version etc)
* New releases (e.g. v2.10.5) should be created in `$product/releases/`
* Files and resources are named according to the convention: `$component-$product-$branch`
  * `main` & `master` branches are gathered as `main` for simplicity

## Main branches

If several products reuse the same branch (for example `main` for their integration), we could consider factorize the build.
It is currently not done because it would imply to chose a Dockerfile that matches _all_ products.

## SaaS

Resources related to SaaS deployment & releases

Only one release is maintained at a time, but it could target `master` or `cloud_hotfix_releases` branches.

Without the `cloud_hotfix_releases` branch, `assisted-service` & `assisted-image-service` could be released together as a single application (of 2 components).
That would be more close to our current release process. It should be possible to setup once there is a dedicated branch per release.

Applications that are auto-released
* assisted-events-stream
* auto-report
* bug-master-bot
* jira-unfurl-bot
* prow-jobs-scraper

Applications that are not auto-released
* assisted-image-service
* assisted-service (main & hotfix)
