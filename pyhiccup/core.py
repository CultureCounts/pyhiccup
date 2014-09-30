# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Nicolas Bessi
#    Copyright 2014
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License 3
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging
import copy
from itertools import chain

from .page import get_doc_type, get_html_enclosing_tag, get_xml_enclosing_tag
from .page import XMl_DECLARATION

_logger = logging.getLogger('pyhiccup.convert')

TREE_TYPE = (list, tuple)


def format_attributes(attributes):
    """Transform dict to XMl/HTMl attributes

    {'class': 'a-class', 'data-sel': 'a-sel'}
    returns ``class="a-class" data-sel="a-sel"``

    :param attributes: dict of XML/HMTL attributes to transform
                       to string
    :type attributes: dict

    :return: a list of attributes eg. ``class="a-class" data-sel="a-sel"``
    :rtype: str

    """
    output = []
    for item in attributes.items():
        output.append('%s=\"%s\"' % item)
    return " %s" % ' '.join(output)


def _convert_tree(node):
    """Transform a list describing HTML leaf to a list of HTML string

    ready to be joined

    :param args: leaf list describing HTML
    :type args: list, tuple

    :return: a list of string
    :rtype: list

    """
    btype = node[0]
    rest = node[1:]
    attrs = u''
    inner_trees = []
    inner_element = u''
    for element in rest:
        if not element:
            continue
        if isinstance(element, TREE_TYPE):
            if isinstance(element[0], TREE_TYPE):
                inner_trees.extend(element)
            else:
                inner_trees.append(element)
        elif isinstance(element, dict):
            attrs = format_attributes(element)
        else:
            inner_element = element
    if inner_element or inner_trees:
        yield u'<%s%s>' % (
            btype,
            attrs,
        )
        yield inner_element
        if inner_trees:
            for ext in inner_trees:
                for x in _convert_tree(ext):
                    yield x
            yield u'</%s>' % btype
    else:
        yield u'<%s%s/>' % (
            btype,
            attrs,
        )


def _inclose_page(declaration, enclosing_tag, value):
    """Take a page code and a value
    and inclose value into page code
    :param declaration: Declaration of the document
    :type declaration: str
    :param enclosing_tag: page code list type e.g. `['html', {'xmlns':...}]`
    :type enclosing_tag: str
    :param value: the list to be converted to *ML
    :type value: str

    """
    to_convert = copy.deepcopy(enclosing_tag)
    to_convert.append(value)
    converted = chain(
        [declaration],
        _convert_tree(to_convert)
    )
    if _logger.getEffectiveLevel() == logging.DEBUG:
        _logger.debug(
            list(chain([declaration],
                       _convert_tree(to_convert)))
        )
    return converted


def html(value, etype='html5', **kwargs):
    """Transform a list describing HTML to raw HTML

    :param value: list of list describing HTML
    :type value: list, tuple
    :param etype: enclosing type `html5, html4, xhtml-strict,
                  xhtml-transitional`
    :type etype: str
    :param kwargs: dict of enclosing tag attributes
    :type kwargs: dict
    :return: HTML string representation
    :rtype: str, unicode

    """
    declaration = get_doc_type(etype)
    enclosing_tag = get_html_enclosing_tag(etype)
    converted = _inclose_page(declaration, enclosing_tag, value)
    return ''.join(converted)


def xml(value, etype, **kwargs):
    """Transform a list describing XML to raw XML

    :param value: list of list describing XML
    :type value: list, tuple
    :param etype: enclosing type the root tag name
    :type etype: str
    :param kwargs: dict of enclosing tag attributes
    :type kwargs: dict
    :return: XML string representation
    :rtype: str, unicode

    """
    declaration = XMl_DECLARATION
    enclosing_tag = get_xml_enclosing_tag(etype, **kwargs)
    converted = _inclose_page(declaration, enclosing_tag, value)
    return ''.join(converted)
