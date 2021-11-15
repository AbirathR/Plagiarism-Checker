#import libraries
import os
from flask import Flask, render_template, request
from send_email import send_email
from werkzeug.utils import secure_filename
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import PDFObjectNotFound
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator

#folder creation
UPLOAD_FOLDER = 'C:\plagz'
ALLOWED_EXTENSIONS = {'pdf'}

base_path = "C:/plagz/"
password = ""


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#into the website
@app.route("/")
def index():
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#storing the files to folder
@app.route("/success",methods=['GET','POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #file 2
        if 'file2' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file2 = request.files['file2']

        if file2.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file2 and allowed_file(file2.filename):
            filename = secure_filename(file2.filename)
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #files collected
        for file in os.listdir(base_path):
            if file.endswith(".pdf"):
                fp = open(base_path+file, "rb")
                parser = PDFParser(fp)
                document = PDFDocument(parser, password)
                if not document.is_extractable:
                    raise PDFTextExtractionNotAllowed
                rsrcmgr = PDFResourceManager()
                laparams = LAParams()
                device = PDFPageAggregator(rsrcmgr, laparams=laparams)
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                for page in PDFPage.create_pages(document):
                    interpreter.process_page(page)
                    layout = device.get_result()
                    for lt_obj in layout:
                        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                            extracted_text = ""
                            extracted_text += lt_obj.get_text()


                    txtfile = open(base_path+file[:-4]+".txt",'w')
                    with open(base_path+file[:-4]+".txt", "wb") as my_log:
                        my_log.write(extracted_text.encode("utf-8"))
                        
                    fp.close()

        student_files = [doc for doc in os.listdir('C:\\plagiarism') if doc.endswith('.txt')]
    student_notes =[open(base_path+File).read() for File in  student_files]
    vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
    similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])
    vectors = vectorize(student_notes)
    s_vectors = list(zip(student_files, vectors))
    def check_plagiarism():
        plagiarism_results = set()
        global s_vectors
        for student_a, text_vector_a in s_vectors:
            new_vectors =s_vectors.copy()
            current_index = new_vectors.index((student_a, text_vector_a))
            del new_vectors[current_index]
        for student_b , text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            student_pair = sorted((student_a, student_b))
            score = (student_pair[0], student_pair[1],sim_score)
            plagiarism_results.add(score)
        return plagiarism_results
    for data in check_plagiarism():
        print(data)
        send_email(email)
    return render_template("thanks.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
