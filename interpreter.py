import os

class SyntaxChecker:
  def __init__(self, filename):
    self.filename = filename

    # List of error messages
    self.error_messages = {
      "VAR_NOT_DECLARED": "Variable is not declared",
      "DUPLICATE_VAR": "Duplicate variable declaration",
      "INCOMP_DATA_TYPE": "Incompatible data type",
      "INVALID_SYNTAX": "Invalid syntax",
      "INVALID_OP": "Invalid arithmetic operation",
      "INVALID_EXPR": "Invalid expression",
      "INVALID_DATA_TYPE": "Invalid data type",
      "INVALID_DATA_TYPE_INPUT": "Invalid data type input",
      "INVALID_EOF": "Invalid end of file"
    }

  def execute(self):
    is_valid = True
    is_complete_section = False

    with open(self.filename, "r") as f:
      count = 1
      last_line = ""

      for line in f:
        print("Line {}, {}".format(count, line.strip()))

        # check if complete section
        if (count == 1 and line == "BEGIN"):
          is_complete_section = True

        if (line != ""):
          last_line = line

        count += 1
  

    if (last_line != "END"):
      is_complete_section = False
      print("Error at Line {}: {}".format(count-1, self.error_messages["INVALID_EOF"]))

    
    print("Last line")
    print(last_line)





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
      if (filename.find(".ipol") == -1):                    # If file is invalid - does not end in .ipol
        print(self.error_messages["INVALID_FILE"])
        proceed = False
      elif (os.path.exists(filename) == False):             # If file does not exist - size of the file in bytes is 0
        print(self.error_messages["FILE_NOT_FOUND"])
        proceed = False
      elif (os.stat(filename).st_size == 0):                # If file is empty
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