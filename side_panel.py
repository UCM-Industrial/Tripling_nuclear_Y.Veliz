from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QLineEdit, QLabel, QCheckBox, QGridLayout, QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import matplotlib.container
import os

class SidePanelWindow(QWidget):

    def __init__(self, main_window):
        """
        Initialize the Settings window with the provided main window.

        Parameters:
        main_window (QWidget): The main window that the Settings window will interact with.

        Returns:
        None
        """
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 300, 800)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "assets", "Logo_NBackground.png")
        self.setWindowIcon(QIcon(icon_path))

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.init_model_settings_ui()
        self.init_plot_settings_ui()
        self.init_correction_settings_ui()
        self.init_line_settings_ui()

        self.show_model_settings()

    def init_model_settings_ui(self):
        """
        Initializes the model settings user interface.

        Parameters:
        self (SidePanel): The instance of the SidePanel class.

        Returns:
        None
        """
        self.title_section1 = QPushButton("📈 Model Settings")
        self.layout.addWidget(self.title_section1, 0, 0, 1, 3)

        self.model_combo = QComboBox()
        self.model_combo.addItems(["SARIMAX", "ARIMA"])
        self.model_combo.currentTextChanged.connect(self.update_model_parameters)
        self.layout.addWidget(self.model_combo, 1, 0, 1, 3)

        self.p_range_label = QLabel("p_range :")
        self.layout.addWidget(self.p_range_label, 2, 0)
        self.p_range_input = QLineEdit("0,2")
        self.layout.addWidget(self.p_range_input, 2, 1, 1, 2)

        self.d_range_label = QLabel("d_range :")
        self.layout.addWidget(self.d_range_label, 3, 0)
        self.d_range_input = QLineEdit("0,2")
        self.layout.addWidget(self.d_range_input, 3, 1, 1, 2)

        self.q_range_label = QLabel("q_range :")
        self.layout.addWidget(self.q_range_label, 4, 0)
        self.q_range_input = QLineEdit("0,2")
        self.layout.addWidget(self.q_range_input, 4, 1, 1, 2)

        self.seasonal_period_label = QLabel("Seasonality :")
        self.layout.addWidget(self.seasonal_period_label, 5, 0)
        self.seasonal_period_input = QLineEdit("12")
        self.layout.addWidget(self.seasonal_period_input, 5, 1, 1, 2)

        self.enable_seasonality_checkbox = QCheckBox("Enable Seasonality")
        self.enable_seasonality_checkbox.setChecked(True)
        self.layout.addWidget(self.enable_seasonality_checkbox, 6, 0, 1, 3)

        self.forecast_until_label = QLabel("Forecast Year:")
        self.layout.addWidget(self.forecast_until_label, 7, 0)
        self.forecast_until_input = QLineEdit("2100")
        self.layout.addWidget(self.forecast_until_input, 7, 1, 1, 2)
        
        self.sigma_label = QLabel("Sigma for Confidence Interval:")
        self.layout.addWidget(self.sigma_label, 8, 0)
        self.sigma_input = QLineEdit("1.96")
        self.layout.addWidget(self.sigma_input, 8, 1, 1, 2)

        self.replace_negative_forecast_checkbox = QCheckBox("No Negative Values")
        self.layout.addWidget(self.replace_negative_forecast_checkbox, 9, 0, 1, 3)

        self.show_confidence_interval_checkbox = QCheckBox("Show Confidence Interval")
        self.layout.addWidget(self.show_confidence_interval_checkbox, 10, 0, 1, 3)

        self.apply_button = QPushButton("Apply Settings")
        self.apply_button.clicked.connect(self.apply_model)
        self.layout.addWidget(self.apply_button, 11, 0, 1, 3)

    def init_plot_settings_ui(self):
        """
        Initializes the UI elements for plot settings in the side panel window.

        Parameters:
        self (SidePanelWindow): The instance of the side panel window.

        Returns:
        None
        """  
        self.title_section2 = QPushButton("📊 Plot Settings")
        self.title_section2.setVisible(False)
        self.layout.addWidget(self.title_section2, 0, 0, 1, 3)

        self.x_axis_label = QLabel("X-axis :")
        self.x_axis_label.setVisible(False)
        self.layout.addWidget(self.x_axis_label, 1, 0)
        self.x_axis_input = QLineEdit("0,2100")
        self.x_axis_input.setVisible(False)
        self.layout.addWidget(self.x_axis_input, 1, 1, 1, 2)

        self.y_axis_label = QLabel("Y-axis :")
        self.y_axis_label.setVisible(False)
        self.layout.addWidget(self.y_axis_label, 2, 0)
        self.y_axis_input = QLineEdit("0,100")
        self.y_axis_input.setVisible(False)
        self.layout.addWidget(self.y_axis_input, 2, 1, 1, 2)

        self.title_label = QLabel("Chart Title:")
        self.title_label.setVisible(False)
        self.layout.addWidget(self.title_label, 3, 0)
        self.title_input = QLineEdit("Chart Title")
        self.title_input.setVisible(False)
        self.layout.addWidget(self.title_input, 3, 1, 1, 2)

        self.legend_size_label = QLabel("Legend Size:")
        self.legend_size_label.setVisible(False)
        self.layout.addWidget(self.legend_size_label, 4, 0)
        self.legend_size_input = QLineEdit("10")
        self.legend_size_input.setVisible(False)
        self.layout.addWidget(self.legend_size_input, 4, 1, 1, 2)

        self.legend_position_label = QLabel("Legend Position:")
        self.legend_position_label.setVisible(False)
        self.layout.addWidget(self.legend_position_label, 5, 0)
        self.legend_position_combo = QComboBox()
        self.legend_position_combo.addItems(["Upper Left", "Bottom Left", "Upper Right", "Bottom Right"])
        self.legend_position_combo.setVisible(False)
        self.layout.addWidget(self.legend_position_combo, 5, 1, 1, 2)

        self.ylabel_label = QLabel("Y-axis Label:")
        self.ylabel_label.setVisible(False)
        self.layout.addWidget(self.ylabel_label, 6, 0)
        self.ylabel_input = QLineEdit("Y-axis Label")
        self.ylabel_input.setVisible(False)
        self.layout.addWidget(self.ylabel_input, 6, 1, 1, 2)

        self.xlabel_label = QLabel("X-axis Label:")
        self.xlabel_label.setVisible(False)
        self.layout.addWidget(self.xlabel_label, 7, 0)
        self.xlabel_input = QLineEdit("X-axis Label")
        self.xlabel_input.setVisible(False)
        self.layout.addWidget(self.xlabel_input, 7, 1, 1, 2)

        self.ylabel_size_label = QLabel("Y-axis Label Size:")
        self.ylabel_size_label.setVisible(False)
        self.layout.addWidget(self.ylabel_size_label, 8, 0)
        self.ylabel_size_input = QLineEdit("14")
        self.ylabel_size_input.setVisible(False)
        self.layout.addWidget(self.ylabel_size_input, 8, 1, 1, 2)

        self.xlabel_size_label = QLabel("X-axis Label Size:")
        self.xlabel_size_label.setVisible(False)
        self.layout.addWidget(self.xlabel_size_label, 9, 0)
        self.xlabel_size_input = QLineEdit("14")
        self.xlabel_size_input.setVisible(False)
        self.layout.addWidget(self.xlabel_size_input, 9, 1, 1, 2)

        self.apply_plot_button = QPushButton("Apply Plot Settings")
        self.apply_plot_button.clicked.connect(self.apply_plot_settings)
        self.apply_plot_button.setVisible(False)
        self.layout.addWidget(self.apply_plot_button, 10, 0, 1, 3)

    def show_model_settings(self):
        """
        Shows the model settings section in the side panel window.

        Parameters:
        - self: The instance of the class.

        Returns:
        - None
        """
        self.title_section1.setVisible(True)
        self.model_combo.setVisible(True)
        self.p_range_label.setVisible(True)
        self.p_range_input.setVisible(True)
        self.d_range_label.setVisible(True)
        self.d_range_input.setVisible(True)
        self.q_range_label.setVisible(True)
        self.q_range_input.setVisible(True)
        self.seasonal_period_label.setVisible(self.model_combo.currentText() == "SARIMAX")
        self.seasonal_period_input.setVisible(self.model_combo.currentText() == "SARIMAX")
        self.enable_seasonality_checkbox.setVisible(self.model_combo.currentText() == "SARIMAX")
        self.forecast_until_label.setVisible(True)
        self.forecast_until_input.setVisible(True)
        self.replace_negative_forecast_checkbox.setVisible(True)
        self.show_confidence_interval_checkbox.setVisible(True)
        self.target_year_label.setVisible(True)
        self.target_year_input.setVisible(True)
        self.target_value_label.setVisible(True)
        self.target_value_input.setVisible(True)
        self.continuous_correction_checkbox.setVisible(True)
        self.short_correction_checkbox.setVisible(True)
        self.start_correction_checkbox.setVisible(True)
        self.apply_correction_button.setVisible(True)
        self.apply_button.setVisible(True)
        self.start_target_year_label.setVisible(True)
        self.start_target_year_input.setVisible(True)
        self.sigma_label.setVisible(True)
        self.sigma_input.setVisible(True)

        self.title_section2.setVisible(False)
        self.x_axis_label.setVisible(False)
        self.x_axis_input.setVisible(False)
        self.y_axis_label.setVisible(False)
        self.y_axis_input.setVisible(False)
        self.title_label.setVisible(False)
        self.title_input.setVisible(False)
        self.legend_size_label.setVisible(False)
        self.legend_size_input.setVisible(False)
        self.legend_position_label.setVisible(False)
        self.legend_position_combo.setVisible(False)
        self.ylabel_label.setVisible(False)
        self.ylabel_input.setVisible(False)
        self.xlabel_label.setVisible(False)
        self.xlabel_input.setVisible(False)
        self.ylabel_size_label.setVisible(False)
        self.ylabel_size_input.setVisible(False)
        self.xlabel_size_label.setVisible(False)
        self.xlabel_size_input.setVisible(False)
        self.apply_plot_button.setVisible(False)
        self.line_list_label.setVisible(False)
        self.line_list.setVisible(False)
        self.new_line_label.setVisible(False)
        self.line_name_label.setVisible(False)
        self.line_name_input.setVisible(False)
        self.line_value_label.setVisible(False)
        self.line_value_input.setVisible(False)
        self.line_color_label.setVisible(False)
        self.line_color_combo.setVisible(False)
        self.line_type_label.setVisible(False)
        self.line_type_combo.setVisible(False)
        self.add_line_button.setVisible(False)
        self.line_axis_label.setVisible(False)
        self.line_axis_combo.setVisible(False)
        self.line_type_combo.setVisible(False)

    def show_plot_settings(self):
        """
        Shows the plot settings section in the side panel window.

        Parameters:
        - self: The instance of the class.

        Returns:
        - None
        """
        self.title_section1.setVisible(False)
        self.model_combo.setVisible(False)
        self.p_range_label.setVisible(False)
        self.p_range_input.setVisible(False)
        self.d_range_label.setVisible(False)
        self.d_range_input.setVisible(False)
        self.q_range_label.setVisible(False)
        self.q_range_input.setVisible(False)
        self.seasonal_period_label.setVisible(False)
        self.seasonal_period_input.setVisible(False)
        self.enable_seasonality_checkbox.setVisible(False)
        self.forecast_until_label.setVisible(False)
        self.forecast_until_input.setVisible(False)
        self.replace_negative_forecast_checkbox.setVisible(False)
        self.show_confidence_interval_checkbox.setVisible(False)
        self.target_year_label.setVisible(False)
        self.target_year_input.setVisible(False)
        self.target_value_label.setVisible(False)
        self.target_value_input.setVisible(False)
        self.continuous_correction_checkbox.setVisible(False)
        self.short_correction_checkbox.setVisible(False)
        self.start_correction_checkbox.setVisible(False)
        self.apply_correction_button.setVisible(False)
        self.apply_button.setVisible(False)
        self.start_target_year_label.setVisible(False)
        self.start_target_year_input.setVisible(False)
        self.sigma_label.setVisible(False)
        self.sigma_input.setVisible(False)

        self.title_section2.setVisible(True)
        self.x_axis_label.setVisible(True)
        self.x_axis_input.setVisible(True)
        self.y_axis_label.setVisible(True)
        self.y_axis_input.setVisible(True)
        self.title_label.setVisible(True)
        self.title_input.setVisible(True)
        self.legend_size_label.setVisible(True)
        self.legend_size_input.setVisible(True)
        self.legend_position_label.setVisible(True)
        self.legend_position_combo.setVisible(True)
        self.ylabel_label.setVisible(True)
        self.ylabel_input.setVisible(True)
        self.xlabel_label.setVisible(True)
        self.xlabel_input.setVisible(True)
        self.ylabel_size_label.setVisible(True)
        self.ylabel_size_input.setVisible(True)
        self.xlabel_size_label.setVisible(True)
        self.xlabel_size_input.setVisible(True)
        self.apply_plot_button.setVisible(True)
        self.line_list_label.setVisible(True)
        self.line_list.setVisible(True)
        self.new_line_label.setVisible(True)
        self.line_name_label.setVisible(True)
        self.line_name_input.setVisible(True)
        self.line_value_label.setVisible(True)
        self.line_value_input.setVisible(True)
        self.line_color_label.setVisible(True)
        self.line_color_combo.setVisible(True)
        self.line_type_label.setVisible(True)
        self.line_type_combo.setVisible(True)
        self.add_line_button.setVisible(True)
        self.line_axis_label.setVisible(True)
        self.line_axis_combo.setVisible(True)
        self.line_type_combo.setVisible(True)

    def update_model_parameters(self, model_name):
        """
        Updates the visibility of UI elements based on the selected model name.

        Parameters:
        model_name (str): The name of the selected model.

        Returns:
        None
        """
        is_sarimax = model_name == "SARIMAX"
        self.p_range_label.setVisible(True)
        self.p_range_input.setVisible(True)
        self.d_range_label.setVisible(True)
        self.d_range_input.setVisible(True)
        self.q_range_label.setVisible(True)
        self.q_range_input.setVisible(True)
        self.seasonal_period_label.setVisible(is_sarimax)
        self.seasonal_period_input.setVisible(is_sarimax)
        self.enable_seasonality_checkbox.setVisible(is_sarimax)
        self.forecast_until_label.setVisible(True)
        self.forecast_until_input.setVisible(True)
        self.replace_negative_forecast_checkbox.setVisible(True)

    def apply_model(self):
        """
        Applies the selected model to the data.

        Parameters:
        - model_name (str): The name of the selected model. It can be either "SARIMAX" or "ARIMA".

        Returns:
        - None

        Raises:
        - ValueError: If an invalid model name is provided.
        """
        model_name = self.model_combo.currentText()
        if model_name == "SARIMAX":
            self.apply_sarimax()
        elif model_name == "ARIMA":
            self.apply_arima()

    def apply_sarimax(self):
        """
        Applies the SARIMAX model settings and triggers the SARIMAX model run in the main window.

        Parameters:
        - p_range (list): The range of p values for the SARIMAX model.
        - d_range (list): The range of d values for the SARIMAX model.
        - q_range (list): The range of q values for the SARIMAX model.
        - seasonal_period (int): The seasonal period for the SARIMAX model.
        - enable_seasonality (bool): A flag indicating whether to enable seasonality in the SARIMAX model.

        Returns:
        - None
        """     
        p_range = self.get_range(self.p_range_input.text(), [0, 2])
        d_range = self.get_range(self.d_range_input.text(), [0, 2])
        q_range = self.get_range(self.q_range_input.text(), [0, 2])
        
        seasonal_period = int(self.seasonal_period_input.text()) if self.seasonal_period_input.text() else 11
        enable_seasonality = self.enable_seasonality_checkbox.isChecked()

        forecast_until_year = int(self.forecast_until_input.text()) if self.forecast_until_input.text() else 2100
        self.main_window.forecast_until_year = forecast_until_year

        self.main_window.replace_negative_forecast = self.replace_negative_forecast_checkbox.isChecked()

        self.main_window.run_sarimax(p_range, d_range, q_range, seasonal_period, enable_seasonality)

    def apply_arima(self):
        """
        Applies the ARIMA model settings and triggers the ARIMA model run in the main window.

        Parameters:
        - p_range (list): The range of p values for the ARIMA model.
        - d_range (list): The range of d values for the ARIMA model.
        - q_range (list): The range of q values for the ARIMA model.

        Returns:
        - None
        """      
        p_range = self.get_range(self.p_range_input.text(), [0, 2])
        d_range = self.get_range(self.d_range_input.text(), [0, 2])
        q_range = self.get_range(self.q_range_input.text(), [0, 2])

        forecast_until_year = int(self.forecast_until_input.text()) if self.forecast_until_input.text() else 2100
        self.main_window.forecast_until_year = forecast_until_year

        self.main_window.replace_negative_forecast = self.replace_negative_forecast_checkbox.isChecked()

        self.main_window.run_arima(p_range, d_range, q_range)

    def get_range(self, text, default):
        """
        Parses a comma-separated string to a list of two integers or returns a default value.

        Parameters:
        text (str): The comma-separated string to be parsed.
        default (list): The default value to return if parsing fails.

        Returns:
        list: The parsed range as a list of two integers or the default value.
        """
        if text:
            try:
                values = list(map(int, text.split(',')))
                if len(values) == 2:
                    return values
                else:
                    return default
            except ValueError:
                return default
        else:
            return default

    def apply_plot_settings(self):
        """
        Applies the plot settings to the active figure in the main window.

        Parameters:
        - x_axis_input (QLineEdit): The input field for the x-axis range.
        - y_axis_input (QLineEdit): The input field for the y-axis range.
        - title_input (QLineEdit): The input field for the plot title.
        - legend_size_input (QLineEdit): The input field for the legend size.
        - legend_position_combo (QComboBox): The combo box for the legend position.
        - xlabel_input (QLineEdit): The input field for the x-axis label.
        - ylabel_input (QLineEdit): The input field for the y-axis label.
        - xlabel_size_input (QLineEdit): The input field for the x-axis label size.
        - ylabel_size_input (QLineEdit): The input field for the y-axis label size.

        Returns:
        - None
        """       
        x_range = self.get_range(self.x_axis_input.text(), None)
        y_range = self.get_range(self.y_axis_input.text(), None)
        title = self.title_input.text()
        legend_size = int(self.legend_size_input.text()) if self.legend_size_input.text() else None
        legend_position = self.legend_position_combo.currentText().replace(" ", "").lower()
        legend_position = self.map_legend_position(legend_position)
        xlabel = self.xlabel_input.text()
        ylabel = self.ylabel_input.text()
        xlabel_size = int(self.xlabel_size_input.text()) if self.xlabel_size_input.text() else None
        ylabel_size = int(self.ylabel_size_input.text()) if self.ylabel_size_input.text() else None

        if self.main_window.canvas.figure.axes:
            ax = self.main_window.canvas.figure.axes[0]
            if x_range and len(x_range) == 2:
                ax.set_xlim(x_range)
            if y_range and len(y_range) == 2:
                ax.set_ylim(y_range)
            if title:
                ax.set_title(title, fontsize=16, fontweight='bold')
            if legend_size:
                ax.legend(fontsize=legend_size, loc=legend_position)
            if xlabel:
                ax.set_xlabel(xlabel, fontsize=xlabel_size if xlabel_size else 14)
            if ylabel:
                ax.set_ylabel(ylabel, fontsize=ylabel_size if ylabel_size else 14)
            if xlabel_size and not xlabel:
                ax.xaxis.label.set_size(xlabel_size)
            if ylabel_size and not ylabel:
                ax.yaxis.label.set_size(ylabel_size)
            self.main_window.canvas.draw()

        for index in range(self.line_list.count()):
            item = self.line_list.item(index)
            line_name = item.text()
            for line in self.main_window.active_lines:
                if line['name'] == line_name:
                    line['active'] = item.checkState() == Qt.Checked

        self.clear_lines()
        self.draw_lines()
        self.update_legend()

    def init_correction_settings_ui(self):
        """
        Initializes the UI elements for the correction settings section in the side panel window.

        Parameters:
        - self: The instance of the class.

        Returns:
        - None
        """
        self.target_year_label = QLabel("Target Year:")
        self.layout.addWidget(self.target_year_label, 12, 0)
        self.target_year_input = QLineEdit("")
        self.layout.addWidget(self.target_year_input, 12, 1, 1, 2)

        self.start_target_year_label = QLabel("Start Target Year:")
        self.layout.addWidget(self.start_target_year_label, 13, 0)
        self.start_target_year_input = QLineEdit("")
        self.layout.addWidget(self.start_target_year_input, 13, 1, 1, 2)

        self.target_value_label = QLabel("Target Value:")
        self.layout.addWidget(self.target_value_label, 14, 0)
        self.target_value_input = QLineEdit("")
        self.layout.addWidget(self.target_value_input, 14, 1, 1, 2)

        self.continuous_correction_checkbox = QCheckBox("Continuous Correction")
        self.layout.addWidget(self.continuous_correction_checkbox, 15, 0, 1, 3)

        self.short_correction_checkbox = QCheckBox("Short Correction")
        self.layout.addWidget(self.short_correction_checkbox, 16, 0, 1, 3)

        self.start_correction_checkbox = QCheckBox("Start Correction")
        self.layout.addWidget(self.start_correction_checkbox, 17, 0, 1, 3)

        self.apply_correction_button = QPushButton("Apply Correction")
        self.apply_correction_button.clicked.connect(self.main_window.apply_forecast_corrections)
        self.layout.addWidget(self.apply_correction_button, 18, 0, 1, 3)

    def init_line_settings_ui(self):
        """
        Initializes the UI elements for the line settings section in the side panel window.

        Parameters:
        - self: The instance of the class.

        Returns:
        - None
        """       
        self.line_list_label = QLabel("Active Lines:")
        self.layout.addWidget(self.line_list_label, 17, 0)
        self.line_list = QListWidget()
        self.update_line_list()
        self.layout.addWidget(self.line_list, 18, 0, 1, 3)

        self.new_line_label = QLabel("Add New Line:")
        self.layout.addWidget(self.new_line_label, 19, 0)
        self.line_name_label = QLabel("Name:")
        self.layout.addWidget(self.line_name_label, 20, 0)
        self.line_name_input = QLineEdit()
        self.layout.addWidget(self.line_name_input, 20, 1, 1, 2)

        self.line_value_label = QLabel("Value:")
        self.layout.addWidget(self.line_value_label, 21, 0)
        self.line_value_input = QLineEdit()
        self.layout.addWidget(self.line_value_input, 21, 1, 1, 2)

        self.line_color_label = QLabel("Color:")
        self.layout.addWidget(self.line_color_label, 22, 0)
        self.line_color_combo = QComboBox()
        self.line_color_combo.addItems(["red", "blue", "green", "yellow", "black"])
        self.layout.addWidget(self.line_color_combo, 22, 1, 1, 2)

        self.line_axis_label = QLabel("Axis:")
        self.layout.addWidget(self.line_axis_label, 23, 0)
        self.line_axis_combo = QComboBox()
        self.line_axis_combo.addItems(["x-axis", "y-axis"])
        self.layout.addWidget(self.line_axis_combo, 23, 1, 1, 2)

        self.line_type_label = QLabel("Type:")
        self.layout.addWidget(self.line_type_label, 24, 0)
        self.line_type_combo = QComboBox()
        self.line_type_combo.addItems(["solid", "dashed", "dotted"])
        self.layout.addWidget(self.line_type_combo, 24, 1, 1, 2)

        self.add_line_button = QPushButton("Add Line")
        self.add_line_button.clicked.connect(self.add_line)
        self.layout.addWidget(self.add_line_button, 25, 0, 1, 3)

    def update_line_list(self):
        """
        Updates the line list in the side panel window.

        This function clears the current line list and adds new items to it. Each item represents a line in the
        active lines list of the main window. The item's text is set to the name of the line, and its check state is
        set based on whether the line is active or not.

        Parameters:
        - self: The instance of the class.

        Returns:
        - None
        """
        self.line_list.clear()
        for line in self.main_window.active_lines:
            item = QListWidgetItem(line['name'])
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if line['active'] else Qt.Unchecked)
            self.line_list.addItem(item)

    def add_line(self):
        """
        Adds a new line to the active lines list in the main window.

        Parameters:
        - name (str): The name of the line.
        - value (str): The value of the line.
        - color (str): The color of the line.
        - line_type (str): The type of the line (solid, dashed, dotted).
        - axis (str): The axis on which the line will be drawn (x-axis, y-axis).

        Returns:
        - None

        Raises:
        - ValueError: If the value provided for the line is not a valid float.
        """
        name = self.line_name_input.text()
        value = self.line_value_input.text()
        color = self.line_color_combo.currentText()
        line_type = self.line_type_combo.currentText()
        axis = self.line_axis_combo.currentText()

        try:
            value = float(value)
            line = {'name': name, 'value': value, 'color': color, 'type': line_type, 'axis': axis, 'active': True}
            self.main_window.active_lines.append(line)
            self.main_window.console.append(f"Added line: {line}")
            self.update_line_list()
        except ValueError:
            self.main_window.console.append("Invalid value for the line.")

    def draw_lines(self):
        """
        Draws lines on the active figure based on the active lines in the main window.

        The function iterates through the active lines in the main window. For each active line, it determines the line style
        based on the line type. It then draws a vertical or horizontal line on the x-axis or y-axis, respectively, using the line's
        value, color, and label. The line is made visible on the figure. Finally, the figure is drawn.

        Parameters:
        None

        Returns:
        None
        """
        ax = self.main_window.canvas.figure.gca()
        for line in self.main_window.active_lines:
            if line['active']:
                linestyle = '-' if line['type'] == 'solid' else '--' if line['type'] == 'dashed' else ':'
                if line['axis'] == 'x-axis':
                    ax.axvline(x=line['value'], color=line['color'], linestyle=linestyle, label=line['name'])
                else:
                    ax.axhline(y=line['value'], color=line['color'], linestyle=linestyle, label=line['name'])
                ax.lines[-1].set_visible(True)
        self.main_window.canvas.draw()

    def clear_lines(self):
        """
        Clears lines from the active figure based on the active lines in the main window.

        This function iterates through the lines in the active figure. For each line, it checks if the line's label is in the list of active line names.
        If the label is found, the line's visibility is set to False. Finally, the figure is drawn to reflect the changes.

        Parameters:
        None

        Returns:
        None
        """
        ax = self.main_window.canvas.figure.gca()
        for line in ax.get_lines():
            if line.get_label() in [l['name'] for l in self.main_window.active_lines]:
                line.set_visible(False)
        self.main_window.canvas.draw()
        
    def map_legend_position(self, position):
        """
        Maps a given legend position to a standardized format.

        Parameters:
        position (str): The input legend position.

        Returns:
        str: The standardized legend position. If the input position is not found in the mapping, it returns "upper right".
        """
        position_mapping = {
            "upperleft": "upper left",
            "bottomleft": "lower left",
            "upperright": "upper right",
            "bottomright": "lower right"
        }
        return position_mapping.get(position, "upper right")

    def update_legend(self):
        """
        Updates the legend on the active figure based on the visible lines.

        Retrieves the legend size and position from the UI elements.
        Retrieves the handles and labels of the legend from the active figure.
        Filters the visible handles and labels based on their visibility.
        Updates the legend with the filtered handles and labels, using the specified legend size and position.
        If no visible handles and labels are found, removes the legend from the figure.
        Draws the updated figure.

        Parameters:
        None

        Returns:
        None
        """
        legend_size = int(self.legend_size_input.text()) if self.legend_size_input.text() else 10
        legend_position = self.legend_position_combo.currentText().replace(" ", "").lower()
        legend_position = self.map_legend_position(legend_position)

        ax = self.main_window.canvas.figure.gca()
        handles, labels = ax.get_legend_handles_labels()
        visible_handles_labels = []
        for handle, label in zip(handles, labels):
            if isinstance(handle, matplotlib.container.BarContainer):
                if any(bar.get_visible() for bar in handle.get_children()):
                    visible_handles_labels.append((handle, label))
            else:
                if handle.get_visible():
                    visible_handles_labels.append((handle, label))

        if visible_handles_labels:
            handles, labels = zip(*visible_handles_labels)
            ax.legend(handles, labels, fontsize=legend_size, loc=legend_position)
        else:
            ax.legend().remove()
        self.main_window.canvas.draw()
