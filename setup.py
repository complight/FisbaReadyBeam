import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name="FisbaReadyBeam",
    version="0.0.1",
    author="Kaan Akşit",
    author_email="kaanaksit@kaanaksit.com",
    description="A library to control Fisba ReadyBeam laser light sources.",
    license=read('LICENSE'),
    keywords="laser, light, control",
    url="https://github.com/complight/FisbaReadyBeam",
    install_requires=install_requires,
    packages=[
        'FisbaReadyBeam',
    ],
    package_dir={'FisbaReadyBeam': 'FisbaReadyBeam'},
    data_files=[
        ('', ['LICENSE', 'README.md', 'THANKS.txt', 'requirements.txt'])],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    ],
    python_requires='>=3.7.5',
)
