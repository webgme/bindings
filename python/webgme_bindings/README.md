## Python Bindings to WebGME

This is the python package needed to use the webgme-apis in python.

The python api is confirmed to work both with both `2.7.x` and `3.x`. The only third part dependency is
[pyzmq](https://github.com/zeromq/pyzmq) which should work [down to 2.5](https://pyzmq.readthedocs.io/en/latest/pyversions.html).

Note that in the Python API strings are documented as `str` even though in python `2.7` they technically are `unicode`.
(PyZMQ has an explanation of the differences for the interested one [over here](https://pyzmq.readthedocs.io/en/latest/unicode.html).)

[Click here for documentation on how to use bindings in webgme!](https://github.com/webgme/bindings)