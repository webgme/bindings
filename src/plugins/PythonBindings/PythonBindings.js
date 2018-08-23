/* globals define */
/* eslint-env node */

/**
 * Example plugin that calls a "plugin" written in python.
 */

define([
    'q',
    'plugin/PluginConfig',
    'text!./metadata.json',
    'plugin/PluginBase'
], function (
    Q,
    PluginConfig,
    pluginMetadata,
    PluginBase) {
    'use strict';

    pluginMetadata = JSON.parse(pluginMetadata);

    const START_PORT = 5555;
    const COMMAND = 'python';
    const SCRIPT_FILE = 'src/plugins/PythonBindings/run_plugin.py';

    /**
     * Initializes a new instance of PythonBindings.
     * @class
     * @augments {PluginBase}
     * @classdesc This class represents the plugin PythonBindings.
     * @constructor
     */
    function PythonBindings() {
        // Call base class' constructor.
        PluginBase.call(this);
        this.pluginMetadata = pluginMetadata;
    }

    /**
     * Metadata associated with the plugin. Contains id, name, version, description, icon, configStructue etc.
     * This is also available at the instance at this.pluginMetadata.
     * @type {object}
     */
    PythonBindings.metadata = pluginMetadata;

    // Prototypical inheritance from PluginBase.
    PythonBindings.prototype = Object.create(PluginBase.prototype);
    PythonBindings.prototype.constructor = PythonBindings;

    /**
     * Main function for the plugin to execute. This will perform the execution.
     * Notes:
     * - Always log with the provided logger.[error,warning,info,debug].
     * - Do NOT put any user interaction logic UI, etc. inside this method.
     * - callback always has to be called even if error happened.
     *
     * @param {function(null|Error|string, plugin.PluginResult)} callback - the result callback
     */
    PythonBindings.prototype.main = function (callback) {
        const path = require('path');
        const CoreZMQ = require(path.join(process.cwd(), 'index')).CoreZMQ;
        const cp = require('child_process');
        const logger = this.logger;

        const callScript = (program, scriptPath, port) => {
            let deferred = Q.defer(),
                options = {},
                args = [
                    scriptPath,
                    port,
                    `"${this.commitHash}"`,
                    `"${this.branchName}"`,
                    `"${this.core.getPath(this.activeNode)}"`,
                    `"${this.activeSelection.map(node => this.core.getPath(node)).join(',')}"`,
                    `"${this.namespace}"`,
                ];

            const childProc = cp.spawn(program, args, options);

            childProc.stdout.on('data', data => {
                logger.info(data.toString());
                // logger.debug(data.toString());
            });

            childProc.stderr.on('data', data => {
                logger.error(data.toString());
            });

            childProc.on('close', (code) => {
                if (code > 0) {
                    deferred.reject(new Error(`${program} ${args.join(' ')} exited with code ${code}.`));
                } else {
                    deferred.resolve();
                }
            });

            childProc.on('error', (err) => {
                deferred.resolve(err);
            });

            return deferred.promise;
        };

        const corezmq = new CoreZMQ(this.project, this.core, this.logger, {port: START_PORT, plugin: this});
        corezmq.startServer()
            .then((port) => {
                logger.info(`zmq-server listening at port ${port}`);
                return callScript(COMMAND, SCRIPT_FILE, port);
            })
            .then(() => {
                return corezmq.stopServer();
            })
            .then(() => {
                this.result.setSuccess(true);
                callback(null, this.result);
            })
            .catch((err) => {
                this.logger.error(err.stack);
                // Result success is false at invocation.
                corezmq.stopServer()
                    .finally(() => {
                        callback(err, this.result);
                    });
            });

    };

    return PythonBindings;
});
