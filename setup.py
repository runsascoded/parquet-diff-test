from setuptools import setup, find_packages

setup(
    name="parquet-diff-test",
    version="0.0.1",
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'parquet-diff-test=parquet_diff_test.cli:main',
        ],
    },
)
