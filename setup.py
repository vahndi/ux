from setuptools import setup, find_packages

setup(
    name='ux',
    version='0.1.12',
    packages=find_packages(),
    url='https://github.com/vahndi/ux',
    license='MIT',
    author='vahndi.minah',
    author_email='',
    description='A Python package for measuring and analyzing User Experience',
    install_requires=[
        'matplotlib',
        'numba',
        'numpy',
        'pandas',
        'scipy',
        'seaborn',
        'statsmodels'
    ]
)
