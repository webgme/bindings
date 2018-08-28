"""
For more details regarding inputs and output in form of complex dictionaries see the original source docs at:

%host%/docs/source/ProjectInterface.html

for example:

`https://editor.webgme.org/docs/source/ProjectInterface.html <https://editor.webgme.org/docs/source/ProjectInterface.html>`_
"""


class Project(object):
    """
    Class for accessing and making changes in a project repository.
    """

    def __init__(self, webgme):
        self._webgme = webgme
        self._CONSTANTS = None

    def _send(self, payload):
        payload['type'] = 'project'
        self._webgme.send_request(payload)
        return self._webgme.handle_response()

    @property
    def CONSTANTS(self):
        """
        A dictionary with the `constants associated with the storage/project <https://github.com/webgme/webgme-engine/blob/master/src/common/storage/constants.js>`_.
        """
        if self._CONSTANTS is None:
            self._CONSTANTS = self._send({'name': 'CONSTANTS', 'args': []})

        return self._CONSTANTS

    def create_branch(self, branch_name, new_hash):
        """
        Creates a new branch with head pointing to the provided commit hash.

        :param branch_name: Name of branch to create.
        :type branch_name: str
        :param new_hash: New commit hash for branch head.
        :type new_hash: str
        :returns: Status about the branch update.
        :rtype: dict
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'createBranch', 'args': [branch_name, new_hash]})

    def create_tag(self, tag_name, commit_hash):
        """
        Creates a new tag pointing to the provided commit hash.

        :param tag_name: Name of tag to create.
        :type tag_name: str
        :param commit_hash: Commit hash tag will point to.
        :type commit_hash: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'createTag', 'args': [tag_name, commit_hash]})

    def delete_branch(self, branch_name, old_hash):
        """
        Deletes the branch.

        :param branch_name: Name of branch to create.
        :type branch_name: str
        :param old_hash: Previous commit hash for branch head.
        :type old_hash: str
        :returns: Status about the branch update.
        :rtype: dict
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'deleteBranch', 'args': [branch_name, old_hash]})

    def delete_tag(self, tag_name):
        """
        Deletes the given tag.

        :param tag_name: Name of tag to delete.
        :type tag_name: str
        :returns: Nothing is returned by the function.
        :rtype: None
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'deleteTag', 'args': [tag_name]})

    def get_branch_hash(self, branch_name):
        """
        Retrieves the commit hash for the head of the branch.

        :param branch_name: Name of branch.
        :type branch_name: str
        :returns: The commit hash.
        :rtype: str
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'getBranchHash', 'args': [branch_name]})

    def get_branches(self):
        """
        Retrieves all branches and their current heads within the project.

        :returns: An object with branch names as keys\        and their commit-hashes as values.
        :rtype: dict
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'getBranches', 'args': []})

    def get_commit_object(self, branch_name_or_commit_hash):
        """
        Retrieves the commit-object at the provided branch or commit-hash.

        :param branch_name_or_commit_hash: Name of branch or a commit-hash.
        :type branch_name_or_commit_hash: str
        :returns: The commit-object.
        :rtype: dict
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'getCommitObject', 'args': [branch_name_or_commit_hash]})

    def get_commits(self, before, number):
        """
        Retrieves and array of the latest (sorted by timestamp) commits for the project.\        If timestamp is given it will get <b>number</b> of commits strictly before <b>before</b>.\        If commit hash is specified that commit will be included too.\        <br> N.B. due to slight time differences on different machines, ancestors may be returned before\        their descendants. Unless looking for 'headless' commits 'getHistory' is the preferred method.

        :param before: Timestamp or commitHash to load history from.
        :type before: int or float or str
        :param number: Number of commits to load.
        :type number: int or float
        :returns: The commits that match the input, ordered\        by their time of insertion.
        :rtype: list of dict
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'getCommits', 'args': [before, number]})

    def get_common_ancestor_commit(self, commit_a, commit_b):
        """
        Retrieves the common ancestor of two commits. If no ancestor exists it will result in an error.

        :param commit_a: Commit hash.
        :type commit_a: str
        :param commit_b: Commit hash.
        :type commit_b: str
        :returns: The commit hash of the common ancestor.
        :rtype: str
        :raises JSError: The result of the execution (will be non-null if e.g. the commits do not exist or have no common ancestor).
        """
        return self._send({'name': 'getCommonAncestorCommit', 'args': [commit_a, commit_b]})

    def get_history(self, start, number):
        """
        Retrieves an array of commits starting from a branch(es) and/or commitHash(es).\        <br> The result is ordered by the rules (applied in order)\        <br> 1. Descendants are always returned before their ancestors.\        <br> 2. By their timestamp.

        :param start: Branch name,\        commit hash or array of these.
        :type start: str or str or list of str or list of str
        :param number: Number of commits to load.
        :type number: int or float
        :returns: The commits that match the input ordered\        as explained.
        :rtype: list of dict
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'getHistory', 'args': [start, number]})

    def get_project_info(self):
        """
        Retrieves the metadata of the project.

        :returns: An object with info about the project.
        :rtype: dict
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'getProjectInfo', 'args': []})

    def get_root_hash(self, branch_name_or_commit_hash):
        """
        Retrieves the root hash at the provided branch or commit-hash.

        :param branch_name_or_commit_hash: Name of branch or a commit-hash.
        :type branch_name_or_commit_hash: str
        :returns: The root hash.
        :rtype: str
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'getRootHash', 'args': [branch_name_or_commit_hash]})

    def get_tags(self):
        """
        Retrieves all tags and their commits hashes within the project.

        :returns: An object with tag names as keys and\        their commit-hashes as values.
        :rtype: dict
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'getTags', 'args': []})

    def get_user_id(self):
        """
        Return the identity of the current user of this project.

        :returns: the userId
        :rtype: str
        """
        return self._send({'name': 'getUserId', 'args': []})

    def make_commit(self, branch_name, parents, root_hash, core_objects, msg):
        """
        Makes a commit to data base. Based on the root hash and commit message a new\        {@link module:Storage.CommitObject} (with returned hash)\        is generated and insert together with the core objects to the database on the server.

        :param branch_name: Name of branch to update (none if null).
        :type branch_name: str
        :param parents: Parent commit hashes.
        :type parents: list of str
        :param root_hash: Hash of root object.
        :type root_hash: str
        :param core_objects: Core objects associated with the commit.
        :type core_objects: dict
        :param msg: Commit message.
        :type msg: str
        :returns: Status about the commit and branch update.
        :rtype: dict
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'makeCommit', 'args': [branch_name, parents, root_hash, core_objects, msg]})

    def set_branch_hash(self, branch_name, new_hash, old_hash):
        """
        Updates the head of the branch.

        :param branch_name: Name of branch to update.
        :type branch_name: str
        :param new_hash: New commit hash for branch head.
        :type new_hash: str
        :param old_hash: Current state of the branch head inside the database.
        :type old_hash: str
        :returns: Status about the branch update.
        :rtype: dict
        :raises JSError: The result of the execution.
        """
        return self._send({'name': 'setBranchHash', 'args': [branch_name, new_hash, old_hash]})
