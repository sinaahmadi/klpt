from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding = "utf-8") as f:
    long_description = f.read()

with open('requirements.txt', encoding = "utf-8") as f:
    required = [req.strip() for req in f.read().splitlines() if req.strip()]

setup(
    name="klpt",
    version="0.1.6",
    description="Kurdish Language Processing Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sina Ahmadi",
    author_email="ahmadi.sina@outlook.com",
    url="https://github.com/sinaahmadi/klpt",
    packages=find_packages(exclude=["tests", "cinder"]),
    license="CC BY-SA 4.0",
    install_requires=required,
    include_package_data=True,
    python_requires=">=3.6"
)
