import streamlit as st # Frontend 
import json # Data Handling, Rank Calcuatin 
import pandas as pd # for Data displaying results in st

# TODO : need to train model based on colelcted data
def calculate_overall_score(student):
    score = student["Academicscore"] * 0.5 + student["ConsistencyScore"] * 0.1 +  student["CoreCoursesScore"] * 0.15 + student["Hackathons"] * 10 + student["PaperPresentations"] * 5 + student["AssistanceScore"] * 0.5
    return round(score,2)

# TODO : ranks are going to given by diversfying order based on Feature importance 
def assign_rank(students):
    for student in students:
        student["Overallscore"] = calculate_overall_score(student)
        student["Overallscore"] = round(student["Overallscore"],2)
        
    sorted_students = sorted(students, key=lambda x: x["Overallscore"], reverse=True)

    for rank, student in enumerate(sorted_students, start=1):
        student["Rank"] = rank

    return sorted_students

# adding student 
def add_student(student_data, filename='students.json'):
    try:
        with open(filename, 'r') as file:
            students = json.load(file)
    except FileNotFoundError:
        students = []

    students.append(student_data)

    with open(filename, 'w') as file:
        json.dump(students, file, indent=4)

# Function to display results
def display_results(filename='students.json'):
    try:
        with open(filename, 'r') as file:
            students = json.load(file)
    except FileNotFoundError:
        st.error("No data found.")
        return []

    ranked_students = assign_rank(students)
    return ranked_students

# Set page layout and theme
st.set_page_config(page_title="Best-Performing Student Recognition System", layout="wide")

# Main title of the app
st.markdown("<h1 style='text-align: center;'>Best-Performing Student Recognition System</h1>", unsafe_allow_html=True)

# Center the logo image
st.image("media/rgm_logo.jpg", width=110, use_column_width=False)  

col1, col2 = st.columns([1, 1])  

with col1:
    st.markdown("<h3 style='text-align: center;'>Rajeev Gandhi Memorial College of Engineering & Technology</h3>", unsafe_allow_html=True)

with col2:
    st.markdown("<h3 style='text-align: center;'>Dept of Computer Science Engineering</h3>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)


col1, col2 = st.columns([7, 3])  # Adjust proportions as needed

with col1:
    # Display results
    student_results = """
        <h3 style='font-weight: bold; margin: 0;'>🎓 Rankings Criteria and Student Results</h3>
    """
    st.markdown(student_results, unsafe_allow_html=True)

    ranked_student = display_results() 

    if ranked_student:
        df = pd.DataFrame(ranked_student)
        df['Overallscore'] = (df['Overallscore'] / df['Overallscore'].max()) * 100
        
        def rank_symbol(rank):
            if rank == 1:
                return "🏆"  
            elif rank == 2:
                return "🥈"  
            elif rank == 3:
                return "🥉"  
            return str(rank)  

        df['Rank'] = df['Rank'].apply(rank_symbol)
        
        st.dataframe(df[['Rank', 'Name', 'Batch', 'Academicscore','ConsistencyScore' , 'CoreCoursesScore' , 'Hackathons', 'PaperPresentations', 'AssistanceScore' , 'Overallscore']], width=700, hide_index=True)
    else:
        st.dataframe(ranked_student[['Rank', 'Name', 'Batch', 'Academicscore','ConsistencyScore' , 'CoreCoursesScore' , 'Hackathons', 'PaperPresentations', 'AssistanceScore' , 'Overallscore']], width=700, hide_index=True)


with col2:
    ranking_criteria = [
        "Academic Performance (50%)",
        "Consistency over Semesters (10%)",
        "Excellence in Core Engineering Courses (15%)",
        "Hackathon Participation (10%)",
        "Paper Presentations (10%)",
        "Teacher Assistance and Contributions (5%)"
    ]
    
    criteria_html = """
    <div style='background-color: #f9f9f9; border: 1px solid #e0e0e0; padding: 15px; border-radius: 5px;'>
        <h3 style='font-weight: bold; margin: 0;'>❕ Ranking Criteria</h3>
        <ul style='list-style-type: disc; padding-left: 20px; margin-top: 10px;'>
    """
    
    for criterion in ranking_criteria:
        criteria_html += f"<li style='margin: 5px 0; font-size: 18px; color: #333;'>{criterion}</li>"
    
    criteria_html += """
    <div style='font-size: 16px; color: #666; margin-top: 10px;'>
        Note: The ranking system uses machine learning to dynamically adjust weights based on overall student performance and contributions.
    """
    
    st.markdown(criteria_html, unsafe_allow_html=True)


st.markdown("### Add New Student")
with st.form(key='student_form'):
    name = st.text_input("Name")
    
    # Batch dropdown from 1995 to 2025
    batch_options = [str(year) for year in range(1995, 2026)]  # List of years as strings
    batch = st.selectbox("Batch", batch_options)
    
    # Academic Score should accept values from 0-99
    academic_score = st.number_input("Academic Score", min_value=0, max_value=99)

    #Consistency over semesters
    consistency_score = st.number_input("ConsistencyScore", min_value=0, max_value=99)

    #Excellencein Core Engineering Courses
    core_courses_score = st.number_input("CoreCoursesScore", min_value=0, max_value=99)
    
    # Hackathons input with options 1-10 or 10+
    hackathons = st.number_input("Hackathons", min_value=0, max_value=99)
    
    # Paper Presentations input with options 1-10 or 10+
    paper_presentations = st.number_input("PaperPresentations", min_value=0, max_value=99)
    
    #Teacher Assistance and contributions
    assistance_score = st.number_input("AssistanceScore", min_value=0, max_value=99)
    
    submit_button = st.form_submit_button("Add Student")
    
    if submit_button:
        # Convert hackathons and paper_presentations to integers for processing
        hackathons_count = 10 if hackathons == "10+" else int(hackathons)
        paper_presentations_count = 10 if paper_presentations == "10+" else int(paper_presentations)

        new_student = {
            "Name": name,
            "Batch": batch,
            "Academicscore": academic_score,
            "ConsistencyScore": consistency_score,
            "CoreCoursesScore": core_courses_score,
            "Hackathons": hackathons_count,
            "PaperPresentations": paper_presentations_count,
            "AssistanceScore": assistance_score
        }
        add_student(new_student)
        st.success(f"Added student: {name}")




