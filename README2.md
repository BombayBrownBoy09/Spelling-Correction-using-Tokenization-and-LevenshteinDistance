# Spell Checker

This repository contains a context-aware spell-checking application that functions like a Grammarly-type service. It uses advanced NLP techniques to suggest spelling and grammar corrections, taking the context of each word into account.

## Features
- **Context-Aware Spell Checking**: Uses a pre-trained language model to provide corrections based on the context in which a word is used.
- **Top Suggestions**: Displays the top three suggested replacements for detected spelling errors.
- **Streamlit Interface**: A user-friendly web interface for checking text and viewing corrections.

## Files
- `spellcheck.py`: Contains the `AdvancedSpellChecker` class, which performs the spell-checking and suggests corrections based on a pre-trained transformer model.
- `streamlit_app.py`: The main script for running the Streamlit web app that interacts with `spellcheck.py`.

## Technologies Used
- **Python**: The core programming language.
- **Hugging Face Transformers**: For integrating a pre-trained language model (e.g., `bert-base-uncased`).
- **Streamlit**: For creating a web interface.
- **NLTK**: For tokenizing text input.

