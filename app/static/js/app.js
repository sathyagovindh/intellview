let questions = [];
let currentIndex = 0;
let answers = [];
let recognition;
let isRecognizing = false;
let finalTranscript = ''; // ✅ Moved to top-level scope


let hasSpokenQuestion = false; // <-- Added flag

// Function to speak a question once
function speakQuestion(questionText) {
    if (!hasSpokenQuestion) {
        const utterance = new SpeechSynthesisUtterance(questionText);
        speechSynthesis.speak(utterance);
        hasSpokenQuestion = true;
    }
}

// Initialize speech recognition API
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onstart = function () {
        isRecognizing = true;
    };

    recognition.onresult = function (event) {
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
            const transcript = event.results[i][0].transcript;

            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }

        document.getElementById('userAnswer').value = finalTranscript + interimTranscript;
    };

    recognition.onerror = function (event) {
        console.error("Speech recognition error:", event.error);
    };

    recognition.onend = function () {
        if (isRecognizing) {
            recognition.start();
            // ✅ Do NOT repeat the question here
        }
    };
}

// ✅ CAMERA + MIC FUNCTION
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        const video = document.getElementById('webcam');
        video.srcObject = stream;
        video.play();
        console.log('Camera and mic started successfully');
    } catch (err) {
        console.error('Camera/mic access error:', err);
        alert("Camera and microphone access are required to continue the interview.");
    }
}

function startSpeechRecognition() {
    if (recognition && !isRecognizing) {
        recognition.start();
    }
}


document.getElementById('get_start').addEventListener('click', async function () {
    document.getElementById('interviewForm').style.display = 'block';
    document.getElementById('home').style.display = 'none';
});


// ✅ FORM SUBMISSION
document.getElementById('interviewForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const formData = new FormData(this);

    const response = await fetch('/start_interview', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    questions = data.questions.map(q => q.question);
    currentIndex = 0;
    answers = [];

    document.getElementById('interviewForm').style.display = 'none';
    document.getElementById('questionContainer').style.display = 'block';
    document.getElementById('container').style.display = 'none';

    startCamera();
    startSpeechRecognition();
    showQuestion();
});

// ✅ DISPLAY QUESTION
function showQuestion() {
    const currentQuestion = questions[currentIndex];
    document.getElementById('currentQuestion').innerText = currentQuestion;

    const speech = new SpeechSynthesisUtterance(currentQuestion);
    window.speechSynthesis.speak(speech);
}

// ✅ NEXT BUTTON
document.getElementById('nextBtn').addEventListener('click', async function () {
    let answer = document.getElementById('userAnswer').value.trim();
    answers.push(answer || "No answer given");

    currentIndex++;

    if (currentIndex < questions.length) {
        // ✅ Reset transcript and textarea for next question
        finalTranscript = '';
        document.getElementById('userAnswer').value = '';
        showQuestion();
    } else {
        // ✅ Stop recognition after last question
        if (recognition && isRecognizing) {
            recognition.stop();
            isRecognizing = false;
        }
        await submitAnswers();
    }
});

// ✅ SUBMIT ANSWERS
async function submitAnswers() {
    const response = await fetch('/submit_answers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            answers: answers,
            questions: questions
        })
    });

    const data = await response.json();

    document.getElementById('questionContainer').style.display = 'none';
    document.getElementById('container').style.display = 'none';
    document.getElementById('feedbackContainer').style.display = 'block';

    let feedbackHtml = '';
    data.feedback.forEach((fb, idx) => {
        feedbackHtml += `<h3>Question ${idx + 1}: ${questions[idx]}</h3>`;
        feedbackHtml += `<p><strong>Your Answer:</strong> ${fb.answer}</p>`;
        feedbackHtml += `<p><strong>Feedback:</strong> ${fb.feedback}</p>`;
        feedbackHtml += `<p><strong>Sample Answer:</strong> ${fb.sample_answer}</p>`;
    });

    feedbackHtml += `<h2>Overall Interview Feedback</h2>`;
    feedbackHtml += `<p>${data.overall_feedback}</p>`;

    document.getElementById('feedbackList').innerHTML = feedbackHtml;
}
// In your app.js or a script tag at the end of the page:
document.addEventListener('DOMContentLoaded', () => {
  const downloadBtn = document.getElementById('downloadPdfBtn');
  const feedbackContainer = document.getElementById('feedbackContainer');

  downloadBtn.addEventListener('click', () => {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Get the entire HTML content inside feedbackContainer as plain text
    // or you can use innerText to preserve line breaks better
    const contentText = feedbackContainer.innerText || feedbackContainer.textContent;

    // Split the text into lines to fit PDF page width
    const lines = doc.splitTextToSize(contentText, 180);

    // Add title manually or you can skip this if it's inside your content
    doc.setFontSize(16);
    doc.text("Interview Feedback", 10, 20);

    // Add the rest of the content starting a bit lower (y=30)
    doc.setFontSize(12);
    doc.text(lines, 10, 30);

    doc.save("interview_feedback.pdf");
  });
});

