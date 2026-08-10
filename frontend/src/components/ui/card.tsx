import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'highlighted' | 'interactive';
}

export const Card: React.FC<CardProps> = ({ variant = 'default', children, className = '', ...props }) => {
  let vClass = 'glass rounded-xl p-6';
  if (variant === 'highlighted') vClass += ' border-accent-primary/50 shadow-[0_0_15px_rgba(124,58,237,0.2)]';
  if (variant === 'interactive') vClass += ' cursor-pointer hover:-translate-y-1';

  return (
    <div className={`${vClass} ${className}`} {...props}>
      {children}
    </div>
  );
};
