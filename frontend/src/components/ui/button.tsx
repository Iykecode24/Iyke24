import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ variant = 'primary', size = 'md', isLoading, children, className = '', ...props }) => {
  const base = 'inline-flex items-center justify-center rounded-md font-medium transition-all duration-200 focus:outline-none';
  const variants = {
    primary: 'bg-gradient-to-r from-accent-primary to-accent-secondary hover:shadow-pulse-glow text-white border-0',
    secondary: 'glass text-text-primary hover:text-white',
    danger: 'bg-accent-red/20 text-accent-red border border-accent-red/50 hover:bg-accent-red hover:text-white',
    ghost: 'bg-transparent text-text-secondary hover:text-text-primary hover:bg-white/5'
  };
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  return (
    <button className={`${base} ${variants[variant]} ${sizes[size]} ${isLoading ? 'opacity-70 cursor-not-allowed' : ''} ${className}`} disabled={isLoading || props.disabled} {...props}>
      {isLoading ? <span className="mr-2 animate-spin rounded-full h-4 w-4 border-2 border-white/20 border-t-white"></span> : null}
      {children}
    </button>
  );
};
