'use client';
import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Bell, Search, Plus, ChevronDown } from 'lucide-react';
import { useAuthStore } from '@/stores/auth-store';

export const Header = () => {
  const { user, logout } = useAuthStore();

  return (
    <header className="h-16 bg-bg-secondary border-b border-border flex items-center justify-between px-6 shrink-0 sticky top-0 z-40">
      
      {/* ── Top Left Logo ── */}
      <Link href="/" className="flex items-center gap-3 group">
        <div className="relative w-8 h-8 rounded-lg overflow-hidden border border-white/20 group-hover:border-accent-purple transition-colors shadow-lg">
          <Image src="/brand-hero.png" alt="Logo" fill className="object-cover object-top" />
        </div>
        <span className="text-[10px] font-bold text-text-secondary leading-[1.1] tracking-widest mt-1">
          CONTENT<br />STUDIO
        </span>
      </Link>

      <div className="flex items-center gap-5 flex-1 justify-end">
        {/* ── Search ── */}
        <div className="relative w-72 hidden md:block group">
          <Search size={14} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-text-muted group-focus-within:text-accent-purple transition-colors" />
          <input
            type="text"
            placeholder="Search projects"
            className="w-full bg-white/5 border border-border rounded-lg pl-9 pr-4 py-2 text-sm text-white placeholder:text-text-muted outline-none focus:border-accent-purple/50 focus:bg-white/10 transition-all"
          />
        </div>

        {/* ── Notification Bell ── */}
        <button className="relative w-9 h-9 rounded-lg flex items-center justify-center bg-white/5 border border-border hover:bg-white/10 transition-colors">
          <Bell size={16} className="text-text-secondary" />
          <span className="absolute top-2 right-2 w-1.5 h-1.5 bg-accent-pink rounded-full shadow-[0_0_8px_rgba(236,72,153,0.8)]" />
        </button>

        {/* ── New Project Button ── */}
        <Link href="/movie" className="hidden sm:flex items-center gap-2 bg-accent-purple hover:bg-accent-blue text-white text-sm font-semibold px-4 py-2 rounded-lg transition-all shadow-btn-glow hover:shadow-glow-blue">
          <Plus size={16} strokeWidth={2.5} /> New Project
        </Link>

        {/* ── Avatar Dropdown ── */}
        <div className="flex items-center gap-2 cursor-pointer group" onClick={logout}>
          <div className="w-8 h-8 rounded bg-bg-card border border-border overflow-hidden relative group-hover:border-accent-purple transition-colors">
            <Image src="/brand-hero.png" alt={user?.displayName || 'User'} fill className="object-cover object-top" />
          </div>
          <ChevronDown size={12} className="text-text-muted group-hover:text-white transition-colors" />
        </div>
      </div>
    </header>
  );
};
