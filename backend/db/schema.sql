-- Schema for AI Learning Platform

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('student', 'instructor', 'admin')),
    learning_preferences JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- Courses Table
CREATE TABLE IF NOT EXISTS courses (
    course_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT,
    instructor_id UUID NOT NULL REFERENCES users(user_id),
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Modules Table
CREATE TABLE IF NOT EXISTS modules (
    module_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    sequence_number INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Content Items Table
CREATE TABLE IF NOT EXISTS content_items (
    content_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    module_id UUID NOT NULL REFERENCES modules(module_id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('video', 'text', 'quiz', 'interactive')),
    content JSONB NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Quizzes Table
CREATE TABLE IF NOT EXISTS quizzes (
    quiz_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id UUID NOT NULL REFERENCES content_items(content_id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    time_limit INTEGER, -- in seconds
    passing_score INTEGER NOT NULL DEFAULT 70, -- percentage
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Questions Table
CREATE TABLE IF NOT EXISTS questions (
    question_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    quiz_id UUID NOT NULL REFERENCES quizzes(quiz_id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('multiple-choice', 'true-false', 'fill-in-blank', 'matching')),
    options JSONB NOT NULL,
    correct_answer JSONB NOT NULL,
    points INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enrollments Table
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    course_id UUID NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'completed')),
    UNIQUE(user_id, course_id)
);

-- User Progress Table
CREATE TABLE IF NOT EXISTS user_progress (
    progress_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    content_id UUID NOT NULL REFERENCES content_items(content_id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed')),
    completion_percentage INTEGER NOT NULL DEFAULT 0 CHECK (completion_percentage BETWEEN 0 AND 100),
    time_spent INTEGER, -- in seconds
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, content_id)
);

-- Quiz Submissions Table
CREATE TABLE IF NOT EXISTS quiz_submissions (
    submission_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    quiz_id UUID NOT NULL REFERENCES quizzes(quiz_id) ON DELETE CASCADE,
    score FLOAT NOT NULL CHECK (score BETWEEN 0 AND 100),
    answers JSONB NOT NULL,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    time_taken INTEGER NOT NULL -- in seconds
);

-- Content Views Table (for analytics)
CREATE TABLE IF NOT EXISTS content_views (
    view_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    content_id UUID NOT NULL REFERENCES content_items(content_id) ON DELETE CASCADE,
    course_id UUID NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    viewed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    device_info JSONB DEFAULT '{}'::jsonb
);

-- Achievements Table
CREATE TABLE IF NOT EXISTS achievements (
    achievement_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    criteria JSONB NOT NULL,
    icon TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User Achievements Table
CREATE TABLE IF NOT EXISTS user_achievements (
    user_achievement_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    achievement_id UUID NOT NULL REFERENCES achievements(achievement_id) ON DELETE CASCADE,
    awarded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, achievement_id)
);

-- AI Recommendations Table
CREATE TABLE IF NOT EXISTS ai_recommendations (
    recommendation_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    content_id UUID NOT NULL REFERENCES content_items(content_id) ON DELETE CASCADE,
    recommendation_type TEXT NOT NULL,
    reasoning TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'dismissed', 'completed'))
);

-- Learning Paths Table
CREATE TABLE IF NOT EXISTS learning_paths (
    path_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    course_id UUID NOT NULL REFERENCES courses(course_id) ON DELETE CASCADE,
    path_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(user_id, course_id)
);

-- Row Level Security Policies

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE modules ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE quizzes ENABLE ROW LEVEL SECURITY;
ALTER TABLE questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE enrollments ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_views ENABLE ROW LEVEL SECURITY;
ALTER TABLE achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_paths ENABLE ROW LEVEL SECURITY;

-- Users Policies
CREATE POLICY users_select ON users
    FOR SELECT USING (true); -- Everyone can see users

CREATE POLICY users_insert ON users
    FOR INSERT WITH CHECK (auth.uid() = user_id::text); -- Only the user can insert themselves

CREATE POLICY users_update ON users
    FOR UPDATE USING (auth.uid() = user_id::text); -- Only the user can update themselves

-- Courses Policies
CREATE POLICY courses_select ON courses
    FOR SELECT USING (
        status = 'published' OR -- Anyone can see published courses
        auth.uid() = instructor_id::text OR -- Instructors can see their own courses
        auth.role() = 'admin' -- Admins can see all courses
    );

CREATE POLICY courses_insert ON courses
    FOR INSERT WITH CHECK (
        auth.uid() = instructor_id::text OR -- Instructors can create courses
        auth.role() = 'admin' -- Admins can create courses
    );

CREATE POLICY courses_update ON courses
    FOR UPDATE USING (
        auth.uid() = instructor_id::text OR -- Instructors can update their own courses
        auth.role() = 'admin' -- Admins can update any course
    );

-- Modules Policies
CREATE POLICY modules_select ON modules
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM courses
            WHERE courses.course_id = modules.course_id
            AND (
                courses.status = 'published' OR -- Anyone can see modules in published courses
                auth.uid() = courses.instructor_id::text OR -- Instructors can see their own modules
                auth.role() = 'admin' -- Admins can see all modules
            )
        )
    );

CREATE POLICY modules_insert ON modules
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM courses
            WHERE courses.course_id = modules.course_id
            AND (
                auth.uid() = courses.instructor_id::text OR -- Instructors can create modules in their courses
                auth.role() = 'admin' -- Admins can create modules in any course
            )
        )
    );

CREATE POLICY modules_update ON modules
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM courses
            WHERE courses.course_id = modules.course_id
            AND (
                auth.uid() = courses.instructor_id::text OR -- Instructors can update their own modules
                auth.role() = 'admin' -- Admins can update any module
            )
        )
    );

-- Similar policies for other tables...

-- Create indexes for performance
CREATE INDEX idx_courses_instructor ON courses(instructor_id);
CREATE INDEX idx_modules_course ON modules(course_id);
CREATE INDEX idx_content_module ON content_items(module_id);
CREATE INDEX idx_quizzes_content ON quizzes(content_id);
CREATE INDEX idx_questions_quiz ON questions(quiz_id);
CREATE INDEX idx_enrollments_user ON enrollments(user_id);
CREATE INDEX idx_enrollments_course ON enrollments(course_id);
CREATE INDEX idx_progress_user ON user_progress(user_id);
CREATE INDEX idx_progress_content ON user_progress(content_id);
CREATE INDEX idx_submissions_user ON quiz_submissions(user_id);
CREATE INDEX idx_submissions_quiz ON quiz_submissions(quiz_id);
CREATE INDEX idx_views_user ON content_views(user_id);
CREATE INDEX idx_views_content ON content_views(content_id);
CREATE INDEX idx_user_achievements_user ON user_achievements(user_id);
CREATE INDEX idx_recommendations_user ON ai_recommendations(user_id);
CREATE INDEX idx_learning_paths_user ON learning_paths(user_id);
CREATE INDEX idx_learning_paths_course ON learning_paths(course_id);
