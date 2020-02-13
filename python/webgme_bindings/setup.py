import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webgme_bindings",
    version="1.0.2",
    license='MIT',
    author="Patrik Meijer",
    author_email="webgme@vanderbilt.edu",
    description="Package containing webgme-bindings through zeromq",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/webgme/bindings",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyzmq'
    ],
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ),
)
