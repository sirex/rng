from setuptools import setup, find_packages

setup(
    name="rng",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy<0.14.0',
        'skidmarks',
    ],
    entry_points={
        'console_scripts': [
            'rng = rng:main',
            'rngtests = rngtests:main',
        ],
    },
)
