import streamlit as st
import sqlite3
import pandas as pd  # Import pandas for DataFrame operations
import sql_query_generator
import time  # Import time for spinners and delays
import requests
import json
# Set Streamlit to wide layout
st.set_page_config(layout="wide")

# Function to query the SQLite database
def query_database(query, task, prompt):
    try:
        with st.spinner("Fetching data... Please wait!"):
                time.sleep(1)
        conn = sqlite3.connect("student_database.db")  # Replace with your SQLite database file
        if task.lower() != "view":
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            conn.close()
            return "Query executed"
        else:
            df = pd.read_sql_query(query, conn)  # Fetch data as DataFrame
            conn.close()
            return df
    except Exception as e:
        return f"Error: {e}"
def find_braces_indices(input_string):
        """
        Finds the indices of all opening '{' and closing '}' in the input string.
        
        Args:
            input_string (str): The input string.
        
        Returns:
            dict: A dictionary with two keys:
                - 'opening': A list of indices of '{'
                - 'closing': A list of indices of '}'
        """
        opening_indices = [i for i, char in enumerate(input_string) if char == '{']
        closing_indices = [i for i, char in enumerate(input_string) if char == '}']
        
        return opening_indices, closing_indices   
def convert_json(ans):
    start,end=find_braces_indices(ans)
    if end==[]:
        ans+="}"
        end=[len(ans)]
    #print(start,end)
    #print(CodeGenerator_Agent_Response)
    start=start[0]

    end=end[0]
    CodeGenerator_Agent_Response=ans[start:end+1]
    CodeGenerator_Agent_Response=CodeGenerator_Agent_Response.replace("\n","")
    json_result=json.loads(CodeGenerator_Agent_Response)
    return json_result 
def generate_query(query):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
        
    },
    data=json.dumps({
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [{
        'role': 'system',
        'content': '''
            'You are a SQL query generator for a database with the following schema:\n\n'
            # Updated SQL Schema
                """
    -- Create the Students table
    CREATE TABLE IF NOT EXISTS Students (
        studentID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,   --Name of student
        email TEXT UNIQUE,  --Student's Email ID
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Create the Subjects table
    CREATE TABLE IF NOT EXISTS Subjects (
        subjectID TEXT PRIMARY KEY, --Subject ID for a subject, for example, "SUBJ001"
        subjectName TEXT UNIQUE NOT NULL --Name of subject corresponding to a subjectID, for example "Mathematics"
    );
    
    -- Create the Assignments table
    CREATE TABLE IF NOT EXISTS Assignments (
        subjectID TEXT NOT NULL,  --SubjectID for which the assignment is created , for example "SUBJ001"
        assignmentName TEXT NOT NULL, --Name of the assignment with values Assignment1,Assignment2,Assignment3,Mid Term, and Final Exam
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        PRIMARY KEY (subjectID, assignmentName),
        FOREIGN KEY (subjectID) REFERENCES Subjects(subjectID)
    );
    
    -- Create the Marks table
    CREATE TABLE IF NOT EXISTS Marks (
        markID INTEGER PRIMARY KEY AUTOINCREMENT,
        studentID INTEGER NOT NULL, --Identifier for each student
        subjectID TEXT NOT NULL, --SubjectID for which the assignment is created , for example "SUBJ001"
        assignmentName TEXT NOT NULL, --Name of the assignment
        marks INTEGER CHECK (marks BETWEEN 0 AND 100),
        grade TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        FOREIGN KEY (studentID) REFERENCES Students(studentID),
        FOREIGN KEY (subjectID, assignmentName) REFERENCES Assignments(subjectID, assignmentName)
    );
    """

    'The output should only be a json with format with key and values as strings in double quotes'
    '''
    '''
    {
        "task": insert', 'delete', 'update' or 'view',
        "SQL Query": "sql guery generated"
    }
    Do not output anything else besides the json. Make sure end  bracket "}" is there in json. 
    '''
    
    },
    {
        'role': 'user',
        'content': f'{query}',
    },
    ]
        
    })
    )
    response_json = response.json() 
    result=response_json['choices'][0]['message']['content']
    return result

# Function to render the Home page
def render_home():
    st.markdown(
        """
        <div style="text-align: center; padding: 30px;">
            <h1 style="color: #39FF14; font-family: 'Trebuchet MS', sans-serif; font-size: 4rem;">
                Welcome to EduNexus AI!
            </h1>
            <p style="color: #4682B4; font-size: 1.5rem; margin: 20px 0;">
                A natural language interface that allows users to manage backend systems through conversational commands.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px;">
                <h2 style="color: #2F4F4F; text-align: center;">🎯 Key Features</h2>
                <ul style="color: #4682B4; font-size: 1.1rem;">
                    <li>Natural language command processing</li>
                    <li>Intelligent operation parsing</li>
                    <li>Real-time response generation</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div style="background-color: #f0fff0; padding: 20px; border-radius: 10px;">
                <h2 style="color: #2F4F4F; text-align: center;">⚙️ Current Implementation</h2>
                <ul style="color: #4682B4; font-size: 1.1rem;">
                    <li>CRUD operations support</li>
                    <li>Error handling and recovery</li>
                    <li>Data persistence</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div style="background-color: #fff0f5; padding: 20px; border-radius: 10px;">
                <h2 style="color: #2F4F4F; text-align: center;">🚀 Applications</h2>
                <ul style="color: #4682B4; font-size: 1.1rem;">
                    <li>Database management</li>
                    <li>API interaction</li>
                    <li>Data analytics</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="margin-top: 40px; text-align: center;">
            <h2 style="color: #2F4F4F;">🎈 Getting Started</h2>
            <p style="color: #4682B4; font-size: 1.2rem;">
                Navigate to the Chatbox using the sidebar menu to start interacting with the system.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Chatbox logic
# Chatbox logic
def render_chatbox():
    st.title("Welcome to EduNexus AI, So what would you like to do?")

    # Initialize session state variables
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display chat messages from history
    for message in st.session_state["messages"]:
        if message["role"] == "assistant":
            with st.chat_message("assistant"):
                if isinstance(message["content"], pd.DataFrame):
                    st.dataframe(message["content"])
                else:
                    st.markdown(message["content"])
        else:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What would you like to ask?"):
        # Add user message to session state and display it
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Create a placeholder for loading status
        with st.chat_message("assistant"):
            loading_placeholder = st.empty()
            loading_placeholder.markdown("Fetching data... Please wait!")

        # Process the user query
        result = generate_query(prompt)
        result=convert_json(result)
        sql_query = result['SQL Query']
        task = result['task']
        query_result = query_database(sql_query, task, prompt)

        # Update the placeholder with the final response
        if "Error" in query_result:
            loading_placeholder.markdown("Error occurred. Retrying...")
            result = sql_query_generator.retryQueryGeneratingAgent(sql_query, prompt, query_result)
            sql_query = result['SQL Query']
            task = result['task']
            query_result = query_database(sql_query, task, prompt)

        # Replace loading message with actual output
        if "Error" in query_result:
            response = "Error occurred with this prompt. Please retry with another prompt."
            loading_placeholder.markdown(response)
            st.session_state["messages"].append({"role": "assistant", "content": response})
        elif task.lower() != "view":
            response = f"Query executed successfully. View the database to check changes.\n\n**SQL Query:** `{sql_query}`"
            loading_placeholder.markdown(response)
            st.session_state["messages"].append({"role": "assistant", "content": response})
        else:
            loading_placeholder.empty()  # Remove the loading message
            st.markdown("**SQL Query used for your reference:**")
            st.markdown(sql_query)
            st.dataframe(query_result.drop_duplicates())
            st.session_state["messages"].append({"role": "assistant", "content": query_result})



page = st.sidebar.radio(
    "Navigate to:",
    ["🏠 Home", "💬 Chatbox"],
    index=0,
    key="sidebar_navigation",
)

if page == "🏠 Home":
    render_home()
elif page == "💬 Chatbox":
    render_chatbox()

