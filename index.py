import streamlit as st

# Set title for the app
st.title("Best-Performing Student Recognition System")

# Create an input field
name = st.text_input("Enter your name:")

# Create a slider to select age
age = st.slider("Select your age:", 1, 100)

# Create a button
if st.button("Submit"):
    # Display the input values when the button is clicked
    st.write(f"Hello, {name}! You are {age} years old.")
