/**
 * API Service - Xử lý tất cả HTTP requests đến backend
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Health check API
 */
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

/**
 * Gửi tin nhắn chat (non-streaming)
 */
export const sendMessage = async (message, conversationHistory = [], useRag = true) => {
  const response = await api.post('/chat', {
    message,
    conversation_history: conversationHistory,
    use_rag: useRag,
  });
  return response.data;
};

/**
 * Gửi tin nhắn với streaming response
 */
export const streamMessage = async (message, conversationHistory = [], useRag = true, onChunk) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        conversation_history: conversationHistory,
        use_rag: useRag,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.chunk) {
              onChunk(data.chunk);
            } else if (data.error) {
              throw new Error(data.error);
            }
          } catch (e) {
            console.error('Error parsing SSE data:', e);
          }
        }
      }
    }
  } catch (error) {
    console.error('Streaming error:', error);
    throw error;
  }
};

/**
 * Upload PDF document
 */
export const uploadDocument = async (file, onProgress) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent) => {
      const percentCompleted = Math.round(
        (progressEvent.loaded * 100) / progressEvent.total
      );
      if (onProgress) onProgress(percentCompleted);
    },
  });

  return response.data;
};

/**
 * Lấy thống kê documents
 */
export const getDocumentStats = async () => {
  const response = await api.get('/documents/stats');
  return response.data;
};

/**
 * Reindex tất cả documents
 */
export const reindexDocuments = async () => {
  const response = await api.post('/documents/reindex');
  return response.data;
};

export default api;
