import streamlit as st
from google import genai

# ব্র্যান্ডিং এবং টাইটেল
st.set_page_config(page_title="LumiAI", page_icon="✨")
st.title("✨ LumiAI - Public AI Tool")
st.markdown("---")

# সাইডবারে সেটিংস
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # আগের চ্যাট প্রদর্শন
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # ইনপুট বক্স
        if prompt := st.chat_input("LumiAI কে কিছু জিজ্ঞেস করুন..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Gemini থেকে উত্তর আনা
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt
            )
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")
else:
    st.info("👋 LumiAI-তে স্বাগতম! শুরু করতে বাম পাশের সাইডবারে আপনার Gemini API Key দিন।")
