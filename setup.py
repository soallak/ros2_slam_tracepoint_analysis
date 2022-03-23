from setuptools import setup

package_name = 'slam_tracepoint_analysis'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='swallak',
    maintainer_email='sw.allak@gmail.com',
    description='SLAM tracepoints analyis tool<',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'process = slam_tracepoint_analysis.process:main'
        ],
    },
)
