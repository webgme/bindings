const { execSync } = require('child_process');
const path = require('path');
const { stdout } = require('process');
const pluginNames = [
    'PythonBindings',
    'PythonBindingsError',
    'PythonBindingsWait',
    'PythonExtraFunctions',
];


pluginNames.forEach(pluginName => {
    const debug = 'python src/plugins/'+ pluginName + '/run_debug.py';
    try {
        execSync(debug,{encoding:'utf8'});
    } catch (e) {
        console.log('execution of' + pluginName + ' failed!!!');
    }
});