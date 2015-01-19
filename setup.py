from setuptools import setup

setup(
    name='TankRemote',
    version='1.0',
    description='Remote controller application for a WiFi tank',
    author='Michael Cooper',
    author_email='mic159@gmail.com',
    packages=['tank'],
    install_requires=[
    #    'pygtk'
    ],
    entry_points={
        'gui_scripts': [
            'tank_remote = tank.main:main'
        ]
    }
)