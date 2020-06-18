from setuptools import setup, find_packages

setup(
    name='clicov',
    version='0.0.3',
    author= "Heru Handika",
    author_email = "hhandika.us@gmail.com",
    py_modules=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click', 'pandas', 'requests', 'tabulate'
    ],
    entry_points='''
        [console_scripts]
        clicov=clicov.clicov:main
    ''',
)