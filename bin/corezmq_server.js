/* eslint-env node */
/* eslint no-console: 0 */
/**
 *
 * @author pmeijer / https://github.com/pmeijer
 */

const webgme = require('webgme-engine');
const Q = require('q');
const Command = require('commander').Command;
const CoreZMQ = require('../src/corezmq');
const STORAGE_CONSTANTS = webgme.CONSTANTS.STORAGE;
const getPluginMock = require('./getPluginMock');
const getPlugin = require('./getRealPlugin');
const Core = webgme.Core;

/**
 *
 * @param {object} parameters
 * @param {string} parameters.pluginId
 * @param {string} parameters.projectName
 * @param {GmeConfig} parameters.gmeConfig
 * @param {GmeLogger} parameters.logger
 * @param {string} [parameters.user='guest']
 * @param {string} [parameters.owner=parameters.user]
 * @param {int|string} [parameters.port=5555]
 * @param {string} [parameters.address]
 * @param {string} [parameters.serverUrl]
 * @param {string} [parameters.pluginMetadataPath]
 * @param {string} [parameters.pluginConfigPath]
 * @param {function} [callback]
 * @returns {Promise}
 */
const main = (parameters, callback) => {
    const deferred = Q.defer();
    const userName = parameters.user ? parameters.user.split(':')[0] : parameters.gmeConfig.authentication.guestAccount;
    const projectName = parameters.projectName;
    let projectId = userName + STORAGE_CONSTANTS.PROJECT_ID_SEP + projectName;
    let storage;
    let gmeAuth;
    let zmqServer;

    console.log(JSON.stringify(parameters, null, 2));

    function shutdown() {
        const promises = [];

        if (zmqServer) {
            promises.push(zmqServer.stopServer());
        }

        if (storage) {
            if (gmeAuth) {
                promises.push(storage.closeDatabase());
                promises.push(gmeAuth.unload());
            } else {
                promises.push(storage.close());
            }
        }

        return Q.allSettled(promises);
    }

    if (parameters.owner) {
        projectId = parameters.owner + STORAGE_CONSTANTS.PROJECT_ID_SEP + projectName;
    }

    let projectDeferred;
    let webgmeToken;

    if (parameters.serverUrl) {
        projectDeferred = webgme.utils.requestWebGMEToken(parameters.gmeConfig, userName, parameters.user.split(':')[1],
            parameters.serverUrl)
            .then((token) => {
                webgmeToken = token;
                const storageDeferred = Q.defer();
                storage = webgme.ConnectedStorage.createStorage(parameters.serverUrl, token, parameters.logger,
                    parameters.gmeConfig);

                storage.open((status) => {
                    if (status === STORAGE_CONSTANTS.CONNECTED) {
                        storage.openProject(projectId)
                            .then((res) => {
                                storageDeferred.resolve(res[0]);
                            })
                            .catch(storageDeferred.reject);
                    } else {
                        storageDeferred.reject(new Error(`Unexpected connection status to storage ${status}`));
                    }
                });

                return storageDeferred.promise;
            });
    } else {
        projectDeferred = webgme.getGmeAuth(parameters.gmeConfig)
            .then(function (gmeAuth_) {
                gmeAuth = gmeAuth_;
                storage = webgme.getStorage(parameters.logger, parameters.gmeConfig, gmeAuth);
                return storage.openDatabase();
            })
            .then(function () {
                return storage.openProject({projectId, username: userName});
            })
            .then(function (project) {
                project.setUser(userName);

                return project;
            })
    }

    let project = null;
    let core = null;
    projectDeferred
        .then(project_ => {
            project = project_;
            core = new Core(project, {
                globConf: parameters.gmeConfig,
                logger: parameters.logger.fork('Core')
            });
            if (parameters.pluginId) {
                return getPlugin(
                    parameters.pluginId || 'PythonBindings',
                    webgme,
                    parameters.serverUrl,
                    webgmeToken, 
                    parameters.gmeConfig, 
                    parameters.logger, 
                    parameters.pluginMetadataPath, 
                    parameters.pluginConfigPath, 
                    core, 
                    project);
            } else {
                return Q(getPluginMock(
                    parameters.serverUrl, 
                    webgmeToken, 
                    parameters.gmeConfig, 
                    parameters.logger,
                    parameters.pluginMetadataPath, 
                    parameters.pluginConfigPath));
            }
        })
        .then((plugin) => {

            zmqServer = new CoreZMQ(project, core, parameters.logger, {
                port: parseInt(parameters.port || 5555),
                address: parameters.address,
                plugin: plugin,
            });

            return zmqServer.startServer();
        })
        .then((port) => {
            deferred.resolve({
                shutdown: shutdown,
                port: port,
            });
        })
        .catch((err) => {
            shutdown().then(() => {
                deferred.reject(err);
            });
        });

    return deferred.promise.nodeify(callback);
};

if (require.main === module) {
    const program = new Command();
    const gmeConfig = webgme.getGmeConfig();
    const logger = webgme.Logger.create('gme:bin:coremq_server', gmeConfig.bin.log);

    const exit = (err) => {
        if (err) {
            logger.error(err.stack);
            process.exit(1);
        } else {
            process.exit(0);
        }
    };

    program
        .version('1.0.0')
        .arguments('<projectName>')
        .description('Starts a zero-mq server exposing the core and project API at the provided project.')
        .option('-i, --pluginId [string]', 'The pluginId you wish to debug, if not given mock js wrapper will be used')
        .option('-p, --port [number]', 'Port the server should listen at [5555]', 5555)
        .option('-a, --address [string]', 'If given the port is not used and the server will listen at the ' +
            'given address.', '')
        .option('-u, --user [string]', 'the user of the command [if not given we use the default user]. Note that if ' +
            'this is used together with the --serverUrl option the password can be provided by adding ' +
            'a semicolon.', gmeConfig.authentication.guestAccount)
        .option('-o, --owner [string]', 'the owner of the project [by default, the user is the owner]')
        .option('-s, --serverUrl [string]', 'If specified the project will connect to the database via ' +
            'a running webgme server, example "http://localhost:8888". Note that if a different user than the ' +
            'guest is used the password needs to be added after a semicolon, e.g. "-u someUser:pass".')
        .option('-m, --pluginMetadataPath [string]', 'Optional file-path to the metadata of a plugin.')
        .option('-j, --pluginConfigPath [string]',
            'Path to json file with plugin options that should be overwritten.', '')
        .on('--help', function () {
            console.log('  Examples:');
            console.log();
            console.log('    $ node coremq_server.js MyProject');
            console.log('    $ node coremq_server.js MyProject -i MyPluginId');
            console.log('    $ node coremq_server.js MyProject -m ./src/plugins/MyPythonPlugin/metadata.json');
            console.log('    $ node coremq_server.js MyProject -p 5656 -s http://127.0.0.1:8888');
            console.log();
        })
        .parse(process.argv);

    if (program.args.length < 1) {
        program.help();
    } else {
        program.projectName = program.args[0];
        program.logger = logger;
        program.gmeConfig = gmeConfig;
        main(program)
            .then((server) => {
                function abort() {
                    server.shutdown()
                        .finally(() => {
                            exit();
                        });
                }

                logger.info(`corezmq server listening at ${program.address || server.port}`);
                process.on('SIGINT', abort);
                process.on('SIGTERM', abort);
            })
            .catch(exit);
    }
}

module.exports = main;

