import os, subprocess, sys, time, uuid
from flask import Blueprint, request, render_template, jsonify, make_response, send_file, abort
from werkzeug.utils import secure_filename
from ..config import const
from pathlib import Path


# = = = = = = = = = = = = = = = = = =
### Native private methods
def _response_(status, msg, code='', data=''):
    """
    Basic web interface format
    ---
    description: 
    
    1.Bool status : 0 -> success / 1 -> failure
    2.String msg : error message
    3.Data : fetching data when success
    4.String code : error code when fail (start with 'CE')
    
    example:
    {"status" : 0, "msg" : "request success", "data":[]}
    {"status" : 1, "msg" : "password invalid", "code":"CE00001"}
    """
    if status:
        return jsonify({"status" : 0, "msg" : msg, "data" : data})
    else :
        return jsonify({"status" : 1, "msg" : msg, "code" : code})

def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in const.ALLOWED_EXTENSIONS


def _get_user_id():
    # Production
    return request.cookies.get(const.FIELD_USER_ID)
    # Test
    # return request.form.get(const.FIELD_USER_ID)


def _check_path():
    parent = const.PATH_TMP_STORAGE + os.sep + _get_user_id()
    path = parent + os.sep + const.DEFAULT_FILE_NAME
    if not Path(parent).exists(): Path(parent).mkdir()
    if not Path(path).exists(): Path(path).touch()
    return path
# = = = = = = = = = = = = = = = = = =


### Web interface
editor = Blueprint("editor", __name__, url_prefix="/editor")


@editor.route("/", methods = ['GET'])
def initial():
    """
    Main page for users
    ---
    description: show users an online Cyclone IDE
    parameters:
      - name: id
        type: string
        required: false
        default: null
        description: every new user will have an unique id or retrieve the previous id stored in the cookie
    responses:
      200:
        description: successfully show the webpage 'index.html'
    """

    if _get_user_id():
        parent = const.PATH_TMP_STORAGE + os.sep + _get_user_id()
        if Path(parent).exists():
            code = Path(parent + os.sep + const.DEFAULT_FILE_NAME).read_text()
            return render_template(const.HTML_INDEX, code=code)
    
    code = Path(const.PATH_TMP_STORAGE + os.sep + const.DEFAULT_FILE_NAME).read_text()
    res = make_response(render_template(const.HTML_INDEX, code=code))
    res.set_cookie(const.FIELD_USER_ID, const.BRAND_PREFIX + str(uuid.uuid4()))
    return res


@editor.route("/run", methods = ['POST'])
def runCode():
    """
    Run Cyclone code
    ---
    description: runing the code sent by users and return the result
    parameters:
      - name: id
        type: string
        required: true
        description: every new user will have an unique id or retrieve the previous id stored in the cookie
      - name: code
        type: string
        required: true
        description: the code that user wants to run
    responses:
      200:
        description: successfully run the Cyclone code or not
    """

    if not _get_user_id(): return _response_(False, const.ERROR_USER_ID, code=const.CODE_USER_ID)
    code = request.form.get(const.FIELD_USER_CODE)
    if code and id:
        path = _check_path()
        Path(path).write_text(code)
        result = subprocess.Popen([const.SPT_EX, const.PATH_PROJECT, path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = result.communicate()
        
        symbol = "Trace Generated"
        res = stdout.decode(sys.getdefaultencoding())
        if symbol not in res:
            return _response_(True, const.SUCCESS_REQ, data=res);
        else:
            # translate the local path into an <a> html tage and return
            for line in res.splitlines():
                if symbol in line:
                    kv = line.split(":")
                    if len(kv) < 2:
                        return _response_(False, const.ERROR_CYC_TRACE_RETURN, code=const.CODE_CYC_TRACE_RETURN)
                    else:
                        return _response_(True, const.SUCCESS_REQ, data=res.replace(kv[1], "<a href='/editor/file?path=" + kv[1] + "'>Trace file download</a>"))
    else: return _response_(False, const.ERROR_CODE_ETY, code=const.CODE_CODE_ETY)
        

@editor.route("/file", methods = ['GET'])
def send_trace_file():
    """
    Send trace file to users
    ---
    description: send trace file to users through the unique file path
    parameters:
      - name: id
        type: string
        required: true
        description: every new user will have an unique id or retrieve the previous id stored in the cookie
      - name: file
        type: string
        required: true
        description: the absolute trace file path produced by Cyclone
    responses:
      200:
        description: successfully send the trace file to the user
    """

    if not _get_user_id(): return _response_(False, const.ERROR_USER_ID, code=const.CODE_USER_ID)
    path = request.args.get(const.FIELD_FILE_PATH)
    if not path: return _response_(False, const.ERROR_FILE_NOT_EXIST, code=const.CODE_FILE_NOT_EXIST)
    try: 
        return send_file(path, as_attachment=False)
    except Exception as e:
        # check if the trace file is sent successfully
        none


@editor.route('/upload', methods = ['POST'])
def upload():
    """
    User the code from the file to cover with the local code
    ---
    description: User the code from the file uploaded by user to replace the local code
    parameters:
      - name: id
        type: string
        required: true
        description: every new user will have an unique id or retrieve the previous id stored in the cookie
      - name: file
        type: file
        required: true
        description: the file provided by user's device
    responses:
      200:
        description: successfully replace the local code
    """
    
    if not _get_user_id(): return _response_(False, const.ERROR_USER_ID, code=const.CODE_USER_ID)
 
    # check if the post request has the file part
    if const.FIELD_FILE in request.files: file = request.files[const.FIELD_FILE]
    else: return _response_(False, const.ERROR_FILE_NOT_EXIST, code=const.CODE_FILE_NOT_EXIST)
    
    # If the user does not select a file, the browser submits an empty file without a filename.
    if file.filename == '': 
        return _response_(False, const.ERROR_FILE_NAME_ETY, code=const.CODE_FILE_NAME_ETY)
    if file and _allowed_file(file.filename):
        path_org = _check_path()
        path = os.path.join(const.PATH_TMP_STORAGE + os.sep + _get_user_id(), secure_filename(file.filename))
        file.save(path)
        code = Path(path).read_text()
        os.remove(path)
        Path(path_org).write_text(code)
        return _response_(True, const.SUCCESS_REQ_UPDATE, data=code)
    else:
        return _response_(False, const.ERROR_FILE_UPDATE, code=const.CODE_FILE_UPDATE)


@editor.route('/save2LocalFile', methods = ['POST'])
def downLoadFile():
    """
    Download the local code
    ---
    description: Download the local code
    parameters:
      - name: id
        type: string
        required: true
        description: every new user will have an unique id or retrieve the previous id stored in the cookie
      - name: code
        type: string
        required: true
        description: the code provided by user's online IDE
    responses:
      200:
        description: successfully Download the local code
    """

    if not _get_user_id(): return _response_(False, const.ERROR_USER_ID, code=const.CODE_USER_ID)
 
    code = request.form.get(const.FIELD_USER_CODE)
    if code:
        path = _check_path()
        Path(path).write_text(code)
        return send_file(path, download_name=const.DEFAULT_FILE_NAME, as_attachment=True)
    else:  return _response_(False, const.ERROR_CODE_ETY, code=const.CODE_CODE_ETY)


@editor.route("/examples", methods = ['POST'])
def getExamplesList():
    """
    Show examples from the Cyclone folder
    ---
    description: Show every example from the Cyclone folder in light of its structure
    parameters:
      - name: id
        type: string
        required: true
        description: every new user will have an unique id or retrieve the previous id stored in the cookie
    responses:
      200:
        description: successfully return the structure of examples
    """
    
    if not _get_user_id(): return _response_(False, const.ERROR_USER_ID, code=const.CODE_USER_ID)
 
    structure = {}
    if Path(const.PATH_EXAMPLE).exists():
        for path, dirs, files in os.walk(const.PATH_EXAMPLE):
            if path != const.PATH_EXAMPLE:
                s_folder = path.split(os.sep)[-1]
                if s_folder and len(files) > 0:
                    structure[s_folder] = files
                    structure[s_folder].sort()
    return _response_(True, const.SUCCESS_REQ, data=structure)


@editor.route("/example", methods = ['POST'])
def getExample():
    """
    Get the code from a example in the Cyclone folder
    ---
    description: Read the code from a specific example
    parameters:
      - name: id
        type: string
        required: true
        description: every new user will have an unique id or retrieve the previous id stored in the cookie
      - name: file
        type: string
        required: true
        description: the file name
      - name: folder
        type: string
        required: true
        description: the folder name
    responses:
      200:
        description: successfully return the code from a example in the Cyclone folder
    """
    
    if not _get_user_id(): return _response_(False, const.ERROR_USER_ID, code=const.CODE_USER_ID)

    file = request.form.get(const.FIELD_FILE)
    folder = request.form.get(const.FIELD_FOLDER)
    # TODO verify the data
    if file and folder:
        code = Path(const.PATH_EXAMPLE + os.sep + folder + os.sep + file).read_text()
        return _response_(True, const.SUCCESS_REQ, data=code)
    else: return _response_(False, const.ERROR_FILE_NOT_EXIST, code=CODE_FILE_NOT_EXIST)