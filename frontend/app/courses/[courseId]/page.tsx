'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import MainLayout from '@/components/layout/MainLayout';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { coursesApi } from '@/lib/api';

interface Module {
  module_id: string;
  title: string;
  description: string;
  sequence_number: number;
}

interface Course {
  id: string;
  title: string;
  description: string;
  instructor_id: string;
  instructorName: string;
  modules: Module[];
}

export default function CourseDetailPage() {
  const params = useParams();
  const courseId = params.courseId as string;
  
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [enrolled, setEnrolled] = useState(false);
  
  useEffect(() => {
    const fetchCourse = async () => {
      try {
        setLoading(true);
        const courseData = await coursesApi.getCourse(courseId);
        
        // Fetch modules for this course
        const modulesData = await coursesApi.getCourseModules(courseId);
        
        // Fetch instructor details
        // In a real app, you would fetch the instructor's name from the API
        const instructorName = "John Doe"; // Placeholder
        
        setCourse({
          ...courseData,
          instructorName,
          modules: modulesData || []
        });
        
        // Check if user is enrolled
        // In a real app, you would check this from the API
        setEnrolled(false); // Placeholder
      } catch (err) {
        console.error('Error fetching course:', err);
        setError('Failed to load course details. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    
    if (courseId) {
      fetchCourse();
    }
  }, [courseId]);
  
  const handleEnroll = async () => {
    try {
      await coursesApi.enrollCourse(courseId);
      setEnrolled(true);
    } catch (err) {
      console.error('Error enrolling in course:', err);
      setError('Failed to enroll in course. Please try again.');
    }
  };
  
  if (loading) {
    return (
      <MainLayout>
        <div className="flex justify-center items-center min-h-[60vh]">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
        </div>
      </MainLayout>
    );
  }
  
  if (error || !course) {
    return (
      <MainLayout>
        <div className="text-center py-10">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Error</h2>
          <p className="mt-2 text-gray-600 dark:text-gray-400">{error || 'Course not found'}</p>
          <Link href="/courses" className="mt-4 inline-block">
            <Button variant="secondary">Back to Courses</Button>
          </Link>
        </div>
      </MainLayout>
    );
  }
  
  return (
    <MainLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold">{course.title}</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2">Instructor: {course.instructorName}</p>
          </div>
          
          {!enrolled ? (
            <Button onClick={handleEnroll}>Enroll in Course</Button>
          ) : (
            <Button variant="secondary" disabled>Enrolled</Button>
          )}
        </div>
        
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">About this Course</h2>
          <p className="text-gray-700 dark:text-gray-300">{course.description}</p>
        </div>
        
        <div className="space-y-4">
          <h2 className="text-2xl font-semibold">Course Content</h2>
          
          {course.modules.length === 0 ? (
            <p className="text-gray-600 dark:text-gray-400">No modules available yet.</p>
          ) : (
            <div className="space-y-4">
              {course.modules.map((module) => (
                <Card key={module.module_id}>
                  <CardHeader>
                    <CardTitle>{module.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600 dark:text-gray-400 mb-4">{module.description}</p>
                    <Link href={`/courses/${courseId}/modules/${module.module_id}`}>
                      <Button variant="secondary">View Module</Button>
                    </Link>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  );
}
