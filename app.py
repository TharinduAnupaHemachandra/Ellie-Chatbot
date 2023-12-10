from flask import Flask, request, jsonify, render_template, session
from elipsechat.chat import chat_generate_text
from elipsechat.query import ask_query

import os

import uuid

import firebase_admin
from firebase_admin import credentials, firestore, storage, auth

import threading

session_id = str(uuid.uuid4())

# Generate a random secret key
secret_key = os.urandom(24)

app = Flask(__name__)
app.secret_key = secret_key

cred = credentials.Certificate("firebaseCredentials.json")

firebase_app = firebase_admin.initialize_app(cred)
firebase_db = firestore.client()
# firebase_bucket = storage.bucket()
firebase_auth = auth

final_context = []

# Generate a unique session ID for each client
def generate_unique_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())  # Generate a random UUID as the session ID
    return session['session_id']

@app.route('/')
def index():
    session_id = generate_unique_session_id()
    return render_template('chat.html'), 'Session ID: {}'.format(session_id)

@app.route('/chat', methods=["GET", "POST"])
def chat():
    user_selected = ["AIA"]
    user_message = request.json.get('user')

    # Ask your query and get the context
    all, final = ask_query(user_message, user_selected, 2, 6)

    print(final)

    for f in final:
        final_context.append(f.page_content)

    # Combine the context with the user's question
    full_prompt = (
        "answer the given question by considering the context given." \
        "if the context is empty, answer based on the previous messages and analyze them when answering." \
        "Please don't make any assumptions or your knowledge to answer." \
        "don't give any answers out of the context." \
        "when giving the answers, chat like a human. Don't include content like 'based on the provided context', 'according to the context', etc" \
        "If the context have half sentences, ignore them when giving the answer." \
        "question: " + user_message +
        "context: " + " ".join(final_context)
    )

    # Generate the bot's response
    bot_response = chat_generate_text(firebase_db, session["session_id"], full_prompt)

    #return jsonify({'bot_response': bot_response})

    return bot_response

if __name__ == '__main__':
    app.run()









# from flask import Flask, request, jsonify, render_template
#
# from elipsechat.chat import chat_generate_text
# from elipsechat.query import ask_query
#
# app = Flask(__name__)
#
# final_context = []
#
# @app.route('/')
# def index():
#     return render_template('chat.html')
#
# @app.route('/chat', methods = ["GET", "POST"])
# def chat():
#     data = request.json
#     userselected = ["AIA_Health"]
#
#     user_message = data.get('user')
#
#     # Ask your query and get the context
#     all, final = ask_query(user_message, userselected, 1, 6)
#
#     for f in final:
#         final_context.append(f.page_content)
#
#     # Combine the context with the user's question
#     full_prompt = (
#             "answer the given question by considering the context given." \
#             "if the context is empty, answer based on the previous messages and analyze them when answering." \
#             "Please don't make any assumptions." \
#             "when giving the answers, chat like a human. Don't include content like 'based on the provided context', 'according to the context', etc" \
#             "question: " + user_message +
#             "context: " + " ".join(final_context)
#     )
#
#     # Generate the bot's response
#     bot_response = chat_generate_text(full_prompt)
#     return bot_response
#
#
#
# if __name__ == '__main__':
#     app.run()







# from flask import Flask, request, jsonify, render_template
#
# from elipsechat.chat import chat_generate_text
# from elipsechat.query import ask_query
#
# app = Flask(__name__)
#
# final_context = []
#
# @app.route('/')
# def index():
#     return render_template('chat.html')
#
# @app.route('/chat', methods = ["GET", "POST"])
# def chat():
#     data = request.json
#     userselected = ["AIA_Health"]
#
#     user_message = data.get('user')
#
#     # Ask your query and get the context
#     all, final = ask_query(user_message, userselected, 1, 6)
#
#     for f in final:
#         final_context.append(f.page_content)
#
#     # Combine the context with the user's question
#     full_prompt = (
#             "answer the given question by considering the context given." \
#             "if the context is empty, answer based on the previous messages and analyze them when answering." \
#             "Please don't make any assumptions or your knowledge to answer." \
#             "don't give any answers out of the context." \
#             "when giving the answers, chat like a human. Don't include content like 'based on the provided context', " \
#             "'according to the context', etc" \
#             "question: " + user_message +
#             "context: " + " ".join(final_context)
#         )
#
#     # Generate the bot's response
#     bot_response = chat_generate_text(full_prompt)
#     return bot_response
#
#
#
# if __name__ == '__main__':
#     app.run()
#
# # full_prompt = (
# #         "answer the given question by considering the context given." \
# #         "if the context is empty, answer based on the previous messages and analyze them when answering." \
# #         "Please don't make any assumptions or your knowledge to answer." \
# #         "don't give any answers out of the context." \
# #         "when giving the answers, chat like a human. Don't include content like 'based on the provided context', " \
# #         "'according to the context', etc" \
# #         "question: " + user_message +
# #         "context: " + " ".join(final_context)
# #     )