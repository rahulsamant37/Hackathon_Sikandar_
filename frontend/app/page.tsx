import Link from 'next/link'
import { BookOpen, Award, Lightbulb, TrendingUp, CheckCircle } from '@/components/ui/Icons'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      {/* Header/Navigation */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="h-8 w-8 rounded-full bg-primary-600 flex items-center justify-center text-white font-bold mr-2">
                AI
              </div>
              <span className="text-xl font-semibold text-gray-800">LearnAI</span>
            </div>
            <nav className="hidden md:flex space-x-10">
              <a href="#features" className="text-base font-medium text-gray-500 hover:text-gray-900">
                Features
              </a>
              <a href="#testimonials" className="text-base font-medium text-gray-500 hover:text-gray-900">
                Testimonials
              </a>
              <a href="#pricing" className="text-base font-medium text-gray-500 hover:text-gray-900">
                Pricing
              </a>
            </nav>
            <div className="flex items-center space-x-4">
              <Link href="/auth/login" className="text-base font-medium text-gray-500 hover:text-gray-900">
                Log in
              </Link>
              <Link
                href="/auth/register"
                className="inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-primary-600 hover:bg-primary-700"
              >
                Sign up
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-16 pb-24 sm:pt-24 sm:pb-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:grid lg:grid-cols-12 lg:gap-8">
            <div className="sm:text-center md:max-w-2xl md:mx-auto lg:col-span-6 lg:text-left">
              <h1>
                <span className="block text-sm font-semibold uppercase tracking-wide text-primary-600">
                  Introducing LearnAI
                </span>
                <span className="mt-1 block text-4xl tracking-tight font-extrabold sm:text-5xl xl:text-6xl">
                  <span className="block text-gray-900">Learn Smarter with</span>
                  <span className="block text-primary-600">AI-Powered Education</span>
                </span>
              </h1>
              <p className="mt-3 text-base text-gray-500 sm:mt-5 sm:text-xl lg:text-lg xl:text-xl">
                Our adaptive learning platform leverages artificial intelligence to create personalized learning experiences tailored to your unique style, pace, and goals.
              </p>
              <div className="mt-8 sm:max-w-lg sm:mx-auto sm:text-center lg:text-left lg:mx-0">
                <div className="flex flex-col sm:flex-row sm:justify-center lg:justify-start gap-4">
                  <Link
                    href="/auth/register"
                    className="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    Get Started
                  </Link>
                  <Link
                    href="/courses"
                    className="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-primary-700 bg-primary-100 hover:bg-primary-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    Browse Courses
                  </Link>
                </div>
              </div>
            </div>
            <div className="mt-12 relative sm:max-w-lg sm:mx-auto lg:mt-0 lg:max-w-none lg:mx-0 lg:col-span-6 lg:flex lg:items-center">
              <div className="relative mx-auto w-full rounded-lg shadow-lg lg:max-w-md">
                <div className="relative block w-full bg-white rounded-lg overflow-hidden">
                  <div className="w-full h-80 bg-gradient-to-r from-primary-500 to-primary-700 flex items-center justify-center">
                    <div className="text-center px-6">
                      <BookOpen className="h-12 w-12 text-white mx-auto mb-4" />
                      <h3 className="text-2xl font-bold text-white">Interactive Learning Experience</h3>
                      <p className="mt-2 text-white opacity-90">Engage with AI-powered content that adapts to your learning style</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-base font-semibold text-primary-600 tracking-wide uppercase">Features</h2>
            <p className="mt-1 text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight">A better way to learn</p>
            <p className="max-w-xl mt-5 mx-auto text-xl text-gray-500">Our platform combines cutting-edge AI with proven educational methods to deliver an unparalleled learning experience.</p>
          </div>

          <div className="mt-16">
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
              <div className="pt-6">
                <div className="flow-root bg-gray-50 rounded-lg px-6 pb-8">
                  <div className="-mt-6">
                    <div>
                      <span className="inline-flex items-center justify-center p-3 bg-primary-600 rounded-md shadow-lg">
                        <Lightbulb className="h-6 w-6 text-white" />
                      </span>
                    </div>
                    <h3 className="mt-8 text-lg font-medium text-gray-900 tracking-tight">Personalized Learning Paths</h3>
                    <p className="mt-5 text-base text-gray-500">
                      Our AI analyzes your learning style, pace, and goals to create a customized learning journey that maximizes your potential.
                    </p>
                  </div>
                </div>
              </div>

              <div className="pt-6">
                <div className="flow-root bg-gray-50 rounded-lg px-6 pb-8">
                  <div className="-mt-6">
                    <div>
                      <span className="inline-flex items-center justify-center p-3 bg-primary-600 rounded-md shadow-lg">
                        <TrendingUp className="h-6 w-6 text-white" />
                      </span>
                    </div>
                    <h3 className="mt-8 text-lg font-medium text-gray-900 tracking-tight">Adaptive Assessments</h3>
                    <p className="mt-5 text-base text-gray-500">
                      Dynamic quizzes and tests that adjust difficulty based on your performance, ensuring you're always appropriately challenged.
                    </p>
                  </div>
                </div>
              </div>

              <div className="pt-6">
                <div className="flow-root bg-gray-50 rounded-lg px-6 pb-8">
                  <div className="-mt-6">
                    <div>
                      <span className="inline-flex items-center justify-center p-3 bg-primary-600 rounded-md shadow-lg">
                        <Award className="h-6 w-6 text-white" />
                      </span>
                    </div>
                    <h3 className="mt-8 text-lg font-medium text-gray-900 tracking-tight">Achievement System</h3>
                    <p className="mt-5 text-base text-gray-500">
                      Earn badges, certificates, and rewards as you progress, keeping you motivated and engaged throughout your learning journey.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-base font-semibold text-primary-600 tracking-wide uppercase">Testimonials</h2>
            <p className="mt-1 text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight">Hear from our students</p>
          </div>

          <div className="mt-16 grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <div className="h-12 w-12 rounded-full bg-gray-200 flex items-center justify-center text-gray-500 font-bold">JS</div>
                <div className="ml-4">
                  <h4 className="text-lg font-bold">John Smith</h4>
                  <p className="text-gray-500">Software Developer</p>
                </div>
              </div>
              <p className="text-gray-600">"The personalized learning path helped me master machine learning concepts in half the time I expected. The adaptive quizzes were particularly helpful in identifying my weak areas."</p>
              <div className="mt-4 flex text-yellow-400">
                <span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <div className="h-12 w-12 rounded-full bg-gray-200 flex items-center justify-center text-gray-500 font-bold">EJ</div>
                <div className="ml-4">
                  <h4 className="text-lg font-bold">Emily Johnson</h4>
                  <p className="text-gray-500">Data Scientist</p>
                </div>
              </div>
              <p className="text-gray-600">"As someone who struggles with traditional learning methods, LearnAI's approach was a game-changer. The platform adapted to my visual learning style and kept me engaged."</p>
              <div className="mt-4 flex text-yellow-400">
                <span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <div className="h-12 w-12 rounded-full bg-gray-200 flex items-center justify-center text-gray-500 font-bold">MR</div>
                <div className="ml-4">
                  <h4 className="text-lg font-bold">Michael Rodriguez</h4>
                  <p className="text-gray-500">Student</p>
                </div>
              </div>
              <p className="text-gray-600">"The achievement system kept me motivated throughout my courses. I found myself excited to log in each day to continue my learning streak and earn new badges."</p>
              <div className="mt-4 flex text-yellow-400">
                <span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-base font-semibold text-primary-600 tracking-wide uppercase">Pricing</h2>
            <p className="mt-1 text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight">Plans for every learner</p>
            <p className="max-w-xl mt-5 mx-auto text-xl text-gray-500">Choose the plan that works best for your learning goals and budget.</p>
          </div>

          <div className="mt-16 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {/* Basic Plan */}
            <div className="border border-gray-200 rounded-lg shadow-sm divide-y divide-gray-200">
              <div className="p-6">
                <h2 className="text-lg font-medium text-gray-900">Basic</h2>
                <p className="mt-4 text-sm text-gray-500">Perfect for beginners and casual learners.</p>
                <p className="mt-8">
                  <span className="text-4xl font-extrabold text-gray-900">Free</span>
                  <span className="text-base font-medium text-gray-500"></span>
                </p>
                <Link
                  href="/auth/register"
                  className="mt-8 block w-full bg-gray-800 border border-gray-800 rounded-md py-2 text-sm font-semibold text-white text-center hover:bg-gray-900"
                >
                  Start Free
                </Link>
              </div>
              <div className="pt-6 pb-8 px-6">
                <h3 className="text-xs font-medium text-gray-900 tracking-wide uppercase">What's included</h3>
                <ul className="mt-6 space-y-4">
                  <li className="flex space-x-3">
                    <CheckCircle className="flex-shrink-0 h-5 w-5 text-green-500" />
                    <span className="text-sm text-gray-500">Access to 5 free courses</span>
                  </li>
                  <li className="flex space-x-3">
                    <CheckCircle className="flex-shrink-0 h-5 w-5 text-green-500" />
                    <span className="text-sm text-gray-500">Basic learning tools</span>
                  </li>
                  <li className="flex space-x-3">
                    <CheckCircle className="flex-shrink-0 h-5 w-5 text-green-500" />
                    <span className="text-sm text-gray-500">Limited progress tracking</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Pro Plan */}
            <div className="border border-primary-600 rounded-lg shadow-sm divide-y divide-gray-200 relative">
              <div className="p-6 bg-primary-50">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 transform">
                  <span className="inline-block rounded-full bg-primary-600 px-4 py-1.5 text-xs font-semibold uppercase tracking-wide text-white">Most Popular</span>
                </div>
                <h2 className="text-lg font-medium text-primary-900">Pro</h2>
                <p className="mt-4 text-sm text-primary-700">For serious learners who want to master new skills.</p>
                <p className="mt-8">
                  <span className="text-4xl font-extrabold text-gray-900">$19</span>
                  <span className="text-base font-medium text-gray-500">/mo</span>
                </p>
                <Link
                  href="/auth/register"
                  className="mt-8 block w-full bg-primary-600 border border-primary-600 rounded-md py-2 text-sm font-semibold text-white text-center hover:bg-primary-700"
                >
                  Get Started
                </Link>
              </div>
              <div className="pt-6 pb-8 px-6">
                <h3 className="text-xs font-medium text-gray-900 tracking-wide uppercase">What's included</h3>
                <ul className="mt-6 space-y-4">
                  <li className="flex space-x-3">
                    <CheckCircle className="flex-shrink-0 h-5 w-5 text-green-500" />
                    <span className="text-sm text-gray-500">Access to all courses</span>
                  </li>
                  <li className="flex space-x-3">
                    <CheckCircle className="flex-shrink-0 h-5 w-5 text-green-500" />
                    <span className="text-sm text-gray-500">Advanced AI learning paths</span>
                  </li>
                  <li className="flex space-x-3">
                    <CheckCircle className="flex-shrink-0 h-5 w-5 text-green-500" />
                    <span className="text-sm text-gray-500">Adaptive assessments</span>
                  </li>
                  <li className="flex space-x-3">
                    <CheckCircle className="flex-shrink-0 h-5 w-5 text-green-500" />
                    <span className="text-sm text-gray-500">Detailed analytics</span>
                  </li>
                  <li className="flex space-x-3">
                    <CheckCircle className="flex-shrink-0 h-5 w-5 text-green-500" />
                    <span className="text-sm text-gray-500">Certificate of completion</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Enterprise Plan */}
            <div className="border border-gray-200 rounded-lg shadow-sm divide-y divide-gray-200">
              <div className="p-6">
                <h2 className="text-lg font-medium text-gray-900">Enterprise</h2>
                <p className="mt-4 text-sm text-gray-500">For organizations looking to train their teams.</p>
                <p className="mt-8">
                  <span className="text-4xl font-extrabold text-gray-900">$49</span>
                  <span className="text-base font-medium text-gray-500">/user/mo</span>
                </p>
                <Link
                  href="/contact"
                  className="mt-8 block w-full bg-gray-800 border border-gray-800 rounded-md py-2 text-sm font-semibold text-white text-center hover:bg-gray-900"
                >
                  Contact Sales
                </Link>
              </div>
              <div className="pt-6 pb-8 px-6">
                <h3 className="text-xs font-medium text-gray-900 tracking-wide uppercase">What's included</h3>
                <ul className="mt-6 space-y-4">
                  <li className="flex space-x-3">
                    <CheckCircle className="flex-shrink-0 h-5 w-5 text-green-500" />
                    <span className="text-sm text-gray-500">Everything in Pro plan</span>
                  </li>
                  <li className="flex space-x-3">
                    <CheckCircle className="flex-shrink-0 h-5 w-5 text-green-500" />
                    <span className="text-sm text-gray-500">Team management</span>
                  </li>
                  <li className="flex space-x-3">
                    <CheckCircle className="flex-shrink-0 h-5 w-5 text-green-500" />
                    <span className="text-sm text-gray-500">Custom learning paths</span>
                  </li>
                  <li className="flex space-x-3">
                    <CheckCircle className="flex-shrink-0 h-5 w-5 text-green-500" />
                    <span className="text-sm text-gray-500">Advanced reporting</span>
                  </li>
                  <li className="flex space-x-3">
                    <CheckCircle className="flex-shrink-0 h-5 w-5 text-green-500" />
                    <span className="text-sm text-gray-500">Dedicated support</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary-700">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between">
          <h2 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            <span className="block">Ready to start learning?</span>
            <span className="block text-primary-200">Join thousands of satisfied students today.</span>
          </h2>
          <div className="mt-8 flex lg:mt-0 lg:flex-shrink-0">
            <div className="inline-flex rounded-md shadow">
              <Link
                href="/auth/register"
                className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-primary-700 bg-white hover:bg-gray-50"
              >
                Get started
              </Link>
            </div>
            <div className="ml-3 inline-flex rounded-md shadow">
              <Link
                href="/courses"
                className="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-500"
              >
                Browse courses
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">Platform</h3>
              <ul className="mt-4 space-y-4">
                <li>
                  <a href="#" className="text-base text-gray-500 hover:text-gray-900">Features</a>
                </li>
                <li>
                  <a href="#" className="text-base text-gray-500 hover:text-gray-900">Courses</a>
                </li>
                <li>
                  <a href="#" className="text-base text-gray-500 hover:text-gray-900">Pricing</a>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">Support</h3>
              <ul className="mt-4 space-y-4">
                <li>
                  <a href="#" className="text-base text-gray-500 hover:text-gray-900">Documentation</a>
                </li>
                <li>
                  <a href="#" className="text-base text-gray-500 hover:text-gray-900">Guides</a>
                </li>
                <li>
                  <a href="#" className="text-base text-gray-500 hover:text-gray-900">Contact Us</a>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">Company</h3>
              <ul className="mt-4 space-y-4">
                <li>
                  <a href="#" className="text-base text-gray-500 hover:text-gray-900">About</a>
                </li>
                <li>
                  <a href="#" className="text-base text-gray-500 hover:text-gray-900">Blog</a>
                </li>
                <li>
                  <a href="#" className="text-base text-gray-500 hover:text-gray-900">Careers</a>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">Legal</h3>
              <ul className="mt-4 space-y-4">
                <li>
                  <a href="#" className="text-base text-gray-500 hover:text-gray-900">Privacy</a>
                </li>
                <li>
                  <a href="#" className="text-base text-gray-500 hover:text-gray-900">Terms</a>
                </li>
              </ul>
            </div>
          </div>
          <div className="mt-12 border-t border-gray-200 pt-8">
            <p className="text-base text-gray-400 text-center">&copy; 2023 LearnAI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
