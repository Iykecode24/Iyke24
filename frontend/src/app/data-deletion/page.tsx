import React from 'react';
import Link from 'next/link';

export default function DataDeletionPage() {
  return (
    <div className="min-h-screen bg-bg-primary text-text-primary py-20 px-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl md:text-5xl font-bold mb-8 gradient-text text-accent-red">Data Deletion Instructions</h1>
        
        <div className="space-y-8 stagger-children">
          <section className="glass p-8 rounded-2xl">
            <p className="text-text-secondary mb-6 text-lg">
              We respect your right to privacy and your right to be forgotten. If you wish to delete your data from Iyke Content Studio, follow the instructions below.
            </p>
            
            <h2 className="text-2xl font-bold mb-4 text-white">How to Delete Your Account and Data</h2>
            <ol className="list-decimal list-inside text-text-secondary space-y-4 mb-8">
              <li>Log in to your Iyke Content Studio account.</li>
              <li>Navigate to the <Link href="/settings" className="text-accent-secondary hover:underline">Settings</Link> page.</li>
              <li>Scroll down to the &quot;Danger Zone&quot; section.</li>
              <li>Click on the &quot;Delete Account&quot; button.</li>
              <li>Confirm your decision by typing your email address in the prompt.</li>
            </ol>
            
            <h2 className="text-2xl font-bold mb-4 text-white">What Happens When You Delete Your Account?</h2>
            <ul className="list-disc list-inside text-text-secondary space-y-2 mb-8">
              <li>All your generated content, scripts, and media files will be permanently deleted.</li>
              <li>All connected social media OAuth tokens will be revoked and deleted from our servers.</li>
              <li>Your personal profile information (name, email) will be purged.</li>
              <li>This action is irreversible. We cannot recover your data once it is deleted.</li>
            </ul>
            
            <div className="bg-red-500/10 border border-red-500/30 p-6 rounded-xl">
              <h3 className="text-xl font-bold text-accent-red mb-2">Need Help?</h3>
              <p className="text-text-secondary">If you are unable to access your account to perform the deletion, please contact our support team at <a href="mailto:privacy@iykecontent.studio" className="text-accent-primary hover:underline">privacy@iykecontent.studio</a> with the subject &quot;Data Deletion Request&quot;. We will process your request within 7 business days.</p>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
