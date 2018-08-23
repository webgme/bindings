/* eslint-env node */
/* eslint no-console: 0 */

const Case = require('case');
const docs = require('./jsdoc.json').docs;
const config = require('./config.json');
const ejs = require('ejs');
const fs = require('fs');
const Q = require('q');

const CORE_EXCLUDES = {
    traverse: true,
    getChild: true,
    loadTree: true,
};

const PROJECT_EXCLUDES = {
    sendDocumentOperation: true,
    sendDocumentSelection: true,
    watchDocument: true,
    unwatchDocument: true,
    insertObject: true,
    insertPatchObject: true,
    loadPaths: true,
    loadObject: true,
};

const fileReadPromises = [];

config.forEach((templateInfo) => {
    fileReadPromises.push(
        Q.all([
            Q.ninvoke(fs, 'readFile', templateInfo.core.template, 'utf8'),
            Q.ninvoke(fs, 'readFile', templateInfo.project.template, 'utf8'),
        ])
            .then((res) => {
                return {
                    core: {
                        template: res[0],
                        output: templateInfo.core.output,
                    },
                    project: {
                        template: res[1],
                        output: templateInfo.project.output,
                    }
                }
            })
    );
});

const data = {
    core: [],
    project: []
};

docs.forEach((docItem) => {
    if (docItem.kind !== 'function' || CORE_EXCLUDES[docItem.name] || PROJECT_EXCLUDES[docItem.name]) {
        return;
    }

    const methodData = {
        name: docItem.name,
        description: docItem.description,
        exceptions: docItem.exceptions || [],
        args: [],
        returns: docItem.returns || [],
    };

    (docItem.params || []).forEach((arg) => {
        try {
            if (docItem.name === 'updateLibrary' && arg.name === 'updateInstructions') {
                console.log('Skipping "updateInstructions" for updateLibrary');
            } else if (arg.name.indexOf('.') > -1) {
                if (arg.name.indexOf('callback.') === 0) {
                    if (arg.type.names.indexOf('Error') > -1) {
                        methodData.returns = []; // Remove the promise description..
                        arg.type.names.forEach((name) => {
                            let hasExceptionDeclared = false;

                            methodData.exceptions.forEach((eData) => {
                                hasExceptionDeclared = hasExceptionDeclared || eData.type.names.indexOf(name) > -1;
                            });

                            if (name !== 'null' && name !== 'undefined' && hasExceptionDeclared === false) {
                                methodData.exceptions.push({
                                    type: {
                                        names: [name]
                                    },
                                    description: arg.description,
                                });
                            }
                        });
                    } else {
                        methodData.returns = [arg];
                    }
                } else {
                    console.log('Skipping argument with dot which is not part of callback', arg.name);
                }
                // } else if (arg.type.names[0] === 'module:Core~Node') {
                //     const nodePathArg = copy(arg);
                //     nodePathArg.type.names[0] = 'string';
                //
                //     methodData.args.push(nodePathArg);
                // } else if (arg.type.names[0] === 'Array.module:Core~Node') {
                //     const nodePathArg = copy(arg);
                //     nodePathArg.type.names[0] = 'Array.string';
                //     nodePathArg.name = `${arg.name.endsWith('s') ? arg.name.slice(0, -1) : arg.name}Paths`;
                //     methodData.args.push(nodePathArg);
            } else if (arg.type.names[0] === 'function' && arg.optional === true && arg.name === 'callback') {
                console.log('Skipping callback arg for ', docItem.longname);
            } else {
                methodData.args.push(arg);
            }
        } catch (e) {
            console.error(`Failed handling param ${JSON.stringify(arg, null, 2)} for\
${JSON.stringify(docItem, null, 2)}, err: ${e}`);
        }
    });

    if (methodData.returns.length === 0) {
        methodData.returns.push({
            type: {
                names: ['undefined']
            },
            description: 'Nothing is returned by the function.',
        })
    }

    if (docItem.memberof === 'Core') {
        // if (docItem.name.indexOf('load') === 0) {
        //     console.log('Skipping core load method:', docItem.name);
        //     return;
        // }

        data.core.push(methodData);
    } else if (docItem.memberof === 'ProjectInterface') {
        data.project.push(methodData);
    }
});

function comp(a, b) {
    if (a.name > b.name) {
        return 1;
    } else if (a.name < b.name) {
        return -1;
    }

    return 0;
}

data.core.sort(comp);
data.project.sort(comp);

const typeMaps = {
    python: {
        'string': 'str',
        'undefined': 'None',
        'object': 'dict',
        'integer': 'int',
        'number': 'int or float',
        'bool': 'bool',
        'boolean': 'bool',
        'null': 'None',
        'module:Core~Node': 'dict',
        'Array.<module:Core~Node>': 'list of dict',
        'module:Core~ObjectHash': 'str',
        'module:Core~Constraint': 'dict',
        'module:Core~GUID': 'str',
        'module:Storage~CommitHash': 'str',
        'module:Storage~CommitResult': 'dict',
        'Array.<module:Storage~CommitHash>': 'list of str',
        'Array.<module:Core~MixinViolation>': 'list of dict',
        'Array.<module:Storage~CommitObject>': 'list of dict',
        'module:Storage~CommitObject': 'dict',
        'Array.<string>': 'list of str',
        'module:Core~DataObject': 'dict',
        'module:Core~DefinitionInfo': 'dict',
        'module:Core~RelationRule': 'dict',
        'module:Core~GmePersisted': 'dict',
        'Object.<string, module:Core~Node>': 'dict',
        'Object.<string, module:Core~ObjectHash>': 'dict',
        'Object.<string, module:Storage~CommitHash>': 'dict',
        'Error': 'JSError',
    }
};

Q.all(fileReadPromises)
    .then((templates) => {
        const promises = [];

        templates.forEach((templateInfo) => {
            const coreStr = ejs.render(templateInfo.core.template, {methods: data.core, Case, typeMaps});
            const projectStr = ejs.render(templateInfo.project.template, {methods: data.project, Case, typeMaps});

            promises.push(
                Q.all([
                    Q.ninvoke(fs, 'writeFile', templateInfo.core.output, coreStr),
                    Q.ninvoke(fs, 'writeFile', templateInfo.project.output, projectStr),
                ])
                    .then(() => console.log(`Wrote out ${templateInfo.core.output} and ${templateInfo.project.output}`))
            );
        });

        return Q.all(promises);
    })
    .catch(err => console.error(err));
