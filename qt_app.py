import sys
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QFileDialog, QWidget, QMessageBox, QInputDialog
)
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Define normalized curves
curves = {
    "ELE": [0.13, 0.19, 0.29, 0.58, 1.16, 1.62, 2.10, 2.19, 2.30, 2.39, 2.49, 2.51],
    "ISM": [0.35, 0.54, 0.79, 1.44, 1.67, 1.76, 2.29, 2.73, 3.75, 4.95, 5.54, 6.14],
}
normalized_curves = {
    name: [p / sum(values) for p in values] for name, values in curves.items()
}

# Helper function to scale a curve
def scale_curve(percentages, original_weeks, new_weeks):
    original_x = np.linspace(0, 1, original_weeks)
    new_x = np.linspace(0, 1, new_weeks)
    interpolation_function = interp1d(original_x, percentages, kind="linear")
    scaled_curve = interpolation_function(new_x)
    return scaled_curve / np.sum(scaled_curve)

# Function to redistribute hours
def redistribute_hours(total_hours, num_weeks, curve_type, custom_curve=None, percentages=None, original_weeks=None):
    if curve_type in normalized_curves:
        curve = scale_curve(normalized_curves[curve_type], len(curves[curve_type]), num_weeks)
    elif curve_type == "Linear":
        curve = np.ones(num_weeks) / num_weeks
    elif curve_type == "Bell":
        curve = np.exp(-0.5 * (np.linspace(-2, 2, num_weeks) ** 2))
        curve /= np.sum(curve)  # Normalize
    elif curve_type == "Custom" and custom_curve is not None:
        curve = np.array(custom_curve) / np.sum(custom_curve)  # Normalize
    elif curve_type == "Fitted" and percentages is not None and original_weeks is not None:
        curve = scale_curve(percentages, original_weeks, num_weeks)
    else:
        raise ValueError("Invalid curve type or missing input for selected option.")

    # Redistribute the hours
    redistributed_hours = total_hours * curve
    weeks = [f"Week {i+1}" for i in range(num_weeks)]
    return pd.DataFrame({"Week": weeks, "Redistributed Hours": redistributed_hours, "Curve Value": curve})

# Main Application Window
class BudgetRedistributionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Redistribution Tool")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Inputs
        layout.addWidget(QLabel("Total Hours Budget:"))
        self.total_hours_input = QLineEdit()
        self.total_hours_input.setText("1000")
        layout.addWidget(self.total_hours_input)

        layout.addWidget(QLabel("Number of Weeks:"))
        self.num_weeks_input = QLineEdit()
        self.num_weeks_input.setText("50")
        layout.addWidget(self.num_weeks_input)

        layout.addWidget(QLabel("Curve Type:"))
        self.curve_selector = QComboBox()
        self.curve_selector.addItems(["ELE", "ISM", "Linear", "Bell", "Custom", "Fitted"])
        layout.addWidget(self.curve_selector)

        # Buttons
        button_layout = QHBoxLayout()
        self.redistribute_button = QPushButton("Redistribute Hours")
        self.redistribute_button.clicked.connect(self.redistribute)
        button_layout.addWidget(self.redistribute_button)

        self.save_button = QPushButton("Save to Excel")
        self.save_button.setDisabled(True)
        self.save_button.clicked.connect(self.save_to_excel)
        button_layout.addWidget(self.save_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def redistribute(self):
        try:
            total_hours = float(self.total_hours_input.text())
            num_weeks = int(self.num_weeks_input.text())
            curve_type = self.curve_selector.currentText()

            if curve_type in normalized_curves:
                curve = normalized_curves[curve_type]
            elif curve_type == "Linear":
                curve = np.ones(num_weeks) / num_weeks
            elif curve_type == "Bell":
                curve = np.exp(-0.5 * (np.linspace(-2, 2, num_weeks) ** 2))
                curve /= np.sum(curve)
            elif curve_type == "Custom":
                custom_input, ok = self.get_user_input("Custom Curve", f"Enter {num_weeks} values (comma-separated):")
                if not ok or not custom_input:
                    QMessageBox.warning(self, "Error", "Invalid custom input.")
                    return
                custom_curve = [float(x) for x in custom_input.split(",")]
                if len(custom_curve) != num_weeks:
                    QMessageBox.warning(self, "Error", f"Enter exactly {num_weeks} values.")
                    return
                curve = np.array(custom_curve) / np.sum(custom_curve)
            elif curve_type == "Fitted":
                original_weeks_input, ok = self.get_user_input("Original Weeks", "Enter the number of weeks in the original curve:")
                if not ok or not original_weeks_input.isdigit():
                    QMessageBox.warning(self, "Error", "Invalid input for original weeks.")
                    return
                original_weeks = int(original_weeks_input)

                percentages_input, ok = self.get_user_input(
                    "Fitted Curve", f"Enter {original_weeks} percentages (comma-separated):"
                )
                if not ok or not percentages_input:
                    QMessageBox.warning(self, "Error", "Invalid input for fitted curve.")
                    return
                percentages = [float(x) for x in percentages_input.split(",")]
                if len(percentages) != original_weeks:
                    QMessageBox.warning(self, "Error", f"Enter exactly {original_weeks} percentages.")
                    return
                curve = scale_curve(percentages, original_weeks, num_weeks)
            else:
                QMessageBox.critical(self, "Error", "Invalid curve type selected!")
                return

            # Redistribute hours
            self.results = redistribute_hours(total_hours, num_weeks, curve_type, custom_curve, percentages, original_weeks)
            QMessageBox.information(self, "Success", "Redistribution complete!")
            self.plot_curve()
            self.save_button.setDisabled(False)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def plot_curve(self):
        if hasattr(self, "results"):
            df = self.results
            plt.figure(figsize=(8, 5))
            plt.plot(df["Week"], df["Curve Value"], label="Curve", marker="o")
            plt.xticks(rotation=45)
            plt.xlabel("Weeks")
            plt.ylabel("Redistributed Fraction")
            plt.title("Redistributed Curve")
            plt.grid(True)
            plt.show()

    def save_to_excel(self):
        if hasattr(self, "results"):
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save File", "", "Excel Files (*.xlsx)", options=options
            )
            if file_path:
                self.results.to_excel(file_path, index=False)
                QMessageBox.information(self, "Success", f"File saved to {file_path}")

    def get_user_input(self, title, label):
        """Helper method to show a dialog for user input."""
        input_text, ok = QInputDialog.getText(self, title, label)
        return input_text, ok


# Main application loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BudgetRedistributionApp()
    window.show()
    sys.exit(app.exec_())