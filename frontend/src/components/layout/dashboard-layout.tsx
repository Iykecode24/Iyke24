import React from 'react';
import Link from 'next/link';
import { Sidebar } from './sidebar';
import { Header } from './header';

export const DashboardLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="flex min-h-screen bg-bg-secondary overflow-hidden selection:bg-accent-purple/30 selection:text-white">
      {/* ── Left Sidebar (bg-primary: #05050B) ── */}
      <Sidebar />
      
      {/* ── Main Content Area (bg-secondary: #0B0B16) ── */}
      <div className="flex-1 flex flex-col min-w-0 relative">
        <Header />
        
        <main className="flex-1 overflow-y-auto overflow-x-hidden relative">
          {children}
        </main>
      </div>
    </div>
  );
};
