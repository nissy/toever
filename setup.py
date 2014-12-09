from setuptools import setup, find_packages
import sys
import toever.config as config

install_requires = ['evernote', 'clint', 'chardet', 'keyring']

if sys.version_info < (2, 7):
    install_requires.append('argparse')

setup(name='toever',
      version=config.version,
      description='Evernote command line tool',
      author='Yoshihiko Nishida',
      author_email='nishida@ngc224.org',
      url='https://github.com/ngc224/toever',
      packages=find_packages(),
      install_requires=install_requires,
      entry_points="""
      [console_scripts]
      toever = toever.toever:main
      """,)
