import React from 'react';
import LoginForm from '@/components/features/auth/LoginForm';

export const metadata = {
  title: 'Login | AI Learning Platform',
  description: 'Login to your AI Learning Platform account',
};

export default function LoginPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <LoginForm />
    </div>
  );
}
