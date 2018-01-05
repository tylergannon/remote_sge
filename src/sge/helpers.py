# -----------------------------------------------------------
#  Copyright (C) 2009 StatPro Italia s.r.l.
#
#  StatPro Italia
#  Via G. B. Vico 4
#  I-20123 Milano
#  ITALY
#
#  phone: +39 02 96875 1
#  fax:   +39 02 96875 605
#
#  email: info@riskmap.net
#
#  This program is distributed in the hope that it will be
#  useful, but WITHOUT ANY WARRANTY; without even the
#  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#  PURPOSE. See the license for more details.
# -----------------------------------------------------------
#
#  Author: Enrico Sirola <enrico.sirola@statpro.com>
#  Author: Dan Blanchard <dan.blanchard@gmail.com>

"""
internal helpers
"""

from __future__ import absolute_import, print_function, unicode_literals

import sys
from collections import namedtuple
from ctypes import (byref, c_uint, create_string_buffer, POINTER, pointer,
                    sizeof)

from sge.const import ATTR_BUFFER, ENCODING, NO_MORE_ELEMENTS, QSubOptions
from sge.errors import error_buffer
from datetime import datetime

_BUFLEN = ATTR_BUFFER


class QSubOption(object):
    """
    Descriptor for properties on the JobTemplate class, to translate DRMAA options
    to properly formatted qsub options.

    A qsub option is internally identified by the option name as it is seen
    on the command line, e.g. "-V".

    Setting the attribute on a JobTemplate will result in the value being encoded
    as needed (e.g. boolean values become yes/no, etc), and then stored in the
    :func:`drmaa.JobTemplate.options` dictionary, using *option_name* as its key.

    """
    def __init__(self, option_name, type_converter=None):
        """
        Args:
            option_name (str): the name of the qsub_ option, as described
                `on the qsub man page`__.
            type_converter

        .. _qsub: http://gridscheduler.sourceforge.net/htmlman/htmlman1/qsub.html
        __ qsub_
        """
        self.option_name = option_name
        self.converter = type_converter

    def __get__(self, instance, _):
        raw_value = instance.qsub_options[self.option_name]
        if self.converter:
            return self.converter.from_string(raw_value)
        else:
            return raw_value

    def __set__(self, instance, value):
        print(instance)
        if self.converter:
            value = self.converter.to_string(value)
        elif isinstance(value, str):
            value = value.encode(ENCODING)

        instance.qsub_options[self.option_name] = value

    def __delete__(self, instance):
        print( "deleted in descriptor object")
        del instance.qsub_options[self.option_name]



class QSubTypeConverter(object):
    """
    Abstract class representing how to convert between int,
    boolean or dict types, and their string representations
    that are accepted by qsub_.

    .. _qsub: http://gridscheduler.sourceforge.net/htmlman/htmlman1/qsub.html
    """
    @staticmethod
    def to_string(value):
        pass
    @staticmethod
    def from_string(value):
        pass

class DictionaryConverter(QSubTypeConverter):
    @staticmethod
    def to_string(dictionary):
        # result = []
        # for item in dictionary.items():
        #     result.append("%s=%s" % item)
        return ','.join(["%s=%s" % item for item in dictionary.items()])
    @staticmethod
    def from_string(value):
        return dict(item.split("=") for item in value.split(","))

class DateTimeConverter(QSubTypeConverter):
    """
    Converts a python :class:`~datetime.datetime` into a string in the format
    YYYYMMDDhhmm.SS, as described in the sge datetype_ specification.

    .. _datatype: http://gridscheduler.sourceforge.net/htmlman/htmlman1/sge_types.html
    """
    FORMAT = r"%Y%m%d%H%M.%S"
    @staticmethod
    def to_string(datetime):
        return datetime.strftime(DateTimeConverter.FORMAT)
    @staticmethod
    def from_string(string):
        return datetime.strptime(string, DateTimeConverter.FORMAT)


class BoolConverter(QSubTypeConverter):
    """Helper class to convert to/from bool attributes."""
    TRUE = r'yes'
    FALSE = r'no'

    @staticmethod
    def to_string(value):
        if value:
            return BoolConverter.TRUE
        else:
            return BoolConverter.FALSE
        
    @staticmethod
    def from_string(value):
        return value == BoolConverter.TRUE


class IntConverter(QSubTypeConverter):

    """Helper class to convert to/from int attributes."""
    @staticmethod
    def to_string(value):
        return str(value)

    @staticmethod
    def from_string(value):
        return int(value)

