import chromadb

from sentence_transformers import SentenceTransformer
from langchain_ollama import OllamaLLM


# --------------------------------
# Embedding Model
# --------------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# --------------------------------
# Ollama
# --------------------------------

llm = OllamaLLM(
    model="llama3.2"
)


# --------------------------------
# ChromaDB
# --------------------------------

client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_collection(
    name="cyberathon"
)


# --------------------------------
# Greetings
# --------------------------------

greetings = [
    "hello",
    "hi",
    "hey",
    "hii",
    "hiii",
    "hello there",
    "hi there",
    "good morning",
    "good afternoon",
    "good evening"
]


# --------------------------------
# Build Chat History
# --------------------------------


def build_chat_history(chat_history):

    if not chat_history:
        return ""

    history = []

    recent_messages = chat_history[-8:]

    for message in recent_messages:

        if not isinstance(message, dict):
            continue

        role = message.get("role")
        content = message.get("content")

        if not role or content is None:
            continue

        if role not in ["user", "assistant"]:
            continue

        history.append(
            f"{role}: {content}"
        )

    return "\n".join(history)

# --------------------------------
# Get Relevant Cyberathon Data
# --------------------------------

def get_context(search_query, n_results=15):

    query_embedding = (
        embedding_model
        .encode(search_query)
        .tolist()
    )

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=n_results
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    if not documents:
        return ""

    return "\n\n".join(documents)


# --------------------------------
# Vacancy Data From Cyberathon
# --------------------------------

def vacancy_response(question_clean):

    career_url = (
        "https://www.cyberathon.com/cyberathon-careers"
    )

    vacancies = {
        "python": (
            "Python Development",
            2
        ),
        "java": (
            "Java Development",
            2
        ),
        "php": (
            "PHP Development",
            2
        ),
        "mern": (
            "MERN Stack",
            2
        ),
        "mean": (
            "MEAN Stack",
            2
        ),
        "dot net": (
            "Dot Net Development",
            2
        ),
        ".net": (
            "Dot Net Development",
            2
        ),
        "android": (
            "Android Development",
            2
        ),
        "hr": (
            "Human Resources (HR)",
            2
        ),
        "human resources": (
            "Human Resources (HR)",
            2
        )
    }


    # --------------------------------
    # Backend Vacancy
    # --------------------------------

    backend_words = [
        "backend",
        "back end",
        "back-end"
    ]

    if any(
        word in question_clean
        for word in backend_words
    ):

        backend_positions = [
            ("PHP Development", 2),
            ("MERN Stack", 2),
            ("Dot Net Development", 2)
        ]

        answer = (
            "Yes! Cyberathon has the following "
            "backend-related openings:\n\n"
        )

        for position, number in backend_positions:

            answer += (
                f"• **{position}** – "
                f"{number} vacancies\n"
            )

        answer += (
            f"\n**Apply Now:** {career_url}"
        )

        return answer


    # --------------------------------
    # Frontend Vacancy
    # --------------------------------

    frontend_words = [
        "frontend",
        "front end",
        "front-end"
    ]

    if any(
        word in question_clean
        for word in frontend_words
    ):

        frontend_positions = [
            ("MERN Stack", 2),
            ("MEAN Stack", 2)
        ]

        answer = (
            "Yes! Cyberathon has the following "
            "frontend-related openings:\n\n"
        )

        for position, number in frontend_positions:

            answer += (
                f"• **{position}** – "
                f"{number} vacancies\n"
            )

        answer += (
            f"\n**Apply Now:** {career_url}"
        )

        return answer


    # --------------------------------
    # Web Vacancy
    # --------------------------------

    web_words = [
        "web vacancy",
        "web vacancies",
        "web opening",
        "web openings",
        "web development vacancy",
        "web development vacancies",
        "web development opening",
        "web developer vacancy"
    ]

    if any(
        word in question_clean
        for word in web_words
    ):

        web_positions = [
            ("MERN Stack", 2),
            ("MEAN Stack", 2),
            ("Java Development", 2)
        ]

        answer = (
            "Yes! Cyberathon has the following "
            "web development openings:\n\n"
        )

        for position, number in web_positions:

            answer += (
                f"• **{position}** – "
                f"{number} vacancies\n"
            )

        answer += (
            f"\n**Apply Now:** {career_url}"
        )

        return answer


    # --------------------------------
    # Marketing Vacancy
    # --------------------------------

    marketing_words = [
        "marketing vacancy",
        "marketing vacancies",
        "marketing opening",
        "marketing openings",
        "digital marketing vacancy",
        "digital marketing vacancies"
    ]

    if any(
        word in question_clean
        for word in marketing_words
    ):

        return (
            "Yes! Cyberathon has an opening for "
            "**Digital Marketing**.\n\n"
            "**Number of vacancies:** 2\n\n"
            f"**Apply Now:** {career_url}"
        )


    # --------------------------------
    # Exact Technology Vacancy
    # --------------------------------

    for key, value in vacancies.items():

        if key in question_clean:

            position, number = value

            return (
                f"Yes! Cyberathon has an opening for "
                f"**{position}**.\n\n"
                f"**Number of vacancies:** {number}\n\n"
                f"**Apply Now:** {career_url}"
            )


    # --------------------------------
    # General Development Vacancy
    # --------------------------------

    development_words = [
        "development vacancy",
        "development vacancies",
        "developer vacancy",
        "developer vacancies",
        "development opening",
        "development openings",
        "software vacancy",
        "software vacancies"
    ]

    if any(
        word in question_clean
        for word in development_words
    ):

        development_positions = [
            ("Python Development", 2),
            ("MERN Stack", 2),
            ("MEAN Stack", 2),
            ("Java Development", 2),
            ("PHP Development", 2),
            ("Dot Net Development", 2),
            ("Android Development", 2)
        ]

        answer = (
            "Yes! Cyberathon currently has "
            "the following development openings:\n\n"
        )

        for position, number in development_positions:

            answer += (
                f"• **{position}** – "
                f"{number} vacancies\n"
            )

        answer += (
            f"\n**Apply Now:** {career_url}"
        )

        return answer


    return None


# --------------------------------
# Ask Chatbot
# --------------------------------

def ask_chatbot(
    question,
    chat_history=None
):

    question_clean = (
        question
        .lower()
        .strip()
    )


    # --------------------------------
    # Greeting
    # --------------------------------

    if question_clean in greetings:

        return """Hello! 👋 Welcome to Cyberathon.

What do you want to know?

🛠️ **Services**

🎓 **Internship**

💼 **Careers / Vacancy**

📦 **Products**

ℹ️ **About Cyberathon**

📞 **Contact**

You can simply type the topic you are interested in."""


    # --------------------------------
    # Conversation History
    # --------------------------------

    history = build_chat_history(
        chat_history
    )


    # --------------------------------
    # Resume / HR Application Request
    # --------------------------------

    resume_words = [
        "resume",
        "cv",
        "my resume",
        "my cv",
        "send resume",
        "send cv",
        "send my resume",
        "send my cv",
        "submit resume",
        "submit cv",
        "submit my resume",
        "submit my cv",
        "where should i send resume",
        "where should i send my resume",
        "where can i send resume",
        "where can i send my resume",
        "where should i send cv",
        "where can i send cv",
        "how can i apply",
        "how do i apply",
        "i want to apply",
        "want to apply",
        "i want to send resume",
        "i want to send my resume",
        "apply for job",
        "apply for vacancy",
        "apply for this job",
        "apply for this vacancy"
    ]


    is_resume_request = any(
        word in question_clean
        for word in resume_words
    )


    if is_resume_request:

        hr_email = "hr.cyberathon@gmail.com"

        career_url = (
            "https://www.cyberathon.com/cyberathon-careers"
        )


        # Get previous conversation context
        if history:

            search_query = (
                history
                + "\nUser: "
                + question
            )

        else:

            search_query = question


        context = get_context(
            search_query,
            15
        )


        # --------------------------------
        # Resume Answer
        # --------------------------------

        return (
            "Sure! You can send your resume/CV to "
            f"**{hr_email}** for the application process.\n\n"
            f"You can also apply through the Cyberathon "
            f"Careers page:\n"
            f"**Apply Now:** {career_url}"
        )


    # --------------------------------
    # Internship Selection
    # --------------------------------

    internship_words = [
        "internship",
        "internships",
        "intern"
    ]


    if question_clean in internship_words:

        return """Sure! 🎓 Cyberathon offers internship opportunities in different technologies.

You can ask about:

• Java Internship
• Python Internship
• MERN Stack Internship
• MEAN Stack Internship
• PHP Internship
• Android Internship
• Other internship programs

Just type the technology name you are interested in."""


    # --------------------------------
    # Vacancy Selection
    # --------------------------------

    vacancy_words = [
        "vacancy",
        "vacancies",
        "opening",
        "openings",
        "job",
        "jobs",
        "position",
        "positions",
        "hiring"
    ]


    is_vacancy = any(
        word in question_clean
        for word in vacancy_words
    )


    # --------------------------------
    # Vacancy Response
    # --------------------------------

    if is_vacancy:

        answer = vacancy_response(
            question_clean
        )

        if answer:
            return answer


    # --------------------------------
    # Java / PHP / Python etc.
    # --------------------------------

    technologies = [
        "java",
        "php",
        "python",
        "mern",
        "mean",
        "android",
        "dot net",
        ".net"
    ]


    technology_found = None

    for technology in technologies:

        if question_clean == technology:

            technology_found = technology
            break


    if technology_found:

        return (
            f"Sure! I can help you with "
            f"**{technology_found.upper()}** information.\n\n"
            f"Are you looking for "
            f"**{technology_found.upper()} Internship** "
            f"or **{technology_found.title()} Development Vacancy**?"
        )


    # --------------------------------
    # Specific Internship
    # --------------------------------

    internship_query_words = [
        "java internship",
        "php internship",
        "python internship",
        "mern internship",
        "mean internship",
        "android internship",
        "dot net internship",
        ".net internship"
    ]


    if any(
        word in question_clean
        for word in internship_query_words
    ):

        search_query = (
            "Cyberathon internship "
            + question
        )

        context = get_context(
            search_query,
            15
        )

        if not context:

            return (
                "I couldn't find this information "
                "in the Cyberathon data."
            )


        prompt = f"""
You are the official Cyberathon company
information assistant.

The user is asking specifically about
an internship.

Previous conversation:
{history}

Cyberathon data:
{context}

User question:
{question}

Rules:

1. Answer only using the Cyberathon data.

2. Give the exact internship information.

3. Do not change internship information
into vacancy information.

4. Include technologies, curriculum,
training topics, duration, eligibility,
fees or application information only
when present in the data.

5. Do not invent information.

6. Do not mention RAG.

7. Do not mention context or documents.

8. If Apply/Enroll URL exists, provide it.

9. Give a clear and direct answer.

Answer:
"""

        response = llm.invoke(
            prompt
        )

        return response.strip()


    # --------------------------------
    # Short Follow-up
    # --------------------------------

    short_words = [
        "details",
        "detail",
        "more",
        "more details",
        "duration",
        "fees",
        "fee",
        "eligibility",
        "apply",
        "enroll",
        "link",
        "email",
        "mail",
        "contact",
        "phone",
        "number",
        "address",
        "blog",
        "gallery",
        "yes",
        "no"
    ]


    if (
        question_clean in short_words
        and history
    ):

        search_query = (
            history
            + "\nUser: "
            + question
        )

    else:

        search_query = question


    # --------------------------------
    # Get Relevant Data
    # --------------------------------

    context = get_context(
        search_query,
        15
    )


    if not context:

        return (
            "I couldn't find this information "
            "in the Cyberathon data."
        )


    # --------------------------------
    # Prompt
    # --------------------------------

    prompt = f"""
You are the official Cyberathon
company information assistant.

Answer the user's question using ONLY
the Cyberathon website data.

Previous conversation:
{history}

Relevant Cyberathon data:
{context}

Current user question:
{question}

IMPORTANT RULES:

1. Answer only using the Cyberathon data.

2. Use previous conversation to understand
follow-up questions such as:
"yes", "more", "details", "apply",
"link", "duration", etc.

3. Do not invent any information.

4. If the user asks about services,
provide the services actually present
in the Cyberathon data.

5. If the user asks about products,
provide product information from the data.

6. If the user asks about contact,
provide email, phone or address only
when present in the data.

7. If the user asks about an internship,
provide internship information only.

8. If the user asks about a vacancy,
provide vacancy information only.

9. If the user asks about a technology
vacancy, give the matching position
and number of vacancies.

10. If Apply Now URL exists, provide it.

11. If Enroll Now URL exists, provide it.

12. Never confuse internship information
with vacancy information.

13. Never mention RAG.

14. Never mention retrieved documents.

15. Never say "According to the context".

16. If the information is not available,
say exactly:

"I couldn't find this information
in the Cyberathon data."

17. Keep the answer clear and direct.

Answer:
"""


    # --------------------------------
    # Ollama
    # --------------------------------

    response = llm.invoke(
        prompt
    )

    return response.strip()