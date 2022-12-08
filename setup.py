try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'micloud',
    packages = ['micloud'],
    include_package_data=True,
    version = '0.6',
    license='MIT',
    description = 'Xiaomi cloud connect library',
    author = 'Sammy Svensson',
    author_email = 'sammy@ssvensson.se',
    url = 'https://github.com/squachen/micloud',
    download_url = 'https://github.com/Squachen/micloud/archive/v_0.6.tar.gz',
    install_requires=[
        'requests',
        'tzlocal',
        'click',
        'pycryptodome'
    ],
    entry_points='''
        [console_scripts]
        micloud=micloud.cli:cli
    ''',
)
