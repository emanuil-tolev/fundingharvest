from setuptools import setup, find_packages

setup(
    name = 'fundingharvest',
    version = '0.1',
    packages = find_packages(),
    url = 'https://github.com/emanuil-tolev/fundingharvest',
    author = 'Emanuil Tolev',
    author_email = 'emanuil.tolev@gmail.com',
    description = 'Funding Harvest digests data from RSS feeds and (soon) other sources and stores it (presently just POST-s to an elasticsearch instance). Started as the data gathering piece of FundFind https://github.com/emanuil-tolev/fundfind/',
    license = 'MIT',
    install_requires = [
    'pyes==0.16',
    'requests==1.1.0',
    'parsedatetime==0.8.7',
    'feedparser==5.1.3',
    'python-dateutil==2.2'
    ],
    # TODO look for other potentially useful classifiers
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)

