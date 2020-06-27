# -*- coding: utf-8 -*-
import configparser
import functools
import re
import textwrap


def is_not_empty(f):
    """Assert generator yields value at least once."""

    @functools.wraps(f)
    def wrapper():
        count = 0
        for value in f():
            count += 1
            yield value
        assert count > 0

    return wrapper


def tox_info(var):
    """Get variable value from all sections in the tox.ini file."""
    ini_parser = configparser.ConfigParser()
    ini_parser.read("tox.ini")
    for section in ini_parser:
        if var in ini_parser[section]:
            value = textwrap.dedent(ini_parser[section][var].strip())
            yield section, value


def tox_parse_envlist(string):
    """Parse tox environment list with proper comma escaping."""
    escaped = string
    while re.search(r"({[^,}]*),", escaped):
        escaped = re.subn(r"({[^,}]*),", r"\1:", escaped)[0]
    parts = escaped.split(",")
    return [re.subn(r":", ",", p)[0].strip() for p in parts]
