from setuptools import setup, find_packages
import sys


install_requires = ['evernote', 'clint']

if sys.version_info < (2, 7):
    install_requires.append('argparse')

setup(name='everton',
      version='0.2',
      description='Evernote command line tool',
      author='Yoshihiko Nishida',
      author_email='nishida@ngc224.org',
      url='https://github.com/ngc224/everton',
      packages=find_packages(),
      install_requires=install_requires,
      entry_points="""
      [console_scripts]
      everton = everton.everton:main
      """,)
