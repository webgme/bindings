/*jshint node: true*/
/**
 * @author lattmann / https://github.com/lattmann
 * @author pmeijer / https://github.com/pmeijer
 */

var env = process.env.NODE_ENV || 'default',
    configFilename = __dirname + '/config.' + env + '.js',
    config = require(configFilename),
    validator = require('webgme-engine/config/validator'),
    overrideFromEnv = require('webgme-engine/config/overridefromenv');

overrideFromEnv(config);
validator.validateConfig(config);
module.exports = config;
