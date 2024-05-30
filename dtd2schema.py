"""
This script converts DTDs to XSD Schemas,
according to https://www.w3.org/TR/xmlschema11-1/

It was originally developed as part of a Python2 module,
and partly ported to Python3 with the `2to3` utility (lib2to3).
"""

import sys
import os.path
from xml.sax.saxutils import escape

from xmlproc import xmldtd


# ===== CONSTANTS


USAGE = """
Usage:

  python dtd2schema.py <inputfile> [<outputfile> --debug]

  Input file names can be URLs.

  If the output file name is omitted, it will be inferred from the
  input file name. Note that this inference does not work for URLs.
"""

VERSION = '0.3'

DECL_MAP = {
    '#REQUIRED': 'required',
    '#IMPLIED': 'optional',
    '#DEFAULT': 'optional',
    '#FIXED': 'fixed',
}

TYPE_MAP = {'CDATA': 'xs:string'}


# ===== UTILITY FUNCTIONS


class CountingDict:
    def __init__(self):
        self._items = {}

    def count(self, item):
        self._items.setdefault(item, 0)
        self._items[item] = self._items[item] + 1

    def clear(self):
        self._items = {}

    def keys(self):
        return list(self._items.keys())

    def __getitem__(self, item):
        return self._items[item]

    def __delitem__(self, item):
        del self._items[item]


def escape_attr_value(value: str) -> str:
    """
    Escapes special characters in an XML attribute value.
    Uses sax.escape with some additional entities.
    """
    return escape(value, entities={"'": '&apos;', '"': '&quot;'})


def write_attr(out, attr):
    value = attr.get_default()
    if value == None:
        value = ''
    else:
        value = ' default="%s"' % escape_attr_value(value)

    # to do: xsd should be string, instead of CDATA and stuff; so make map
    attrtype = attr.get_type()
    if isinstance(attrtype, list):
        out.write(
            '      <xs:attribute name="%s" use="%s"%s>\n'
            % (attr.get_name(), DECL_MAP[attr.get_decl()], value)
        )
        out.write('        <xs:simpleType>\n')
        out.write('            <xs:restriction base="xs:NMTOKEN">\n')
        for token in attrtype:
            out.write('          <xs:enumeration value="%s"/>\n' % token)
        out.write('            </xs:restriction>\n')
        out.write('        </xs:simpleType>\n')
        out.write('      </xs:attribute>\n')
    else:
        attrtype = TYPE_MAP.get(attr.get_type())
        out.write(
            '      <xs:attribute name="%s" type="%s" use="%s"%s/>\n'
            % (attr.get_name(), attrtype, DECL_MAP[attr.get_decl()], value)
        )


def write_attributes(out, elem):
    attrnames = elem.get_attr_list()
    for attrname in attrnames:
        write_attr(out, elem.get_attr(attrname))


def write_element_type(out, elem):
    cm = elem.get_content_model()
    if cm == ('', [('#PCDATA', '')], ''):
        if not elem.get_attr_list():
            # to do: check again
            # out.write('    <xs:simpleType ref="string"/>\n')
            # out.write('    <xs:simpleType/>\n')
            pass
        else:
            out.write(
                # to do: check again
                # '    <xs:complexType base="string" derivedBy="extension">\n'
                '    <xs:complexType>\n'
            )
            write_attributes(out, elem)
            out.write('    </xs:complexType>\n')
        return

    content = ''

    out.write('    <xs:complexType%s>\n' % content)
    if cm == None:
        out.write('    <xs:sequence>\n')
        out.write('    <xs:any processContents="skip"/>\n')
        out.write('    </xs:sequence>\n')
    elif cm != ('', [], ''):
        write_cm(out, cm)

    write_attributes(out, elem)
    out.write('    </xs:complexType>\n')


def write_cm(out, cm):
    (sep, cps, mod) = cm

    if sep == '|':
        wrapper = 'choice'
    else:
        wrapper = 'sequence'

    out.write('      <xs:%s>\n' % wrapper)
    for cp in cps:
        if len(cp) == 2:
            (name, mod) = cp
            if name == '#PCDATA':
                continue

            if mod == '?':
                occurs = ' minOccurs="0"'
            elif mod == '*':
                occurs = ' minOccurs="0" maxOccurs="unbounded"'
            elif mod == '+':
                occurs = ' minOccurs="1" maxOccurs="unbounded"'
            else:
                occurs = ''

            out.write('        <xs:element ref="%s"%s/>\n' % (name, occurs))
        elif len(cp) == 3:
            write_cm(out, cp)
        else:
            out.write('        <!-- %s -->\n' % (cp,))

    out.write('      </xs:%s>\n' % wrapper)


def convert(infile: str, outfile: str, modifiers: dict = {}) -> bytes:
    """
    Wrapper for conversion.
    """
    # Load DTD

    if modifiers.get('debug'):
        print('Loading DTD...')

    dtd = xmldtd.load_dtd(infile)

    # Find attribute groups

    if modifiers.get('debug'):
        print('Doing reverse-engineering...')

    # Write out schema

    if modifiers.get('debug'):
        print('Writing out schema')

    with open(outfile, 'w') as out:

        out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        out.write('<!-- Converted from a DTD by dtd2schema.py -->\n')
        out.write(
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">\n\n'
        )

        for elemname in dtd.get_elements():
            elem = dtd.get_elem(elemname)
            out.write('  <xs:element name="%s">\n' % elemname)
            write_element_type(out, elem)
            out.write('  </xs:element>\n\n')

        notations = dtd.get_notations()

        if notations:

            for notname in notations:
                (pubid, sysid) = dtd.get_notation(notname)
                if sysid == None:
                    sysid = ''
                else:
                    sysid = ' system="%s"'

                out.write(
                    '  <xs:notation name="%s" public="%s"%s>\n'
                    % (notname, pubid, sysid)
                )

        out.write('</xs:schema>\n')

    with open(outfile, 'rb') as reader:
        return reader.read()


def argparse() -> tuple[str, str, dict]:
    """
    Interpreting command-line arguments and modifiers
    """

    modifiers = {}

    for arg in sys.argv:
        if arg.startswith('--'):
            modifier = arg.lstrip('-')
            modifiers[modifier] = True
            sys.argv.remove(arg)

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(USAGE)
        sys.exit(1)

    infile = sys.argv[1]
    if len(sys.argv) == 3:
        outfile = sys.argv[2]
    else:
        ext = os.path.splitext(infile)[1]
        outfile = os.path.split(infile)[1]
        outfile = outfile[: -len(ext)] + '.xsd'

    return (infile, outfile, modifiers)


if __name__ == '__main__':

    infile, outfile, modifiers = argparse()
    _ = convert(infile, outfile, modifiers)
