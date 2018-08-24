## Generating APIs in other languages

- Check for available [ZeroMQ bindings](http://zeromq.org/bindings:_start)
- All data is communicated via JSON (including core-node objects which are dictionaries with a `nodePath` and `rootId`).
There for make sure that you have a convenient way of parsing (dynamically structured) JSONs.
- Add a new directory at the top, e.g. python, java.
- Write a client in zmq and ensure you can connect to a running bin/corezmq_server.js
- Once the basics is working you can use [generate_api](./generate_api.js) for generating the core and project API.
  - Make sure `jsdoc.json` is up-to-date with the latest webgme-engine
    ```
    npm run update_docs_json
    ```
  - Add an entry in [config.json](./config.json) (generate_api uses ejs templates - do consider starting off from the existing ones.)
  - Add a new mapping in typeMaps for the language inside generate_api.
- Generate a new test plugin for the language, e.g.,
    ```
    webgme new plugin JavaBindings
    ```
- Make sure there is a way to start the "plugin" from the webgme framework (`run_plugin.py`) and from the language itself (`run_debug.py`).
The latter makes debugging much easier. For the js portion of the plugin most of [PythonBindings](../src/plugins/PythonBindings/PythonBindings.js) can be reused.
- Publish the API at a suiting registry (or include instructions on how to use it from this repo).
- In the webgme-engine repo, add an option to the language config in PluginGenerator and suitable templates.

