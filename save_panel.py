from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon
import os

class SavePanel(QWidget):
    def __init__(self, main_window):
        """
        Initialize the SavePanel widget.

        Parameters:
        main_window (QWidget): The main window of the application.

        The SavePanel widget is a dialog window for saving data. It provides options for selecting the data type, format, and saving path.
        """        
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Save Data")
        self.setGeometry(100, 100, 300, 200)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "assets", "Logo_NBackground.png")
        self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()

        self.save_type_label = QLabel("Select data type to save:", self)
        layout.addWidget(self.save_type_label)

        self.save_type_combo = QComboBox(self)
        self.save_type_combo.addItems(["Historical", "Forecast", "Both"])
        layout.addWidget(self.save_type_combo)

        self.format_label = QLabel("Select format to save:", self)
        layout.addWidget(self.format_label)

        self.format_combo = QComboBox(self)
        self.format_combo.addItems(["Format 1 (List)", "Format 2 (Columns)"])
        layout.addWidget(self.format_combo)

        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_data)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_data(self):
        """
        Save the selected data type and format to the specified path.

        This function retrieves the selected data type, format, and save path from the GUI components.
        It then calls the `save_forecast` method of the `main_window` object to perform the actual saving process.
        Finally, it closes the SavePanel window.

        Parameters:
        self (SavePanel): The instance of the SavePanel class.

        Returns:
        None
        """        
        save_type = self.save_type_combo.currentText()
        format_type = self.format_combo.currentText()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", self.main_window.extracted_dataset_dir, "CSV Files (*.csv);;All Files (*)")
        if save_path:
            self.main_window.save_forecast(save_type, format_type, save_path)
            self.close()
