FROM python:3.13.1

RUN pip install discord.py
RUN pip install audioop-lts
RUN pip install python-dotenv
RUN pip install pyperclip
RUN pip install pyautogui
RUN pip install pytesseract
RUN pip install openpyxl

COPY . .

CMD [ "python3", "Scan.py" ]