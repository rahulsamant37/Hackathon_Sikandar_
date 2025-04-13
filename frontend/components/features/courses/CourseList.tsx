'use client';

import React, { useState, useEffect } from 'react';
import CourseCard from './CourseCard';
import { Input } from '@/components/ui/Input';

interface Course {
  id: string;
  title: string;
  description: string;
  instructorName: string;
  progress?: number;
  enrolled?: boolean;
}

interface CourseListProps {
  initialCourses: Course[];
  showEnrolled?: boolean;
}

const CourseList: React.FC<CourseListProps> = ({
  initialCourses,
  showEnrolled = false
}) => {
  const [courses, setCourses] = useState<Course[]>(initialCourses);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    if (searchTerm.trim() === '') {
      setCourses(initialCourses);
      return;
    }

    const filtered = initialCourses.filter(
      course =>
        course.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        course.description.toLowerCase().includes(searchTerm.toLowerCase())
    );

    setCourses(filtered);
  }, [searchTerm, initialCourses]);

  return (
    <div className="space-y-6">
      <div className="flex items-center">
        <Input
          type="search"
          placeholder="Search courses..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="max-w-md"
        />
      </div>

      {courses.length === 0 ? (
        <div className="text-center py-10">
          <h3 className="text-lg font-medium text-gray-900">No courses found</h3>
          <p className="mt-1 text-sm text-gray-500">
            {showEnrolled
              ? "You haven't enrolled in any courses yet."
              : "No courses match your search criteria."}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {courses.map((course) => (
            <CourseCard
              key={course.id}
              id={course.id}
              title={course.title}
              description={course.description}
              instructorName={course.instructorName}
              progress={course.progress}
              enrolled={course.enrolled}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default CourseList;
