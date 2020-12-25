import os

class SyntaxChecker:
  def __init__(self, filename):
    self.filename = filename

  def execute(self):
    is_valid = True

    with open(self.filename) as f:
      line = f.readline()
      count = 1

      while line:
        print("Line {}, {}".format(count, line.strip()))
        line = f.readline()
        count += 1





# Main class for the program
class Interpreter:
  # Keywords and reserved words are listed here.
  # ASCII printable characters will be checked through ord() 
  def __init__(self):
    self.error_messages = {
      "INVALID_FILE": "Invalid File",
      "FILE_EMPTY": "File is empty",
      "FILE_NOT_FOUND": "File not found"
    }

  # Checks for file-related errors
  def check_file_errors(self, filename):
    proceed = True

    try:
      # If file is invalid - does not end in .ipol
      if (filename.find(".ipol") == -1):
        print(self.error_messages["INVALID_FILE"])
        proceed = False
      elif (os.path.exists(filename) == False):
        # If file does not exist - size of the file in bytes is 0
        print(self.error_messages["FILE_NOT_FOUND"])
        proceed = False
      # If file is empty
      elif (os.stat(filename).st_size == 0):
        print(self.error_messages["FILE_EMPTY"])
        proceed = False
    except FileNotFoundError:
      pass

    return proceed

  # Runs the program and asks for a file input to evalute
  def execute(self):
    is_valid_program = True
    filename = ""

    filename = input("Enter INTERPOL file: ")
    is_valid_program = self.check_file_errors(filename)

    if (is_valid_program == True):
      syntaxChecker = SyntaxChecker(filename)
      syntaxChecker.execute()



# Starts the program
interpreter = Interpreter()
interpreter.execute()