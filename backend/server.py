from flask import Flask, request #Imports the Flask package
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
from pymongo import MongoClient

#databases
client = MongoClient('localhost', 27017)
db = client['easy-slip-database']

app = Flask(__name__)
CORS(app)
# @app.route('/', methods=['GET', 'POST'])
# def allowed_file(filename):
#     return '.' in filename and \filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/upload', methods=['POST'])
def upload():
    pdf_file = request.files['permission_slip']
    csv_file = request.files["csv_file"]
    
    uniq_pdf_name = str(uuid.uuid4())
    uniq_csv_name = str(uuid.uuid4())
    pdf_name = secure_filename(pdf_file.filename)
    pdf_file.save(os.path.join("static/documents", uniq_pdf_name))
    csv_name = secure_filename(csv_file.filename)
    csv_file.save(os.path.join("static/csv_files", uniq_csv_name))

        # TODO: make unique id for document and csv
        # store the information to the database
    #collection of permission_slip drafts
    slip = {
        "pdf": uniq_pdf_name,
        "csv": uniq_csv_name,
        "name": "example_name"
    }
    slips = db.slips
    slip_id = slips.inserte_one(slip).inserted_id
    return {"msg": slip_id}

@app.route('/slips', methods= ['GET'])
def slips():
    return {"msg": "eiqpweirw"}

# TODO: add a route to actually send stuff

@app.route('/signers', methods=['GET'])
def signers():
    '''
    should get the parents, student, and permission slip status and return it

    '''
    return {"msg": "it works"}

if __name__ == '__main__':
    app.run(debug=True)
