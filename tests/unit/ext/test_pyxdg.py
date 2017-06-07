from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pytest

from pymenu.ext.pyxdg import exec_parser


class TestData(object):
    def __init__(self, input, expected):
        self.input = input
        self.expected = expected


exec_strings = [
    (r'vim',
     [['v', 'i', 'm'], []]),
    (r'"vim"',
     [['v', 'i', 'm'], []]),
    (r'vim arg1 arg2',
     [['v', 'i', 'm'], [['a', 'r', 'g', '1'], ['a', 'r', 'g', '2']]]),
    (r'vim "arg"',
     [['v', 'i', 'm'], [['a', 'r', 'g']]]),
    (r'"vim arg"',
     [['v', 'i', 'm', ' ', 'a', 'r', 'g'], []]),
    (r'"vim arg" "x y"',
     [['v', 'i', 'm', ' ', 'a', 'r', 'g'], [['x', ' ', 'y']]]),
    (r'vim %u',
     [['v', 'i', 'm'], [['%u']]]),
    (r'vim "%u"',
     [['v', 'i', 'm'], [['%u']]]),
    (r'vim "%u" foo %F',
     [['v', 'i', 'm'], [['%u'], ['f', 'o', 'o'], ['%F']]]),
    (r'vim "\$foo"',
     [['v', 'i', 'm'], [['$', 'f', 'o', 'o']]]),
    (r'"a a" b "c \" 3"',
     [['a', ' ', 'a'], [['b'], ['c', ' ', '"', ' ', '3']]]),
    (r'"a \\\\ \$f\`"',
     [['a', ' ', '\\', '\\', ' ', '$', 'f', '`'], []]),
]


@pytest.fixture(params=exec_strings)
def exec_string(request):
    return TestData(*request.param)


def test_exec_parser(exec_string):
    """
    Check that the exec_parser properly parse the input from exec_string.

    Args:
        exec_string (TestData):

    Returns:

    """
    assert exec_parser(exec_string.input) == exec_string.expected
