"""
For more details regarding inputs and output in form of complex dictionaries see the original source docs at:

%host%/docs/source/Core.html

for example:

`https://editor.webgme.org/docs/source/Core.html <https://editor.webgme.org/docs/source/Core.html>`_
"""


class Core(object):
    """
    Class for querying and manipulating the tree graph in a gme project. Practically, each method takes at least one
    node-dict as input. Use core.load_root(root_hash) to get an initial root-node of a the tree.
    """

    def __init__(self, webgme):
        self._webgme = webgme
        self._CONSTANTS = None

    def _send(self, payload):
        payload['type'] = 'core'
        self._webgme.send_request(payload)
        return self._webgme.handle_response()

    @property
    def CONSTANTS(self):
        """
        A dictionary with the `constants associated with the Core <https://github.com/webgme/webgme-engine/blob/master/src/common/core/constants.js>`_.
        """
        if self._CONSTANTS is None:
            self._CONSTANTS = self._send({'name': 'CONSTANTS', 'args': []})

        return self._CONSTANTS

    def add_library(self, node, name, library_root_hash, library_info=None):
        """
        It adds a project as library to your project by copying it over. The library will be a node\        with the given name directly under your project's ROOT. It becomes a read-only portion of your project.\        You will only be able to manipulate it with library functions, but cannot edit the individual nodes inside.\        However you will be able to instantiate or copy the nodes into other places of your project. Every node\        that was part of the META in the originating project becomes part of your project's meta.

        :param node: any regular node in your project.
        :type node: dict
        :param name: the name of the library you wish to use as a namespace in your project.
        :type name: str
        :param library_root_hash: the hash of your library's root\        (must exist in the project's collection at the time of call).
        :type library_root_hash: str
        :param library_info: information about your project.
        :type library_info: dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the result of the execution.
        :raises CoreIllegalOperationError: the result of the execution.
        :raises CoreInternalError: the result of the execution.
        """
        return self._send({'name': 'addLibrary', 'args': [node, name, library_root_hash, library_info]})

    def add_member(self, node, name, member):
        """
        Adds a member to the given set.

        :param node: the owner of the set.
        :type node: dict
        :param name: the name of the set.
        :type name: str
        :param member: the new member of the set.
        :type member: dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'addMember', 'args': [node, name, member]})

    def add_mixin(self, node, path):
        """
        Adds a mixin to the mixin set of the node.

        :param node: the node in question.
        :type node: dict
        :param path: the path of the mixin node.
        :type path: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'addMixin', 'args': [node, path]})

    def apply_resolution(self, conflict):
        """
        When our attempt to merge two patches ended in some conflict, then we can modify that result highlighting\        that in case of every conflict, which side we prefer (mine vs. theirs). If we give that object as an input\        to this function, it will finish the merge resolving the conflict according our settings and present a final\        patch.

        :param conflict: the object that represents our settings for every conflict and the so-far-merged\        patch.
        :type conflict: dict
        :returns: The function results in a tree structured patch object that contains the changesthat cover\        both parties modifications (and the conflicts are resolved according the input settings).
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'applyResolution', 'args': [conflict]})

    def apply_tree_diff(self, node, patch):
        """
        Apply changes to the current project.

        :param node: the root of the containment hierarchy where we wish to apply the changes
        :type node: dict
        :param patch: the tree structured collection of changes represented with a special JSON object
        :type patch: dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the result of the execution.
        :raises CoreInternalError: the result of the execution.
        """
        return self._send({'name': 'applyTreeDiff', 'args': [node, patch]})

    def can_set_as_mixin(self, node, path):
        """
        Checks if the given path can be added as a mixin to the given node.

        :param node: the node in question.
        :type node: dict
        :param path: the path of the mixin node.
        :type path: str
        :returns: Returns an object with isOk set to true if the given path can be added as a\        mixin to the given node. If it cannot, the reason will be reported under reason.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'canSetAsMixin', 'args': [node, path]})

    def clear_meta_rules(self, node):
        """
        Removes all META rules defined at the node. Note that it does not clear any rules from other meta-nodes\        where the node if referenced.

        :param node: the node in question.
        :type node: dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'clearMetaRules', 'args': [node]})

    def clear_mixins(self, node):
        """
        Removes all mixins for a given node.

        :param node: the node in question.
        :type node: dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'clearMixins', 'args': [node]})

    def copy_node(self, node, parent):
        """
        Copies the given node into parent.

        :param node: the node to be copied.
        :type node: dict
        :param parent: the parent node of the copy.
        :type parent: dict
        :returns: The function returns the copied node.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'copyNode', 'args': [node, parent]})

    def copy_nodes(self, nodes, parent):
        """
        Copies the given nodes into parent.

        :param nodes: the nodes to be copied.
        :type nodes: list of dict
        :param parent: the parent node of the copy.
        :type parent: dict
        :returns: The function returns an array of the copied nodes. The order follows\        the order of originals.
        :rtype: list of dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'copyNodes', 'args': [nodes, parent]})

    def create_child(self, node, base):
        """
        Creates a child, with base as provided, inside the provided node.

        :param node: the parent of the node to be created.
        :type node: dict
        :param base: the base of the node to be created.
        :type base: dict
        :returns: The function returns the created child node.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'createChild', 'args': [node, base]})

    def create_node(self, parameters=None):
        """
        Creates a node according to the given parameters.

        :param parameters: the details of the creation.
        :type parameters: dict
        :returns: The function returns the created node.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'createNode', 'args': [parameters]})

    def create_set(self, node, name):
        """
        Creates a set for the node.

        :param node: the owner of the set.
        :type node: dict
        :param name: the name of the set.
        :type name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'createSet', 'args': [node, name]})

    def del_aspect_meta(self, node, name):
        """
        Removes the given aspect rule of the node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the aspect.
        :type name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delAspectMeta', 'args': [node, name]})

    def del_aspect_meta_target(self, node, name, path):
        """
        Removes a valid type from the given aspect of the node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the aspect.
        :type name: str
        :param path: the absolute path of the valid type of the aspect.
        :type path: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delAspectMetaTarget', 'args': [node, name, path]})

    def del_attribute(self, node, name):
        """
        Removes the given attributes from the given node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the attribute.
        :type name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delAttribute', 'args': [node, name]})

    def del_attribute_meta(self, node, name):
        """
        Removes an attribute definition from the META rules of the node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the attribute.
        :type name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delAttributeMeta', 'args': [node, name]})

    def del_child_meta(self, node, path):
        """
        Removes the given child rule from the node.

        :param node: the node in question.
        :type node: dict
        :param path: the absolute path of the child which rule is to be removed from the node.
        :type path: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delChildMeta', 'args': [node, path]})

    def del_constraint(self, node, name):
        """
        Removes a constraint from the node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the constraint.
        :type name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delConstraint', 'args': [node, name]})

    def del_member(self, node, name, path):
        """
        Removes a member from the set. The functions doesn't remove the node itself.

        :param node: the owner of the set.
        :type node: dict
        :param name: the name of the set.
        :type name: str
        :param path: the absolute path of the member to be removed.
        :type path: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delMember', 'args': [node, name, path]})

    def del_member_attribute(self, node, set_name, member_path, attr_name):
        """
        Removes an attribute which represented a property of the given set membership.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param member_path: the absolute path of the member node.
        :type member_path: str
        :param attr_name: the name of the attribute.
        :type attr_name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delMemberAttribute', 'args': [node, set_name, member_path, attr_name]})

    def del_member_registry(self, node, set_name, path, reg_name):
        """
        Removes a registry entry which represented a property of the given set membership.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param path: the absolute path of the member node.
        :type path: str
        :param reg_name: the name of the registry entry.
        :type reg_name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delMemberRegistry', 'args': [node, set_name, path, reg_name]})

    def del_mixin(self, node, path):
        """
        Removes a mixin from the mixin set of the node.

        :param node: the node in question.
        :type node: dict
        :param path: the path of the mixin node.
        :type path: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delMixin', 'args': [node, path]})

    def del_pointer(self, node, name):
        """
        Removes the pointer from the node. (Aliased deletePointer.)

        :param node: the node in question.
        :type node: dict
        :param name: the name of the pointer in question.
        :type name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delPointer', 'args': [node, name]})

    def del_pointer_meta(self, node, name):
        """
        Removes the complete META rule regarding the given pointer/set of the node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the pointer/set.
        :type name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delPointerMeta', 'args': [node, name]})

    def del_pointer_meta_target(self, node, name, path):
        """
        Removes a possible target type from the pointer/set of the node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the pointer/set
        :type name: str
        :param path: the absolute path of the possible target type.
        :type path: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If node is read-only, or definition does not exist.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delPointerMetaTarget', 'args': [node, name, path]})

    def del_registry(self, node, name):
        """
        Removes the given registry entry from the given node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the registry entry.
        :type name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delRegistry', 'args': [node, name]})

    def del_set(self, node, name):
        """
        Removes a set from the node. (Aliased deleteSet.)

        :param node: the owner of the set.
        :type node: dict
        :param name: the name of the set.
        :type name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delSet', 'args': [node, name]})

    def del_set_attribute(self, node, set_name, attr_name):
        """
        Removes the attribute entry for the set at the node.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param attr_name: the name of the attribute entry.
        :type attr_name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delSetAttribute', 'args': [node, set_name, attr_name]})

    def del_set_registry(self, node, set_name, reg_name):
        """
        Removes the registry entry for the set at the node.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param reg_name: the name of the registry entry.
        :type reg_name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'delSetRegistry', 'args': [node, set_name, reg_name]})

    def delete_node(self, node):
        """
        Removes a node from the containment hierarchy.

        :param node: the node to be removed.
        :type node: dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'deleteNode', 'args': [node]})

    def delete_pointer(self, node, name):
        """
        Removes the pointer from the node. (Aliased delPointer.)

        :param node: the node in question.
        :type node: dict
        :param name: the name of the pointer in question.
        :type name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'deletePointer', 'args': [node, name]})

    def delete_set(self, node, name):
        """
        Removes a set from the node. (Aliased delSet.)

        :param node: the owner of the set.
        :type node: dict
        :param name: the name of the set.
        :type name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'deleteSet', 'args': [node, name]})

    def generate_tree_diff(self, source_root, target_root):
        """
        Generates a differential tree among the two states of the project that contains the necessary changes\        that can modify the source to be identical to the target. The result is in form of a json object.

        :param source_root: the root node of the source state.
        :type source_root: dict
        :param target_root: the root node of the target state.
        :type target_root: dict
        :returns: the difference between the two containment hierarchies in\        a special JSON object
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the status of the exectuion.
        :raises CoreInternalError: the status of the exectuion.
        """
        return self._send({'name': 'generateTreeDiff', 'args': [source_root, target_root]})

    def get_all_meta_nodes(self, node):
        """
        Returns all META nodes.

        :param node: any node of the containment hierarchy.
        :type node: dict
        :returns: The function returns a dictionary. The keys of the dictionary\        are the absolute paths of the META nodes of the project. Every value of the dictionary\        is a {@link module:Core~Node}.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getAllMetaNodes', 'args': [node]})

    def get_aspect_definition_info(self, node, name, member):
        """
        Returns the meta nodes that introduce the given aspect relationship.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the set in question.
        :type name: str
        :param member: the child.
        :type member: dict
        :returns: The owner and the target of the aspect meta-rule that makes member a\        valid member of the named aspect of node.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getAspectDefinitionInfo', 'args': [node, name, member]})

    def get_aspect_definition_owner(self, node, name):
        """
        Returns the meta node that introduces the given aspect.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the set in question.
        :type name: str
        :returns: The meta-node that defines the aspect and makes a valid aspect for the given node.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getAspectDefinitionOwner', 'args': [node, name]})

    def get_aspect_meta(self, node, name):
        """
        Returns the list of valid children types of the given aspect.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the aspect.
        :type name: str
        :returns: The function returns a list of absolute paths of nodes that are valid children of the node\        and fits to the META rules defined for the aspect. Any children, visible under the given aspect of the node\        must be an instance of at least one node represented by the absolute paths.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getAspectMeta', 'args': [node, name]})

    def get_attribute(self, node, name):
        """
        Retrieves the value of the given attribute of the given node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the attribute.
        :type name: str
        :returns: The function returns the value of the attribute of the node.\        If the value is undefined that means the node do not have\        such attribute defined.
        :rtype: str or int or float or bool or dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getAttribute', 'args': [node, name]})

    def get_attribute_definition_owner(self, node, name):
        """
        Returns the meta node that introduces the given attribute.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the attribute in question.
        :type name: str
        :returns: The meta-node that defines the attribute and makes it valid attribute for the\        given node.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getAttributeDefinitionOwner', 'args': [node, name]})

    def get_attribute_meta(self, node, name):
        """
        Returns the definition object of an attribute from the META rules of the node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the attribute.
        :type name: str
        :returns: The function returns the definition object, where type is always defined.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getAttributeMeta', 'args': [node, name]})

    def get_attribute_names(self, node):
        """
        Returns the names of the defined attributes of the node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns an array of the names of the attributes of the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getAttributeNames', 'args': [node]})

    def get_base(self, node):
        """
        Returns the base node.

        :param node: the node in question.
        :type node: dict
        :returns: Returns the base of the given node or null if there is no such node.
        :rtype: dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getBase', 'args': [node]})

    def get_base_root(self, node):
        """
        Returns the root of the inheritance chain of the given node.

        :param node: the node in question.
        :type node: dict
        :returns: Returns the root of the inheritance chain (usually the FCO).
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getBaseRoot', 'args': [node]})

    def get_base_type(self, node):
        """
        Returns the meta-node of the node in question, that is the first base node that is part of the meta.\        (Aliased getMetaType).

        :param node: the node in question
        :type node: dict
        :returns: Returns the first node (including itself) among the inheritance chain\        that is a META node. It returns null if it does not find such node (ideally the only node with this result\        is the ROOT).
        :rtype: dict or None
        :raises CoreIllegalArgumentError: If node is not a Node
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getBaseType', 'args': [node]})

    def get_base_types(self, node):
        """
        Searches for the closest META node of the node in question and the direct mixins of that node.

        :param node: the node in question
        :type node: dict
        :returns: Returns the closest Meta node that is a base of the given node\        plus it returns all the mixin nodes associated with the base.
        :rtype: list of dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getBaseTypes', 'args': [node]})

    def get_child_definition_info(self, node, child):
        """
        Returns the meta nodes that introduce the given containment relationship.

        :param node: the node in question.
        :type node: dict
        :param child: the child.
        :type child: dict
        :returns: The owner and the target of the containment meta-rule that makes child a\        valid child of node.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getChildDefinitionInfo', 'args': [node, child]})

    def get_children_hashes(self, node):
        """
        Collects the data hash values of the children of the node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns a dictionary of\        {@link module:Core~ObjectHash} that stored in pair with the relative id of the corresponding\        child of the node.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getChildrenHashes', 'args': [node]})

    def get_children_meta(self, node):
        """
        Return a JSON representation of the META rules regarding the valid children of the given node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns a detailed JSON structure that represents the META\        rules regarding the possible children of the node.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getChildrenMeta', 'args': [node]})

    def get_children_paths(self, node):
        """
        Collects the paths of all the children of the given node.

        :param node: the container node in question.
        :type node: dict
        :returns: The function returns an array of the absolute paths of the children.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getChildrenPaths', 'args': [node]})

    def get_children_relids(self, node):
        """
        Collects the relative ids of all the children of the given node.

        :param node: the container node in question.
        :type node: dict
        :returns: The function returns an array of the relative ids.
        :rtype: list of str
        """
        return self._send({'name': 'getChildrenRelids', 'args': [node]})

    def get_closure_information(self, nodes):
        """
        Collects the necessary information to export the set of input nodes and use it in other\        - compatible - projects.

        :param nodes: the set of nodes that we want to export
        :type nodes: list of dict
        :returns: If the closure is available for export, the returned special JSON object\        will contain information about the necessary data that needs to be exported as well as relations\        that will need to be recreated in the destination project to preserve the structure of nodes.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getClosureInformation', 'args': [nodes]})

    def get_collection_names(self, node):
        """
        Retrieves a list of the defined pointer names that has the node as target.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns an array of the names of the pointers pointing to the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getCollectionNames', 'args': [node]})

    def get_collection_paths(self, node, name):
        """
        Retrieves a list of absolute paths of nodes that has a given pointer which points to the given node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the pointer.
        :type name: str
        :returns: The function returns an array of absolute paths of nodes that\        has the pointer pointing to the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getCollectionPaths', 'args': [node, name]})

    def get_common_base(self, nodes):
        """
        Returns the common base node of all supplied nodes.

        :param nodes: a variable number of nodes to compare
        :type nodes: list of dict
        :returns: The common base or null if e.g. the root node was passed.
        :rtype: dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getCommonBase', 'args': [nodes]})

    def get_common_parent(self, nodes):
        """
        Returns the common parent node of all supplied nodes.

        :param nodes: a variable number of nodes to compare
        :type nodes: list of dict
        :returns: The common base or null if no nodes were passed.
        :rtype: dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getCommonParent', 'args': [nodes]})

    def get_constraint(self, node, name):
        """
        Gets a constraint object of the node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the constraint.
        :type name: str
        :returns: Returns the defined constraint or null if it was not\        defined for the node.
        :rtype: dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getConstraint', 'args': [node, name]})

    def get_constraint_names(self, node):
        """
        Retrieves the list of constraint names defined for the node.

        :param node: the node in question.
        :type node: dict
        :returns: Returns the array of names of constraints available for the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getConstraintNames', 'args': [node]})

    def get_fco(self, node):
        """
        Return the root of the inheritance chain of your Meta nodes.

        :param node: any node in your project.
        :type node: dict
        :returns: Returns the acting FCO of your project.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getFCO', 'args': [node]})

    def get_fully_qualified_name(self, node):
        """
        Returns the fully qualified name of the node, which is the list of its namespaces separated\        by dot and followed by the name of the node.

        :param node: the node in question.
        :type node: dict
        :returns: Returns the fully qualified name of the node,\        i.e. its namespaces and name join together by dots.
        :rtype: str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getFullyQualifiedName', 'args': [node]})

    def get_guid(self, node):
        """
        Get the GUID of a node.

        :param node: the node in question.
        :type node: dict
        :returns: Returns the globally unique identifier.
        :rtype: str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getGuid', 'args': [node]})

    def get_hash(self, node):
        """
        Returns the calculated hash and database id of the data for the node.

        :param node: the node in question.
        :type node: dict
        :returns: Returns the hash value of the data for the given node.\        An empty string is returned when the node was mutated and not persisted.
        :rtype: str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getHash', 'args': [node]})

    def get_instance_paths(self, node):
        """
        Collects the paths of all the instances of the given node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns an array of the absolute paths of the instances.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getInstancePaths', 'args': [node]})

    def get_json_meta(self, node):
        """
        Gives a JSON representation of the META rules of the node.

        :param node: the node in question.
        :type node: dict
        :returns: Returns an object that represents all the META rules of the node.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getJsonMeta', 'args': [node]})

    def get_library_guid(self, node, name=None):
        """
        Returns the origin GUID of any library node. (If name is not provided the returned GUID will be the same\        across all projects where the library node is contained - regardless of library hierarchy.)

        :param node: the node in question.
        :type node: dict
        :param name: name of the library where we want to compute the GUID from.\        If not given, then the GUID is computed from the direct library root of the node.
        :type name: None or str
        :returns: Returns the origin GUID of the node.
        :rtype: str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getLibraryGuid', 'args': [node, name]})

    def get_library_info(self, node, name):
        """
        Returns the info associated with the library.

        :param node: any node in the project.
        :type node: dict
        :param name: the name of the library.
        :type name: str
        :returns: Returns the information object, stored alongside the library (that basically\        carries metaData about the library).
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getLibraryInfo', 'args': [node, name]})

    def get_library_meta_nodes(self, node, name, only_own=None):
        """
        Returns all the Meta nodes within the given library.\        By default it will include nodes defined in any library within the given library.

        :param node: any node of your project.
        :type node: dict
        :param name: name of your library.
        :type name: str
        :param only_own: if true only returns with Meta nodes defined in the library itself.
        :type only_own: bool
        :returns: Returns an array of core nodes that are part of your meta from\        the given library.
        :rtype: list of dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getLibraryMetaNodes', 'args': [node, name, only_own]})

    def get_library_names(self, node):
        """
        Gives back the list of libraries in your project.

        :param node: any node in your project.
        :type node: dict
        :returns: Returns the fully qualified names of all the libraries in your project\        (even embedded ones).
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getLibraryNames', 'args': [node]})

    def get_library_root(self, node, name):
        """
        Returns the root node of the given library.

        :param node: any node in the project.
        :type node: dict
        :param name: the name of the library.
        :type name: str
        :returns: Returns the library root node or null, if the library is unknown.
        :rtype: dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getLibraryRoot', 'args': [node, name]})

    def get_member_attribute(self, node, set_name, path, attr_name):
        """
        Get the value of the attribute in relation with the set membership.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param path: the absolute path of the member node.
        :type path: str
        :param attr_name: the name of the attribute.
        :type attr_name: str
        :returns: Return the value of the attribute. If it is undefined,\        then there is no such attributed connected to the given set membership.
        :rtype: str or int or float or bool or dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getMemberAttribute', 'args': [node, set_name, path, attr_name]})

    def get_member_attribute_names(self, node, name, path):
        """
        Return the names of the attributes defined for the set membership to the member node.

        :param node: the owner of the set.
        :type node: dict
        :param name: the name of the set.
        :type name: str
        :param path: the absolute path of the member.
        :type path: str
        :returns: Returns the array of names of attributes that represents some property of the membership.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getMemberAttributeNames', 'args': [node, name, path]})

    def get_member_own_attribute(self, node, set_name, path, attr_name):
        """
        Get the value of the attribute for the set membership specifically defined to the member node.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param path: the absolute path of the member node.
        :type path: str
        :param attr_name: the name of the attribute.
        :type attr_name: str
        :returns: Return the value of the attribute. If it is undefined,\        then there is no such attributed connected to the given set membership.
        :rtype: str or int or float or bool or dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getMemberOwnAttribute', 'args': [node, set_name, path, attr_name]})

    def get_member_own_attribute_names(self, node, name, path):
        """
        Return the names of the attributes defined for the set membership specifically defined to the member node.

        :param node: the owner of the set.
        :type node: dict
        :param name: the name of the set.
        :type name: str
        :param path: the absolute path of the member.
        :type path: str
        :returns: Returns the array of names of attributes that represents some property of the membership.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getMemberOwnAttributeNames', 'args': [node, name, path]})

    def get_member_own_registry(self, node, set_name, path, reg_name):
        """
        Get the value of the registry entry for the set membership specifically defined to the member node.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param path: the absolute path of the member node.
        :type path: str
        :param reg_name: the name of the registry entry.
        :type reg_name: str
        :returns: Return the value of the registry. If it is undefined,\        then there is no such registry connected to the given set membership.
        :rtype: str or int or float or bool or dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getMemberOwnRegistry', 'args': [node, set_name, path, reg_name]})

    def get_member_own_registry_names(self, node, name, path):
        """
        Return the names of the registry entries defined for the set membership specifically defined to\        the member node.

        :param node: the owner of the set.
        :type node: dict
        :param name: the name of the set.
        :type name: str
        :param path: the absolute path of the member.
        :type path: str
        :returns: Returns the array of names of registry entries that represents some property of the\        membership.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getMemberOwnRegistryNames', 'args': [node, name, path]})

    def get_member_paths(self, node, name):
        """
        Returns the list of absolute paths of the members of the given set of the given node.

        :param node: the set owner.
        :type node: dict
        :param name: the name of the set.
        :type name: str
        :returns: Returns an array of absolute path strings of the member nodes of the set.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getMemberPaths', 'args': [node, name]})

    def get_member_registry(self, node, set_name, path, reg_name):
        """
        Get the value of the registry entry in relation with the set membership.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param path: the absolute path of the member node.
        :type path: str
        :param reg_name: the name of the registry entry.
        :type reg_name: str
        :returns: Return the value of the registry. If it is undefined,\        then there is no such registry connected to the given set membership.
        :rtype: str or int or float or bool or dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getMemberRegistry', 'args': [node, set_name, path, reg_name]})

    def get_member_registry_names(self, node, name, path):
        """
        Return the names of the registry entries defined for the set membership to the member node.

        :param node: the owner of the set.
        :type node: dict
        :param name: the name of the set.
        :type name: str
        :param path: the absolute path of the member.
        :type path: str
        :returns: Returns the array of names of registry entries that represents some property of the\        membership.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getMemberRegistryNames', 'args': [node, name, path]})

    def get_meta_type(self, node):
        """
        Returns the meta-node of the node in question, that is the first base node that is part of the meta.\        (Aliased getBaseType).

        :param node: the node in question
        :type node: dict
        :returns: Returns the first node (including itself) among the inheritance chain\        that is a META node. It returns null if it does not find such node (ideally the only node with this result\        is the ROOT).
        :rtype: dict or None
        :raises CoreIllegalArgumentError: If node is not a Node
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getMetaType', 'args': [node]})

    def get_mixin_errors(self, node):
        """
        Checks if the mixins allocated with the node can be used.\        Every mixin node should be on the Meta.\        Every rule (attribute/pointer/set/aspect/containment/constraint) should be defined only in one mixin.

        :param node: the node to test.
        :type node: dict
        :returns: Returns the array of violations. If the array is empty,\        there is no violation.
        :rtype: list of dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getMixinErrors', 'args': [node]})

    def get_mixin_nodes(self, node):
        """
        Gathers the mixin nodes defined directly at the node.

        :param node: the node in question.
        :type node: dict
        :returns: The dictionary of the mixin nodes keyed by their paths.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getMixinNodes', 'args': [node]})

    def get_mixin_paths(self, node):
        """
        Gathers the paths of the mixin nodes defined directly at the node.

        :param node: the node in question.
        :type node: dict
        :returns: The paths of the mixins in an array ordered by their order of use (which is important\        in case of some collision among definitions would arise).
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getMixinPaths', 'args': [node]})

    def get_namespace(self, node):
        """
        Returns the resolved namespace for the node. If node is not in a library it returns the\        empty string. If the node is in a library of a library -\        the full name space is the library names joined together by dots.

        :param node: the node in question.
        :type node: dict
        :returns: Returns the name space of the node.
        :rtype: str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getNamespace', 'args': [node]})

    def get_own_attribute(self, node, name):
        """
        Returns the value of the attribute defined for the given node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the attribute.
        :type name: str
        :returns: Returns the value of the attribute defined specifically for\        the node. If undefined then it means that there is no such attribute defined directly for the node, meaning\        that it either inherits some value or there is no such attribute at all.
        :rtype: str or int or float or bool or dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnAttribute', 'args': [node, name]})

    def get_own_attribute_names(self, node):
        """
        Returns the names of the attributes of the node that have been first defined for the node and not for its\        bases.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns an array of the names of the own attributes of the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnAttributeNames', 'args': [node]})

    def get_own_children_paths(self, parent):
        """
        Collects the paths of all the children of the given node that has some data as well and not just inherited.

        :param parent: the container node in question.
        :type parent: dict
        :returns: The function returns an array of the absolute paths of the children.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnChildrenPaths', 'args': [parent]})

    def get_own_children_relids(self, node):
        """
        Collects the relative ids of all the children of the given node that has some data and not just inherited.\        N.B. Do not mutate the returned array!

        :param node: the container node in question.
        :type node: dict
        :returns: The function returns an array of the relative ids.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnChildrenRelids', 'args': [node]})

    def get_own_constraint_names(self, node):
        """
        Retrieves the list of constraint names defined specifically for the node.

        :param node: the node in question.
        :type node: dict
        :returns: Returns the array of names of constraints for the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnConstraintNames', 'args': [node]})

    def get_own_json_meta(self, node):
        """
        Returns the META rules specifically defined for the given node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns an object that represent the META rules that were defined\        specifically for the node.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnJsonMeta', 'args': [node]})

    def get_own_member_paths(self, node, name):
        """
        Returns the list of absolute paths of the members of the given set of the given node that not simply\        inherited.

        :param node: the set owner.
        :type node: dict
        :param name: the name of the set.
        :type name: str
        :returns: Returns an array of absolute path strings of the member nodes of the set that has\        information on the node's inheritance level.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnMemberPaths', 'args': [node, name]})

    def get_own_pointer_names(self, node):
        """
        Returns the list of the names of the pointers that were defined specifically for the node.

        :param node: the node in question.
        :type node: dict
        :returns: Returns an array of names of pointers defined specifically for the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnPointerNames', 'args': [node]})

    def get_own_pointer_path(self, node, name):
        """
        Returns the absolute path of the target of the pointer specifically defined for the node.

        :param node: the node in question
        :type node: dict
        :param name: the name of the pointer
        :type name: str
        :returns: Returns the absolute path. If the path is null, then it means that\        'no-target' was defined specifically for this node for the pointer. If undefined it means that the node\        either inherits the target of the pointer or there is no pointer defined at all.
        :rtype: str or None or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnPointerPath', 'args': [node, name]})

    def get_own_registry(self, node, name):
        """
        Returns the value of the registry entry defined for the given node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the registry entry.
        :type name: str
        :returns: Returns the value of the registry entry defined specifically\        for the node. If undefined then it means that there is no such registry entry defined directly for the node,\        meaning that it either inherits some value or there is no such registry entry at all.
        :rtype: str or int or float or bool or dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnRegistry', 'args': [node, name]})

    def get_own_registry_names(self, node):
        """
        Returns the names of the registry enrties of the node that have been first defined for the node\        and not for its bases.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns an array of the names of the own registry entries of the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnRegistryNames', 'args': [node]})

    def get_own_set_attribute(self, node, set_name, attr_name):
        """
        Get the value of the attribute entry specifically set for the set at the node.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param attr_name: the name of the attribute entry.
        :type attr_name: str
        :returns: Return the value of the attribute. If it is undefined,\        then there is no such attribute at the set.
        :rtype: str or int or float or bool or dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnSetAttribute', 'args': [node, set_name, attr_name]})

    def get_own_set_attribute_names(self, node, name):
        """
        Return the names of the attribute entries specifically set for the set at the node.

        :param node: the owner of the set.
        :type node: dict
        :param name: the name of the set.
        :type name: str
        :returns: Returns the array of names of attribute entries defined in the set at the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnSetAttributeNames', 'args': [node, name]})

    def get_own_set_names(self, node):
        """
        Returns the names of the sets created specifically at the node.\        N.B. When adding a member to a set of a node, the set is automatically created at the node.

        :param node: the node in question.
        :type node: dict
        :returns: Returns an array of set names that were specifically created at the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnSetNames', 'args': [node]})

    def get_own_set_registry(self, node, set_name, reg_name):
        """
        Get the value of the registry entry specifically set for the set at the node.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param reg_name: the name of the registry entry.
        :type reg_name: str
        :returns: Return the value of the registry. If it is undefined,\        then there is no such registry at the set.
        :rtype: str or int or float or bool or dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnSetRegistry', 'args': [node, set_name, reg_name]})

    def get_own_set_registry_names(self, node, name):
        """
        Return the names of the registry entries specifically set for the set at the node.

        :param node: the owner of the set.
        :type node: dict
        :param name: the name of the set.
        :type name: str
        :returns: Returns the array of names of registry entries defined in the set at the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnSetRegistryNames', 'args': [node, name]})

    def get_own_valid_aspect_names(self, node):
        """
        Returns the list of the META defined aspect names of the node that were specifically defined for the node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns the aspect names that are specifically defined for the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnValidAspectNames', 'args': [node]})

    def get_own_valid_aspect_target_paths(self, node, name):
        """
        Returns the paths of the meta nodes that are valid target members of the given aspect\        specifically defined for the node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the aspec in question.
        :type name: str
        :returns: The paths of the meta nodes whose instances could be members of the aspect.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnValidAspectTargetPaths', 'args': [node, name]})

    def get_own_valid_attribute_names(self, node):
        """
        Returns the list of the META defined attribute names of the node that were specifically defined for the node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns the attribute names that are defined specifically for the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnValidAttributeNames', 'args': [node]})

    def get_own_valid_pointer_names(self, node):
        """
        Returns the list of the META defined pointer names of the node that were specifically defined for the node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns all the pointer names that are defined among the META\        rules of the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnValidPointerNames', 'args': [node]})

    def get_own_valid_set_names(self, node):
        """
        Returns the list of the META defined set names of the node that were specifically defined for the node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns all the set names that are defined among the META rules of the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnValidSetNames', 'args': [node]})

    def get_own_valid_target_paths(self, node, name):
        """
        Returns the paths of Meta nodes that are possible targets of the given pointer/set introduced by the node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of pointer/set.
        :type name: str
        :returns: The function returns the paths of valid nodes.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getOwnValidTargetPaths', 'args': [node, name]})

    def get_parent(self, node):
        """
        Returns the parent of the node.

        :param node: the node in question
        :type node: dict
        :returns: Returns the parent of the node or NULL if it has no parent.
        :rtype: dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getParent', 'args': [node]})

    def get_path(self, node):
        """
        Returns the complete path of the node in the containment hierarchy.

        :param node: the node in question.
        :type node: dict
        :returns: Returns a path string where each portion is a relative id and they are separated by '/'.\        The path can be empty as well if the node in question is the  root itself, otherwise it should be a chain\        of relative ids from the root of the containment hierarchy.
        :rtype: str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getPath', 'args': [node]})

    def get_pointer_definition_info(self, node, name, target):
        """
        Returns the meta nodes that introduce the given pointer relationship.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the pointer in question.
        :type name: str
        :param target: the target node.
        :type target: dict
        :returns: The owner and the target of the pointer meta-rule that makes target a\        valid target of the named pointer of node.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getPointerDefinitionInfo', 'args': [node, name, target]})

    def get_pointer_meta(self, node, name):
        """
        Return a JSON representation of the META rules regarding the given pointer/set of the given node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the pointer/set.
        :type name: str
        :returns: The function returns a detailed JSON structure that\        represents the META rules regarding the given pointer/set of the node.
        :rtype: dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getPointerMeta', 'args': [node, name]})

    def get_pointer_names(self, node):
        """
        Retrieves a list of the defined pointer names of the node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns an array of the names of the pointers of the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getPointerNames', 'args': [node]})

    def get_pointer_path(self, node, name):
        """
        Retrieves the path of the target of the given pointer of the given node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the pointer in question.
        :type name: str
        :returns: The function returns the absolute path of the target node\        if there is a valid target. It returns null if though the pointer is defined it does not have any\        valid target. Finally, it return undefined if there is no pointer defined for the node under the given name.
        :rtype: str or None or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getPointerPath', 'args': [node, name]})

    def get_registry(self, node, name):
        """
        Retrieves the value of the given registry entry of the given node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the registry entry.
        :type name: str
        :returns: The function returns the value of the registry entry\        of the node. The value can be an object or any primitive type. If the value is undefined that means\        the node do not have such attribute defined.
        :rtype: str or int or float or bool or dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getRegistry', 'args': [node, name]})

    def get_registry_names(self, node):
        """
        Returns the names of the defined registry entries of the node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns an array of the names of the registry entries of the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getRegistryNames', 'args': [node]})

    def get_relid(self, node):
        """
        Returns the parent-relative identifier of the node.

        :param node: the node in question.
        :type node: dict
        :returns: Returns the last segment of the node path.
        :rtype: str or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getRelid', 'args': [node]})

    def get_root(self, node):
        """
        Returns the root node of the containment tree that node is part of.

        :param node: the node in question.
        :type node: dict
        :returns: Returns the root of the containment hierarchy (it can be the node itself).
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getRoot', 'args': [node]})

    def get_set_attribute(self, node, set_name, attr_name):
        """
        Get the value of the attribute entry in the set.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param attr_name: the name of the attribute entry.
        :type attr_name: str
        :returns: Return the value of the attribute. If it is undefined,\        then there is no such attribute at the set.
        :rtype: str or int or float or bool or dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getSetAttribute', 'args': [node, set_name, attr_name]})

    def get_set_attribute_names(self, node, name):
        """
        Return the names of the attribute entries for the set.

        :param node: the owner of the set.
        :type node: dict
        :param name: the name of the set.
        :type name: str
        :returns: Returns the array of names of attribute entries in the set.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getSetAttributeNames', 'args': [node, name]})

    def get_set_definition_info(self, node, name, member):
        """
        Returns the meta nodes that introduce the given set relationship.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the set in question.
        :type name: str
        :param member: the member.
        :type member: dict
        :returns: The owner and the target of the set meta-rule that makes member a\        valid member of the named set of node.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getSetDefinitionInfo', 'args': [node, name, member]})

    def get_set_names(self, node):
        """
        Returns the names of the sets of the node.

        :param node: the node in question.
        :type node: dict
        :returns: Returns an array of set names that the node has.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getSetNames', 'args': [node]})

    def get_set_registry(self, node, set_name, reg_name):
        """
        Get the value of the registry entry in the set.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param reg_name: the name of the registry entry.
        :type reg_name: str
        :returns: Return the value of the registry. If it is undefined,\        then there is no such registry at the set.
        :rtype: str or int or float or bool or dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getSetRegistry', 'args': [node, set_name, reg_name]})

    def get_set_registry_names(self, node, name):
        """
        Return the names of the registry entries for the set.

        :param node: the owner of the set.
        :type node: dict
        :param name: the name of the set.
        :type name: str
        :returns: Returns the array of names of registry entries in the set.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getSetRegistryNames', 'args': [node, name]})

    def get_type_root(self, node):
        """
        Returns the root of the inheritance chain (cannot be the node itself).

        :param node: the node in question.
        :type node: dict
        :returns: Returns the root of the inheritance chain of the node. If returns null,\        that means the node in question is the root of the chain.
        :rtype: dict or None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getTypeRoot', 'args': [node]})

    def get_valid_aspect_names(self, node):
        """
        Returns the list of the META defined aspect names of the node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns all the aspect names that are defined among the META rules of the\        node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getValidAspectNames', 'args': [node]})

    def get_valid_aspect_target_paths(self, node, name):
        """
        Returns the paths of the meta nodes that are valid target members of the given aspect.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the aspec in question.
        :type name: str
        :returns: The paths of the meta nodes whose instances could be members of the aspect.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getValidAspectTargetPaths', 'args': [node, name]})

    def get_valid_attribute_names(self, node):
        """
        Returns the list of the META defined attribute names of the node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns all the attribute names that are defined among the META rules of the\        node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getValidAttributeNames', 'args': [node]})

    def get_valid_children_meta_nodes(self, parameters):
        """
        Retrieves the valid META nodes that can be base of a child of the node.

        :param parameters: the input parameters of the query.
        :type parameters: dict
        :returns: The function returns a list of valid nodes that can be instantiated as a\        child of the node.
        :rtype: list of dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getValidChildrenMetaNodes', 'args': [parameters]})

    def get_valid_children_paths(self, node):
        """
        Returns the list of absolute path of the valid children types of the node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns an array of absolute paths of the nodes that was defined as valid\        children for the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getValidChildrenPaths', 'args': [node]})

    def get_valid_pointer_names(self, node):
        """
        Returns the list of the META defined pointer names of the node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns all the pointer names that are defined among the META rules\        of the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getValidPointerNames', 'args': [node]})

    def get_valid_set_elements_meta_nodes(self, parameters):
        """
        Retrieves the valid META nodes that can be base of a member of the set of the node.

        :param parameters: the input parameters of the query.
        :type parameters: dict
        :returns: The function returns a list of valid nodes that can be instantiated as a\        member of the set of the node.
        :rtype: list of dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getValidSetElementsMetaNodes', 'args': [parameters]})

    def get_valid_set_names(self, node):
        """
        Returns the list of the META defined set names of the node.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns all the set names that are defined among the META rules of the node.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getValidSetNames', 'args': [node]})

    def get_valid_target_paths(self, node, name):
        """
        Returns the paths of Meta nodes that are possible targets of the given pointer/set.

        :param node: the node in question.
        :type node: dict
        :param name: the name of pointer/set.
        :type name: str
        :returns: The function returns the paths of valid nodes.
        :rtype: list of str
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'getValidTargetPaths', 'args': [node, name]})

    def import_closure(self, node, closure_information):
        """
        Imports the set of nodes in the closureInformation - that has the format created by\        [getClosureInformation]{@link Core#getClosureInformation} - as direct children of the parent node.\        All data necessary for importing the closure has to be imported beforehand!

        :param node: the parent node where the closure will be imported.
        :type node: dict
        :param closure_information: the information about the closure.
        :type closure_information: dict
        :returns: If the closure cannot be imported the resulting error highlights the causes,\        otherwise a specific object will be returned that holds information about the closure.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'importClosure', 'args': [node, closure_information]})

    def is_abstract(self, node):
        """
        Checks if the node is abstract.

        :param node: the node in question.
        :type node: dict
        :returns: The function returns true if the registry entry 'isAbstract' of the node if true hence\        the node is abstract.
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isAbstract', 'args': [node]})

    def is_connection(self, node):
        """
        Check is the node is a connection-like node.

        :param node: the node in question.
        :type node: dict
        :returns: Returns true if both the 'src' and 'dst' pointer are defined as valid for the node.
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isConnection', 'args': [node]})

    def is_empty(self, node):
        """
        Checks if the node in question has some actual data.

        :param node: the node in question.
        :type node: dict
        :returns: Returns true if the node is 'empty' meaning that it is not reserved by real data.\        Returns false if the node is exists and have some meaningful value.
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isEmpty', 'args': [node]})

    def is_fully_overridden_member(self, node, name, path):
        """
        Checks if the member is completely overridden in the set of the node.

        :param node: the node to test.
        :type node: dict
        :param name: the name of the set of the node.
        :type name: str
        :param path: the path of the member in question.
        :type path: str
        :returns: Returns true if the member exists in the base of the set, but was\        added to the given set as well, which means a complete override. If the set does not exist\        or the member do not have a 'base' member or just some property was overridden, the function returns\        false.
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isFullyOverriddenMember', 'args': [node, name, path]})

    def is_instance_of(self, node, base_node_or_path):
        """
        Checks if the node is an instance of base.

        :param node: the node in question.
        :type node: dict
        :param base_node_or_path: a potential base node (or its path) of the node
        :type base_node_or_path: dict or str
        :returns: Returns true if the base is on the inheritance chain of node.\        A node is considered to be an instance of itself here.
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isInstanceOf', 'args': [node, base_node_or_path]})

    def is_library_element(self, node):
        """
        Returns true if the node in question is a library element..

        :param node: the node in question.
        :type node: dict
        :returns: Returns true if your node is a library element, false otherwise.
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isLibraryElement', 'args': [node]})

    def is_library_root(self, node):
        """
        Returns true if the node in question is a library root..

        :param node: the node in question.
        :type node: dict
        :returns: Returns true if your node is a library root (even if it is embedded in other library),\        false otherwise.
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isLibraryRoot', 'args': [node]})

    def is_member_of(self, node):
        """
        Returns all membership information of the given node.

        :param node: the node in question
        :type node: dict
        :returns: Returns a dictionary where every the key of every entry is an absolute path of a set owner\        node. The value of each entry is an array with the set names in which the node can be found as a member.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isMemberOf', 'args': [node]})

    def is_meta_node(self, node):
        """
        Checks if the node is a META node.

        :param node: the node to test.
        :type node: dict
        :returns: Returns true if the node is a member of the METAAspectSet of the ROOT node hence can be\        seen as a META node.
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isMetaNode', 'args': [node]})

    def is_type_of(self, node, type_node_or_path):
        """
        Checks if the given node in any way inherits from the typeNode. In addition to checking if the node\        "isInstanceOf" of typeNode, this methods also takes mixins into account.

        :param node: the node in question.
        :type node: dict
        :param type_node_or_path: the type node we want to check or its path.
        :type type_node_or_path: dict or str
        :returns: The function returns true if the typeNodeOrPath represents a base node,\        or a mixin of any of the base nodes, of the node.\        Every node is considered to be a type of itself.
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isTypeOf', 'args': [node, type_node_or_path]})

    def is_valid_aspect_member_of(self, node, parent, name):
        """
        Returns if a node could be contained in the given container's aspect.

        :param node: the node in question.
        :type node: dict
        :param parent: the container node in question.
        :type parent: dict
        :param name: the name of aspect.
        :type name: str
        :returns: The function returns true if the given container could contain the node in the asked aspect.
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isValidAspectMemberOf', 'args': [node, parent, name]})

    def is_valid_attribute_value_of(self, node, name, value):
        """
        Checks if the given value is of the necessary type, according to the META rules.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the attribute.
        :type name: str
        :param value: the value to test.
        :type value: str or int or float or bool or dict
        :returns: Returns true if the value matches the META definitions.
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isValidAttributeValueOf', 'args': [node, name, value]})

    def is_valid_child_of(self, node, parent):
        """
        Checks if according to the META rules the given node can be a child of the parent.

        :param node: the node in question
        :type node: dict
        :param parent: the parent we like to test.
        :type parent: dict
        :returns: The function returns true if according to the META rules the node can be a child of the\        parent. The check does not cover multiplicity (so if the parent can only have twi children and it already\        has them, this function will still returns true).
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isValidChildOf', 'args': [node, parent]})

    def is_valid_new_base(self, node, base):
        """
        Checks if base can be the new base of node.

        :param node: the node in question.
        :type node: dict
        :param base: the new base.
        :type base: dict or None or None
        :returns: True if the supplied base is a valid base for the node.
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isValidNewBase', 'args': [node, base]})

    def is_valid_new_child(self, parent_node, base_node):
        """
        Checks if an instance of the given base can be created under the parent. It does not check for\        meta consistency. It only validates if the proposed creation would cause any loops in the\        combined containment inheritance trees.

        :param parent_node: the parent in question.
        :type parent_node: dict or None
        :param base_node: the intended type of the node.
        :type base_node: dict or None
        :returns: True if a child of the type can be created.
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isValidNewChild', 'args': [parent_node, base_node]})

    def is_valid_new_parent(self, node, parent):
        """
        Checks if parent can be the new parent of node.

        :param node: the node in question.
        :type node: dict
        :param parent: the new parent.
        :type parent: dict
        :returns: True if the supplied parent is a valid parent for the node.
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isValidNewParent', 'args': [node, parent]})

    def is_valid_target_of(self, node, source, name):
        """
        Checks if the node can be a target of a pointer of the source node in accordance with the META rules.

        :param node: the node in question.
        :type node: dict
        :param source: the source to test.
        :type source: dict
        :param name: the name of the pointer.
        :type name: str
        :returns: The function returns true if according to the META rules, the given node is a valid\        target of the given pointer of the source.
        :rtype: bool
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'isValidTargetOf', 'args': [node, source, name]})

    def load_by_path(self, node, relative_path):
        """
        From the given starting node, it loads the path given as a series of relative ids (separated by '/')\        and returns the node it finds at the ends of the path. If there is no node, the function will return null.

        :param node: the starting node of our search.
        :type node: dict
        :param relative_path: the relative path - built by relative ids - of the node in question.
        :type relative_path: str
        :returns: the resulting node
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the result of the execution
        :raises CoreInternalError: the result of the execution
        """
        return self._send({'name': 'loadByPath', 'args': [node, relative_path]})

    def load_child(self, parent, relative_id):
        """
        Loads the child of the given parent pointed by the relative id. Behind the scenes, it means\        that it actually loads the data pointed by a hash stored inside the parent under the given id\        and wraps it in a node object which will be connected to the parent as a child in the containment\        hierarchy. If there is no such relative id reserved, the call will return with null.

        :param parent: the container node in question.
        :type parent: dict
        :param relative_id: the relative id of the child in question.
        :type relative_id: str
        :returns: the resulting child
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the result of the execution
        :raises CoreInternalError: the result of the execution
        """
        return self._send({'name': 'loadChild', 'args': [parent, relative_id]})

    def load_children(self, node):
        """
        Loads all the children of the given parent. As it first checks the already reserved relative ids of\        the parent, it only loads the already existing children (so no on-demand empty node creation).

        :param node: the container node in question.
        :type node: dict
        :returns: the resulting children
        :rtype: list of dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the result of the execution
        :raises CoreInternalError: the result of the execution
        """
        return self._send({'name': 'loadChildren', 'args': [node]})

    def load_collection(self, node, pointer_name):
        """
        Loads all the source nodes that has such a pointer and its target is the given node.

        :param node: the target node in question.
        :type node: dict
        :param pointer_name: the name of the pointer of the sources.
        :type pointer_name: str
        :returns: the resulting sources
        :rtype: list of dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the result of the execution
        :raises CoreInternalError: the result of the execution
        """
        return self._send({'name': 'loadCollection', 'args': [node, pointer_name]})

    def load_instances(self, node):
        """
        Loads all the instances of the given node.

        :param node: the node in question.
        :type node: dict
        :returns: the found instances of the node.
        :rtype: list of dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the status of the execution.
        :raises CoreInternalError: the status of the execution.
        """
        return self._send({'name': 'loadInstances', 'args': [node]})

    def load_members(self, node, set_name):
        """
        Loads all the members of the given set of the node.

        :param node: the node in question.
        :type node: dict
        :param set_name: the name of the set in question.
        :type set_name: str
        :returns: the found members of the set of the node.
        :rtype: list of dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the status of the execution.
        :raises CoreInternalError: the status of the execution.
        """
        return self._send({'name': 'loadMembers', 'args': [node, set_name]})

    def load_own_children(self, node):
        """
        Loads all the children of the given parent that has some data and not just inherited. As it first checks\        the already reserved relative ids of the parent, it only loads the already existing children\        (so no on-demand empty node creation).

        :param node: the container node in question.
        :type node: dict
        :returns: the resulting children
        :rtype: list of dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the result of the execution
        :raises CoreInternalError: the result of the execution
        """
        return self._send({'name': 'loadOwnChildren', 'args': [node]})

    def load_own_members(self, node, set_name):
        """
        Loads all the own members of the given set of the node.

        :param node: the node in question.
        :type node: dict
        :param set_name: the name of the set in question.
        :type set_name: str
        :returns: the found own members of the set of the node.
        :rtype: list of dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the status of the execution.
        :raises CoreInternalError: the status of the execution.
        """
        return self._send({'name': 'loadOwnMembers', 'args': [node, set_name]})

    def load_own_sub_tree(self, node):
        """
        Loads a complete sub-tree of the containment hierarchy starting from the given node, but load only those\        children that has some additional data and not purely inherited.

        :param node: the container node in question.
        :type node: dict
        :returns: the resulting sources
        :rtype: list of dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the result of the execution
        :raises CoreInternalError: the result of the execution
        """
        return self._send({'name': 'loadOwnSubTree', 'args': [node]})

    def load_pointer(self, node, pointer_name):
        """
        Loads the target of the given pointer of the given node. In the callback the node can have three values:\        if the node is valid, then it is the defined target of a valid pointer,\        if the returned value is null, then it means that the pointer is defined, but has no real target,\        finally if the returned value is undefined than there is no such pointer defined for the given node.

        :param node: the source node in question.
        :type node: dict
        :param pointer_name: the name of the pointer.
        :type pointer_name: str
        :returns: the resulting target
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the result of the execution
        :raises CoreInternalError: the result of the execution
        """
        return self._send({'name': 'loadPointer', 'args': [node, pointer_name]})

    def load_root(self, hash):
        """
        Loads the data object with the given hash and makes it a root of a containment hierarchy.

        :param hash: the hash of the data object we like to load as root.
        :type hash: str
        :returns: the resulting root node
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the result of the execution
        :raises CoreInternalError: the result of the execution
        """
        return self._send({'name': 'loadRoot', 'args': [hash]})

    def load_sub_tree(self, node):
        """
        Loads a complete sub-tree of the containment hierarchy starting from the given node.

        :param node: the node that is the root of the sub-tree in question.
        :type node: dict
        :returns: the resulting sources
        :rtype: list of dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the result of the execution
        :raises CoreInternalError: the result of the execution
        """
        return self._send({'name': 'loadSubTree', 'args': [node]})

    def move_aspect_meta_target(self, node, target, old_name, new_name):
        """
        Moves the given target definition over to a new aspect. As actual values in case of\        relation definitions vary quite a bit from the meta-targets, this function does not deals with\        the actual pointer/set target/members.

        :param node: the node in question.
        :type node: dict
        :param target: the target that should be moved among definitions.
        :type target: dict
        :param old_name: the current name of the aspect that has the target.
        :type old_name: str
        :param new_name: the new aspect name where the target should be moved over.
        :type new_name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'moveAspectMetaTarget', 'args': [node, target, old_name, new_name]})

    def move_member(self, node, member_path, old_set_name, new_set_name):
        """
        Moves an own member of the set over to another set of the node.

        :param node: the node in question.
        :type node: dict
        :param member_path: the path of the memberNode that should be moved.
        :type member_path: str
        :param old_set_name: the name of the set where the member is currently reside.
        :type old_set_name: str
        :param new_set_name: the name of the target set where the member should be moved to.
        :type new_set_name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'moveMember', 'args': [node, member_path, old_set_name, new_set_name]})

    def move_node(self, node, parent):
        """
        Moves the given node under the given parent.

        :param node: the node to be moved.
        :type node: dict
        :param parent: the parent node of the copy.
        :type parent: dict
        :returns: The function returns the node after the move.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'moveNode', 'args': [node, parent]})

    def move_pointer_meta_target(self, node, target, old_name, new_name):
        """
        Moves the given target definition over to a new pointer or set.\        Note this does not alter the actual pointer target or set members.

        :param node: the node in question.
        :type node: dict
        :param target: the target that should be moved among definitions.
        :type target: dict
        :param old_name: the current name of the pointer/set definition in question.
        :type old_name: str
        :param new_name: the new name of the relation towards the target.
        :type new_name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'movePointerMetaTarget', 'args': [node, target, old_name, new_name]})

    def persist(self, node):
        """
        Persists the changes made in memory and computed the data blobs that needs to be saved into the database\        to make the change and allow other users to see the new state of the project.

        :param node: some node element of the modified containment hierarchy (usually the root).
        :type node: dict
        :returns: The function returns an object which collects all the changes\        on data level and necessary to update the database on server side. Keys of the returned object are 'rootHash'\        and 'objects'. The values of these should be passed to project.makeCommit.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'persist', 'args': [node]})

    def remove_library(self, node, name):
        """
        Removes a library from your project. It will also remove any remaining instances of the specific library.

        :param node: any node in your project.
        :type node: dict
        :param name: the name of your library.
        :type name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'removeLibrary', 'args': [node, name]})

    def rename_attribute(self, node, old_name, new_name):
        """
        Renames the given attribute of the node if its value is not inherited.

        :param node: the node in question.
        :type node: dict
        :param old_name: the current name of the attribute in question.
        :type old_name: str
        :param new_name: the new name of the attribute.
        :type new_name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'renameAttribute', 'args': [node, old_name, new_name]})

    def rename_attribute_meta(self, node, old_name, new_name):
        """
        Renames the given attribute definition of the node. It also renames the default value of the definition!\        As a result of this operation, all instances of node will have the new attribute, but if they have\        overriden the old attribute it will remain under that name (and become meta invalid).

        :param node: the node in question.
        :type node: dict
        :param old_name: the current name of the attribute definition in question.
        :type old_name: str
        :param new_name: the new name of the attribute.
        :type new_name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'renameAttributeMeta', 'args': [node, old_name, new_name]})

    def rename_library(self, node, old_name, new_name):
        """
        Rename a library in your project.

        :param node: any node in your project.
        :type node: dict
        :param old_name: the current name of the library.
        :type old_name: str
        :param new_name: the new name of the project.
        :type new_name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'renameLibrary', 'args': [node, old_name, new_name]})

    def rename_pointer(self, node, old_name, new_name):
        """
        Renames the given pointer of the node if its target is not inherited.

        :param node: the node in question.
        :type node: dict
        :param old_name: the current name of the pointer in question.
        :type old_name: str
        :param new_name: the new name of the pointer.
        :type new_name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'renamePointer', 'args': [node, old_name, new_name]})

    def rename_registry(self, node, old_name, new_name):
        """
        Renames the given registry of the node if its value is not inherited.

        :param node: the node in question.
        :type node: dict
        :param old_name: the current name of the registry in question.
        :type old_name: str
        :param new_name: the new name of the registry.
        :type new_name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'renameRegistry', 'args': [node, old_name, new_name]})

    def rename_set(self, node, old_name, new_name):
        """
        Renames the given set of the node if its is not inherited.

        :param node: the node in question.
        :type node: dict
        :param old_name: the current name of the set in question.
        :type old_name: str
        :param new_name: the new name of the set.
        :type new_name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'renameSet', 'args': [node, old_name, new_name]})

    def set_aspect_meta_target(self, node, name, target):
        """
        Sets a valid type for the given aspect of the node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the aspect.
        :type name: str
        :param target: the valid type for the aspect.
        :type target: dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'setAspectMetaTarget', 'args': [node, name, target]})

    def set_attribute(self, node, name, value):
        """
        Sets the value of the given attribute of the given node. It defines the attribute on demand, means that it\        will set the given attribute even if was ot defined for the node beforehand.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the attribute.
        :type name: str
        :param value: the new of the attribute, undefined is not allowed.
        :type value: str or int or float or bool or dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'setAttribute', 'args': [node, name, value]})

    def set_attribute_meta(self, node, name, rule):
        """
        Sets the META rules of the attribute of the node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the attribute.
        :type name: str
        :param rule: the rules that defines the attribute
        :type rule: dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'setAttributeMeta', 'args': [node, name, rule]})

    def set_base(self, node, base):
        """
        Sets the base node of the given node. The function doesn't touches the properties or the children of the node\        so it can cause META rule violations that needs to be corrected manually.

        :param node: the node in question.
        :type node: dict
        :param base: the new base.
        :type base: dict or None
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'setBase', 'args': [node, base]})

    def set_child_meta(self, node, child, min=None, max=None):
        """
        Sets the given child as a valid children type for the node.

        :param node: the node in question.
        :type node: dict
        :param child: the valid child node.
        :type child: dict
        :param min: the allowed minimum number of children from this given node type (if not given or\        -1 is set, then there will be no minimum rule according this child type)
        :type min: int
        :param max: the allowed maximum number of children from this given node type (if not given or\        -1 is set, then there will be no minimum rule according this child type)
        :type max: int
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'setChildMeta', 'args': [node, child, min, max]})

    def set_children_meta_limits(self, node, min=None, max=None):
        """
        Sets the global containment limits for the node.

        :param node: the node in question.
        :type node: dict
        :param min: the allowed minimum number of children (if not given or\        -1 is set, then there will be no minimum rule according children)
        :type min: int
        :param max: the allowed maximum number of children (if not given or\        -1 is set, then there will be no maximum rule according children)
        :type max: int
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'setChildrenMetaLimits', 'args': [node, min, max]})

    def set_constraint(self, node, name, constraint):
        """
        Sets a constraint object of the node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the constraint.
        :type name: str
        :param constraint: the constraint to be set.
        :type constraint: dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'setConstraint', 'args': [node, name, constraint]})

    def set_guid(self, node, guid):
        """
        Set the GUID of a node. As the Core itself do not checks whether the GUID already exists. The use of\        this function is only advised during the creation of the node.

        :param node: the node in question.
        :type node: dict
        :param guid: the new globally unique identifier.
        :type guid: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the result of the execution.
        :raises CoreIllegalOperationError: the result of the execution.
        :raises CoreInternalError: the result of the execution.
        """
        return self._send({'name': 'setGuid', 'args': [node, guid]})

    def set_member_attribute(self, node, set_name, path, attr_name, value):
        """
        Sets the attribute value which represents a property of the membership.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param path: the absolute path of the member node.
        :type path: str
        :param attr_name: the name of the attribute.
        :type attr_name: str
        :param value: the new value of the attribute.
        :type value: str or int or float or bool or dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'setMemberAttribute', 'args': [node, set_name, path, attr_name, value]})

    def set_member_registry(self, node, set_name, path, reg_name, value):
        """
        Sets the registry entry value which represents a property of the membership.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param path: the absolute path of the member node.
        :type path: str
        :param reg_name: the name of the registry entry.
        :type reg_name: str
        :param value: the new value of the registry.
        :type value: str or int or float or bool or dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'setMemberRegistry', 'args': [node, set_name, path, reg_name, value]})

    def set_pointer(self, node, name, target):
        """
        Sets the target of the pointer of the node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the pointer in question.
        :type name: str
        :param target: the new target of the pointer.
        :type target: dict or None
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'setPointer', 'args': [node, name, target]})

    def set_pointer_meta_limits(self, node, name, min=None, max=None):
        """
        Sets the global target limits for pointer/set of the node. On META level the only distinction between\        pointer and sets is the global multiplicity which has to maximize the number of possible targets to 1 in\        case of 'pure' pointer definitions.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the pointer/set.
        :type name: str
        :param min: the allowed minimum number of children (if not given or\        -1 is set, then there will be no minimum rule according targets)
        :type min: int
        :param max: the allowed maximum number of children (if not given or\        -1 is set, then there will be no maximum rule according targets)
        :type max: int
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'setPointerMetaLimits', 'args': [node, name, min, max]})

    def set_pointer_meta_target(self, node, name, target, min=None, max=None):
        """
        Sets the given target as a valid target type for the pointer/set of the node.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the pointer/set.
        :type name: str
        :param target: the valid target/member node.
        :type target: dict
        :param min: the allowed minimum number of target/member from this given node type (if not\        given or -1 is set, then there will be no minimum rule according this target type)
        :type min: int
        :param max: the allowed maximum number of target/member from this given node type (if not\        given or -1 is set, then there will be no minimum rule according this target type)
        :type max: int
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'setPointerMetaTarget', 'args': [node, name, target, min, max]})

    def set_registry(self, node, name, value):
        """
        Sets the value of the given registry entry of the given node. It defines the registry entry on demand,\        means that it will set the given registry entry even if was ot defined for the node beforehand.

        :param node: the node in question.
        :type node: dict
        :param name: the name of the registry entry.
        :type name: str
        :param value: the new of the registry entry. Can be any primitive\        type or object. Undefined is not allowed.
        :type value: str or int or float or bool or dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'setRegistry', 'args': [node, name, value]})

    def set_set_attribute(self, node, set_name, attr_name, value):
        """
        Sets the attribute entry value for the set at the node.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param attr_name: the name of the attribute entry.
        :type attr_name: str
        :param value: the new value of the attribute.
        :type value: str or int or float or bool or dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'setSetAttribute', 'args': [node, set_name, attr_name, value]})

    def set_set_registry(self, node, set_name, reg_name, value):
        """
        Sets the registry entry value for the set at the node.

        :param node: the owner of the set.
        :type node: dict
        :param set_name: the name of the set.
        :type set_name: str
        :param reg_name: the name of the registry entry.
        :type reg_name: str
        :param value: the new value of the registry.
        :type value: str or int or float or bool or dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'setSetRegistry', 'args': [node, set_name, reg_name, value]})

    def try_to_concat_changes(self, mine, theirs):
        """
        Tries to merge two patch object. The patches ideally represents changes made by two parties. They represents\        changes from the same source ending in different states. Our aim is to generate a single patch that could\        cover the changes of both party.

        :param mine: the tree structured JSON patch that represents my changes.
        :type mine: dict
        :param theirs: the tree structured JSON patch that represents the changes of the other party.
        :type theirs: dict
        :returns: The function returns with an object that contains the conflicts (if any) and the merged\        patch.
        :rtype: dict
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        """
        return self._send({'name': 'tryToConcatChanges', 'args': [mine, theirs]})

    def update_library(self, node, name, library_root_hash, library_info=None):
        """
        It updates a library in your project based on the input information. It will 'reaplace' the old\        version, keeping as much information as possible regarding the instances.

        :param node: any regular node in your project.
        :type node: dict
        :param name: the name of the library you want to update.
        :type name: str
        :param library_root_hash: the hash of your library's new root\        (must exist in the project's collection at the time of call).
        :type library_root_hash: str
        :param library_info: information about your project.
        :type library_info: dict
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises JSError: the status of the execution.
        :raises CoreIllegalOperationError: the status of the execution.
        :raises CoreInternalError: the status of the execution.
        """
        return self._send({'name': 'updateLibrary', 'args': [node, name, library_root_hash, library_info]})
