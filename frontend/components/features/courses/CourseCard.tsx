import React from 'react';
import Link from 'next/link';
import { Card, CardContent, CardFooter, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Clock, User, BookOpen } from '@/components/ui/Icons';

interface CourseCardProps {
  id: string;
  title: string;
  description: string;
  instructorName: string;
  progress?: number;
  enrolled?: boolean;
}

const CourseCard: React.FC<CourseCardProps> = ({
  id,
  title,
  description,
  instructorName,
  progress,
  enrolled = false,
}) => {
  return (
    <Card className="overflow-hidden hover:shadow-lg transition-shadow duration-300 h-full flex flex-col">
      <div className="h-40 bg-gradient-to-r from-primary-600 to-primary-400 relative">
        <div className="absolute inset-0 bg-black bg-opacity-20"></div>
        <div className="absolute bottom-4 left-4 right-4">
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-white bg-opacity-90 text-primary-800">
            <BookOpen className="w-3 h-3 mr-1" />
            {enrolled ? 'Enrolled' : 'Available'}
          </span>
        </div>
      </div>

      <CardHeader className="pb-2">
        <div className="flex justify-between items-start">
          <CardTitle className="text-lg">{title}</CardTitle>
        </div>
        <CardDescription className="flex items-center mt-1">
          <User className="w-3 h-3 mr-1" /> {instructorName}
        </CardDescription>
      </CardHeader>

      <CardContent className="flex-grow">
        <p className="text-sm text-gray-600 line-clamp-3">
          {description}
        </p>

        {enrolled && progress !== undefined && (
          <div className="mt-4">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-600 font-medium flex items-center">
                <Clock className="w-3 h-3 mr-1" /> Progress
              </span>
              <span className="font-semibold text-primary-700">{progress}%</span>
            </div>
            <div className="w-full bg-gray-100 rounded-full h-2">
              <div
                className={`h-2 rounded-full ${progress < 30 ? 'bg-orange-500' : progress < 70 ? 'bg-yellow-500' : 'bg-green-500'}`}
                style={{ width: `${progress}%` }}
              ></div>
            </div>
          </div>
        )}
      </CardContent>

      <CardFooter className="pt-4 border-t border-gray-100">
        {enrolled ? (
          <Link href={`/courses/${id}`} className="w-full">
            <Button variant="default" className="w-full group">
              Continue Learning
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-4 w-4 ml-2 transition-transform duration-200 group-hover:translate-x-1"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M14 5l7 7m0 0l-7 7m7-7H3"
                />
              </svg>
            </Button>
          </Link>
        ) : (
          <Link href={`/courses/${id}`} className="w-full">
            <Button variant="outline" className="w-full hover:bg-primary-50 border-primary-200 text-primary-700 hover:text-primary-800 group">
              View Course
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-4 w-4 ml-2 transition-transform duration-200 group-hover:translate-x-1"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M14 5l7 7m0 0l-7 7m7-7H3"
                />
              </svg>
            </Button>
          </Link>
        )}
      </CardFooter>
    </Card>
  );
};

export default CourseCard;
