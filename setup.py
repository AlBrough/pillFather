from setuptools import setup, find_packages

setup(
    name='Rapt Pill To Brewfather',
    version='1.0',
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'runwebhook = app:run',
        ],
    }
)
