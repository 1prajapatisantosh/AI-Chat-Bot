import streamlit as st
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
import pandas as pd

# Initialize NLP pipeline
model_name = "deepset/roberta-base-squad2"
model = AutoModelForQuestionAnswering.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
chunk_size = 400
context = ("""
Our courses are tailored to accommodate both beginners and advanced users. Whether you're just starting your journey or looking to enhance your existing skills, we have learning paths suitable for all levels.\
Absolutely! We understand the importance of flexibility in learning. You have the freedom to learn at your own pace, accessing course materials and completing assignments according to your schedule.\
Assignments vary based on the course you choose. They may include quizzes, projects, and practical exercises designed to reinforce your learning and skills.\
Prerequisites vary depending on the course. However, basic computer literacy and familiarity with relevant software are usually recommended. Check the course details for specific requirements.\
Course duration varies, most course take about 3 month to complete.You can find the estimated duration on the course description page.\
Pricing details can be found on our website. Costs may vary depending on the course and any ongoing promotions. We aim to provide competitive pricing to make quality education accessible to all.\
We offer robust doubt support through various channels including live chat, discussion forums, and dedicated instructor support. Our team is committed to addressing your queries and ensuring a seamless learning experience.\
Yes, we provide placement oppurtunities to eligible learners upon course completion. Our dedicated placement cell works to connect you with relevant job opportunities in your field of study.\
Our course is different form other  with its hands-on learning approach,expert,instructors and better curriculum tailored to meet industry demands. We prioritize practical skills development to ensure our learners are well-equipped for the real world.\
Yes, we offer a satisfaction guarantee. If you're not satisfied with the course within the specified time frame, you can request a full refund, no questions asked. Your satisfaction is our priority.\
Absolutely! Our courses are designed to equip you with in-demand skills that are highly relevant in today's dynamic job market. We continuously update our curriculum to reflect industry trends and emerging technologies.\
While a strong foundation in Data Structures and Algorithms (DSA) can be beneficial, it's not always a prerequisite. However, some advanced courses may require proficiency in DSA concepts. Check the course description for specific requirements.\
you will make around the current market payout after completing this course and depending on factors such as industry, location, and experience. Our courses are designed to enhance your skills and increase your job prospects in lucrative fields. Your dedication and expertise will ultimately determine your earning potential.\
Yes, we offer flexible payment options including EMI (Equated Monthly Installments) to make our courses more accessible to learners. You can choose EMI plan that suits your financial situation.\
We strive to make education accessible to everyone. Yes,we have available financial aid options for unde-previleged people.We're committed to supporting learners from all backgrounds in their educational journey.\
 Yes, course offer certificate to showcase your achievements and enhance your professional profile . Our certificates are recognized and valued by employers worldwide.\
You can find testimonials from our satisfied learners on our website and social media channels. Hear directly from past students about their experiences and the benefits they've gained from our courses.\
Our courses are taught by industry experts and seasoned professionals with extensive experience in their respective fields. You'll benefit from their expertise, guidance, and insights throughout your learning journey.\
This is an online course, allowing you to access materials and participate in learning activities from anywhere with an internet connection. Enjoy the convenience of learning at your own pace, on your own schedule, without the constraints of a physical classroom.\
""")
chunks = [context[i:i+chunk_size] for i in range(0, len(context), chunk_size)]

# FAQ Database
faq = {
    "Suitable for beginner or advanced users ?": "Our courses are tailored to accommodate both beginners and advanced users.",
    "Can I learn at my own pace?": "Absolutely! You have the freedom to learn at your own pace.",
    "What type of assignment do you give ?": "Assignments vary based on the course you choose.",
    "What are the pre-requirement for this course ?": "Prerequisites vary depending on the course.",
    "How long does this course take to complete ?": "Course duration varies, most courses take about 3 months to complete.",
    "How much does the course cost ?": "Pricing details can be found on our website.",
    "How is the doubt support ?": "We offer robust doubt support through various channels.",
    "Does this course offer placement opportunities also ?": "Yes, we provide placement opportunities to eligible learners upon course completion.",
    "How is the course different from other platform courses ?": "Our course is different with its hands-on learning approach and expert instructors.",
    "Is there any money back guarantee if I did not like the course ?": "Yes, we offer a satisfaction guarantee.",
    "Is this course relevant in today's market ?": "Our courses are designed to equip you with in-demand skills.",
    "Is good DSA a prerequisite for this course ?": "While a strong foundation in Data Structures and Algorithms (DSA) can be beneficial, it's not always a prerequisite.",
    "How much I can make after completing this course ?": "Your earning potential depends on factors such as industry, location, and experience.",
    "Can I pay in EMI for this course ?": "Yes, we offer flexible payment options including EMI.",
    "Does this course offer financial aid for underprivileged people ?": "Yes, we have available financial aid options.",
    "Does this course offer any certificate ?": "Yes, course offers certificate to showcase your achievements.",
    "Where can I get testimonials for this course ?": "You can find testimonials from our satisfied learners on our website.",
    "Who is the mentor for this course ?": "Our courses are taught by industry experts and seasoned professionals.",
    "Is it an online or offline course ?": "This is an online course, allowing you to access materials from anywhere."
}

 #Initialize chat history
chat_history = []

# Function to save chat history to CSV
def save_chat_history():
    df = pd.DataFrame(chat_history, columns=["User Query", "Bot Response"])
    df.to_csv("chat_histo#ry.csv", index=False)

# Title and description
st.title("AI Chat Bot for Course Queries")
st.write("Welcome! Feel free to ask any questions about our courses.")
question = st.text_input("Question:", "", key="question_input_1")

answers = []
counter = 1
while question:
    for chunk in chunks:
        QA_input = {
            'question': question,
            'context': chunk
        }
        res = nlp(QA_input)
        answers.append(res['answer'])

    # Break loop if user ends conversation
    if question.lower() == "end conversation":
        st.write("Thank you for chatting with us!")
        save_chat_history()
        break

    # Check if user query is empty
    if not question:
        st.write("Please enter a valid question.")
        continue

    # Answer from FAQ
    if question in faq:
        bot_response = faq[question]
        st.write("AIBot:", bot_response)
        chat_history.append([question, bot_response])
    else:
        # Answer from NLP
        QA_input = {
            'question': question,
            'context': context
        }
        res = nlp(QA_input)
        bot_response = res['answer']

        # Check if answer is valid
        if bot_response != "":
            st.write("Bot:", bot_response)
            chat_history.append([question, bot_response])
        else:
            st.write("Bot:", "I'm sorry, I don't have an answer to that. Let me pass it to our doubt assistant.")
            chat_history.append([question, "No answer found. Passing to doubt assistant."])
  
    answers = []
    counter += 1
    question = st.text_input("Question:", "", key="question_input_" + str(counter))
    

# Display feedback and data sharing option
if st.button("Provide Feedback and Share Data"):
    user_satisfaction = st.radio("How satisfied are you with the chat experience?", ["Satisfied", "Neutral", "Not Satisfied"])
    if user_satisfaction != "Neutral":
        st.write("Thank you for your feedback!")
        save_chat_history()
        # Here you can implement data sharing with the sales team
    else:
        st.write("Please provide more details so we can improve our chat bot.")
