from setuptools import setup, find_packages

setup(name='everton',
      version='0.1',
      description='Evernote command line tool',
      author='Yoshihiko Nishida',
      author_email='nishida@ngc224.org',
      url='https://github.com/ngc224/everton',
      packages=find_packages(),
      install_requires=['evernote', 'clint'],
      entry_points="""
      [console_scripts]
      everton = everton.everton:main
      """,)
