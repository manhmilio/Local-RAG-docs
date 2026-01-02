/**
 * App Component - Main application
 */
import React, { useState, useEffect, useRef } from 'react';
import Header from './components/Header';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import TypingIndicator from './components/TypingIndicator';
import UploadModal from './components/UploadModal';
import { streamMessage } from './services/api';
import { MessageSquare } from 'lucide-react';

function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingMessage]);

  // Load messages from localStorage
  useEffect(() => {
    const savedMessages = localStorage.getItem('chatMessages');
    if (savedMessages) {
      try {
        setMessages(JSON.parse(savedMessages));
      } catch (e) {
        console.error('Error loading messages:', e);
      }
    }
  }, []);

  // Save messages to localStorage
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('chatMessages', JSON.stringify(messages));
    }
  }, [messages]);

  const handleSendMessage = async (messageText) => {
    // Add user message
    const userMessage = {
      role: 'user',
      content: messageText,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setStreamingMessage('');
    setIsStreaming(true);

    try {
      let fullResponse = '';

      await streamMessage(
        messageText,
        messages,
        true,
        (chunk) => {
          fullResponse += chunk;
          setStreamingMessage(fullResponse);
        }
      );

      // Add assistant message
      const assistantMessage = {
        role: 'assistant',
        content: fullResponse,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setStreamingMessage('');

    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage = {
        role: 'assistant',
        content: '❌ Xin lỗi, đã có lỗi xảy ra khi xử lý câu hỏi của bạn. Vui lòng thử lại.',
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, errorMessage]);
      setStreamingMessage('');
    } finally {
      setIsLoading(false);
      setIsStreaming(false);
    }
  };

  const handleClearChat = () => {
    if (window.confirm('Bạn có chắc muốn xóa toàn bộ lịch sử chat?')) {
      setMessages([]);
      setStreamingMessage('');
      localStorage.removeItem('chatMessages');
    }
  };

  const handleUploadSuccess = () => {
    // Reload stats or show notification
    console.log('Upload successful');
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <Header onUploadClick={() => setShowUploadModal(true)} />

      {/* Chat Area */}
      <div className="flex-1 overflow-hidden flex flex-col">
        <div className="flex-1 overflow-y-auto custom-scrollbar">
          <div className="max-w-4xl mx-auto px-4 py-6">
            {messages.length === 0 && !streamingMessage && (
              <div className="flex flex-col items-center justify-center h-full text-center py-12">
                <div className="w-20 h-20 rounded-full bg-primary-100 flex items-center justify-center mb-6">
                  <MessageSquare className="w-10 h-10 text-primary-600" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  Chào mừng đến với Medical Chatbot
                </h2>
                <p className="text-gray-600 max-w-md mb-8">
                  Tôi là trợ lý y tế AI. Hãy hỏi tôi về các triệu chứng, bệnh tật, 
                  hoặc bất kỳ thông tin y tế nào bạn cần tìm hiểu.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl w-full">
                  {[
                    'Triệu chứng của bệnh cảm cúm là gì?',
                    'Làm thế nào để phòng ngừa bệnh tiểu đường?',
                    'Tôi bị đau đầu và chóng mặt, có thể là bệnh gì?',
                    'Chế độ ăn nào tốt cho người cao huyết áp?',
                  ].map((suggestion, index) => (
                    <button
                      key={index}
                      onClick={() => handleSendMessage(suggestion)}
                      className="text-left p-4 bg-white border border-gray-200 rounded-lg hover:border-primary-400 hover:bg-primary-50 transition-all"
                    >
                      <p className="text-sm text-gray-700">{suggestion}</p>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Messages */}
            {messages.map((message, index) => (
              <ChatMessage
                key={index}
                message={message.content}
                isUser={message.role === 'user'}
              />
            ))}

            {/* Streaming Message */}
            {streamingMessage && (
              <ChatMessage
                message={streamingMessage}
                isUser={false}
                isStreaming={true}
              />
            )}

            {/* Typing Indicator */}
            {isLoading && !streamingMessage && <TypingIndicator />}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Clear Chat Button */}
        {messages.length > 0 && (
          <div className="px-4 py-2 bg-gray-50 border-t border-gray-200">
            <div className="max-w-4xl mx-auto">
              <button
                onClick={handleClearChat}
                className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
              >
                🗑️ Xóa lịch sử chat
              </button>
            </div>
          </div>
        )}

        {/* Input */}
        <ChatInput
          onSend={handleSendMessage}
          disabled={isLoading}
          placeholder={
            isLoading
              ? 'Đang xử lý câu hỏi...'
              : 'Nhập câu hỏi của bạn... (Enter để gửi, Shift+Enter để xuống dòng)'
          }
        />
      </div>

      {/* Upload Modal */}
      <UploadModal
        isOpen={showUploadModal}
        onClose={() => setShowUploadModal(false)}
        onUploadSuccess={handleUploadSuccess}
      />
    </div>
  );
}

export default App;
