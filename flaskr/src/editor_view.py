import subprocess, sys
from flask import Blueprint, request, render_template, jsonify
from pathlib import Path

editor = Blueprint("editor", __name__, url_prefix="/editor")

@editor.route("/index", methods = ['GET'])
def setCode():
    code = Path("Main.java").read_text()
    return render_template('index.html', code=code)

@editor.route("/run", methods = ['POST'])
def runCode():
    code = request.form.get('code')
    Path("Main.java").write_text(code)
    result = subprocess.Popen(["javac", "Main.java"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = result.communicate()
    if not stdout:
        result = subprocess.Popen(["java", "Main"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = result.communicate()
    return jsonify({"response": stdout.decode(sys.getdefaultencoding())})
