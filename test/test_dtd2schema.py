from lxml import etree
from pathlib import Path
from typing import Any
from os import remove

import sys

sys.path.append(str(Path().cwd().parent))

from dtd2schema import convert


def normalize(data: Any):
    if not data:
        return ''
    else:
        return str(data).strip()


def elements_equal(e1: etree._Element, e2: etree._Element):
    """
    Recursively compares two lxml.etree elements for equality.
    Returns True if they are identical, otherwise False.
    """
    if normalize(e1.tag) != normalize(e2.tag):
        return False
    if normalize(e1.text) != normalize(e2.text):
        return False
    if normalize(e1.tail) != normalize(e2.tail):
        return False
    if normalize(e1.attrib) != normalize(e2.attrib):
        return False
    if len(e1) != len(e2):
        return False
    return all(elements_equal(c1, c2) for c1, c2 in zip(e1, e2))


def test_xml_equality():

    with open('expected.xsd', 'r') as reader:
        expected = etree.fromstring(reader.read())
    test = etree.fromstring(convert('test.dtd', 'test.xsd'))

    remove('test.xsd')

    assert elements_equal(expected, test)


if __name__ == '__main__':
    test_xml_equality()
