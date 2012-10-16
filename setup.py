from setuptools import setup

setup(
    name = "zsets",
    url = "http://github.com/sebleier/python-zsets/",
    author = "Sean Bleier",
    author_email = "sebleier@gmail.com",
    version = "0.1.0",
    packages = ["zsets"],
    description = "Python datastructure for sorted sets, similar to Redis sorted sets and inspired by Redis-py's api",
    install_requires=[]
    classifiers = [
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
