'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Mail, Send, Plus } from 'lucide-react';

interface Message {
  id: number;
  channel_id: number | null;
  sender_id: number;
  recipient_id: number | null;
  message: string;
  is_read: boolean;
  created_at: string;
}

export default function MessagesPage() {
  const [selectedChannel, setSelectedChannel] = useState<number | null>(null);

  const { data: channels = [] } = useQuery({
    queryKey: ['messaging', 'channels'],
    queryFn: async () => {
      const response = await api.get('/api/messaging/channels/');
      return response.data;
    },
  });

  const { data: messages = [] } = useQuery({
    queryKey: ['messaging', 'messages', selectedChannel],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (selectedChannel) params.append('channel_id', selectedChannel.toString());
      const response = await api.get(`/api/messaging/messages/?${params}`);
      return response.data;
    },
  });

  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Internal Messages</h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Team communication and internal chat
          </p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
          <Plus className="h-5 w-5" />
          New Channel
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <h3 className="font-semibold text-gray-900 dark:text-white mb-4">Channels</h3>
          <div className="space-y-2">
            {channels.map((channel: any) => (
              <button
                key={channel.id}
                onClick={() => setSelectedChannel(channel.id)}
                className={`w-full text-left p-2 rounded-lg ${
                  selectedChannel === channel.id
                    ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
                    : 'hover:bg-gray-50 dark:hover:bg-gray-700'
                }`}
              >
                {channel.name}
              </button>
            ))}
          </div>
        </div>
        <div className="md:col-span-2 bg-white dark:bg-gray-800 rounded-lg shadow p-4">
          <div className="h-96 overflow-y-auto space-y-4 mb-4">
            {messages.map((message: Message) => (
              <div key={message.id} className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <p className="text-sm text-gray-900 dark:text-white">{message.message}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  {new Date(message.created_at).toLocaleString()}
                </p>
              </div>
            ))}
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Type a message..."
              className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700"
            />
            <button className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
              <Send className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
