from setuptools import setup, find_packages

__version__ = "0.1"

install_requires = [
    'requests',
    #    'pynacl',
    'requests_oauthlib',
    #    'python-dateutil',
    #    'pillow',
    'cryptography',
    'pygobject',
]

setup(
    name="eduvpn",
    version=__version__,
    packages=find_packages(),
    install_requires=install_requires,
    author="Gijs Molenaar",
    author_email="gijs@pythonic.nl",
    description="eduVPN client",
    license="GPL3",
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite="tests",
    keywords="vpn openvpn networking security",
    url="https://github.com/eduvpn/python-eduvpn-client",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Operating System Kernels :: Linux",
        "Topic :: System :: Networking",
        "Environment :: X11 Applications",
    ],
    entry_points={
        'console_scripts': [
            'pyeduvpn = pyeduvpn.__main__:main'
        ]
    }
)
