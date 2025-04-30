import streamlit as st
import os

import google.generativeai as genai

#-------------------------------------api-----------------------------------------------


# get gemini api
gemini_api_key = st.secrets["GEMINI_API_KEY"]
if not gemini_api_key:
    st.error("❌ API not found")
    st.stop

#configure gemini api
genai.configure(api_key=gemini_api_key)
gemini_model = genai.GenerativeModel('gemini-1.5-pro-latest')

#-----------------------------------ui--------------------------------------------------

# layout
st.set_page_config(layout="wide")

# heading
st.title("Your Words, AI's Speed: The Ultimate Writing Sidekick")

# sub title
st.header("Why Spend Hours Drafting When AI Can Polish Your Thoughts in Minutes?")

# initialize session state to generate blog
if "generated blog" not in st.session_state:
    st.session_state.generated_blog=None

    # side bar inputs
    with st.sidebar:
        st.title("Blog Settings")
        blog_title = st.text_input("Blog Title", "How to Start a Successful Blog")
        blog_keywords = st.text_input("Keywords (comma separated)", "blogging, writing, content")
        word_count = st.slider("Word Count", min_value=250, max_value=1000, value=500)


        if st.button("Generate Blog"):
            try:
                st.session_state.generated_blog=None

                with st.spinner("Generating blog ..... "):
                    try:
                        prompt=[f"Generate a comprehensive, engaging blog post relevant to the given title \"{blog_title}\" and keywords \"{blog_keywords}\". Make sure to incorporate these keywords in the blog post. The blog should be approximately {word_count} words in length, suitable for an online audience. Ensure the content is original, informative, and maintains a consistent tone throughout."]

                        response=gemini_model.generate_content(prompt)
                        st.session_state.generated_blog=response.text
                        st.success("✨ Blog generated successfully! 🎉😎")
                    except Exception as e:
                        st.error("❌ Blog generation failed. ")
                        st.stop()
            except Exception as e:
                st.error("⚠️ An unexpected error occurred. Please try again or check your connection.")

# displaying generated blog
if st.session_state.generated_blog:
    st.subheader("Generated Blog Post")
    st.markdown(st.session_state.generated_blog)
else:
    st.info("Enter your blog details in the sidebar and click 'Generate Blog Post'")




    


