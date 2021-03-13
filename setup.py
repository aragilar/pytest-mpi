from setuptools import setup, find_packages
import versioneer

DESCRIPTION_FILES = ["pypi-intro.rst"]

long_description = []
import codecs
for filename in DESCRIPTION_FILES:
    with codecs.open(filename, 'r', 'utf-8') as f:
        long_description.append(f.read())
long_description = "\n".join(long_description)

setup(
    name="pytest-mpi",
    version=versioneer.get_version(),
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ["pytest"],
    author = "James Tocknell",
    author_email = "aragilar@gmail.com",
    description = "pytest plugin to collect information from tests",
    long_description = long_description,
    license = "3-clause BSD",
    keywords = "pytest testing",
    url = "https://pytest-mpi.readthedocs.io",
    entry_points = {
        'pytest11': [
            'pytest_mpi = pytest_mpi',
        ]
    },
    classifiers=[
        'Framework :: Pytest',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    cmdclass=versioneer.get_cmdclass(),
)
