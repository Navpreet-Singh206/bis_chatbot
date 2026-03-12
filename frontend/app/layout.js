import '../styles/global.css';

export const metadata = {
  title: 'BIS Assistant - Bureau of Indian Standards Chatbot',
  description: 'Ask about BIS certification, ISI mark, hallmarking, and more',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

