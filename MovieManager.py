import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MovieManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie Manager")
        self.setGeometry(100, 100, 700, 600)
        self.movies = []
        self.edit_index = None
        self.dark_mode = False
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title_label = QLabel("🎬 Movie Manager")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        student_info = QLabel("By: Rizky Maulana Ramdhani | F1D022095")
        student_info.setAlignment(Qt.AlignCenter)
        student_info.setStyleSheet("font-size: 12px; font-style: italic; color: gray;")

        layout.addWidget(title_label)
        layout.addWidget(student_info)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search movie title...")
        self.search_input.textChanged.connect(self.update_list)
        layout.addWidget(self.search_input)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter movie title")
        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.title_input)

        self.genre_combo = QComboBox()
        self.genre_combo.addItems(["Action", "Comedy", "Drama", "Sci-Fi", "Horror"])
        layout.addWidget(QLabel("Genre:"))
        layout.addWidget(self.genre_combo)

        self.rating_spin = QSpinBox()
        self.rating_spin.setRange(1, 10)
        layout.addWidget(QLabel("Rating (1-10):"))
        layout.addWidget(self.rating_spin)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Description...")
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.desc_input)

        self.watched_check = QCheckBox("Watched")
        layout.addWidget(self.watched_check)

        btn_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Movie")
        self.add_button.clicked.connect(self.add_movie)
        self.add_button.setFixedHeight(30)
        self.add_button.setStyleSheet("background-color: #28a745; color: white;")
        btn_layout.addWidget(self.add_button)

        self.update_button = QPushButton("Update Movie")
        self.update_button.clicked.connect(self.update_movie)
        self.update_button.setFixedHeight(30)
        self.update_button.setStyleSheet("background-color: #ffc107; color: white;")
        btn_layout.addWidget(self.update_button)

        self.clear_button = QPushButton("Clear List")
        self.clear_button.clicked.connect(self.clear_list)
        self.clear_button.setFixedHeight(30)
        self.clear_button.setStyleSheet("background-color: #dc3545; color: white;")
        btn_layout.addWidget(self.clear_button)

        layout.addLayout(btn_layout)

        self.movie_list = QListWidget()
        self.movie_list.itemClicked.connect(self.fill_form)
        layout.addWidget(QLabel("Movie List:"))
        layout.addWidget(self.movie_list)

        self.darkmode_button = QPushButton("Toggle Dark Mode")
        self.darkmode_button.clicked.connect(self.toggle_dark_mode)
        self.darkmode_button.setFixedHeight(30)
        layout.addWidget(self.darkmode_button)

        self.setLayout(layout)
        self.apply_light_mode()

    def add_movie(self):
        title = self.title_input.text()
        genre = self.genre_combo.currentText()
        rating = self.rating_spin.value()
        desc = self.desc_input.toPlainText()
        watched = self.watched_check.isChecked()

        if not title:
            QMessageBox.warning(self, "Warning", "Movie title cannot be empty.")
            return

        self.movies.append({
            "title": title,
            "genre": genre,
            "rating": rating,
            "desc": desc,
            "watched": watched
        })
        self.clear_form()
        self.update_list()

    def update_movie(self):
        if self.edit_index is None:
            QMessageBox.information(self, "Info", "Select a movie to update.")
            return

        self.movies[self.edit_index] = {
            "title": self.title_input.text(),
            "genre": self.genre_combo.currentText(),
            "rating": self.rating_spin.value(),
            "desc": self.desc_input.toPlainText(),
            "watched": self.watched_check.isChecked()
        }
        self.edit_index = None
        self.clear_form()
        self.update_list()

    def fill_form(self, item):
        index = self.movie_list.row(item)
        movie = self.filtered_movies()[index]
        self.edit_index = self.movies.index(movie)

        self.title_input.setText(movie['title'])
        self.genre_combo.setCurrentText(movie['genre'])
        self.rating_spin.setValue(movie['rating'])
        self.desc_input.setPlainText(movie['desc'])
        self.watched_check.setChecked(movie['watched'])

    def filtered_movies(self):
        query = self.search_input.text().lower()
        return [m for m in self.movies if query in m['title'].lower()]

    def update_list(self):
        self.movie_list.clear()
        for movie in self.filtered_movies():
            status_icon = "✅" if movie["watched"] else "❌"
            item_text = f"{status_icon} {movie['title']} | {movie['genre']} | Rating: {movie['rating']} | Desc: {movie['desc']}"
            item = QListWidgetItem(item_text)

            if movie["watched"]:
                item.setBackground(QColor("#d4edda"))
            else:
                item.setBackground(QColor("#f8d7da"))

            self.movie_list.addItem(item)

    def clear_form(self):
        self.title_input.clear()
        self.rating_spin.setValue(1)
        self.desc_input.clear()
        self.watched_check.setChecked(False)

    def clear_list(self):
        confirm = QMessageBox.question(
            self, "Clear All", "Are you sure you want to clear the movie list?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.movies.clear()
            self.movie_list.clear()
            self.clear_form()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_dark_mode()
        else:
            self.apply_light_mode()

    def apply_dark_mode(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2e2e2e;
                color: white;
            }
            QLineEdit, QComboBox, QTextEdit, QSpinBox {
                background-color: #444;
                color: white;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 6px;
            }
            QListWidget {
                background-color: #333;
                color: white;
                border-radius: 8px;
                padding: 6px;
            }
            QPushButton {
                background-color: #555;
                color: white;
                border-radius: 8px;
                padding: 6px;
                font-weight: bold;
            }
        """)

    def apply_light_mode(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                color: black;
            }
            QLineEdit, QComboBox, QTextEdit, QSpinBox, QListWidget {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 6px;
            }
            QPushButton {
                border-radius: 8px;
                padding: 6px;
                font-weight: bold;
            }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)    
    window = MovieManager()
    window.show()
    sys.exit(app.exec_())