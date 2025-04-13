'use client';

import React from 'react';
import Link from 'next/link';
import DashboardLayout from '@/components/layout/DashboardLayout';
import {
  BookOpen,
  Clock,
  Award,
  TrendingUp,
  Calendar,
  ArrowRight
} from '@/components/ui/Icons';

export default function Dashboard() {
  // Mock data for the dashboard
  const stats = [
    { name: 'Courses Enrolled', value: '8', icon: BookOpen, color: 'bg-blue-100 text-blue-600' },
    { name: 'Hours Learned', value: '42', icon: Clock, color: 'bg-green-100 text-green-600' },
    { name: 'Achievements', value: '12', icon: Award, color: 'bg-purple-100 text-purple-600' },
    { name: 'Current Streak', value: '5 days', icon: TrendingUp, color: 'bg-orange-100 text-orange-600' },
  ];

  const inProgressCourses = [
    { id: 1, title: 'Introduction to AI', progress: 75, lastAccessed: '2 days ago' },
    { id: 2, title: 'Machine Learning Fundamentals', progress: 45, lastAccessed: '1 week ago' },
    { id: 3, title: 'Deep Learning with Python', progress: 20, lastAccessed: 'Yesterday' },
  ];

  const upcomingDeadlines = [
    { id: 1, title: 'AI Concepts Quiz', course: 'Introduction to AI', dueDate: 'Tomorrow' },
    { id: 2, title: 'Final Project', course: 'Machine Learning Fundamentals', dueDate: 'Next week' },
  ];

  const recommendations = [
    { id: 1, title: 'Natural Language Processing', description: 'Based on your interest in AI and Machine Learning' },
    { id: 2, title: 'Computer Vision', description: 'Popular among students with similar learning paths' },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Welcome section */}
        <div className="bg-white rounded-lg shadow p-6">
          <h1 className="text-2xl font-bold text-gray-800">Welcome back, John!</h1>
          <p className="text-gray-600 mt-1">Here's what's happening with your learning journey today.</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat) => (
            <div key={stat.name} className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className={`flex-shrink-0 rounded-md p-3 ${stat.color}`}>
                    <stat.icon className="h-6 w-6" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">{stat.name}</dt>
                      <dd>
                        <div className="text-lg font-medium text-gray-900">{stat.value}</div>
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Main content */}
        <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">
          {/* In Progress Courses */}
          <div className="bg-white overflow-hidden shadow rounded-lg lg:col-span-2">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">In Progress Courses</h3>
            </div>
            <div className="px-4 py-5 sm:p-6">
              <div className="space-y-4">
                {inProgressCourses.map((course) => (
                  <div key={course.id} className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="text-md font-medium text-gray-900">{course.title}</h4>
                        <p className="text-sm text-gray-500">Last accessed {course.lastAccessed}</p>
                      </div>
                      <Link
                        href={`/courses/${course.id}`}
                        className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 bg-primary-600 text-white hover:bg-primary-700 h-9 px-3"
                      >
                        Continue
                      </Link>
                    </div>
                    <div className="mt-4">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-gray-500">Progress</span>
                        <span className="font-medium">{course.progress}%</span>
                      </div>
                      <div className="mt-1 w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full"
                          style={{ width: `${course.progress}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-6">
                <Link
                  href="/courses"
                  className="inline-flex w-full items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 py-2 px-4"
                >
                  View all courses
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </div>
            </div>
          </div>

          {/* Right column */}
          <div className="space-y-5">
            {/* Upcoming Deadlines */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
                <h3 className="text-lg leading-6 font-medium text-gray-900">Upcoming Deadlines</h3>
              </div>
              <div className="px-4 py-5 sm:p-6">
                {upcomingDeadlines.length > 0 ? (
                  <ul className="divide-y divide-gray-200">
                    {upcomingDeadlines.map((deadline) => (
                      <li key={deadline.id} className="py-3">
                        <div className="flex items-start">
                          <div className="flex-shrink-0">
                            <Calendar className="h-5 w-5 text-gray-400" />
                          </div>
                          <div className="ml-3">
                            <p className="text-sm font-medium text-gray-900">{deadline.title}</p>
                            <p className="text-sm text-gray-500">{deadline.course}</p>
                            <p className="text-sm text-red-500">Due: {deadline.dueDate}</p>
                          </div>
                        </div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-gray-500">No upcoming deadlines</p>
                )}
              </div>
            </div>

            {/* Recommendations */}
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
                <h3 className="text-lg leading-6 font-medium text-gray-900">Recommended for You</h3>
              </div>
              <div className="px-4 py-5 sm:p-6">
                <ul className="divide-y divide-gray-200">
                  {recommendations.map((recommendation) => (
                    <li key={recommendation.id} className="py-3">
                      <div className="flex items-start">
                        <div className="flex-shrink-0">
                          <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
                            <BookOpen className="h-4 w-4 text-primary-600" />
                          </div>
                        </div>
                        <div className="ml-3">
                          <p className="text-sm font-medium text-gray-900">{recommendation.title}</p>
                          <p className="text-sm text-gray-500">{recommendation.description}</p>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
                <div className="mt-4">
                  <Link
                    href="/recommendations"
                    className="inline-flex items-center text-primary-600 hover:text-primary-700 text-sm font-medium"
                  >
                    View all recommendations
                    <ArrowRight className="ml-1 h-4 w-4" />
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
