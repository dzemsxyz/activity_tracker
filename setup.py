import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("LICENSE", "r", encoding="utf-8") as f:
    license = f.read()  # pylint:disable=redefined-builtin

setuptools.setup(
    version="0.1.0",
    name="activity_tracker",
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=license,
)