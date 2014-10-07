#!/usr/bin/env bash
echo '2 ** 10 items'
echo -n '2 slices: '
python -m timeit -s'import speedtest' 'speedtest.test(2, 10, None)'
echo -n '0 slices: '
python -m timeit -s'import speedtest' 'speedtest.test(0, 10, None)'
echo -n "Lenski's: "
python -m timeit -s'import speedtest' 'speedtest.test(1, 10, None)'
echo -n "recipe:   "
python -m timeit -s'import speedtest' 'speedtest.test(3, 10, None)'
echo

echo '2 ** 15 items'
echo -n '2 slices: '
python -m timeit -s'import speedtest' 'speedtest.test(2, 15, None)'
echo -n '0 slices: '
python -m timeit -s'import speedtest' 'speedtest.test(0, 15, None)'
echo -n "Lenski's: "
python -m timeit -s'import speedtest' 'speedtest.test(1, 15, None)'
echo -n "recipe:   "
python -m timeit -s'import speedtest' 'speedtest.test(3, 15, None)'
echo
