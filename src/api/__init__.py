#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __init__.py
# response format:
# 1）al data format: a json list like [{...}, {....}]
# 2) delta data format: json like {....}
if __name__ == '__main__':
    print('run as main')
else:
    __all__ = ['utils', 'the_block', 'etc', 'http_utils_']
    print('package api init.')
