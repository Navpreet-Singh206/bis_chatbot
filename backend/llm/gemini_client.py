import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

def generate_answer(question, chunks, chat_history=None):
    '''
    Fallback Gemini RAG Answer.
    '''
    if chat_history is None:
        chat_history = []
    
    context = '\n\n'.join([
        f"Title: {c.get('title', 'N/A')}\nSource: {c.get('source', 'N/A')}\nContent: {c['content']}\n---"
        for c in chunks[:4]
    ])
    
    history_msgs = []
    for h in chat_history[-6:]:
        history_msgs.extend([
            h["user"],
            h["assistant"]
        ])
    
    system_prompt = f'''You are BIS Assistant. Answer using ONLY context.

Context:
{context}'''
    
    full_prompt = f"{system_prompt}\n\nHistory: {' | '.join(history_msgs[-12:])}\n\nQ: {question}"
    
    try:
        response = model.generate_content(full_prompt)
        answer = response.text
        
        sources = list({c['source'] for c in chunks[:4] if c.get('source')})
        
        return {
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        return {
            "answer": f"Gemini error: {str(e)}. Check API key.",
            "sources": []
        }
