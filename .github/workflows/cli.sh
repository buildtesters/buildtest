#!/bin/bash
set -veo

# tutorial check
buildtest --help

# Building Test
buildtest build -b $BUILDTEST_ROOT/tutorials/hello_world.yml
buildtest build -b $BUILDTEST_ROOT/tutorials/hello_world.yml -b $BUILDTEST_ROOT/general_tests/configuration
buildtest build -b general_tests/configuration -x general_tests/configuration/ulimits.yml

# this command will fail
buildtest build -b general_tests/configuration -x general_tests/configuration || true

buildtest build -b tutorials/sleep.yml
buildtest build -b tutorials/sleep.yml --timeout=1
buildtest build -b tutorials/sleep.yml --timeout=5

buildtest build -t network

# Querying Test Report
buildtest report path
buildtest report list
buildtest rt --fail
buildtest rt --pass
buildtest rt --fail --row-count
buildtest rt --pager
buildtest rt --filter tags=network --format name,id,tags
buildtest rt --helpfilter
buildtest rt --helpformat

# Inspecting Test
buildtest it list
buildtest it list -b
buildtest it name hello_world circle_area
buildtest it query -o -e -t hello_world
buildtest path hello_world
buildtest path -o hello_world
buildtest path -e hello_world

# Interacting with Buildspecs
buildtest buildspec find --rebuild -q
buildtest buildspec find
buildtest buildspec find --tags
buildtest buildspec find --filter tags=python
buildtest buildspec find --filter tags=python --format name,tags,description
buildtest buildspec summary
buildtest bc validate -b tutorials/hello_world.yml -b general_tests/configuration
buildtest bc validate -t python
# this command will fail
buildtest bc validate -b tutorials/invalid_executor.yml || true
buildtest bc show sleep hello_world
buildtest bc show --theme emacs sleep
# this command will fail
buildtest bc find invalid || true


# query details from buildtest configuration
buildtest config path
buildtest cg view
buildtest cg executors list
buildtest cg executors list --json
buildtest cg executors list --yaml