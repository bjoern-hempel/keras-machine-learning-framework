from setuptools import setup

setup(
    name='machineLearning',
    version='1.0',
    py_modules=['ml'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        ml=ml:cli
    ''',
)
