from setuptools import find_packages, setup

setup(
    name="elevenlabs",
    packages=find_packages(exclude=[]),
    version="0.2.13",
    description="The official elevenlabs python package.",
    long_description_content_type="text/markdown",
    author="Elevenlabs",
    url="https://github.com/elevenlabs/elevenlabs-python",
    keywords=["artificial intelligence", "deep learning"],
    install_requires=[
        "pydantic>=1.10",
        "ipython>=7.0",
        "requests>=2.20",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
