from flask import Flask, request, render_template, send_from_directory, redirect, url_for, jsonify
import os
import classroom_controller

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

@app.route('/get-simulated-temp')
def get_simulated_temp():
    temp = classroom_controller.sim_temp
    return jsonify({'temp': temp})


@app.route('/get-attendance-list')
def get_attendance_list():
    names = list(classroom_controller.students.values()) 
    return jsonify({'students': names})

@app.route('/get-presences')
def get_presences():
    presences = list(classroom_controller.student_present)
    presences_str = [] 
    for i in presences:
        if i == False:
            presences_str += ["Missing"]
        elif i == True:
            presences_str += ["Present"]
    print(classroom_controller.student_present)
    return jsonify({'presences': presences_str})


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
        students_ids = list(classroom_controller.students.keys())
        print(students_ids)
        print(school_code)
        if school_code in students_ids:
            ind = students_ids.index(school_code)
            classroom_controller.student_present[ind] = True
            return redirect(url_for('room123student'))
        elif school_code == 't':
            return redirect(url_for('room123teacher'))
    else:
        # Redirect to some other page if the classroom code is not 12345
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False)