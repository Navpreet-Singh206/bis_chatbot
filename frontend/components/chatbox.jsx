'use client';

import { useState, useRef, useEffect } from 'react';
import MessageBubble from './MessageBuble';
import InputBar from './InputBar';
import { sendMessage } from '../services/api';
import { User, Loader2 } from 'lucide-react';

export default function Chatbox() {
  const [messages, setMessages] = useState([
    { 
      role: 'assistant', 
      content: 'Hello! I am your BIS Assistant. Ask me about Bureau of Indian Standards, ISI certification, hallmarking, or how to get your product certified.',
      sources: []
    }
  ]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (question) => {
    const userMessage = { role: 'user', content: question, sources: [] };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const history = messages.filter(m => m.role !== 'system');
      const response = await sendMessage(question, history);
      
      const assistantMessage = { 
        role: 'assistant', 
        content: response.answer || 'No response received.',
        sources: response.sources || [] 
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.',
        sources: []
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chatbox">
      <div className="chat-header">
        <div className="header-content">
          <img src="/bis-logo.webp" alt="BIS Logo" width={48} height={48} className="robot-icon" />
          <div>
            <h1>BIS Assistant</h1>
            <p>🤖 Your AI expert for BIS queries</p>
          </div>
        </div>
      </div>
      
      <div className="messages-container">
        {messages.map((msg, index) => (
          <MessageBubble 
            key={index} 
            message={msg.content} 
            sources={msg.sources || []}
            isUser={msg.role === 'user'} 
            avatar={msg.role === 'assistant' ? <img src="/bis-logo.webp" alt="BIS" width={32} height={32} className="avatar-icon" /> : <User className="avatar-icon user-avatar" />}
          />
        ))}
        {loading && (
          <div className="message-bubble assistant">
            <div className="avatar">
              <img src="/bis-logo.webp" alt="BIS" width={32} height={32} className="avatar-icon" />
            </div>
            <div className="typing-container">
              <Loader2 className="typing-dots" />
              <div className="typing-text">BIS Assistant is thinking...</div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <InputBar onSend={handleSend} disabled={loading} />
    </div>
  );
}
