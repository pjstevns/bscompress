from setuptools import setup, find_packages

version = '0.1'

long_description = (open('README.md').read())

setup(name='bscompress',
      version=version,
      description="BlobStorage compressor",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='ZODB BlobStorage',
      author='Paul J Stevens',
      author_email='paul@nfg.nl',
      url='http://github.com/pjstevns/bscompress',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'bscompress'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      extras_require={'test': ['zope.testing']},
      entry_points="""
      [console_scripts]
      bscompress = bscompress.bscompress:main
      """,
      )
