if [ $# != 1 ] ; then
    echo "Usage: $0 <directory with samples>"
    exit 1
fi

solver='python3 proj3_bool_compare.py'
tests="$1"

fail=0
for f in ${tests}/*.smp; do
    echo '===' $f '==='
    ${solver} < "${f}"
done

if [ $fail -eq 0 ]; then
    echo 'All OK - GREAT SUCCESS'
fi
