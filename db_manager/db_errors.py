class DBError(Exception):
    def __init__(self, message=None):
        """
        Class to rise exception for error that happen in voice app. This is the general class.

        Args:
            message (str): message explaining the error thrown. By default
                            "An error has occurred at Voice app"

        Notes:
            Author: Glorimar Castro-Noriega
            Date: 3-3-19
        """
        if message is None:
            message = "An error has occurred at DB Manager"
        super(DBError, self).__init__(message)


class ArgsCantBeNone(DBError):
    def __init__(self, funct_name=None, *args):
        """
        Exception to be raise when an argument value was expected but instead None was set
        Args:
            funct_name (str): name of the function were ArgsCantBeNone is raise
            *args (str): args at function that cannot be None. At least one value should be pass
        Notes:
            Author: Glorimar Castro-Noriega
            Date: 3-3-19
        """
        if funct_name is None:
            funct_name = "unknown function at db manager"
        message = "The following arguments can't be None: "
        for arg in args:
            message += arg + ", "

        message = message[:-2] + ' at %s() function' % funct_name

        super(ArgsCantBeNone, self).__init__(message)


class InvalidArgValue(DBError):
    message = None

    def __init__(self, given_value=None, *allowed_values):
        """
        Exception to be raise if a value is not in an allowed value
        Args:
            given_value (str): the invalid value given
            *allowed_values (str): list of all allowed values
        Notes:
            Author: Glorimar Castro-Noriega
            Date: 3-3-19
        """
        self.message = 'The given value "%s" is invalid. Possible values are: ' % given_value
        for arg in allowed_values:
            self.message += arg + ", "
        self.message = self.message[:-2] + "."

        super(InvalidArgValue, self).__init__(self.message)
