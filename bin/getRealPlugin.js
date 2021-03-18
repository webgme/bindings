/* eslint-env node */
/**
 * This plugin loader only works for plugins that have their js as a wrapper and work in their own!
 * This will fail with all other type of plugins!
 * @author kecso / https://github.com/kecso
 */

 const Q = require('q');

 function getPluginInstance(pluginId, logger, callback) {
    var deferred = Q.defer(),
    pluginPath;

    function instantiatePlugin(PluginClass, PluginResult) {
        var plugin;

        if (!PluginClass) {
            // This should not happen, but just in case..
            deferred.reject(new Error('Loading plugin "' + pluginId +
                '" with requirejs return undefined.'));
            return;
        }

        plugin = new PluginClass();
        plugin.result = new PluginResult();
        deferred.resolve(plugin);
    }

    pluginPath = 'plugin/' + pluginId + '/' + pluginId + '/' + pluginId;
    logger.debug('requirejs plugin from path: ' + pluginPath);
    requireJS([pluginPath, 'plugin/PluginResult'], instantiatePlugin,
        function (err) {
            deferred.reject(err);
        }
    );

    return deferred.promise.nodeify(callback);
}

 function getPlugin(
        pluginId, 
        webgme, 
        serverUrl, 
        webgmeToken, 
        gmeConfig, 
        logger, 
        metadataPath, 
        pluginConfigPath, 
        core, 
        project, 
        callback) {
     const deferred = Q.defer();
     let blobClient;
     let pluginConfig = {};
     if (serverUrl) {
         const BlobClient = requirejs('blob/BlobClient');
         // FIXME: The server url should to be broken down in pieces
         blobClient = new BlobClient({
             serverPort: gmeConfig.server.port,
             httpsecure: false,
             server: serverUrl,
             webgmeToken: webgmeToken,
             logger: logger.fork('BlobClient')
         });
     } else {
         const BlobClient = require('webgme-engine/src/server/middleware/blob/BlobClientWithFSBackend');
         blobClient = new BlobClient(gmeConfig, logger);
     }
 
     let metaData = {};
     if (metadataPath) {
         metaData = require(metadataPath)
         metaData.configStructure.forEach((cInfo) => {
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
 
     getPluginInstance(pluginId, logger)
     .then(plugin => {
         plugin.pluginMetaData = metaData;
         plugin.gmeConfig = gmeConfig;
         plugin.logger = logger.fork(pluginId);
         plugin.blobClient = blobClient;
         plugin._currentConfig = pluginConfig;
         plugin.core = core;
         plugin.project = project;
         plugin.projectName = project.projectName;
         plugin.projectId = project.projectId;

         // due to the restrictions of 'binded plugins' other fields do not have to
         // be initialized

         deferred.resolve(plugin);
     })
     .catch(deferred.reject);

     return deferred.promise.nodeify(callback);
 }
 
 module.exports = getPlugin;