from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import os

class AboutWindow(QWidget):
    def __init__(self):
        """
        Initialize the AboutWindow class.

        This class represents a window that displays information about the application.

        Parameters:
        None

        Returns:
        None
        """
        super().__init__()
        self.setWindowTitle("About")
        self.setGeometry(100, 100, 300, 350)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "assets", "Logo_NBackground.png")
        github_icon_path = os.path.join(script_dir, "assets", "github.png")
        linkedin_icon_path = os.path.join(script_dir, "assets", "linkedin.png")
        self.setWindowIcon(QIcon(icon_path))
        
        layout = QVBoxLayout()

        about_label = QLabel("Forecasting Application\nVersion Alpha 1.0\nContact: yerko.veliz@alu.ucm.cl", self)
        about_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(about_label)

        logo_label = QLabel(self)
        pixmap = QPixmap(icon_path)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        
        github_layout = QHBoxLayout()
        github_layout.setAlignment(Qt.AlignCenter)
        github_icon_label = QLabel(self)
        github_icon = QPixmap(github_icon_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        github_icon_label.setPixmap(github_icon)
        github_layout.addWidget(github_icon_label)

        github_label = QLabel('<a href="https://github.com/UCM-Industrial/Thesis-Y_Veliz-Electricity-forecast/tree/main">Thesis Link</a>', self)
        github_label.setOpenExternalLinks(True)
        github_layout.addWidget(github_label)

        layout.addLayout(github_layout)

        linkedin_layout = QHBoxLayout()
        linkedin_layout.setAlignment(Qt.AlignCenter)
        linkedin_icon_label = QLabel(self)
        linkedin_icon = QPixmap(linkedin_icon_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        linkedin_icon_label.setPixmap(linkedin_icon)
        linkedin_layout.addWidget(linkedin_icon_label)

        linkedin_label = QLabel('<a href="https://www.linkedin.com/in/yerko-v0/">LinkedIn Profile</a>', self)
        linkedin_label.setOpenExternalLinks(True)
        linkedin_layout.addWidget(linkedin_label)

        layout.addLayout(linkedin_layout)

        self.setLayout(layout)

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    aboutWin = AboutWindow()
    aboutWin.show()
    sys.exit(app.exec_())