'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Building2, Plus, Users, Edit, Trash2 } from 'lucide-react';

interface Department {
  id: number;
  name: string;
  description: string | null;
  manager_id: number | null;
  is_active: boolean;
}

export default function DepartmentsPage() {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const queryClient = useQueryClient();

  const { data: departments = [] } = useQuery({
    queryKey: ['hr', 'departments'],
    queryFn: async () => {
      const response = await api.get('/api/hr/departments/');
      return response.data;
    },
  });

  return (
    <div className="p-6">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Departments</h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Manage organizational structure and departments
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
        >
          <Plus className="h-5 w-5" />
          New Department
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {departments.map((dept: Department) => (
          <div key={dept.id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <Building2 className="h-8 w-8 text-primary-500" />
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white">{dept.name}</h3>
                  {dept.description && (
                    <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{dept.description}</p>
                  )}
                </div>
              </div>
            </div>
            <div className="flex items-center justify-between mt-4">
              <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400">
                <Users className="h-4 w-4" />
                <span>0 employees</span>
              </div>
              <div className="flex items-center gap-2">
                <button className="text-primary-600 hover:text-primary-900">
                  <Edit className="h-5 w-5" />
                </button>
                <button className="text-red-600 hover:text-red-900">
                  <Trash2 className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

