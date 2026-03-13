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
        for c in chunks[:6]  # Use top 6 for richer context
    ])
    
    # History messages
    history_msgs = []
    for h in chat_history[-8:]:  # Last 8 turns for better memory
        history_msgs.extend([
            {"role": "user", "content": h["user"]},
            {"role": "assistant", "content": h["assistant"]}
        ])
    
    system_prompt = f'''You are BIS Assistant - Bureau of Indian Standards expert. Use ONLY the provided context to give comprehensive, detailed answers about BIS services, certification, hallmarking, standards, labs.

LONG DETAILED ANSWERS REQUIRED:
- Provide complete step-by-step processes (numbered lists)
- Explain technical terms, eligibility criteria, documents needed
- Include timelines, costs, links where available
- Compare schemes/options when relevant
- Use professional tone suitable for consumers/businesses
- Cite [Source: URL] after key facts

If question unclear or not in context: "This information is not available in BIS website data. Ask about certification, hallmarking, standards or schemes."

Context ({len(chunks)} sources):
{context}'''
    
    messages = [
        {"role": "system", "content": system_prompt},
        *history_msgs,
        {"role": "user", "content": question}
    ]
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Updated model (llama3-70b-8192 deprecated)
            messages=messages,
            temperature=0.3,
            max_tokens=2048  # Longer detailed responses
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

