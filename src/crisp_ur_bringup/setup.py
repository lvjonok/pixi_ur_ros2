from setuptools import setup
from glob import glob
import os

package_name = 'crisp_ur_bringup'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Lev Kozlov',
    maintainer_email='kozlov.l.a10@gmail.com',
    description='CRISP Controllers bringup for Universal Robots',
    license='Apache-2.0',

    entry_points={
        'console_scripts': [],
    },
)
