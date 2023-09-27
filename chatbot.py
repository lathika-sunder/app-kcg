import os
import streamlit as st
os.environ["OPENAI_API_KEY"] = "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"

from langchain.document_loaders import WebBaseLoader

loader = WebBaseLoader(["https://www.linkedin.com/jobs"])
scrape_data = loader.load()
from langchain.indexes import VectorstoreIndexCreator

index = VectorstoreIndexCreator().from_loaders([loader])
st.image("https://tekmonks.com/apps/tekmonks/articles/.home/logo.png/logo.png")

text=st.text_input(label="Enter ur Company related queries...")

if text:
    print("hi")
    st.write(index.query(text))