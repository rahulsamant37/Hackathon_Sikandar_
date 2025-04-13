'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';

interface ProgressData {
  moduleId: string;
  moduleName: string;
  progress: number;
  quizScore?: number;
}

interface StudentProgressChartProps {
  data: ProgressData[];
  title?: string;
  showQuizScores?: boolean;
}

const StudentProgressChart: React.FC<StudentProgressChartProps> = ({
  data,
  title = 'Course Progress',
  showQuizScores = true
}) => {
  // Calculate overall progress
  const overallProgress = data.length > 0
    ? Math.round(data.reduce((sum, item) => sum + item.progress, 0) / data.length)
    : 0;
  
  // Calculate average quiz score if available
  const quizScores = data.filter(item => item.quizScore !== undefined).map(item => item.quizScore as number);
  const averageQuizScore = quizScores.length > 0
    ? Math.round(quizScores.reduce((sum, score) => sum + score, 0) / quizScores.length)
    : undefined;
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Overall Progress */}
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="font-medium">Overall Progress</span>
              <span>{overallProgress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-4 dark:bg-gray-700">
              <div
                className={`h-4 rounded-full ${
                  overallProgress < 30 
                    ? 'bg-red-600' 
                    : overallProgress < 70 
                      ? 'bg-yellow-400' 
                      : 'bg-green-600'
                }`}
                style={{ width: `${overallProgress}%` }}
              ></div>
            </div>
          </div>
          
          {/* Average Quiz Score */}
          {showQuizScores && averageQuizScore !== undefined && (
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="font-medium">Average Quiz Score</span>
                <span>{averageQuizScore}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-4 dark:bg-gray-700">
                <div
                  className={`h-4 rounded-full ${
                    averageQuizScore < 60 
                      ? 'bg-red-600' 
                      : averageQuizScore < 80 
                        ? 'bg-yellow-400' 
                        : 'bg-green-600'
                  }`}
                  style={{ width: `${averageQuizScore}%` }}
                ></div>
              </div>
            </div>
          )}
          
          {/* Module Progress */}
          <div className="space-y-4 mt-6">
            <h3 className="text-lg font-medium">Module Progress</h3>
            {data.map((item) => (
              <div key={item.moduleId} className="space-y-2">
                <div className="flex justify-between">
                  <span>{item.moduleName}</span>
                  <span>{item.progress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                  <div
                    className="bg-primary-600 h-2.5 rounded-full"
                    style={{ width: `${item.progress}%` }}
                  ></div>
                </div>
                
                {/* Quiz Score for this module if available */}
                {showQuizScores && item.quizScore !== undefined && (
                  <div className="flex justify-between text-sm text-gray-500 dark:text-gray-400">
                    <span>Quiz Score</span>
                    <span>{item.quizScore}%</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default StudentProgressChart;
