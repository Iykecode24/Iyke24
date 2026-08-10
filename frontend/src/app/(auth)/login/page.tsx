'use client';
import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { motion } from 'framer-motion';

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-bg-primary flex flex-col items-center justify-center relative overflow-hidden selection:bg-accent-purple/30 selection:text-white">
      
      {/* ── Background Effects ── */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-accent-purple/10 rounded-full blur-[100px] pointer-events-none" />
        <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-accent-blue/10 rounded-full blur-[100px] pointer-events-none" />
      </div>

      {/* ── Login Container ── */}
      <motion.div 
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        className="relative z-10 w-full max-w-md px-6"
      >
        {/* Logo */}
        <div className="flex justify-center mb-8">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="relative w-12 h-12 rounded-lg overflow-hidden border border-white/20 group-hover:border-accent-purple transition-colors shadow-lg">
              <Image src="/brand-hero.png" alt="Logo" fill className="object-cover object-top" />
            </div>
            <span className="text-[11px] font-bold text-text-secondary leading-[1.1] tracking-widest mt-1">
              CONTENT<br />STUDIO
            </span>
          </Link>
        </div>

        {/* Glass Card */}
        <div className="glass-card rounded-2xl p-8 shadow-card relative overflow-hidden">
          
          <h2 className="text-white text-2xl font-bold mb-2 text-center">Welcome back</h2>
          <p className="text-text-secondary text-sm text-center mb-8">Sign in to your account to continue</p>

          {/* Social Logins */}
          <div className="flex gap-4 mb-6">
            <button className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-lg bg-white/5 border border-border hover:bg-white/10 hover:border-white/20 transition-all text-white text-sm font-medium">
              <svg viewBox="0 0 24 24" width="18" height="18" xmlns="http://www.w3.org/2000/svg"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
              Google
            </button>
            <button className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-lg bg-white/5 border border-border hover:bg-white/10 hover:border-white/20 transition-all text-white text-sm font-medium">
              <svg viewBox="0 0 24 24" width="18" height="18" xmlns="http://www.w3.org/2000/svg" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.469h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.469h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
              Facebook
            </button>
          </div>

          <div className="relative flex items-center py-5">
            <div className="flex-grow border-t border-border"></div>
            <span className="flex-shrink-0 mx-4 text-text-muted text-xs font-medium uppercase">Or continue with</span>
            <div className="flex-grow border-t border-border"></div>
          </div>

          {/* Form */}
          <form className="space-y-4">
            <div>
              <label className="block text-text-secondary text-xs font-medium mb-1.5">Email address</label>
              <input 
                type="email" 
                placeholder="you@example.com" 
                className="w-full bg-white/5 border border-border rounded-lg px-4 py-2.5 text-sm text-white placeholder:text-text-muted focus:outline-none focus:border-accent-purple/50 focus:bg-white/10 transition-all"
              />
            </div>
            <div>
              <label className="block text-text-secondary text-xs font-medium mb-1.5">Password</label>
              <input 
                type="password" 
                placeholder="••••••••" 
                className="w-full bg-white/5 border border-border rounded-lg px-4 py-2.5 text-sm text-white placeholder:text-text-muted focus:outline-none focus:border-accent-purple/50 focus:bg-white/10 transition-all"
              />
            </div>

            <div className="flex items-center justify-between pt-2">
              <label className="flex items-center gap-2 cursor-pointer group">
                <div className="w-4 h-4 rounded border border-border bg-white/5 flex items-center justify-center group-hover:border-accent-purple transition-colors">
                  <svg className="w-2.5 h-2.5 text-accent-purple opacity-0" viewBox="0 0 14 14" fill="none"><path d="M2 7.5L5.5 11L12 3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
                </div>
                <span className="text-xs text-text-secondary group-hover:text-white transition-colors">Remember me</span>
              </label>
              <Link href="/forgot-password" className="text-xs text-accent-purple hover:text-accent-blue transition-colors font-medium">
                Forgot password?
              </Link>
            </div>

            <button type="button" className="w-full mt-4 bg-accent-purple hover:bg-accent-blue text-white text-sm font-semibold py-2.5 rounded-lg transition-all shadow-btn-glow hover:shadow-glow-blue mt-6">
              Sign In
            </button>
          </form>

        </div>

        <p className="text-center text-text-secondary text-sm mt-6">
          Don't have an account?{' '}
          <Link href="/signup" className="text-accent-purple hover:text-accent-blue font-semibold transition-colors">
            Create an account
          </Link>
        </p>

      </motion.div>
    </div>
  );
}
