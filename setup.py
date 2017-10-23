from setuptools import setup

setup(
    name='albumreviewscraper',
    packages=['albumreviewscraper'],
    include_package_data=True,
    install_requires=[
        'requests',
        'bs4',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
