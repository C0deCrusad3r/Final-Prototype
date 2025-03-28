from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

csv1_path = "/home/hardik/Projects/python-rmf/GpaData.csv"
csv2_path = "/home/hardik/Projects/python-rmf/AttachmentHUM_1071_-_08-2025.csv"

def find_roommates(name):
    name = name.strip().lower()
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)

    # Standardize column names
    df1['Name'] = df1['Name'].str.strip().str.lower()
    df2['Name'] = df2['Name'].str.strip().str.lower()

    # Find user's registration number in df2
    student_row = df2[df2['Name'] == name]
    if student_row.empty:
        return "Student not found. Check the name."

    reg_no = str(student_row.iloc[0]['Registration No']).strip()

    # Find all instances of this registration number in df1
    matched_students = df1[df1['Registration No'].astype(str).str.strip() == reg_no]
    if matched_students.empty:
        return "No matching registration number found."

    # Extract all registration numbers associated with the same name
    roommate_reg_nos = df1[df1['Name'] == matched_students.iloc[0]['Name']]['Registration No'].astype(str).str.strip().tolist()
    roommate_reg_nos = [r for r in roommate_reg_nos if r != reg_no]

    # Find the names of these registration numbers from df2
    roommates = df2[df2['Registration No'].astype(str).str.strip().isin(roommate_reg_nos)]
    roommate_details = [f"{row['Name'].title()} (Reg No: {row['Registration No']})" for _, row in roommates.iterrows()]

    if not roommate_details:
        return "No roommates found."

    return "Roommates found: " + ", ".join(roommate_details)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        name = request.form['name']
        result = find_roommates(name)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
