import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });

export const metadata: Metadata = {
  title: 'Iyke Content Studio — AI-Powered Video Production',
  description: 'From script to screen in hours. Create movies, cartoons, ads, and news videos with AI on Iyke Content Studio.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${inter.variable} antialiased`}>
        {children}
        <div id="toast-container" className="fixed bottom-4 right-4 z-50 flex flex-col gap-2" />
      </body>
    </html>
  );
}
