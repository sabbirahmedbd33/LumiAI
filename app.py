import streamlit as st
from google import genai

# ব্র্যান্ডিং এবং টাইটেল
st.set_page_config(page_title="LumiAI", page_icon="✨")
st.title("✨ LumiAI - Developed by Sabbir Ahmed")
st.markdown("---")

# সেটিংস: এখানে সিক্রেটস থেকে API Key নেবে
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.sidebar.warning("API Key not found in Secrets! Please add it in Streamlit settings.")
    api_key = None

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
            # শুরুর মেসেজ
            st.session_state.messages.append({"role": "assistant", "content": "হ্যালো! আমি LumiAI। আমাকে তৈরি করেছেন সাব্বির আহমেদ। আমি আপনাকে কীভাবে সাহায্য করতে পারি?"})

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("LumiAI কে কিছু জিজ্ঞেস করুন..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # AI-কে আপনার পরিচয় শিখিয়ে দেওয়ার ইন্সট্রাকশন
            system_instruction = "Your name is LumiAI. You are a helpful AI assistant created by Sabbir Ahmed, who is a professional SEO expert from Bangladesh. Always be polite and remember your creator."
            
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=f"{system_instruction}\n\nUser: {prompt}"
            )
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error("দুঃখিত, একটি কারিগরি সমস্যা হয়েছে। কিছুক্ষণ পর আবার চেষ্টা করুন।")
else:
    st.info("অ্যাপটি চালু করতে Streamlit Secrets-এ API Key যোগ করুন।")
