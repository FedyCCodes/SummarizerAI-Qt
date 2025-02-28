# textbox.py
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
# For the user interface

from http.server import HTTPServer, BaseHTTPRequestHandler
from transformers import pipeline
# For the HuggingFace model

HuggingFaceSummarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# Gets the HuggingFace model set up

# 65,536, https://huggingface.co/facebook/bart-large-cnn

print(QtCore.__version__)
# Prints the Qt version used to compile PySide6

"""
The class that handles the user interface
"""
class SummarizerAI(QtWidgets.QWidget):
  def __init__(self):
    super().__init__()
    
    self.button = QtWidgets.QPushButton("Send Data")
    # creates the main button
    
    self.title = QtWidgets.QLabel("Summarizer AI",
                   alignment=QtCore.Qt.AlignCenter, objectName="title")
    # title for the app
    
    self.input_text = QtWidgets.QTextEdit("",
                   alignment=QtCore.Qt.AlignLeft)
    # the input text frame
    
    self.output_text = QtWidgets.QTextEdit("",
                   alignment=QtCore.Qt.AlignLeft, readOnly = True,  objectName="output")
    # the output text frame
    
    self.details = QtWidgets.QLabel("Made with PyQt and HuggingFace | Developed by Fedy Cherif",
                   alignment=QtCore.Qt.AlignCenter)
    # the credit of the app
    
    self.layout = QtWidgets.QVBoxLayout(self)
    # creates a vertical box layout
    
    self.layout.addWidget(self.title)
    self.layout.addWidget(self.input_text)
    self.layout.addWidget(self.button)
    self.layout.addWidget(self.output_text)
    self.layout.addWidget(self.details)
    # adds all the elements top to bottom
    
    self.button.clicked.connect(self.magic)
    # sets the callback for the button

  @QtCore.Slot()
  def magic(self):
    
    input_sending_data = self.input_text.toPlainText()
    # gets the input text
    
    max_set_length = 4096
    # sets the max length
    
    if (len(input_sending_data) > max_set_length): 
      # # if it's too long
      
      self.output_text.setText('Text is too long please shorten it (' + str(len(input_sending_data)) + '/' + str(max_set_length) + ').')
      # it sends a message in the output that the user should shorten it
      
      return
      # stops the function
    
    self.output_text.setText("Loading, estimated wait time is " + str(((len(input_sending_data) / max_set_length) * (7456 * 2)) / 1000) + " seconds.")
    # gives a time estimate
    
    resulting_data = HuggingFaceSummarizer(input_sending_data, max_length=max_set_length, min_length=128, do_sample=False)
    # uses hugging face to summarize the text
    
    resulting_text_data = resulting_data[0]['summary_text']
    # truncates the resulting data
    
    self.output_text.setText(resulting_text_data)
    # displays the resulting data

if __name__ == "__main__":
  app = QtWidgets.QApplication([])
  # creates the app
  
  with open("style.qss", "r") as f:
    _style = f.read()
    app.setStyleSheet(_style)
    # loads the style sheet
  
  widget = SummarizerAI()
  widget.resize(800, 600)
  widget.show()
  # creates the window
  
  sys.exit(app.exec())
  # runs the app