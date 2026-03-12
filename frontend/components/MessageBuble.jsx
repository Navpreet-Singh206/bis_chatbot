export default function MessageBubble({ message, isUser, avatar }) {
  // Function to convert URLs to clickable links
  const parseMessage = (text) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const parts = text.split(urlRegex);
    
    return parts.map((part, i) => {
      if (part.match(urlRegex)) {
        return (
          <a 
            key={i} 
            href={part} 
            target="_blank" 
            rel="noopener noreferrer"
            className="source-link"
          >
            {part}
          </a>
        );
      }
      return part;
    });
  };

  return (
    <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
      {!isUser && avatar && <div className="avatar">{avatar}</div>}
      <div className="message-content">
        {message.split('\n').map((line, i) => (
          <p key={i}>{parseMessage(line)}</p>
        ))}
      </div>
      {isUser && avatar && <div className="avatar user-avatar">{avatar}</div>}
    </div>
  );
}

