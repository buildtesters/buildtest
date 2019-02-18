#!/bin/sh
buildtest --help > docs/scripts/how_to_use_buildtest/buildtest-help.txt

# Show Subcommand
buildtest show --help > docs/scripts/show_subcommand/help.txt
buildtest show -c > docs/scripts/show_subcommand/configuration.txt
buildtest show -k singlesource > docs/scripts/show_subcommand/singlesource.txt

# build Subcommand
buildtest build --help > docs/scripts/build_subcommand/help.txt
echo "buildtest build --package gcc --testdir $HOME/tmp/" > docs/scripts/build_subcommand/custom_test_dir.txt
buildtest build --package gcc --testdir $HOME/tmp/ >> docs/scripts/build_subcommand/custom_test_dir.txt
echo "buildtest build --package coreutils" > docs/scripts/build_subcommand/coreutils.txt
buildtest build --package coreutils >> docs/scripts/build_subcommand/coreutils.txt

buildtest build -S compilers > docs/scripts/build_subcommand/suite/build_compilers.txt
buildtest run -S compilers > docs/scripts/build_subcommand/suite/run_compilers.txt

buildtest build -S openmp > docs/scripts/build_subcommand/suite/build_openmp.txt
buildtest run -S openmp > docs/scripts/build_subcommand/suite/run_openmp.txt

# List Subcommand
buildtest list --help > docs/scripts/list_subcommand/help.txt

# Find Subcommand
buildtest find --help > docs/scripts/find_subcommand/help.txt
buildtest find -fc all > docs/scripts/find_subcommand/find_allyaml.txt
buildtest find -fc hello > docs/scripts/find_subcommand/find_hello_yaml.txt
