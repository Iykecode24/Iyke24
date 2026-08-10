import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement> {
  label?: string;
  error?: string;
  helperText?: string;
  as?: 'input' | 'textarea' | 'select';
  options?: {label: string, value: string}[];
}

export const Input: React.FC<InputProps> = ({ label, error, helperText, as = 'input', options, className = '', ...props }) => {
  const baseClass = 'w-full bg-bg-secondary border border-white/10 rounded-md px-4 py-2 text-text-primary focus:outline-none focus:ring-2 focus:ring-accent-primary transition-all';
  
  return (
    <div className="flex flex-col gap-1 w-full">
      {label && <label className="text-sm font-medium text-text-secondary">{label}</label>}
      {as === 'input' && <input className={`${baseClass} ${className}`} {...(props as any)} />}
      {as === 'textarea' && <textarea className={`${baseClass} min-h-[100px] ${className}`} {...(props as any)} />}
      {as === 'select' && (
        <select className={`${baseClass} ${className}`} {...(props as any)}>
          {options?.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
        </select>
      )}
      {error && <span className="text-xs text-accent-red">{error}</span>}
      {helperText && !error && <span className="text-xs text-text-muted">{helperText}</span>}
    </div>
  );
};
