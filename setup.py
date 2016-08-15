from setuptools import setup

setup(
    name='eveapp',
    packages=['eve_tokenauth'],
    include_package_data=True,
    install_requires=[
        'eve',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
