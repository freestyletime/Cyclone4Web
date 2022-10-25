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
const.DEFAULT_FILE_NAME = 'Main.java'
const.PATH_EXAMPLE = './cyclone/examples/'
const.PATH_TMP_STORAGE = './tmp'