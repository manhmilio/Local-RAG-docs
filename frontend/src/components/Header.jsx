/**
 * Header Component - Header của ứng dụng
 */
import React, { useState, useEffect } from 'react';
import { Activity, Upload, Database, AlertCircle, CheckCircle } from 'lucide-react';
import { healthCheck, getDocumentStats } from '../services/api';

const Header = ({ onUploadClick }) => {
  const [health, setHealth] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const data = await healthCheck();
        setHealth(data);
      } catch (error) {
        console.error('Health check failed:', error);
        setHealth({ status: 'error' });
      }
    };

    const loadStats = async () => {
      try {
        const data = await getDocumentStats();
        setStats(data);
      } catch (error) {
        console.error('Failed to load stats:', error);
      }
    };

    checkHealth();
    loadStats();

    const interval = setInterval(() => {
      checkHealth();
      loadStats();
    }, 30000); // Check every 30s

    return () => clearInterval(interval);
  }, []);

  const isHealthy = health?.status === 'healthy' && health?.ollama_connected;

  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo & Title */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center">
              <Activity className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Medical Chatbot</h1>
              <p className="text-sm text-gray-500">Trợ lý Y tế AI</p>
            </div>
          </div>

          {/* Status & Actions */}
          <div className="flex items-center gap-4">
            {/* Document Stats */}
            {stats && (
              <div className="hidden sm:flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-lg">
                <Database className="w-4 h-4 text-gray-600" />
                <span className="text-sm text-gray-700">
                  {stats.total_documents} tài liệu
                </span>
              </div>
            )}

            {/* Health Status */}
            <div
              className={`flex items-center gap-2 px-3 py-2 rounded-lg ${
                isHealthy
                  ? 'bg-green-50 text-green-700'
                  : 'bg-red-50 text-red-700'
              }`}
            >
              {isHealthy ? (
                <>
                  <CheckCircle className="w-4 h-4" />
                  <span className="text-sm font-medium hidden sm:inline">Đang hoạt động</span>
                </>
              ) : (
                <>
                  <AlertCircle className="w-4 h-4" />
                  <span className="text-sm font-medium hidden sm:inline">Lỗi kết nối</span>
                </>
              )}
            </div>

            {/* Upload Button */}
            <button
              onClick={onUploadClick}
              className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              <Upload className="w-4 h-4" />
              <span className="hidden sm:inline">Upload PDF</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
