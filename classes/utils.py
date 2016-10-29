"""
HandBrake CLI Wrapper


Released under the MIT license
Copyright (c) 2012, Jason Millward

@category   misc
@version    $Id: 1.7.0, 2016-08-22 14:53:29 ACST $;
@author     Jason Millward
@license    http://opensource.org/licenses/MIT
"""

import re
import unicodedata


def strip_accents(s):
    """
        Remove accents from an input string

        Inputs:
            s       (Str): A string to remove accents from:

        Outputs:
            Str     a string without accents
    """
    s = s.decode('utf-8')
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')


def clean_special_chars(s):
    """
        Remove any special chars from a string.

        Inputs:
            s       (Str): A string to remove special chars from:

        Outputs:
            Str     a string without special chars
    """
    s = s.replace('\'', '_')
    s = s.replace('"', '_')
    return re.sub('\W+\.',' ', s)
