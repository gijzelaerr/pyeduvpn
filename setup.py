from setuptools import setup, find_packages

__version__ = "0.3.1"

install_requires = [
    'requests',
    'requests_oauthlib',
    'cryptography',
]

extras_require = {
    'gui': ['pygobject'],
}

data_files = [
    ('share/applications', ['share/applications/eduvpn-client.desktop']),
    ('share/eduvpn', [
        'share/eduvpn/eduvpn.png',
    ]),
    ('share/icons/hicolor/48x48/apps', ['share/icons/hicolor/48x48/apps/eduvpn-client.png']),
    ('share/icons/hicolor/128x128/apps', ['share/icons/hicolor/128x128/apps/eduvpn-client.png']),
    ('share/icons/hicolor/256x256/apps', ['share/icons/hicolor/256x256/apps/eduvpn-client.png']),
    ('share/icons/hicolor/512x512/apps', ['share/icons/hicolor/512x512/apps/eduvpn-client.png']),
]

setup(
    name="eduvpn",
    version=__version__,
    packages=find_packages(),
    data_files=data_files,
    install_requires=install_requires,
    extras_require=extras_require,
    author="Gijs Molenaar",
    author_email="gijs@pythonic.nl",
    description="eduVPN client",
    license="GPL3",
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite="tests",
    keywords="vpn openvpn networking security",
    url="https://github.com/eduvpn/python-eduvpn",
    python_requires='>=3.6',
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
            'eduvpn = eduvpn.__main__:main'
        ]
    }
)
