#!/usr/bin/env python
from setuptools import setup
from pip.req import parse_requirements
install_reqs = parse_requirements('requirements.txt', session=False)
requirements = [str(ir.req) for ir in install_reqs]
setup(
  name             = 'GrowBot',
  version          = '0.0.0',
  description      = '',
  author           = 'Josiah Kerley',
  author_email     = 'josiahkerley.@gmail.com',
  url              = '',
  install_requires = requirements,
  packages         = [
    'GrowBot'
  ]
)