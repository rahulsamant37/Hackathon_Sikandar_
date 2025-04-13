import React, { ReactNode, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  Home,
  BookOpen,
  BarChart2,
  Settings,
  Bell,
  Search,
  Menu,
  X,
  LogOut,
  User,
  Lightbulb,
  Award,
  MessageSquare
} from '@/components/ui/Icons';

import { Button } from '@/components/ui/Button';

interface DashboardLayoutProps {
  children: ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const router = useRouter();

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const handleLogout = async () => {
    // Implement logout logic here
    router.push('/auth/login');
  };

  const navItems = [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'My Courses', href: '/courses', icon: BookOpen },
    { name: 'Learning Paths', href: '/learning-paths', icon: Lightbulb },
    { name: 'Achievements', href: '/achievements', icon: Award },
    { name: 'Analytics', href: '/analytics', icon: BarChart2 },
    { name: 'Messages', href: '/messages', icon: MessageSquare },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black bg-opacity-50 lg:hidden"
          onClick={toggleSidebar}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 z-30 w-64 transform bg-white shadow-lg transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex h-full flex-col">
          {/* Sidebar header */}
          <div className="flex items-center justify-between px-4 py-5 border-b">
            <Link href="/dashboard" className="flex items-center">
              <div className="h-8 w-8 rounded-full bg-primary-600 flex items-center justify-center text-white font-bold mr-2">
                AI
              </div>
              <span className="text-xl font-semibold text-gray-800">LearnAI</span>
            </Link>
            <button
              className="p-1 rounded-md lg:hidden hover:bg-gray-100"
              onClick={toggleSidebar}
            >
              <X size={24} />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto py-4 px-3">
            <ul className="space-y-1">
              {navItems.map((item) => (
                <li key={item.name}>
                  <Link
                    href={item.href}
                    className="flex items-center px-3 py-2 text-gray-700 rounded-md hover:bg-primary-50 hover:text-primary-600 group"
                  >
                    <item.icon className="h-5 w-5 mr-3 text-gray-500 group-hover:text-primary-600" />
                    <span>{item.name}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </nav>

          {/* User profile */}
          <div className="border-t p-4">
            <div className="flex items-center">
              <div className="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center">
                <User className="h-6 w-6 text-gray-500" />
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-700">John Doe</p>
                <p className="text-xs text-gray-500">john.doe@example.com</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="mt-4 flex w-full items-center px-3 py-2 text-sm text-gray-700 rounded-md hover:bg-red-50 hover:text-red-600"
            >
              <LogOut className="h-4 w-4 mr-2" />
              <span>Log out</span>
            </button>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Top navigation */}
        <header className="bg-white shadow-sm z-10">
          <div className="px-4 sm:px-6 lg:px-8">
            <div className="flex h-16 items-center justify-between">
              {/* Left section */}
              <div className="flex items-center">
                <button
                  className="p-2 rounded-md text-gray-500 lg:hidden"
                  onClick={toggleSidebar}
                >
                  <Menu size={24} />
                </button>
              </div>

              {/* Search */}
              <div className="flex-1 max-w-md mx-auto">
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Search className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    type="text"
                    className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                    placeholder="Search courses, modules..."
                  />
                </div>
              </div>

              {/* Right section */}
              <div className="flex items-center">
                <button className="p-1 ml-3 rounded-full text-gray-500 hover:text-gray-700 focus:outline-none">
                  <Bell className="h-6 w-6" />
                </button>
              </div>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto bg-gray-50 p-4 sm:p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
