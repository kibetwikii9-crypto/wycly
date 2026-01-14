'use client';

import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { TrendingUp, Plus } from 'lucide-react';

interface PipelineOpportunity {
  id: number;
  contact_id: number;
  stage_id: number;
  title: string;
  value: number | null;
  probability: number;
  expected_close_date: string | null;
}

interface PipelineStage {
  id: number;
  name: string;
  order: number;
  color: string | null;
}

export default function PipelinePage() {
  const { data: stages = [] } = useQuery({
    queryKey: ['crm', 'pipeline', 'stages'],
    queryFn: async () => {
      const response = await api.get('/api/crm/pipeline/stages/');
      return response.data;
    },
  });

  const { data: opportunities = [] } = useQuery({
    queryKey: ['crm', 'pipeline', 'opportunities'],
    queryFn: async () => {
      const response = await api.get('/api/crm/pipeline/opportunities/');
      return response.data;
    },
  });

  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Sales Pipeline</h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Track your sales opportunities through the pipeline
          </p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
          <Plus className="h-5 w-5" />
          New Opportunity
        </button>
      </div>

      <div className="flex gap-4 overflow-x-auto pb-4">
        {stages.map((stage: PipelineStage) => {
          const stageOpportunities = opportunities.filter(
            (opp: PipelineOpportunity) => opp.stage_id === stage.id
          );
          return (
            <div key={stage.id} className="flex-shrink-0 w-80 bg-white dark:bg-gray-800 rounded-lg shadow p-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-gray-900 dark:text-white">{stage.name}</h3>
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {stageOpportunities.length}
                </span>
              </div>
              <div className="space-y-2">
                {stageOpportunities.map((opp: PipelineOpportunity) => (
                  <div
                    key={opp.id}
                    className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600"
                  >
                    <p className="font-medium text-gray-900 dark:text-white">{opp.title}</p>
                    {opp.value && (
                      <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        ${opp.value.toFixed(2)}
                      </p>
                    )}
                    <div className="mt-2 flex items-center gap-2">
                      <div className="flex-1 bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full"
                          style={{ width: `${opp.probability}%` }}
                        />
                      </div>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        {opp.probability}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
