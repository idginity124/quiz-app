import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QPushButton, \
    QButtonGroup, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from PyQt5.QtCore import Qt


class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.questions = self.load_questions()  # Load questions from JSON file / Soruları JSON dosyasından yükleyin
        self.current_question = 0
        self.score = 0
        self.user_answers = []  # List to store user answers / Kullanıcı yanıtlarını tutan liste

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Şıklı Sorular Quiz Uygulaması')  # Set window title / Pencere başlığını ayarlayın
        self.setWindowIcon(QIcon('path_to_icon.ico'))  # Set window icon / Pencere simgesini ayarlayın
        self.setGeometry(100, 100, 800, 400)  # Set window size / Pencere boyutunu ayarlayın

        # Application palette for colors / Uygulama için renk paleti
        app_palette = QPalette()
        app_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        app_palette.setColor(QPalette.WindowText, Qt.white)
        app_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        app_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        app_palette.setColor(QPalette.ToolTipBase, Qt.white)
        app_palette.setColor(QPalette.ToolTipText, Qt.white)
        app_palette.setColor(QPalette.Text, Qt.white)
        app_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        app_palette.setColor(QPalette.ButtonText, Qt.white)
        app_palette.setColor(QPalette.BrightText, Qt.red)
        app_palette.setColor(QPalette.Link, QColor(100, 200, 255))
        app_palette.setColor(QPalette.Highlight, QColor(100, 150, 255))
        app_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(app_palette)

        # Font for question title / Soru başlığı için font
        font_title = QFont('Arial', 18, QFont.Bold)
        # Font for options / Seçenekler için font
        font_options = QFont('Arial', 12)

        self.layout = QVBoxLayout()

        # Label for question / Soru için etiket
        self.question_label = QLabel(self)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setFont(font_title)
        self.question_label.setStyleSheet("color: white; padding: 10px;")
        self.question_label.setWordWrap(True)  # Word wrap for the question text / Soru metni için kelime kaydırma
        self.layout.addWidget(self.question_label)

        # Label for feedback / Geribildirim için etiket
        self.feedback_label = QLabel(self)
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setFont(font_title)
        self.feedback_label.setStyleSheet("color: yellow; padding: 10px;")
        self.feedback_label.setWordWrap(True)  # Word wrap for feedback text / Geribildirim metni için kelime kaydırma
        self.layout.addWidget(self.feedback_label)

        # Group to manage options / Seçenekleri yönetmek için grup
        self.option_group = QButtonGroup(self)
        self.option_layout = QVBoxLayout()

        # Loop to create 5 radio buttons for options (A, B, C, D, E) / 5 seçenek (A, B, C, D, E) için radio button'lar oluşturmak
        for i in range(5):
            btn = QRadioButton(self)
            btn.setFont(font_options)
            btn.setStyleSheet("color: white; padding: 5px;")
            self.option_layout.addWidget(btn)
            self.option_group.addButton(btn)
            btn.setAutoExclusive(True)
            btn.clicked.connect(self.enableVerifyButton)  # Enable "Verify" button when an option is selected / Bir seçenek seçildiğinde "Doğrula" butonunu etkinleştir

        self.layout.addLayout(self.option_layout)

        # Button layout for navigation and verification / Navigasyon ve doğrulama butonları için düzen
        self.button_layout = QHBoxLayout()

        # Previous button / Önceki butonu
        self.prev_button = QPushButton('Önceki', self)
        self.prev_button.setFont(font_options)
        self.prev_button.setStyleSheet("background-color: #171a21; color: white; padding: 10px; border: none;")
        self.prev_button.clicked.connect(self.prevQuestion)
        self.button_layout.addWidget(self.prev_button)

        # Next button / Sonraki butonu
        self.next_button = QPushButton('Sonraki', self)
        self.next_button.setFont(font_options)
        self.next_button.setStyleSheet("background-color: #171a21; color: white; padding: 10px; border: none;")
        self.next_button.clicked.connect(self.nextQuestion)
        self.button_layout.addWidget(self.next_button)

        # Verify button / Doğrula butonu
        self.verify_button = QPushButton('Doğrula', self)
        self.verify_button.setFont(font_options)
        self.verify_button.setStyleSheet("background-color: #28a745; color: white; padding: 10px; border: none;")
        self.verify_button.clicked.connect(self.verifyAnswer)
        self.button_layout.addWidget(self.verify_button)

        # Finish button / Bitir butonu
        self.finish_button = QPushButton('Bitir', self)
        self.finish_button.setFont(font_options)
        self.finish_button.setStyleSheet("background-color: #d9534f; color: white; padding: 10px; border: none;")
        self.finish_button.clicked.connect(self.finishQuiz)
        self.finish_button.setVisible(False)  # Initially hidden / İlk başta gizli
        self.button_layout.addWidget(self.finish_button)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

        self.loadQuestion()

    def enableVerifyButton(self):
        """Enable the verify button when an option is selected."""
        # Bir seçenek seçildiğinde "Doğrula" butonunu etkinleştir
        self.verify_button.setEnabled(True)

    def load_questions(self):
        """Load the questions from the JSON file and return them."""
        # Soruları JSON dosyasından okuyun ve döndürün
        with open('questions.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def loadQuestion(self):
        """Load the current question and options."""
        # Mevcut soruyu ve seçenekleri yükleyin
        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.question_label.setText(f"{self.current_question + 1}. {question_data['question']}")
            self.feedback_label.setText("")  # Reset feedback text / Geribildirim metnini sıfırlayın

            options = question_data['options']
            for i, option in enumerate(options):
                btn = self.option_layout.itemAt(i).widget()
                btn.setText(option)
                btn.setChecked(False)  # Uncheck options / Seçenekleri işaretten kaldır

        if self.current_question == len(self.questions) - 1:  # If this is the last question / Eğer bu son soruysa
            self.next_button.setVisible(False)  # Hide the next button / Sonraki butonunu gizle
            self.finish_button.setVisible(True)  # Show the finish button / Bitir butonunu göster
        else:
            self.next_button.setVisible(True)
            self.finish_button.setVisible(False)

    def prevQuestion(self):
        """Go to the previous question."""
        # Önceki soruya git
        if self.current_question > 0:
            self.current_question -= 1
            self.loadQuestion()

    def nextQuestion(self):
        """Go to the next question."""
        # Sonraki soruya git
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.loadQuestion()

    def verifyAnswer(self):
        """Verify the selected answer and give feedback."""
        # Seçilen cevabı doğrula ve geribildirim ver
        selected_option = self.option_group.checkedButton()
        if selected_option:
            user_answer = selected_option.text()[0]  # Get the first character (A, B, C, D, E) / İlk harfi (A, B, C, D, E) al
            self.user_answers.append(user_answer)
            correct_answer = self.questions[self.current_question]['answer']
            if user_answer == correct_answer:
                self.score += 1
                self.feedback_label.setText("Doğru!")  # Correct answer feedback / Doğru cevap geribildirimi
                self.feedback_label.setStyleSheet("color: green; font-size: 14pt;")
            else:
                self.feedback_label.setText(f"Yanlış! Doğru cevap: {correct_answer}")  # Incorrect answer feedback / Yanlış cevap geribildirimi
                self.feedback_label.setStyleSheet("color: red; font-size: 14pt;")
        else:
            self.feedback_label.setText("Lütfen bir seçenek işaretleyiniz.")  # Ask the user to select an option / Kullanıcıdan bir seçenek işaretlemesini isteyin
            self.feedback_label.setStyleSheet("color: yellow; font-size: 14pt;")

        self.verify_button.setEnabled(False)

        if self.current_question == len(self.questions) - 1:
            self.next_button.setVisible(False)
            self.finish_button.setVisible(True)

    def finishQuiz(self):
        """Finish the quiz and show the result."""
        # Quiz'i bitir ve sonucu göster
        self.showDetailedResults()
        QMessageBox.information(self, "Quiz Sonucu", f"Quiz tamamlandı!\nToplam Puanınız: {self.score}/{len(self.questions)}")  # Display final score / Sonuçları göster
        self.close()

    def showDetailedResults(self):
        """Show the detailed results after quiz completion."""
        # Quiz tamamlandığında detaylı sonuçları göster
        result_window = QWidget()
        result_window.setWindowTitle("Detaylı Sonuçlar")
        layout = QVBoxLayout()

        for i, question in enumerate(self.questions):
            result_label = QLabel(f"Soru {i+1}: {question['question']}")
            result_label.setStyleSheet("color: white;")
            layout.addWidget(result_label)

            user_answer = self.user_answers[i] if i < len(self.user_answers) else None
            correct_answer = question["answer"]
            result_label = QLabel(f"Doğru Cevap: {correct_answer}")
            result_label.setStyleSheet("color: green;" if correct_answer == user_answer else "color: red;")
            layout.addWidget(result_label)

        result_window.setLayout(layout)
        result_window.show()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    quiz = QuizApp()
    quiz.show()
    sys.exit(app.exec_())
