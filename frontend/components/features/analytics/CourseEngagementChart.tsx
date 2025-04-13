'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';

interface EngagementData {
  date: string;
  activeStudents: number;
  contentViews: number;
  quizSubmissions: number;
}

interface CourseEngagementChartProps {
  data: EngagementData[];
  title?: string;
  totalStudents: number;
}

const CourseEngagementChart: React.FC<CourseEngagementChartProps> = ({
  data,
  title = 'Course Engagement',
  totalStudents
}) => {
  // Format dates for display
  const formattedData = data.map(item => ({
    ...item,
    formattedDate: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }));
  
  // Calculate average engagement metrics
  const avgActiveStudents = Math.round(
    data.reduce((sum, item) => sum + item.activeStudents, 0) / data.length
  );
  
  const avgContentViews = Math.round(
    data.reduce((sum, item) => sum + item.contentViews, 0) / data.length
  );
  
  const avgQuizSubmissions = Math.round(
    data.reduce((sum, item) => sum + item.quizSubmissions, 0) / data.length
  );
  
  // Calculate engagement rate
  const engagementRate = Math.round((avgActiveStudents / totalStudents) * 100);
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Engagement Summary */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-primary-50 p-4 rounded-lg dark:bg-gray-800">
              <div className="text-sm text-gray-500 dark:text-gray-400">Engagement Rate</div>
              <div className="text-2xl font-bold">{engagementRate}%</div>
              <div className="text-xs text-gray-500 dark:text-gray-400">
                {avgActiveStudents} of {totalStudents} students active
              </div>
            </div>
            
            <div className="bg-primary-50 p-4 rounded-lg dark:bg-gray-800">
              <div className="text-sm text-gray-500 dark:text-gray-400">Avg. Content Views</div>
              <div className="text-2xl font-bold">{avgContentViews}</div>
              <div className="text-xs text-gray-500 dark:text-gray-400">
                per day
              </div>
            </div>
            
            <div className="bg-primary-50 p-4 rounded-lg dark:bg-gray-800">
              <div className="text-sm text-gray-500 dark:text-gray-400">Avg. Quiz Submissions</div>
              <div className="text-2xl font-bold">{avgQuizSubmissions}</div>
              <div className="text-xs text-gray-500 dark:text-gray-400">
                per day
              </div>
            </div>
          </div>
          
          {/* Engagement Chart */}
          <div className="mt-6">
            <h3 className="text-lg font-medium mb-4">Daily Engagement</h3>
            
            {/* Chart Header */}
            <div className="grid grid-cols-4 text-xs text-gray-500 dark:text-gray-400 mb-2">
              <div>Date</div>
              <div>Active Students</div>
              <div>Content Views</div>
              <div>Quiz Submissions</div>
            </div>
            
            {/* Chart Rows */}
            <div className="space-y-3">
              {formattedData.map((item, index) => (
                <div key={index} className="grid grid-cols-4 items-center">
                  <div className="text-sm">{item.formattedDate}</div>
                  
                  <div>
                    <div className="flex items-center">
                      <div className="w-full bg-gray-200 rounded-full h-2.5 mr-2 dark:bg-gray-700">
                        <div
                          className="bg-blue-600 h-2.5 rounded-full"
                          style={{ width: `${(item.activeStudents / totalStudents) * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-xs">{item.activeStudents}</span>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex items-center">
                      <div className="w-full bg-gray-200 rounded-full h-2.5 mr-2 dark:bg-gray-700">
                        <div
                          className="bg-green-600 h-2.5 rounded-full"
                          style={{ width: `${(item.contentViews / (avgContentViews * 2)) * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-xs">{item.contentViews}</span>
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex items-center">
                      <div className="w-full bg-gray-200 rounded-full h-2.5 mr-2 dark:bg-gray-700">
                        <div
                          className="bg-purple-600 h-2.5 rounded-full"
                          style={{ width: `${(item.quizSubmissions / (avgQuizSubmissions * 2)) * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-xs">{item.quizSubmissions}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          {/* Insights */}
          <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg dark:bg-gray-800 dark:border-gray-700">
            <h3 className="text-lg font-medium text-yellow-800 dark:text-yellow-400 mb-2">Insights</h3>
            <p className="text-gray-700 dark:text-gray-300">
              Student engagement is highest on weekdays, with a notable drop during weekends.
              Quiz submissions tend to peak at the end of modules, suggesting students are completing content in sequence.
              Consider adding more interactive elements to increase engagement throughout the course.
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default CourseEngagementChart;
