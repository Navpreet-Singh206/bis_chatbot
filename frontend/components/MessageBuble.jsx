export default function MessageBubble({ message, sources = [], isUser, avatar }) {
  // Strip any leaked "Sources: ..." text from LLM
  const cleanMessage = message.replace(/Sources?:[^•]*$/i, '').replace(/\n{2,}Sources?:/i, '').trim();

  // Parse remaining text for inline URLs
  const parseMessage = (text) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const parts = text.split(urlRegex);
    
    return parts.map((part, i) => 
      part.match(urlRegex) ? (
        <a key={i} href={part} target="_blank" rel="noopener noreferrer" className="source-link">
          {part}
        </a>
      ) : part
    );
  };

  // Render ONLY clickable sources footer (non-user only)
  const renderSources = () => {
    if (!sources?.length || isUser) return null;
    
    return (
      <div className="sources-section">
        <div className="sources-label">📚 Sources:</div>
        <div className="sources-list">
          {sources.map((source, i) => {
            const fullUrl = source.startsWith('http') ? source : `https://${source}`;
            return (
              <a
                key={i}
                href={fullUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="source-link"
              >
                {source.replace(/^https?:\/\//, '')}
              </a>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
      {!isUser && avatar && <div className="avatar">{avatar}</div>}
      <div className="message-content">
        {cleanMessage.split('\n').map((line, i) => (
          <p key={i}>{parseMessage(line)}</p>
        ))}
        {renderSources()}
      </div>
      {isUser && avatar && <div className="avatar user-avatar">{avatar}</div>}
    </div>
  );
}
