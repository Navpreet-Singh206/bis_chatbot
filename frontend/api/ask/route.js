import Groq from 'groq-sdk';
import chunksData from '../../../backend/data/chunks.json' with { type: 'json' };

const client = new Groq({ apiKey: process.env.GROQ_API_KEY });

export async function POST(request) {
  const { question, history } = await request.json();

  // Simple search
  const chunks = chunksData.chunks.slice(0, 5);
  const context = chunks.join('\\n');

  try {
    const chatCompletion = await client.chat.completions.create({
      messages: [
        { role: 'system', content: 'BIS expert. Use context.' },
        { role: 'user', content: `Context: ${context} Question: ${question}` }
      ],
      model: 'llama3-70b-8192',
    });

    return Response.json({ 
      answer: chatCompletion.choices[0]?.message?.content || 'BIS standards expert.',
      sources: ['bis.gov.in']
    });
  } catch (e) {
    return Response.json({ answer: 'Sorry, try again. BIS certification info.', sources: [] });
  }
}
