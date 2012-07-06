#!/bin/bash

# clean up previous results:
rm -rf htmlcov
mkdir htmlcov
rm .coverage

# I do not want coverage data for my South migrations:
PARMS=--omit='*migrations*'

# run the tests and collect coverage, only for our applications
coverage run manage.py test

# generate plaintext and HTML report
echo "----------------------------"
echo "Coverage results:"
coverage report $PARMS
coverage html $PARMS
echo "HTML report generated in htmlcov/index.html"

# optionally display an HTML report
if [ "$1" == "-f" ]
then
   firefox htmlcov/index.html
fi
