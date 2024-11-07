# streamlit_app.py

import streamlit as st
from spellcheck import AdvancedSpellChecker

# Initialize the advanced spell checker
checker = AdvancedSpellChecker()

st.title("Advanced Grammarly-Type Spell Checker")
st.subheader("Check your text for spelling errors with contextual awareness")

# Input area for the user to type or paste text
user_input = st.text_area("Enter text to check", "", height=200)

if st.button("Check Text"):
    if user_input.strip():
        # Get corrections for the input text
        corrections = checker.get_corrections(user_input)

        if corrections:
            st.subheader("Context-Aware Corrections Found")
            for idx, correction in enumerate(corrections, start=1):
                st.write(f"**Issue {idx}:** {correction['word']}")
                st.write(f"**Context:** {correction['context']}")
                st.write(f"**Suggestions:** {', '.join(correction['suggestions'])}")
                st.write("---")
            
            if not corrections:
                st.success("No issues found! Your text looks great.")
        else:
            st.success("No spelling errors detected.")
    else:
        st.warning("Please enter some text to check.")
