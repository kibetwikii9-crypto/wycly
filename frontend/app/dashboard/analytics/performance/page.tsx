'use client';

import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Activity, Target, TrendingUp, Users, CheckCircle2, Clock } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

export default function PerformancePage() {
  const { data: projects = [] } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const response = await api.get('/api/projects/projects/');
      return response.data;
    },
  });

  const { data: tasks = [] } = useQuery({
    queryKey: ['tasks'],
    queryFn: async () => {
      const response = await api.get('/api/projects/tasks/');
      return response.data;
    },
  });

  // Calculate performance metrics
  const completedProjects = projects.filter((p: any) => p.status === 'completed').length;
  const activeProjects = projects.filter((p: any) => p.status === 'active').length;
  const completedTasks = tasks.filter((t: any) => t.status === 'done').length;
  const totalTasks = tasks.length;
  const completionRate = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;
  const avgProgress = projects.length > 0 
    ? projects.reduce((sum: number, p: any) => sum + p.progress, 0) / projects.length 
    : 0;

  // Project status distribution
  const projectStatusData = [
    { name: 'Completed', value: completedProjects, color: '#10b981' },
    { name: 'Active', value: activeProjects, color: '#3b82f6' },
    { name: 'Planning', value: projects.filter((p: any) => p.status === 'planning').length, color: '#f59e0b' },
    { name: 'On Hold', value: projects.filter((p: any) => p.status === 'on_hold').length, color: '#ef4444' },
  ];

  // Task status distribution
  const taskStatusData = [
    { name: 'Done', value: completedTasks, color: '#10b981' },
    { name: 'In Progress', value: tasks.filter((t: any) => t.status === 'in_progress').length, color: '#3b82f6' },
    { name: 'Todo', value: tasks.filter((t: any) => t.status === 'todo').length, color: '#f59e0b' },
  ];

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Performance Tracking</h1>
        <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Employee and project performance metrics
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Total Projects</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
                {projects.length}
              </p>
            </div>
            <Target className="h-8 w-8 text-primary-500" />
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Active Projects</p>
              <p className="text-2xl font-bold text-blue-600 dark:text-blue-400 mt-1">
                {activeProjects}
              </p>
            </div>
            <Activity className="h-8 w-8 text-blue-500" />
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Task Completion</p>
              <p className="text-2xl font-bold text-green-600 dark:text-green-400 mt-1">
                {completionRate.toFixed(1)}%
              </p>
            </div>
            <CheckCircle2 className="h-8 w-8 text-green-500" />
          </div>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Avg Progress</p>
              <p className="text-2xl font-bold text-primary-600 dark:text-primary-400 mt-1">
                {avgProgress.toFixed(0)}%
              </p>
            </div>
            <TrendingUp className="h-8 w-8 text-primary-500" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Project Status</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={projectStatusData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Task Status</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={taskStatusData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
