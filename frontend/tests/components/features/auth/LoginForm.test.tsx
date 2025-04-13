import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import LoginForm from '@/components/features/auth/LoginForm';
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs';

// Mock the useRouter hook
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
    refresh: jest.fn(),
  }),
}));

// Mock the Supabase client
jest.mock('@supabase/auth-helpers-nextjs', () => ({
  createClientComponentClient: jest.fn(),
}));

describe('LoginForm Component', () => {
  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();
    
    // Setup default mock implementation
    (createClientComponentClient as jest.Mock).mockReturnValue({
      auth: {
        signInWithPassword: jest.fn().mockResolvedValue({
          error: null,
        }),
      },
    });
  });
  
  it('renders correctly', () => {
    render(<LoginForm />);
    
    expect(screen.getByText('Login')).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    expect(screen.getByText('Forgot password?')).toBeInTheDocument();
    expect(screen.getByText('Register')).toBeInTheDocument();
  });
  
  it('handles form submission with valid credentials', async () => {
    const mockSignIn = jest.fn().mockResolvedValue({ error: null });
    (createClientComponentClient as jest.Mock).mockReturnValue({
      auth: {
        signInWithPassword: mockSignIn,
      },
    });
    
    render(<LoginForm />);
    
    // Fill in the form
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' },
    });
    
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'password123' },
    });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /login/i }));
    
    // Check if the signInWithPassword method was called with the correct arguments
    await waitFor(() => {
      expect(mockSignIn).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
    });
    
    // Button should be in loading state
    expect(screen.getByRole('button', { name: /logging in/i })).toBeInTheDocument();
  });
  
  it('displays an error message when login fails', async () => {
    const mockSignIn = jest.fn().mockResolvedValue({
      error: { message: 'Invalid login credentials' },
    });
    
    (createClientComponentClient as jest.Mock).mockReturnValue({
      auth: {
        signInWithPassword: mockSignIn,
      },
    });
    
    render(<LoginForm />);
    
    // Fill in the form
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'test@example.com' },
    });
    
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'wrongpassword' },
    });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: /login/i }));
    
    // Check if the error message is displayed
    await waitFor(() => {
      expect(screen.getByText('Invalid login credentials')).toBeInTheDocument();
    });
    
    // Button should not be in loading state anymore
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });
  
  it('navigates to the register page when clicking the register link', () => {
    render(<LoginForm />);
    
    const registerLink = screen.getByText('Register');
    expect(registerLink).toHaveAttribute('href', '/auth/register');
  });
  
  it('navigates to the forgot password page when clicking the forgot password link', () => {
    render(<LoginForm />);
    
    const forgotPasswordLink = screen.getByText('Forgot password?');
    expect(forgotPasswordLink).toHaveAttribute('href', '/auth/forgot-password');
  });
});
