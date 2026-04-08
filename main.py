import sys, webbrowser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox, QScrollArea
)
from PyQt5.QtGui import QPixmap, QImage, QFont, QColor
from PyQt5.QtCore import Qt
from rdkit import Chem
from rdkit.Chem import Draw


# --- DATABASE: Elements + Compounds (Expandable) ---
CHEM_DATA = {
    # === Elements (partial list for brevity) ===
    "hydrogen": {"symbol": "H", "atomic_number": 1, "mass": 1.008, "phase": "Gas", "type": "Nonmetal", "group": 1, "info": "Lightest and most abundant element in the universe.", "smiles": "[H][H]", "wiki": "https://en.wikipedia.org/wiki/Hydrogen"},
    "helium": {"symbol": "He", "atomic_number": 2, "mass": 4.0026, "phase": "Gas", "type": "Noble Gas", "group": 18, "info": "Inert gas used in balloons and cryogenics.", "smiles": "[He]", "wiki": "https://en.wikipedia.org/wiki/Helium"},
    "lithium": {"symbol": "Li", "atomic_number": 3, "mass": 6.94, "phase": "Solid", "type": "Alkali Metal", "group": 1, "info": "Soft, silvery metal used in batteries.", "smiles": "[Li]", "wiki": "https://en.wikipedia.org/wiki/Lithium"},
    "carbon": {"symbol": "C", "atomic_number": 6, "mass": 12.011, "phase": "Solid", "type": "Nonmetal", "group": 14, "info": "Basis of organic chemistry and all known life.", "smiles": "C", "wiki": "https://en.wikipedia.org/wiki/Carbon"},
    "nitrogen": {"symbol": "N", "atomic_number": 7, "mass": 14.007, "phase": "Gas", "type": "Nonmetal", "group": 15, "info": "Makes up 78% of Earth’s atmosphere.", "smiles": "N#N", "wiki": "https://en.wikipedia.org/wiki/Nitrogen"},
    "oxygen": {"symbol": "O", "atomic_number": 8, "mass": 15.999, "phase": "Gas", "type": "Nonmetal", "group": 16, "info": "Essential for life; supports combustion.", "smiles": "O=O", "wiki": "https://en.wikipedia.org/wiki/Oxygen"},
    "sodium": {"symbol": "Na", "atomic_number": 11, "mass": 22.990, "phase": "Solid", "type": "Alkali Metal", "group": 1, "info": "Reacts violently with water; forms salts.", "smiles": "[Na]", "wiki": "https://en.wikipedia.org/wiki/Sodium"},
    "magnesium": {"symbol": "Mg", "atomic_number": 12, "mass": 24.305, "phase": "Solid", "type": "Alkaline Earth Metal", "group": 2, "info": "Essential nutrient and used in alloys.", "smiles": "[Mg]", "wiki": "https://en.wikipedia.org/wiki/Magnesium"},
    "aluminum": {"symbol": "Al", "atomic_number": 13, "mass": 26.982, "phase": "Solid", "type": "Metal", "group": 13, "info": "Lightweight metal used in airplanes and cans.", "smiles": "[Al]", "wiki": "https://en.wikipedia.org/wiki/Aluminium"},
    "silicon": {"symbol": "Si", "atomic_number": 14, "mass": 28.085, "phase": "Solid", "type": "Metalloid", "group": 14, "info": "Semiconductor used in electronics.", "smiles": "[Si]", "wiki": "https://en.wikipedia.org/wiki/Silicon"},
    "phosphorus": {"symbol": "P", "atomic_number": 15, "mass": 30.974, "phase": "Solid", "type": "Nonmetal", "group": 15, "info": "Key element in DNA, fertilizers, and matches.", "smiles": "P", "wiki": "https://en.wikipedia.org/wiki/Phosphorus"},
    "sulfur": {"symbol": "S", "atomic_number": 16, "mass": 32.06, "phase": "Solid", "type": "Nonmetal", "group": 16, "info": "Yellow solid used in rubber and fertilizers.", "smiles": "S", "wiki": "https://en.wikipedia.org/wiki/Sulfur"},
    "chlorine": {"symbol": "Cl", "atomic_number": 17, "mass": 35.45, "phase": "Gas", "type": "Halogen", "group": 17, "info": "Used in disinfectants and table salt.", "smiles": "Cl-Cl", "wiki": "https://en.wikipedia.org/wiki/Chlorine"},
    "iron": {"symbol": "Fe", "atomic_number": 26, "mass": 55.845, "phase": "Solid", "type": "Metal", "group": 8, "info": "Essential in blood (hemoglobin); used in steel.", "smiles": "[Fe]", "wiki": "https://en.wikipedia.org/wiki/Iron"},
    "copper": {"symbol": "Cu", "atomic_number": 29, "mass": 63.546, "phase": "Solid", "type": "Metal", "group": 11, "info": "Excellent electrical conductor.", "smiles": "[Cu]", "wiki": "https://en.wikipedia.org/wiki/Copper"},
    "silver": {"symbol": "Ag", "atomic_number": 47, "mass": 107.87, "phase": "Solid", "type": "Metal", "group": 11, "info": "Precious metal with high conductivity.", "smiles": "[Ag]", "wiki": "https://en.wikipedia.org/wiki/Silver"},
    "gold": {"symbol": "Au", "atomic_number": 79, "mass": 196.97, "phase": "Solid", "type": "Metal", "group": 11, "info": "Precious yellow metal used in jewelry.", "smiles": "[Au]", "wiki": "https://en.wikipedia.org/wiki/Gold"},
    "mercury": {"symbol": "Hg", "atomic_number": 80, "mass": 200.59, "phase": "Liquid", "type": "Metal", "group": 12, "info": "Liquid metal at room temperature.", "smiles": "[Hg]", "wiki": "https://en.wikipedia.org/wiki/Mercury_(element)"},

    # === Compounds ===
    "water": {"formula": "H₂O", "mass": 18.015, "phase": "Liquid", "type": "Compound", "info": "Universal solvent essential for life.", "smiles": "O", "wiki": "https://en.wikipedia.org/wiki/Water"},
    "carbon dioxide": {"formula": "CO₂", "mass": 44.01, "phase": "Gas", "type": "Compound", "info": "Produced by respiration and combustion.", "smiles": "O=C=O", "wiki": "https://en.wikipedia.org/wiki/Carbon_dioxide"},
    "methane": {"formula": "CH₄", "mass": 16.04, "phase": "Gas", "type": "Compound", "info": "Main component of natural gas.", "smiles": "C", "wiki": "https://en.wikipedia.org/wiki/Methane"},
    "ammonia": {"formula": "NH₃", "mass": 17.03, "phase": "Gas", "type": "Compound", "info": "Used in fertilizers and cleaning.", "smiles": "N", "wiki": "https://en.wikipedia.org/wiki/Ammonia"},
    "ethanol": {"formula": "C₂H₆O", "mass": 46.07, "phase": "Liquid", "type": "Compound", "info": "Alcohol found in beverages and fuels.", "smiles": "CCO", "wiki": "https://en.wikipedia.org/wiki/Ethanol"},
    "glucose": {"formula": "C₆H₁₂O₆", "mass": 180.16, "phase": "Solid", "type": "Compound", "info": "Primary sugar used by living cells for energy.", "smiles": "C(C1C(C(C(C(O1)O)O)O)O)O", "wiki": "https://en.wikipedia.org/wiki/Glucose"},
    "salt": {"formula": "NaCl", "mass": 58.44, "phase": "Solid", "type": "Ionic Compound", "info": "Sodium chloride, essential for life.", "smiles": "[Na+].[Cl-]", "wiki": "https://en.wikipedia.org/wiki/Sodium_chloride"},
    "baking soda": {"formula": "NaHCO₃", "mass": 84.01, "phase": "Solid", "type": "Compound", "info": "Used in baking and as an antacid.", "smiles": "[Na+].O=C([O-])O[H]", "wiki": "https://en.wikipedia.org/wiki/Sodium_bicarbonate"},
    "vinegar": {"formula": "CH₃COOH", "mass": 60.05, "phase": "Liquid", "type": "Acid", "info": "Weak acid used in cooking and cleaning.", "smiles": "CC(=O)O", "wiki": "https://en.wikipedia.org/wiki/Acetic_acid"},
}


# --- MAIN APP CLASS ---
class ChemExplorer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧪 ChemExplorer Ultimate")
        self.resize(850, 700)
        self.setStyleSheet("background-color: #F4F6F7;")

        title = QLabel("🧪 ChemExplorer Ultimate — Elements & Compounds")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("background-color: #2471A3; color: white; padding: 10px;")

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search element or compound (e.g., Oxygen, H₂O, NaCl)...")
        self.search_box.setFont(QFont("Segoe UI", 12))
        self.search_box.setAlignment(Qt.AlignCenter)

        self.dropdown = QComboBox()
        self.dropdown.addItem("Select...")
        self.dropdown.addItems(sorted([k.capitalize() for k in CHEM_DATA.keys()]))
        self.dropdown.currentIndexChanged.connect(self.show_info)

        self.info_label = QLabel("")
        self.info_label.setWordWrap(True)
        self.info_label.setFont(QFont("Segoe UI", 12))
        self.info_label.setAlignment(Qt.AlignTop)
        self.info_label.setStyleSheet("padding: 10px; color: #1A5276;")

        self.image_label = QLabel()
        self.image_label.setFixedSize(350, 350)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed #AED6F1; background-color: #EBF5FB;")

        # Buttons
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.show_info)
        learn_btn = QPushButton("Learn More (Wikipedia)")
        learn_btn.clicked.connect(self.open_wiki)
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_display)
        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(lambda: QApplication.quit())

        for b in (search_btn, learn_btn, clear_btn, exit_btn):
            b.setFont(QFont("Segoe UI", 10))
            b.setStyleSheet("QPushButton { background-color:#2E86C1; color:white; border-radius:5px; padding:6px 10px; } QPushButton:hover { background-color:#1B4F72; }")

        button_layout = QHBoxLayout()
        for b in (search_btn, learn_btn, clear_btn, exit_btn):
            button_layout.addWidget(b)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.search_box)
        layout.addWidget(self.dropdown)
        layout.addLayout(button_layout)
        layout.addWidget(self.info_label)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        self.current_item = None

    def show_info(self):
        query = self.search_box.text().strip().lower()
        if not query or query == "select...":
            query = self.dropdown.currentText().lower()

        if query not in CHEM_DATA:
            QMessageBox.information(self, "Not Found", f"No data for '{query}'.")
            return

        data = CHEM_DATA[query]
        self.current_item = data

        html = f"<h2>{query.capitalize()}</h2>"
        if "atomic_number" in data:
            html += f"<b>Symbol:</b> {data['symbol']}<br>"
            html += f"<b>Atomic Number:</b> {data['atomic_number']}<br>"
        else:
            html += f"<b>Formula:</b> {data['formula']}<br>"

        html += f"<b>Mass:</b> {data['mass']} g/mol<br>"
        html += f"<b>Phase:</b> <span style='color:{self.phase_color(data['phase'])}'>{data['phase']}</span><br>"
        html += f"<b>Type:</b> {data['type']}<br>"

        if "group" in data:
            html += f"<b>Group:</b> {data['group']}<br>"

        html += f"<p>{data['info']}</p>"
        self.info_label.setText(html)

        if data.get("smiles"):
            mol = Chem.MolFromSmiles(data["smiles"])
            if mol:
                img = Draw.MolToImage(mol, size=(350, 350))
                qim = QImage(img.tobytes("raw", "RGB"), img.size[0], img.size[1], QImage.Format_RGB888)
                self.image_label.setPixmap(QPixmap.fromImage(qim))

    def phase_color(self, phase):
        return {"Gas": "#E74C3C", "Solid": "#1F618D", "Liquid": "#28B463"}.get(phase, "black")

    def open_wiki(self):
        if self.current_item and "wiki" in self.current_item:
            webbrowser.open(self.current_item["wiki"])
        else:
            QMessageBox.information(self, "Info", "Select a chemical first!")

    def clear_display(self):
        self.search_box.clear()
        self.dropdown.setCurrentIndex(0)
        self.info_label.setText("")
        self.image_label.clear()
        self.current_item = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ChemExplorer()
    win.show()
    sys.exit(app.exec_())
