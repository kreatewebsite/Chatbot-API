from flask import Flask, render_template,jsonify,request
from flask_cors import CORS
from ok import ans_llm
import os, gdown

#from upload_pinecone import up_pine

app = Flask(__name__)
CORS(app)

@app.route('/')
def main():
    return 'Homepage'

@app.route("/upload" , methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        file = request.form.get('url')
        
        slides = []
        file_names = []
        try:
            if url.split('/')[-1] == '?usp=sharing':
                url= url.replace('?usp=sharing','')
            gdown.download_folder(url)
            for dir,_,files in os.walk(os.getcwd()):
                for file in files :
                    if file.lower().endswith(('.pdf','.html','docx')):
                            pptx = os.path.join(dir,file)
                            slides.append(pptx)
                            file_names.append(file)
    
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        

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