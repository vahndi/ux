from setuptools import setup

setup(
    name='ux',
    version='0.1.1',
    packages=['ux', 'ux.calcs', 'ux.plots', 'ux.classes', 'ux.classes.ux', 'ux.classes.stats', 'ux.interfaces',
              'ux.interfaces.ux', 'tests', 'examples'],
    url='https://github.com/vahndi/ux',
    license='MIT',
    author='vahndi.minah',
    author_email='',
    description='A Python package for measuring and analyzing User Experience',
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'seaborn',
        'statsmodels'
    ]
)
