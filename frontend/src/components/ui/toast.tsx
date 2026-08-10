import React, { useEffect } from 'react';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';

interface ToastProps {
  message: string;
  type: 'success' | 'error' | 'warning' | 'info';
  onClose: () => void;
}

export const Toast: React.FC<ToastProps> = ({ message, type, onClose }) => {
  const icons = {
    success: <CheckCircle className="text-accent-green" size={20} />,
    error: <AlertCircle className="text-accent-red" size={20} />,
    warning: <AlertTriangle className="text-accent-gold" size={20} />,
    info: <Info className="text-accent-secondary" size={20} />
  };

  return (
    <div className="glass flex items-center gap-3 p-4 rounded-lg shadow-lg border-l-4 border-l-accent-primary animate-slide-in pointer-events-auto">
      {icons[type]}
      <p className="text-sm font-medium text-text-primary flex-1">{message}</p>
      <button onClick={onClose} className="text-text-secondary hover:text-white">
        <X size={16} />
      </button>
    </div>
  );
};
