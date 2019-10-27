from flask import Flask, request #Imports the Flask package
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid

#databases
from sqlalchemy import create_engine


#database setting up
# Create an engine to communicate with the database. The
# "cockroachdb://" prefix for the engine URL indicates that we are
# connecting to CockroachDB using the 'cockroachdb' dialect.
engine = create_engine(
    'cockroachdb://bk:123@aws-us-east-1.easyslip-1.crdb.io:26257/easyslipdb?sslmode=verify-full&sslrootcert=/Users/frenielzabala/projects/easyslip/backend/easyslip-1-ca.crt',
    echo=True   
)

app = Flask(__name__)
CORS(app)
# @app.route('/', methods=['GET', 'POST'])
# def allowed_file(filename):
#     return '.' in filename and \filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        pdf_file = request.files['permission_slip']
        csv_file = request.files["csv_file"]
        
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     return redirect(url_for('uploaded_file',
        #                             filename=filename))

        uniq_pdf_name = str(uuid.uuid4())
        uniq_csv_name = str(uuid.uuid4())
        pdf_name = secure_filename(pdf_file.filename)
        pdf_file.save(os.path.join("static/documents", uniq_pdf_name))
        csv_name = secure_filename(csv_file.filename)
        csv_file.save(os.path.join("static/csv_files", uniq_csv_name))

        # TODO: make unique id for document and csv
        # store the information to the database

    return {"msg": "sent"}

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
