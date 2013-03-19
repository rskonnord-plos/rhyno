from __future__ import print_function
from __future__ import with_statement

_BANNER_WIDTH = 79

def pretty_dict_repr(d):
    """Represent a dictionary with human-friendly text.

    Assuming d is of type dict, the output should be syntactically
    equivalent to repr(d), but with each key-value pair on its own,
    indented line.
    """
    lines = ['    {0!r}: {1!r},'.format(k, v) for (k, v) in sorted(d.items())]
    return '\n'.join(['{'] + lines + ['}'])

def section(*parts):
    """Print a section banner."""
    print('=' * _BANNER_WIDTH)
    print(*parts)
    print()

def report(description, response):
    """Print a description of the HTTP response."""
    print('-' * _BANNER_WIDTH)
    print(description)
    print()
    print(">>>>>>>>")
    print("REQUEST:")
    print(">>>>>>>>")
    print("%s %s" % (response.request.method, response.request.url))
    print('Headers:', pretty_dict_repr(response.request.headers))
    try:
        print('Request size:', len(response.request.data))
        print(response.request.data)
    except AttributeError:
        pass
    try:
        print('Files:', pretty_dict_repr(response.request.files))
    except AttributeError:
        pass
    print()
    print("<<<<<<<<<")
    print("RESPONSE:")
    print("<<<<<<<<<")
    print('Status {0}: {1!r}'.format(response.status_code, response.reason))
    print('Headers:', pretty_dict_repr(response.headers))
    print()

    print('Response size:', len(response.content))
    content_lines = list(response.iter_lines())
    for (line_number, line) in enumerate(content_lines):
        if line_number > 24:
            print('...')
            print(content_lines[-1])
            break
        print(line)
    print()
