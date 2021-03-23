#!/bin/bash
rm -rf $BUILDTEST_ROOT/var
rm -rf ~/.buildtest/
coverage run -m pytest
coverage report
