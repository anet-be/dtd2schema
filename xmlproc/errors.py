# -*- coding: utf-8 -*-

# This file contains the lists of error messages used by xmlproc

# The interface to the outside world

error_lists = {}  # The hash of errors


def add_error_list(language, list):
    error_lists[language.lower()] = list


def get_error_list(language):
    return error_lists[language.lower()]


def get_language_list():
    return list(error_lists.keys())


# Errors in English

english = {
    # --- Warnings: 1000-1999
    1000: "Undeclared namespace prefix '%s'",
    1002: "Unsupported encoding '%s'",
    1003: 'Obsolete namespace syntax',
    1005: "Unsupported character number '%d' in character reference",
    1006: "Element '%s' has attribute list, but no element declaration",
    1007: "Attribute '%s' defined more than once",
    1008: 'Ambiguous content model',
    # --- Namespace warnings
    1900: "Namespace prefix names cannot contain ':'s.",
    1901: 'Namespace URI cannot be empty',
    1902: 'Namespace prefix not declared',
    1903: 'Attribute names not unique after namespace processing',
    # --- Validity errors: 2000-2999
    2000: "Actual value of attribute '%s' does not match fixed value",
    2001: "Element '%s' not allowed here",
    2002: "Document root element '%s' does not match declared root element",
    2003: "Element '%s' not declared",
    2004: "Element '%s' ended, but not finished",
    2005: 'Character data not allowed in the content of this element',
    2006: "Attribute '%s' not declared",
    2007: "ID '%s' appears more than once in document",
    2008: 'Only unparsed entities allowed as the values of ENTITY attributes',
    2009: "Notation '%s' not declared",
    2010: "Required attribute '%s' not present",
    2011: "IDREF referred to non-existent ID '%s'",
    2012: "Element '%s' declared more than once",
    2013: 'Only one ID attribute allowed on each element type',
    2014: 'ID attributes cannot be #FIXED or defaulted',
    2015: 'xml:space must be declared an enumeration type',
    2016: "xml:space must have exactly the values 'default' and 'preserve'",
    2017: "'%s' is not an allowed value for the '%s' attribute",
    2018: "Value of '%s' attribute must be a valid name",
    2019: "Value of '%s' attribute not a valid name token",
    2020: "Value of '%s' attribute not a valid name token sequence",
    2021: "Token '%s' in the value of the '%s' attribute is not a valid name",
    2022: "Notation attribute '%s' uses undeclared notation '%s'",
    2023: "Unparsed entity '%s' uses undeclared notation '%s'",
    # --- Well-formedness errors: 3000-3999
    # From xmlutils
    3000: "Couldn't open resource '%s'",
    3001: 'Construct started, but never completed',
    3002: 'Whitespace expected here',
    3003: "Didn't match '%s'",  ## FIXME: This must be redone
    3004: "One of %s or '%s' expected",
    3005: "'%s' expected",
    # From xmlproc.XMLCommonParser
    3006: 'SYSTEM or PUBLIC expected',
    3007: 'Text declaration must appear first in entity',
    3008: 'XML declaration must appear first in document',
    3009: 'Multiple text declarations in a single entity',
    3010: 'Multiple XML declarations in a single document',
    3011: 'XML version missing on XML declaration',
    3012: 'Standalone declaration on text declaration not allowed',
    3045: "Processing instruction target names beginning with 'xml' are reserved",
    3046: 'Unsupported XML version',
    # From xmlproc.XMLProcessor
    3013: 'Illegal construct',
    3014: "Premature document end, element '%s' not closed",
    3015: 'Premature document end, no root element',
    3016: "Attribute '%s' occurs twice",
    3017: 'Elements not allowed outside root element',
    3018: "Illegal character number '%d' in character reference",
    3019: 'Entity recursion detected',
    3020: 'External entity references not allowed in attribute values',
    3021: "Undeclared entity '%s'",
    3022: "'<' not allowed in attribute values",
    3023: "End tag for '%s' seen, but '%s' expected",
    3024: "Element '%s' not open",
    3025: "']]>' must not occur in character data",
    3027: 'Not a valid character number',
    3028: 'Character references not allowed outside root element',
    3029: 'Character data not allowed outside root element',
    3030: 'Entity references not allowed outside root element',
    3031: 'References to unparsed entities not allowed in element content',
    3032: 'Multiple document type declarations',
    3033: 'Document type declaration not allowed inside root element',
    3034: 'Premature end of internal DTD subset',
    3042: 'Element crossed entity boundary',
    # From xmlproc.DTDParser
    3035: 'Parameter entities cannot be unparsed',
    3036: 'Parameter entity references not allowed in internal subset declarations',
    3037: 'External entity references not allowed in entity replacement text',
    3038: "Unknown parameter entity '%s'",
    3039: 'Expected type or alternative list',
    3040: 'Choice and sequence lists cannot be mixed',
    3041: 'Conditional sections not allowed in internal subset',
    3043: 'Conditional section not closed',
    3044: "Token '%s' defined more than once",
    # next: 3047
    # From regular expressions that were not matched
    3900: 'Not a valid name',
    3901: 'Not a valid version number (%s)',
    3902: 'Not a valid encoding name',
    3903: 'Not a valid comment',
    3905: 'Not a valid hexadecimal number',
    3906: 'Not a valid number',
    3907: 'Not a valid parameter reference',
    3908: 'Not a valid attribute type',
    3909: 'Not a valid attribute default definition',
    3910: 'Not a valid enumerated attribute value',
    3911: 'Not a valid standalone declaration',
    # --- Internal errors: 4000-4999
    4000: 'Internal error: Entity stack broken',
    4001: 'Internal error: Entity reference expected.',
    4002: 'Internal error: Unknown error number.',
    4003: 'Internal error: External PE references not allowed in declarations',
    # --- XCatalog errors: 5000-5099
    5000: 'Uknown XCatalog element: %s.',
    5001: 'Required XCatalog attribute %s on %s missing.',
    # --- SOCatalog errors: 5100-5199
    5100: 'Invalid or unsupported construct: %s.',
}

# Updating the error hash

add_error_list('en', english)
