from google import genai

client = genai.Client(api_key="AIzaSyAjt53_dGsfjDQUdkRwuAIvW6ED4yg9H88")

sample_answers = {}

def generate_interview_questions(job_role, interview_type, duration, resume):
    global sample_answers  # So we can update the dictionary

    if duration == 5:
        num_questions = 2
    elif duration == 10:
        num_questions = 6
    else:
        num_questions = 5  # Default if no match

    prompt = f"""
    Just Generate {num_questions} interview questions for a {job_role}.
    Type: {interview_type}.
    Based on the skills and projects in this resume content:
    {resume}.
    For each question, also provide a short sample answer (clear, professional, and not too long).
    Format like:
    Q: [question here]
    A: [sample answer here]
    (Note: No extra text, just questions with sample answers)
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    content = response.text.strip().split('\n')
    questions = []
    sample_answers = {}

    current_question = None
    for line in content:
        line = line.strip()
        if line.startswith('Q:'):
            current_question = line[2:].strip()
            questions.append(current_question)
        elif line.startswith('A:') and current_question:
            answer = line[2:].strip()
            sample_answers[current_question] = answer
            current_question = None

    return questions[:num_questions]

def generate_feedback(answer):
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"Provide feedback on the following interview answer(just short and simple in one line and to the point) and correct grammatical errors and correct the format of it: '{answer}'"
    )
    return response.text

def get_sample_answer_for_question(question):
    return sample_answers.get(question, "No sample answer available.")
