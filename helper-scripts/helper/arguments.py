# -*- coding: utf-8 -*-
"""Argument reading functions

This module offers some functions to read arguments from command line.

"""
import sys

from typing import List


def read_parameter_string(number: int, default: str = None) -> str:
    """Returns the value from argument <number> as string.

    Parameters
    ----------
    number : int
        The wanted number of argument.
    default : str
        The default value if no argument is given.

    Returns
    -------
    str
        Returns the value from argument as string.

    """
    value: str = default

    if len(sys.argv) > number:
        value = sys.argv[number]

    return value


def read_parameter_integer(number: int, default: int = None) -> int:
    """Returns the value from argument <number> as integer.

    Parameters
    ----------
    number : int
        The wanted number of argument.
    default : int
        The default value if no argument is given.

    Returns
    -------
    int
        Returns the value from argument as integer.

    """
    value: int = default

    if len(sys.argv) > number:
        value = int(sys.argv[number])

    return value


def read_parameter_boolean(number: int, default: bool = False) -> bool:
    """Returns the value from argument <number> as boolean.

    Parameters
    ----------
    number : int
        The wanted number of argument.
    default : bool
        The default value if no argument is given.

    Returns
    -------
    bool
        Returns the value from argument as integer.

    """
    value: bool = '1' if default else '0'

    allowed = ['1', '0', 'True', 'False']

    if len(sys.argv) > number:
        value = str(sys.argv[number])

    if value not in allowed:
        raise Exception('The given boolean value \'%s\' is not in the allowed list %s' % (value, allowed))

    if value == '1' or value == 'True':
        value = True
    else:
        value = False

    return value


def read_parameter(parameter_type: str = 'string', number: int = 1, default = None, options: List = None) -> object:
    """Returns the value from argument <number> as <parameter_type>.

    Parameters
    ----------
    parameter_type : str
        The type to parse from argument.
    number : int
        The wanted number of argument.
    default : object
        The default value if no argument is given.
    options : List
        An optional option list that is allowed to parse from arguments.

    Returns
    -------
    object
        Returns the value from argument as <parameter_type>.

    """
    switcher = {
        'string': read_parameter_string,
        'integer': read_parameter_integer,
        'boolean': read_parameter_boolean,
    }

    func = switcher.get(parameter_type, lambda: 'Invalid type "%s"' % parameter_type)
    value = func(number=number, default=default)

    if options is not None:
        if value not in options:
            raise Exception('The parsed value \'%s\' is not inside %s' % (value, options))

    return value
