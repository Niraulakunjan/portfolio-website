import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt

class EmailSenderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iClass - Course Order Email Sender")
        self.setGeometry(100, 100, 400, 300)
        
        # SMTP Configuration
        self.smtp_config = {
            'server': 'smtp.gmail.com',  # Change this to your SMTP server
            'port': 587,                 # Change this to your SMTP port
            'email': 'niraula67kunjan@gmail.com',  # Change this to your email
            'password': 'acfj alcr fbts xojl'   # Change this to your app password
        }
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create input fields
        self.receiver_email = self.create_input_field("Receiver Email:", layout)
        self.order_id = self.create_input_field("Order ID:", layout)
        self.course_name = self.create_input_field("Course Name:", layout)
        self.amount = self.create_input_field("Amount:", layout)
        
        # Create send button
        send_button = QPushButton("Send Email")
        send_button.clicked.connect(self.send_email)
        layout.addWidget(send_button)
        
    def create_input_field(self, label_text, layout):
        label = QLabel(label_text)
        input_field = QLineEdit()
        layout.addWidget(label)
        layout.addWidget(input_field)
        return input_field
    
    def send_email(self):
        # Get email content
        receiver = self.receiver_email.text()
        order_id = self.order_id.text()
        course = self.course_name.text()
        amount = self.amount.text()
        
        # Validate inputs
        if not all([receiver, order_id, course, amount]):
            QMessageBox.warning(self, "Warning", "Please fill in all fields")
            return
        
        # Email content
        subject = f"Course Order Confirmation - Order #{order_id}"
        
        # HTML Email template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    color: #333333;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .header {{
                    background-color: #2c3e50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .content {{
                    padding: 20px;
                    background-color: #ffffff;
                }}
                .course-details {{
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #3498db;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    background-color: #f8f9fa;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>iClass</h1>
            </div>
            
            <div class="content">
                <h2>Course Order Confirmation</h2>
                <p>Dear Student,</p>
                
                <p>Thank you for choosing iClass! We have received your request for Order #{order_id}.</p>
                
                <div class="course-details">
                    <h3>Course Details:</h3>
                    <p><strong>Course Name:</strong> {course}</p>
                    <p><strong>Amount:</strong> ${amount}</p>
                </div>
                
                <p>To complete your payment and access your course, please click the button below:</p>
                
                <a href="https://wa.me/qr/VAVOAZC45SDGP1" class="button">Complete Payment</a>
                
                <p>If you have any questions, please don't hesitate to contact our support team.</p>
                
                <p>Best regards,<br>
                iClass Support Team</p>
            </div>
            
            <div class="footer">
                <p>Visit us at: <a href="http://www.niraulakunjan.com.np">www.niraulakunjan.com.np</a></p>
                <p>© 2024 iClass. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_config['email']
            msg['To'] = receiver
            msg['Subject'] = subject
            
            # Attach both plain text and HTML versions
            text_part = MIMEText(f"""
            Course Order Confirmation - Order #{order_id}
            
            Dear Student,
            
            We have received your request for Order #{order_id}.
            
            Course Details:
            - Course Name: {course}
            - Amount: ${amount}
            
            To complete your payment and access your course, please visit:
            https://wa.me/qr/VAVOAZC45SDGP1
            
            Visit us at: www.niraulakunjan.com.np
            
            Best regards,
            iClass Support Team
            """, 'plain')
            
            html_part = MIMEText(html_content, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Connect to SMTP server and send email
            with smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port']) as server:
                server.starttls()
                server.login(self.smtp_config['email'], self.smtp_config['password'])
                server.send_message(msg)
            
            QMessageBox.information(self, "Success", "Email sent successfully!")
            
            # Clear input fields
            self.receiver_email.clear()
            self.order_id.clear()
            self.course_name.clear()
            self.amount.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to send email: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmailSenderApp()
    window.show()
    sys.exit(app.exec_())