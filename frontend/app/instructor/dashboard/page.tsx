'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import MainLayout from '@/components/layout/MainLayout';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { analyticsApi, coursesApi } from '@/lib/api';

interface CourseAnalytics {
  courseId: string;
  title: string;
  totalStudents: number;
  averageCompletion: number;
  strugglingStudents: number;
}

interface StudentAnalytics {
  userId: string;
  username: string;
  email: string;
  enrolledCourses: number;
  averageProgress: number;
  lastActive: string;
}

export default function InstructorDashboardPage() {
  const [courseAnalytics, setCourseAnalytics] = useState<CourseAnalytics[]>([]);
  const [studentAnalytics, setStudentAnalytics] = useState<StudentAnalytics[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        
        // In a real app, you would fetch this data from the API
        // For now, we'll use mock data
        
        // Mock course analytics
        const mockCourseAnalytics = [
          {
            courseId: "course1",
            title: "Introduction to AI",
            totalStudents: 45,
            averageCompletion: 68,
            strugglingStudents: 7
          },
          {
            courseId: "course2",
            title: "Machine Learning Fundamentals",
            totalStudents: 32,
            averageCompletion: 42,
            strugglingStudents: 12
          },
          {
            courseId: "course3",
            title: "Deep Learning with Python",
            totalStudents: 28,
            averageCompletion: 35,
            strugglingStudents: 9
          }
        ];
        
        // Mock student analytics
        const mockStudentAnalytics = [
          {
            userId: "user1",
            username: "johndoe",
            email: "john.doe@example.com",
            enrolledCourses: 2,
            averageProgress: 75,
            lastActive: "2023-11-15T14:30:00Z"
          },
          {
            userId: "user2",
            username: "janedoe",
            email: "jane.doe@example.com",
            enrolledCourses: 3,
            averageProgress: 42,
            lastActive: "2023-11-14T09:15:00Z"
          },
          {
            userId: "user3",
            username: "bobsmith",
            email: "bob.smith@example.com",
            enrolledCourses: 1,
            averageProgress: 28,
            lastActive: "2023-11-10T16:45:00Z"
          },
          {
            userId: "user4",
            username: "alicejones",
            email: "alice.jones@example.com",
            enrolledCourses: 2,
            averageProgress: 92,
            lastActive: "2023-11-15T11:20:00Z"
          },
          {
            userId: "user5",
            username: "charliegreen",
            email: "charlie.green@example.com",
            enrolledCourses: 3,
            averageProgress: 15,
            lastActive: "2023-11-08T13:10:00Z"
          }
        ];
        
        setCourseAnalytics(mockCourseAnalytics);
        setStudentAnalytics(mockStudentAnalytics);
      } catch (err) {
        console.error('Error fetching analytics:', err);
        setError('Failed to load analytics data. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchAnalytics();
  }, []);
  
  if (loading) {
    return (
      <MainLayout>
        <div className="flex justify-center items-center min-h-[60vh]">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
        </div>
      </MainLayout>
    );
  }
  
  if (error) {
    return (
      <MainLayout>
        <div className="text-center py-10">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Error</h2>
          <p className="mt-2 text-gray-600 dark:text-gray-400">{error}</p>
        </div>
      </MainLayout>
    );
  }
  
  return (
    <MainLayout>
      <div className="space-y-8">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Instructor Dashboard</h1>
          <Link href="/instructor/courses/create">
            <Button>Create New Course</Button>
          </Link>
        </div>
        
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardContent className="p-6">
              <div className="flex flex-col items-center">
                <div className="text-4xl font-bold text-primary-600">{courseAnalytics.length}</div>
                <div className="text-gray-500 dark:text-gray-400 mt-2">Active Courses</div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex flex-col items-center">
                <div className="text-4xl font-bold text-primary-600">
                  {courseAnalytics.reduce((sum, course) => sum + course.totalStudents, 0)}
                </div>
                <div className="text-gray-500 dark:text-gray-400 mt-2">Total Students</div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex flex-col items-center">
                <div className="text-4xl font-bold text-primary-600">
                  {courseAnalytics.reduce((sum, course) => sum + course.strugglingStudents, 0)}
                </div>
                <div className="text-gray-500 dark:text-gray-400 mt-2">Struggling Students</div>
              </div>
            </CardContent>
          </Card>
        </div>
        
        {/* Course Analytics */}
        <Card>
          <CardHeader>
            <CardTitle>Course Analytics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                  <tr>
                    <th scope="col" className="px-6 py-3">Course</th>
                    <th scope="col" className="px-6 py-3">Students</th>
                    <th scope="col" className="px-6 py-3">Avg. Completion</th>
                    <th scope="col" className="px-6 py-3">Struggling Students</th>
                    <th scope="col" className="px-6 py-3">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {courseAnalytics.map((course) => (
                    <tr key={course.courseId} className="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                      <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">
                        {course.title}
                      </td>
                      <td className="px-6 py-4">{course.totalStudents}</td>
                      <td className="px-6 py-4">
                        <div className="flex items-center">
                          <div className="w-full bg-gray-200 rounded-full h-2.5 mr-2 dark:bg-gray-700">
                            <div
                              className="bg-primary-600 h-2.5 rounded-full"
                              style={{ width: `${course.averageCompletion}%` }}
                            ></div>
                          </div>
                          <span>{course.averageCompletion}%</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <span className="bg-red-100 text-red-800 text-xs font-medium px-2.5 py-0.5 rounded dark:bg-red-900 dark:text-red-300">
                          {course.strugglingStudents}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <Link href={`/instructor/courses/${course.courseId}`}>
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
        
        {/* Student Analytics */}
        <Card>
          <CardHeader>
            <CardTitle>Student Analytics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                  <tr>
                    <th scope="col" className="px-6 py-3">Student</th>
                    <th scope="col" className="px-6 py-3">Email</th>
                    <th scope="col" className="px-6 py-3">Enrolled Courses</th>
                    <th scope="col" className="px-6 py-3">Avg. Progress</th>
                    <th scope="col" className="px-6 py-3">Last Active</th>
                    <th scope="col" className="px-6 py-3">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {studentAnalytics.map((student) => (
                    <tr key={student.userId} className="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                      <td className="px-6 py-4 font-medium text-gray-900 dark:text-white">
                        {student.username}
                      </td>
                      <td className="px-6 py-4">{student.email}</td>
                      <td className="px-6 py-4">{student.enrolledCourses}</td>
                      <td className="px-6 py-4">
                        <div className="flex items-center">
                          <div className="w-full bg-gray-200 rounded-full h-2.5 mr-2 dark:bg-gray-700">
                            <div
                              className={`h-2.5 rounded-full ${
                                student.averageProgress < 30 
                                  ? 'bg-red-600' 
                                  : student.averageProgress < 70 
                                    ? 'bg-yellow-400' 
                                    : 'bg-green-600'
                              }`}
                              style={{ width: `${student.averageProgress}%` }}
                            ></div>
                          </div>
                          <span>{student.averageProgress}%</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        {new Date(student.lastActive).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4">
                        <Link href={`/instructor/students/${student.userId}`}>
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
      </div>
    </MainLayout>
  );
}
