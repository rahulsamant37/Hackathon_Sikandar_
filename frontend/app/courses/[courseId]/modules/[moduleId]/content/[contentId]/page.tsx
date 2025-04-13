'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import MainLayout from '@/components/layout/MainLayout';
import { Button } from '@/components/ui/Button';
import { Card, CardContent } from '@/components/ui/Card';
import { coursesApi } from '@/lib/api';

interface ContentItem {
  content_id: string;
  title: string;
  type: string;
  content: any;
  completed?: boolean;
}

export default function ContentViewerPage() {
  const params = useParams();
  const router = useRouter();
  const courseId = params.courseId as string;
  const moduleId = params.moduleId as string;
  const contentId = params.contentId as string;
  
  const [contentItem, setContentItem] = useState<ContentItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [completed, setCompleted] = useState(false);
  
  useEffect(() => {
    const fetchContent = async () => {
      try {
        setLoading(true);
        // In a real app, you would fetch the content data from the API
        // For now, we'll use mock data based on the content type
        let mockContent;
        
        if (contentId === 'content1') {
          mockContent = {
            content_id: contentId,
            title: "What is AI?",
            type: "video",
            content: {
              videoUrl: "https://www.youtube.com/embed/mJeNghZXtMo",
              duration: "10:30",
              transcript: "In this video, we explore the fundamentals of artificial intelligence..."
            },
            completed: false
          };
        } else if (contentId === 'content2') {
          mockContent = {
            content_id: contentId,
            title: "Machine Learning Fundamentals",
            type: "text",
            content: {
              text: `
                <h2>Introduction to Machine Learning</h2>
                <p>Machine learning is a subset of artificial intelligence that focuses on developing systems that can learn from and make decisions based on data.</p>
                <h3>Key Concepts</h3>
                <ul>
                  <li>Supervised Learning</li>
                  <li>Unsupervised Learning</li>
                  <li>Reinforcement Learning</li>
                </ul>
                <p>In supervised learning, algorithms are trained using labeled examples, where the desired output is known...</p>
              `
            },
            completed: false
          };
        } else if (contentId === 'content3') {
          mockContent = {
            content_id: contentId,
            title: "Quiz: AI Basics",
            type: "quiz",
            content: {
              questions: [
                {
                  id: "q1",
                  text: "What does AI stand for?",
                  options: [
                    { id: "a", text: "Automated Intelligence" },
                    { id: "b", text: "Artificial Intelligence" },
                    { id: "c", text: "Advanced Integration" },
                    { id: "d", text: "Algorithmic Implementation" }
                  ],
                  correctAnswer: "b"
                },
                {
                  id: "q2",
                  text: "Which of the following is NOT a type of machine learning?",
                  options: [
                    { id: "a", text: "Supervised Learning" },
                    { id: "b", text: "Unsupervised Learning" },
                    { id: "c", text: "Reinforcement Learning" },
                    { id: "d", text: "Deterministic Learning" }
                  ],
                  correctAnswer: "d"
                }
              ]
            },
            completed: false
          };
        } else {
          throw new Error("Content not found");
        }
        
        setContentItem(mockContent);
        setCompleted(mockContent.completed || false);
      } catch (err) {
        console.error('Error fetching content:', err);
        setError('Failed to load content. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    
    if (courseId && moduleId && contentId) {
      fetchContent();
    }
  }, [courseId, moduleId, contentId]);
  
  const handleMarkComplete = async () => {
    try {
      // In a real app, you would call the API to mark the content as completed
      // await coursesApi.markContentComplete(contentId);
      setCompleted(true);
    } catch (err) {
      console.error('Error marking content as complete:', err);
      setError('Failed to mark content as complete. Please try again.');
    }
  };
  
  const renderContent = () => {
    if (!contentItem) return null;
    
    switch (contentItem.type) {
      case 'video':
        return (
          <div className="space-y-4">
            <div className="aspect-w-16 aspect-h-9">
              <iframe
                src={contentItem.content.videoUrl}
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                className="w-full h-[400px] rounded-lg"
              ></iframe>
            </div>
            <div className="mt-4">
              <h3 className="text-lg font-semibold">Transcript</h3>
              <p className="text-gray-700 dark:text-gray-300 mt-2">{contentItem.content.transcript}</p>
            </div>
          </div>
        );
      case 'text':
        return (
          <div className="prose prose-blue max-w-none dark:prose-invert" dangerouslySetInnerHTML={{ __html: contentItem.content.text }}></div>
        );
      case 'quiz':
        return (
          <div className="space-y-6">
            {contentItem.content.questions.map((question: any) => (
              <Card key={question.id} className="overflow-hidden">
                <CardContent className="p-6">
                  <h3 className="text-lg font-semibold mb-4">{question.text}</h3>
                  <div className="space-y-2">
                    {question.options.map((option: any) => (
                      <div key={option.id} className="flex items-center space-x-3 p-3 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700">
                        <input
                          type="radio"
                          id={`${question.id}-${option.id}`}
                          name={question.id}
                          value={option.id}
                          className="h-4 w-4 text-primary-600 focus:ring-primary-500"
                        />
                        <label htmlFor={`${question.id}-${option.id}`} className="flex-1 cursor-pointer">
                          {option.text}
                        </label>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
            <div className="flex justify-end">
              <Button>Submit Quiz</Button>
            </div>
          </div>
        );
      default:
        return <p>Unsupported content type</p>;
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
  
  if (error || !contentItem) {
    return (
      <MainLayout>
        <div className="text-center py-10">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Error</h2>
          <p className="mt-2 text-gray-600 dark:text-gray-400">{error || 'Content not found'}</p>
          <Link href={`/courses/${courseId}/modules/${moduleId}`} className="mt-4 inline-block">
            <Button variant="secondary">Back to Module</Button>
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
            <Link href={`/courses/${courseId}/modules/${moduleId}`} className="text-primary-600 hover:text-primary-800 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
              </svg>
              Back to Module
            </Link>
            <h1 className="text-3xl font-bold mt-2">{contentItem.title}</h1>
          </div>
          
          {!completed ? (
            <Button onClick={handleMarkComplete}>Mark as Complete</Button>
          ) : (
            <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Completed
            </div>
          )}
        </div>
        
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          {renderContent()}
        </div>
      </div>
    </MainLayout>
  );
}
