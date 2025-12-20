'use client';

import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import {
  MessageSquare,
  Users,
  TrendingUp,
  Zap,
  ArrowUpRight,
  ArrowDownRight,
} from 'lucide-react';

interface OverviewData {
  total_conversations: number;
  active_chats: number;
  leads_captured: number;
  most_common_intents: Array<{ intent: string; count: number }>;
  channel_distribution: Array<{ channel: string; count: number }>;
  period_days: number;
}

export default function DashboardPage() {
  const { data, isLoading } = useQuery<OverviewData>({
    queryKey: ['dashboard', 'overview'],
    queryFn: async () => {
      const response = await api.get('/api/dashboard/overview');
      return response.data;
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  const stats = [
    {
      name: 'Total Conversations',
      value: data?.total_conversations || 0,
      icon: MessageSquare,
      change: '+12%',
      changeType: 'positive',
    },
    {
      name: 'Active Chats',
      value: data?.active_chats || 0,
      icon: Zap,
      change: '+5%',
      changeType: 'positive',
    },
    {
      name: 'Leads Captured',
      value: data?.leads_captured || 0,
      icon: Users,
      change: '+8%',
      changeType: 'positive',
    },
    {
      name: 'Response Rate',
      value: '98%',
      icon: TrendingUp,
      change: '+2%',
      changeType: 'positive',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Overview
        </h1>
        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Your chatbot performance at a glance
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <div
            key={stat.name}
            className="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg border border-gray-200 dark:border-gray-700"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <stat.icon className="h-6 w-6 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">
                      {stat.name}
                    </dt>
                    <dd className="flex items-baseline">
                      <div className="text-2xl font-semibold text-gray-900 dark:text-white">
                        {stat.value}
                      </div>
                      <div
                        className={`ml-2 flex items-baseline text-sm font-semibold ${
                          stat.changeType === 'positive'
                            ? 'text-green-600'
                            : 'text-red-600'
                        }`}
                      >
                        {stat.changeType === 'positive' ? (
                          <ArrowUpRight className="h-4 w-4" />
                        ) : (
                          <ArrowDownRight className="h-4 w-4" />
                        )}
                        <span className="sr-only">
                          {' '}
                          {stat.changeType === 'positive' ? 'Increased' : 'Decreased'} by{' '}
                        </span>
                        {stat.change}
                      </div>
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Most Common Intents */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">
            Most Common Intents
          </h3>
          <div className="mt-5">
            <div className="space-y-4">
              {data?.most_common_intents.map((item, index) => (
                <div key={item.intent} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <span className="text-sm font-medium text-gray-500 dark:text-gray-400 w-8">
                      #{index + 1}
                    </span>
                    <span className="text-sm font-medium text-gray-900 dark:text-white capitalize">
                      {item.intent}
                    </span>
                  </div>
                  <span className="text-sm font-semibold text-gray-900 dark:text-white">
                    {item.count}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Channel Distribution */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white">
            Channel Distribution
          </h3>
          <div className="mt-5">
            <div className="space-y-4">
              {data?.channel_distribution.map((item) => (
                <div key={item.channel} className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-900 dark:text-white capitalize">
                    {item.channel}
                  </span>
                  <span className="text-sm font-semibold text-gray-900 dark:text-white">
                    {item.count}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}



