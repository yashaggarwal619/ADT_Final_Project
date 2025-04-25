import ollama
import json
# def return_sql_query1(user_query):
#     response = ollama.chat(model='llama3.2',messages=[
#     {
#         'role': 'system',
#         'content': (
#             'You are a SQL query generator for a database with the following schema:\n\n'
#             # Updated SQL Schema
#              """
# -- Create the Students table
# CREATE TABLE IF NOT EXISTS Students (
#     studentID INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     email TEXT UNIQUE,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
 
# -- Create the Subjects table
# CREATE TABLE IF NOT EXISTS Subjects (
#     subjectID TEXT PRIMARY KEY,
#     subjectName TEXT UNIQUE NOT NULL
# );
 
# -- Create the Assignments table
# CREATE TABLE IF NOT EXISTS Assignments (
#     subjectID TEXT NOT NULL,
#     assignmentName TEXT NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY (subjectID, assignmentName),
#     FOREIGN KEY (subjectID) REFERENCES Subjects(subjectID)
# );
 
# -- Create the Marks table
# CREATE TABLE IF NOT EXISTS Marks (
#     markID INTEGER PRIMARY KEY AUTOINCREMENT,
#     studentID INTEGER NOT NULL,
#     subjectID TEXT NOT NULL,
#     assignmentName TEXT NOT NULL,
#     marks INTEGER CHECK (marks BETWEEN 0 AND 100),
#     grade TEXT NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (studentID) REFERENCES Students(studentID),
#     FOREIGN KEY (subjectID, assignmentName) REFERENCES Assignments(subjectID, assignmentName)
# );
# """
#             'The output should only be a json with format'
#             '''
#             {
#                 'task': 'insert', 'delete', 'update' or 'view',
#                 'SQL Query': sql guery generated
#             }
#             Do not output anything else besides the json. Make sure end  bracket "}" is there in json 
#             '''
#         ),
#     },
#     {
#         'role': 'user',
#         'content': f'{user_query}',
#     },
# ],options={'temperature': 0})
#     result=response['message']['content']
#     start,end=find_braces_indices(result)
#     if end==[]:
#         result+="}"
#         end=[len(result)]
#     print(start,end)
#     print(result)
#     start=start[0]
    
#     end=end[0]
#     result=result[start:end+1]
#     result=result.replace("\n","")
#     json_result=json.loads(result)
#     return json_result


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

def Simplifying_Agent(query):
    response = ollama.chat(model='qwen2.5-coder:3b',messages=[
    {
        'role': 'system',
        'content': (
            'You are a step generator.query analyser given the datbase schema  and user query you need to provide detailed steps required to get the result when querying the database. Keep in mind that i will use your setps to create my query. Also for task view keep in mind to show only distint values of results:\n\n'
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
            'The output should only steps in natural language need to be followed to generate a good sql query. Make sure all the steps are written in detail and foolows exact requiremnt of user query. If the task is to update a value then make sure to update the particular value in all the instances of the object in other tables also.'
            'Also when joining multiple tables make sure to use Distinct command for the query'
        ),
    },
    {
        'role': 'user',
        'content': f'{query} ',
    },
],options={'temperature': 0})
    result=response['message']['content']
    return result


def CodeGeneratingAgent(query,result):
    response = ollama.chat(model='qwen2.5-coder:3b',messages=[
{
    'role': 'system',
    'content': (
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
f'''
Steps need to be followed to generate the correct results:
{result}
'''
'The output should only be a json with format with key and values as strings in double quotes'
'''
{
    "task": insert', 'delete', 'update' or 'view',
    "SQL Query": "sql guery generated"
}
Do not output anything else besides the json. Make sure end  bracket "}" is there in json. 
'''
    ),
},
{
    'role': 'user',
    'content': f'{query}. ',
},
],options={'temperature': 0})
    result=response['message']['content']
    return result

def return_sql_query(query):
    Agent1_Response = Simplifying_Agent(query)
    CodeGenerator_Agent_Response = CodeGeneratingAgent(query,Agent1_Response)
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

    import json
    start,end=find_braces_indices(CodeGenerator_Agent_Response)
    if end==[]:
        CodeGenerator_Agent_Response+="}"
        end=[len(CodeGenerator_Agent_Response)]
    #print(start,end)
    #print(CodeGenerator_Agent_Response)
    start=start[0]

    end=end[0]
    CodeGenerator_Agent_Response=CodeGenerator_Agent_Response[start:end+1]
    CodeGenerator_Agent_Response=CodeGenerator_Agent_Response.replace("\n","")
    json_result=json.loads(CodeGenerator_Agent_Response)
    return json_result    



def retryQueryGeneratingAgent(sql_query,query,error):
    response = ollama.chat(model='qwen2.5-coder:1.5b',messages=[
{
    'role': 'system',
    'content': (
        'You are a SQL query error handler or sql query for a database with the following schema:\n\n'
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
    assignmentName TEXT NOT NULL, --Name of the assignment
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

f''' Given original query and the error recived after executing the query please revise the query

Based on the error revise the "Original Query" to eliminate the error keeping original objective intact.
'''

'The output should only be a json with format'
'''
{   
    "task": "insert", "delete", "update" or "view",
    "SQL Query": "sql guery generated"
}
Do not output anything else besides the json. Make sure end  bracket "}" is there in json 
'''
    ),
},
{
    'role': 'user',
    'content': f'''User Query: {query}
    Original Query: {sql_query}

    Error Seen: {error}''',
},
],options={'temperature': 0})
    RetryResponse=response['message']['content']
    #print("yash",RetryResponse)
    start,end=find_braces_indices(RetryResponse)
    if end==[]:
        RetryResponse+="}"
        end=[len(RetryResponse)]
    start=start[0]

    end=end[0]
    RetryResponse=RetryResponse[start:end+1]
    RetryResponse=RetryResponse.replace("\n","")
    print(response)
    json_result=json.loads(RetryResponse)
    return json_result

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
