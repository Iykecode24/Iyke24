'use client';
import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  TrendingUp, Users, Eye, ThumbsUp, MessageCircle, Share2, 
  Sparkles, Calendar, Clock, Hash, MousePointerClick, Activity
} from 'lucide-react';

const METRICS = [
  { label: 'Total Views (30d)', value: '1.2M', change: '+15%', trend: 'up' },
  { label: 'Avg Engagement Rate', value: '4.8%', change: '+0.5%', trend: 'up' },
  { label: 'Followers Gained', value: '8.4K', change: '-2%', trend: 'down' },
  { label: 'Est. Revenue', value: '$4,250', change: '+22%', trend: 'up' },
];

const TOP_POSTS = [
  { id: '1', title: 'The Last Horizon Trailer', platform: 'YouTube', views: '450K', engagement: '8.2%' },
  { id: '2', title: 'Summer Sneaker Sale', platform: 'Instagram Reels', views: '280K', engagement: '5.1%' },
  { id: '3', title: 'How Quantum Computers Work', platform: 'TikTok', views: '150K', engagement: '12.4%' },
  { id: '4', title: 'Startup Pitch Deck Tips', platform: 'LinkedIn', views: '45K', engagement: '3.8%' }
];

export default function AnalyticsDashboardPage() {
  const [timeRange, setTimeRange] = useState('30d');
  const [showAiAssistant, setShowAiAssistant] = useState(false);

  return (
    <div className="space-y-8 animate-fade-in pb-12 relative">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold mb-1">Unified Analytics</h1>
          <p className="text-text-secondary">Track cross-platform performance and let AI optimize your strategy.</p>
        </div>
        <div className="flex gap-2">
          <select 
            className="bg-bg-secondary border border-white/10 rounded-lg px-4 py-2 text-sm text-white focus:outline-none"
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
          >
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
            <option value="all">All Time</option>
          </select>
          <Button 
            className="gap-2 bg-gradient-to-r from-accent-purple to-accent-blue text-white border-0 shadow-lg shadow-accent-purple/20"
            onClick={() => setShowAiAssistant(!showAiAssistant)}
          >
            <Sparkles size={16} /> AI Assistant
          </Button>
        </div>
      </div>

      {/* Main KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {METRICS.map((metric, i) => (
          <Card key={i} className="p-5 bg-bg-card/50 border-white/10 hover:border-white/20 transition-all">
            <div className="text-sm text-text-muted mb-2">{metric.label}</div>
            <div className="flex items-end justify-between">
              <div className="text-3xl font-bold text-white">{metric.value}</div>
              <div className={`text-sm font-medium flex items-center gap-1 ${metric.trend === 'up' ? 'text-accent-green' : 'text-accent-red'}`}>
                {metric.trend === 'up' ? <TrendingUp size={14} /> : <TrendingUp size={14} className="rotate-180" />} 
                {metric.change}
              </div>
            </div>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Placeholder for Chart */}
        <Card className="p-6 col-span-2 border-white/10 bg-bg-card/50 flex flex-col">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-bold text-lg text-white">Cross-Platform Growth</h3>
            <div className="flex gap-2">
              <span className="flex items-center gap-1 text-xs text-text-muted"><div className="w-2 h-2 rounded-full bg-red-500"></div> YouTube</span>
              <span className="flex items-center gap-1 text-xs text-text-muted"><div className="w-2 h-2 rounded-full bg-pink-500"></div> Instagram</span>
              <span className="flex items-center gap-1 text-xs text-text-muted"><div className="w-2 h-2 rounded-full bg-white"></div> TikTok</span>
            </div>
          </div>
          <div className="flex-1 min-h-[300px] border border-white/5 rounded-xl bg-bg-primary/50 flex items-center justify-center relative overflow-hidden">
            <div className="absolute inset-0 flex items-end justify-between px-10 pb-10 opacity-30">
              {/* Simulated Chart Bars */}
              {[30, 45, 25, 60, 80, 50, 90, 75, 100, 65, 85, 120].map((h, i) => (
                <div key={i} className="w-8 flex flex-col justify-end gap-1 h-full">
                  <div className="w-full bg-white rounded-t-sm" style={{ height: `${h * 0.4}%` }}></div>
                  <div className="w-full bg-pink-500 rounded-t-sm" style={{ height: `${h * 0.3}%` }}></div>
                  <div className="w-full bg-red-500 rounded-t-sm" style={{ height: `${h * 0.2}%` }}></div>
                </div>
              ))}
            </div>
            <div className="z-10 text-text-muted flex items-center gap-2">
              <Activity size={20} /> Interactive Chart Rendering Engine
            </div>
          </div>
        </Card>

        {/* Top Performing Content */}
        <Card className="p-6 border-white/10 bg-bg-card/50">
          <h3 className="font-bold text-lg text-white mb-6">Top Performing Content</h3>
          <div className="space-y-4">
            {TOP_POSTS.map((post, i) => (
              <div key={post.id} className="group p-3 -mx-3 rounded-xl hover:bg-white/5 transition-colors cursor-pointer flex items-center gap-4">
                <div className="w-8 h-8 rounded-full bg-bg-secondary flex items-center justify-center font-bold text-sm text-text-muted shrink-0 group-hover:bg-accent-primary group-hover:text-white transition-colors">
                  {i + 1}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="font-bold text-white text-sm truncate">{post.title}</div>
                  <div className="text-xs text-text-muted mt-1">{post.platform}</div>
                </div>
                <div className="text-right shrink-0">
                  <div className="text-sm font-bold text-white">{post.views}</div>
                  <div className="text-[10px] text-accent-green">{post.engagement} ER</div>
                </div>
              </div>
            ))}
          </div>
          <Button variant="ghost" className="w-full mt-4 text-xs">View All Content Rankings</Button>
        </Card>
      </div>

      {/* AI Analytics Assistant Widget */}
      {showAiAssistant && (
        <Card className="fixed bottom-6 right-6 w-96 max-w-[calc(100vw-3rem)] shadow-2xl border-accent-purple/30 bg-bg-card/95 backdrop-blur-xl z-50 animate-slide-up overflow-hidden">
          <div className="bg-gradient-to-r from-accent-purple/20 to-accent-blue/20 p-4 border-b border-white/10 flex justify-between items-center">
            <h3 className="font-bold text-white flex items-center gap-2">
              <Sparkles size={18} className="text-accent-purple" /> Studio Intelligence
            </h3>
            <button onClick={() => setShowAiAssistant(false)} className="text-text-muted hover:text-white">✕</button>
          </div>
          
          <div className="p-5 space-y-6 max-h-[60vh] overflow-y-auto hide-scrollbar">
            <div className="space-y-2">
              <div className="text-xs font-bold text-text-muted uppercase tracking-wider flex items-center gap-2">
                <Clock size={12} /> Optimal Posting Times
              </div>
              <div className="bg-white/5 p-3 rounded-xl border border-white/5 text-sm text-white leading-relaxed">
                Based on your last 30 days of data, your audience is most active on <strong>Thursdays at 6:00 PM EST</strong> and <strong>Sundays at 11:00 AM EST</strong>. I recommend scheduling your next TikTok upload for Thursday evening.
              </div>
            </div>

            <div className="space-y-2">
              <div className="text-xs font-bold text-text-muted uppercase tracking-wider flex items-center gap-2">
                <Hash size={12} /> Trending Hashtags
              </div>
              <div className="flex flex-wrap gap-2">
                <Badge className="bg-accent-blue/20 text-accent-blue border-0">#AIAnimation</Badge>
                <Badge className="bg-accent-blue/20 text-accent-blue border-0">#Storytelling</Badge>
                <Badge className="bg-accent-blue/20 text-accent-blue border-0">#TechNews</Badge>
              </div>
              <p className="text-xs text-text-secondary mt-1">These tags yielded a 22% higher CTR on your recent Instagram Reels.</p>
            </div>

            <div className="space-y-2">
              <div className="text-xs font-bold text-text-muted uppercase tracking-wider flex items-center gap-2">
                <Eye size={12} /> Content Recommendations
              </div>
              <div className="bg-accent-purple/10 p-3 rounded-xl border border-accent-purple/20 text-sm text-white leading-relaxed">
                Your <strong>Explainer Videos</strong> between 45-60 seconds have the highest retention rate (68%). Your recent videos over 2 minutes saw a sharp drop-off at the 1:15 mark. Consider splitting long-form topics into multiple short parts.
              </div>
            </div>
            
            <Button className="w-full bg-accent-purple hover:bg-accent-purple/90 text-white border-0 gap-2">
              Apply Recommendations to Next Render
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
}
