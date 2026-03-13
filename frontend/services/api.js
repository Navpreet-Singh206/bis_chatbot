const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

export const sendMessage = async (question, history = []) => {
  try {
    // Map history correctly: user messages have role='user', assistant have role='assistant'
    const formattedHistory = history.map(h => ({
      user: h.role === 'user' ? h.content : '',
      assistant: h.role === 'assistant' ? h.content : ''
    })).filter(h => h.user || h.assistant);

    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        question,
        history: formattedHistory
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to get response');
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    return {
      answer: 'Sorry, I encountered an error. Please try again.',
      sources: []
    };
  }
};

