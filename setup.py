from setuptools import setup, find_packages

setup(
    name='clicov',
    version='0.0.1',
    author= "Heru Handika",
    author_email = "hhandika.us [at] gmail [dot] com",
    include_package_data=True,
    py_modules=find_packages(),
    install_requires=[
        'Click', 'pandas', 'requests',
    ],
    entry_points='''
        [console_scripts]
        clicov=clicov:main
    ''',
)