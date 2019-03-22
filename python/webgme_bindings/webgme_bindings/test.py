"""
To run with coverage first:
    pip install coverage

Then from <rootDir>/python/webgme_bindings:

coverage run -m unittest discover -s <rootDir>/python/webgme_bindings/webgme_bindings -p test.py -t <rootDir>/python/webgme_bindings
coverage html

coverage run -m unittest discover -s C:/Users/patrik85/GIT/webgme-core-bindings/python/webgme_bindings/webgme_bindings -p test.py -t C:/Users/patrik85/GIT/webgme-core-bindings/python/webgme_bindings
"""

import unittest
import os
import signal
import subprocess
import time
import logging
from .webgme import WebGME
from .exceptions import JSError, CoreIllegalArgumentError, CoreIllegalOperationError
from .pluginbase import PluginBase

logger = logging.getLogger('test-logger')
logger.setLevel(logging.ERROR)

# Stuff needed for calling webgme from nodejs
WEBGME_IMPORT_BIN = 'node_modules/webgme-engine/src/bin/import.js'
SEED_FILE = 'node_modules/webgme-engine/seeds/EmptyProject.webgmex'
TEST_PROJECT = 'PythonTestProject'
PORT = '5555'
dir_path = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.join(dir_path, '..', '..', '..')
my_env = os.environ.copy()
my_env['NODE_ENV'] = 'test'
COREZMQ_SERVER_FILE = os.path.join(root_dir, 'bin', 'corezmq_server.js')


def node_dict_sort(n_dict):
    return n_dict['nodePath']


class ConnectedTestClass(unittest.TestCase):
    def setUp(self):
        if 'DO_NOT_START_SERVER' in my_env:
            self.node_process = None
        else:
            self.node_process = subprocess.Popen(['node', COREZMQ_SERVER_FILE, TEST_PROJECT, '-p', PORT],
                                                 env=my_env, cwd=root_dir)
        self.webgme = WebGME(PORT, logger)
        self.project = self.webgme.project
        self.core = self.webgme.core
        self.util = self.webgme.util

    def tearDown(self):
        self.webgme.disconnect()
        if self.node_process is not None:
            self.node_process.send_signal(signal.SIGTERM)


# class ProjectTests(object):
class ProjectTests(ConnectedTestClass):
    def test_constants(self):
        const = self.project.CONSTANTS
        self.assertTrue(const['COMMIT_TYPE'] == 'commit')
        const2 = self.project.CONSTANTS
        self.assertTrue(const is const2)  # Referencing the same object

    def test_metadata_related(self):
        self.assertEqual(self.project.get_user_id(), 'guest')
        p_info = self.project.get_project_info()
        self.assertEqual(p_info['owner'], 'guest')
        self.assertEqual(p_info['_id'], 'guest+{0}'.format(TEST_PROJECT))
        self.assertTrue('info' in p_info)
        self.assertTrue('branches' in p_info)
        self.assertTrue('rights' in p_info)
        self.assertTrue('hooks' in p_info)

    def test_commit_related(self):
        branch_hash = self.project.get_branch_hash('master')
        root_hash = self.project.get_root_hash('master')
        commit_obj = self.project.get_commit_object('master')

        self.assertTrue('_id' in commit_obj)
        self.assertTrue('time' in commit_obj)
        self.assertTrue('updater' in commit_obj)
        self.assertTrue('parents' in commit_obj)
        self.assertTrue('message' in commit_obj)

        self.assertEqual(commit_obj['_id'], branch_hash)
        self.assertEqual(commit_obj['root'], root_hash)

        c_res1 = self.project.make_commit(None, [branch_hash], root_hash, {}, 'commit1')
        c_res2 = self.project.make_commit(None, [branch_hash], root_hash, {}, 'commit2')

        common = self.project.get_common_ancestor_commit(c_res1['hash'], c_res2['hash'])
        self.assertEqual(common, branch_hash)

        hist = self.project.get_history(c_res1['hash'], 100)
        self.assertEqual(len(hist), 2)

        time_ms = int(time.time() * 1000)
        hist = self.project.get_commits(time_ms, 100)
        self.assertTrue(len(hist) > 2)

        hist = self.project.get_history([c_res1['hash'], c_res2['hash']], 100)
        self.assertEqual(len(hist), 3)

    def test_branch_related(self):
        init_branches = self.project.get_branches()
        self.assertEqual(len(init_branches.keys()), 1)
        self.assertEqual(list(init_branches.keys())[0], 'master')

        branch_hash = self.project.get_branch_hash('master')
        self.assertEqual(init_branches['master'], branch_hash)

        self.project.create_branch('new_branch', branch_hash)
        res = self.project.create_branch('new_branch2', branch_hash)
        self.assertEqual(res['hash'], branch_hash)
        self.assertEqual(len(self.project.get_branches().keys()), 3)

        root_hash = self.project.get_root_hash('new_branch')
        res = self.project.make_commit('new_branch', [branch_hash], root_hash, {}, 'Test commit')

        self.project.set_branch_hash('new_branch2', res['hash'], branch_hash)

        self.assertDictEqual(self.project.get_branches(), {'new_branch': res['hash'],
                                                           'new_branch2': res['hash'],
                                                           'master': branch_hash,
                                                           })

        self.project.delete_branch('new_branch', branch_hash)
        res = self.project.delete_branch('new_branch2', branch_hash)
        self.assertEqual(res['hash'], '')
        self.assertEqual(len(self.project.get_branches().keys()), 1)

    def test_tag_related(self):
        init_tags = self.project.get_tags()
        self.assertEqual(len(init_tags.keys()), 0)

        branch_hash = self.project.get_branch_hash('master')
        self.project.create_tag('tage', branch_hash)
        self.project.create_tag('tage2', branch_hash)

        self.assertDictEqual(self.project.get_tags(), {'tage': branch_hash,
                                                       'tage2': branch_hash,
                                                       })

        self.project.delete_tag('tage')
        self.project.delete_tag('tage2')

        self.assertDictEqual(self.project.get_tags(), {})

    def test_exceptions(self):
        # All should throw JSError
        self.assertRaises(JSError, self.project.create_branch, 1, 1)
        self.assertRaises(JSError, self.project.create_tag, 1, 1)
        self.assertRaises(JSError, self.project.delete_branch, 1, 1)
        self.assertRaises(JSError, self.project.delete_tag, 1)
        self.assertRaises(JSError, self.project.get_branch_hash, 1)
        # self.assertRaises(JSError, self.project.get_branches)
        self.assertRaises(JSError, self.project.get_commit_object, 1)
        self.assertRaises(JSError, self.project.get_commits, 'Herro', 1)
        self.assertRaises(JSError, self.project.get_common_ancestor_commit, 1, 1)
        self.assertRaises(JSError, self.project.get_history, 1, 1)
        # self.assertRaises(JSError, self.project.get_project_info)
        self.assertRaises(JSError, self.project.get_root_hash, 1)
        # self.assertRaises(JSError, self.project.get_tags)
        # self.assertRaises(JSError, self.project.get_user_id)
        self.assertRaises(JSError, self.project.make_commit, 1, 1, 1, 1, 1)
        self.assertRaises(JSError, self.project.set_branch_hash, 1, 1, 1)


# class CoreTests(object):
class CoreTests(ConnectedTestClass):
    def equal(self, node1, node2):
        return self.util.equal(node1, node2)

    def setUp(self):
        super(CoreTests, self).setUp()
        root_hash = self.project.get_root_hash('master')
        self.root = self.core.load_root(root_hash)
        self.fco = self.core.get_fco(self.root)

        self.child = self.core.create_child(self.root, self.fco)
        self.core.set_attribute(self.child, 'name', 'child')

        self.child2 = self.core.create_child(self.root, self.fco)
        self.core.set_attribute(self.child2, 'name', 'child2')
        self.child_instance = self.core.create_child(self.root, self.child)
        self.core.set_attribute(self.child_instance, 'name', 'child_instance')

    def tearDown(self):
        self.util.unload_root(self.root)
        super(CoreTests, self).tearDown()

    # @unittest.skip("Temp")
    def test_constants(self):
        const = self.core.CONSTANTS
        self.assertTrue(const['META_SET_NAME'] == 'MetaAspectSet')
        const2 = self.core.CONSTANTS
        self.assertTrue(const is const2)  # Referencing the same object

    # @unittest.skip("Temp")
    def test_load_by_path(self):
        node = self.core.load_by_path(self.root, self.core.get_path(self.child))
        self.assertTrue(self.equal(node, self.child))

    # @unittest.skip("Temp")
    def test_basic_properties(self):
        self.core.set_attribute(self.child, 'intAttr', 1)
        self.core.set_attribute(self.child, 'floatAttr', 1.1)
        self.core.set_attribute(self.child, 'boolAttr', True)
        self.core.set_attribute(self.child_instance, 'boolAttr', False)

        self.core.set_registry(self.child, 'intReg', 1)
        self.core.set_registry(self.child, 'floatReg', 1.1)
        self.core.set_registry(self.child, 'boolReg', True)
        self.core.set_registry(self.child_instance, 'boolReg', False)

        # General properties
        relid = self.core.get_relid(self.child)
        self.assertEqual(self.core.get_path(self.child), '/{0}'.format(relid))
        self.assertEqual(len(self.core.get_guid(self.child)), 36)
        self.assertEqual(len(self.core.get_hash(self.fco)), 41)
        self.assertFalse(self.core.is_abstract(self.child))
        self.assertFalse(self.core.is_connection(self.child))

        # Attributes
        self.assertEqual(self.core.get_attribute(self.child, 'name'), 'child')
        self.assertEqual(self.core.get_attribute(self.child_instance, 'intAttr'), 1)
        self.assertEqual(self.core.get_attribute(self.child_instance, 'floatAttr'), 1.1)
        self.assertEqual(self.core.get_attribute(self.child_instance, 'boolAttr'), False)

        self.assertEqual(self.core.get_own_attribute(self.child_instance, 'intAttr'), None)

        attrs = self.core.get_attribute_names(self.child_instance)
        own_attrs = self.core.get_own_attribute_names(self.child_instance)
        valid_attrs = self.core.get_valid_attribute_names(self.child_instance)
        own_valid_attrs = self.core.get_own_valid_attribute_names(self.child_instance)

        self.assertEqual(len(attrs), 4)
        self.assertEqual(len(own_attrs), 2)
        self.assertEqual(len(valid_attrs), 1)
        self.assertEqual(len(own_valid_attrs), 0)

        self.core.del_attribute(self.child_instance, 'boolAttr')
        self.assertEqual(len(self.core.get_own_attribute_names(self.child_instance)), 1)

        self.core.rename_attribute(self.child, 'intAttr', 'intAttrNew')
        self.assertEqual(self.core.get_attribute(self.child_instance, 'intAttrNew'), 1)
        self.assertEqual(self.core.get_registry(self.child_instance, 'intAttr'), None)

        # Registry
        self.assertEqual(self.core.get_registry(self.child_instance, 'intReg'), 1)
        self.assertEqual(self.core.get_registry(self.child_instance, 'floatReg'), 1.1)
        self.assertEqual(self.core.get_registry(self.child_instance, 'boolReg'), False)

        self.assertEqual(self.core.get_own_registry(self.child_instance, 'intReg'), None)

        regs = self.core.get_registry_names(self.child_instance)
        own_regs = self.core.get_own_registry_names(self.child_instance)

        self.assertEqual(len(regs), 5)
        self.assertEqual(len(own_regs), 1)

        self.core.del_registry(self.child_instance, 'boolReg')
        self.assertEqual(len(self.core.get_own_registry_names(self.child_instance)), 0)

        self.core.rename_registry(self.child, 'intReg', 'intRegNew')
        self.assertEqual(self.core.get_registry(self.child_instance, 'intRegNew'), 1)
        self.assertEqual(self.core.get_registry(self.child_instance, 'intReg'), None)

    # @unittest.skip("Temp")
    def test_node_creation_deletion(self):
        self.assertEqual(len(self.core.load_children(self.child_instance)), 0)
        new_child = self.core.create_child(self.child_instance, self.fco)
        self.assertEqual(len(self.core.load_children(self.child_instance)), 1)
        new_child2 = self.core.copy_node(new_child, self.child_instance)
        self.assertEqual(len(self.core.load_children(self.child_instance)), 2)
        new_child3 = self.core.create_node({'parent': self.child_instance, 'base': self.fco})
        self.assertEqual(len(self.core.load_children(self.child_instance)), 3)
        new_children = self.core.copy_nodes([new_child, new_child2], self.child_instance)
        self.assertEqual(len(self.core.load_children(self.child_instance)), 5)

        self.core.delete_node(new_child)
        self.core.delete_node(new_child2)
        self.core.delete_node(new_child3)

        self.assertEqual(len(self.core.load_children(self.child_instance)), 2)

        self.core.move_node(new_children[0], self.child2)
        self.core.move_node(new_children[1], self.child2)
        self.assertEqual(len(self.core.load_children(self.child_instance)), 0)
        self.assertEqual(len(self.core.load_children(self.child2)), 2)

    # @unittest.skip("Temp")
    def test_child_parent_related(self):
        self.assertEqual(self.core.get_parent(self.root), None)
        self.assertTrue(self.equal(self.core.get_root(self.fco), self.root))

        children = self.core.load_children(self.root)
        own_children = self.core.load_own_children(self.root)
        child_paths = self.core.get_children_paths(self.root)
        own_child_paths = self.core.get_own_children_paths(self.root)
        child_relids = self.core.get_children_relids(self.root)
        own_child_relids = self.core.get_own_children_relids(self.root)
        tree_nodes = self.core.load_sub_tree(self.root)
        own_tree_nodes = self.core.load_own_sub_tree(self.root)

        self.assertEqual(len(children), 4)
        self.assertEqual(len(children), len(child_paths))
        self.assertEqual(len(children), len(child_relids))
        self.assertEqual(len(children), len(tree_nodes) - 1)  # root included in tree
        children.sort(key=node_dict_sort)
        own_children.sort(key=node_dict_sort)
        child_paths.sort()
        own_child_paths.sort()
        child_relids.sort()
        own_child_relids.sort()
        tree_nodes.sort(key=node_dict_sort)
        own_tree_nodes.sort(key=node_dict_sort)
        self.assertEqual(children, own_children)
        self.assertEqual(own_child_paths, child_paths)
        self.assertEqual(own_child_relids, child_relids)
        self.assertEqual(tree_nodes, own_tree_nodes)

        name_to_child = {}
        for child in children:
            rel_id = self.core.get_relid(child)
            self.assertTrue(self.util.equal(self.core.load_child(self.root, rel_id), child))
            name_to_child[self.core.get_attribute(child, 'name')] = child
            self.assertTrue(self.util.equal(self.core.get_parent(child), self.root))
            def_info = self.core.get_child_definition_info(self.root, child)
            self.assertTrue(self.util.equal(def_info['ownerNode'], self.root))
            self.assertTrue(self.util.equal(def_info['targetNode'], self.fco))

        self.assertEqual(len(name_to_child.keys()), 4)

        self.assertEqual(len(self.core.get_children_hashes(self.root).keys()), 4)
        self.assertTrue(self.equal(self.core.get_common_parent(children), self.root))
        self.assertEqual(self.core.get_common_parent([children[0]]), self.root)
        self.assertEqual(self.core.get_common_parent([self.root]), None)

        self.assertTrue(self.core.is_valid_new_parent(self.child2, self.child))
        self.assertFalse(self.core.is_valid_new_parent(self.child2, self.fco))

        self.assertTrue(self.core.is_valid_new_child(self.child2, self.child))
        self.assertFalse(self.core.is_valid_new_child(self.fco, self.fco))

    # @unittest.skip("Temp")
    def test_instance_base_related(self):
        self.assertEqual(self.core.get_base(self.fco), None)
        self.assertEqual(self.core.get_type_root(self.fco), None)
        self.assertTrue(self.equal(self.core.get_type_root(self.child), self.fco))
        self.assertTrue(self.equal(self.core.get_base(self.child_instance), self.child))

        instances = self.core.load_instances(self.child)
        instance_paths = self.core.get_instance_paths(self.child)
        self.assertEqual(len(instances), 1)
        self.assertEqual(len(instance_paths), 1)
        self.assertEqual(instance_paths[0], self.core.get_path(self.child_instance))
        self.assertTrue(self.equal(instances[0], self.child_instance))

        self.assertTrue(self.core.is_instance_of(self.child_instance, self.child))
        self.assertTrue(self.core.is_type_of(self.child_instance, self.child))
        self.assertTrue(self.core.is_instance_of(self.child_instance, self.core.get_path(self.child)))
        self.assertTrue(self.core.is_type_of(self.child_instance, self.core.get_path(self.child)))
        self.assertFalse(self.core.is_instance_of(self.child, self.child_instance))
        self.assertFalse(self.core.is_type_of(self.child, self.child_instance))

        self.assertTrue(self.equal(self.fco, self.core.get_base_root(self.child_instance)))
        self.assertTrue(self.equal(self.fco, self.core.get_base_type(self.child_instance)))
        self.assertTrue(self.equal(self.fco, self.core.get_meta_type(self.child_instance)))
        self.assertTrue(self.equal(self.core.get_base_root(self.root), self.root))
        self.assertEqual(self.core.get_base_type(self.root), None)
        self.assertEqual(self.core.get_meta_type(self.root), None)

        fco_instances = self.core.load_instances(self.fco)
        self.assertTrue(self.equal(self.core.get_common_base(fco_instances), self.fco))
        self.assertEqual(self.core.get_common_base([self.root, self.fco]), None)
        self.assertEqual(self.core.get_common_base([self.fco]), None)

        base_types = self.core.get_base_types(self.child)
        self.assertEqual(len(base_types), 1)
        self.assertTrue(self.equal(base_types[0], self.fco))

        self.assertTrue(self.core.is_valid_new_base(self.child_instance, self.child2))
        self.assertFalse(self.core.is_valid_new_base(self.child, self.child_instance))
        self.core.set_base(self.child_instance, self.child2)
        self.assertTrue(self.equal(self.core.get_base(self.child_instance), self.child2))

    # @unittest.skip("Temp")
    def test_pointer_related(self):
        self.core.set_pointer(self.child, 'ptr', self.fco)
        ptr_target = self.core.load_pointer(self.child_instance, 'ptr')
        ptr_path = self.core.get_pointer_path(self.child_instance, 'ptr')
        self.assertTrue(self.core.get_path(ptr_target), ptr_path)
        self.assertEqual(self.core.get_own_pointer_path(self.child_instance, 'ptr'), None)

        ptr_names = self.core.get_pointer_names(self.child_instance)
        own_ptr_names = self.core.get_own_pointer_names(self.child_instance)

        self.assertEqual(len(ptr_names), 2)
        ptr_names.sort()
        own_ptr_names.sort()
        self.assertEqual(len(ptr_names), 2)
        self.assertEqual(len(own_ptr_names), 1)
        self.assertEqual(ptr_names[0], own_ptr_names[0])

        coll_names = self.core.get_collection_names(self.fco)
        self.assertEqual(len(coll_names), 2)
        coll_names.sort()
        self.assertEqual(coll_names, ['base', 'ptr'])

        coll = self.core.load_collection(self.fco, 'ptr')
        coll_paths = self.core.get_collection_paths(self.fco, 'ptr')
        self.assertEqual(len(coll), 1)
        self.assertEqual(len(coll_paths), 1)
        self.assertEqual(self.core.get_path(coll[0]), coll_paths[0])

        self.core.rename_pointer(self.child, 'ptr', 'new_ptr')
        self.assertEqual(self.core.load_pointer(self.child, 'ptr'), None)
        self.assertTrue(self.equal(self.core.load_pointer(self.child, 'new_ptr'), self.fco))

        self.core.del_pointer(self.child, 'new_ptr')
        self.assertEqual(self.core.load_pointer(self.child, 'new_ptr'), None)

        self.core.set_pointer(self.child, 'ptr', self.fco)
        self.assertTrue(self.equal(self.core.load_pointer(self.child, 'ptr'), self.fco))
        self.core.delete_pointer(self.child, 'ptr')
        self.assertEqual(self.core.load_pointer(self.child, 'ptr'), None)

    # @unittest.skip("Temp")
    def test_set_related(self):
        self.core.create_set(self.child, 'set')
        self.core.add_member(self.child, 'set', self.child2)
        members = self.core.load_members(self.child_instance, 'set')
        own_members = self.core.load_own_members(self.child_instance, 'set')
        member_paths = self.core.get_member_paths(self.child_instance, 'set')
        own_member_paths = self.core.get_own_member_paths(self.child_instance, 'set')

        self.assertEqual(len(members), 1)
        self.assertEqual(len(own_members), 0)
        self.assertEqual(len(own_member_paths), 0)
        self.assertEqual([self.core.get_path(members[0])], member_paths)

        # Set attrs and regs
        self.core.set_set_attribute(self.child, 'set', 'attr', 'val')
        self.assertEqual(self.core.get_set_attribute_names(self.child_instance, 'set'), ['attr'])
        self.assertEqual(self.core.get_own_set_attribute_names(self.child_instance, 'set'), [])
        self.assertEqual(self.core.get_set_attribute(self.child_instance, 'set', 'attr'), 'val')
        self.assertEqual(self.core.get_own_set_attribute(self.child_instance, 'set', 'attr'), None)
        self.core.del_set_attribute(self.child, 'set', 'attr')
        self.assertEqual(self.core.get_set_attribute(self.child_instance, 'set', 'attr'), None)

        self.core.set_set_registry(self.child, 'set', 'reg', 'val')
        self.assertEqual(self.core.get_set_registry_names(self.child_instance, 'set'), ['reg'])
        self.assertEqual(self.core.get_own_set_registry_names(self.child_instance, 'set'), [])
        self.assertEqual(self.core.get_set_registry(self.child_instance, 'set', 'reg'), 'val')
        self.assertEqual(self.core.get_own_set_registry(self.child_instance, 'set', 'reg'), None)
        self.core.del_set_registry(self.child, 'set', 'reg')
        self.assertEqual(self.core.get_set_registry(self.child_instance, 'set', 'reg'), None)

        # Set-member attrs and regs
        p = member_paths[0]
        self.core.set_member_attribute(self.child, 'set', p, 'attr', 'val')
        self.assertEqual(self.core.get_member_attribute_names(self.child_instance, 'set', p), ['attr'])
        self.assertEqual(self.core.get_member_own_attribute_names(self.child_instance, 'set', p), [])
        self.assertEqual(self.core.get_member_attribute(self.child_instance, 'set', p, 'attr'), 'val')
        self.assertEqual(self.core.get_member_own_attribute(self.child_instance, 'set', p, 'attr'), None)
        self.core.del_member_attribute(self.child, 'set', p, 'attr')
        self.assertEqual(self.core.get_member_attribute(self.child_instance, 'set', p, 'attr'), None)

        self.core.set_member_registry(self.child, 'set', p, 'reg', 'val')
        self.assertEqual(self.core.get_member_registry_names(self.child_instance, 'set', p), ['reg'])
        self.assertEqual(self.core.get_member_own_registry_names(self.child_instance, 'set', p), [])
        self.assertEqual(self.core.get_member_registry(self.child_instance, 'set', p, 'reg'), 'val')
        self.assertEqual(self.core.get_member_own_registry(self.child_instance, 'set', p, 'reg'), None)
        self.core.del_member_registry(self.child, 'set', p, 'reg')
        self.assertEqual(self.core.get_member_registry(self.child_instance, 'set', p, 'reg'), None)

        # Renaming, deletions etc.
        self.core.rename_set(self.child, 'set', 'newSet')
        self.assertEqual(self.core.get_set_names(self.child_instance), ['newSet'])
        self.assertEqual(self.core.get_own_set_names(self.child_instance), [])
        self.core.del_member(self.child, 'newSet', p)
        self.assertEqual(self.core.load_members(self.child, 'newSet'), [])
        self.core.del_set(self.child, 'newSet')
        self.assertEqual(self.core.get_set_names(self.child), [])

        self.core.create_set(self.child, 'set')
        self.core.create_set(self.child, 'set2')
        self.core.add_member(self.child, 'set', self.child2)
        self.assertEqual(self.core.get_set_names(self.child), ['set', 'set2'])
        self.assertEqual(self.core.get_member_paths(self.child, 'set'), [p])
        self.assertEqual(self.core.get_member_paths(self.child, 'set2'), [])
        self.core.move_member(self.child, p, 'set', 'set2')
        # TODO: Should move_member delete the set when its the last member?
        # self.assertEqual(self.core.get_member_paths(self.child, 'set'), [])
        self.assertEqual(self.core.get_member_paths(self.child, 'set2'), [p])

        self.core.delete_set(self.child, 'set')
        self.core.delete_set(self.child, 'set2')
        self.assertEqual(self.core.get_set_names(self.child), [])

    # @unittest.skip("Temp")
    def test_meta_and_mixin_related(self):
        p = self.core.get_path(self.child)
        p2 = self.core.get_path(self.child2)
        self.assertFalse(self.core.is_meta_node(self.child))

        self.core.add_member(self.root, 'MetaAspectSet', self.child)
        self.core.add_member(self.root, 'MetaAspectSet', self.child2)
        self.core.add_mixin(self.child, self.core.get_path(self.child2))

        self.assertTrue(self.core.is_meta_node(self.child))
        all_meta_nodes = self.core.get_all_meta_nodes(self.root)
        meta_nodes_paths = [p, p2]
        meta_nodes_paths.sort()
        self.assertEqual(len(list(all_meta_nodes.keys())), 3)
        self.assertTrue(self.equal(self.core.get_meta_type(self.child_instance), self.child))
        self.assertTrue(self.equal(self.core.get_base_type(self.child_instance), self.child))

        base_types = list(map(lambda b: self.core.get_path(b), self.core.get_base_types(self.child_instance)))
        base_types.sort()
        self.assertEqual(base_types, meta_nodes_paths)

        # Containment
        self.core.set_child_meta(self.child, self.child2)
        child_meta = self.core.get_children_meta(self.child)
        self.assertEqual(len(list(child_meta.keys())), 1)
        self.assertEqual(child_meta[p2], {'max': -1, 'min': -1})
        self.assertTrue(self.core.is_valid_child_of(self.child2, self.child))
        self.assertEqual(self.core.get_valid_children_paths(self.child), child_meta.keys())

        child_info = self.core.get_child_definition_info(self.child_instance, self.child2)
        self.assertTrue(self.equal(child_info['ownerNode'], self.child))
        self.assertTrue(self.equal(child_info['targetNode'], self.child2))

        valid_children = self.core.get_valid_children_meta_nodes({'node': self.child_instance})

        self.assertEqual(len(valid_children), 2)
        valid_children = list(map(lambda c: self.core.get_path(c), valid_children))
        valid_children.sort()
        self.assertEqual(valid_children, meta_nodes_paths)

        self.core.set_children_meta_limits(self.child, 1, 2)
        child_meta = self.core.get_children_meta(self.child)

        self.assertEqual(len(list(child_meta.keys())), 3)
        self.assertEqual(child_meta[p2], {'max': -1, 'min': -1})
        self.assertEqual(child_meta['min'], 1)
        self.assertEqual(child_meta['max'], 2)

        # Attributes
        self.assertEqual(self.core.get_valid_attribute_names(self.child_instance), ['name'])
        self.core.set_attribute_meta(self.child, 'attr', {'type': 'string', 'default': 'val'})
        self.assertEqual(len(self.core.get_valid_attribute_names(self.child_instance)), 2)
        self.assertEqual(self.core.get_own_valid_attribute_names(self.child_instance), [])
        self.assertTrue(self.core.is_valid_attribute_value_of(self.child_instance, 'attr', 'aString'))
        self.assertFalse(self.core.is_valid_attribute_value_of(self.child_instance, 'attr', 1))
        self.assertTrue(self.equal(self.core.get_attribute_definition_owner(self.child_instance, 'attr'), self.child))

        self.core.rename_attribute_meta(self.child, 'attr', 'newAttr')
        self.assertEqual(self.core.get_own_valid_attribute_names(self.child), ['newAttr'])

        attr_meta = self.core.get_attribute_meta(self.child, 'newAttr')
        self.assertEqual(attr_meta, {'type': 'string'})

        # Pointers
        self.core.set_pointer_meta_target(self.child, 'ptr', self.child2)
        self.core.set_pointer_meta_limits(self.child, 'ptr', 1, 1)
        self.assertEqual(self.core.get_valid_pointer_names(self.child_instance), ['ptr'])
        self.assertEqual(self.core.get_own_valid_pointer_names(self.child_instance), [])
        self.assertEqual(self.core.get_valid_target_paths(self.child_instance, 'ptr'), [p2])
        self.assertEqual(self.core.get_own_valid_target_paths(self.child_instance, 'ptr'), [])
        self.assertTrue(self.core.is_valid_target_of(self.child2, self.child_instance, 'ptr'))
        self.assertFalse(self.core.is_valid_target_of(self.child_instance, self.child2, 'ptr'))

        ptr_info = self.core.get_pointer_definition_info(self.child_instance, 'ptr', self.child2)
        self.assertTrue(self.equal(ptr_info['ownerNode'], self.child))
        self.assertTrue(self.equal(ptr_info['targetNode'], self.child2))

        self.core.move_pointer_meta_target(self.child, self.child2, 'ptr', 'newPtr')
        ptr_meta = self.core.get_pointer_meta(self.child_instance, 'newPtr')

        self.assertEqual(len(ptr_meta.keys()), 3)
        self.assertEqual(ptr_meta[p2], {'max': -1, 'min': -1})
        self.assertEqual(ptr_meta['min'], 1)
        self.assertEqual(ptr_meta['max'], 1)

        # Sets
        self.core.set_pointer_meta_target(self.child, 'set', self.child2)
        self.assertEqual(self.core.get_valid_set_names(self.child_instance), ['set'])
        self.assertEqual(self.core.get_own_valid_set_names(self.child_instance), [])
        self.assertEqual(self.core.get_valid_target_paths(self.child_instance, 'set'), [p2])
        self.assertEqual(self.core.get_own_valid_target_paths(self.child_instance, 'set'), [])
        self.assertTrue(self.core.is_valid_target_of(self.child2, self.child_instance, 'set'))
        self.assertFalse(self.core.is_valid_target_of(self.child_instance, self.child2, 'set'))

        set_info = self.core.get_set_definition_info(self.child_instance, 'set', self.child2)
        self.assertTrue(self.equal(set_info['ownerNode'], self.child))
        self.assertTrue(self.equal(set_info['targetNode'], self.child2))

        valid_set_nodes = self.core.get_valid_set_elements_meta_nodes({'node': self.child_instance, 'name': 'set'})

        self.assertEqual(len(valid_set_nodes), 2)
        valid_set_nodes = map(lambda c: self.core.get_path(c), valid_set_nodes)
        valid_set_nodes.sort()
        self.assertEqual(valid_set_nodes, meta_nodes_paths)

        self.core.move_pointer_meta_target(self.child, self.child2, 'set', 'newSet')
        set_meta = self.core.get_pointer_meta(self.child_instance, 'newSet')

        self.assertEqual(len(set_meta.keys()), 3)
        self.assertEqual(set_meta[p2], {'max': -1, 'min': -1})
        self.assertEqual(set_meta['min'], -1)
        self.assertEqual(set_meta['max'], -1)

        # Constraints
        c_input = {
            'script': "function (core, node, callback) {callback(null, {hasViolation: false, message: ''});}",
            'priority': 1,
            'info': "Should check unique name"
        }
        self.core.set_constraint(self.child, 'cc', c_input)

        self.assertEqual(self.core.get_own_constraint_names(self.child_instance), [])
        self.assertEqual(self.core.get_constraint_names(self.child_instance), ['cc'])
        constraint_meta = self.core.get_constraint(self.child_instance, 'cc')
        self.assertEqual(constraint_meta, c_input)

        # Aspects
        self.core.set_aspect_meta_target(self.child, 'ass', self.child2)
        self.assertEqual(self.core.get_valid_aspect_names(self.child_instance), ['ass'])
        self.assertEqual(self.core.get_own_valid_aspect_names(self.child_instance), [])
        self.assertEqual(self.core.get_valid_aspect_target_paths(self.child_instance, 'ass'), [p2])
        self.assertEqual(self.core.get_own_valid_aspect_target_paths(self.child_instance, 'ass'), [])
        self.assertTrue(self.core.is_valid_aspect_member_of(self.child2, self.child_instance, 'ass'))
        self.assertFalse(self.core.is_valid_aspect_member_of(self.fco, self.child_instance, 'ass'))
        aspect_info = self.core.get_aspect_definition_info(self.child_instance, 'ass', self.child2)
        self.assertTrue(self.equal(aspect_info['ownerNode'], self.child))
        self.assertTrue(self.equal(aspect_info['targetNode'], self.child2))
        self.assertTrue(self.equal(self.core.get_aspect_definition_owner(self.child_instance, 'ass'), self.child))

        self.core.move_aspect_meta_target(self.child, self.child2, 'ass', 'newAss')
        ass_meta = self.core.get_aspect_meta(self.child_instance, 'newAss')

        self.assertEqual(ass_meta, [p2])

        # Mixins
        mix_paths = self.core.get_mixin_paths(self.child)
        mix_nodes = self.core.get_mixin_nodes(self.child)
        self.assertTrue(self.core.can_set_as_mixin(self.child, p2)['isOk'])
        self.assertFalse(self.core.can_set_as_mixin(self.child, self.core.get_path(self.fco))['isOk'])
        self.assertEqual(len(mix_paths), 1)
        self.assertEqual(len(mix_nodes.keys()), 1)
        self.assertEqual(mix_paths[0], mix_nodes.keys()[0])

        self.assertEqual(len(self.core.get_mixin_paths(self.child_instance)), 0)
        self.assertEqual(len(self.core.get_mixin_errors(self.child)), 0)

        # Json and removals
        json_meta = self.core.get_json_meta(self.child_instance)
        self.assertEqual(self.core.get_own_json_meta(self.child_instance), {})

        self.assertEqual(json_meta['aspects']['newAss'], ass_meta)
        self.assertEqual(json_meta['attributes']['newAttr'], attr_meta)

        self.assertEqual(json_meta['children']['max'], child_meta['max'])
        self.assertEqual(json_meta['children']['min'], child_meta['min'])
        self.assertEqual(json_meta['children']['items'], [p2])
        self.assertEqual(json_meta['children']['maxItems'], [child_meta[p2]['max']])
        self.assertEqual(json_meta['children']['minItems'], [child_meta[p2]['min']])

        self.assertEqual(json_meta['constraints']['cc'], constraint_meta)

        self.assertEqual(json_meta['pointers']['newPtr']['max'], ptr_meta['max'])
        self.assertEqual(json_meta['pointers']['newPtr']['min'], ptr_meta['min'])
        self.assertEqual(json_meta['pointers']['newPtr']['items'], [p2])
        self.assertEqual(json_meta['pointers']['newPtr']['maxItems'], [ptr_meta[p2]['max']])
        self.assertEqual(json_meta['pointers']['newPtr']['minItems'], [ptr_meta[p2]['min']])

        self.assertEqual(json_meta['pointers']['newSet']['max'], set_meta['max'])
        self.assertEqual(json_meta['pointers']['newSet']['min'], set_meta['min'])
        self.assertEqual(json_meta['pointers']['newSet']['items'], [p2])
        self.assertEqual(json_meta['pointers']['newSet']['maxItems'], [set_meta[p2]['max']])
        self.assertEqual(json_meta['pointers']['newSet']['minItems'], [set_meta[p2]['min']])

        self.core.del_mixin(self.child, p2)
        self.core.clear_mixins(self.child)
        self.core.del_aspect_meta_target(self.child, 'newAss', p2)
        self.core.del_aspect_meta(self.child, 'newAss')
        self.core.del_attribute_meta(self.child, 'newAttr')
        self.core.del_pointer_meta_target(self.child, 'newPtr', p2)
        self.core.del_pointer_meta(self.child, 'newPtr')
        self.core.del_pointer_meta_target(self.child, 'newSet', p2)
        self.core.del_pointer_meta(self.child, 'newSet')
        self.core.del_child_meta(self.child, p2)
        self.core.del_constraint(self.child, 'cc')

        self.assertEqual(self.core.get_own_json_meta(self.child), {})

        self.core.set_attribute_meta(self.child2, 'attr', {'type': 'string', 'default': 'val'})
        self.core.clear_meta_rules(self.child2)
        self.assertEqual(self.core.get_own_json_meta(self.child2), {})

    def test_exceptions(self):
        self.assertRaises(CoreIllegalOperationError, self.core.get_set_attribute, self.fco, 'doesNotExist', 'attr')
        self.assertRaises(CoreIllegalArgumentError, self.core.get_set_attribute, self.fco, 'doesNotExist', 45)

    @unittest.skip("TODO")
    def test_library_related(self):
        pass

    @unittest.skip("TODO")
    def test_diff_related(self):
        pass


# class UtilTests(object):
class UtilTests(ConnectedTestClass):
    def setUp(self):
        super(UtilTests, self).setUp()
        c_obj = self.project.get_commit_object('master')
        self.commit_hash = c_obj['_id']
        self.root = self.core.load_root(c_obj['root'])
        self.fco = self.core.get_fco(self.root)

    def tearDown(self):
        self.util.unload_root(self.root)
        super(UtilTests, self).tearDown()

    def test_gme_config(self):
        gme_conf = self.util.gme_config
        self.assertFalse(gme_conf['debug'])
        gme_conf2 = self.util.gme_config
        self.assertTrue(gme_conf is gme_conf2)  # Referencing the same object

    def test_retrieving_meta_map(self):
        META = self.util.META(self.root)
        self.assertTrue(len(META.keys()), 1)
        self.assertEqual(list(META.keys())[0], 'FCO')
        self.assertEqual(self.core.get_path(META[list(META.keys())[0]]), self.core.get_path(self.fco))

    def test_error_handling_at_retrieving_meta_map_with_none_existing_nsp(self):
        self.assertRaises(JSError, self.util.META, self.root, 'doesNotExist')

    def test_save_should_make_a_commit(self):
        self.core.set_attribute(self.fco, 'name', 'new_name')
        c_res = self.util.save(self.root, self.commit_hash, None, 'Herro')
        c_obj = self.project.get_commit_object(c_res['hash'])

        self.assertEqual(c_obj['parents'][0], self.commit_hash)
        self.assertEqual(c_obj['message'], 'Herro')

        new_root = self.core.load_root(c_obj['root'])
        new_fco = self.core.get_fco(new_root)
        self.assertEqual(self.core.get_attribute(new_fco, 'name'), 'new_name')
        self.util.unload_root(new_root)

    def test_persist_and_commit_without_util(self):
        self.core.set_attribute(self.fco, 'name', 'another_new_name')
        persisted = self.core.persist(self.root)
        c_res = self.project.make_commit(None, [self.commit_hash], persisted['rootHash'], persisted['objects'],
                                         'PersCom')

        c_obj = self.project.get_commit_object(c_res['hash'])

        self.assertEqual(c_obj['parents'][0], self.commit_hash)
        self.assertEqual(c_obj['message'], 'PersCom')

        new_root = self.core.load_root(c_obj['root'])
        new_fco = self.core.get_fco(new_root)
        self.assertEqual(self.core.get_attribute(new_fco, 'name'), 'another_new_name')
        self.util.unload_root(new_root)

    def test_unloading_root(self):
        self.assertEqual(self.core.get_attribute(self.fco, 'name'), 'FCO')
        self.util.unload_root(self.fco)  # any node can be passed
        self.assertRaises(JSError, self.core.get_attribute, self.fco, 'name')

    def test_traverse_should_visit_all_nodes(self):
        self.child = self.core.create_child(self.root, self.fco)
        self.core.set_attribute(self.child, 'name', 'child')

        self.child2 = self.core.create_child(self.root, self.fco)
        self.core.set_attribute(self.child2, 'name', 'child2')
        self.child_instance = self.core.create_child(self.root, self.child)
        self.core.set_attribute(self.child_instance, 'name', 'child_instance')
        names = []

        def at_node(node):
            names.append(self.core.get_attribute(node, 'name'))

        self.util.traverse(self.root, at_node)
        self.assertEqual(len(names), 5)


class PluginExample(PluginBase):
    def main(self):
        return True


# class PluginTests(object):
class PluginTests(ConnectedTestClass):
    def setUp(self):
        super(PluginTests, self).setUp()
        c_obj = self.project.get_commit_object('master')
        self.commit_hash = c_obj['_id']
        self.root = self.core.load_root(c_obj['root'])
        self.fco = self.core.get_fco(self.root)
        self.plugin = PluginExample(self.webgme, self.commit_hash)

    def tearDown(self):
        self.util.unload_root(self.root)
        super(PluginTests, self).tearDown()

    def test_main_should_throw_from_base_but_not_derived(self):
        plugin_base = PluginBase(self.webgme, self.commit_hash)

        self.assertRaises(NotImplementedError, plugin_base.main)
        self.assertTrue(self.plugin.main())

    def test_should_add_active_selection(self):
        path = self.core.get_path(self.fco)
        plugin = PluginExample(self.webgme, self.commit_hash, 'master', path, [path])
        self.assertTrue(self.util.equal(plugin.active_node, self.fco))
        self.assertTrue(self.util.equal(plugin.active_selection[0], self.fco))

    def test_should_get_properties(self):
        META = self.plugin.META
        self.assertEqual(len(META.keys()), 1)
        self.assertTrue(self.util.equal(META[list(META.keys())[0]], self.fco))
        config = self.plugin.gme_config
        self.assertFalse(config['debug'])

    def test_should_get_current_config(self):
        config = self.plugin.get_current_config()
        self.assertEqual(len(config.keys()), 0)

    def test_should_add_get_file(self):
        text = 'Hello world'
        hash = self.plugin.add_file('my_file.txt', text)
        self.assertEqual(len(hash), 40)
        self.assertEqual(self.plugin.get_file(hash), text)

    def test_should_add_get_artifact(self):
        hash = self.plugin.add_artifact('anArtifact', {'f1.txt': 'Hello1', 'f2.txt': 'Hello2'})
        self.assertEqual(len(hash), 40)
        art = self.plugin.get_artifact(hash)
        self.assertEqual(art['f1.txt'], 'Hello1')
        self.assertEqual(art['f2.txt'], 'Hello2')
        self.assertEqual(len(art.keys()), 2)

    def test_should_not_fail_to_message(self):
        # Note that these are no-ops
        self.plugin.create_message(self.root, 'hello')
        self.plugin.send_notification('hello')


# Import test project(s)
if 'DO_NOT_START_SERVER' not in my_env:
    status = subprocess.call(['node', WEBGME_IMPORT_BIN, SEED_FILE, '-p', TEST_PROJECT, '--overwrite'],
                             env=my_env, cwd=root_dir)
else:
    print('DO_NOT_START_SERVER env. set -> will not start any nodejs processes')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ProjectTests)
    runner = unittest.TextTestRunner().run(suite)
