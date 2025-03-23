from flask import Flask, request, render_template, jsonify
import subprocess
import os

app = Flask(__name__)

# Directory for uploaded files
UPLOAD_FOLDER = "dirr"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
PROFILE_SCRIPT_PATH="../user_data_to_profile/user_data_to_profile.py"
PROFILE_UPLOAD_FOLDER="../user_data_to_profile"

n_json_path = "profiles_user/n.json"
if os.path.exists(n_json_path):
    os.remove(n_json_path)
    print("n.json removed successfully")

@app.route("/")
def index():
    return render_template("index.html")  # Loads the frontend

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    user = request.form.get("user", "Unknown_User")

    if file.filename == "":
        return "No selected file", 400

    # Empty the folder before uploading the new file
    for filename in os.listdir(app.config["UPLOAD_FOLDER"]):
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)


    # Save file with user prefix
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], f"{file.filename}")
    file.save(filepath)
    
    # Run the newmain.py script with the user argument
    os.system(f"python newmain.py {user}")
    return "Uploaded"

@app.route('/results')
def show_results():
    try:
        with open('output.txt', 'r', encoding="utf-8") as f:
            output_content = f.read()
        return render_template("results.html", output=output_content)
    except FileNotFoundError:
        return render_template("results.html", output="Output file not found. The process may have failed.")
    

@app.route("/uploadprofile", methods=["POST"])  # Changed endpoint
def upload_profile():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = os.path.join(PROFILE_UPLOAD_FOLDER, "user_data_example.txt")
    file.save(file_path)

    return jsonify({"message": "File uploaded successfully", "file_path": file_path})

@app.route("/run-script", methods=["POST"])
def run_script():
    try:
        result = subprocess.run(["python", PROFILE_SCRIPT_PATH], capture_output=True, text=True)
        return jsonify({"output": result.stdout, "error": result.stderr})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/checkfile")
def check_file():
    filename = request.args.get("filename")
    file_path = os.path.join("profiles_user", filename)

    return jsonify({"exists": os.path.exists(file_path)})

if __name__ == "__main__":
    app.run(debug=True)
