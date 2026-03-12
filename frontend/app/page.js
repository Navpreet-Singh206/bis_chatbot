'use client';

import Chatbox from '../components/chatbox';
import { useEffect } from 'react';

export default function Home() {
  useEffect(() => {
    // Ensure no page scroll
    document.body.style.overflow = 'hidden';
  }, []);

  return (
    <div className="scrollable-chat-wrapper">
      <Chatbox />
    </div>
  );
}

