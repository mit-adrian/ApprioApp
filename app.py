from flask import Flask, render_template, request, redirect, url_for, session, make_response
import os
import json
import csv
import io
from mining.apriori import run_association_rule_mining

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def index():
    return render_template('index.html', show_quick_links=True, show_tips=False)

@app.route('/process')
def process():
    return render_template('process.html', show_quick_links=False, show_tips=True)

@app.route('/results')
def results():
    rules_json = session.get('rules')
    rules = json.loads(rules_json) if rules_json else []
    return render_template(
        'results.html', 
        rules=rules,
        show_quick_links=False, 
        show_tips=False
        )

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['dataset']
    min_support = float(request.form.get('min_support', 0.4))
    min_confidence = float(request.form.get('min_confidence', 0.6))
    min_threshold = float(request.form.get('min_threshold', 2.0))

    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        rules = run_association_rule_mining(filepath, min_support, min_confidence, min_threshold)

        session['rules'] = json.dumps(rules)

        return redirect(
            url_for('results')
        )

    return "Invalid file format. Please upload a CSV."

from flask import send_from_directory

@app.route('/download-sample')
def download_sample():
    return send_from_directory(
        directory='static',
        path='sample.csv',
        as_attachment=True
    )

from flask import send_file

@app.route('/download_results')
def download_results():
    # FIX: Parse JSON string into list of dictionaries
    rules_json = session.get('rules', '[]')
    rules = json.loads(rules_json)

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(["Antecedent", "Consequent", "Support", "Confidence", "Lift"])

    # Write data rows
    for rule in rules:
        writer.writerow([
            ', '.join(rule['antecedents']),  # assuming these are lists
            ', '.join(rule['consequents']),
            f"{rule['support']:.2f}",
            f"{rule['confidence']:.2f}",
            f"{rule['lift']:.2f}",
        ])

    # Clear the rules from the session
    session.pop('rules', None)

    # Return response
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=association_rules.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response






if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
