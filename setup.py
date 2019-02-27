import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="saiyan",
    version="0.0.4",
    author="Matteo Cremonesi",
    author_email="matteoc@fnal.gov",
    description="Sophisticated Algorithms Implemented to make Your Analysis Nice",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mcremone/saiyan.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
