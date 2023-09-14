from flask import Flask, render_template,jsonify,request
from werkzeug.utils import secure_filename
from ok import ans_llm
import os
#from upload_pinecone import up_pine
from wtforms.validators import InputRequired
UPLOAD_FOLDER="E:\test-main\save"
ALLOWED_EXTENSION=set(['pdf','html','doc'])

def allowed_filename(filename):
     return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSION
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def main():
    return 'Homepage'

@app.route("/upload" , methods=['GET', 'POST'])
def uploader():
    if 'file' in request.files:
        return jsonify({'error': 'file not provided'}),400
    file=request.files['file']
    if file.filename=='':
        return jsonify({'error': 'no file selected'}),400
    if file and allowed_filename(file.filename):
        filename = secure_filename(file.filename)

        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    return jsonify({'msg': 'file succesfully'}),400

@app.route("/chatbot/<string:input>")
def response(input):
    # user_input=request.args.get('input')
    aa=ans_llm(input)
    result={
        'query':input,
        "answer":aa
    }
    return jsonify(result)



#Response=namedtuple('Response', 'Response_score')

    
if __name__ == '__main__':
    app.run(debug=True)