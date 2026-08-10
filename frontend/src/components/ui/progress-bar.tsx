import React from 'react';

interface ProgressBarProps {
  progress: number; // 0 to 100
  label?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({ progress, label }) => {
  return (
    <div className="w-full">
      {label && (
        <div className="flex justify-between text-xs mb-1 text-text-secondary">
          <span>{label}</span>
          <span>{progress}%</span>
        </div>
      )}
      <div className="h-2 w-full bg-bg-secondary rounded-full overflow-hidden">
        <div 
          className="h-full bg-gradient-to-r from-accent-primary to-accent-secondary transition-all duration-500 ease-out"
          style={{ width: `${Math.min(100, Math.max(0, progress))}%` }}
        />
      </div>
    </div>
  );
};
