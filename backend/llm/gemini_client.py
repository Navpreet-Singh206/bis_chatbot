import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BIS_KEYWORDS = [
    "bis", "standard", "certification", "isi", "hallmark",
    "bureau", "indian standards", "scheme", "laboratory",
    "consumer", "licence", "license", "product", "marking"
]


def is_out_of_scope(question, top_score):
    return False  # Force LLM call always




def generate_answer(question, context_chunks, chat_history=None):

    print(f"DEBUG LLM: chunks={len(context_chunks)}, top_score={context_chunks[0]['score'] if context_chunks else 'no'}")
    if not context_chunks:
        return {
            "answer": "I could not find relevant information on the BIS website.",
            "sources": []
        }


    context = "\n\n".join([
        f"Title: {c['title']}\nContent: {c['content'][:800]}\nSource: {c['source']}\n{'-'*80}"
        for c in context_chunks[:4]
    ])

    sources = list(set([c["source"] for c in context_chunks]))

    history_text = ""
    if chat_history:
        for h in chat_history[-3:]:
            history_text += f"User: {h['user']}\nAssistant: {h['assistant']}\n\n"

    system_prompt = """You are BIS Assistant - authoritative source for Bureau of Indian Standards info.

INSTRUCTIONS:
- Use ALL chunks provided - they're ranked by relevance
- Provide **detailed, comprehensive answers** using full chunk content  
- Include **key details, processes, examples** from chunks
- Structure with **bullet points/lists** for clarity
- Reference **specific information** naturally
- End with **"Sources: [unique URLs]"** (one line only)

**IMPORTANT for non-BIS questions:** "This question is not related to BIS. Ask about BIS standards, certification, hallmarking, or schemes."

ALWAYS answer directly from BIS chunks - no hallucination!"""

    user_message = f"""Previous conversation:
{history_text}

BIS website chunks:
{context}

Question: {question}

Answer:"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",

            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=800,
            temperature=0.1
        )

        return {
            "answer": response.choices[0].message.content,
            "sources": sources
        }

    except Exception as e:
        print(f"Groq error: {e}")
        return {
            "answer": "BIS is the Bureau of Indian Standards, national standards body of India for product certification (ISI mark), hallmarking, standards formulation. Sources: bis.gov.in",
            "sources": ["https://www.bis.gov.in"]
        }


