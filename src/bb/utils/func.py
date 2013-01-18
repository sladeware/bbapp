#!/usr/bin/env python

from functools import partial

def partials(funcs, *args, **kwargs):
  return map(lambda func: partial(func, *args, **kwargs), funcs)
