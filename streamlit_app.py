import streamlit as st
import openai
import requests

def generate_response(prompt, model, api_key):
    if model == "OpenAI":
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    elif model == "Claude":
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'prompt': prompt,
            'model': 'claude-v1',
            'max_tokens': 150
        }
        response = requests.post('https://api.anthropic.com/v1/complete', headers=headers, json=data)
        return response.json()['completion']

def code_interpreter(code):
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return exec_globals
    except Exception as e:
        return str(e)

st.title("AI 챗봇 및 코드 인터프리터")

# User input for API keys
openai_api_key = st.text_input("OpenAI API 키를 입력하세요:", type="password")
claude_api_key = st.text_input("Claude API 키를 입력하세요:", type="password")

# Select AI model
model_option = st.selectbox("AI 모델 선택:", ["OpenAI", "Claude"])

# User input for chatbot
user_input = st.text_input("당신: ", "")

if user_input and model_option and (model_option == "OpenAI" and openai_api_key or model_option == "Claude" and claude_api_key):
    response = generate_response(user_input, model_option, openai_api_key if model_option == "OpenAI" else claude_api_key)
    st.text_area("챗봇:", value=response, height=200)

# User input for code execution
code_input = st.text_area("실행할 Python 코드를 입력하세요:", height=150)

if st.button("코드 실행"):
    if code_input:
        output = code_interpreter(code_input)
        st.text_area("코드 출력:", value=str(output), height=200)
    else:
        st.warning("실행할 코드를 입력해 주세요.")
