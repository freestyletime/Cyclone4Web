import os

class Config(object):
    """ It's used for setting web application parameters """
    DEBUG = True


class Constants(object):
    """ It's used for maintaining constants """
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise (self.ConsError, "Can't change const.%s" % name)
        if not name.isupper():
            raise (self.ConstCaseError, "const name '%s' is not all uppercase" % name)
        self.__dict__[name] = value

const = Constants()
# resource
const.HTML_INDEX = "index.html"
const.HTML_ABOUT = "about.html"
const.HTML_ERROR = "error.html"
const.SPT_EX = "./ex.sh"
const.SPT_DOT = "./dot2png.sh"
const.PNG_CYCLONE = "cyclone.png"
# upload configuration
const.ALLOWED_EXTENSIONS = set(["cyclone"])
const.ALLOWED_EXTENSIONS_DOT = "dot"
const.MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
# constant keys & values
const.BRAND_PREFIX = "CYCLONE4WEB-USER-";
const.DEFAULT_FILE_NAME = 'Main.cyclone'

const.PATH_PROJECT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
const.PATH_EXAMPLE = const.PATH_PROJECT + os.sep + 'cyclone' + os.sep + 'examples'
const.PATH_TMP_STORAGE = const.PATH_PROJECT + os.sep + 'tmp'

const.FIELD_USER_ID = "unique_user_id"
const.FIELD_USER_CODE = "code"
const.FIELD_FILE = "file"
const.FIELD_FOLDER = "folder"
const.FIELD_FILE_PATH = "path"

const.SUCCESS_REQ = "Request successully!"
const.SUCCESS_REQ_UPDATE = "Successully upload your file!"

const.ERROR_USER_ID = "Lacking of user id! Try going back to the homepage."
const.ERROR_CODE_ETY = "The code is empty, please run again!"
const.ERROR_CYC_TRACE_RETURN = "Cyclone doesn't return the trace file! Please contact administration to fix it!"
const.ERROR_FILE_NOT_EXIST = "Lacking of the file!"
const.ERROR_FILE_NAME_ETY = "The file name is empty!"
const.ERROR_FILE_UPDATE = "Only support the file with .cyclone format. Please try it again!"

const.CODE_USER_ID = "CE00001";
const.CODE_CODE_ETY = "CE00002";
const.CODE_CYC_TRACE_RETURN = "CE00003";
const.CODE_FILE_NOT_EXIST = "CE00004";
const.CODE_FILE_NAME_ETY = "CE00005";
const.CODE_FILE_UPDATE = "CE00006";

const.DES_HTTP_CODE_404 = "Hey, sorry, but the page you're trying to access doesn't exist. Try going back to the homepage, or use the navigation menu above to find what you're looking for."
const.DES_HTTP_CODE_405 = "This page can not support this way to request. Please try going back to the home page."