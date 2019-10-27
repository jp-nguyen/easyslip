from flask import Flask, request, jsonify #Imports the Flask package
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
from pymongo import MongoClient
from os import path
import csv
from docusign_tooling import send_slip_worker, get_docusign_credentials
from dotenv import load_dotenv

load_dotenv()
#paths
pdf_path = path.abspath(path.join(path.dirname(path.realpath(__file__)), os.getenv("DOCUMENT_PATH")))
csv_path = path.abspath(path.join(path.dirname(path.realpath(__file__)), os.getenv("CSV_PATH")))

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
    
    uniq_pdf_name = str(uuid.uuid4())+ ".pdf"
    uniq_csv_name = str(uuid.uuid4()) + ".csv"
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
        "sent": False
    }

    slips = db.slips
    slip_id = slips.insert_one(slip).inserted_id   
    return {
        "pdf": uniq_pdf_name,
        "csv": uniq_csv_name,
        "id": str(slip_id),
    }

@app.route('/slips', methods= ['GET'])
def slips():
    slips = db.slips
    result = []
    for slip in slips.find({}):
        slip["_id"] = str(slip["_id"])
        result.append(slip)

    return {"slips": result}


@app.route('/slips/<slip_id>')
def sendSlip(slip_id, methods= ['GET']):
    
    
    slip = pymongo.find({"_id": slip_id})
    fullname = path.join(csv_path, slip["csv"])
    cred_info = get_docusign_credentials()
    
    input_file = csv.DictReader(open(slip["csv"]))
    for row in input_file:
        env_info = {
            "signer_email":row["parent_email"],
            "signer_name": row["parent_name"],
            "status": "sent",
            "child_name": row["student_name"]
        }
        document_name = path.join(pdf_path, slip["pdf"])
        send_slip_worker(cred_info, env_info, document_name)
    return {"msg": "envelops sent"}

@app.route('/signers', methods=['GET'])
def signers():
    '''
    should get the parents, student, and permission slip status and return it

    '''
    return {"msg": "it works"}

if __name__ == '__main__':
    app.run(debug=True)
