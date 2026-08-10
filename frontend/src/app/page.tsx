'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { motion } from 'framer-motion';
import { Play, ChevronDown, Sun, Edit3, MonitorPlay, Mic, Video as VideoIcon, Film, Image as ImageIcon, LayoutTemplate, Megaphone, Newspaper, Camera } from 'lucide-react';

const navLinks = ['Features', 'Studio Tools', 'Templates', 'Pricing'];

const featureCards = [
  { icon: Edit3, title: 'AI Script Writer', sub: 'Generate story & scripts' },
  { icon: MonitorPlay, title: 'Scene Visualizer', sub: 'Visualize scenes' },
  { icon: Mic, title: 'AI Voiceover', sub: 'Realistic AI voices' },
  { icon: VideoIcon, title: '4K Export', sub: 'High quality output' },
];

const studioModules = [
  { icon: Film, label: 'AI Movie Studio', href: '/movie' },
  { icon: VideoIcon, label: 'Cartoon Studio', href: '/cartoon' },
  { icon: Newspaper, label: 'News Studio', href: '/news' },
  { icon: Megaphone, label: 'Ad Studio', href: '/advertisement' },
  { icon: LayoutTemplate, label: 'Explainer Studio', href: '/explainer' },
  { icon: ImageIcon, label: 'Image to Video', href: '/image-to-video' },
  { icon: Mic, label: 'Voice Studio', href: '/voices' },
  { icon: Camera, label: 'AI Model Studio', href: '/model-studio' },
];

export default function LandingPage() {
  const [scrolled, setScrolled] = useState(false);
  const [particles, setParticles] = useState<{ id: number; left: string; delay: number; duration: number }[]>([]);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    
    // Generate static particles on mount to avoid hydration mismatch
    setParticles(Array.from({ length: 20 }).map((_, i) => ({
      id: i,
      left: `${Math.random() * 100}%`,
      delay: Math.random() * 5,
      duration: 10 + Math.random() * 10
    })));

    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="min-h-screen bg-bg-primary overflow-hidden relative selection:bg-accent-purple/30 selection:text-white">
      
      {/* ── Fixed Top Navigation ── */}
      <motion.nav 
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className={`fixed top-0 inset-x-0 z-50 h-16 flex items-center justify-between px-8 lg:px-12 transition-all duration-300 ${
          scrolled ? 'bg-bg-primary/80 backdrop-blur-xl border-b border-white/5' : 'bg-transparent'
        }`}
      >
        <Link href="/" className="flex items-center gap-3 group">
          <div className="relative w-10 h-10 rounded-lg overflow-hidden border border-white/20 group-hover:border-accent-purple transition-colors shadow-lg">
            <Image src="/brand-hero.png" alt="Logo" fill className="object-cover object-top" />
          </div>
          <span className="text-[10px] font-bold text-text-secondary leading-[1.1] tracking-widest mt-1">
            CONTENT<br />STUDIO
          </span>
        </Link>

        <div className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <Link key={link} href={`#${link.toLowerCase().replace(' ', '-')}`} className="text-sm font-medium text-text-secondary hover:text-white transition-colors">
              {link}
            </Link>
          ))}
          <button className="flex items-center gap-1 text-sm font-medium text-text-secondary hover:text-white transition-colors">
            Resources <ChevronDown size={14} className="mt-0.5" />
          </button>
        </div>

        <div className="flex items-center gap-6">
          <button className="text-text-secondary hover:text-white transition-colors">
            <Sun size={18} />
          </button>
          <Link href="/login" className="text-sm font-medium text-text-secondary hover:text-white transition-colors hidden sm:block">
            Log in
          </Link>
          <Link href="/login" className="bg-accent-purple hover:bg-accent-blue text-white text-sm font-semibold px-5 py-2.5 rounded-lg transition-all shadow-btn-glow hover:shadow-glow-blue hover:-translate-y-0.5">
            Get Started Free
          </Link>
        </div>
      </motion.nav>

      {/* ── Hero Section ── */}
      <section className="relative min-h-screen flex items-center pt-16">
        
        {/* Background Effects */}
        <div className="absolute inset-0 z-0">
          {/* Radial purple lighting behind the man */}
          <div className="absolute top-[10%] right-[-5%] w-[60%] h-[80%] rounded-full bg-accent-purple/20 blur-[120px] pointer-events-none" />
          
          {/* Cinematic rings */}
          <div className="absolute top-[20%] right-[10%] w-[800px] h-[800px] rounded-full border-[1px] border-accent-purple/10 pointer-events-none" />
          <div className="absolute top-[25%] right-[15%] w-[600px] h-[600px] rounded-full border-[1px] border-accent-purple/15 pointer-events-none" />
          <div className="absolute top-[30%] right-[20%] w-[400px] h-[400px] rounded-full border-[1px] border-accent-purple/20 pointer-events-none" />
          
          {/* Ambient Particles */}
          {particles.map(p => (
            <div 
              key={p.id} 
              className="particle"
              style={{ left: p.left, animationDelay: `${p.delay}s`, animationDuration: `${p.duration}s` }} 
            />
          ))}
        </div>

        {/* Content Container */}
        <div className="container mx-auto px-8 lg:px-12 relative z-10 flex w-full">
          
          {/* LEFT: Text Content */}
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
            className="w-full lg:w-1/2 flex flex-col justify-center pb-20"
          >
            <h1 className="text-[3.5rem] lg:text-[4.5rem] font-black text-white leading-[1.05] tracking-tight mb-6">
              Your Ideas.<br />
              Our AI-Powered Studio.<br />
              <span className="text-gradient-purple">One Epic Story.</span>
            </h1>
            
            <p className="text-text-secondary text-base lg:text-lg max-w-md leading-relaxed mb-10">
              Create movies, videos, cartoons, news, ads, and more with AI tools built for creators. From script to screen — all in one place.
            </p>
            
            <div className="flex items-center gap-4">
              <Link href="/login" className="group flex items-center gap-2 bg-accent-purple text-white font-semibold px-6 py-3.5 rounded-xl shadow-btn-glow hover:shadow-glow-purple transition-all hover:-translate-y-0.5">
                Start Creating for Free 
                <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
              </Link>
              
              <button className="flex items-center gap-2 text-white font-semibold px-6 py-3.5 rounded-xl border border-white/20 hover:bg-white/5 transition-colors">
                See How It Works 
                <div className="w-5 h-5 rounded-full border border-white flex items-center justify-center">
                  <Play size={10} fill="white" />
                </div>
              </button>
            </div>
          </motion.div>
        </div>

        {/* CENTER-RIGHT: Hero Image */}
        <div className="absolute bottom-0 right-[15%] w-[45%] h-[90%] z-20 pointer-events-none hidden lg:block">
          <motion.div 
            initial={{ opacity: 0, scale: 0.95, x: 20 }}
            animate={{ opacity: 1, scale: 1, x: 0 }}
            transition={{ duration: 1, delay: 0.3, ease: [0.16, 1, 0.3, 1] }}
            className="relative w-full h-full"
          >
            <Image
              src="/brand-hero.png"
              alt="Iyke Content Studio Director"
              fill
              className="object-contain object-bottom drop-shadow-2xl"
              priority
              style={{
                WebkitMaskImage: 'linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%), linear-gradient(to top, transparent 0%, black 5%)',
                maskImage: 'linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%), linear-gradient(to top, transparent 0%, black 5%)',
              }}
            />
          </motion.div>
        </div>

        {/* FAR RIGHT: Feature Cards */}
        <div className="absolute right-8 top-1/2 -translate-y-1/2 z-30 hidden xl:flex flex-col gap-4">
          {featureCards.map((feat, index) => (
            <motion.div
              key={feat.title}
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.6 + (index * 0.1), ease: "easeOut" }}
              className="glass-card flex items-center gap-4 px-4 py-3 rounded-2xl w-64 group hover:-translate-x-2 transition-transform cursor-pointer"
            >
              <div className="w-10 h-10 rounded-xl bg-accent-purple/10 border border-accent-purple/20 flex items-center justify-center shrink-0 group-hover:bg-accent-purple/20 transition-colors">
                <feat.icon size={18} className="text-accent-purple" />
              </div>
              <div>
                <h4 className="text-white text-sm font-semibold">{feat.title}</h4>
                <p className="text-text-muted text-[11px] font-medium">{feat.sub}</p>
              </div>
            </motion.div>
          ))}
        </div>

        {/* BOTTOM: Studio Module Icon Row */}
        <motion.div 
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.8, ease: "easeOut" }}
          className="absolute bottom-8 left-1/2 -translate-x-1/2 z-30 w-full max-w-5xl px-8 hidden md:block"
        >
          <div className="glass-card rounded-2xl px-8 py-5 flex items-center justify-between">
            {studioModules.map((mod, index) => (
              <Link key={mod.label} href={mod.href} className="flex flex-col items-center gap-3 group">
                <div className="w-12 h-12 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-text-secondary group-hover:text-white group-hover:bg-accent-purple/20 group-hover:border-accent-purple/30 group-hover:shadow-glow-purple transition-all duration-300 group-hover:-translate-y-1">
                  <mod.icon size={22} strokeWidth={1.5} />
                </div>
                <span className="text-[10px] font-semibold text-text-muted group-hover:text-white transition-colors">{mod.label}</span>
              </Link>
            ))}
          </div>
        </motion.div>
      </section>
    </div>
  );
}

function ArrowRight({ size, className }: { size: number; className?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <path d="M5 12h14" />
      <path d="m12 5 7 7-7 7" />
    </svg>
  );
}
