'use client';

import { useAuth } from '@/lib/auth';
import { usePathname } from 'next/navigation';
import { LogOut, Moon, Sun } from 'lucide-react';
import { useState, useEffect } from 'react';

export default function Header() {
  const { user, logout } = useAuth();
  const pathname = usePathname();
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    const isDark = document.documentElement.classList.contains('dark');
    setDarkMode(isDark);
  }, []);

  const toggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    if (newDarkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  };

  // Map pathname to readable page name
  const getPageName = (path: string): string => {
    if (path === '/dashboard') return 'Dashboard';
    
    // Remove /dashboard prefix and split by /
    const parts = path.replace('/dashboard', '').split('/').filter(Boolean);
    
    if (parts.length === 0) return 'Dashboard';
    
    // Map common routes - handle nested paths
    const routeMap: { [key: string]: string } = {
      'crm': 'CRM',
      'contacts': 'Contacts',
      'pipeline': 'Sales Pipeline',
      'leads': 'Leads',
      'conversations': 'Conversations',
      'messages': 'Internal Messages',
      'email-templates': 'Email Templates',
      'sales-products': 'Products',
      'sales': 'Sales',
      'products': 'Products',
      'inventory': 'Inventory',
      'orders': 'Orders',
      'purchasing': 'Purchasing',
      'suppliers': 'Suppliers',
      'finance': 'Finance',
      'invoices': 'Invoices',
      'expenses': 'Expenses',
      'payments': 'Payments',
      'reports': 'Financial Reports',
      'taxes': 'Taxes',
      'projects': 'Projects',
      'tasks': 'Tasks',
      'analytics': 'Analytics',
      'financial': 'Financial Analytics',
      'handoff': 'Handoff',
      'automation': 'Automation',
      'knowledge': 'Knowledge Base',
      'ai-rules': 'AI Rules',
      'hr': 'HR & Employees',
      'employees': 'Employees',
      'departments': 'Departments',
      'attendance': 'Attendance',
      'leave': 'Leave Requests',
      'documents': 'Employee Documents',
      'users': 'Users & Roles',
      'integrations': 'Integrations',
      'security': 'Security',
      'settings': 'Settings',
      'notifications': 'Notifications',
      'onboarding': 'Onboarding',
      'ads': 'Ad Studio',
    };
    
    // Handle nested paths (e.g., /dashboard/hr/performance vs /dashboard/analytics/performance)
    if (parts.length >= 2) {
      const parent = parts[parts.length - 2];
      const child = parts[parts.length - 1];
      
      // HR performance reviews
      if (parent === 'hr' && child === 'performance') {
        return 'Performance Reviews';
      }
      // Analytics performance
      if (parent === 'analytics' && child === 'performance') {
        return 'Performance Analytics';
      }
    }
    
    // Get the last part of the path
    const lastPart = parts[parts.length - 1];
    return routeMap[lastPart] || lastPart.split('-').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  const pageName = getPageName(pathname);

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center space-x-4">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            {pageName}
          </h1>
        </div>
        <div className="flex items-center space-x-4">
          <button
            onClick={toggleDarkMode}
            className="p-2 rounded-md text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </button>
          <div className="flex items-center space-x-3">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900 dark:text-white">
                {user?.full_name || user?.email}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400 capitalize">
                {user?.role}
              </p>
            </div>
            <button
              onClick={logout}
              className="p-2 rounded-md text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
              title="Logout"
            >
              <LogOut className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}



