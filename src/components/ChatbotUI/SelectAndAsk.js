// Placeholder for select-and-ask functionality
import React, { useEffect, useState, useCallback } from 'react';

const SelectAndAsk = ({ onSelectAndAsk }) => {
  const [selectedText, setSelectedText] = useState('');
  const [showButton, setShowButton] = useState(false);
  const [buttonPosition, setButtonPosition] = useState({ x: 0, y: 0 });

  const handleTextSelection = useCallback(() => {
    const text = window.getSelection().toString().trim();
    if (text.length > 0) {
      setSelectedText(text);
      
      const selection = window.getSelection();
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        setButtonPosition({
          x: rect.right + window.scrollX - 50, // Adjust position as needed
          y: rect.top + window.scrollY - 50,
        });
        setShowButton(true);
      }
    } else {
      setShowButton(false);
      setSelectedText('');
    }
  }, []);

  useEffect(() => {
    document.addEventListener('mouseup', handleTextSelection);
    return () => {
      document.removeEventListener('mouseup', handleTextSelection);
    };
  }, [handleTextSelection]);

  const handleClick = () => {
    if (selectedText && onSelectAndAsk) {
      onSelectAndAsk(selectedText);
      setShowButton(false);
      setSelectedText('');
    }
  };

  if (!showButton) return null;

  return (
    <button
      style={{ position: 'absolute', left: buttonPosition.x, top: buttonPosition.y, zIndex: 1000 }}
      onClick={handleClick}
      className="button button--primary" // Use Docusaurus button styles
    >
      Ask about selection
    </button>
  );
};

export default SelectAndAsk;
