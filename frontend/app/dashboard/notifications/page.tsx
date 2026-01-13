'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Bell, Mail, Smartphone, CheckCircle2, Clock } from 'lucide-react';
import TimeAgo from '@/components/TimeAgo';

interface Notification {
  id: number;
  type: string;
  title: string;
  message: string;
  category: string | null;
  is_read: boolean;
  action_url: string | null;
  created_at: string;
}

export default function NotificationsPage() {
  const queryClient = useQueryClient();
  const [filter, setFilter] = useState<'all' | 'unread'>('unread');

  const { data: notifications = [], isLoading } = useQuery<Notification[]>({
    queryKey: ['notifications', filter],
    queryFn: async () => {
      const response = await api.get('/api/notifications/', {
        params: { is_read: filter === 'unread' ? false : undefined },
      });
      return response.data;
    },
    refetchInterval: 30000,
  });

  const { data: unreadCount = { count: 0 } } = useQuery({
    queryKey: ['notifications', 'unread-count'],
    queryFn: async () => {
      const response = await api.get('/api/notifications/unread-count');
      return response.data;
    },
    refetchInterval: 30000,
  });

  const markReadMutation = useMutation({
    mutationFn: async (id: number) => {
      await api.post(`/api/notifications/${id}/read`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    },
  });

  const markAllReadMutation = useMutation({
    mutationFn: async () => {
      await api.post('/api/notifications/mark-all-read');
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Notifications & Alerts
          </h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Manage your notifications and preferences
          </p>
        </div>
        {unreadCount.count > 0 && (
          <button
            onClick={() => markAllReadMutation.mutate()}
            className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
          >
            Mark All Read
          </button>
        )}
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 border-b border-gray-200 dark:border-gray-700">
        <button
          onClick={() => setFilter('unread')}
          className={`px-4 py-2 text-sm font-medium border-b-2 ${
            filter === 'unread'
              ? 'border-primary-600 text-primary-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
          }`}
        >
          Unread ({unreadCount.count})
        </button>
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 text-sm font-medium border-b-2 ${
            filter === 'all'
              ? 'border-primary-600 text-primary-600'
              : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
          }`}
        >
          All
        </button>
      </div>

      {/* Notifications List */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700">
        <div className="divide-y divide-gray-200 dark:divide-gray-700">
          {notifications.map((notification) => (
            <div
              key={notification.id}
              className={`p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 ${
                !notification.is_read ? 'bg-primary-50 dark:bg-primary-900/10' : ''
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3 flex-1">
                  <Bell
                    className={`h-5 w-5 mt-0.5 ${
                      notification.is_read ? 'text-gray-400' : 'text-primary-500'
                    }`}
                  />
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h4 className="text-sm font-medium text-gray-900 dark:text-white">
                        {notification.title}
                      </h4>
                      {!notification.is_read && (
                        <span className="h-2 w-2 rounded-full bg-primary-500" />
                      )}
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      {notification.message}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      <TimeAgo timestamp={notification.created_at} />
                    </p>
                  </div>
                </div>
                {!notification.is_read && (
                  <button
                    onClick={() => markReadMutation.mutate(notification.id)}
                    className="ml-4 text-xs text-primary-600 hover:text-primary-700"
                  >
                    Mark read
                  </button>
                )}
              </div>
            </div>
          ))}
          {notifications.length === 0 && (
            <div className="text-center py-12 text-gray-500 dark:text-gray-400">
              <Bell className="h-12 w-12 mx-auto mb-3 opacity-50" />
              <p>No notifications</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
