'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import MainLayout from '@/components/layout/MainLayout';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { analyticsApi, coursesApi } from '@/lib/api';

interface ModuleAnalytics {
  moduleId: string;
  title: string;
  completionRate: number;
  averageQuizScore: number;
}

interface StrugglingStudent {
  userId: string;
  username: string;
  email: string;
  progress: number;
  lastActive: string;
}

interface CourseDetails {
  id: string;
  title: string;
  description: string;
  status: string;
  totalStudents: number;
  averageCompletion: number;
  modules: ModuleAnalytics[];
  strugglingStudents: StrugglingStudent[];
}

export default function CourseAnalyticsPage() {
  const params = useParams();
  const courseId = params.courseId as string;
  
  const [courseDetails, setCourseDetails] = useState<CourseDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const fetchCourseAnalytics = async () => {
      try {
        setLoading(true);
        
        // In a real app, you would fetch this data from the API
        // For now, we'll use mock data
        
        // Mock course details with analytics
        const mockCourseDetails = {
          id: courseId,
          title: "Introduction to AI",
          description: "Learn the basics of artificial intelligence and machine learning.",
          status: "published",
          totalStudents: 45,
          averageCompletion: 68,
          modules: [
            {
              moduleId: "module1",
              title: "What is AI?",
              completionRate: 85,
              averageQuizScore: 78
            },
            {
              moduleId: "module2",
              title: "Machine Learning Basics",
              completionRate: 72,
              averageQuizScore: 65
            },
            {
              moduleId: "module3",
              title: "Neural Networks",
              completionRate: 58,
              averageQuizScore: 62
            },
            {
              moduleId: "module4",
              title: "Deep Learning",
              completionRate: 42,
              averageQuizScore: 58
            }
          ],
          strugglingStudents: [
            {
              userId: "user1",
              username: "johndoe",
              email: "john.doe@example.com",
              progress: 25,
              lastActive: "2023-11-10T14:30:00Z"
            },
            {
              userId: "user2",
              username: "janedoe",
              email: "jane.doe@example.com",
              progress: 18,
              lastActive: "2023-11-08T09:15:00Z"
            },
            {
              userId: "user3",
              username: "bobsmith",
              email: "bob.smith@example.com",
              progress: 12,
              lastActive: "2023-11-05T16:45:00Z"
            }
          ]
        };
        
        setCourseDetails(mockCourseDetails);
      } catch (err) {
        console.error('Error fetching course analytics:', err);
        setError('Failed to load course analytics. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    
    if (courseId) {
      fetchCourseAnalytics();
    }
  }, [courseId]);
  
  if (loading) {
    return (
      <MainLayout>
        <div className="flex justify-center items-center min-h-[60vh]">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
        </div>
      </MainLayout>
    );
  }
  
  if (error || !courseDetails) {
    return (
      <MainLayout>
        <div className="text-center py-10">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Error</h2>
          <p className="mt-2 text-gray-600 dark:text-gray-400">{error || 'Course not found'}</p>
          <Link href="/instructor/dashboard" className="mt-4 inline-block">
            <Button variant="secondary">Back to Dashboard</Button>
          </Link>
        </div>
      </MainLayout>
    );
  }
  
  return (
    <MainLayout>
      <div className="space-y-8">
        <div className="flex justify-between items-start">
          <div>
            <Link href="/instructor/dashboard" className="text-primary-600 hover:text-primary-800 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
              </svg>
              Back to Dashboard
            </Link>
            <h1 className="text-3xl font-bold mt-2">{courseDetails.title}</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">{courseDetails.description}</p>
          </div>
          
          <div className="flex space-x-3">
            <Link href={`/instructor/courses/${courseId}/edit`}>
              <Button variant="secondary">Edit Course</Button>
            </Link>
            <Link href={`/instructor/courses/${courseId}/modules/create`}>
              <Button>Add Module</Button>
            </Link>
          </div>
        </div>
        
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardContent className="p-6">
              <div className="flex flex-col items-center">
                <div className="text-4xl font-bold text-primary-600">{courseDetails.totalStudents}</div>
                <div className="text-gray-500 dark:text-gray-400 mt-2">Enrolled Students</div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex flex-col items-center">
                <div className="text-4xl font-bold text-primary-600">{courseDetails.averageCompletion}%</div>
                <div className="text-gray-500 dark:text-gray-400 mt-2">Average Completion</div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex flex-col items-center">
                <div className="text-4xl font-bold text-primary-600">{courseDetails.modules.length}</div>
                <div className="text-gray-500 dark:text-gray-400 mt-2">Total Modules</div>
              </div>
            </CardContent>
          </Card>
        </div>
        
        {/* Module Analytics */}
        <Card>
          <CardHeader>
            <CardTitle>Module Analytics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                  <tr>
                    <th scope="col" className="px-6 py-3">Module</th>
                    <th scope="col" className="px-6 py-3">Completion Rate</th>
                    <th scope="col" className="px-6 py-3">Avg. Quiz Score</th>
                    <th scope="col" className="px-6 py-3">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {courseDetails.modules.map((module) => (
                    <tr key={module.moduleId} className="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                      <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">
                        {module.title}
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center">
                          <div className="w-full bg-gray-200 rounded-full h-2.5 mr-2 dark:bg-gray-700">
                            <div
                              className="bg-primary-600 h-2.5 rounded-full"
                              style={{ width: `${module.completionRate}%` }}
                            ></div>
                          </div>
                          <span>{module.completionRate}%</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center">
                          <div className="w-full bg-gray-200 rounded-full h-2.5 mr-2 dark:bg-gray-700">
                            <div
                              className={`h-2.5 rounded-full ${
                                module.averageQuizScore < 60 
                                  ? 'bg-red-600' 
                                  : module.averageQuizScore < 80 
                                    ? 'bg-yellow-400' 
                                    : 'bg-green-600'
                              }`}
                              style={{ width: `${module.averageQuizScore}%` }}
                            ></div>
                          </div>
                          <span>{module.averageQuizScore}%</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <Link href={`/instructor/courses/${courseId}/modules/${module.moduleId}`}>
                          <Button variant="secondary" size="sm">View Details</Button>
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
        
        {/* Struggling Students */}
        <Card>
          <CardHeader>
            <CardTitle>Struggling Students</CardTitle>
          </CardHeader>
          <CardContent>
            {courseDetails.strugglingStudents.length === 0 ? (
              <p className="text-gray-600 dark:text-gray-400">No struggling students identified.</p>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm text-left">
                  <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                    <tr>
                      <th scope="col" className="px-6 py-3">Student</th>
                      <th scope="col" className="px-6 py-3">Email</th>
                      <th scope="col" className="px-6 py-3">Progress</th>
                      <th scope="col" className="px-6 py-3">Last Active</th>
                      <th scope="col" className="px-6 py-3">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {courseDetails.strugglingStudents.map((student) => (
                      <tr key={student.userId} className="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                        <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">
                          {student.username}
                        </td>
                        <td className="px-6 py-4">{student.email}</td>
                        <td className="px-6 py-4">
                          <div className="flex items-center">
                            <div className="w-full bg-gray-200 rounded-full h-2.5 mr-2 dark:bg-gray-700">
                              <div
                                className="bg-red-600 h-2.5 rounded-full"
                                style={{ width: `${student.progress}%` }}
                              ></div>
                            </div>
                            <span>{student.progress}%</span>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          {new Date(student.lastActive).toLocaleDateString()}
                        </td>
                        <td className="px-6 py-4">
                          <Button variant="secondary" size="sm">Contact</Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>
        
        {/* AI Insights */}
        <Card>
          <CardHeader>
            <CardTitle>AI Insights</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="p-4 bg-primary-50 border border-primary-200 rounded-lg dark:bg-gray-800 dark:border-gray-700">
                <h3 className="text-lg font-medium text-primary-800 dark:text-primary-400 mb-2">Content Effectiveness</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  The "Neural Networks" module has a significantly lower completion rate (58%) compared to earlier modules. 
                  Consider reviewing the content complexity and adding more interactive elements to improve engagement.
                </p>
              </div>
              
              <div className="p-4 bg-primary-50 border border-primary-200 rounded-lg dark:bg-gray-800 dark:border-gray-700">
                <h3 className="text-lg font-medium text-primary-800 dark:text-primary-400 mb-2">Student Engagement</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  There's a drop-off in student engagement after the second module. 
                  Consider adding a mid-course assessment or interactive project to boost motivation and re-engage students.
                </p>
              </div>
              
              <div className="p-4 bg-primary-50 border border-primary-200 rounded-lg dark:bg-gray-800 dark:border-gray-700">
                <h3 className="text-lg font-medium text-primary-800 dark:text-primary-400 mb-2">Quiz Performance</h3>
                <p className="text-gray-700 dark:text-gray-300">
                  Students are scoring lower on quizzes in later modules. 
                  This may indicate that the difficulty curve is too steep. 
                  Consider adding more preparatory content or practice exercises before quizzes.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  );
}
