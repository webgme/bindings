import zmq
import json
import sys
import logging

from .core import Core
from .project import Project
from .util import Util
from .exceptions import CoreIllegalArgumentError, CoreIllegalOperationError, CoreInternalError, JSError

is_python_3 = sys.version_info > (3, 0)


class WebGME(object):
    """
    The main class for connecting to the webgme api
    """

    def __init__(self, port=5555, logger=None, address=None):
        """
        Creates an instance of WebGME and creates and connects a zmq socket-object to
        tcp://127.0.0.1:<port>. To disconnect use the disconnect method.

        :param port: The port that the webgme zmq-server listens on.
        :type port: int or str
        :param logger: Optional logger (defaults to DEBUG console logger)
        :param address: If given the port is not used and the zmq client will connect to the address.
        :type address: str
        """
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger('webgme')
            if len(self.logger.handlers) == 0:
                self.logger.setLevel(logging.DEBUG)
                handler = logging.StreamHandler(sys.stdout)
                handler.setLevel(logging.DEBUG)
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)

            self.logger.warning('No logger passed to WebGME - created console logger at DEBUG level.')
            self.logger.warning('Pass a configured logger to the constructor to suppress DEBUG messages.')

        self._socket = zmq.Context().socket(zmq.REQ)
        if address is None:
            self._address = 'tcp://127.0.0.1:{0}'.format(port)
        else:
            self._address = address

        self._socket.connect(self._address)
        self.logger.info('Connected to {0}'.format(self._address))
        self.core = Core(self)
        self.util = Util(self)
        self.project = Project(self)

    def disconnect(self):
        """
        Disconnects from the nodejs zmq-server.
        """
        self._socket.disconnect(self._address)
        self.logger.info('Disconnected from {0}'.format(self._address))

    def send_request(self, payload):
        self.logger.debug('send_request: {0}'.format(payload))
        if is_python_3:
            self._socket.send_string(json.dumps(payload))
        else:
            self._socket.send(json.dumps(payload))

    def handle_response(self):
        if is_python_3:
            raw_res = self._socket.recv_string()
        else:
            raw_res = self._socket.recv()

        self.logger.debug('handle_response: {0}'.format(raw_res))
        res = json.loads(raw_res)

        if res['err']:
            if res['err']['type'] == 'CoreIllegalArgumentError':
                raise CoreIllegalArgumentError(res['err'])
            elif res['err']['type'] == 'CoreIllegalOperationError':
                raise CoreIllegalOperationError(res['err'])
            elif res['err']['type'] == 'CoreInternalError':
                raise CoreInternalError(res['err'])
            else:
                raise JSError(res['err'])

        if 'res' in res:
            return res['res']
        else:
            return None
