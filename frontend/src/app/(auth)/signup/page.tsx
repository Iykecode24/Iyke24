'use client';
import React, { useState } from 'react';
import Link from 'next/link';
import { Film } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { useAuthStore } from '@/stores/auth-store';

export default function SignupPage() {
  const { signup, isLoading } = useAuthStore();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await signup(email, password, name);
  };

  return (
    <Card className="animate-slide-up">
      <div className="flex flex-col items-center mb-8">
        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-accent-primary to-accent-secondary flex items-center justify-center mb-4 shadow-pulse-glow">
          <Film className="text-white" size={24} />
        </div>
        <h1 className="text-2xl font-bold tracking-wider gradient-text">CREATE ACCOUNT</h1>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <Input label="Display Name" type="text" value={name} onChange={e => setName(e.target.value)} required />
        <Input label="Email Address" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
        <Input label="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} required helperText="Must be at least 8 characters" />
        
        <label className="flex items-start gap-2 cursor-pointer mt-4 text-sm">
          <input type="checkbox" className="rounded border-white/10 bg-bg-secondary mt-1 text-accent-primary focus:ring-accent-primary" required />
          <span className="text-text-secondary">I agree to the Terms of Service and Privacy Policy</span>
        </label>

        <Button type="submit" className="w-full mt-6" isLoading={isLoading} size="lg">Sign Up</Button>
      </form>

      <p className="text-center text-sm text-text-secondary mt-6">
        Already have an account? <Link href="/login" className="text-accent-secondary hover:text-accent-primary font-medium">Log in</Link>
      </p>
    </Card>
  );
}
