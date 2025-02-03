from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def answer_question_with_context(conversation_history, question):
    context = "You are a P6 Chatbot, a personal assistant to help answer all user questions"

    # Combine conversation history with retrieved documents
    full_context = conversation_history + "\n\n" + context

    # Define the RAG prompt template
    RAG_TEMPLATE = """
    You are P6 Chatbot, a personal assistant to help answer the user's question. Provide a response that fits the context of the user's question. Responses are given using the language spoken by the user.
    
    <context>
    {context}
    </context>

    Answer the following question:

    {question}"""

    rag_prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)
    model = ChatOllama(
        model="qwen2.5:32b-instruct-q3_K_M",
        repetition_penalty=1.05,
        temperature=0.7,
        top_p=0.8,
        top_k=20,
        transformers_version=4.46,
        system="You are a helpful assistant to help answer all user questions"
    )

    chain = (
        RunnablePassthrough.assign(context=lambda input: input["context"])
        | rag_prompt
        | model
        | StrOutputParser()
    )

    response = chain.invoke({"context": full_context, "question": question, "history": conversation_history})
    return {"response": response}
