import logging

from setuptools import find_packages, setup

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
log.debug("Running setup...")

setup(
    name="bonsai-gym",
    version="3.0.0",
    description="A python library for integrating Bonsai BRAIN \
    with Open AI Gym environments.",
    long_description=open("README.md").read(),
    url="https://www.microsoft.com/en-us/ai/autonomous-systems-project-bonsai",
    author="Microsoft Project Bonsai",
    author_email="bonsaiq@microsoft.com",
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Natural Language :: English",
    ],
    keywords="bonsai",
    install_requires=[
        "gymnasium>=0.26,<0.27",
        "microsoft-bonsai-api==0.1.4",
        "numpy>=1.18",
    ],
    python_requires=">=3.8",
    packages=find_packages(),
)
