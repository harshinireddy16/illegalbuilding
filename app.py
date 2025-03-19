from werkzeug.utils import secure_filename
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
app = Flask(__name__)

# Define where to store uploaded images
UPLOAD_FOLDER = 'dataset'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions for images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to check building compliance (you can customize this logic)
def check_compliance(old_image_path, new_image_path):
    is_compliant = True
    errors = []

    # Example compliance checks (these are just placeholder checks)
    new_building_floors = 6
    max_floors = 5

    if new_building_floors > max_floors:
        is_compliant = False
        errors.append(f"New building has {new_building_floors} floors, which exceeds the allowed maximum of {max_floors}.")

    return is_compliant, errors

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_compliance', methods=['POST'])
def check_compliance_page():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'old_image' not in request.files or 'new_image' not in request.files:
            return "No file part"

        old_image = request.files['old_image']
        new_image = request.files['new_image']

        # If no image is selected by the user
        if old_image.filename == '' or new_image.filename == '':
            return "No selected file"

        # Save old image
        if old_image and allowed_file(old_image.filename):
            old_filename = secure_filename(old_image.filename)
            old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], old_filename)
            old_image.save(old_image_path)
        else:
            return "Invalid old image file type"

        # Save new image
        if new_image and allowed_file(new_image.filename):
            new_filename = secure_filename(new_image.filename)
            new_image_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            new_image.save(new_image_path)
        else:
            return "Invalid new image file type"

        # Check compliance (you can add more detailed logic here)
        is_compliant, errors = check_compliance(old_image_path, new_image_path)

        # Render the result page with the check result
        return render_template('result.html', is_compliant=is_compliant, errors=errors,
                               old_image_path=old_image_path, new_image_path=new_image_path)

if __name__ == '__main__':
    # Create dataset folder if it doesn't exist
    if not os.path.exists('dataset'):
        os.makedirs('dataset')
    
    app.run(debug=True)
