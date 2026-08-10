'use client';
import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import { LayoutDashboard, Folder, Film, Video, Newspaper, Megaphone, BookOpen, Image as ImageIcon, Mic, LayoutTemplate, HardDrive, Briefcase, Plus, Menu, X, ChevronRight } from 'lucide-react';
import { useAuthStore } from '@/stores/auth-store';
import { motion } from 'framer-motion';

const navItems = [
  { label: 'Dashboard',        icon: LayoutDashboard, href: '/' },
  { label: 'Projects',         icon: Folder,          href: '/projects' },
  { label: 'AI Movie Studio',  icon: Film,            href: '/movie' },
  { label: 'Cartoon Studio',   icon: Video,           href: '/cartoon' },
  { label: 'News Studio',      icon: Newspaper,       href: '/news' },
  { label: 'Ad Studio',        icon: Megaphone,       href: '/advertisement' },
  { label: 'Explainer Studio', icon: BookOpen,        href: '/explainer' },
  { label: 'Image to Video',   icon: ImageIcon,       href: '/image-to-video' },
  { label: 'Voice Studio',     icon: Mic,             href: '/voices' },
  { label: 'Templates',        icon: LayoutTemplate,  href: '/templates' },
  { label: 'My Media',         icon: HardDrive,       href: '/media' },
  { label: 'Brand Kit',        icon: Briefcase,       href: '/brand-kit' },
];

export const Sidebar = () => {
  const pathname = usePathname();
  const { user } = useAuthStore();
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const SidebarContent = () => (
    <div className="flex flex-col h-full bg-[#05050B] border-r border-border w-[240px] shrink-0">
      
      {/* ── User Profile Box (Top) ── */}
      <div className="p-6 pb-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded bg-bg-secondary border border-border overflow-hidden shrink-0 relative">
            <Image src="/brand-hero.png" alt="Avatar" fill className="object-cover object-top" />
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="text-white text-sm font-semibold truncate">{user?.displayName || 'Iyke'}</h3>
            <div className="flex items-center gap-1 mt-0.5">
              <span className="text-[10px]">👑</span>
              <p className="text-text-muted text-[10px] font-medium tracking-wide">Pro Plan</p>
            </div>
          </div>
          <button className="w-5 h-5 shrink-0 flex items-center justify-center text-text-muted hover:text-white transition-colors">
            <Plus size={16} strokeWidth={2.5} />
          </button>
        </div>
      </div>

      {/* ── Nav Links ── */}
      <nav className="flex-1 overflow-y-auto px-4 pb-6 flex flex-col gap-1 scrollbar-hide">
        {navItems.map((item) => {
          const isActive = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href));
          const Icon = item.icon;
          
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] font-medium transition-all duration-200 group relative ${
                isActive ? 'text-white' : 'text-text-secondary hover:text-white'
              }`}
            >
              {isActive && (
                <motion.div 
                  layoutId="activeNav"
                  className="absolute inset-0 bg-accent-purple rounded-lg -z-10"
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                />
              )}
              
              {!isActive && (
                <div className="absolute inset-0 bg-white/5 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity -z-10" />
              )}
              
              <Icon size={16} strokeWidth={isActive ? 2.5 : 1.5} className={isActive ? 'text-white' : 'text-text-muted group-hover:text-white'} />
              <span>{item.label}</span>
              {isActive && <ChevronRight size={14} className="ml-auto opacity-70" />}
            </Link>
          );
        })}
      </nav>
    </div>
  );

  return (
    <>
      <div className="md:hidden fixed top-3 left-4 z-50">
        <button onClick={() => setMobileOpen(true)} className="p-2 rounded-lg bg-bg-card border border-border text-white">
          <Menu size={20} />
        </button>
      </div>

      {mobileOpen && (
        <div className="md:hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-sm" onClick={() => setMobileOpen(false)}>
          <motion.div 
            initial={{ x: -240 }}
            animate={{ x: 0 }}
            exit={{ x: -240 }}
            className="absolute left-0 top-0 h-full" 
            onClick={e => e.stopPropagation()}
          >
            <SidebarContent />
            <button className="absolute top-4 right-[-40px] text-text-secondary hover:text-white" onClick={() => setMobileOpen(false)}>
              <X size={20} />
            </button>
          </motion.div>
        </div>
      )}

      <div className="hidden md:block h-screen sticky top-0 shrink-0">
        <SidebarContent />
      </div>
    </>
  );
};
