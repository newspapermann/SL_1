#https://docs.streamlit.io/develop/tutorials/llms
#https://platform.openai.com/settings/organization/usage
#https://console.groq.com/playground
#https://pypi.org/project/phidata/

#conda activate streamlitenv
#streamlit run agent_web_search.py

import streamlit as st
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.googlesearch import GoogleSearch
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

################################################################ Main Streamlit app starts here

def create_agent():
    return Agent(
        name="Web Research Assistant",
        description="I am an AI research assistant that combines web search results with analytical insights.",
        task="Research topics and provide both factual summaries and analytical insights in an integrated response.",
        model=OpenAIChat(
            id='gpt-4o-mini',
            api_key=st.secrets["OPENAI_API_KEY"],
            temperature=0.7
        ),
        tools=[GoogleSearch(fixed_max_results=8).google_search(max_results=8)],
        show_tool_calls=True,
        markdown=True,
        instructions=[
            "Blend web sources and AI analysis seamlessly",
            "Start with key findings from sources",
            "Follow with analytical insights and implications",
            "Make connections between different sources",
            "Highlight emerging trends and patterns"
        ],
        guidelines=[
            "Structure: Begin with '🔍 Key Findings:', followed by '💡 Analysis:'",
            "Keep paragraphs concise and focused",
            "Use bullet points for main ideas",
            "Always cite sources inline",
            "Maintain a conversational yet professional tone"
        ]
    )

def main():
    if not check_password():
        st.stop()  # Do not continue if check_password is not True.
    
    #st.title("AI Web Search Assistant")
    st.sidebar.subheader("Prompt engineering tips")
    st.sidebar.caption("By adjusting the Agent class setting input parameters: 'description', 'task', 'instructions' and 'guidelines' for better results.")
    # Initialize agent in session state
    if 'agent' not in st.session_state:
        st.session_state.agent = create_agent()
        
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    # Search interface
    if query := st.chat_input("What are you searching for?"):
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"): # Display user message in chat message container
            st.markdown(query)
            
    # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
            # Get direct response from agent
                response = st.session_state.agent.run(
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages], 
                    stream=False,)
                st.markdown(response.content)       
        st.session_state.messages.append({"role": "assistant", "content": response.content})          
                
if __name__ == "__main__":
    main()