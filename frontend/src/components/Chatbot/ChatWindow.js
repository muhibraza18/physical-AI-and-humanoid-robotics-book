import React, { useState, useEffect, useRef } from 'react';
import styles from './styles.module.css';
import ChatService from '../../services/ChatService'; // Adjust path

const ChatWindow = ({ onClose }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSendMessage = async () => {
    if (input.trim()) {
      const userMessage = { id: Date.now(), text: input, sender: 'user' };
      setMessages((prevMessages) => [...prevMessages, userMessage]);
      setInput('');

      // Attempt to get globally available selected text from Docusaurus content
      // const docusaurusSelectedText = window.docusaurusSelectedText || null;
      // if (docusaurusSelectedText) {
      //   // Optionally, display selected text as part of the user's message or a separate indicator
      //   console.log("Using selected text from Docusaurus (frontend-only for now):", docusaurusSelectedText);
      // }

      try {
        // Only sending query and a new session ID (if needed)
        const response = await ChatService.sendMessage(input); // Removed docusaurusSelectedText
        const botMessage = { id: Date.now() + 1, text: response.answer, sender: 'bot', references: response.source_references };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
        // Clear selected text after use (if it was used for local display)
        // window.docusaurusSelectedText = null;
      } catch (error) {
        console.error('Chatbot error:', error);
        const errorMessage = { id: Date.now() + 1, text: "Sorry, I'm having trouble connecting.", sender: 'bot' };
        setMessages((prevMessages) => [...prevMessages, errorMessage]);
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <div id="chatbot-chat-window" className={styles.chatWindow}>
      <div className={styles.chatHeader}>
        <h3>RAG Chatbot</h3>
        <button onClick={onClose} className={styles.closeButton}>✕</button>
      </div>
      <div className={styles.messagesContainer}>
        {messages.map((msg) => (
          <div key={msg.id} className={`${styles.message} ${styles[msg.sender]}`}>
            <p>{msg.text}</p>
            {msg.references && msg.references.length > 0 && (
              <div className={styles.references}>
                <strong>Sources:</strong>
                {msg.references.map((ref, idx) => (
                  <span key={idx} className={styles.referenceItem}>
                    {ref.chapter} - {ref.section} ({ref.file_path})
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className={styles.chatInputContainer}>
        <input
          id="chatbot-input-field"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question about the book..."
          className={styles.chatInput}
        />
        <button onClick={handleSendMessage} className={styles.sendButton}>Send</button>
      </div>
    </div>
  );
};

export default ChatWindow;