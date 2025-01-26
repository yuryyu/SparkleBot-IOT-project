import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SparkleBot Opening Screen")
        self.setGeometry(400, 400, 900, 550)  # Adjusted size for better layout

        # Create a central widget and set layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # Add a title at the top
        title_label = QLabel("Welcome To SparkleBot!", self)
        title_label.setAlignment(Qt.AlignCenter)  # Center align the text
        title_label.setStyleSheet("font-size: 50px; font-weight: bold; color: orange;")  # Add some styling
        layout.addWidget(title_label)

        # Define your project folder
        self.project_folder = os.path.dirname(os.path.abspath(__file__))

        # Define files and custom button labels
        self.project_files = {
            "BUTTONEMU.py": "On/Off",
            "DHTEMU.py": "Temprature and Battery",
            "RELAYEMU.py": "Relay",
            "MAINGUISparkleBot.py": "Main Gui",
            "datamanager.py": "DataManager"
        }

        for file_name, button_label in self.project_files.items():
            button = QPushButton(button_label, self)
            button.clicked.connect(lambda _, f=file_name: self.run_file(f))
            layout.addWidget(button)

        # Set the layout to the central widget and make it the central widget for the window
        self.setCentralWidget(central_widget)

        # Set background logo using a stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-image: url('sparklebot.png');  /* Replace 'logo.png' with your image file */
                background-repeat: no-repeat;
                background-position: center;
                background-color: #A9A9A9; /* Optional: background color */
            }
        """)

    def run_file(self, file_name):
        file_path = os.path.join(self.project_folder, file_name)
        if os.path.exists(file_path):
            try:
                # Use sys.executable to ensure the current Python interpreter is used
                subprocess.Popen([sys.executable, file_path])
            except Exception as e:
                print(f"Failed to run {file_name}: {e}")
        else:
            print(f"File {file_name} not found in project folder!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
