import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  output: 'export',
  reactStrictMode: true,
  images: {
    // Allow local public folder images without needing external domains
    unoptimized: true,
    remotePatterns: [],
  },
  // Redirects are removed because they require a Node.js server.
  // We will handle them via Cloudflare _redirects if needed.
};

export default nextConfig;
