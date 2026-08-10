'use client';
import React from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function IntegrationsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">API Integrations</h1>
        <p className="text-text-secondary">Manage connections to external services</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {['OpenAI', 'RunPod', 'AWS S3'].map(provider => (
          <Card key={provider} className="flex flex-col">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-bold text-lg">{provider}</h3>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-accent-green animate-pulse" />
                <span className="text-xs text-text-secondary">Connected</span>
              </div>
            </div>
            <div className="mt-auto flex gap-2">
              <Button variant="secondary" size="sm" className="flex-1">Configure</Button>
              <Button variant="ghost" size="sm">Test</Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
