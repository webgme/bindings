"""
This is where the implementation of the plugin code goes.
The PythonExtraFunctions-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('PythonExtraFunctions')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class PythonExtraFunctions(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node
        config = self.get_current_config()

        if config['one']:
            logger.info(self.promising(config['one']))
        self.additional(config['one'], config['two'])

    def additional(self, paramOne, paramTwo):
        return self._send({'name':'additional', 'args':[paramOne, paramTwo]})
    
    def promising(self, paramOne):
        return self._send({'name':'promising', 'args':[paramOne]})
