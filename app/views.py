from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_from_directory, jsonify
from .ai import generate_interview_questions, generate_feedback, get_sample_answer_for_question, client
from .utils import extract_text_from_pdf
from . import mongo, bcrypt
from datetime import datetime
import os

main_bp = Blueprint('main', __name__,static_folder='static',    static_url_path='/main_static')

@main_bp.route('/')
def home():
    user_email = session.get('user')
    return render_template('index.html', logged_in=bool(user_email), email=user_email)


@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            return "Passwords do not match"

        existing_user = mongo.db.users.find_one({'email': email})
        if existing_user:
            return "User already exists"

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        mongo.db.users.insert_one({'email': email, 'password': hashed_pw})
        return redirect(url_for('main.login'))

    return render_template('signup.html')


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = mongo.db.users.find_one({'email': email})

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user'] = email
            return redirect(url_for('main.home'))
        return "Invalid credentials"

    return render_template('login.html')


@main_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.home'))


@main_bp.route('/history')
def history():
    if 'user' not in session:
        return redirect(url_for('main.login'))

    user_email = session['user']
    # Use the new collection 'interview_results'
    history_records = list(mongo.db.interview_results.find({'user': user_email}).sort('timestamp', -1))

    return render_template('history.html', history=history_records)


@main_bp.route('/download_feedback/<filename>')
def download_feedback(filename):
    if 'user' not in session:
        return redirect(url_for('main.login'))

    user_email = session['user']
    feedback_dir = os.path.join('static', 'feedbacks', user_email)
    return send_from_directory(feedback_dir, filename, as_attachment=True)


@main_bp.route('/start_interview', methods=['POST'])
def start_interview():
    job_role = request.form.get('job_role')
    interview_type = request.form.get('interview_type')
    duration = int(request.form.get('duration'))
    resume = request.files.get('resume')

    if not job_role or not interview_type or not duration or not resume:
        return jsonify({'error': 'Missing required fields'}), 400

    # ✅ Store in session
    session['job_role'] = job_role
    session['interview_type'] = interview_type
    session['duration'] = duration

    resume_text = extract_text_from_pdf(resume)
    questions = generate_interview_questions(job_role, interview_type, duration, resume_text)

    session_data = [
        {
            'question': q,
            'answer': '',
            'feedback': '',
            'sample_answer': get_sample_answer_for_question(q)
        }
        for q in questions
    ]

    return jsonify({'questions': session_data})



@main_bp.route('/submit_answers', methods=['POST'])
def submit_answers():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    answers = data.get('answers')
    questions = data.get('questions')

    # ✅ Get from Flask session
    job_role = session.get('job_role')
    interview_type = session.get('interview_type')
    duration = session.get('duration')
    user_email = session['user']

    feedback_list = []
    combined_text = ""

    for idx, answer in enumerate(answers):
        question = questions[idx]
        feedback = generate_feedback(answer)
        sample_answer = get_sample_answer_for_question(question)

        feedback_list.append({
            'question': question,
            'answer': answer,
            'feedback': feedback,
            'sample_answer': sample_answer
        })

        combined_text += f"Q: {question}\nA: {answer}\n"

    overall_prompt = f"Give a short, professional overall feedback for this interview based on all the answers:\n{combined_text}"
    overall_response = client.models.generate_content(model="gemini-1.5-flash", contents=overall_prompt)
    overall_feedback = overall_response.text.strip()

    mongo.db.interview_results.insert_one({
        'user': user_email,
        'job_role': job_role,
        'interview_type': interview_type,
        'duration': duration,
        'questions_feedback': feedback_list,
        'overall_feedback': overall_feedback,
        'timestamp': datetime.utcnow()
    })

    return jsonify({
        'feedback': feedback_list,
        'overall_feedback': overall_feedback
    })
