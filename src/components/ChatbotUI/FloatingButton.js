import React from 'react';
import clsx from 'clsx';
import styles from './ChatbotUI.module.css'; // Assuming a CSS module for styles

const FloatingButton = ({ onClick, isPanelOpen }) => {
  return (
    <button
      className={clsx(styles.floatingButton, { [styles.isOpen]: isPanelOpen })}
      onClick={onClick}
      title="Open Chatbot"
    >
      {isPanelOpen ? (
        <i className="fas fa-times"></i> // Close icon
      ) : (
        <i className="fas fa-comments"></i> // Chat icon
      )}
    </button>
  );
};

export default FloatingButton;
