from setuptools import setup, find_packages

setup(
    name = 'fundingharvest',
    version = '0.1',
    packages = find_packages(),
    url = 'TODO PUT URL HERE WHEN DEPLOYED',
    author = 'Emanuil Tolev',
    author_email = 'emanuil.tolev@gmail.com',
    description = 'Funding Harvest digests data from RSS feeds and (soon) other sources and stores it (presently just POST-s to an elasticsearch instance). Started as the data gathering piece of FundFind https://github.com/emanuil-tolev/fundfind/',
    license = 'TODO PUT LICENCE HERE WHEN DECIDED',
    # TODO define classifiers when decided (also look for other potentially 
    # useful classifiers
    # classifiers = [
        # 'Development Status :: 3 - Alpha',
        # 'Environment :: Console',
        # 'Intended Audience :: Developers',
        # 'License :: OSI Approved :: MIT License',
        # 'Operating System :: OS Independent',
        # 'Programming Language :: Python',
        # 'Topic :: Software Development :: Libraries :: Python Modules'
    # ],
)

