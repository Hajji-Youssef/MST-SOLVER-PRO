import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QPushButton, QLabel, QLineEdit, QFrame)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

class KruskalMST:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def get_mst(self):
        result = []
        i, e = 0, 0
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []; rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        
        while e < self.V - 1 and i < len(self.graph):
            if i >= len(self.graph): break
            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
        return result

class StyledMSTApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MST Solver Pro')
        self.setMinimumSize(500, 650)
        
        # Modern Dark Theme Stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', Arial;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
                color: #89b4fa;
                margin-bottom: 5px;
            }
            QTextEdit, QLineEdit {
                background-color: #313244;
                border: 2px solid #45475a;
                border-radius: 8px;
                padding: 8px;
                color: #cdd6f4;
            }
            QTextEdit:focus, QLineEdit:focus {
                border: 2px solid #89b4fa;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
            QPushButton#clearBtn {
                background-color: #f38ba8;
            }
            QPushButton#clearBtn:hover {
                background-color: #eba0ac;
            }
            QFrame#line {
                background-color: #45475a;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        # Header
        header = QLabel("Minimum Spanning Tree Finder")
        header.setStyleSheet("font-size: 24px; color: #f5c2e7; margin-bottom: 10px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)

        # Node Input Section
        main_layout.addWidget(QLabel("Step 1: Number of Nodes"))
        self.num_nodes_input = QLineEdit()
        self.num_nodes_input.setPlaceholderText("Enter integer (e.g., 5)")
        main_layout.addWidget(self.num_nodes_input)

        # Edge Input Section
        main_layout.addWidget(QLabel("Step 2: Enter Edges (Source Dest Weight)"))
        self.input_area = QTextEdit()
        self.input_area.setPlaceholderText("Example:\n0 1 5\n1 2 10\n0 2 2")
        main_layout.addWidget(self.input_area)

        # Buttons
        btn_layout = QHBoxLayout()
        self.calc_btn = QPushButton("Calculate MST")
        self.calc_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.calc_btn.clicked.connect(self.calculate_mst)
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("clearBtn")
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_fields)
        
        btn_layout.addWidget(self.calc_btn)
        btn_layout.addWidget(self.clear_btn)
        main_layout.addLayout(btn_layout)

        # Divider Line
        line = QFrame()
        line.setObjectName("line")
        line.setFrameShape(QFrame.Shape.HLine)
        main_layout.addWidget(line)

        # Result Section
        main_layout.addWidget(QLabel("Results"))
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setStyleSheet("background-color: #181825; border: 1px dashed #45475a;")
        main_layout.addWidget(self.result_area)

        self.setLayout(main_layout)

    def clear_fields(self):
        self.input_area.clear()
        self.num_nodes_input.clear()
        self.result_area.clear()

    def calculate_mst(self):
        try:
            num_v = int(self.num_nodes_input.text())
            g = KruskalMST(num_v)
            
            lines = self.input_area.toPlainText().strip().split('\n')
            if not lines or lines[0] == "":
                raise ValueError("Input area is empty.")

            for line in lines:
                u, v, w = map(int, line.split())
                g.add_edge(u, v, w)

            mst = g.get_mst()
            
            output = " SUCCESS: Optimal Tree Found\n" + "-"*30 + "\n"
            total_weight = 0
            for u, v, weight in mst:
                output += f"Edge ({u} ↔ {v}) \t Weight: {weight}\n"
                total_weight += weight
            output += "-"*30 + f"\nTOTAL MINIMUM WEIGHT: {total_weight}"
            
            self.result_area.setText(output)
        except Exception as e:
            self.result_area.setText(f" ERROR\n{str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StyledMSTApp()
    window.show()
    sys.exit(app.exec())
