from distutils.core import setup

setup(
    name='albumreviewscraper',
    packages=['AlbumReviewScraper'],
    version="0.1",
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
