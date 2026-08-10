'use client';
import React from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import Link from 'next/link';
import { Search, Plus } from 'lucide-react';

export default function ProjectsPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold">Projects</h1>
          <p className="text-text-secondary">Manage your video production projects</p>
        </div>
        <Link href="/">
          <Button><Plus size={18} className="mr-2"/> New Project</Button>
        </Link>
      </div>

      <div className="glass p-4 rounded-xl flex gap-4 items-center">
        <div className="flex-1 max-w-md relative">
          <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" />
          <input type="text" placeholder="Search projects..." className="w-full bg-bg-primary border border-white/10 rounded-md py-2 pl-10 pr-4 text-sm" />
        </div>
        <select className="bg-bg-primary border border-white/10 rounded-md py-2 px-4 text-sm">
          <option>All Types</option>
          <option>Movie</option>
          <option>Cartoon</option>
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {[1,2,3].map(i => (
          <Link href={`/projects/${i}`} key={i}>
            <Card variant="interactive" className="p-0 overflow-hidden group flex flex-col">
              <div className="h-40 bg-bg-secondary w-full relative">
                <div className="absolute inset-0 bg-gradient-to-t from-bg-card to-transparent z-10" />
                <Badge status="rendering" className="absolute top-2 right-2 z-20" />
              </div>
              <div className="p-5 flex-1 flex flex-col">
                <h3 className="font-bold text-lg mb-1">Project Alpha {i}</h3>
                <p className="text-xs text-text-secondary mb-4">Movie • 10 mins • Sci-Fi</p>
                <div className="mt-auto">
                  <div className="flex justify-between text-xs mb-1 text-text-secondary">
                    <span>Rendering Scene 4</span>
                    <span>45%</span>
                  </div>
                  <div className="h-1.5 w-full bg-bg-secondary rounded-full overflow-hidden">
                    <div className="h-full bg-accent-primary w-[45%]" />
                  </div>
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
