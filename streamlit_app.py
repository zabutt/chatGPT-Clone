from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="ChatGPT-like clone", page_icon="🤖")

st.title("ChatGPT-like clone by Zulfiqar")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.beta_expander(message["role"], expanded=False):
        st.markdown(message["content"])

if prompt := st.text_input("Ask me anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.beta_expander("Your question", expanded=False):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    with st.beta_expander("My answer", expanded=False):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

