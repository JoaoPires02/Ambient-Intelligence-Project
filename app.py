from flask import Flask, request, render_template, session, send_from_directory, redirect, url_for, jsonify
import os
import classroom_controller

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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

@app.route('/ask-question', methods=['POST'])
def send_question():
    if 'question_asked' in request.form:
        question = request.form['question_asked']
        sender = request.form['sender_select']
        if sender == "non_anonymous":
            classroom_controller.web_command = 'question '+ session["studentID"] + ' ' + question
        elif sender == "anonymous":
            classroom_controller.web_command = 'question '+ "Anonymous" + ' ' + question
        classroom_controller.new_web_command = True
    return redirect(url_for('room123student'))

@app.route('/update-temperature', methods=['POST'])
def update_temperature():
    if 'teacher_temp' in request.form:
        new_temp = request.form['teacher_temp']
        classroom_controller.web_command = 'temp '+ new_temp
        classroom_controller.new_web_command = True
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

@app.route('/get-break-votes')
def get_break_votes():
    break_votes = classroom_controller.get_break_votes_percent()
    return jsonify({'break_votes': break_votes})

@app.route('/vote-temp-increase', methods=['POST'])
def vote_temp_increase():
    # Vote to increase temperature
    classroom_controller.web_command = 'vote ' + session["studentID"] + ' temp+'
    classroom_controller.new_web_command = True
    return jsonify({'success': True})

@app.route('/vote-temp-decrease', methods=['POST'])
def vote_temp_decrease():
    # Vote to decrease temperature
    classroom_controller.web_command = 'vote ' + session["studentID"] + ' temp-'
    classroom_controller.new_web_command = True
    return jsonify({'success': True})


@app.route('/vote-break-poll', methods=['POST'])
def vote_break_poll():
    # Reset the poll votes
    classroom_controller.web_command = 'vote ' + session["studentID"] + ' break'
    classroom_controller.new_web_command = True
    return jsonify({'success': True})

@app.route('/vote-poll', methods=['POST'])
def vote_poll():
    # Vote to poll
    classroom_controller.web_command = 'vote ' + session["studentID"] + ' poll'
    classroom_controller.new_web_command = True
    return jsonify({'success': True})

@app.route('/reset-votes', methods=['POST'])
def reset_votes():
    # Reset the votes
    print(session['studentID'])
    classroom_controller.web_command = 'vote reset poll'
    classroom_controller.new_web_command = True
    return jsonify({'success': True})

@app.route('/reset-break-votes', methods=['POST'])
def reset_break_votes():
    # Reset the break votes
    classroom_controller.web_command = 'vote reset break'
    classroom_controller.new_web_command = True
    return jsonify({'success': True})

@app.route('/get-attendance-list')
def get_attendance_list():
    names = list(classroom_controller.students.values()) 
    return jsonify({'students': names})

@app.route('/get-questions')
def get_questions():
    questions = classroom_controller.questions 
    return jsonify({'questions': questions})

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
    session['studentID'] = student_id
    students_ids = list(classroom_controller.students.keys())
    if classroom_code == '123':
        if student_id in students_ids:
            ind = students_ids.index(student_id)
            classroom_controller.student_present[ind] = True
            return redirect(url_for('room123student'))
        elif student_id == 't':
            return redirect(url_for('room123teacher'))
        else:
            return render_template('index2.html', invalid_student_id=True)
    elif student_id in students_ids:
        return render_template('index2.html', invalid_classroom_code=True)
    else:
        return render_template('index2.html', invalid_classroom_code=True, invalid_student_id=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)