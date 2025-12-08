import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const FloatingButton = ({ onClick, isPanelOpen }) => {
  return (
    <button
      className={clsx(styles.floatingButton, { [styles.isOpen]: isPanelOpen })}
      onClick={onClick}
      title={isPanelOpen ? "Close Chat" : "Open Chatbot"}
      aria-label={isPanelOpen ? "Close Chat" : "Open Chatbot"}
    >
      <div className={styles.iconContainer}>
        {/* Simple chat icon */}
        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" className={clsx(styles.icon, styles.chatIcon, { [styles.hidden]: isPanelOpen })}>
          <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
        </svg>
        {/* Simple close icon (X) */}
        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" className={clsx(styles.icon, styles.closeIcon, { [styles.visible]: isPanelOpen })}>
          <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
        </svg>
      </div>
    </button>
  );
};

export default FloatingButton;
