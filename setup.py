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
    download_url = 'https://github.com/Squachen/micloud/archive/v_0.1.tar.gz',
    install_requires=[
        'requests',
        'tzlocal'
    ]
)