import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

faqs = [
    {
        "question": "How do I choose the right institution?",
        "answer": "Choose an institution based on accreditation, faculty quality, course structure, placement records, and infrastructure."
    },
    {
        "question": "How many colleges should I apply to?",
        "answer": "It is recommended to apply to 3 to 6 colleges depending on your academic profile and preferences."
    },
    {
        "question": "What documents are needed for admission?",
        "answer": "Common documents include mark sheets, transfer certificate, ID proof, photos, and entrance exam scores if applicable."
    },
    {
        "question": "What is the difference between a college and a university?",
        "answer": "A college usually offers specific courses under a university, while a university is an umbrella institution that can include multiple colleges and offer degrees."
    },
    {
        "question": "What is an academic credit?",
        "answer": "An academic credit represents the value of a course based on workload and learning hours."
    },
    {
        "question": "How are classes structured in college?",
        "answer": "Classes are usually structured into lectures, tutorials, and practical sessions depending on the course."
    },
    {
        "question": "Can I get financial assistance for my studies?",
        "answer": "Yes, students can apply for scholarships, education loans, or government financial aid programs."
    },
    {
        "question": "What support is available for struggling students?",
        "answer": "Colleges offer mentoring, remedial classes, counseling services, and academic support programs."
    },
    {
        "question": "When is the last date to apply for admission?",
        "answer": "The last date varies by institution and course; students should check official college notifications."
    },
    {
        "question": "What are the eligibility criteria for this course?",
        "answer": "Eligibility typically depends on academic qualifications such as 10+2 marks and required subjects."
    },
    {
        "question": "How do I apply for a scholarship or financial aid?",
        "answer": "You can apply through the college portal or government scholarship websites by submitting required documents."
    },
    {
        "question": "What documents are required to upload with the application?",
        "answer": "You may need scanned copies of mark sheets, ID proof, photographs, and certificates."
    },
    {
        "question": "How can I check my application status?",
        "answer": "You can check application status through the official admission portal using your login credentials."
    },
    {
        "question": "Is an entrance exam required for admission?",
        "answer": "Some courses require entrance exams while others offer direct admission based on merit."
    },
    {
        "question": "What is the total fee structure for my course?",
        "answer": "The fee structure varies depending on the course, institution, and category of admission."
    },
    {
        "question": "How do I pay my semester fees online?",
        "answer": "Semester fees can be paid through the college portal using net banking, UPI, or cards."
    },
    {
        "question": "What is the refund policy if I cancel admission?",
        "answer": "Refund policies vary by institution and are usually based on cancellation timing and rules."
    },
    {
        "question": "Are there any additional or hidden exam fees?",
        "answer": "Most colleges mention all fees transparently, but students should verify fee breakdown from official sources."
    },
    {
        "question": "Can I pay tuition fees in installments?",
        "answer": "Some institutions allow installment payments depending on their financial policies."
    },
    {
        "question": "How can I download the course syllabus?",
        "answer": "You can download the syllabus from the college website or academic portal."
    },
    {
        "question": "What is the minimum attendance required for exams?",
        "answer": "Most colleges require at least 75% attendance to be eligible for exams."
    },
    {
        "question": "When will the semester exam timetable be released?",
        "answer": "The timetable is usually released a few weeks before the exams on the official portal."
    },
    {
        "question": "How do I apply for revaluation or rechecking of exams?",
        "answer": "You can apply through the examination cell or online portal within the given deadline."
    },
    {
        "question": "What is the process to change major or elective subjects?",
        "answer": "Subject changes are allowed within a specific timeframe with academic approval."
    },
    {
        "question": "Which companies visit campus for placements?",
        "answer": "Companies vary each year, including IT, core engineering, and consulting firms."
    }
]

faq_questions = [item["question"] for item in faqs]
faq_answers = [item["answer"] for item in faqs]

vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(faq_questions)

def get_answer(user_query):
    user_vec = vectorizer.transform([user_query])
    similarity = cosine_similarity(user_vec, faq_vectors)

    best_match_index = similarity.argmax()
    best_score = similarity[0][best_match_index]

    if best_score < 0.4:
        return "⚠️ Sorry, I couldn't find a relevant answer. Please ask a college-related question."

    return faq_answers[best_match_index]

st.title("🎓 College FAQ Chatbot")

st.markdown("💬 Ask questions about admissions, fees, exams, placements, scholarships, and more.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)

user_question = st.chat_input("💬 Ask a college-related question")

if user_question:
    st.chat_message("user").write(f"🧑‍🎓 {user_question}")
    answer = get_answer(user_question)
    st.chat_message("assistant").write(f"🤖 {answer}")
    st.session_state.chat_history.append(("user", user_question))
    st.session_state.chat_history.append(("assistant", answer))
