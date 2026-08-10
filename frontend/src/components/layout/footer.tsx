import React from 'react';
import Link from 'next/link';

export function Footer() {
  return (
    <footer className="w-full border-t border-white/10 bg-bg-primary/80 backdrop-blur-md py-8 mt-auto z-40">
      <div className="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-text-muted">
        <div>
          &copy; {new Date().getFullYear()} Iyke Content Studio. All rights reserved.
        </div>
        <div className="flex flex-wrap gap-6 justify-center">
          <Link href="/privacy-policy" className="hover:text-accent-primary transition-colors">
            Privacy Policy
          </Link>
          <Link href="/terms-of-service" className="hover:text-accent-primary transition-colors">
            Terms of Service
          </Link>
          <Link href="/data-deletion" className="hover:text-accent-primary transition-colors">
            Data Deletion
          </Link>
          <Link href="/social-account-removal" className="hover:text-accent-primary transition-colors">
            Social Account Removal
          </Link>
        </div>
      </div>
    </footer>
  );
}
