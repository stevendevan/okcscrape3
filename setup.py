from setuptools import setup

setup(
    name='okcscrape3',
    version='0.1.0',
    packages=['okcscrape3'],
    entry_points={
        'console_scripts': [
            'okcscrape3 = okcscrape3.__main__:main'
        ]
    })
