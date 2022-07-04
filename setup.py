import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name= "prepars",
    version= 0.1,
    long_description="",
    packages=setuptools.find_packages(),
    py_modules=["prepars"],             # Name of the python package
    package_dir={'':'src/prepars'},
)