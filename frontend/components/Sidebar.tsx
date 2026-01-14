'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  MessageSquare,
  BookOpen,
  Settings,
  BarChart3,
  Video,
  Zap,
  Plug,
  Users,
  UserCheck,
  TrendingUp,
  CreditCard,
  Shield,
  Bell,
  CheckCircle2,
  ShoppingBag,
  ChevronDown,
  ChevronRight,
  Users2,
  FileText,
  DollarSign,
  Receipt,
  TrendingDown,
  FolderKanban,
  CheckSquare,
  Mail,
  FileCode,
  Package,
  ShoppingCart,
  Truck,
  Wallet,
  PieChart,
  Activity,
  Workflow,
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface NavItem {
  name: string;
  href: string;
  icon: any;
  comingSoon?: boolean;
}

interface NavSection {
  name: string;
  icon: any;
  items: NavItem[];
  defaultOpen?: boolean;
}

const navigation: (NavItem | NavSection)[] = [
  // Dashboard - Single item
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  
  // Customers & CRM - Section
  {
    name: 'Customers & CRM',
    icon: Users2,
    defaultOpen: true,
    items: [
      { name: 'Contacts', href: '/dashboard/crm/contacts', icon: Users2 },
      { name: 'Leads', href: '/dashboard/leads', icon: TrendingUp },
      { name: 'Pipeline', href: '/dashboard/crm/pipeline', icon: TrendingUp },
    ],
  },
  
  // Communication - Section
  {
    name: 'Communication',
    icon: MessageSquare,
    defaultOpen: true,
    items: [
      { name: 'Conversations', href: '/dashboard/conversations', icon: MessageSquare },
      { name: 'Internal Messages', href: '/dashboard/messages', icon: Mail },
      { name: 'Email Templates', href: '/dashboard/email-templates', icon: FileCode },
    ],
  },
  
  // Sales & Inventory - Section
  {
    name: 'Sales & Inventory',
    icon: ShoppingBag,
    defaultOpen: true,
    items: [
      { name: 'Products', href: '/dashboard/sales-products', icon: Package },
      { name: 'Inventory', href: '/dashboard/inventory', icon: ShoppingBag },
      { name: 'Orders', href: '/dashboard/sales/orders', icon: ShoppingCart },
      { name: 'Suppliers', href: '/dashboard/purchasing/suppliers', icon: Truck },
    ],
  },
  
  // Finance - Section
  {
    name: 'Finance',
    icon: DollarSign,
    defaultOpen: false,
    items: [
      { name: 'Invoices', href: '/dashboard/finance/invoices', icon: FileText },
      { name: 'Expenses', href: '/dashboard/finance/expenses', icon: TrendingDown },
      { name: 'Payments', href: '/dashboard/finance/payments', icon: Wallet },
      { name: 'Reports', href: '/dashboard/finance/reports', icon: PieChart },
      { name: 'Taxes', href: '/dashboard/finance/taxes', icon: Receipt },
    ],
  },
  
  // Projects & Tasks - Section
  {
    name: 'Projects & Tasks',
    icon: FolderKanban,
    defaultOpen: false,
    items: [
      { name: 'Projects', href: '/dashboard/projects', icon: FolderKanban },
      { name: 'Tasks', href: '/dashboard/tasks', icon: CheckSquare },
    ],
  },
  
  // Analytics & Reports - Section
  {
    name: 'Analytics & Reports',
    icon: BarChart3,
    defaultOpen: false,
    items: [
      { name: 'Sales Analytics', href: '/dashboard/analytics', icon: TrendingUp },
      { name: 'Financial Analytics', href: '/dashboard/analytics/financial', icon: DollarSign },
      { name: 'Performance', href: '/dashboard/analytics/performance', icon: Activity },
    ],
  },
  
  // Operations - Section
  {
    name: 'Operations',
    icon: Zap,
    defaultOpen: false,
    items: [
      { name: 'Handoff', href: '/dashboard/handoff', icon: UserCheck },
      { name: 'Automation', href: '/dashboard/automation', icon: Workflow },
      { name: 'Knowledge Base', href: '/dashboard/knowledge', icon: BookOpen },
      { name: 'AI Rules', href: '/dashboard/ai-rules', icon: Zap },
    ],
  },
  
  // Settings - Section
  {
    name: 'Settings',
    icon: Settings,
    defaultOpen: false,
    items: [
      { name: 'General', href: '/dashboard/settings', icon: Settings },
      { name: 'Users & Roles', href: '/dashboard/users', icon: Users },
      { name: 'Integrations', href: '/dashboard/integrations', icon: Plug },
      { name: 'Security', href: '/dashboard/security', icon: Shield },
      { name: 'Notifications', href: '/dashboard/notifications', icon: Bell },
    ],
  },
];

export default function Sidebar() {
  const pathname = usePathname();
  const [openSections, setOpenSections] = useState<Set<string>>(
    new Set(navigation.filter((item): item is NavSection => 'items' in item && (item.defaultOpen === true)).map(item => item.name))
  );

  const toggleSection = (sectionName: string) => {
    setOpenSections((prev) => {
      const next = new Set(prev);
      if (next.has(sectionName)) {
        next.delete(sectionName);
      } else {
        next.add(sectionName);
      }
      return next;
    });
  };

  const isSectionOpen = (sectionName: string) => openSections.has(sectionName);
  const isPathActive = (href: string) => pathname === href || pathname.startsWith(href + '/');

  return (
    <div className="hidden md:flex md:flex-shrink-0">
      <div className="flex flex-col w-64">
        <div className="flex flex-col flex-grow pt-5 pb-4 overflow-y-auto bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
          <div className="flex items-center flex-shrink-0 px-4">
            <h1 className="text-xl font-bold text-[#007FFF]">
              Wycly
            </h1>
          </div>
          <div className="mt-5 flex-grow flex flex-col">
            <nav className="flex-1 px-2 space-y-1">
              {navigation.map((item) => {
                // Single item (not a section)
                if ('href' in item) {
                  const isActive = pathname === item.href;
                  return (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={cn(
                        'group flex items-center justify-between px-2 py-2 text-sm font-medium rounded-md',
                        isActive
                          ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
                          : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white'
                      )}
                    >
                      <div className="flex items-center">
                        <item.icon
                          className={cn(
                            'mr-3 flex-shrink-0 h-5 w-5',
                            isActive
                              ? 'text-primary-500'
                              : 'text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-300'
                          )}
                        />
                        {item.name}
                      </div>
                    </Link>
                  );
                }

                // Section with sub-items
                const section = item as NavSection;
                const isOpen = isSectionOpen(section.name);
                const hasActiveChild = section.items.some((subItem) => isPathActive(subItem.href));

                return (
                  <div key={section.name}>
                    <button
                      onClick={() => toggleSection(section.name)}
                      className={cn(
                        'w-full group flex items-center justify-between px-2 py-2 text-sm font-medium rounded-md',
                        hasActiveChild
                          ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
                          : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white'
                      )}
                    >
                      <div className="flex items-center">
                        <section.icon
                          className={cn(
                            'mr-3 flex-shrink-0 h-5 w-5',
                            hasActiveChild
                              ? 'text-primary-500'
                              : 'text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-300'
                          )}
                        />
                        {section.name}
                      </div>
                      {isOpen ? (
                        <ChevronDown className="h-4 w-4 text-gray-400" />
                      ) : (
                        <ChevronRight className="h-4 w-4 text-gray-400" />
                      )}
                    </button>
                    {isOpen && (
                      <div className="ml-4 mt-1 space-y-1">
                        {section.items.map((subItem) => {
                          const isActive = isPathActive(subItem.href);
                          return (
                            <Link
                              key={subItem.name}
                              href={subItem.href}
                              className={cn(
                                'group flex items-center justify-between px-2 py-2 text-sm font-medium rounded-md',
                                isActive
                                  ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
                                  : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white',
                                subItem.comingSoon && 'opacity-75'
                              )}
                            >
                              <div className="flex items-center">
                                <subItem.icon
                                  className={cn(
                                    'mr-3 flex-shrink-0 h-4 w-4',
                                    isActive
                                      ? 'text-primary-500'
                                      : 'text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-300'
                                  )}
                                />
                                {subItem.name}
                              </div>
                              {subItem.comingSoon && (
                                <span className="text-xs px-2 py-0.5 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 font-medium">
                                  Soon
                                </span>
                              )}
                            </Link>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              })}
            </nav>
          </div>
        </div>
      </div>
    </div>
  );
}



