'use client';

import React, { useEffect, useState } from 'react';
import MainLayout from '@/components/layout/MainLayout';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { authApi, analyticsApi } from '@/lib/api';

interface UserProfile {
  id: string;
  username: string;
  email: string;
  role: string;
  learningPreferences: any;
}

interface Achievement {
  id: string;
  title: string;
  description: string;
  awardedAt: string;
  icon: string;
}

interface CourseProgress {
  courseId: string;
  title: string;
  progress: number;
}

export default function ProfilePage() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [courseProgress, setCourseProgress] = useState<CourseProgress[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        setLoading(true);
        
        // In a real app, you would fetch this data from the API
        // For now, we'll use mock data
        
        // Mock user profile
        const mockProfile = {
          id: "user123",
          username: "johndoe",
          email: "john.doe@example.com",
          role: "student",
          learningPreferences: {
            primary_style: "visual",
            secondary_style: "reading",
            pace_preference: "moderate",
            content_preferences: {
              videos: 8,
              text: 7,
              interactive: 6,
              quizzes: 5
            }
          }
        };
        
        // Mock achievements
        const mockAchievements = [
          {
            id: "ach1",
            title: "First Course Completed",
            description: "Completed your first course",
            awardedAt: "2023-10-15T14:30:00Z",
            icon: "🏆"
          },
          {
            id: "ach2",
            title: "Perfect Quiz Score",
            description: "Scored 100% on a quiz",
            awardedAt: "2023-11-02T09:15:00Z",
            icon: "🎯"
          },
          {
            id: "ach3",
            title: "Learning Streak",
            description: "Completed content for 7 consecutive days",
            awardedAt: "2023-11-10T18:45:00Z",
            icon: "🔥"
          }
        ];
        
        // Mock course progress
        const mockCourseProgress = [
          {
            courseId: "course1",
            title: "Introduction to AI",
            progress: 75
          },
          {
            courseId: "course2",
            title: "Machine Learning Fundamentals",
            progress: 30
          },
          {
            courseId: "course3",
            title: "Deep Learning with Python",
            progress: 10
          }
        ];
        
        setProfile(mockProfile);
        setAchievements(mockAchievements);
        setCourseProgress(mockCourseProgress);
      } catch (err) {
        console.error('Error fetching profile data:', err);
        setError('Failed to load profile data. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchProfileData();
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
  
  if (error || !profile) {
    return (
      <MainLayout>
        <div className="text-center py-10">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Error</h2>
          <p className="mt-2 text-gray-600 dark:text-gray-400">{error || 'Profile not found'}</p>
        </div>
      </MainLayout>
    );
  }
  
  return (
    <MainLayout>
      <div className="space-y-8">
        <div className="flex flex-col md:flex-row gap-8">
          {/* Profile Information */}
          <div className="md:w-1/3">
            <Card>
              <CardHeader>
                <CardTitle>Profile Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex justify-center mb-6">
                  <div className="h-24 w-24 rounded-full bg-primary-200 flex items-center justify-center text-primary-800 text-3xl font-semibold">
                    {profile.username.charAt(0).toUpperCase()}
                  </div>
                </div>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Username</label>
                  <Input value={profile.username} readOnly />
                </div>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Email</label>
                  <Input value={profile.email} readOnly />
                </div>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Role</label>
                  <Input value={profile.role.charAt(0).toUpperCase() + profile.role.slice(1)} readOnly />
                </div>
                
                <Button className="w-full">Edit Profile</Button>
              </CardContent>
            </Card>
          </div>
          
          {/* Learning Preferences */}
          <div className="md:w-2/3">
            <Card>
              <CardHeader>
                <CardTitle>Learning Preferences</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  <div>
                    <h3 className="text-lg font-medium mb-2">Learning Style</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-primary-50 dark:bg-gray-700 p-4 rounded-lg">
                        <p className="text-sm text-gray-500 dark:text-gray-400">Primary Style</p>
                        <p className="text-lg font-medium capitalize">{profile.learningPreferences.primary_style}</p>
                      </div>
                      <div className="bg-primary-50 dark:bg-gray-700 p-4 rounded-lg">
                        <p className="text-sm text-gray-500 dark:text-gray-400">Secondary Style</p>
                        <p className="text-lg font-medium capitalize">{profile.learningPreferences.secondary_style}</p>
                      </div>
                      <div className="bg-primary-50 dark:bg-gray-700 p-4 rounded-lg">
                        <p className="text-sm text-gray-500 dark:text-gray-400">Pace Preference</p>
                        <p className="text-lg font-medium capitalize">{profile.learningPreferences.pace_preference}</p>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="text-lg font-medium mb-2">Content Preferences</h3>
                    <div className="space-y-3">
                      {Object.entries(profile.learningPreferences.content_preferences).map(([key, value]) => (
                        <div key={key} className="space-y-1">
                          <div className="flex justify-between">
                            <span className="capitalize">{key}</span>
                            <span>{value}/10</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                            <div
                              className="bg-primary-600 h-2.5 rounded-full"
                              style={{ width: `${(Number(value) / 10) * 100}%` }}
                            ></div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
        
        {/* Course Progress */}
        <Card>
          <CardHeader>
            <CardTitle>Course Progress</CardTitle>
          </CardHeader>
          <CardContent>
            {courseProgress.length === 0 ? (
              <p className="text-gray-600 dark:text-gray-400">You haven't enrolled in any courses yet.</p>
            ) : (
              <div className="space-y-6">
                {courseProgress.map((course) => (
                  <div key={course.courseId} className="space-y-2">
                    <div className="flex justify-between">
                      <span className="font-medium">{course.title}</span>
                      <span>{course.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                      <div
                        className="bg-primary-600 h-2.5 rounded-full"
                        style={{ width: `${course.progress}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
        
        {/* Achievements */}
        <Card>
          <CardHeader>
            <CardTitle>Achievements</CardTitle>
          </CardHeader>
          <CardContent>
            {achievements.length === 0 ? (
              <p className="text-gray-600 dark:text-gray-400">You haven't earned any achievements yet.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {achievements.map((achievement) => (
                  <div key={achievement.id} className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4 flex items-start">
                    <div className="text-3xl mr-4">{achievement.icon}</div>
                    <div>
                      <h3 className="font-medium">{achievement.title}</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">{achievement.description}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                        Awarded on {new Date(achievement.awardedAt).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  );
}
