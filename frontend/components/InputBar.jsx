import { useState } from 'react';
import { Button } from './ui/button';

export default function InputBar({ onSend, disabled }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSend(input);
      setInput('');
    }
  };

  return (
    <form className="input-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask about BIS certification, ISI mark, hallmarking..."
        disabled={disabled}
      />
      <Button type="submit" disabled={disabled || !input.trim()}>
        {disabled ? '...' : 'Send'}
      </Button>
    </form>
  );
}

