/* eslint-env node */
/**
 * FIXME: This is not an elegant solution!
 * When running Python (on any other language) from outside the context of a plugin. This
 * Mock provides the methods needed in order for the same code to work the same except there are
 * no state added to the plugin's result.
 * This should typically only be used for testing purposes when running, e.g. run_debug.py of a plugin.
 *
 * @author pmeijer / https://github.com/pmeijer
 */

const Q = require('q');

function getPluginMock(serverUrl, webgmeToken, gmeConfig, logger, metadataPath, pluginConfigPath) {
    let blobClient;
    let pluginConfig = {};

    if (serverUrl) {
        const BlobClient = requirejs('blob/BlobClient');
        // FIXME: The server url should to be broken down in pieces
        blobClient = new BlobClient({
            serverPort: gmeConfig.server.port,
            httpsecure: false,
            server: '127.0.0.1',
            webgmeToken: webgmeToken,
            logger: logger.fork('BlobClient')
        });
    } else {
        const BlobClient = require('webgme-engine/src/server/middleware/blob/BlobClientWithFSBackend');
        blobClient = new BlobClient(gmeConfig, logger);
    }

    if (metadataPath) {
        require(metadataPath).configStructure
            .forEach((cInfo) => {
                pluginConfig[cInfo.name] = cInfo.value;
            });
    } else {
        pluginConfig = {};
    }

    if (pluginConfigPath) {
        const pConfig = require(pluginConfigPath);
        Object.keys(pConfig)
            .forEach((name) => {
                pluginConfig[name] = pConfig[name];
            });
    }

    return {
        createMessage: () => {
        },
        sendNotification: () => {
        },
        getCurrentConfig: () => {
            return pluginConfig;
        },
        addFile: (name, content, cb) => {
            return blobClient.putFile(name, content).nodeify(cb);
        },
        addArtifact: (name, files, callback) => {
            const artifact = blobClient.createArtifact(name);
            return artifact.addFilesAsSoftLinks(files)
                .then(function () {
                    return artifact.save();
                })
                .nodeify(callback);
        },
        getFile: (metadataHash, cb) => {
            return blobClient.getObjectAsString(metadataHash).nodeify(cb);
        },
        getArtifact: (metadataHash, cb) => {
            const result = {};
            return blobClient.getMetadata(metadataHash)
                .then(function (metadata) {
                    const promises = Object.keys(metadata.content)
                        .map(function (fileName) {
                            return blobClient.getObjectAsString(metadata.content[fileName].content)
                                .then(function (content) {
                                    result[fileName] = content;
                                });
                        });

                    return Q.all(promises);
                })
                .then(function () {
                    return result;
                })
                .nodeify(cb);
        },
    };
}

module.exports = getPluginMock;