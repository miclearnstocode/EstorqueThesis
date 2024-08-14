import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_warning_email(student_email, student_name, course, missing_items):
    sender_email = "your_email@youruniversity.edu"
    password = "your_password"

    message = MIMEMultipart("alternative")
    message["Subject"] = f"Warning: Incomplete Grade in {course}"
    message["From"] = sender_email
    message["To"] = student_email

    text = f"""
    Dear {student_name},

    This is a warning that you have an incomplete grade in {course}.
    Missing items: {', '.join(missing_items)}

    Please submit these items as soon as possible.

    Best regards,
    Your Professor
    """

    part1 = MIMEText(text, "plain")
    message.attach(part1)

    with smtplib.SMTP_SSL("smtp.youruniversity.edu", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, student_email, message.as_string())

# Example usage
send_warning_email("student@email.com", "John Doe", "MATH101", ["Midterm Exam", "Final Project"])
