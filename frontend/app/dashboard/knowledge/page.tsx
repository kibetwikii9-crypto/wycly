'use client';

import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { useState } from 'react';
import TimeAgo from '@/components/TimeAgo';
import {
  Plus,
  Search,
  Edit,
  Trash2,
  TrendingUp,
  TrendingDown,
  AlertCircle,
  CheckCircle2,
  Clock,
  Tag,
  Download,
  Eye,
  EyeOff,
  Filter,
  X,
  Link as LinkIcon,
  Unlink,
  FileText,
  BarChart3,
  Target,
  Zap,
  Activity,
} from 'lucide-react';

interface KnowledgeEntry {
  id: number;
  question: string;
  answer: string;
  keywords: string[];
  intent: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  usage_count: number;
  quality_signals: string[];
  has_intent_link: boolean;
  last_used: string;
}

interface KnowledgeHealth {
  total_entries: number;
  active_entries: number;
  entries_with_intent: number;
  intents_without_knowledge: string[];
  unused_entries_count: number;
  coverage_percentage: number;
}

interface IntentMapping {
  intent: string;
  conversation_count: number;
  knowledge_entries: Array<{
    id: number;
    question: string;
    is_active: boolean;
  }>;
  has_coverage: boolean;
}

export default function KnowledgePage() {
  const [page, setPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState('');
  const [intentFilter, setIntentFilter] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [selectedEntryId, setSelectedEntryId] = useState<number | null>(null);
  const [showPreview, setShowPreview] = useState(false);

  const { data, isLoading } = useQuery({
    queryKey: ['knowledge', page, intentFilter, statusFilter, searchQuery],
    queryFn: async () => {
      const params = new URLSearchParams({
        page: page.toString(),
        limit: '20',
      });
      if (intentFilter) params.append('intent', intentFilter);
      if (statusFilter) params.append('status', statusFilter);
      if (searchQuery) params.append('search', searchQuery);
      const response = await api.get(`/api/dashboard/knowledge?${params}`);
      return response.data;
    },
    refetchInterval: 30000,
    refetchIntervalInBackground: false,
    refetchOnWindowFocus: true,
    staleTime: 30000,
  });

  const { data: healthData } = useQuery<KnowledgeHealth>({
    queryKey: ['knowledge-health'],
    queryFn: async () => {
      const response = await api.get('/api/dashboard/knowledge/health');
      return response.data;
    },
    refetchInterval: 30000,
    refetchIntervalInBackground: false,
    refetchOnWindowFocus: true,
    staleTime: 30000,
  });

  const { data: mappingData } = useQuery<{ mapping: IntentMapping[] }>({
    queryKey: ['knowledge-mapping'],
    queryFn: async () => {
      const response = await api.get('/api/dashboard/knowledge/mapping');
      return response.data;
    },
    refetchInterval: 30000,
    refetchIntervalInBackground: false,
    refetchOnWindowFocus: true,
    staleTime: 30000,
  });

  const { data: entryDetail } = useQuery({
    queryKey: ['knowledge-entry', selectedEntryId],
    queryFn: async () => {
      const response = await api.get(`/api/dashboard/knowledge/${selectedEntryId}`);
      return response.data;
    },
    enabled: selectedEntryId !== null,
    refetchInterval: selectedEntryId !== null ? 30000 : false,
    refetchIntervalInBackground: false,
    refetchOnWindowFocus: true,
    staleTime: 30000,
  });

  const getQualitySignalColor = (signal: string) => {
    switch (signal) {
      case 'high_performing':
        return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400';
      case 'unused':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
      case 'needs_intent_link':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400';
      case 'inactive':
        return 'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  const getQualitySignalLabel = (signal: string) => {
    switch (signal) {
      case 'high_performing':
        return 'High Performing';
      case 'unused':
        return 'Unused';
      case 'needs_intent_link':
        return 'Needs Intent Link';
      case 'inactive':
        return 'Inactive';
      default:
        return signal;
    }
  };


  const exportKnowledge = () => {
    if (!data) return;
    
    const exportData = {
      entries: data.entries,
      health: healthData,
      mapping: mappingData,
      exported_at: new Date().toISOString(),
    };

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `knowledge-base-export-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Knowledge Base
          </h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Manage FAQs and knowledge entries with intelligent insights
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={exportKnowledge}
            className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 shadow-sm text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
          >
            <Download className="h-4 w-4 mr-2" />
            Export
          </button>
          <button className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700">
            <Plus className="h-5 w-5 mr-2" />
            Add Entry
          </button>
        </div>
      </div>

      {/* Knowledge Health & Coverage Dashboard */}
      {healthData && (
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">
              Knowledge Health & Coverage
            </h3>
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-6">
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400">Total Entries</p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white mt-1">
                  {healthData.total_entries}
                </p>
              </div>
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400">Active</p>
                <p className="text-2xl font-semibold text-green-600 dark:text-green-400 mt-1">
                  {healthData.active_entries}
                </p>
              </div>
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400">With Intent</p>
                <p className="text-2xl font-semibold text-blue-600 dark:text-blue-400 mt-1">
                  {healthData.entries_with_intent}
                </p>
              </div>
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400">Coverage</p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white mt-1">
                  {healthData.coverage_percentage}%
                </p>
              </div>
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400">Unused</p>
                <p className="text-2xl font-semibold text-gray-600 dark:text-gray-400 mt-1">
                  {healthData.unused_entries_count}
                </p>
              </div>
              <div>
                <p className="text-xs text-gray-500 dark:text-gray-400">Gaps</p>
                <p className="text-2xl font-semibold text-yellow-600 dark:text-yellow-400 mt-1">
                  {healthData.intents_without_knowledge.length}
                </p>
              </div>
            </div>
            {healthData.intents_without_knowledge.length > 0 && (
              <div className="mt-4 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-md">
                <p className="text-sm font-medium text-yellow-800 dark:text-yellow-400 mb-1">
                  Intents without knowledge coverage:
                </p>
                <div className="flex flex-wrap gap-2">
                  {healthData.intents_without_knowledge.map((intent, idx) => (
                    <span
                      key={idx}
                      className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400 capitalize"
                    >
                      {intent}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Intent ↔ Knowledge Mapping Visualizer */}
      {mappingData && mappingData.mapping.length > 0 && (
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 dark:text-white mb-4">
              Intent ↔ Knowledge Mapping
            </h3>
            <div className="space-y-3">
              {mappingData.mapping.slice(0, 5).map((item) => (
                <div
                  key={item.intent}
                  className={`p-3 rounded-lg border ${
                    item.has_coverage
                      ? 'border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/10'
                      : 'border-yellow-200 dark:border-yellow-800 bg-yellow-50 dark:bg-yellow-900/10'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-gray-900 dark:text-white capitalize">
                        {item.intent}
                      </span>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        ({item.conversation_count} conversations)
                      </span>
                    </div>
                    {item.has_coverage ? (
                      <CheckCircle2 className="h-4 w-4 text-green-600 dark:text-green-400" />
                    ) : (
                      <AlertCircle className="h-4 w-4 text-yellow-600 dark:text-yellow-400" />
                    )}
                  </div>
                  {item.knowledge_entries.length > 0 && (
                    <div className="mt-2 space-y-1">
                      {item.knowledge_entries.map((entry) => (
                        <div
                          key={entry.id}
                          className="text-xs text-gray-600 dark:text-gray-400 flex items-center gap-2"
                        >
                          <LinkIcon className="h-3 w-3" />
                          {entry.question}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700 p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search knowledge base..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 text-sm"
            />
          </div>
          <select
            value={intentFilter}
            onChange={(e) => setIntentFilter(e.target.value)}
            className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500 text-sm"
          >
            <option value="">All Intents</option>
            <option value="greeting">Greeting</option>
            <option value="help">Help</option>
            <option value="pricing">Pricing</option>
            <option value="human">Human</option>
          </select>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500 text-sm"
          >
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
          <button
            onClick={() => {
              setSearchQuery('');
              setIntentFilter('');
              setStatusFilter('');
            }}
            className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-600"
          >
            Clear Filters
          </button>
        </div>
      </div>

      {/* Knowledge Entries */}
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700">
        {isLoading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : (
          <div className="divide-y divide-gray-200 dark:divide-gray-700">
            {data?.entries?.map((entry: KnowledgeEntry) => (
              <div
                key={entry.id}
                className="p-6 hover:bg-gray-50 dark:hover:bg-gray-700/50 cursor-pointer"
                onClick={() => setSelectedEntryId(entry.id)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                        {entry.question}
                      </h3>
                      {entry.is_active ? (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400">
                          Active
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300">
                          Inactive
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
                      {entry.answer}
                    </p>
                    
                    {/* Quality Signals */}
                    {entry.quality_signals.length > 0 && (
                      <div className="flex flex-wrap gap-2 mb-3">
                        {entry.quality_signals.map((signal, idx) => (
                          <span
                            key={idx}
                            className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${getQualitySignalColor(signal)}`}
                          >
                            {getQualitySignalLabel(signal)}
                          </span>
                        ))}
                      </div>
                    )}

                    {/* Performance Indicators */}
                    <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
                      <div className="flex items-center gap-1">
                        <Activity className="h-4 w-4" />
                        <span>{entry.usage_count} uses</span>
                      </div>
                      {entry.intent && (
                        <div className="flex items-center gap-1">
                          <Tag className="h-4 w-4" />
                          <span className="capitalize">{entry.intent}</span>
                        </div>
                      )}
                      <div className="flex items-center gap-1">
                        <Clock className="h-4 w-4" />
                        <span>Updated <TimeAgo timestamp={entry.updated_at} /></span>
                      </div>
                    </div>

                    {/* Keywords */}
                    {entry.keywords && entry.keywords.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-3">
                        {entry.keywords.map((keyword, idx) => (
                          <span
                            key={idx}
                            className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200"
                          >
                            {keyword}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                  <div className="flex space-x-2 ml-4">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedEntryId(entry.id);
                        setShowPreview(true);
                      }}
                      className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                    >
                      <Eye className="h-5 w-5" />
                    </button>
                    <button className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                      <Edit className="h-5 w-5" />
                    </button>
                    <button className="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400">
                      <Trash2 className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Pagination */}
        {data && data.total_pages > 1 && (
          <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between">
            <div className="text-sm text-gray-700 dark:text-gray-300">
              Showing {((page - 1) * 20) + 1} to {Math.min(page * 20, data.total)} of{' '}
              {data.total} entries
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <button
                onClick={() => setPage((p) => Math.min(data.total_pages, p + 1))}
                disabled={page === data.total_pages}
                className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Entry Detail Modal/Preview */}
      {selectedEntryId && entryDetail && showPreview && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  Knowledge Entry Details
                </h2>
                <button
                  onClick={() => {
                    setShowPreview(false);
                    setSelectedEntryId(null);
                  }}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Question</p>
                  <p className="text-base text-gray-900 dark:text-white">{entryDetail.entry.question}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Answer</p>
                  <p className="text-base text-gray-900 dark:text-white whitespace-pre-wrap">
                    {entryDetail.entry.answer}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Version Info</p>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    <p>Created: {new Date(entryDetail.entry.created_at).toLocaleString()}</p>
                    <p>Updated: {new Date(entryDetail.entry.updated_at).toLocaleString()}</p>
                  </div>
                </div>
                {entryDetail.usage_timeline && entryDetail.usage_timeline.length > 0 && (
                  <div>
                    <p className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Usage Timeline</p>
                    <div className="space-y-2">
                      {entryDetail.usage_timeline.slice(0, 10).map((event: any, idx: number) => (
                        <div key={idx} className="flex items-start gap-3 p-2 bg-gray-50 dark:bg-gray-700 rounded">
                          <Activity className="h-4 w-4 text-blue-600 dark:text-blue-400 mt-0.5" />
                          <div className="flex-1">
                            <p className="text-sm text-gray-900 dark:text-white">
                              Used in conversation
                            </p>
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                              {event.user_message} • <TimeAgo timestamp={event.timestamp} />
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
