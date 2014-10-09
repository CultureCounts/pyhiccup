[![Build Status](https://travis-ci.org/nbessi/pyhiccup.svg?branch=master)](https://travis-ci.org/nbessi/pyhiccup)
[![Coverage Status](https://img.shields.io/coveralls/nbessi/pyhiccup.svg)](https://coveralls.io/r/nbessi/pyhiccup?branch=master)
pyhiccup beta
=============

Python version of clojure hiccup https://github.com/weavejester/hiccup


Pyhiccup is a library for representing HTML in Python. It uses list or tuple
to represent elements, and dict to represent an element's attributes.
Supported Python versions are:

 - 2.6
 - 2.7
 - 3.3
 - 3.4

Install
-------
TODO

Syntax
------

Here is a basic example of pyhiccup syntax:

```python
>>> from pyhiccup.core import html
>>> data = [
        ['div',
         {'class': 'a-class', 'data-y': '23'},
         ['span', 'my-text',
          ['ul', [['li', x] for x in ['coffe', 'milk', 'sugar']]]]]
    ]
>>> html(data)
>>> u'<!DOCTYPE html><html lang="en" xml:lang="en" dir="rtl"><div data-y="23" class="a-class"><span>my-text<ul><li>café<li>milk<li>sugar</ul></span></div></html>'
```

The `html` function supports different default type `html5, html4, xhtml-strict, xhtml-transitional`

```python
>>> from pyhiccup.core import html
>>> data = []
>>> html(data, etype='xhtml-strict')
>>> u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> <html lang="en" xml:lang="en" dir="rtl" xmlns="http://www.w3.org/1999/xhtml"/>'
```
You can pass arbitrary keyword arguments to the `html` they will be transformed into `html` tag attributes

```python
>>> from pyhiccup.core import html
>>> data = []
>>> html(data, etype='xhtml-strict', an-attr='foo')
>>> u'... <html an-attr="foo" lang="en" xml:lang="en" dir="rtl" xmlns="http://www.w3.org/1999/xhtml"/>'
```
Pyhiccup also provides a function to represent arbitrary XML. Arbitrary keyword arguments are also supported.

```python
>>> from pyhiccup.core import xml
>>> data = ['form-desc',
>>>         ['field', {'name': 'a_name'}],
>>>         ['field', {'name': 'a_other_name'}]]
>>> conv = xml(data, 'foo-ns', bar='an_attr')
>>> u'<?xml version="1.0" encoding="UTF-8"?><foo-ns bar="an_attr"><form-desc><field name="a_name"/><field name="a_other_name"/></form-desc></foo-ns>'
```

Helpers are available on the elements namespace. The will help you to add hyperlink, images etc.

```python
>>> from pyhiccup.element import link_to
>>> link_to(u'https://github.com/nbessi/pyhiccup', u'pyhiccup' )
>>> [u'a', {u'href': u'https://github.com/nbessi/pyhiccup'}, u'pyhiccup']
```

