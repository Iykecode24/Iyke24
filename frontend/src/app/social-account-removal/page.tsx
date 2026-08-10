import React from 'react';
import Link from 'next/link';

export default function SocialAccountRemovalPage() {
  return (
    <div className="min-h-screen bg-bg-primary text-text-primary py-20 px-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl md:text-5xl font-bold mb-8 gradient-text">Social Account Removal</h1>
        
        <div className="space-y-8 stagger-children">
          <section className="glass p-8 rounded-2xl">
            <p className="text-text-secondary mb-6 text-lg">
              You have full control over which social media accounts are connected to Iyke Content Studio. You can revoke our access to your accounts at any time.
            </p>
            
            <h2 className="text-2xl font-bold mb-4 text-accent-primary">Disconnecting from within Iyke Content Studio</h2>
            <ol className="list-decimal list-inside text-text-secondary space-y-2 mb-8">
              <li>Go to <Link href="/settings/connected-accounts" className="text-accent-secondary hover:underline">Settings &gt; Connected Accounts</Link>.</li>
              <li>Find the social media account you wish to disconnect.</li>
              <li>Click the &quot;Disconnect&quot; button next to the account.</li>
              <li>We will immediately delete the OAuth token from our servers and lose access to publish on your behalf.</li>
            </ol>

            <h2 className="text-2xl font-bold mb-4 text-accent-primary">Removing Access via Third-Party Platforms</h2>
            <p className="text-text-secondary mb-4">You can also revoke our access directly from the social networks. Here are the instructions for each platform:</p>
            
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold mb-2 text-white">Google & YouTube</h3>
                <p className="text-text-secondary">Go to your <a href="https://myaccount.google.com/permissions" target="_blank" rel="noopener noreferrer" className="text-accent-secondary hover:underline">Google Account Security Settings</a>, find &quot;Third-party apps with account access&quot;, select Iyke Content Studio, and click &quot;Remove Access&quot;.</p>
              </div>
              
              <div>
                <h3 className="text-xl font-semibold mb-2 text-white">Meta (Facebook & Instagram)</h3>
                <p className="text-text-secondary">Navigate to your Facebook Settings, select &quot;Business Integrations&quot;, find our app, and click &quot;Remove&quot;.</p>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2 text-white">TikTok</h3>
                <p className="text-text-secondary">Open the TikTok app, go to Settings and Privacy &gt; Security and Login &gt; Manage App Permissions, select Iyke Content Studio, and remove access.</p>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
