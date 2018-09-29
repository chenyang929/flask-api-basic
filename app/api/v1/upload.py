import os
import uuid
from app.libs.tools import secure_filename
from flask import request, current_app, jsonify
from app.libs.redprint import Redprint

api = Redprint('upload')


@api.route('', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and _allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 因为上次的文件可能有重名，因此使用uuid保存文件
            file_name = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1]
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file_name))
            return jsonify({"msg": "success", "file_name": file_name})
        return jsonify({"msg": "failed"})
    return '''
    <!doctype html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
  <title>Upload new File</title>
  <h1>Upload new File</h1>
  <form action="" method=post enctype=multipart/form-data>
   <p><input type=file name=file>
     <input type=submit value=Upload>
  </form>
    '''


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOW_EXTENSIONS']
