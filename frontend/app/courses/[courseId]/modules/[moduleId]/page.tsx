'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import MainLayout from '@/components/layout/MainLayout';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { coursesApi } from '@/lib/api';

interface ContentItem {
  content_id: string;
  title: string;
  type: string;
  completed?: boolean;
}

interface Module {
  module_id: string;
  title: string;
  description: string;
  content: ContentItem[];
}

export default function ModuleDetailPage() {
  const params = useParams();
  const router = useRouter();
  const courseId = params.courseId as string;
  const moduleId = params.moduleId as string;
  
  const [module, setModule] = useState<Module | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const fetchModule = async () => {
      try {
        setLoading(true);
        // In a real app, you would fetch the module data from the API
        const moduleData = {
          module_id: moduleId,
          title: "Introduction to AI",
          description: "Learn the basics of artificial intelligence and machine learning.",
          content: [
            {
              content_id: "content1",
              title: "What is AI?",
              type: "video",
              completed: true
            },
            {
              content_id: "content2",
              title: "Machine Learning Fundamentals",
              type: "text",
              completed: false
            },
            {
              content_id: "content3",
              title: "Quiz: AI Basics",
              type: "quiz",
              completed: false
            }
          ]
        };
        
        setModule(moduleData);
      } catch (err) {
        console.error('Error fetching module:', err);
        setError('Failed to load module details. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    
    if (courseId && moduleId) {
      fetchModule();
    }
  }, [courseId, moduleId]);
  
  const handleContentClick = (contentId: string, contentType: string) => {
    router.push(`/courses/${courseId}/modules/${moduleId}/content/${contentId}`);
  };
  
  const getContentIcon = (type: string) => {
    switch (type) {
      case 'video':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-primary-600" viewBox="0 0 20 20" fill="currentColor">
            <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z" />
          </svg>
        );
      case 'text':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-primary-600" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
          </svg>
        );
      case 'quiz':
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-primary-600" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
          </svg>
        );
      default:
        return (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-primary-600" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clipRule="evenodd" />
          </svg>
        );
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
  
  if (error || !module) {
    return (
      <MainLayout>
        <div className="text-center py-10">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Error</h2>
          <p className="mt-2 text-gray-600 dark:text-gray-400">{error || 'Module not found'}</p>
          <Link href={`/courses/${courseId}`} className="mt-4 inline-block">
            <Button variant="secondary">Back to Course</Button>
          </Link>
        </div>
      </MainLayout>
    );
  }
  
  return (
    <MainLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <Link href={`/courses/${courseId}`} className="text-primary-600 hover:text-primary-800 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
              </svg>
              Back to Course
            </Link>
            <h1 className="text-3xl font-bold mt-2">{module.title}</h1>
          </div>
        </div>
        
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Module Overview</h2>
          <p className="text-gray-700 dark:text-gray-300">{module.description}</p>
        </div>
        
        <div className="space-y-4">
          <h2 className="text-2xl font-semibold">Module Content</h2>
          
          {module.content.length === 0 ? (
            <p className="text-gray-600 dark:text-gray-400">No content available yet.</p>
          ) : (
            <div className="space-y-4">
              {module.content.map((item) => (
                <Card 
                  key={item.content_id}
                  className={`cursor-pointer transition-colors hover:bg-gray-50 dark:hover:bg-gray-700 ${
                    item.completed ? 'border-l-4 border-green-500' : ''
                  }`}
                  onClick={() => handleContentClick(item.content_id, item.type)}
                >
                  <CardContent className="p-4">
                    <div className="flex items-center">
                      <div className="mr-4">
                        {getContentIcon(item.type)}
                      </div>
                      <div className="flex-1">
                        <h3 className="font-medium">{item.title}</h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400 capitalize">{item.type}</p>
                      </div>
                      {item.completed && (
                        <div className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full">
                          Completed
                        </div>
                      )}
                    </div>
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
