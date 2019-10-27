#get: get info about the slip sent
#return dict, no info

#post: route for those who post pdf/csv (how do i actually post pdf)
#more work

#client interaction with the server; CLIENT
#get/post = rest api frameworks; between web app and backend
#flask runs on server; recieves
#web app/front end; sends get/post requests

#envelope is pdf to each recipient
#GET = web browser get info from server
#POST = user input into browser, browers posts info to server
#NOT IN ANY order
#Can be mismatched and used multiple

from flask import Flask #Imports the Flask package
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def allowed_file(filename):
    return '.' in filename and \filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    

def upload_file():
    if request.method == 'POST':
        #check if post request has file
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        #if user does not select file, browser also submit an em
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))


if __name__ == '__main__':
    app.run(debug=True)
