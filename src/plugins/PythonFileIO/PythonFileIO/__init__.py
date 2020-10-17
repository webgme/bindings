"""
This is where the implementation of the plugin code goes.
The PythonFileIO-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
import os
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('PythonFileIO')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class PythonFileIO(PluginBase):
    def main(self):
        core = self.core
        root_node = self.root_node
        active_node = self.active_node

        name = core.get_attribute(active_node, 'name')

        binary_file = open('./src/plugins/PythonFileIO/PythonFileIO/heart.png','rb')
        binary_content = binary_file.read()

        bin_hash = self.add_file('heart.png', binary_content)
        retrieved_content = self.get_bin_file(bin_hash)
        if binary_content != retrieved_content:
            self.logger.error('issue in simple binary')
            self.result_set_success(False)
            self.result_set_error('simple binary content mismatch')

        arti_hash = self.add_artifact('myArti', {'text.txt':'just because', 'heart.png':binary_content})
        retrieved_content_from_arti = self.get_bin_file(arti_hash,'heart.png')
        if binary_content != retrieved_content_from_arti:
            self.logger.error('issue in complex blob')
            self.result_set_success(False)
            self.result_set_error('embedded binary content mismatch')

        
