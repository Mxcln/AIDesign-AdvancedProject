from langchain_openai import OpenAI
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain

class Summarizer:
    def __init__(self, openai_api_key):
        self.llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
        self.chain = load_summarize_chain(self.llm, chain_type='map_reduce')

    def summarize_text(self, txt):
        text_splitter = CharacterTextSplitter()
        texts = text_splitter.split_text(txt)
        docs = [Document(page_content=t) for t in texts]
        return self.chain.invoke(docs)['output_text']

# Usage:
# summarizer = Summarizer("sk-...")
# summary = summarizer.summarize_text("Your text here.")
# print(summary)