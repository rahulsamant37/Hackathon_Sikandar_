-- Seed data for AI Learning Platform

-- Insert sample users
-- Note: In a real application, passwords would be properly hashed
INSERT INTO users (user_id, email, username, password_hash, role, learning_preferences, created_at)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'admin@example.com', 'admin', '$2b$12$K8Y6F9qGYhZeX4z3p1M3aO6mK5YfYBVcQYJvPXGbL5GjS9fDOXvAa', 'admin', '{}', NOW()),
    ('22222222-2222-2222-2222-222222222222', 'instructor1@example.com', 'instructor1', '$2b$12$K8Y6F9qGYhZeX4z3p1M3aO6mK5YfYBVcQYJvPXGbL5GjS9fDOXvAa', 'instructor', '{}', NOW()),
    ('33333333-3333-3333-3333-333333333333', 'instructor2@example.com', 'instructor2', '$2b$12$K8Y6F9qGYhZeX4z3p1M3aO6mK5YfYBVcQYJvPXGbL5GjS9fDOXvAa', 'instructor', '{}', NOW()),
    ('44444444-4444-4444-4444-444444444444', 'student1@example.com', 'student1', '$2b$12$K8Y6F9qGYhZeX4z3p1M3aO6mK5YfYBVcQYJvPXGbL5GjS9fDOXvAa', 'student', '{"primary_style": "visual", "secondary_style": "reading", "pace_preference": "moderate"}', NOW()),
    ('55555555-5555-5555-5555-555555555555', 'student2@example.com', 'student2', '$2b$12$K8Y6F9qGYhZeX4z3p1M3aO6mK5YfYBVcQYJvPXGbL5GjS9fDOXvAa', 'student', '{"primary_style": "auditory", "secondary_style": "kinesthetic", "pace_preference": "fast"}', NOW()),
    ('66666666-6666-6666-6666-666666666666', 'student3@example.com', 'student3', '$2b$12$K8Y6F9qGYhZeX4z3p1M3aO6mK5YfYBVcQYJvPXGbL5GjS9fDOXvAa', 'student', '{"primary_style": "reading", "secondary_style": "visual", "pace_preference": "slow"}', NOW());

-- Insert sample courses
INSERT INTO courses (course_id, title, description, instructor_id, status, created_at)
VALUES
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Introduction to AI', 'Learn the basics of artificial intelligence and machine learning.', '22222222-2222-2222-2222-222222222222', 'published', NOW()),
    ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'Machine Learning Fundamentals', 'Understand the core concepts and algorithms of machine learning.', '22222222-2222-2222-2222-222222222222', 'published', NOW()),
    ('cccccccc-cccc-cccc-cccc-cccccccccccc', 'Deep Learning with Python', 'Master deep learning techniques using Python and popular frameworks.', '33333333-3333-3333-3333-333333333333', 'published', NOW()),
    ('dddddddd-dddd-dddd-dddd-dddddddddddd', 'Natural Language Processing', 'Explore techniques for processing and analyzing human language data.', '33333333-3333-3333-3333-333333333333', 'draft', NOW());

-- Insert sample modules for Introduction to AI course
INSERT INTO modules (module_id, course_id, title, description, sequence_number, status, created_at)
VALUES
    ('11111111-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'What is AI?', 'Introduction to artificial intelligence concepts and history.', 1, 'published', NOW()),
    ('22222222-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Machine Learning Basics', 'Overview of machine learning approaches and applications.', 2, 'published', NOW()),
    ('33333333-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Neural Networks', 'Introduction to neural networks and deep learning.', 3, 'published', NOW()),
    ('44444444-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'AI Ethics', 'Ethical considerations in artificial intelligence.', 4, 'published', NOW());

-- Insert sample content items for the first module
INSERT INTO content_items (content_id, module_id, title, type, content, created_at)
VALUES
    ('content1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Introduction to AI', 'video', '{"videoUrl": "https://www.example.com/videos/intro-to-ai", "duration": 600, "transcript": "In this video, we explore the fundamentals of artificial intelligence..."}', NOW()),
    ('content2-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'History of AI', 'text', '{"text": "<h2>The History of Artificial Intelligence</h2><p>Artificial intelligence has a rich history dating back to the 1950s...</p>"}', NOW()),
    ('content3-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'AI Concepts Quiz', 'quiz', '{"instructions": "Test your understanding of basic AI concepts."}', NOW());

-- Insert a sample quiz
INSERT INTO quizzes (quiz_id, content_id, title, description, passing_score, created_at)
VALUES
    ('quiz1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'content3-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'AI Concepts Quiz', 'Test your understanding of basic AI concepts.', 70, NOW());

-- Insert sample questions for the quiz
INSERT INTO questions (question_id, quiz_id, text, type, options, correct_answer, created_at)
VALUES
    ('question1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'quiz1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'What does AI stand for?', 'multiple-choice', '[{"id": "a", "text": "Automated Intelligence"}, {"id": "b", "text": "Artificial Intelligence"}, {"id": "c", "text": "Advanced Integration"}, {"id": "d", "text": "Algorithmic Implementation"}]', '{"id": "b"}', NOW()),
    ('question2-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'quiz1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Which of the following is NOT a type of machine learning?', 'multiple-choice', '[{"id": "a", "text": "Supervised Learning"}, {"id": "b", "text": "Unsupervised Learning"}, {"id": "c", "text": "Reinforcement Learning"}, {"id": "d", "text": "Deterministic Learning"}]', '{"id": "d"}', NOW()),
    ('question3-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'quiz1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'True or False: Deep learning is a subset of machine learning.', 'true-false', '[{"id": "true", "text": "True"}, {"id": "false", "text": "False"}]', '{"id": "true"}', NOW());

-- Insert sample enrollments
INSERT INTO enrollments (enrollment_id, user_id, course_id, enrolled_at, status)
VALUES
    (uuid_generate_v4(), '44444444-4444-4444-4444-444444444444', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', NOW() - INTERVAL '30 days', 'active'),
    (uuid_generate_v4(), '44444444-4444-4444-4444-444444444444', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', NOW() - INTERVAL '20 days', 'active'),
    (uuid_generate_v4(), '55555555-5555-5555-5555-555555555555', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', NOW() - INTERVAL '25 days', 'active'),
    (uuid_generate_v4(), '55555555-5555-5555-5555-555555555555', 'cccccccc-cccc-cccc-cccc-cccccccccccc', NOW() - INTERVAL '15 days', 'active'),
    (uuid_generate_v4(), '66666666-6666-6666-6666-666666666666', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', NOW() - INTERVAL '10 days', 'active');

-- Insert sample user progress
INSERT INTO user_progress (progress_id, user_id, content_id, status, completion_percentage, last_accessed, created_at)
VALUES
    (uuid_generate_v4(), '44444444-4444-4444-4444-444444444444', 'content1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'completed', 100, NOW() - INTERVAL '25 days', NOW() - INTERVAL '28 days'),
    (uuid_generate_v4(), '44444444-4444-4444-4444-444444444444', 'content2-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'completed', 100, NOW() - INTERVAL '23 days', NOW() - INTERVAL '26 days'),
    (uuid_generate_v4(), '44444444-4444-4444-4444-444444444444', 'content3-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'in_progress', 50, NOW() - INTERVAL '20 days', NOW() - INTERVAL '24 days'),
    (uuid_generate_v4(), '55555555-5555-5555-5555-555555555555', 'content1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'completed', 100, NOW() - INTERVAL '22 days', NOW() - INTERVAL '24 days'),
    (uuid_generate_v4(), '55555555-5555-5555-5555-555555555555', 'content2-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'in_progress', 75, NOW() - INTERVAL '20 days', NOW() - INTERVAL '22 days');

-- Insert sample quiz submissions
INSERT INTO quiz_submissions (submission_id, user_id, quiz_id, score, answers, submitted_at, time_taken)
VALUES
    (uuid_generate_v4(), '44444444-4444-4444-4444-444444444444', 'quiz1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 66.67, '[{"question_id": "question1-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "answer_data": {"id": "b"}, "is_correct": true}, {"question_id": "question2-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "answer_data": {"id": "a"}, "is_correct": false}, {"question_id": "question3-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "answer_data": {"id": "true"}, "is_correct": true}]', NOW() - INTERVAL '20 days', 300),
    (uuid_generate_v4(), '55555555-5555-5555-5555-555555555555', 'quiz1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 100.0, '[{"question_id": "question1-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "answer_data": {"id": "b"}, "is_correct": true}, {"question_id": "question2-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "answer_data": {"id": "d"}, "is_correct": true}, {"question_id": "question3-aaaa-aaaa-aaaa-aaaaaaaaaaaa", "answer_data": {"id": "true"}, "is_correct": true}]', NOW() - INTERVAL '19 days', 240);

-- Insert sample content views
INSERT INTO content_views (view_id, user_id, content_id, course_id, viewed_at)
VALUES
    (uuid_generate_v4(), '44444444-4444-4444-4444-444444444444', 'content1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', NOW() - INTERVAL '28 days'),
    (uuid_generate_v4(), '44444444-4444-4444-4444-444444444444', 'content1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', NOW() - INTERVAL '27 days'),
    (uuid_generate_v4(), '44444444-4444-4444-4444-444444444444', 'content1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', NOW() - INTERVAL '26 days'),
    (uuid_generate_v4(), '44444444-4444-4444-4444-444444444444', 'content2-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', NOW() - INTERVAL '26 days'),
    (uuid_generate_v4(), '44444444-4444-4444-4444-444444444444', 'content2-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', NOW() - INTERVAL '25 days'),
    (uuid_generate_v4(), '44444444-4444-4444-4444-444444444444', 'content3-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', NOW() - INTERVAL '24 days'),
    (uuid_generate_v4(), '55555555-5555-5555-5555-555555555555', 'content1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', NOW() - INTERVAL '24 days'),
    (uuid_generate_v4(), '55555555-5555-5555-5555-555555555555', 'content1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', NOW() - INTERVAL '23 days'),
    (uuid_generate_v4(), '55555555-5555-5555-5555-555555555555', 'content2-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', NOW() - INTERVAL '22 days');

-- Insert sample achievements
INSERT INTO achievements (achievement_id, title, description, criteria, icon, created_at)
VALUES
    ('achievement1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'First Course Completed', 'Completed your first course', '{"type": "course_completion", "count": 1}', '🏆', NOW()),
    ('achievement2-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Perfect Quiz Score', 'Scored 100% on a quiz', '{"type": "quiz_score", "score": 100}', '🎯', NOW()),
    ('achievement3-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Learning Streak', 'Completed content for 7 consecutive days', '{"type": "daily_streak", "days": 7}', '🔥', NOW());

-- Insert sample user achievements
INSERT INTO user_achievements (user_achievement_id, user_id, achievement_id, awarded_at)
VALUES
    (uuid_generate_v4(), '55555555-5555-5555-5555-555555555555', 'achievement2-aaaa-aaaa-aaaa-aaaaaaaaaaaa', NOW() - INTERVAL '19 days');

-- Insert sample AI recommendations
INSERT INTO ai_recommendations (recommendation_id, user_id, content_id, recommendation_type, reasoning, created_at, status)
VALUES
    (uuid_generate_v4(), '44444444-4444-4444-4444-444444444444', 'content3-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'personalized', 'Based on your learning style and progress, this quiz will help reinforce your understanding of AI concepts.', NOW() - INTERVAL '22 days', 'active'),
    (uuid_generate_v4(), '55555555-5555-5555-5555-555555555555', 'content3-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'personalized', 'You have completed the introductory content. This quiz will test your knowledge before moving to the next module.', NOW() - INTERVAL '21 days', 'completed');

-- Insert sample learning paths
INSERT INTO learning_paths (path_id, user_id, course_id, path_data, created_at)
VALUES
    (uuid_generate_v4(), '44444444-4444-4444-4444-444444444444', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 
    '{
        "recommended_sequence": [
            {
                "module_id": "11111111-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "title": "What is AI?",
                "content_items": [
                    {
                        "content_id": "content1-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                        "title": "Introduction to AI",
                        "type": "video",
                        "priority": "high",
                        "reason": "Foundational content for the course"
                    },
                    {
                        "content_id": "content2-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                        "title": "History of AI",
                        "type": "text",
                        "priority": "medium",
                        "reason": "Provides historical context"
                    },
                    {
                        "content_id": "content3-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                        "title": "AI Concepts Quiz",
                        "type": "quiz",
                        "priority": "high",
                        "reason": "Tests understanding of core concepts"
                    }
                ]
            }
        ],
        "focus_areas": [
            {
                "topic": "AI Fundamentals",
                "reason": "Building a strong foundation is essential"
            }
        ],
        "estimated_completion_time": "2 hours",
        "learning_strategy": "Visual learner - focus on video content first"
    }', NOW() - INTERVAL '29 days'),
    
    (uuid_generate_v4(), '55555555-5555-5555-5555-555555555555', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 
    '{
        "recommended_sequence": [
            {
                "module_id": "11111111-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "title": "What is AI?",
                "content_items": [
                    {
                        "content_id": "content1-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                        "title": "Introduction to AI",
                        "type": "video",
                        "priority": "medium",
                        "reason": "Foundational content for the course"
                    },
                    {
                        "content_id": "content3-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                        "title": "AI Concepts Quiz",
                        "type": "quiz",
                        "priority": "high",
                        "reason": "Tests understanding of core concepts"
                    },
                    {
                        "content_id": "content2-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                        "title": "History of AI",
                        "type": "text",
                        "priority": "low",
                        "reason": "Provides historical context"
                    }
                ]
            }
        ],
        "focus_areas": [
            {
                "topic": "AI Fundamentals",
                "reason": "Building a strong foundation is essential"
            }
        ],
        "estimated_completion_time": "1.5 hours",
        "learning_strategy": "Auditory learner - focus on video content and interactive elements"
    }', NOW() - INTERVAL '24 days');
