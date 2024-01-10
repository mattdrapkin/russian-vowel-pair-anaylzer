# app.py
from flask import Flask, render_template, request, send_file, session
from analyze import analyze_non_contiguous, analyze_contiguous

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    text = request.form.get('user_input', '')
    n_highlighted_result, n_combo_freq, n_combo_line_num = analyze_non_contiguous(text)
    highlighted_result, combo_freq, combo_line_num = analyze_contiguous(text)

    # Sort frequency table in descending order of frequencies
    n_combo_freq = dict(sorted(n_combo_freq.items(), key=lambda item: item[1], reverse=True))
    combo_freq = dict(sorted(combo_freq.items(), key=lambda item: item[1], reverse=True))

    # Display the processed text with highlighting on the /process endpoint
    return render_template('process.html', non_contig_result=n_highlighted_result,
                           contig_result=highlighted_result,
                           non_contig_occurances=sum(n_combo_freq.values()),
                           contig_occurances=sum(combo_freq.values()),
                           n_combo_freq=n_combo_freq, combo_freq=combo_freq,
                           n_combo_line_num=n_combo_line_num, combo_line_num=combo_line_num)


@app.route('/save_to_html', methods=['POST'])
def save_to_html():
    text_input = request.form.get('text_input', '')

    # Save the text to an HTML file
    file_path = 'output.html'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(
            f'<html><head><title>Output HTML</title></head><body><pre>{text_input}</pre></body></html>')

    # Send the file as an attachment for download
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
