#!/bin/bash

echo "make:"
make ; ret=$?
if [ $ret -ne 0 ] ; then echo "failure" ; exit 1 ; fi

if [[ "$(uname)" == "Linux" ]] ; then
  executable="$(find . -executable -type f)"
else
  executable="$(find . -perm +111 -type f)"
fi

echo "executable: $executable"
if [ -z "$executable" ] ; then
  echo "no executable found"
  exit 1
fi

echo "run pytest:"
env PYTHONPATH=".:$PYTHONPATH" python3 -m pytest -v ; ret=$?
if [ $ret -ne  0 ] ; then echo "failure" ; exit 1 ; fi

echo "make test:"
make test ; ret=$?
if [ $ret -ne 0 ] ; then echo "failure" ; exit 1 ; fi

echo "make clean"
make clean ; ret=$?
if [ $ret -ne 0 ] ; then echo "failure" ; exit 1 ; fi

sofiles="$(ls *.so)"
echo "sofiles: $sofiles"
if [ -n "$sofiles" ] ; then
    echo "shared object is not deleted"
    exit 1
fi
