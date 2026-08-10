import React from 'react';
import { ProjectStatus } from '@/types';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  status?: ProjectStatus;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({ status, className = '', children, ...props }) => {
  const colors: Record<string, string> = {
    draft: 'bg-gray-500/20 text-gray-400 border-gray-500/50',
    planning: 'bg-blue-500/20 text-blue-400 border-blue-500/50',
    rendering: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/50 animate-pulse',
    published: 'bg-green-500/20 text-green-400 border-green-500/50',
    failed: 'bg-red-500/20 text-red-400 border-red-500/50',
  };

  const color = status ? (colors[status] || 'bg-accent-primary/20 text-accent-primary border-accent-primary/50') : '';

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border flex items-center justify-center ${color} ${className}`} {...props}>
      {children || (status ? status.replace('_', ' ').toUpperCase() : null)}
    </span>
  );
};
