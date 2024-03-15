from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/room123student')
def room123student():
    return render_template('room123student.html')

@app.route('/room123teacher')
def room123teacher():
    return render_template('room123teacher.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/submit-codes', methods=['POST'])
def submit_codes():
    classroom_code = request.form['classroom_code']
    school_code = request.form['school_code']
    print(classroom_code)
    print(school_code)    
    if classroom_code == '123':
        if school_code == '123':
            return redirect(url_for('room123student'))
        elif school_code == 't':
            return redirect(url_for('room123teacher'))
    else:
        # Redirect to some other page if the classroom code is not 12345
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)