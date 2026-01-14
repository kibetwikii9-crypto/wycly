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

  // Map pathname to category and page name
  const getPageBreadcrumb = (path: string): { category: string; page: string } => {
    if (path === '/dashboard') return { category: '', page: 'Dashboard' };
    
    // Remove /dashboard prefix and split by /
    const parts = path.replace('/dashboard', '').split('/').filter(Boolean);
    
    if (parts.length === 0) return { category: '', page: 'Dashboard' };
    
    // Category mapping
    const categoryMap: { [key: string]: string } = {
      'crm': 'Customers & CRM',
      'leads': 'Customers & CRM',
      'conversations': 'Communication',
      'messages': 'Communication',
      'email-templates': 'Communication',
      'sales-products': 'Sales & Inventory',
      'sales': 'Sales & Inventory',
      'products': 'Sales & Inventory',
      'inventory': 'Sales & Inventory',
      'orders': 'Sales & Inventory',
      'purchasing': 'Sales & Inventory',
      'suppliers': 'Sales & Inventory',
      'finance': 'Finance',
      'invoices': 'Finance',
      'expenses': 'Finance',
      'payments': 'Finance',
      'reports': 'Finance',
      'taxes': 'Finance',
      'projects': 'Projects & Tasks',
      'tasks': 'Projects & Tasks',
      'analytics': 'Analytics & Reports',
      'financial': 'Analytics & Reports',
      'performance': 'Analytics & Reports',
      'handoff': 'Operations',
      'automation': 'Operations',
      'knowledge': 'Operations',
      'ai-rules': 'Operations',
      'hr': 'HR & Employees',
      'employees': 'HR & Employees',
      'departments': 'HR & Employees',
      'attendance': 'HR & Employees',
      'leave': 'HR & Employees',
      'documents': 'HR & Employees',
      'users': 'Settings',
      'integrations': 'Settings',
      'security': 'Settings',
      'settings': 'Settings',
      'notifications': 'Settings',
      'onboarding': 'Settings',
      'ads': 'Settings',
    };
    
    // Page name mapping
    const pageMap: { [key: string]: string } = {
      'contacts': 'Contacts',
      'pipeline': 'Pipeline',
      'leads': 'Leads',
      'conversations': 'Conversations',
      'messages': 'Internal Messages',
      'email-templates': 'Email Templates',
      'sales-products': 'Products',
      'products': 'Products',
      'inventory': 'Inventory',
      'orders': 'Orders',
      'suppliers': 'Suppliers',
      'invoices': 'Invoices',
      'expenses': 'Expenses',
      'payments': 'Payments',
      'reports': 'Financial Reports',
      'taxes': 'Taxes',
      'projects': 'Projects',
      'tasks': 'Tasks',
      'analytics': 'Sales Analytics',
      'financial': 'Financial Analytics',
      'handoff': 'Handoff',
      'automation': 'Automation',
      'knowledge': 'Knowledge Base',
      'ai-rules': 'AI Rules',
      'employees': 'Employees',
      'departments': 'Departments',
      'attendance': 'Attendance',
      'leave': 'Leave Requests',
      'documents': 'Employee Documents',
      'users': 'Users & Roles',
      'integrations': 'Integrations',
      'security': 'Security',
      'settings': 'General',
      'notifications': 'Notifications',
      'onboarding': 'Onboarding',
      'ads': 'Ad Studio',
    };
    
    // Handle nested paths
    if (parts.length >= 2) {
      const parent = parts[parts.length - 2];
      const child = parts[parts.length - 1];
      
      // HR performance reviews
      if (parent === 'hr' && child === 'performance') {
        return { category: 'HR & Employees', page: 'Performance Reviews' };
      }
      // Analytics performance
      if (parent === 'analytics' && child === 'performance') {
        return { category: 'Analytics & Reports', page: 'Performance Analytics' };
      }
      
      // Get category from parent, page from child
      const category = categoryMap[parent] || categoryMap[child] || '';
      const page = pageMap[child] || child.split('-').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
      ).join(' ');
      return { category, page };
    }
    
    // Single level path
    const lastPart = parts[parts.length - 1];
    const category = categoryMap[lastPart] || '';
    const page = pageMap[lastPart] || lastPart.split('-').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
    
    return { category, page };
  };

  const { category, page } = getPageBreadcrumb(pathname);

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center space-x-2">
          {category ? (
            <>
              <span className="text-xs font-medium text-gray-500 dark:text-gray-400">
                {category}
              </span>
              <span className="text-xs text-gray-400 dark:text-gray-500">›</span>
              <span className="text-xs font-semibold text-gray-900 dark:text-white">
                {page}
              </span>
            </>
          ) : (
            <span className="text-xs font-semibold text-gray-900 dark:text-white">
              {page}
            </span>
          )}
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



