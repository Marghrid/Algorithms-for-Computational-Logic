#!/bin/bash
#
# File:  chk_all.sh
# Author:  mikolas
# Created on:  Mon Oct 14 14:14:24 WEST 2019
# Copyright (C) 2019, Mikolas Janota
#
if [[ $# != 2 ]] ; then
    echo "Usage: $0 <solver> <directory with samples>"
    exit 1
fi

solver="$1"
tests="$2"

fail=0
for f in ${tests}/*.smp; do
    echo $f '==='
    if "${solver}" <"${f}" 2>/dev/null | ./chk.py "$f"; then
        echo '   ==='
    else
        let fail=${fail}+1
        break
    fi
done

if [ $fail -eq 0 ]; then
    echo 'All OK - GREAT SUCCESS'
fi
