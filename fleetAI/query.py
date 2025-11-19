from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from secure import KEY
from fleetAI.db import connect_to_quadrant


class QueryRetriever:
    def __init__(self, collection, model_name="gpt-3.5-turbo", temperature=0.1, openai_api_key=KEY):
        self.collection = collection
        self.vector_db = connect_to_quadrant(self.collection)
        self.llm = ChatOpenAI(model_name=model_name,
                              temperature=temperature, 
                              openai_api_key=openai_api_key)
        
        chain_type = self.determine_chain_type()

        self.qa_chain = RetrievalQA.from_chain_type(self.llm,
                                                    chain_type="stuff",
                                                    chain_type_kwargs=chain_type,
                                                    retriever=self.vector_db.as_retriever(), 
                                                    return_source_documents=True)

    def determine_chain_type(self):
        template = """
        Answer the question based on the context below. If the 
        question cannot be answered using the context provided answer 
        with "I don't know". If you don't know then do not return any source documents. 

        {context} 
        Question: {question}
        Answer:"""

        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

        return {"prompt": QA_CHAIN_PROMPT}

    def retrieve(self, query):
        result = self.qa_chain({"query": query})

        if result["result"] == "I don't know.":
            return [result["result"], ""]

        return [result["result"], f"Source: {result['source_documents'][0].metadata['filename']}"]
