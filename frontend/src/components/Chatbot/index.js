import React, { useState } from 'react';
import FloatingButton from './FloatingButton';
import ChatWindow from './ChatWindow';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      <FloatingButton onClick={toggleChat} />
      {isOpen && <ChatWindow onClose={toggleChat} />}
    </>
  );
};

export default Chatbot;