from distutils.core import setup

setup(
  name = 'tsag',
  packages = ['tsag'],
  version = '0.1',
  license='MIT',
  description = 'Time series anomaly generator',
  author = 'Jet New',
  author_email = 'notesjet@gmail.com',
  url = 'https://github.com/jetnew/tsag',
  download_url = 'https://github.com/jetnew/tsag/archive/v_01.tar.gz',
  keywords = ['time', 'series', 'anomaly', 'generator', 'detection', 'generation', 'data', 'anomalous'],
  install_requires = [
        'numpy',
        'pandas',
        'matplotlib',
      ],
  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)