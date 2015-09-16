#!/usr/bin/env python3

import time
import argparse
import collections


def expensive_operation(n):
    for i in range(n):
        1 / 3


def get_exec_time(n):
    stamp = time.time()
    expensive_operation(n)
    return time.time() - stamp


def normalize(sample):
    smin, smax = min(sample), max(sample)
    return [(x - smin) / (smax - smin) for x in sample]


def drop(s, items):
    return [x for x in s if x not in items]


def check_quality(norm, threshold):
    total = len(norm)
    norm = [int(x * 1000) for x in norm]
    unique = len(set(norm))
    percent = 100 / total * unique
    if percent < threshold:
        raise ValueError()
    else:
        return norm


def get_random_number(threshold=80, n_samples=10, start_num_of_ops=100):
    n = start_num_of_ops
    number = 0
    while number == 0:
        sample = [get_exec_time(n) for i in range(n_samples)]
        try:
            norm = check_quality(normalize(sample), threshold)
        except (ZeroDivisionError, ValueError):
            n += 1
            number = 0
        else:
            norm = drop(norm, {0, 1000})
            number = collections.Counter(norm).most_common()[-1][0]
    return number % 2


def gen_random_numbers(count=32, threshold=80, n_samples=10, start_num_of_ops=100):
    """Yields specified `count` of numbers in 0-1 range."""
    for i in range(count):
        yield get_random_number(threshold, n_samples, start_num_of_ops)


def main():
    """
    This random number generator generates binary numbers.

    Random numbers are taken by testing how much time it takes for CPU to
    calculate an expensive calculation. Expensive calculation is performaned
    many times, starting with number specified in --start-num-of-ops. This
    number is automatically increased if percent of unique numbers specified by
    --threshold is not satisfied.

    Expensive calculation is performed several times, how many times is
    specified by --samples parameter. The second last measurment is taken and
    it's normalized value is checked if this is event or odd number accordingly
    returning 0 or 1.

    This is how single random number is produced. --count parameter specifies
    how meny numbers should be generated.

    """

    parser = argparse.ArgumentParser(usage=main.__doc__)
    parser.add_argument('-c', '--count', type=int, default=32, help='Number of digits to generate.')
    parser.add_argument('-t', '--threshold', type=int, default=80, help=(
        'Percent of unique values between time measurements.'
    ))
    parser.add_argument('-s', '--samples', type=int, default=10, help='Number of samples to take.')
    parser.add_argument('-n', '--start-num-of-ops', type=int, default=100, help=(
        'Initial number of operations that will be measured.'
    ))
    parser.add_argument('-w', '--wrap', type=int, default=140, help='Wrap new line at specified number of digits.')
    args = parser.parse_args()

    for i, n in enumerate(gen_random_numbers(args.count, args.threshold, args.samples, args.start_num_of_ops), 1):
        print(n, end='')

        # Split random number into lines
        if i % args.wrap == 0:
            print()


if __name__ == '__main__':
    main()
