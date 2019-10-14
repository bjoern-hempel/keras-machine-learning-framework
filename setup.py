from setuptools import setup

setup(
    name='machineLearning',
    version='1.0',
    py_modules=['mlks.main'],
    install_requires=[
        'Click', 'keras', 'matplotlib', 'numpy', 'tensorflow', 'magic'
    ],
    entry_points='''
        [console_scripts]
        ml=mlks.main:cli
        run_http=mlks.runner.run_http:run
    ''',
)
