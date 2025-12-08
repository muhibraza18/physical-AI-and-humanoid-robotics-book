import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './ChatbotUI.module.css'; // Assuming a CSS module for styles
import ChatService from './ChatService'; // Import the ChatService

const AgentPanel = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async () => {
    if (input.trim()) {
      const userMessage = { type: 'user', text: input };
      setMessages((prev) => [...prev, userMessage]);
      setInput('');
      setIsLoading(true);

      try {
        const response = await ChatService.sendMessage(userMessage.text);
        setMessages((prev) => [...prev, { type: 'bot', text: response.answer, evidence: response.evidence }]);
      } catch (error) {
        setMessages((prev) => [...prev, { type: 'bot', text: `Error: ${error.message}` }]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className={clsx(styles.agentPanel, { [styles.isOpen]: isOpen })}>
      <div className={styles.header}>
        <h3>RAG Chatbot</h3>
        <button onClick={onClose} className={styles.closeButton}>
          <i className="fas fa-times"></i>
        </button>
      </div>
      <div className={styles.messages}>
        {messages.map((msg, index) => (
          <div key={index} className={clsx(styles.message, styles[msg.type])}>
            {msg.text}
            {msg.evidence && msg.evidence.length > 0 && (
              <div className={styles.evidence}>
                <strong>Sources:</strong>
                {msg.evidence.map((ev, evIndex) => (
                  <span key={evIndex} className={styles.evidenceItem}>
                    {ev.source}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
        {isLoading && <div className={styles.loadingMessage}>Thinking...</div>}
      </div>
      <div className={styles.inputArea}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter' && !isLoading) handleSendMessage();
          }}
          placeholder="Ask me anything about the book..."
          disabled={isLoading}
        />
        <button onClick={handleSendMessage} className={clsx(styles.sendButton, { [styles.loading]: isLoading })} disabled={isLoading}>
          {isLoading ? (
            <i className="fas fa-spinner fa-spin"></i>
          ) : (
            <i className="fas fa-paper-plane"></i>
          )}
        </button>
      </div>
    </div>
  );
};

export default AgentPanel;