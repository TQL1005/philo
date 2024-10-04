from django.http import HttpResponse
from django.shortcuts import render
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# LLM

template = """
    Hello! I will ask you some questions. If, in the course of answering, you need some information about my personal thoughts, don't ask the web: 
    Ask me by eliciting the definition that I already raise up, then from eliciting the definition, try testing the definition with counterexamples. 
    After that, revise the definition and further examine it. Next, try to help me realize the ignorance of the statement I first introduce, 
    and then continue the inquiry in a way that an 8-year-old can understand so I can be skeptical about my assumptions.
    don't repeat my requirement above and jump straight in to answer my question.   
    Try to raise short questions and use a witty tone so I am very happy to provide such information 

    Is that ok?

    Now, answer the user's question below:
    Here is the conversation history : {context}
    User's Question : {question}
    Answer:
"""
model = OllamaLLM(model="llama3.1")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Initialize a dictionary to hold contexts for multiple users
user_contexts = {}


def handle_conversation(user_id, user_message):
    # Get the user's context or create a new one if it doesn't exist
    context = user_contexts.get(user_id, "")

    # Invoke the model with the current context and user message
    result = chain.invoke({"context": context, "question": user_message})

    # Update the context with the new interaction
    user_contexts[user_id] = f"{context}\nUser: {user_message}\nAI: {result}"

    return result


# Create your views here.
def main(request):
    context = {}
    return render(request, 'socrate/main.html', context)


def getResponse(request):
    user_id = request.session.session_key  # Use session key as a user identifier
    user_message = request.GET.get('userMessage')

    # Ensure user_message is not None or empty
    if user_message:
        bot_response = handle_conversation(user_id, user_message)
        return HttpResponse(bot_response)
    else:
        return HttpResponse("No user message provided.")
