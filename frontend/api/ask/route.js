import Groq from 'groq-sdk';
import chunksData from '../../../backend/data/chunks.json' with { type: 'json' };

const client = new Groq({ apiKey: process.env.GROQ_API_KEY });

// Fixed search for array chunks + metadata structure
function searchChunks(question, chunksArray, metadataArray, topK = 6) {
  const qLower = question.toLowerCase();
  const qWords = new Set(qLower.split(/\s+/).filter(w => w.length > 3));
  
  if (qWords.size === 0) {
    // Fallback to top chunks
    return chunksArray.slice(0, topK).map((chunk, i) => ({
      content: chunk,
      title: metadataArray[i]?.title || 'BIS Information',
      source: metadataArray[i]?.source || 'https://bis.gov.in'
    }));
  }
  
  const scored = chunksArray.map((chunk, i) => {
    const title = metadataArray[i]?.title || '';
    const textLower = (title + ' ' + chunk).toLowerCase();
    const titleMatches = Array.from(qWords).filter(w => title.toLowerCase().includes(w)).length * 2; // Weight title higher
    const contentMatches = Array.from(qWords).filter(w => textLower.includes(w)).length;
    const matches = titleMatches + contentMatches;
    const score = matches / (qWords.size * 3); // Normalize
    return { chunk: { content: chunk, title, source: metadataArray[i]?.source || 'https://bis.gov.in' }, score };
  })
  .sort((a, b) => b.score - a.score)
  .slice(0, topK)
  .map(item => item.chunk);
  
  return scored.length > 0 ? scored : chunksArray.slice(0, topK).map((chunk, i) => ({
    content: chunk,
    title: metadataArray[i]?.title || 'BIS Information',
    source: metadataArray[i]?.source || 'https://bis.gov.in'
  }));
}

export async function POST(request) {
  const { question } = await request.json();
  
  try {
    const relevantChunks = searchChunks(question, chunksData.chunks, chunksData.metadata);
    
    const context = relevantChunks.map(c => 
      `TITLE: ${c.title}\nCONTENT: ${c.content.substring(0, 1400)}\nPAGE: ${c.source}`
    ).join('\n\n==================\n\n');
    
    const sources = Array.from(new Set(relevantChunks.map(c => c.source)));

    const messages = [{
      role: 'system',
      content: `You are BIS Assistant. EXCLUSIVELY use the EXACT content from provided BIS website chunks below. 

ABSOLUTE RULES - VIOLATION = BAD RESPONSE:
1. Generate LONG comprehensive answer (500-1200 words) using ALL chunk details
2. Bullet points/numbers for processes, lists for requirements
3. Steps, documents, fees, timelines, examples from chunks ONLY
4. NO "Sources:", NO URLs, NO citations, NO "based on", NO references in answer
5. Structure: Intro + Details + Summary. Professional tone.

CHUNKS: ${context}`
    }, {
      role: 'user',
      content: question
    }];

    const completion = await client.chat.completions.create({
      messages,
      model: 'llama3-70b-8192',
      max_tokens: 2000,
      temperature: 0.0
    });

    return Response.json({ 
      answer: completion.choices[0].message.content.trim(),
      sources 
    });
  } catch (error) {
    console.error('Error:', error);
    return Response.json({ 
      answer: 'Technical issue. BIS manages standards and certification - see https://bis.gov.in',
      sources: ['https://bis.gov.in']
    });
  }
}
