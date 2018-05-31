from setuptools import setup, find_packages

__version__ = '0.1'


setup(
    name='fm_database',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'click',
        'sqlalchemy',
        'passlib'
    ],
    entry_points={
        'console_scripts': [
            'fm_database = fm_database.manage:cli'
        ]
    }
)
