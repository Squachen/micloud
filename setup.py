try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'micloud',
    packages = ['micloud'],
    version = '0.1',
    license='MIT',
    description = 'Xiaomi cloud connect library',
    author = 'Sammy Svensson',
    author_email = 'sammy@ssvensson.se',
    url = 'https://github.com/squachen/micloud',
    download_url = '',
    install_requires=[
        'requests',
        'tzlocal'
    ]
)