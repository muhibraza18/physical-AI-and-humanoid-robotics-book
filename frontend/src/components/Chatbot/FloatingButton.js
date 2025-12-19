import React, { useState } from 'react';
import styles from './styles.module.css';

const FloatingButton = ({ onClick }) => {
  return (
    <button id="chatbot-floating-button" className={styles.floatingButton} onClick={onClick}>
      💬
    </button>
  );
};

export default FloatingButton;