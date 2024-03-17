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

@app.route('/update-temperature', methods=['POST'])
def update_temperature():
    if 'teacher_temp' in request.form:
        new_temp = request.form['teacher_temp']
        classroom_controller.web_command = 'temp '+ new_temp
        classroom_controller.new_web_command = True
    print(classroom_controller.ideal_temp)
    return redirect(url_for('room123teacher'))

@app.route('/update-light', methods=['POST'])
def update_light():
    data = request.json
    light_nr = data.get('light_nr')
    state = data.get('state')
    classroom_controller.web_command = 'light ' + light_nr + ' ' + state
    classroom_controller.new_web_command = True
    return redirect(url_for('room123teacher'))

@app.route('/update-proj', methods=['POST'])
def update_proj():
    data = request.json
    state = data.get('state')
    classroom_controller.web_command = 'proj ' + state
    classroom_controller.new_web_command = True
    return redirect(url_for('room123teacher'))


@app.route('/get-updated-votes')
def get_updated_votes():
    votes = classroom_controller.get_votes_percent()
    return jsonify({'votes': votes})

@app.route('/reset-votes', methods=['POST'])
def reset_votes():
    # Reset the votes
    classroom_controller.web_command = 'vote reset'
    classroom_controller.new_web_command = True
    return jsonify({'success': True})

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
    return jsonify({'presences': presences_str})


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/submit-codes', methods=['POST'])
def submit_codes():
    classroom_code = request.form['classroom_code']
    student_id = request.form['student_id']
    print(classroom_code)
    print(student_id)
    if classroom_code == '123':
        students_ids = list(classroom_controller.students.keys())
        print(students_ids)
        print(student_id)
        if student_id in students_ids:
            ind = students_ids.index(student_id)
            classroom_controller.student_present[ind] = True
            return redirect(url_for('room123student'))
        elif student_id == 't':
            return redirect(url_for('room123teacher'))
    else:
        # Redirect to some other page if the classroom code is not 12345
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=False)