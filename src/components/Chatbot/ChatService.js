// const API_BASE_URL = process.env.NODE_ENV === 'production'
//   ? 'https://muhib-dev-physical-ai-book-backend.hf.space'
//   : 'http://localhost:8000';
const API_BASE_URL = 'https://muhib-dev-physical-ai-book-backend.hf.space';

const ChatService = {
  // async sendMessage(query) {
  //   const payload = {
  //     query,
  //     session_id: this.getSessionId(),
  async sendMessage(query, selectedText = null) {
    const payload = {
      query,
      session_id: this.getSessionId(),
      ...(selectedText && { context: selectedText })
    };

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error('Backend error');
      }

      return await response.json();
    } catch (error) {
      console.error('ChatService error:', error);
      return {
        answer: "Sorry, I couldn't connect to the backend. Please check the API server.",
        source_references: [],
      };
    }
  },

  getSessionId() {
    let sessionId = localStorage.getItem('chatbot_session_id');
    if (!sessionId) {
      sessionId = `session_${Date.now()}_${Math.random().toString(36).slice(2)}`;
      localStorage.setItem('chatbot_session_id', sessionId);
    }
    return sessionId;
  },
};

export default ChatService;











// // src/components/Chatbot/ChatService.js

// // const API_BASE_URL = process.env.NODE_ENV === 'production' 
// //   ? 'https://your-deployed-fastapi-backend.vercel.app' // IMPORTANT: Replace with your deployed Vercel URL
// //   : 'http://localhost:8000'; // Local development URL

// const API_BASE_URL = process.env.NODE_ENV === 'production'
//   ? 'https://muhib-dev-physical-ai-book-backend.hf.space'
//   : 'http://localhost:8000';

// const ChatService = {
//   async sendMessage(query, selectedText = null) {
//     const endpoint = selectedText ? '/api/chat/select-and-ask' : '/chat';
//     const payload = {
//       query,
//       selected_text: selectedText,
//       session_id: this.getSessionId(), // Ensure session ID is sent
//     };

//     try {
//       const response = await fetch(`${API_BASE_URL}${endpoint}`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify(payload),
//       });

//       if (!response.ok) {
//         const errorData = await response.json();
//         throw new Error(errorData.detail || 'Failed to fetch response from chatbot backend.');
//       }

//       const data = await response.json();
//       return data;
//     } catch (error) {
//       console.error('ChatService error:', error);
//       // Return a structured error to be displayed in the UI
//       return {
//         answer: "Sorry, I couldn't connect to the backend. Please check the API server.",
//         evidence: [],
//       };
//     }
//   },

//   getSessionId() {
//     let sessionId = localStorage.getItem('chatbot_session_id');
//     if (!sessionId) {
//       sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
//       localStorage.setItem('chatbot_session_id', sessionId);
//     }
//     return sessionId;
//   },
// };

// export default ChatService;
