from setuptools import setup

setup(
    name='machineLearning',
    version='1.0',
    py_modules=['mlks.main'],
    install_requires=[
        'Click', 'tensorflow'
    ],
    entry_points='''
        [console_scripts]
        ml=mlks.main:cli
    ''',
)
