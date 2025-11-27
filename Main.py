import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Main_window import MainWindow




def main():
    app = QApplication(sys.argv)
    
    try:
       # with open("style/", "r") as f:
        #    app.setStyleSheet(f.read())
        pass
    except Exception as e:
        print("Failed to load stylesheet:", e)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    
    


        
        