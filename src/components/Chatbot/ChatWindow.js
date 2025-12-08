import React, { useState, useRef, useEffect } from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const ChatWindow = ({ isOpen, onClose, messages, isLoading, onSendMessage, chatMode, onModeChange, selectedText }) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = () => {
    if (input.trim()) {
      onSendMessage(input);
      setInput('');
    }
  };

  return (
    <div className={clsx(styles.chatWindow, { [styles.isOpen]: isOpen })}>
      <div className={styles.header}>
        <h3>Physical AI Assistant</h3>
        <button onClick={onClose} className={styles.closeButton}>&times;</button>
      </div>
      <div className={styles.chatModes}>
        <button 
          className={clsx(styles.modeButton, { [styles.active]: chatMode === 'book' })}
          onClick={() => onModeChange('book')}
        >
          Entire Book
        </button>
        <button 
          className={clsx(styles.modeButton, { [styles.active]: chatMode === 'selection' })}
          onClick={() => onModeChange('selection')}
          disabled={!selectedText}
          title={!selectedText ? "Highlight text on the page to enable this mode" : "Ask about your selected text"}
        >
          Selected Text
        </button>
      </div>
      <div className={styles.messages}>
        {messages.map((msg, index) => (
          <div key={index} className={clsx(styles.message, styles[msg.type])}>
            <p>{msg.text}</p>
            {msg.evidence && msg.evidence.length > 0 && (
              <div className={styles.evidence}>
                <strong>Sources:</strong>
                {msg.evidence.map((ev, evIndex) => (
                  <span key={evIndex} className={styles.evidenceItem} title={ev.text}>
                    {ev.source}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
        {isLoading && <div className={clsx(styles.message, styles.bot, styles.loading)}><span className={styles.loader}></span></div>}
        <div ref={messagesEndRef} />
      </div>
      <div className={styles.inputArea}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => { if (e.key === 'Enter' && !isLoading) handleSend(); }}
          placeholder={chatMode === 'selection' ? 'Ask about selected text...' : 'Ask about the book...'}
          disabled={isLoading}
        />
        <button onClick={handleSend} className={styles.sendButton} disabled={isLoading}>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
          </svg>
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;
