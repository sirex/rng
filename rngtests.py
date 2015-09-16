import sys
import numpy
import skidmarks


def format_dict(data, keys):
    fmt = {
        float: '%s=%.04f',
        numpy.float64: '%s=%.04f',
    }
    items = [(k, data[k]) for k in keys]
    items.extend([(k, v) for k, v in data.items() if k not in keys])
    return ' '.join([
        fmt.get(type(v), '%s=%s') % (k, v)
        for k, v in items
    ])


def main():
    orig_sample = sys.stdin.read()
    clean_sample = orig_sample.replace('\n', '')

    table = []

    result = skidmarks.gap_test(clean_sample)
    table.append(('gap_test', result['p'] < 0.05, format_dict(result, ['p', 'chi'])))

    result = skidmarks.wald_wolfowitz(clean_sample)
    table.append(('wald_wolfowitz', result['p'] < 0.05, format_dict(result, ['p'])))

    result = skidmarks.auto_correlation(clean_sample)
    table.append(('auto_correlation', result['p'] < 0.05, format_dict(result, ['p'])))

    result = skidmarks.serial_test(clean_sample)
    table.append(('serial_test', result['p'] < 0.05, format_dict(result, ['p', 'chi'])))

    print('Sample:')
    print()
    print('-' * 8)
    print(orig_sample)
    print('-' * 8)
    print()
    print('Results:')
    print()

    for name, result, params in table:
        result = 'PASSED' if result else 'FAILED'
        print('%-18s %s  %s' % (name, result, params))


if __name__ == '__main__':
    main()
