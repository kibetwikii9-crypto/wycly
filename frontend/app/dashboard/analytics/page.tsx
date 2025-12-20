'use client';

import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

export default function AnalyticsPage() {
  const { data: intentData } = useQuery({
    queryKey: ['analytics', 'intents'],
    queryFn: async () => {
      const response = await api.get('/api/dashboard/analytics/intents?days=30');
      return response.data;
    },
  });

  const { data: channelData } = useQuery({
    queryKey: ['analytics', 'channels'],
    queryFn: async () => {
      const response = await api.get('/api/dashboard/analytics/channels?days=30');
      return response.data;
    },
  });

  const { data: timelineData } = useQuery({
    queryKey: ['analytics', 'timeline'],
    queryFn: async () => {
      const response = await api.get('/api/dashboard/analytics/timeline?days=7');
      return response.data;
    },
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Analytics & Reports
        </h1>
        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Detailed analytics and insights
        </p>
      </div>

      {/* Intent Frequency Chart */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
          Intent Frequency (Last 30 Days)
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={intentData?.intents || []}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="intent" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#0ea5e9" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Timeline Chart */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
          Conversation Timeline (Last 7 Days)
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={timelineData?.timeline || []}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="count" stroke="#0ea5e9" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Channel Performance */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
          Channel Performance
        </h3>
        <div className="space-y-4">
          {channelData?.channels?.map((channel: any) => (
            <div key={channel.channel} className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-900 dark:text-white capitalize">
                {channel.channel}
              </span>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {channel.unique_users} users
                </span>
                <span className="text-sm font-semibold text-gray-900 dark:text-white">
                  {channel.total_conversations} conversations
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}



