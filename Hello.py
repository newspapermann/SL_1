#https://docs.streamlit.io/develop/tutorials/llms
#https://platform.openai.com/settings/organization/usage
#conda activate streamlitenv
#streamlit run Hello.py

import streamlit as st
from openai import OpenAI
import hmac

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Main Streamlit app starts here

#with st.sidebar:
#    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    
#st.title("ChatGPT-like clone")

# Get OpenAI API key from Input
    #client = OpenAI(api_key=openai_api_key)
    
# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    #if not openai_api_key:
    #    st.info("Please add your OpenAI API key to continue.")
    #    st.stop()
    
    # Get OpenAI API key from Input
    #client = OpenAI(api_key=openai_api_key)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    
###Custom domain
#https://ploomber.io/blog/streamlit-custom-domain/
#https://stackoverflow.com/questions/70250954/how-does-one-display-a-url-in-the-address-bar-when-running-streamlit
#https://discuss.streamlit.io/t/how-do-i-connect-a-recently-purchased-domain-name-and-have-it-point-to-my-strreamlit-app-url/42739

###Deploy on AWS
#Medium PDF
#https://discuss.streamlit.io/t/streamlit-deployment-guide-wiki/5099
#https://stackoverflow.com/questions/69676247/streamlit-hosting
#https://appliku.com/guides/how-to-deploy-streamlit-app-on-your-server/

###iFrame on Streamlit webapp
#https://giswqs.medium.com/add-a-custom-domain-to-your-streamlit-web-app-daed6d11dd72
#https://discuss.streamlit.io/t/using-our-own-domain-instead-of-subdomain-of-streamlit-i-e-streamlit-app/76157
#https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app/embed-your-app
#https://discuss.streamlit.io/t/i-would-like-to-hide-full-screen-and-built-with-streamlit-when-embed-true/52607/5

###Prompt Engineering
#https://huggingface.co/docs/transformers/en/tasks/prompting
#https://www.cmswire.com/digital-marketing/gemini-gems-vs-chatgpt-customgpts-a-marketers-guide-to-ai-mini-agents/
#PDFs
