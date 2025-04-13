"""
Email service for sending emails.
"""

import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

from app.core.config import settings
from app.core.logging import logger

class EmailService:
    """
    Service for sending emails.
    """

    def __init__(self):
        """
        Initialize the email service.
        """
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.username = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAIL_FROM

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
    ) -> bool:
        """
        Send an email.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            text_content: Plain text content of the email (optional)
            cc: List of CC recipients (optional)
            bcc: List of BCC recipients (optional)

        Returns:
            True if the email was sent successfully, False otherwise
        """
        if not all([self.host, self.port, self.username, self.password, self.from_email]):
            logger.warning("Email service is not configured properly")
            return False

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.from_email
        msg['To'] = to_email

        if cc:
            msg['Cc'] = ", ".join(cc)

        if bcc:
            msg['Bcc'] = ", ".join(bcc)

        # Attach parts
        if text_content:
            msg.attach(MIMEText(text_content, 'plain'))

        msg.attach(MIMEText(html_content, 'html'))

        try:
            # Connect to SMTP server
            server = smtplib.SMTP(self.host, self.port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.username, self.password)

            # Send email
            recipients = [to_email]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)

            server.sendmail(self.from_email, recipients, msg.as_string())
            server.quit()

            logger.info(f"Email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    def send_password_reset_email(self, to_email: str, reset_token: str, username: str) -> bool:
        """
        Send a password reset email.

        Args:
            to_email: Recipient email address
            reset_token: Password reset token
            username: Username of the recipient

        Returns:
            True if the email was sent successfully, False otherwise
        """
        subject = "Password Reset - AI Learning Platform"

        # Create reset link
        reset_link = f"{settings.FRONTEND_URL}/auth/reset-password?token={reset_token}"

        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4f46e5; color: white; padding: 10px 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .button {{ display: inline-block; background-color: #4f46e5; color: white; text-decoration: none; padding: 10px 20px; border-radius: 4px; }}
                .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Password Reset</h1>
                </div>
                <div class="content">
                    <p>Hello {username},</p>
                    <p>We received a request to reset your password for your AI Learning Platform account. If you didn't make this request, you can ignore this email.</p>
                    <p>To reset your password, click the button below:</p>
                    <p style="text-align: center;">
                        <a href="{reset_link}" class="button">Reset Password</a>
                    </p>
                    <p>Or copy and paste this link into your browser:</p>
                    <p>{reset_link}</p>
                    <p>This link will expire in 1 hour.</p>
                    <p>Best regards,<br>The AI Learning Platform Team</p>
                </div>
                <div class="footer">
                    <p>This is an automated email. Please do not reply to this message.</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Hello {username},

        We received a request to reset your password for your AI Learning Platform account. If you didn't make this request, you can ignore this email.

        To reset your password, click the link below:
        {reset_link}

        This link will expire in 1 hour.

        Best regards,
        The AI Learning Platform Team

        This is an automated email. Please do not reply to this message.
        """

        return self.send_email(to_email, subject, html_content, text_content)

    def send_welcome_email(self, to_email: str, username: str) -> bool:
        """
        Send a welcome email to a new user.

        Args:
            to_email: Recipient email address
            username: Username of the recipient

        Returns:
            True if the email was sent successfully, False otherwise
        """
        subject = "Welcome to AI Learning Platform"

        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4f46e5; color: white; padding: 10px 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .button {{ display: inline-block; background-color: #4f46e5; color: white; text-decoration: none; padding: 10px 20px; border-radius: 4px; }}
                .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to AI Learning Platform</h1>
                </div>
                <div class="content">
                    <p>Hello {username},</p>
                    <p>Welcome to AI Learning Platform! We're excited to have you join our community of learners.</p>
                    <p>With AI Learning Platform, you can:</p>
                    <ul>
                        <li>Access personalized learning paths tailored to your learning style</li>
                        <li>Explore a wide range of courses on various topics</li>
                        <li>Track your progress and earn achievements</li>
                        <li>Connect with instructors and other learners</li>
                    </ul>
                    <p>To get started, click the button below to explore our courses:</p>
                    <p style="text-align: center;">
                        <a href="{settings.FRONTEND_URL}/courses" class="button">Explore Courses</a>
                    </p>
                    <p>If you have any questions or need assistance, please don't hesitate to contact our support team.</p>
                    <p>Best regards,<br>The AI Learning Platform Team</p>
                </div>
                <div class="footer">
                    <p>This is an automated email. Please do not reply to this message.</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Hello {username},

        Welcome to AI Learning Platform! We're excited to have you join our community of learners.

        With AI Learning Platform, you can:
        - Access personalized learning paths tailored to your learning style
        - Explore a wide range of courses on various topics
        - Track your progress and earn achievements
        - Connect with instructors and other learners

        To get started, visit our courses page:
        {settings.FRONTEND_URL}/courses

        If you have any questions or need assistance, please don't hesitate to contact our support team.

        Best regards,
        The AI Learning Platform Team

        This is an automated email. Please do not reply to this message.
        """

        return self.send_email(to_email, subject, html_content, text_content)

    def send_course_completion_email(self, to_email: str, username: str, course_title: str) -> bool:
        """
        Send a course completion email.

        Args:
            to_email: Recipient email address
            username: Username of the recipient
            course_title: Title of the completed course

        Returns:
            True if the email was sent successfully, False otherwise
        """
        subject = f"Congratulations on Completing {course_title}"

        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4f46e5; color: white; padding: 10px 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .button {{ display: inline-block; background-color: #4f46e5; color: white; text-decoration: none; padding: 10px 20px; border-radius: 4px; }}
                .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
                .certificate {{ border: 2px solid #4f46e5; padding: 20px; text-align: center; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Course Completion Certificate</h1>
                </div>
                <div class="content">
                    <p>Hello {username},</p>
                    <p>Congratulations on completing the course <strong>{course_title}</strong>!</p>
                    <div class="certificate">
                        <h2>Certificate of Completion</h2>
                        <p>This certifies that</p>
                        <h3>{username}</h3>
                        <p>has successfully completed the course</p>
                        <h3>{course_title}</h3>
                        <p>on {datetime.now().strftime('%B %d, %Y')}</p>
                    </div>
                    <p>You can view your certificate and share it on social media by clicking the button below:</p>
                    <p style="text-align: center;">
                        <a href="{settings.FRONTEND_URL}/certificates" class="button">View Certificate</a>
                    </p>
                    <p>We hope you enjoyed the course and found it valuable. Check out our other courses to continue your learning journey!</p>
                    <p>Best regards,<br>The AI Learning Platform Team</p>
                </div>
                <div class="footer">
                    <p>This is an automated email. Please do not reply to this message.</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Hello {username},

        Congratulations on completing the course {course_title}!

        This certifies that {username} has successfully completed the course {course_title} on {datetime.now().strftime('%B %d, %Y')}.

        You can view your certificate and share it on social media by visiting:
        {settings.FRONTEND_URL}/certificates

        We hope you enjoyed the course and found it valuable. Check out our other courses to continue your learning journey!

        Best regards,
        The AI Learning Platform Team

        This is an automated email. Please do not reply to this message.
        """

        return self.send_email(to_email, subject, html_content, text_content)

# Create email service instance
email_service = EmailService()
