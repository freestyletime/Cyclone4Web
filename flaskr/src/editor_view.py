import os, subprocess, sys, time
from ..config import const
from flask import Blueprint, request, render_template, jsonify, make_response
from pathlib import Path

# = = = = = = = = = = = = = = = = = =
def current_milli_time():
    return str(round(time.time() * 1000))
# = = = = = = = = = = = = = = = = = =


editor = Blueprint("editor", __name__, url_prefix="/editor")


@editor.route("/index", methods = ['GET'])
def setCode():
    id = request.cookies.get('unique_user_id')
    if id:
        parent = const.PATH_TMP_STORAGE + os.sep + id
        code = Path(parent + os.sep + const.DEFAULT_FILE_NAME).read_text()
        return render_template('index.html', code=code)
    else:
        code = Path(const.PATH_TMP_STORAGE + os.sep + const.DEFAULT_FILE_NAME).read_text()
        res = make_response(render_template('index.html', code=code))
        res.set_cookie('unique_user_id', current_milli_time())
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
    result = subprocess.Popen(["javac", path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = result.communicate()
    if not stdout:
        result = subprocess.Popen(["java", "-classpath", parent, const.DEFAULT_FILE_NAME.split(".java")[0]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = result.communicate()
    return jsonify({"response": stdout.decode(sys.getdefaultencoding())})

@editor.route("/examples", methods = ['POST'])
def getExamplesList():
    structure = {}
    for path, dirs, files in os.walk(const.PATH_EXAMPLE):
        s_folder = path.split(os.sep)[-1]
        if s_folder:
            structure[s_folder] = []
            for name in files:
                structure[s_folder].append(name)
            structure[s_folder].sort()

    return jsonify({"examples": structure})

@editor.route("/example", methods = ['POST'])
def getExample():
    folder = request.form.get('parent')
    name = request.form.get('name')
    # TODO verify the data
    code = Path(const.PATH_EXAMPLE + os.sep + folder + os.sep + name).read_text()
    return jsonify({"code": code})
