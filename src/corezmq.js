/* eslint-env node */
/**
 * Main implementation of the zeromq server that maps to function calls to the main webgme APIs,
 * Core, Project and to a certain extent the PluginBase.
 *
 * There a two main use-cases:
 * - This class is instantiated from a plugin which in turn calls a python script.
 * - This class is instantiated as a standalone zmq server from bin/corezmq_server.js
 *
 * @author pmeijer / https://github.com/pmeijer
 */

const zmq = require('zeromq');
const Q = require('q');
const pluginUtil = require('webgme-engine/src/plugin/util');

/**
 *
 * @param {ProjectInterface} project
 * @param {Core} core - A core instance that requested are proxyed to.
 * @param {GmeLogger} mainLogger - Logger that will be forked off from.
 * @param {object} [opts] - Optional options.
 * @param {number} [opts.port=5555] - Port number of which to bind the server listener.
 * @param {number} [opts.portAttempts=100] - Number of attempts to increase port number while occupied.
 * @param {string} [opts.address] - If given the port is not used and the server will listen at the given address.
 * @param {string} [opts.namespace=''] - Namespace the meta should
 * @param {PluginBase} [opts.plugin] - Optional plugin-instance when running from a plugin.
 */
function CoreZMQ(project, core, mainLogger, opts) {
    const responder = zmq.socket('rep');
    const roots = {};
    const logger = mainLogger.fork('CoreZMQ');
    opts = opts || {};

    const plugin = opts.plugin;

    const initialPort = opts.port || 5555;
    const portAttempts = opts.portAttempts || 100;
    const address = opts.address;

    /**
     * Retrieves a node by loading it.
     * @param {object} nodeWrapper
     * @param {string} nodeWrapper.rootId
     * @param {string} nodeWrapper.nodePath
     * @returns {external:Promise}
     */
    const getNode = (nodeWrapper) => {
        const rootNode = roots[nodeWrapper.rootId];
        if (!rootNode) {
            return Q.reject(new Error(`No root loaded at rootId: [${nodeWrapper.rootId}]!`));
        }

        return core.loadByPath(rootNode, nodeWrapper.nodePath);
    };

    const getNodeDataWrapper = (node, orgNodeWrapper) => {
        return {
            rootId: orgNodeWrapper.rootId,
            nodePath: core.getPath(node),
        };
    };

    const getNodesDictDataWrapper = (nodesDict, orgNodeWrapper) => {
        const result = {};
        Object.keys(nodesDict)
            .forEach((key) => {
                result[key] = getNodeDataWrapper(nodesDict[key], orgNodeWrapper);
            });

        return result;
    };

    function send(payload) {
        const serialized = JSON.stringify(payload);
        if (payload.err) {
            logger.error('res', payload);
        } else {
            logger.debug('res', payload);
        }

        responder.send(serialized);
    }

    function sendError(err, req) {
        send({
            err: {
                message: err.message,
                type: err.name,
                stack: err.stack,
                req: req,
            },
            res: null
        });
    }

    function sendResult(res) {
        send({err: null, res});
    }

    function handleUtilRequest(req) {

        switch (req.name) {
            case 'META':
                return getNode(req.args[0])
                    .then((rootNode) => {
                        const metaNodeMap = pluginUtil.getMetaNodesMap(core, rootNode, logger,
                            typeof req.args[1] === 'string' ? req.args[1] : opts.namespace);

                        return getNodesDictDataWrapper(metaNodeMap, req.args[0]);
                    });
            case 'gmeConfig':
                return Q(project.gmeConfig);
            case 'save':
                return getNode(req.args[0])
                    .then((rootNode) => {
                        const persisted = core.persist(rootNode);

                        return project.makeCommit(req.args[2],
                            [req.args[1]],
                            persisted.rootHash,
                            persisted.objects,
                            req.args[3]);
                    });
            case 'unloadRoot':
                try {
                    delete roots[req.args[0].rootId];
                    return Q();
                } catch (e) {
                    return Q.reject(e);
                }
            default:
                return Q.reject(new Error(`Unexpected request name ${req.name} of type [${req.type}]`));
        }
    }

    function handleCoreRequest(req) {
        const deferred = Q.defer();

        switch (req.name) {
            case 'loadRoot':
                if (roots.hasOwnProperty(req.args[0])) {
                    logger.warn('Attempting to load same root-hash twice, resolving with same node..');
                    deferred.resolve({
                        rootId: req.args[0],
                        nodePath: '',
                    });
                } else {
                    core.loadRoot(req.args[0])
                        .then((rootNode) => {
                            roots[req.args[0]] = rootNode;
                            deferred.resolve({
                                rootId: req.args[0],
                                nodePath: '',
                            });
                        })
                        .catch(deferred.reject);
                }
                break;
            case 'addMember':
            case 'setAspectMetaTarget':
                Q.all([
                    getNode(req.args[0]),
                    getNode(req.args[2]),
                ])
                    .then((nodes) => {
                        deferred.resolve(core[req.name](nodes[0], req.args[1], nodes[1]));
                    })
                    .catch(deferred.reject);
                break;
            case 'setPointer':
                Q.all([
                    getNode(req.args[0]),
                    req.args[2] ? getNode(req.args[2]) : Q(null),
                ])
                    .then((nodes) => {
                        deferred.resolve(core[req.name](nodes[0], req.args[1], nodes[1]));
                    })
                    .catch(deferred.reject);
                break;
            case 'setPointerMetaTarget':
                Q.all([
                    getNode(req.args[0]),
                    getNode(req.args[2]),
                ])
                    .then((nodes) => {
                        deferred.resolve(core[req.name](nodes[0], req.args[1], nodes[1], req.args[3], req.args[4]));
                    })
                    .catch(deferred.reject);
                break;
            case 'applyResolution':
                try {
                    deferred.resolve(core.applyResolution(req.args[0]));
                } catch (e) {
                    deferred.reject(e);
                }
                break;
            case 'tryToConcatChanges':
                try {
                    deferred.resolve(core.tryToConcatChanges(req.args[0], req.args[1]));
                } catch (e) {
                    deferred.reject(e);
                }
                break;
            case 'createChild':
            case 'copyNode':
            case 'moveNode':
                Q.all([
                    getNode(req.args[0]),
                    getNode(req.args[1]),
                ])
                    .then((nodes) => {
                        deferred.resolve(getNodeDataWrapper(core[req.name](nodes[0], nodes[1]), req.args[0]));
                    })
                    .catch(deferred.reject);
                break;
            case 'copyNodes':
                Q.all([
                    Q.all(req.args[0].map(nodeDataWrapper => getNode(nodeDataWrapper))),
                    getNode(req.args[1]),
                ])
                    .then((nodes) => {
                        deferred.resolve(core.copyNodes(nodes[0], nodes[1])
                            .map(newNode => getNodeDataWrapper(newNode, req.args[1]))
                        );
                    })
                    .catch(deferred.reject);
                break;
            case 'createNode':
                Q.all([
                    req.args[0].parent ? getNode(req.args[0].parent) : Q(null),
                    req.args[0].base ? getNode(req.args[0].base) : Q(null),
                ])
                    .then((nodes) => {
                        deferred.resolve(getNodeDataWrapper(
                            core.createNode({
                                parent: nodes[0],
                                base: nodes[1],
                                relid: req.args[0].relid,
                                guid: req.args[0].guid,
                            }), req.args[0].parent || req.args[0].base)
                        );
                    })
                    .catch(deferred.reject);
                break;
            case 'getAllMetaNodes':
            case 'getMixinNodes':
                getNode(req.args[0])
                    .then((node) => {
                        deferred.resolve(getNodesDictDataWrapper(core[req.name](node), req.args[0]));
                    })
                    .catch(deferred.reject);
                break;
            case 'clearMetaRules':
            case 'clearMixins':
            case 'deleteNode':
            case 'getAttributeNames':
            case 'getChildrenHashes':
            case 'getChildrenMeta':
            case 'getChildrenPaths':
            case 'getChildrenRelids':
            case 'getCollectionNames':
            case 'getConstraintNames':
            case 'getFullyQualifiedName':
            case 'getGuid':
            case 'getHash':
            case 'getInstancePaths':
            case 'getJsonMeta':
            case 'getLibraryNames':
            case 'getMixinErrors':
            case 'getMixinPaths':
            case 'getNamespace':
            case 'getOwnAttributeNames':
            case 'getOwnChildrenPaths':
            case 'getOwnChildrenRelids':
            case 'getOwnConstraintNames':
            case 'getOwnJsonMeta':
            case 'getOwnPointerNames':
            case 'getOwnRegistryNames':
            case 'getOwnSetNames':
            case 'getOwnValidAspectNames':
            case 'getOwnValidAttributeNames':
            case 'getOwnValidPointerNames':
            case 'getOwnValidSetNames':
            case 'getPath':
            case 'getPointerNames':
            case 'getRegistryNames':
            case 'getRelid':
            case 'getSetNames':
            case 'getValidAspectNames':
            case 'getValidAttributeNames':
            case 'getValidChildrenPaths':
            case 'getValidPointerNames':
            case 'getValidSetNames':
            case 'isAbstract':
            case 'isConnection':
            case 'isEmpty':
            case 'isLibraryElement':
            case 'isLibraryRoot':
            case 'isMemberOf':
            case 'isMetaNode':
            case 'persist':
                getNode(req.args[0])
                    .then((node) => {
                        deferred.resolve(core[req.name](node));
                    })
                    .catch(deferred.reject);
                break;
            case 'addMixin':
            case 'applyTreeDiff':
            case 'canSetAsMixin':
            case 'createSet':
            case 'delAspectMeta':
            case 'delAttribute':
            case 'delAttributeMeta':
            case 'delChildMeta':
            case 'getCollectionPaths':
            case 'delConstraint':
            case 'deletePointer':
            case 'deleteSet':
            case 'delMixin':
            case 'delPointer':
            case 'delPointerMeta':
            case 'delRegistry':
            case 'delSet':
            case 'getAspectMeta':
            case 'getAttribute':
            case 'getAttributeMeta':
            case 'getConstraint':
            case 'getLibraryGuid':
            case 'getLibraryInfo':
            case 'getMemberPaths':
            case 'getOwnAttribute':
            case 'getOwnMemberPaths':
            case 'getOwnPointerPath':
            case 'getOwnRegistry':
            case 'getOwnSetAttributeNames':
            case 'getOwnSetRegistryNames':
            case 'getOwnValidAspectTargetPaths':
            case 'getOwnValidTargetPaths':
            case 'getPointerMeta':
            case 'getPointerPath':
            case 'getRegistry':
            case 'getSetAttributeNames':
            case 'getSetRegistryNames':
            case 'getValidAspectTargetPaths':
            case 'getValidTargetPaths':
            case 'removeLibrary':
            case 'setGuid':
                getNode(req.args[0])
                    .then((node) => {
                        deferred.resolve(core[req.name](node, req.args[1]));
                    })
                    .catch(deferred.reject);
                break;
            case 'delAspectMetaTarget':
            case 'delMember':
            case 'delSetAttribute':
            case 'delSetRegistry':
            case 'delPointerMetaTarget':
            case 'getMemberAttributeNames':
            case 'getMemberOwnAttributeNames':
            case 'getMemberOwnRegistryNames':
            case 'getMemberRegistryNames':
            case 'getOwnSetAttribute':
            case 'getOwnSetRegistry':
            case 'getSetAttribute':
            case 'getSetRegistry':
            case 'isFullyOverriddenMember':
            case 'isValidAttributeValueOf':
            case 'renameAttribute':
            case 'renameAttributeMeta':
            case 'renameLibrary':
            case 'renamePointer':
            case 'renameRegistry':
            case 'renameSet':
            case 'setAttribute':
            case 'setAttributeMeta':
            case 'setChildrenMetaLimits':
            case 'setConstraint':
            case 'setRegistry':
                getNode(req.args[0])
                    .then((node) => {
                        deferred.resolve(core[req.name](node, req.args[1], req.args[2]));
                    })
                    .catch(deferred.reject);
                break;
            case 'addLibrary':
            case 'delMemberAttribute':
            case 'delMemberRegistry':
            case 'getMemberAttribute':
            case 'getMemberOwnAttribute':
            case 'getMemberOwnRegistry':
            case 'getMemberRegistry':
            case 'moveMember':
            case 'setPointerMetaLimits':
            case 'setSetAttribute':
            case 'setSetRegistry':
            case 'updateLibrary':
                getNode(req.args[0])
                    .then((node) => {
                        deferred.resolve(core[req.name](node, req.args[1], req.args[2], req.args[3]));
                    })
                    .catch(deferred.reject);
                break;
            case 'setMemberAttribute':
            case 'setMemberRegistry':
                getNode(req.args[0])
                    .then((node) => {
                        deferred.resolve(core[req.name](node, req.args[1], req.args[2], req.args[3], req.args[4]));
                    })
                    .catch(deferred.reject);
                break;
            case 'generateTreeDiff':
                deferred.reject(new Error('generateTreeDiff not supported!'));
                break;
            case 'getChildDefinitionInfo':
                Q.all([
                    getNode(req.args[0]),
                    getNode(req.args[1]),
                ])
                    .then((nodes) => {
                        const info = core[req.name](nodes[0], nodes[1]);

                        deferred.resolve({
                            ownerNode: info.ownerNode ? getNodeDataWrapper(info.ownerNode, req.args[0]) : null,
                            targetNode: info.targetNode ? getNodeDataWrapper(info.targetNode, req.args[0]) : null,
                        });
                    })
                    .catch(deferred.reject);
                break;
            case 'getAspectDefinitionInfo':
            case 'getPointerDefinitionInfo':
            case 'getSetDefinitionInfo':
                Q.all([
                    getNode(req.args[0]),
                    getNode(req.args[2]),
                ])
                    .then((nodes) => {
                        const info = core[req.name](nodes[0], req.args[1], nodes[1]);

                        deferred.resolve({
                            ownerNode: info.ownerNode ? getNodeDataWrapper(info.ownerNode, req.args[0]) : null,
                            targetNode: info.targetNode ? getNodeDataWrapper(info.targetNode, req.args[0]) : null,
                        });
                    })
                    .catch(deferred.reject);
                break;
            case 'getBase':
            case 'getBaseRoot':
            case 'getBaseType':
            case 'getFCO':
            case 'getMetaType':
            case 'getParent':
            case 'getRoot':
            case 'getTypeRoot':
                getNode(req.args[0])
                    .then((node) => {
                        const resNode = core[req.name](node);
                        if (resNode) {
                            deferred.resolve(getNodeDataWrapper(resNode, req.args[0]));
                        } else {
                            deferred.resolve(null);
                        }
                    })
                    .catch(deferred.reject);
                break;
            case 'getLibraryRoot':
                getNode(req.args[0])
                    .then((node) => {
                        const resNode = core[req.name](node, req.args[1]);
                        if (resNode) {
                            deferred.resolve(getNodeDataWrapper(resNode, req.args[0]));
                        } else {
                            deferred.resolve(null);
                        }
                    })
                    .catch(deferred.reject);
                break;
            case 'getChild':
                deferred.reject(new Error('getChild not supported!'));
                break;
            case 'isTypeOf':
            case 'isInstanceOf':
                Q.all([
                    getNode(req.args[0]),
                    typeof req.args[1] === 'string' ? Q(req.args[1]) : getNode(req.args[1]),
                ])
                    .then((nodes) => {
                        deferred.resolve(core[req.name](nodes[0], nodes[1]));
                    })
                    .catch(deferred.reject);
                break;
            case 'isValidChildOf':
            case 'isValidNewParent':
                Q.all([
                    getNode(req.args[0]),
                    getNode(req.args[1]),
                ])
                    .then((nodes) => {
                        deferred.resolve(core[req.name](nodes[0], nodes[1]));
                    })
                    .catch(deferred.reject);
                break;
            case 'isValidNewBase':
            case 'setBase':
                Q.all([
                    getNode(req.args[0]),
                    req.args[1] ? getNode(req.args[1]) : Q(null),
                ])
                    .then((nodes) => {
                        deferred.resolve(core[req.name](nodes[0], nodes[1]));
                    })
                    .catch(deferred.reject);
                break;
            case 'isValidNewChild':
                Q.all([
                    req.args[0] ? getNode(req.args[0]) : Q(null),
                    req.args[1] ? getNode(req.args[1]) : Q(null),
                ])
                    .then((nodes) => {
                        deferred.resolve(core[req.name](nodes[0], nodes[1]));
                    })
                    .catch(deferred.reject);
                break;
            case 'isValidAspectMemberOf':
            case 'isValidTargetOf':
                Q.all([
                    getNode(req.args[0]),
                    getNode(req.args[1]),
                ])
                    .then((nodes) => {
                        deferred.resolve(core[req.name](nodes[0], nodes[1], req.args[2]));
                    })
                    .catch(deferred.reject);
                break;
            case 'moveAspectMetaTarget':
            case 'movePointerMetaTarget':
            case 'setChildMeta':
                Q.all([
                    getNode(req.args[0]),
                    getNode(req.args[1]),
                ])
                    .then((nodes) => {
                        deferred.resolve(core[req.name](nodes[0], nodes[1], req.args[2], req.args[3]));
                    })
                    .catch(deferred.reject);
                break;
            case 'loadByPath':
            case 'loadChild':
            case 'loadPointer':
                getNode(req.args[0])
                    .then((node) => {
                        return core[req.name](node, req.args[1]);
                    })
                    .then((resNode) => {
                        if (resNode) {
                            deferred.resolve(getNodeDataWrapper(resNode, req.args[0]));
                        } else {
                            // Important difference between null and undefined!
                            deferred.resolve(resNode);
                        }
                    })
                    .catch(deferred.reject);
                break;
            case 'loadChildren':
            case 'loadInstances':
            case 'loadOwnChildren':
            case 'loadOwnSubTree':
            case 'loadSubTree':
                getNode(req.args[0])
                    .then((node) => {
                        return core[req.name](node);
                    })
                    .then((resNodes) => {
                        deferred.resolve(resNodes.map(resNode => getNodeDataWrapper(resNode, req.args[0])));
                    })
                    .catch(deferred.reject);
                break;
            case 'loadCollection':
            case 'loadMembers':
            case 'loadOwnMembers':
                getNode(req.args[0])
                    .then((node) => {
                        return core[req.name](node, req.args[1]);
                    })
                    .then((resNodes) => {
                        deferred.resolve(resNodes.map(resNode => getNodeDataWrapper(resNode, req.args[0])));
                    })
                    .catch(deferred.reject);
                break;
            case 'getCommonBase':
            case 'getCommonParent':
                try {
                    Q.all(req.args[0].map(nodeDataWrapper => getNode(nodeDataWrapper)))
                        .then((nodes) => {
                            const resNode = core[req.name].apply(core, nodes);
                            if (resNode) {
                                deferred.resolve(getNodeDataWrapper(resNode, req.args[0][0]));
                            } else {
                                deferred.resolve(null);
                            }
                        });
                } catch (e) {
                    deferred.reject(e);
                }
                break;
            case 'getBaseTypes':
                getNode(req.args[0])
                    .then((node) => {
                        deferred.resolve(core[req.name](node)
                            .map(resNode => getNodeDataWrapper(resNode, req.args[0])
                            ));
                    })
                    .catch(deferred.reject);
                break;
            case 'getLibraryMetaNodes':
                getNode(req.args[0])
                    .then((node) => {
                        deferred.resolve(core[req.name](node, req.args[1], req.args[2])
                            .map(resNode => getNodeDataWrapper(resNode, req.args[0])
                            ));
                    })
                    .catch(deferred.reject);
                break;
            case 'getValidChildrenMetaNodes':
                Q.all([
                    getNode(req.args[0].node),
                    Q.all((req.args[0].children || []).map(nodeDataWrapper => getNode(nodeDataWrapper))),
                ])
                    .then((nodes) => {
                        return deferred.resolve(core.getValidChildrenMetaNodes(
                            {
                                node: nodes[0],
                                children: nodes[1],
                                sensitive: !!req.args[0].sensitive,
                                multiplicity: !!req.args[0].multiplicity,
                                aspect: req.args[0].aspect,
                            }).map(validNode => getNodeDataWrapper(validNode, req.args[0].node))
                        );
                    })
                    .catch(deferred.reject);
                break;
            case 'getValidSetElementsMetaNodes':
                Q.all([
                    getNode(req.args[0].node),
                    Q.all((req.args[0].members || []).map(nodeDataWrapper => getNode(nodeDataWrapper))),
                ])
                    .then((nodes) => {
                        return deferred.resolve(core.getValidSetElementsMetaNodes(
                            {
                                node: nodes[0],
                                members: nodes[1],
                                name: req.args[0].name,
                                sensitive: !!req.args[0].sensitive,
                                multiplicity: !!req.args[0].multiplicity,
                            }).map(validNode => getNodeDataWrapper(validNode, req.args[0].node))
                        );
                    })
                    .catch(deferred.reject);
                break;
            case 'getAspectDefinitionOwner':
            case 'getAttributeDefinitionOwner':
                getNode(req.args[0])
                    .then((node) => {
                        deferred.resolve(getNodeDataWrapper(core[req.name](node, req.args[1]), req.args[0]));
                    })
                    .catch(deferred.reject);
                break;
            case 'CONSTANTS':
                deferred.resolve(core.CONSTANTS);
                break;
            default:
                throw new Error(`Unexpected request name ${req.name} of type [${req.type}]`);
        }

        return deferred.promise;
    }

    function handleProjectRequest(req) {
        let deferred;

        switch (req.name) {
            case 'getBranches':
            case 'getProjectInfo':
            case 'getTags':
                return project[req.name]();
            case 'getUserId':
                try {
                    return Q(project.getUserId());
                } catch (e) {
                    return Q.reject(e);
                }
            case 'deleteTag':
            case 'getBranchHash':
            case 'getCommitObject':
            case 'getRootHash':
                return project[req.name](req.args[0]);
            case 'createBranch':
            case 'createTag':
            case 'deleteBranch':
            case 'getCommits':
            case 'getCommonAncestorCommit':
            case 'getHistory':
                return project[req.name](req.args[0], req.args[1]);
            case 'setBranchHash':
                return project[req.name](req.args[0], req.args[1], req.args[2]);
            case 'makeCommit':
                return project[req.name](req.args[0], req.args[1], req.args[2], req.args[3], req.args[4]);
            case 'loadObject':
                deferred = Q.defer();
                project[req.name](req.args[0], (err, obj) => {
                    if (err) {
                        deferred.reject(err);
                    } else {
                        deferred.resolve(obj);
                    }
                });
                return deferred.promise;
            case 'loadPaths':
                deferred = Q.defer();
                project[req.name](req.args[0], req.args[1], (err, obj) => {
                    if (err) {
                        deferred.reject(err);
                    } else {
                        deferred.resolve(obj);
                    }
                });
                return deferred.promise;
            case 'CONSTANTS':
                return Q(project.CONSTANTS);
            default:
                return Q.reject(new Error(`Unexpected request name ${req.name} of type [${req.type}]`));
        }
    }

    function handlePluginRequest(req) {
        switch (req.name) {
            case 'getCurrentConfig':
                try {
                    return Q(plugin[req.name]());
                } catch (e) {
                    return Q.reject(e);
                }
            case 'sendNotification':
                try {
                    return Q(plugin[req.name](req.args[0]));
                } catch (e) {
                    return Q.reject(e);
                }
            case 'createMessage':
                return getNode(req.args[0])
                    .then((node) => {
                        plugin[req.name](node, req.args[1], req.args[2]);
                    });
            case 'getFile':
            case 'getArtifact':
                try {
                    return plugin[req.name](req.args[0]);
                } catch (e) {
                    return Q.reject(e);
                }
            case 'getBinFile':
                try {
                    return plugin[req.name](req.args[0], req.args[1], null)
                    .then(bufferContent => {
                        return Q(bufferContent.toString());
                    })
                    .catch(Q.reject);
                } catch (e) {
                    return Q.reject(e);
                }
            case 'addFile':
                try {
                    const is_bytes = req.args[2];
                    let data;
                    if (is_bytes) {
                        data = Buffer.from(req.args[1])
                    }else{
                        data = req.args[1]
                    }
                    return plugin[req.name](req.args[0], data);
                } catch (e) {
                    return Q.reject(e);
                }
            case 'addArtifact':
                try {
                    const files = {};
                    for (const [key, value] of Object.entries(req.args[1])) {
                        if (value.binary) {
                            files[key] = Buffer.from(value.content);
                        } else {
                            files[key] = value.content;
                        }
                    }

                    return plugin[req.name](req.args[0], files);
                } catch (e) {
                    return Q.reject(e);
                }
            case 'resultSetSuccess':
                try {
                    plugin.result.setSuccess(req.args[0]);
                    return Q(null);
                } catch(e) {
                    return Q.reject(e);
                }
            case 'resultSetError':
                try {
                    plugin.result.setError(req.args[0]);
                    return Q(null);
                } catch(e) {
                    return Q.reject(e);
                }
            default:
                // There will not be an error if the plugin instance has the required function.
                // It will only pass all the arguments as a proxy

                if (typeof plugin[req.name] === 'function') {
                    logger.info(`Special function [${req.name}] is called`);
                    return Q(plugin[req.name](...req.args));
                } else {
                    return Q.reject(new Error(`Unexpected request name ${req.name} of type [${req.type}]`));
                }
        }
    }

    /**
     *
     * @param {function} [callback]
     * @param {null|Error} callback.err
     * @param {number} callback.port
     * @returns {external:Promise}
     */
    this.startServer = (callback) => {
        responder.on('message', (rawReq) => {
            let req;

            try {
                const reqStr = rawReq.toString();
                logger.debug('req:', reqStr);
                req = JSON.parse(reqStr);
            } catch (e) {
                sendError(new Error(`Failed to parse request to json: ${rawReq.toString()}`),
                    'Unable to parse request.');
                return;
            }

            let promise;

            try {
                switch (req.type) {
                    case 'util':
                        promise = handleUtilRequest(req);
                        break;
                    case 'core':
                        promise = handleCoreRequest(req);
                        break;
                    case 'project':
                        promise = handleProjectRequest(req);
                        break;
                    case 'plugin':
                        if (plugin) {
                            promise = handlePluginRequest(req);
                        } else {
                            promise = Q.reject(new Error(`Corezmq wasn't initiated from a plugin - plugin requests.`));
                        }
                        break;
                    default:
                        promise = Q.reject(new Error(`Unexpected request type [${req.type}]`));
                        break;
                }
            } catch (e) {
                promise = Q.reject(e);
            }

            promise.then(sendResult).catch(err => sendError(err, req));
        });
        const maxAttempts = initialPort + portAttempts;

        function bindToPortRec(port) {
            const deferred = Q.defer();
            const errorText = new RegExp('[a|A]ddress.*in use', 'g');
            responder.bind(address || `tcp://127.0.0.1:${port}`, (err) => {
                if (err) {
                    if (!address && errorText.test(err.message)) {
                        logger.warn('Port', port, 'already in use attempting to increase port number');
                        if (port < maxAttempts) {
                            bindToPortRec(port + 1)
                                .then(deferred.resolve)
                                .catch(deferred.reject);
                        } else {
                            deferred.reject(
                                new Error(`Failed to find available port within [${initialPort}, ${maxAttempts}]!`));
                        }
                    } else {
                        deferred.reject(err);
                    }
                } else {
                    deferred.resolve(address || port);
                }
            });

            return deferred.promise;
        }

        return bindToPortRec(initialPort).nodeify(callback);
    };

    /**
     * Stop the server.
     * @param {function} [callback]
     * @returns {Promise}
     */
    this.stopServer = (callback) => {
        responder.close();
        return Q().nodeify(callback);
    };
}

module.exports = CoreZMQ;

