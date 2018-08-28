"""
Collection of Exception-classes that correspond to exceptions thrown within the
running nodejs process.
"""


class JSError(Exception):
    """
    Base class for exceptions/errors raised from coremq on the java-script side while handling a request.
    """

    def __init__(self, err_data):
        # Call the base class constructor with the regular message
        super(JSError, self).__init__(err_data['message'])

        self.js_stack = err_data['stack']
        self.req = err_data['req']

    def get_js_stack(self):
        return self.js_stack

    def get_req(self):
        return self.req


class CoreIllegalArgumentError(JSError):
    """
    CoreIllegalArgumentError should be thrown if the type of the input parameters is not what it should be.
    """
    def __init__(self, err_data):
        super(CoreIllegalArgumentError, self).__init__(err_data)


class CoreIllegalOperationError(JSError):
    """
     CoreIllegalOperationError should be thrown if the set of input parameters are correct but the request\
     or the operation do not apply to the current context. Here we followed the basic javascript principles\
     in terms that whenever the user try to access a 'field' of a 'field' that does not exist, we throw.\
     For example if someone tries to get the member attributes of an non-existing member.\
     Trying to modify read-only nodes are captured within this category.
    """

    def __init__(self, err_data):
        super(CoreIllegalOperationError, self).__init__(err_data)


class CoreInternalError(JSError):
    """
     CoreInternalError should be thrown if some internal ASSERTION fails, it triggers some fault inside the core\
     and should typically be checked by the developer team, not the one who uses it.
    """

    def __init__(self, err_data):
        super(CoreInternalError, self).__init__(err_data)
