import React from 'react';

interface SkeletonProps {
  variant?: 'text' | 'card' | 'image' | 'table-row';
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({ variant = 'text', className = '' }) => {
  const base = 'animate-shimmer bg-gradient-to-r from-bg-secondary via-bg-card-hover to-bg-secondary bg-[length:400%_100%] rounded-md';
  const variants = {
    text: 'h-4 w-3/4',
    card: 'h-32 w-full rounded-xl',
    image: 'h-48 w-full rounded-xl',
    'table-row': 'h-8 w-full'
  };

  return <div className={`${base} ${variants[variant]} ${className}`} />;
};
