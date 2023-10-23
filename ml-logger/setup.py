from setuptools import setup, find_packages

setup(
    name="ml-logger",
    version="1.0",
    packages=find_packages(),
    author="yang",   
    install_requires=[
        "pyyaml",
        "request",
        "nvidia-ml-py"
    ],
    author_email="yang.open@outlook.com",
    description="log lib for machine learning",
    long_description="log lib for machine learning",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)