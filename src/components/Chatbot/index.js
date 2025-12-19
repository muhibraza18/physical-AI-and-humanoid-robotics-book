import React, { useState, useEffect, useCallback } from 'react';
import FloatingButton from './FloatingButton';
import ChatWindow from './ChatWindow';
import ChatService from './ChatService';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [messages, setMessages] = useState([
    { type: 'bot', text: 'Hello! How can I help you understand this book?' }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [chatMode, setChatMode] = useState('book'); // 'book' or 'selection'

  const handleTextSelection = useCallback(() => {
    const text = window.getSelection().toString().trim();
    if (text.length > 0) {
      setSelectedText(text);
      setChatMode('selection'); // Switch to selection mode when text is highlighted
    } else {
      // If user clicks away, revert to book mode if no text is selected
      if (!window.getSelection().toString().trim()) {
        setChatMode('book');
        setSelectedText('');
      }
    }
  }, []);

  useEffect(() => {
    document.addEventListener('mouseup', handleTextSelection);
    return () => document.removeEventListener('mouseup', handleTextSelection);
  }, [handleTextSelection]);

  const toggleChat = () => setIsOpen(!isOpen);

  const handleSendMessage = async (query) => {
    const userMessage = { type: 'user', text: query };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // const response = await ChatService.sendMessage(query, chatMode === 'selection' ? selectedText : null);
      const response = await ChatService.sendMessage(query, selectedText);
      setMessages((prev) => [...prev, { type: 'bot', text: response.answer, evidence: response.evidence }]);
    } catch (error) {
      setMessages((prev) => [...prev, { type: 'bot', text: `Error: ${error.message}` }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <FloatingButton onClick={toggleChat} isPanelOpen={isOpen} />
      <ChatWindow
        isOpen={isOpen}
        onClose={toggleChat}
        messages={messages}
        isLoading={isLoading}
        onSendMessage={handleSendMessage}
        chatMode={chatMode}
        onModeChange={setChatMode}
        selectedText={selectedText}
      />
    </>
  );
};

export default Chatbot;
