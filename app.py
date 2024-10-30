import google.generativeai as genai
import streamlit as st

# Configure API key
test_string = st.secrets["test_string"] 
genai.configure(api_key=test_string)

# Initialize conversation history log
conversation_log = []

def generate_prompt(user_input):
    # Check for empty input
    if not user_input.strip():
        return "Please provide a valid input."
    
    # Summarize previous conversations if any
    summary = "\n".join([f"User: {log['question']} AI: {log['response_summary']}" for log in conversation_log])
    prompt = f"{summary}\nUser: {user_input}\nAI:"
    return prompt

# Streamlit UI
st.title("Chat with AI")

# User input
user_input = st.text_input("Enter your question", "")

if user_input:
    # Generate the prompt with memory
    Question = generate_prompt(user_input)

    # Use the generative AI model to get the response
    with st.spinner("AI is thinking..."):
        try:
            model = genai.GenerativeModel('gemini-pro')  # Check the model name
            response = model.generate_content(Question)
            st.write(f"**AI:** {response.text}")

            # Save interaction in conversation log
            conversation_log.append({
                'question': user_input,
                'response_summary': response.text[:100]  # Store a summary or snippet
            })
        except Exception as e:
            st.error(f"Error: {e}")
