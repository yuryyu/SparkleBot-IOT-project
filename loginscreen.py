import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import subprocess

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login to SparkleBot')
        self.setGeometry(100, 100, 400, 300)  # Increased window size
        
        # Define widgets
        self.label_user = QLabel('Username:')
        self.label_pass = QLabel('Password:')
        self.text_user = QLineEdit(self)
        self.text_pass = QLineEdit(self)
        self.text_pass.setEchoMode(QLineEdit.Password)
        self.button_login = QPushButton('Login')
        
        # Connect the login button to the function
        self.button_login.clicked.connect(self.check_credentials)
        
        # Vertical layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_user)
        layout.addWidget(self.text_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.text_pass)
        layout.addWidget(self.button_login)
        self.setLayout(layout)
        
    def check_credentials(self):
        if self.text_user.text() == '1' and self.text_pass.text() == '1':
            self.goto_sparkle_bot_start_screen()
        else:
            self.text_user.setText('')
            self.text_pass.setText('')
            self.text_user.setPlaceholderText('Invalid credentials')
            self.text_pass.setPlaceholderText('Invalid credentials')
    
    def goto_sparkle_bot_start_screen(self):
        self.hide()
        subprocess.Popen(['python', 'SparkleBotStartScreen.py'])

class SparkleBotStartScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SparkleBot Start Screen')
        self.setGeometry(100, 100, 800, 600)  # Increased window size
        
        # Set background image
        self.background_label = QLabel(self)
        pixmap = QPixmap('background_image.png')  # Replace with your .png file name
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(self.rect())
        self.background_label.setScaledContents(True)
        
        # Add a welcome label
        self.label = QLabel('Welcome to SparkleBot!', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel {color: white; font-size: 24px;}")
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
