import React from 'react';
// import ChatbotUI from '@site/src/components/ChatbotUI';
import ChatbotUI from '@site/src/components/Chatbot';

// Default implementation, that you can customize
export default function Root({children}) {
  return (
    <>
      {children}
      <ChatbotUI /> {/* Add the Chatbot component here */}
    </>
  );
}
