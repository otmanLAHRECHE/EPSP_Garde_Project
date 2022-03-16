# EPSP_Garde_Progect
python application for manage night guard of hospital services

In this project you will find how to:

   1- Manipulating PyQt5 librery with python and use multiple PyQt elements(QtTableWidget, QtTab, .......) and importing .ui files from QtDesigner.
    
   2- Database CRUD operation with SQLite.
    
   3- Use the concept of multithreading and use threads to prevent GUI freezing (PyQT QThread).
    
   4- Create and export PDF reports to local file with fpdf2 librery.
    
![Capture](https://user-images.githubusercontent.com/30577764/158579056-ba017029-0041-4a7e-a4b1-10c1c0966ef8.PNG)
    
![Capture2](https://user-images.githubusercontent.com/30577764/158579115-64dae6da-b43a-4800-9655-78223d29037c.PNG)

![Capture3](https://user-images.githubusercontent.com/30577764/158579187-e6c3bc4b-e8ca-490a-9f89-42f69a3a62fa.PNG)


for create .exe file, use Pyinstaller:
              
              pyinstaller --onefile --windowed --icon=asstes\images\guard.ico --add-data="asstes\images\*.png;asstes\images" --add-data="asstes\images\*.ico;asstes\images" --add-                data="ui\*.ui;ui" main.py

