from setuptools import find_packages, setup

package_name = 'm0609_kinematics'

setup(
    name=package_name,
    version='1.0.0',

    packages=find_packages(exclude=['test']),

    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
    ],

    install_requires=[
        'setuptools',
        'numpy'
    ],

    zip_safe=True,

    maintainer='IMT-342 Robótica Chauca',
    maintainer_email='imt342.robotica@example.com',

    description='Cinemática directa e inversa del robot industrial Doosan M0609.',

    license='Apache-2.0',

    extras_require={
        'test': [
            'pytest',
        ],
    },

    entry_points={
        'console_scripts': [
            'fk_node = m0609_kinematics.fk_node:main',
            'ik_node = m0609_kinematics.ik_node:main',
        ],
    },
)
