import os

# It's used for setting web application parameters
class Config(object):
    DEBUG = True


# It's used for saving constants
class Constants(object):
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise (self.ConsError, "Can't change const.%s" % name)
        if not name.isupper():
            raise (self.ConstCaseError, "const name '%s' is not all uppercase" % name)
        self.__dict__[name] = value

const = Constants()
const.PATH_PROJECT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
const.DEFAULT_FILE_NAME = 'Main.cyclone'
const.PATH_EXAMPLE = const.PATH_PROJECT + os.sep + 'cyclone' + os.sep + 'examples'
const.PATH_TMP_STORAGE = const.PATH_PROJECT + os.sep + 'tmp'