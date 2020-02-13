import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('PythonBindings')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class PythonBindings(PluginBase):

    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node

        logger.info(self.get_current_config())

        name = core.get_attribute(active_node, 'name')

        logger.info('ActiveNode at "{0}" has name {1}'.format(core.get_path(active_node), name))

        def traverse_tree_rec(node, depth):
            indent = '  ' * depth
            node_name = core.get_attribute(node, 'name')
            type_node = core.get_base_type(node)
            type_name = 'N/A'
            if type_node:
                type_name = core.get_attribute(type_node, 'name')

            logger.info('{0}# {1} is of type {2}'.format(indent, node_name, type_name))

            logger.info('{0}  attributes:'.format(indent))
            for attr_name in core.get_attribute_names(node):
                val = core.get_attribute(node, attr_name)
                logger.info('  {0} {1} "{2}" [{3}]:'.format(indent, attr_name, val, type(val)))

            logger.info('{0}  pointers:'.format(indent))
            for ptr_name in core.get_valid_pointer_names(node):
                val = core.get_pointer_path(node, ptr_name)
                logger.info('  {0} {1} "{2}" [{3}]:'.format(indent, ptr_name, val, type(val)))

            for child_node in core.load_children(node):
                traverse_tree_rec(child_node, depth + 1)

        logger.info('## Node Tree ##')
        traverse_tree_rec(root_node, 1)

        self.create_message(root_node, 'Hello')
        self.add_file('f.txt', 'Hello')
