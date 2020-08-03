from setuptools import setup, find_packages

from buildtest import BUILDTEST_VERSION

setup(
    name="buildtest",
    version=BUILDTEST_VERSION,
    author="Shahzeb Siddiqui",
    author_email="shahzebmsiddiqui@gmail.com",
    description="HPC Testing Framework",
    long_description=open("README.rst").read(),
    url="https://github.com/buildtesters/buildtest",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Testing",
    ],
    project_urls={
        "Documentation": "https://buildtest.readthedocs.io/",
        "Source": "https://github.com/buildtesters/buildtest",
    },
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["PyYAML>=5.2", "distro", "jsonschema", "tabulate"],
    entry_points={"console_scripts": ["buildtest=buildtest.main:main"]},
)
