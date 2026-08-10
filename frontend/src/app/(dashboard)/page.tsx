'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Clock, MoreHorizontal, Sparkles, ChevronRight, Folder, Film, Database, Coins, ArrowUp, ArrowDown } from 'lucide-react';
import { useAuthStore } from '@/stores/auth-store';
import { motion } from 'framer-motion';

interface DashboardStats {
  total_projects: number;
  videos_rendered: number;
  storage_used_gb: number;
  storage_total_gb: number;
  credits_remaining: number;
}

function StatCard({ 
  icon: Icon, label, value, sub, delta, deltaPositive, delay 
}: { 
  icon: React.ElementType, label: string; value: string; sub?: string; delta?: string; deltaPositive?: boolean; delay: number 
}) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay, ease: "easeOut" }}
      className="glass-card rounded-2xl p-5 flex flex-col gap-3 group hover:border-white/10 hover:shadow-card transition-all"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-text-secondary text-xs font-medium">
          <Icon size={14} className="text-text-muted group-hover:text-white transition-colors" />
          {label}
        </div>
        {label === 'Storage Used' && <MoreHorizontal size={14} className="text-text-muted cursor-pointer hover:text-white transition-colors" />}
      </div>
      
      <div className="flex items-baseline gap-2">
        <h3 className="text-white text-3xl font-bold tracking-tight">{value}</h3>
        {sub && <span className="text-text-muted text-[11px] font-medium">{sub}</span>}
      </div>
      
      {delta && (
        <div className={`flex items-center gap-1 text-[10px] font-semibold mt-1 ${deltaPositive ? 'text-accent-green' : 'text-accent-red'}`}>
          {deltaPositive ? <ArrowUp size={12} strokeWidth={3} /> : <ArrowDown size={12} strokeWidth={3} />}
          {delta}
        </div>
      )}
    </motion.div>
  );
}

const demoProjects = [
  { id: 1, title: 'The Return of Legacy', date: 'May 20, 2025', duration: '02:45', thumb: '/thumb-legacy.jpg' },
  { id: 2, title: 'City of Dreams', date: 'May 18, 2025', duration: '01:32', thumb: '/thumb-city.jpg' },
  { id: 3, title: 'Tech Future Explainer', date: 'May 16, 2025', duration: '00:58', thumb: '/thumb-tech.jpg' },
  { id: 4, title: 'Product Ad – LuxeWatch', date: 'May 15, 2025', duration: '00:30', thumb: '/thumb-watch.jpg' },
];

export default function DashboardPage() {
  const { user } = useAuthStore();
  const [stats, setStats] = useState<DashboardStats | null>(null);

  useEffect(() => {
    fetch('/api/dashboard/stats', { credentials: 'include' })
      .then(r => r.ok ? r.json() : null)
      .then(data => { if (data) setStats(data); });
  }, []);

  const statCards = [
    { icon: Folder, label: 'Total Projects', value: stats ? String(stats.total_projects) : '24', delta: '12% from last month', deltaPositive: true },
    { icon: Film, label: 'Videos Rendered', value: stats ? String(stats.videos_rendered) : '128', delta: '23% from last month', deltaPositive: true },
    { icon: Database, label: 'Storage Used', value: stats ? `${stats.storage_used_gb.toFixed(1)} GB` : '42.6 GB', sub: 'of 200 GB' },
    { icon: Coins, label: 'Credits Left', value: stats ? stats.credits_remaining.toLocaleString() : '1,250', delta: '8% from last month', deltaPositive: true },
  ];

  return (
    <div className="relative min-h-full px-8 py-8 pb-32 max-w-[1200px]">
      
      {/* ── Man image on the right (overlapping into Dashboard) ── */}
      <motion.div 
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 1, ease: "easeOut" }}
        className="fixed right-0 bottom-0 w-[45%] lg:w-[40%] xl:w-[35%] h-[85vh] pointer-events-none z-10 hidden md:block"
      >
        <Image
          src="/brand-hero.png"
          alt="Director"
          fill
          priority
          className="object-cover object-top drop-shadow-2xl"
          style={{
            WebkitMaskImage: 'linear-gradient(to right, transparent 0%, black 20%, black 100%), linear-gradient(to top, transparent 0%, black 5%)',
            maskImage: 'linear-gradient(to right, transparent 0%, black 20%, black 100%), linear-gradient(to top, transparent 0%, black 5%)'
          }}
        />
      </motion.div>

      <div className="relative z-20">
        
        {/* ── Welcome Area ── */}
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8"
        >
          <h1 className="text-white text-2xl font-bold tracking-tight mb-1 flex items-center gap-2">
            Welcome back, {user?.displayName || 'Iyke'} <span className="text-xl origin-bottom-right hover:animate-[spin-slow_1s_ease-in-out]">👋</span>
          </h1>
          <p className="text-text-secondary text-sm">What will you create today?</p>
        </motion.div>

        {/* ── Statistics Cards ── */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-10 xl:pr-[10%]">
          {statCards.map((s, i) => <StatCard key={s.label} {...s} delay={0.1 + (i * 0.1)} />)}
        </div>

        {/* ── Recent Projects ── */}
        <div className="mb-10 xl:pr-[5%]">
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="flex items-center justify-between mb-4"
          >
            <h2 className="text-white text-base font-semibold">Recent Projects</h2>
            <Link href="/projects" className="flex items-center gap-1 text-xs font-medium text-text-secondary hover:text-white transition-colors group">
              View all <ChevronRight size={14} className="group-hover:translate-x-0.5 transition-transform" />
            </Link>
          </motion.div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {demoProjects.map((p, i) => (
              <motion.div 
                key={p.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.5 + (i * 0.1) }}
              >
                <Link href={`/projects/${p.id}`} className="block group">
                  <div className="glass-card rounded-xl overflow-hidden hover:border-accent-purple/30 hover:shadow-glow-purple transition-all duration-300 hover:-translate-y-1">
                    {/* Thumbnail */}
                    <div className="relative w-full h-32 overflow-hidden bg-bg-primary">
                      <Image 
                        src={p.thumb} 
                        alt={p.title} 
                        fill 
                        className="object-cover group-hover:scale-105 transition-transform duration-500" 
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-bg-card/90 to-transparent" />
                      <button className="absolute top-2 right-2 p-1.5 rounded-lg bg-black/40 text-white opacity-0 group-hover:opacity-100 transition-opacity hover:bg-black/60">
                        <MoreHorizontal size={14} />
                      </button>
                    </div>
                    
                    {/* Info */}
                    <div className="p-3.5">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="text-white text-sm font-semibold truncate pr-2">{p.title}</h3>
                        <MoreHorizontal size={16} className="text-text-muted shrink-0 lg:hidden group-hover:block" />
                      </div>
                      <div className="flex justify-between items-center text-text-muted text-[11px] font-medium">
                        <span>{p.date}</span>
                        <div className="flex items-center gap-1.5 bg-white/5 px-2 py-1 rounded">
                          <Clock size={12} /> {p.duration}
                        </div>
                      </div>
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>

        {/* ── Upgrade Banner ── */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.9 }}
          className="xl:pr-[15%]"
        >
          <div className="rounded-2xl p-5 sm:p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border border-accent-purple/30 bg-gradient-to-r from-accent-purple/20 to-accent-blue/10 backdrop-blur-md shadow-glow-purple">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-xl bg-accent-purple/20 border border-accent-purple/30 flex items-center justify-center shrink-0">
                <Sparkles size={20} className="text-[#c4b5fd]" />
              </div>
              <div>
                <h3 className="text-white text-sm sm:text-base font-bold mb-0.5">Upgrade to Pro for more power</h3>
                <p className="text-[#c4b5fd] text-xs sm:text-sm font-medium">Get more credits, faster renders, and premium features.</p>
              </div>
            </div>
            <Link href="/billing" className="bg-accent-purple hover:bg-accent-blue text-white text-sm font-semibold px-5 py-2.5 rounded-lg transition-all shadow-btn-glow shrink-0 w-full sm:w-auto text-center">
              Upgrade Now
            </Link>
          </div>
        </motion.div>

      </div>
    </div>
  );
}
