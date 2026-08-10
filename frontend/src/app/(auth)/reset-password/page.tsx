'use client';
import React from 'react';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function ResetPasswordPage() {
  return (
    <Card className="animate-slide-up">
      <div className="mb-6 text-center">
        <h1 className="text-2xl font-bold mb-2">Reset Password</h1>
        <p className="text-sm text-text-secondary">Enter your email to receive a reset link</p>
      </div>
      <form className="space-y-4">
        <Input label="Email Address" type="email" required />
        <Button type="submit" className="w-full">Send Reset Link</Button>
      </form>
      <div className="mt-6 text-center">
        <Link href="/login" className="text-sm text-text-secondary hover:text-white">Back to login</Link>
      </div>
    </Card>
  );
}
