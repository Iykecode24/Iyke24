import React, { useState, useRef, useEffect } from 'react';

interface DropdownProps {
  trigger: React.ReactNode;
  children: React.ReactNode;
}

export const Dropdown: React.FC<DropdownProps> = ({ trigger, children }) => {
  const [isOpen, setIsOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative inline-block text-left" ref={ref}>
      <div onClick={() => setIsOpen(!isOpen)} className="cursor-pointer">
        {trigger}
      </div>
      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 rounded-md glass shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-50 animate-fade-in p-1">
          {children}
        </div>
      )}
    </div>
  );
};

export const DropdownItem: React.FC<{onClick?: () => void, children: React.ReactNode}> = ({ onClick, children }) => (
  <div onClick={onClick} className="block px-4 py-2 text-sm text-text-primary hover:bg-white/10 rounded cursor-pointer transition-colors">
    {children}
  </div>
);

export const DropdownDivider = () => <div className="h-px bg-white/10 my-1" />;
