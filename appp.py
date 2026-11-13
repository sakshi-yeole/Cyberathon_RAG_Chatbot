import os
import sqlite3
from datetime import datetime

import streamlit as st

import requests


# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="Cyberathon Chatbot",
    page_icon="🤖",
    layout="centered"
)


API_BASE_URL = os.getenv(
    "BACKEND_API_URL",
    "http://127.0.0.1:8000"
)

# --------------------------------
# Database
# --------------------------------

db_path = os.path.join(
    os.path.dirname(__file__),
    "chat_history.db"
)


def create_database():

    connection = sqlite3.connect(
        db_path
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_date TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            chat_time TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()


create_database()


# --------------------------------
# Save Message
# --------------------------------

def save_message(
    role,
    content
):

    connection = sqlite3.connect(
        db_path
    )

    cursor = connection.cursor()

    current_date = datetime.now().strftime(
        "%d %b %Y"
    )

    current_time = datetime.now().strftime(
        "%I:%M %p"
    )

    cursor.execute(
        """
        INSERT INTO chats
        (chat_date, role, content, chat_time)
        VALUES (?, ?, ?, ?)
        """,
        (
            current_date,
            role,
            content,
            current_time
        )
    )

    connection.commit()

    connection.close()


# --------------------------------
# Get Chat Dates
# --------------------------------

def get_chat_dates():

    connection = sqlite3.connect(
        db_path
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT DISTINCT chat_date
        FROM chats
        ORDER BY id DESC
        """
    )

    dates = cursor.fetchall()

    connection.close()

    return [
        date[0]
        for date in dates
    ]


# --------------------------------
# Get Chat For Selected Date
# --------------------------------

def get_chat_by_date(
    selected_date
):

    connection = sqlite3.connect(
        db_path
    )


    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM chats
        WHERE chat_date = ?
        ORDER BY id ASC
        """,
        (selected_date,)
    )

    chats = cursor.fetchall()

    connection.close()

    return [
        {
            "role": role,
            "content": content
        }
        for role, content in chats
    ]


# --------------------------------
# Title
# --------------------------------

logo_path = os.path.join(
    os.path.dirname(__file__),
    "cyberathon_logo.jpg"
)


col1, col2 = st.columns([1, 5])


with col1:

    st.image(
        logo_path,
        width=80
    )


with col2:

    st.title(
        "Cyberathon Chatbot"
    )


st.caption(
    "Ask questions about Cyberathon"
)


# --------------------------------
# Initialize Chat History
# --------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# --------------------------------
# Sidebar Chat History
# --------------------------------

st.sidebar.title(
    "📜 Chat History"
)


chat_dates = get_chat_dates()


for chat_date in chat_dates:

    if st.sidebar.button(
        f"📅 {chat_date}",
        key=f"date_{chat_date}",
        use_container_width=True
    ):

        st.session_state.messages = (
            get_chat_by_date(chat_date)
        )

        st.rerun()


# --------------------------------
# Clear Chat
# --------------------------------

if st.sidebar.button(
    "🗑️ Clear Chat"
):

    st.session_state.messages = []

    st.rerun()


# --------------------------------
# Display Previous Chat History
# --------------------------------

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message(
            "user",
            avatar="👤"
        ):

            st.markdown(
                message["content"]
            )

    else:

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            st.markdown(
                message["content"]
            )


# --------------------------------
# Chat Input
# --------------------------------

question = st.chat_input(
    "Ask something about Cyberathon..."
)


# --------------------------------
# Process New Question
# --------------------------------

if question:

    # --------------------------------
    # Save User Question
    # --------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # --------------------------------
    # Save User Question Permanently
    # --------------------------------

    save_message(
        "user",
        question
    )


    # --------------------------------
    # Display User Question
    # --------------------------------

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.markdown(
            question
        )


    # --------------------------------
    # Generate Answer
    # --------------------------------

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        with st.spinner("Generating answer..."):
        
            try:
        
                response = requests.post(
                    f"{API_BASE_URL}/ask",
                    json={
                        "question": question,
                        "chat_history": st.session_state.messages
                    },
                    timeout=120
                )
        
                response.raise_for_status()
        
                answer = response.json()["answer"]
        
            except requests.RequestException as e:
        
                st.error(f"Backend API error: {e}")
                st.stop()


        st.markdown(
            answer
        )


    # --------------------------------
    # Save Assistant Answer
    # --------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    # --------------------------------
    # Save Assistant Answer Permanently
    # --------------------------------

    save_message(
        "assistant",
        answer
    )