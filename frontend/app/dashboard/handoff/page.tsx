'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { MessageSquare, User, Clock, AlertCircle, CheckCircle2, UserCheck } from 'lucide-react';
import TimeAgo from '@/components/TimeAgo';

interface Handoff {
  id: number;
  conversation_id: number;
  assigned_to_user_id: number | null;
  status: string;
  priority: string;
  reason: string | null;
  assigned_at: string | null;
  resolved_at: string | null;
  created_at: string;
}

export default function HandoffPage() {
  const [statusFilter, setStatusFilter] = useState<string>('');
  const queryClient = useQueryClient();

  const { data: handoffs = [], isLoading } = useQuery<Handoff[]>({
    queryKey: ['handoffs', statusFilter],
    queryFn: async () => {
      const response = await api.get('/api/handoff/', {
        params: { status: statusFilter || undefined },
      });
      return response.data;
    },
    refetchInterval: 30000,
  });

  const updateHandoffMutation = useMutation({
    mutationFn: async ({ id, data }: { id: number; data: any }) => {
      const response = await api.put(`/api/handoff/${id}`, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['handoffs'] });
    },
  });

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent':
        return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      case 'high':
        return 'bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-400';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400';
      default:
        return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'resolved':
        return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400';
      case 'assigned':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-400';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Human Handoff & Agent Workspace
        </h1>
        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Manage AI-to-human transitions and agent workflows
        </p>
      </div>

      {/* Filters */}
      <div className="flex gap-2">
        <button
          onClick={() => setStatusFilter('')}
          className={`px-4 py-2 text-sm font-medium rounded-lg ${
            statusFilter === ''
              ? 'bg-primary-600 text-white'
              : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
          }`}
        >
          All
        </button>
        <button
          onClick={() => setStatusFilter('pending')}
          className={`px-4 py-2 text-sm font-medium rounded-lg ${
            statusFilter === 'pending'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
          }`}
        >
          Pending
        </button>
        <button
          onClick={() => setStatusFilter('assigned')}
          className={`px-4 py-2 text-sm font-medium rounded-lg ${
            statusFilter === 'assigned'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
          }`}
        >
          Assigned
        </button>
        <button
          onClick={() => setStatusFilter('in_progress')}
          className={`px-4 py-2 text-sm font-medium rounded-lg ${
            statusFilter === 'in_progress'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
          }`}
        >
          In Progress
        </button>
      </div>

      {/* Handoffs List */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
            Agent Inbox ({handoffs.length})
          </h3>
          <div className="space-y-3">
            {handoffs.map((handoff) => (
              <div
                key={handoff.id}
                className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg"
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-3">
                    <MessageSquare className="h-5 w-5 text-gray-400" />
                    <div>
                      <h4 className="text-sm font-medium text-gray-900 dark:text-white">
                        Conversation #{handoff.conversation_id}
                      </h4>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        <TimeAgo timestamp={handoff.created_at} />
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${getPriorityColor(handoff.priority)}`}>
                      {handoff.priority} priority
                    </span>
                    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${getStatusColor(handoff.status)}`}>
                      {handoff.status}
                    </span>
                  </div>
                </div>
                {handoff.reason && (
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                    Reason: {handoff.reason}
                  </p>
                )}
                {handoff.status === 'pending' && (
                  <button
                    onClick={() => updateHandoffMutation.mutate({
                      id: handoff.id,
                      data: { status: 'assigned', assigned_to_user_id: 1 }, // TODO: Get current user ID
                    })}
                    className="mt-3 text-sm text-primary-600 hover:text-primary-700"
                  >
                    Assign to me
                  </button>
                )}
              </div>
            ))}
            {handoffs.length === 0 && (
              <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                <UserCheck className="h-12 w-12 mx-auto mb-3 opacity-50" />
                <p>No handoffs found</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
