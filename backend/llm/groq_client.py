import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(question, chunks, chat_history=None):
    '''
    RAG Answer with citations for BIS Hackathon TC requirements.
    '''
    if chat_history is None:
        chat_history = []
    
    # Build context
    context = '\\n\\n'.join([
        f"Title: {c.get('title', 'N/A')}\\nSource: {c.get('source', 'N/A')}\\nContent: {c['content']}\\n---"
        for c in chunks[:4]  # Top 4 for token limit
    ])
    
    # History messages
    history_msgs = []
    for h in chat_history[-6:]:  # Last 6 turns
        history_msgs.extend([
            {"role": "user", "content": h["user"]},
            {"role": "assistant", "content": h["assistant"]}
        ])
    
    system_prompt = f'''You are BIS Assistant. Answer accurately about BIS using ONLY the provided context.

IMPORTANT HACKATHON RULES:
- Cite sources with [Source: URL] after relevant facts
- For unknown/off-topic: "Sorry, I can only answer about BIS content from bis.gov.in"
- Structure: Clear, concise, numbered steps for processes
- Multi-turn: Maintain context naturally
- TC-05 Out-of-scope: Gracefully decline non-BIS queries

Context:
{context}'''
    
    messages = [
        {"role": "system", "content": system_prompt},
        *history_msgs,
        {"role": "user", "content": question}
    ]
    
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # Excellent for RAG, available on Groq
            messages=messages,
            temperature=0.1,
            max_tokens=1024
        )
        answer = response.choices[0].message.content
        
        # Extract sources
        sources = list({c['source'] for c in chunks[:4] if c.get('source')})
        
        return {
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}. Ask about BIS certification or standards.",
            "sources": []
        }
