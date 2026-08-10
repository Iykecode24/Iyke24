'use client';
import React from 'react';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

export default function CostsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Cost Limits</h1>
      <Card className="max-w-xl">
        <form className="space-y-4">
          <Input label="Per-project Limit ($)" type="number" defaultValue={50} />
          <Input label="Monthly Org Limit ($)" type="number" defaultValue={1000} />
          <Button type="button" className="mt-4">Save Changes</Button>
        </form>
      </Card>
    </div>
  );
}
