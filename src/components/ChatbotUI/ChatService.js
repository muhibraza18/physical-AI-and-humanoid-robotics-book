// Client-side chat service to interact with the FastAPI backend
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-deployed-fastapi-backend.vercel.app' // Replace with your deployed Vercel URL
  : 'http://localhost:8000'; // Local development URL

const ChatService = {
  async sendMessage(query, selectedText = null) {
    const endpoint = selectedText ? '/select-and-ask' : '/chat';
    const payload = selectedText ? { query, selected_text: selectedText } : { query };

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch response from chatbot backend.');
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('ChatService error:', error);
      throw error; // Re-throw to be handled by AgentPanel
    }
  },
};

export default ChatService;