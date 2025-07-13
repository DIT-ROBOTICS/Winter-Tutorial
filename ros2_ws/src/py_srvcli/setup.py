from setuptools import setup
package_name = 'py_srvcli'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    entry_points={
        'console_scripts': [
            'add_two_ints_server = py_srvcli.add_two_ints_server:main',
            'add_two_ints_client = py_srvcli.add_two_ints_client:main',
        ],
    },
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    description='Example Service/Client in Python',
)