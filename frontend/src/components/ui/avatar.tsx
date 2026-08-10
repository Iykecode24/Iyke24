import React from 'react';

interface AvatarProps {
  url?: string;
  name: string;
  size?: 'sm' | 'md' | 'lg';
  status?: 'online' | 'offline';
}

export const Avatar: React.FC<AvatarProps> = ({ url, name, size = 'md', status }) => {
  const sizes = {
    sm: 'w-8 h-8 text-xs',
    md: 'w-10 h-10 text-sm',
    lg: 'w-12 h-12 text-base'
  };

  const initials = name.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2);

  return (
    <div className={`relative inline-flex items-center justify-center rounded-full bg-accent-primary text-white font-medium ${sizes[size]}`}>
      {url ? <img src={url} alt={name} className="w-full h-full rounded-full object-cover" /> : initials}
      {status && (
        <span className={`absolute bottom-0 right-0 block w-2.5 h-2.5 rounded-full ring-2 ring-bg-primary ${status === 'online' ? 'bg-accent-green' : 'bg-gray-500'}`} />
      )}
    </div>
  );
};
