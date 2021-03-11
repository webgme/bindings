"""
This is where the implementation of the plugin code goes.
The PythonBindingsWait-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
import time
from datetime import datetime
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('PythonBindingsWait')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class PythonBindingsWait(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node
        config = self.get_current_config()

        name = core.get_attribute(active_node, 'name')

        logger.info('ActiveNode at "{0}" has name {1}'.format(core.get_path(active_node), name))

        logger.info('Will wait for {0} seconds.'.format(config['wait']))
        time.sleep(config['wait'])
        if config['modify'] == True:
            now = datetime.now()
            core.set_attribute(active_node, 'name', now.strftime('%m/%d/%Y, %H:%M:%S'))
            commit_info = self.util.save(root_node, self.commit_hash, self.branch_name, 'Python plugin updated the model')
            logger.info('committed :{0}'.format(commit_info))
        else:
            logger.info('no modification was done')
