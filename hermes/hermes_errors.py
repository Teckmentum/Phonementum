class HermesError(Exception):
    def __init__(self, message=None):
        """
        Class to rise exception for error that happen in voice app. This is the general class.

        Args:
            message (str): message explaining the error thrown. By default
                            "An error has occurred at Hermes app"

        Notes:
            1. Author: Glorimar Castro-Noriega
        """
        if message is None:
            message = "Hermes seem to be sick"
        super(HermesError, self).__init__(message)


class MissingParameterAtRequest(HermesError):
    message = None

    def __init__(self, *args):
        self.message = 'Hermes is missing a parameter at request.'
        if args is not None:
            self.message += " The following argument(s) is(are) missing: "
        for arg in args:
            self.message += arg + ", "
        if args is not None:
            self.message = self.message[0:-2]

        super(MissingParameterAtRequest, self).__init__(self.message)


