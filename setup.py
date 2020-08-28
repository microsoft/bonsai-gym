import logging
from setuptools import setup, find_packages

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
log.debug("Running setup...")

version = {}
with open("./bonsai_gym/version.py") as fp:
    exec(fp.read(), version)
setup(
    name="bonsai-gym",
    version=version["__version__"],
    description="A python library for integrating Bonsai BRAIN \
    with Open AI Gym environments.",
    long_description=open("README.md").read(),
    url="https://bons.ai",
    author="Bonsai, Inc.",
    author_email="opensource@bons.ai",
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Natural Language :: English",
    ],
    keywords="bonsai",
    install_requires=[
        "bonsai-ai>=2.0.19",
        "gym==0.9.7",
        "bonsai-common @ git+https://github.com/microsoft/bonsai-common",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, " "!=3.3.*, !=3.4.*",
    packages=find_packages(),
)
