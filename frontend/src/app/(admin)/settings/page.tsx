'use client';
import React from 'react';
import { Card } from '@/components/ui/card';
import Link from 'next/link';
import { Settings, Cpu, Users, Link as LinkIcon, Database, Shield, DollarSign } from 'lucide-react';

export default function SettingsPage() {
  const categories = [
    { title: 'Integrations', desc: 'Manage API keys and external services', icon: <LinkIcon/>, href: '/settings/integrations' },
    { title: 'GPU Infrastructure', desc: 'Manage RunPod instances and rendering nodes', icon: <Cpu/>, href: '/settings/gpu' },
    { title: 'Model Registry', desc: 'Configure AI models for generation', icon: <Database/>, href: '/settings/models' },
    { title: 'Cost Limits', desc: 'Set usage limits and monitoring', icon: <DollarSign/>, href: '/settings/costs' },
    { title: 'Users & Roles', desc: 'Manage access and permissions', icon: <Users/>, href: '/settings/users' },
    { title: 'Security', desc: 'Audit logs and MFA policies', icon: <Shield/>, href: '/settings/security' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Admin Settings</h1>
        <p className="text-text-secondary">Platform configuration and management</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {categories.map((c, i) => (
          <Link href={c.href} key={i}>
            <Card variant="interactive" className="h-full flex items-start gap-4">
              <div className="p-3 rounded-lg bg-bg-secondary text-accent-primary">
                {c.icon}
              </div>
              <div>
                <h3 className="font-semibold text-lg">{c.title}</h3>
                <p className="text-sm text-text-secondary">{c.desc}</p>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
