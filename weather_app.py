import sys
import requests
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QMainWindow, QVBoxLayout, QLineEdit
from PySide6.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.enter_label = QLabel("Enter a city name:",self)
        self.city_line = QLineEdit(self)
        self.weather_button = QPushButton("Enter",self)
        self.temperature_label = QLabel(self)
        self.weather_icon = QLabel(self)
        self.weather_condition = QLabel(self)
        self.weather_button.clicked.connect(self.get_weather)
        self.initUI()
    def initUI(self):
        vbox = QVBoxLayout(self)
        self.setLayout(vbox)

        vbox.addWidget(self.enter_label)
        vbox.addWidget(self.city_line)
        vbox.addWidget(self.weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.weather_icon)
        vbox.addWidget(self.weather_condition)

        self.enter_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.weather_icon.setAlignment(Qt.AlignCenter)
        self.weather_condition.setAlignment(Qt.AlignCenter)

        self.enter_label.setObjectName("enter")
        self.temperature_label.setObjectName("temp")
        self.weather_icon.setObjectName("icon")
        self.weather_condition.setObjectName("condition")

        self.setStyleSheet("""

                    QLabel{ 
                        font-size: 48px;         
                        font-family: calibri;
                        
                           }

                    QLabel#enter{
                        font-style:italic;

                           }

                    QLabel#temp{
                        font-size:68px;

                           }

                    QLabel#icon{
                        font-size: ;   
                            font-size:80px;
                            font-family: Segoe UI emoji;
                           }

                    QLineEdit{
                        font-size: 36px;
                        min-height: 48px;
                           }

                    QPushButton{
                        font-size:28px;
                        font-family: calibri;
                        font-weight: bold;
                        padding: 10px;
                           }

                    
""")
    
    def get_weather(self):
        
        api_key = "d727127cbf3120c324fba5a0c22a8b0d"
        city_name = self.city_line.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError:
            match response.status_code:

                case 400:
                    self.display_error("Bad Request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 404:
                    self.display_error("Not Found:\nCity could not found")
                case 500:
                    self.display_error("Internal Server Error\n Please try again later")
                case _:
                    self.display_error("HTTP error occured")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")

        except requests.exceptions.RequestException:
            self.display_error("Please Try Again Later")

    def display_error(self,message):
        self.temperature_label.setStyleSheet("""
                                font-size:24px;

""")
        self.temperature_label.setText(message)
        self.weather_condition.clear()
        self.weather_icon.clear()

    def display_weather(self,data):
        self.temperature_label.setStyleSheet("""
                                font-size:68px;

""")
        temperatureK = data["main"]["temp"]
        temperatureC = temperatureK - 273.15
        self.temperature_label.setText(f"{temperatureC:.0f}°C")
        weather = data["weather"][0]["description"].capitalize()
        self.weather_condition.setText(f"{weather}")
        self.weather_icon.setText(self.weather_emoji(data["weather"][0]["id"]))

    @staticmethod
    def weather_emoji(weather_id):
        if 200<=weather_id<=232:
            return "⛈️"
        elif 300<=weather_id<=321:
            return "🌦️"
        elif 500<=weather_id<=531:
            return "🌧️"
        elif 600<=weather_id<=622:
            return "❄️"
        elif 700<=weather_id<=781:
            if weather_id == 701 | 721 | 741:
                return "🌫️"
            elif weather_id == 762:
                return "🌋"
            elif weather_id == 771:
                return "🌀"
            elif weather_id == 781:
                return "🌪️"
            else:
                return ""
        elif weather_id == 800:
            return "☀️"
        elif weather_id>800:
            return "☁️"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())