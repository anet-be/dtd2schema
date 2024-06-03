"""
Some utilities for use with xmlproc.
"""

import sys
from xmlproc import xmlapp

# --- ErrorPrinter


class ErrorPrinter(xmlapp.ErrorHandler):
    """An error handler that prints out warning messages."""

    def __init__(self, locator, level=0, out=sys.stderr):
        self.locator = locator
        self.level = level
        self.out = out

    def warning(self, msg):
        if self.level < 1:
            self.out.write(
                'WARNING: %s at %s\n' % (msg, self.__get_location())
            )

    def error(self, msg):
        if self.level < 2:
            self.out.write('ERROR: %s at %s\n' % (msg, self.__get_location()))

    def fatal(self, msg):
        self.out.write('ERROR: %s at %s\n' % (msg, self.__get_location()))

    def __get_location(self):
        return '%s:%d:%d' % (
            self.locator.get_current_sysid(),
            self.locator.get_line(),
            self.locator.get_column(),
        )


# --- Various DTD tools


def load_dtd(sysid):
    from xmlproc import dtdparser, xmldtd

    dp = dtdparser.DTDParser()
    dtd = xmldtd.CompleteDTD(dp)
    dp.set_dtd_consumer(dtd)
    dp.parse_resource(sysid)

    return dtd
