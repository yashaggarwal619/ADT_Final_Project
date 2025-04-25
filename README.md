EduNexus AI 

1. Project Overview 

The aim of EduNexus AI is to enhance user experience by automating query processing for accessing student data, like grades, through natural language inputs. The system takes a user’s natural language request, processes it with AI agents, converts it into an SQL query, executes the query, and returns the results to the user. If an error arises during the process, it is intelligently handled by the system. 

Key Features 

Natural Language Processing: Converts user-input natural language requests into structured SQL queries. 
Automated Query Breakdown: Decomposes complex user requests into manageable sub-problems for streamlined processing. 
Seamless Database Integration: Executes queries through API communication with a backend SQLite database. 
Intelligent Error Handling: Identifies and resolves issues in real-time using AI-driven error resolution agents. 
User-Friendly Feedback: Displays results or meaningful error messages in a clear and concise manner. 
Tech Stack 

Backend: Python 
Frontend: Streamlit 
Database: SQLite 
AI Agents: Ollama, Qwen2.5 - Coder:3b 
API: CRUD API for database communication 
2. Functional Workflow 
 

Step-by-Step Flow 


![Flowchart](https://github.com/user-attachments/assets/7783189a-481b-47a8-b306-f3b6e1f7466b)

User Input: 
The user types a natural language request (e.g., "Find all students with grades above 90"). 
Analyzer Agent: 
Processes the request and breaks it down into simpler, understandable, detailed steps. 
Send these steps to the Generator Agent for further action. 
Generator Agent: 
Converts the steps into SQL commands. 
Error Handler Agent: 
Analyzes the error and attempts to resolve it. 
If resolved, returns the corrected results to the user. 
If unresolved, displays a meaningful error message to the user indicating the request failed. 
 

3. System Architecture 

The system is structured as follows: 

Input Flow: 
User → Analyzer Agent → Generator Agent → Database API 
Error Handling: 
Generator Agent → Error Handler Agent (if needed) → User 
Output Flow: 
Results are displayed to the user, or an error message is shown in case of failure. 
 

4. Testing 

Input: 

User requests of varying complexity, written in natural language. 
Output: 

Ensure: 
Correct results for valid queries. 
Meaningful error messages for invalid or unsupported requests. 
Robust handling of edge cases, such as invalid syntax or unsupported operations. 
 

5. Future Enhancements 

Support for Additional Databases: 
Expand compatibility to include systems like PostgreSQL, MongoDB, etc. 
Advanced NLP Capabilities: 
Enable the model to handle more conversational or ambiguous user requests. 
Enhanced Error Diagnosis: 
Implement mechanisms for detailed feedback and suggestions to users. 
Real-Time Query Optimization: 
Improve the efficiency of SQL commands before execution. 
 
