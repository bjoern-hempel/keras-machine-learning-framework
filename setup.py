from setuptools import setup

setup(
    name='machineLearning',
    version='1.0',
    py_modules=['mlks.main'],
    install_requires=[
        'Click', 'matplotlib', 'numpy', 'tensorflow', 'scikit-learn', 'pandas', 'seaborn', 'six'
    ],
    entry_points='''
        [console_scripts]
        ml=mlks.main:cli
        run_http=mlks.runner.run_http:run
    ''',
)
