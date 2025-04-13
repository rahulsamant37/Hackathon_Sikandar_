import React from 'react';
import RegisterForm from '@/components/features/auth/RegisterForm';

export const metadata = {
  title: 'Register | AI Learning Platform',
  description: 'Create a new account on AI Learning Platform',
};

export default function RegisterPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <RegisterForm />
    </div>
  );
}
