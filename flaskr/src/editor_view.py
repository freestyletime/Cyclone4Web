import os, subprocess, sys, time
from ..config import const
from flask import Blueprint, request, render_template, jsonify, make_response, send_file
from pathlib import Path

# = = = = = = = = = = = = = = = = = =
### Native methods
def current_timestamp():
    return str(round(time.time() * 1000))
# = = = = = = = = = = = = = = = = = =

### Web interface
editor = Blueprint("editor", __name__, url_prefix="/editor")


@editor.route("/index", methods = ['GET'])
def setCode():
    id = request.cookies.get('unique_user_id')
    if id:
        parent = const.PATH_TMP_STORAGE + os.sep + id
        if Path(parent).exists():
            code = Path(parent + os.sep + const.DEFAULT_FILE_NAME).read_text()
            return render_template('index.html', code=code)
    
    code = Path(const.PATH_TMP_STORAGE + os.sep + const.DEFAULT_FILE_NAME).read_text()
    res = make_response(render_template('index.html', code=code))
    res.set_cookie('unique_user_id', current_timestamp())
    return res


@editor.route("/run", methods = ['POST'])
def runCode():
    code = request.form.get('code')
    id = request.form.get('user_id')
    # TODO verify the data
    parent = const.PATH_TMP_STORAGE + os.sep + id
    path = parent + os.sep + const.DEFAULT_FILE_NAME
    if not Path(parent).exists(): Path(parent).mkdir()
    if not Path(path).exists(): Path(path).touch()
    Path(path).write_text(code)
    result = subprocess.Popen(["./ex.sh", const.PATH_PROJECT, path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = result.communicate()
    return jsonify({"response": stdout.decode(sys.getdefaultencoding())})


@editor.route('/files', methods = ['POST'])
def downLoadFile():
    code = request.form.get('code')
    id = request.cookies.get('unique_user_id')
    # TODO verify the data
    parent = const.PATH_TMP_STORAGE + os.sep + id
    path = parent + os.sep + const.DEFAULT_FILE_NAME
    if not Path(parent).exists(): Path(parent).mkdir()
    if not Path(path).exists(): Path(path).touch()
    Path(path).write_text(code)
    return send_file(path, download_name=const.DEFAULT_FILE_NAME, as_attachment=True)


@editor.route("/examples", methods = ['POST'])
def getExamplesList():
    structure = {}
    if Path(const.PATH_EXAMPLE).exists():
        for path, dirs, files in os.walk(const.PATH_EXAMPLE):
            if path != const.PATH_EXAMPLE:
                s_folder = path.split(os.sep)[-1]
                if s_folder and len(files) > 0:
                    structure[s_folder] = files
                    structure[s_folder].sort()
    return jsonify({"examples": structure})


@editor.route("/example", methods = ['POST'])
def getExample():
    folder = request.form.get('folder')
    name = request.form.get('name')
    # TODO verify the data
    code = Path(const.PATH_EXAMPLE + os.sep + folder + os.sep + name).read_text()
    return jsonify({"code": code})
