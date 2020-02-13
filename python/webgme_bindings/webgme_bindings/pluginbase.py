from .webgme import WebGME
from .exceptions import JSError, CoreIllegalArgumentError, CoreIllegalOperationError, CoreInternalError


class PluginBase(object):
    """
    This is the base-class for webgme-plugins in Python. Use `webgme-cli <https://github.com/webgme/webgme-cli>`_ \
    for generating the boiler-plate code for a python-plugin.
    """
    def __init__(self, webgme, commit_hash, branch_name=None, active_node='', active_selection=None, nsp=''):
        """

        :param webgme: An instance of an already connected WebGME class
        :type webgme: WebGME
        :param commit_hash: The commit-hash of the current invocation
        :type commit_hash: str
        :param branch_name: The branch of the current invocation
        :type branch_name: str or None
        :param active_node: Path to the active-node of the current invocation
        :type active_node: str
        :param active_selection: List of paths to the active-selection of the current invocation
        :type active_selection: list of str or None
        :param nsp: The namespace the plugin is running under
        :type nsp: str
        """
        self._webgme = webgme

        #: Instance of logger (regular python logger)
        self.logger = webgme.logger

        #: An instance of webgme_bindings.Core
        self.core = webgme.core

        #: An instance of webgme_bindings.Project
        self.project = webgme.project

        #: An instance of webgme_bindings.Util
        self.util = webgme.util

        self._META = None

        #: The current commit-hash (str)
        self.commit_hash = commit_hash

        #: The current branch (str or None)
        self.branch_name = branch_name

        #: The namespace the plugin is running under (str)
        self.namespace = nsp
        root_hash = self.project.get_root_hash(commit_hash)

        #: The root-node of the current invocation (dict)
        self.root_node = self.core.load_root(root_hash)

        #: The active-node of the current invocation (dict)
        self.active_node = self.core.load_by_path(self.root_node, active_node)

        #: The active-selection nodes of the current invocation (list of dict)
        self.active_selection = []

        if active_selection is not None:
            for as_path in active_selection:
                self.active_selection.append(self.core.load_by_path(self.root_node, as_path))

    def main(self):
        """
        Main invocation point for a plugin. This must be implemented in the derived classes.
        """
        raise NotImplementedError('plugin.main must be implemented in derived class!')

    @property
    def gme_config(self):
        """
        A nested dictionary with `configuration parameters for webgme <https://github.com/webgme/webgme/tree/master/config>`_.
        """
        return self.util.gme_config

    @property
    def META(self):
        """
        Dictionary from name of meta-node to node dict.
        """
        if self._META is None:
            self._META = self.util.META(self.root_node, self.namespace)

        return self._META

    def _send(self, payload):
        payload['type'] = 'plugin'
        self._webgme.send_request(payload)
        return self._webgme.handle_response()

    def add_artifact(self, name, files):
        """
        Adds multiple files to the blob storage and bundles them as an artifact of which the hash is added to the\
        plugin-result.

        :param name: name of the file bundle.
        :type name: str
        :param files: Keys are file names and values the content (as strings).
        :type files: dict
        :returns: The metadata-hash (the "id") of the uploaded artifact.
        :rtype: str
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'addArtifact', 'args': [name, files]})

    def add_file(self, name, content):
        """
        Adds a file to the blob storage and adds it to the plugin-result.

        :param name: The name the file should be uploaded as.
        :type name: str
        :param content: The file content.
        :type content: str
        :returns: The metadata-hash (the "id") of the uploaded file.
        :rtype: str
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'addFile', 'args': [name, content]})

    def create_message(self, node, message, severity='info'):
        """
        Creates a new message for the user and adds it to the result.

        :param node: The node related to the message.
        :type node: dict
        :param message: The feedback to the user.
        :type message: str
        :param severity: Severity level of the message: 'debug', 'info' (default), 'warning', 'error'.
        :type severity: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises CoreIllegalArgumentError: If some of the parameters don't match the input criteria.
        :raises CoreIllegalOperationError: If the context of the operation is not allowed.
        :raises CoreInternalError: If some internal error took place inside the core layers.
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'createMessage', 'args': [node, message, severity]})

    def get_artifact(self, metadata_hash):
        """
        Retrieves all the files in the artifact from the blob storage.

        :param metadata_hash: the "id" of the artifact to retrieve.
        :type metadata_hash: str
        :returns: Keys are file names, and values the file content (as strings).
        :rtype: dict
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'getArtifact', 'args': [metadata_hash]})

    def get_file(self, metadata_hash):
        """
        Retrieves the file from blob storage.

        :param metadata_hash: the "id" of the file to retrieve.
        :type metadata_hash: str
        :returns: The file content.
        :rtype: str
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'getFile', 'args': [metadata_hash]})

    def get_current_config(self):
        """
        Gets the current configuration of the plugin that was set by the user and plugin manager.

        :returns: A dictionary with the plugin config for the current execution.
        :rtype: dict
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'getCurrentConfig', 'args': []})

    def send_notification(self, message):
        """
        Sends a notification back to the invoker of the plugin, can be used to notify about progress.\
        Message can either be a string or a dictionary with keys, 'message', 'progress', 'severity'\
        and 'toBranch'. If an object is passed 'message' must be provided - all other are optional.\
        'progress' - Approximate progress (in %) of the plugin at time of sending.\
        'severity' - Severity level ('success', 'info', 'warn', 'error')\
        'toBranch' - If true, and the plugin is running on the server on a branch the notification will be\
        broadcast to all sockets in the branch room.

        :param message: Message string or object containing message.
        :type message: str or dict
        :returns: A dictionary with the plugin config for the current execution.
        :rtype: dict
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'sendNotification', 'args': [message]})

    def result_set_success(self, success):
        """
        Sets the the result value of the execution of the plugin. In python, if the plugin exits with 0,\
        the value will be true.
        
        :param success: The value to be set for the success of the plugin.
        :type success: bool
        :returns: Nothing is returned by the function.
        :rtype: None
        """
        return self._send({'name':'resultSetSuccess', 'args':[success]})

    def result_set_error(self, message):
        """
        Sets the error reason for the failure of the plugin. Should be used together with result_set_success\
        as in case of successfull execution, this message is ignored. Also, only the first message will be visible\
        for the user.
        
        :param message: Textual description of the cause of the failure.
        :type message: str
        :returns: Nothing is returned by the function.
        :rtype: None
        """
        return self._send({'name':'resultSetError', 'args':[message]})
