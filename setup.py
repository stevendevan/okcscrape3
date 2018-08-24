from setuptools import setup, find_packages

setup(
    name='okcscrape3',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['beautifulsoup4',
                      'pandas',
                      'selenium',
                      'regex'],
    entry_points={'console_scripts': ['okcscrape3 = okcscrape3.__main__:main']
                  },
    package_data={'': ['config.ini',
                       'profile_html_targets.json']}
)
