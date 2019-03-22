The module is defined inside webgme_bindings. The README.md inside the
directory is the README.md that is published on [pypi.org](https://pypi.org/project/webgme-bindings/).

## Install module from source
1. `cd webgme_bindings`
2. `pip install -e .`

## Tests
The tests are defined in [./test.py](./webgme_bindings/webgme_bindings/test.py) and
instructions on how to run them are inside the file.

Note that the same tests are called in the java-script tests to generate the JS-coverage.

## To generate source docs
Make sure to install sphinx
```
pip install Sphinx
```

1. Clean up `./webgme_bindings/docs/_build`
2. Run `./webgme_bindings/docs/make.bat html`
3. Main index.html is at `./webgme_bindings/docs/_build/html/index.html`

## To publish
https://packaging.python.org/tutorials/packaging-projects/
