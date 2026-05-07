from flask import Flask, render_template, request
import boto3

app = Flask(__name__)

# S3 client
s3 = boto3.client('s3')

BUCKET_NAME = "mn-data-bucket"

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# Function to check allowed file
def allowed_file(filename):

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Home page
@app.route('/')
def home():
    return render_template("app.html")


# Upload route
@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['file']

    # Check if file selected
    if file.filename == '':
        return "No File Selected"

    # Check image extension
    if file and allowed_file(file.filename):

        # Upload to S3
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)

        # Generate image URL
        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file.filename}"

        # Send URL to HTML
        return render_template("app.html", image_url=file_url)

    return "Only PNG, JPG, JPEG files are allowed!"


# Run Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
