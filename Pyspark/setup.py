from setuptools import setup, find_packages

setup(
    name='regular_patients',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pyspark>=3.5.4,<4.0.0',
        'pytest>=8.3.4,<9.0.0',
        'pytest-mock>=3.14.0,<4.0.0'
    ],
    include_package_data=True,
    zip_safe=False,
)
