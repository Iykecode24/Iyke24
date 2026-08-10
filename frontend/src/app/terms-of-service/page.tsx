import React from 'react';

export default function TermsOfServicePage() {
  return (
    <div className="min-h-screen bg-bg-primary text-text-primary py-20 px-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl md:text-5xl font-bold mb-8 gradient-text">Terms of Service</h1>
        <p className="text-text-secondary mb-12">Last updated: August 1, 2026</p>
        
        <div className="space-y-8 stagger-children">
          <section className="glass p-8 rounded-2xl">
            <h2 className="text-2xl font-bold mb-4 text-accent-primary">1. Acceptance of Terms</h2>
            <p className="text-text-secondary">By accessing or using Iyke Content Studio, you agree to be bound by these Terms of Service. If you disagree with any part of the terms, you may not access the service.</p>
          </section>

          <section className="glass p-8 rounded-2xl">
            <h2 className="text-2xl font-bold mb-4 text-accent-primary">2. Social Publishing & Content Distribution</h2>
            <p className="text-text-secondary mb-4">Our service allows you to connect your social media accounts to publish content directly.</p>
            <ul className="list-disc list-inside text-text-secondary space-y-2">
              <li>You are solely responsible for the content you generate and publish through our platform.</li>
              <li>You must comply with the terms of service, community guidelines, and acceptable use policies of any third-party network you publish to (e.g., YouTube, Meta, TikTok, LinkedIn, X).</li>
              <li>We reserve the right to suspend or terminate your publishing privileges if your content violates our terms or the terms of connected third-party platforms.</li>
              <li>We do not guarantee the performance, reach, or engagement of any content published through our tools.</li>
            </ul>
          </section>

          <section className="glass p-8 rounded-2xl">
            <h2 className="text-2xl font-bold mb-4 text-accent-primary">3. Third-Party Disclaimers</h2>
            <p className="text-text-secondary mb-4">Iyke Content Studio integrates with various third-party APIs and services.</p>
            <ul className="list-disc list-inside text-text-secondary space-y-2">
              <li>We are not affiliated with, endorsed by, or sponsored by YouTube, Google, Meta, TikTok, LinkedIn, or X.</li>
              <li>Service interruptions on third-party platforms are beyond our control, and we are not liable for any delays or failures in publishing caused by these networks.</li>
              <li>Your use of third-party integrations is at your own risk and subject to the respective third-party's terms and privacy policies.</li>
            </ul>
          </section>

          <section className="glass p-8 rounded-2xl">
            <h2 className="text-2xl font-bold mb-4 text-accent-primary">4. Limitation of Liability</h2>
            <p className="text-text-secondary">In no event shall Iyke Content Studio, nor its directors, employees, partners, agents, suppliers, or affiliates, be liable for any indirect, incidental, special, consequential or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from your access to or use of or inability to access or use the Service.</p>
          </section>
        </div>
      </div>
    </div>
  );
}
