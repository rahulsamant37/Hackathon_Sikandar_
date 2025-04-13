'use client';

import React, { useEffect, useState } from 'react';
import DashboardLayout from '@/components/layout/DashboardLayout';
import CourseList from '@/components/features/courses/CourseList';
import { coursesApi } from '@/lib/api';

interface Course {
  id: string;
  title: string;
  description: string;
  instructorName: string;
  progress?: number;
  enrolled?: boolean;
}

export default function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [enrolledCourses, setEnrolledCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        setLoading(true);

        // In a real app, you would fetch this data from the API
        // For now, we'll use mock data

        // Mock all courses
        const mockCourses = [
          {
            id: "course1",
            title: "Introduction to AI",
            description: "Learn the basics of artificial intelligence and machine learning.",
            instructorName: "Dr. Jane Smith",
            enrolled: true,
            progress: 75
          },
          {
            id: "course2",
            title: "Machine Learning Fundamentals",
            description: "Understand the core concepts and algorithms of machine learning.",
            instructorName: "Prof. John Davis",
            enrolled: true,
            progress: 30
          },
          {
            id: "course3",
            title: "Deep Learning with Python",
            description: "Master deep learning techniques using Python and popular frameworks.",
            instructorName: "Dr. Michael Johnson",
            enrolled: true,
            progress: 10
          },
          {
            id: "course4",
            title: "Natural Language Processing",
            description: "Explore techniques for processing and analyzing human language data.",
            instructorName: "Dr. Sarah Williams",
            enrolled: false
          },
          {
            id: "course5",
            title: "Computer Vision",
            description: "Learn how to make computers understand and interpret visual information.",
            instructorName: "Prof. Robert Brown",
            enrolled: false
          },
          {
            id: "course6",
            title: "Reinforcement Learning",
            description: "Understand how agents learn to make decisions through trial and error.",
            instructorName: "Dr. Emily Chen",
            enrolled: false
          }
        ];

        // Filter enrolled courses
        const enrolled = mockCourses.filter(course => course.enrolled);
        const available = mockCourses.filter(course => !course.enrolled);

        setEnrolledCourses(enrolled);
        setCourses(available);
      } catch (err) {
        console.error('Error fetching courses:', err);
        setError('Failed to load courses. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex justify-center items-center min-h-[60vh]">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="text-center py-10">
          <h2 className="text-2xl font-bold text-gray-900">Error</h2>
          <p className="mt-2 text-gray-600">{error}</p>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h1 className="text-2xl font-bold text-gray-800">Courses</h1>
          <p className="text-gray-600 mt-1">Explore our courses and continue your learning journey.</p>
        </div>

        {enrolledCourses.length > 0 && (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-800">My Courses</h2>
            </div>
            <div className="p-6">
              <CourseList initialCourses={enrolledCourses} showEnrolled={true} />
            </div>
          </div>
        )}

        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-800">Available Courses</h2>
          </div>
          <div className="p-6">
            <CourseList initialCourses={courses} />
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
