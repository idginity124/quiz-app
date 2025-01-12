# Detailed Code Explanation / Detaylı Kod Açıklaması

"This document explains the code for the `Quiz App`. The application is a simple multiple-choice quiz built using PyQt5. Below is an explanation of each part of the code."
Bu belge, `Quiz App`'in kodunu açıklar. Uygulama PyQt5 kullanılarak yapılmış basit bir çoktan seçmeli quiz uygulamasıdır. Aşağıda, her bir kod parçasının açıklaması yer almaktadır.

---

## 1. Importing Libraries / Kütüphanelerin İçe Aktarılması

### Code / Kod:

```python
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QPushButton, QButtonGroup, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from PyQt5.QtCore import Qt

json: Reads and writes JSON data, used to load quiz questions from a JSON file.
json: JSON verilerini okur ve yazar, quiz sorularını JSON dosyasından yüklemek için kullanılır.

PyQt5.QtWidgets: Contains essential PyQt5 GUI components like windows, buttons, layouts, etc.
PyQt5.QtWidgets: PyQt5 GUI bileşenlerini içerir, pencere, buton, düzenler vb.

QApplication, QWidget, QVBoxLayout, QHBoxLayout: These are used for setting up the basic UI layout of the application.
QApplication, QWidget, QVBoxLayout, QHBoxLayout: Uygulamanın temel kullanıcı arayüzünü (UI) oluşturmak için kullanılır.

QRadioButton, QPushButton: These are the buttons used for user interaction.
QRadioButton, QPushButton: Kullanıcı etkileşimi için kullanılan butonlardır.

QPalette, QColor: These are used to customize the appearance, such as setting the theme colors.
QPalette, QColor: Görünümü özelleştirmek için kullanılır, tema renklerinin ayarlanmasını sağlar.
