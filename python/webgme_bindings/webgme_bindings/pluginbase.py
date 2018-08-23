from .webgme import WebGME
from .exceptions import JSError, CoreIllegalArgumentError, CoreIllegalOperationError, CoreInternalError


class PluginBase(object):
    def __init__(self, webgme, commit_hash, branch_name=None, active_node='', active_selection=None, nsp=''):
        """

        :param webgme: An instance of an already connected WebGME class
        :type webgme: WebGME
        """
        self._webgme = webgme
        self.logger = webgme.logger
        self.core = webgme.core
        self.project = webgme.project
        self.util = webgme.util
        self._META = None

        self.commit_hash = commit_hash
        self.branch_name = branch_name
        self.namespace = nsp
        root_hash = self.project.get_root_hash(commit_hash)
        self.root_node = self.core.load_root(root_hash)
        self.active_node = self.core.load_by_path(self.root_node, active_node)
        self.active_selection = []

        if active_selection is not None:
            for as_path in active_selection:
                self.active_selection.append(self.core.load_by_path(self.root_node, as_path))

    def main(self):
        raise NotImplementedError('plugin.main must be implemented in derived class!')

    @property
    def gme_config(self):
        return self.util.gme_config

    @property
    def META(self):
        if self._META is None:
            self._META = self.util.META(self.root_node, self.namespace)

        return self._META

    def _send(self, payload):
        payload['type'] = 'plugin'
        self._webgme.send_request(payload)
        return self._webgme.handle_response()

    def add_artifact(self, name, files):
        """
        Adds multiple files to the blob storage and bundles them as an artifact of which the hash is added to the
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
        Sends a notification back to the invoker of the plugin, can be used to notify about progress.
        Message can either be a string or a dictionary with keys, 'message', 'progress', 'severity'
        and 'toBranch'. If an object is passed 'message' must be provided - all other are optional.
        'progress' - Approximate progress (in %) of the plugin at time of sending.
        'severity' - Severity level ('success', 'info', 'warn', 'error')
        'toBranch' - If true, and the plugin is running on the server on a branch the notification will be
        broadcast to all sockets in the branch room.

        :param message: Message string or object containing message.
        :type message: str or dict
        :returns: A dictionary with the plugin config for the current execution.
        :rtype: dict
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'sendNotification', 'args': [message]})
