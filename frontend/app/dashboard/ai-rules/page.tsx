'use client';

import { useState } from 'react';
import { Plus, Save, Trash2, Edit, Zap } from 'lucide-react';

interface IntentRule {
  id: string;
  intent: string;
  keywords: string[];
  response: string;
  priority: number;
}

export default function AIRulesPage() {
  const [rules, setRules] = useState<IntentRule[]>([
    {
      id: '1',
      intent: 'greeting',
      keywords: ['hi', 'hello', 'hey'],
      response: 'Hello! How can I help you today?',
      priority: 1,
    },
    {
      id: '2',
      intent: 'pricing',
      keywords: ['price', 'cost', 'pricing'],
      response: 'Our pricing plans are flexible. Would you like to know more?',
      priority: 2,
    },
  ]);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);

  const handleSave = (rule: IntentRule) => {
    if (editingId) {
      setRules(rules.map((r) => (r.id === editingId ? rule : r)));
      setEditingId(null);
    } else {
      setRules([...rules, { ...rule, id: Date.now().toString() }]);
      setShowAddForm(false);
    }
  };

  const handleDelete = (id: string) => {
    setRules(rules.filter((r) => r.id !== id));
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            AI Rules & Automation
          </h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Configure intent detection and response rules
          </p>
        </div>
        <button
          onClick={() => setShowAddForm(true)}
          className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
        >
          <Plus className="h-5 w-5 mr-2" />
          Add Rule
        </button>
      </div>

      {/* Rules List */}
      <div className="space-y-4">
        {rules.map((rule) => (
          <div
            key={rule.id}
            className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700 p-6"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-2 mb-2">
                  <Zap className="h-5 w-5 text-primary-500" />
                  <span className="text-lg font-semibold text-gray-900 dark:text-white capitalize">
                    {rule.intent}
                  </span>
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    Priority: {rule.priority}
                  </span>
                </div>
                <div className="mb-2">
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Keywords:
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {rule.keywords.map((keyword, idx) => (
                      <span
                        key={idx}
                        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Response:
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {rule.response}
                  </p>
                </div>
              </div>
              <div className="flex space-x-2 ml-4">
                <button
                  onClick={() => setEditingId(rule.id)}
                  className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <Edit className="h-5 w-5" />
                </button>
                <button
                  onClick={() => handleDelete(rule.id)}
                  className="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400"
                >
                  <Trash2 className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {rules.length === 0 && (
        <div className="bg-white dark:bg-gray-800 shadow rounded-lg border border-gray-200 dark:border-gray-700 p-12 text-center">
          <Zap className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500 dark:text-gray-400">
            No rules configured. Add your first rule to get started.
          </p>
        </div>
      )}
    </div>
  );
}



