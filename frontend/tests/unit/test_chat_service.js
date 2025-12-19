// frontend/tests/unit/test_chat_service.js
import ChatService from '../../src/services/ChatService'; // Adjust path as needed

// Mock the global fetch function
global.fetch = jest.fn();

describe('ChatService', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('sendMessage should post to /chat and return response', async () => {
    const mockResponse = { answer: 'Hello from RAG', source_references: [] };
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    });

    const message = 'Hi there';
    const response = await ChatService.sendMessage(message);

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/chat', // Assuming backend runs on 8000
      expect.objectContaining({
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: message, selected_text: null }),
      })
    );
    expect(response).toEqual(mockResponse);
  });

  test('sendMessage should handle selected text', async () => {
    const mockResponse = { answer: 'Response from selected text', source_references: [] };
    fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    });

    const message = 'Explain this';
    const selectedText = 'This is the selected content.';
    const response = await ChatService.sendMessage(message, selectedText);

    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8000/chat',
      expect.objectContaining({
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: message, selected_text: selectedText }),
      })
    );
    expect(response).toEqual(mockResponse);
  });

  test('sendMessage should throw error on network failure', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));

    await expect(ChatService.sendMessage('test')).rejects.toThrow('Network error');
  });

  test('sendMessage should throw error on non-ok response', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: () => Promise.resolve({ detail: 'Server error' }),
    });

    await expect(ChatService.sendMessage('test')).rejects.toThrow('Server error');
  });
});
