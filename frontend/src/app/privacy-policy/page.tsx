import React from 'react';
import Link from 'next/link';

export default function PrivacyPolicyPage() {
  return (
    <div className="min-h-screen bg-bg-primary text-text-primary py-20 px-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl md:text-5xl font-bold mb-8 gradient-text">Privacy Policy</h1>
        <p className="text-text-secondary mb-12">Last updated: August 1, 2026</p>
        
        <div className="space-y-8 stagger-children">
          <section className="glass p-8 rounded-2xl">
            <h2 className="text-2xl font-bold mb-4 text-accent-primary">1. Introduction</h2>
            <p className="text-text-secondary">Welcome to Iyke Content Studio. We are committed to protecting your personal information and your right to privacy. This privacy policy explains how we collect, use, and share your information when you use our platform.</p>
          </section>

          <section className="glass p-8 rounded-2xl">
            <h2 className="text-2xl font-bold mb-4 text-accent-primary">2. Social Media Integrations</h2>
            <p className="text-text-secondary mb-4">When you connect your social media accounts to publish content directly from our platform, we access certain information required to provide this service.</p>
            
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-semibold mb-2 text-white">YouTube API Services</h3>
                <p className="text-text-secondary">We use YouTube API Services to allow you to upload videos directly to your YouTube channel. By using this integration, you are agreeing to be bound by the YouTube Terms of Service and Google Privacy Policy. We collect your authentication token and channel information strictly for the purpose of publishing your approved content.</p>
              </div>
              
              <div>
                <h3 className="text-xl font-semibold mb-2 text-white">TikTok</h3>
                <p className="text-text-secondary">Our TikTok integration requires access to your account to upload and manage your videos. We do not store your TikTok password; we use OAuth tokens which you can revoke at any time from your settings or directly within TikTok.</p>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2 text-white">Meta (Facebook & Instagram)</h3>
                <p className="text-text-secondary">When publishing to Meta platforms, we process your access tokens to post on your behalf. We only access the pages and accounts you explicitly grant us permission to manage. Data is handled in accordance with Meta's developer policies.</p>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2 text-white">LinkedIn</h3>
                <p className="text-text-secondary">For LinkedIn publishing, we require the w_member_social or w_organization_social scopes. This allows us to create posts on your personal profile or company page. We do not access your direct messages or connections.</p>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-2 text-white">X (formerly Twitter)</h3>
                <p className="text-text-secondary">Our X integration allows for the scheduling and posting of tweets. We utilize the X API v2 and store OAuth tokens to authenticate requests. We only perform actions you explicitly trigger.</p>
              </div>
            </div>
          </section>

          <section className="glass p-8 rounded-2xl">
            <h2 className="text-2xl font-bold mb-4 text-accent-primary">3. Data Retention</h2>
            <p className="text-text-secondary">We retain your personal information only for as long as is necessary for the purposes set out in this Privacy Policy. Active OAuth tokens are retained as long as your account is active or until you disconnect the specific integration. If you delete your account, all associated social tokens, generated content, and personal data are permanently deleted from our active databases within 30 days. For instructions on how to remove your data immediately, see our <Link href="/data-deletion" className="text-accent-secondary hover:underline">Data Deletion Policy</Link>.</p>
          </section>
        </div>
      </div>
    </div>
  );
}
