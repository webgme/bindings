'use strict';

var config = require('./config.webgme');

// Add/overwrite any additional settings here
// config.server.port = 8080;
config.mongo.uri = 'mongodb://127.0.0.1:27017/multi';
config.plugin.allowServerExecution = true;
module.exports = config;
