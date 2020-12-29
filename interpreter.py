import os

class SyntaxChecker:
  def __init__(self):
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

    self.lexicons = {
      "MARKER": ["BEGIN", "END"],
      "DISPLAY": ["PRINT", "PRINTLN"],
      "OPERATOR": ["ADD", "SUB", "MUL", "DIV", "MOD", "RAISE", "ROOT", "MEAN", "DIST", "IN"],
      "DECLARE": ["VARINT", "VARSTR"],
      "ASSIGN": ["WITH", "STORE", "IN"],
      "INPUT": ["INPUT"]
    }

    self.grammar = {
      "COMMENT": "#string",
      "OPERATOR_1": "OP int int",
      "OPERATOR_2": "OP int [OPERATOR_1]+",
      "DISPLAY": "DIS string",
      "DECLARE_INT_1": "VARINT var",
      "DECLARE_INT_2": "VARINT var WITH int",
      "DECLARE_INT_3": "VARINT var WITH [OPERATOR]+",
      "DECLARE_STR": "VARSTR str",
      "MARKER": "MARK"
    }

  def is_int(self, token):
    try:
        int(token)
        return True
    except ValueError:
        return False

  # Lexicon validators
  def is_start_marker(self, token):
    return self.check_if_marker(token, "start")

  def is_operator(self, token):
    return True if token in self.lexicons["OPERATOR"] else False

  def is_display_method(self, token):
    return True if token in self.lexicons["DISPLAY"] else False

  def is_number(self, token):
    return True if (self.check_ascii(token) and self.is_int(token)) else False

  def is_string_literal(self, token): 
    return True if (token[0] == '"' and token[len(token) - 1] == '"' and self.check_ascii(token)) else False

  def is_comment(self, token):
    return True if token[0] == '#' else False

  def check_ascii(self, token):
    return True if len(token) == len(token.encode()) else False
    
def get_lexicons(self):
  return self.lexicons

def execute(self, filename):
  is_valid = True
  is_complete_section = False

  with open(filename, "r") as f:
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

    
    


class TokenTable:
  def __init__(self, filename):
    self.filename = filename

    self.lexemes_list = {
      "BEGIN": "PROGRAM_BEGIN",
      "END": "PROGRAM_END",
      "VARINT": "DECLARATION_INT",
      "VARSTR": "DECLARATION_STRING",
      "WITH": "DECLARATION_ASSIGN_WITH_KEY",
      "PRINTLN": "OUTPUT_WITH_LINE",
      "INPUT": "INPUT",
      "ADD": "BASIC_OPERATOR_ADD",
      "SUB": "BASIC_OPERATOR_SUB",
      "MUL": "BASIC_OPERATOR_MUL",
      "DIV": "BASIC_OPERATOR_DIV",
      "MOD": "BASIC_OPERATOR_MOD",
      "STORE": "ASSIGN_KEY",
      "IN": "ASSIGN_VAR_KEY",
      "ROOT": "ADVANCED_OPERATOR_ROOT",
      "RAISE": "ADVANCED_OPERATOR_EXP",
      "AVE": "ADVANCED_OPERATOR_AVE"
    }

  # parses all lexemes per line of code
  def parse_line(self, line, count):
    syntaxChecker = SyntaxChecker()
    lexicons = syntaxChecker.get_lexicons()
    lexemes = line.split()
    last_item = ""
    index = 0

    print("lexemes")
    print(lexemes)

    try:
      for item in lexemes:
        self.output_line(count, self.lexemes_list[item], item)
        last_item = item
        index += 1
    except KeyError:
      # checks the previous lexeme if VAR` 
      item = lexemes[index-1] 
      token = ""
  
      if (self.lexemes_list[item] == "VARSTR" and self.lexemes_list[item] == "VARSTR"):
        token = "IDENTIFIER"
      elif (syntaxChecker.is_number(item) and (item in lexicons["OPERATORS"])):
        token = "NUMBER"
      else:
        token = "STRING"

      self.output_line(index, token, item)

  def output_line(self, count, token, lexeme):
    print("{}\t\t{}\t\t\t{}".format(count, token, lexeme))

      

  # displays the list of tokens and lexemes
  def display_table(self):
    print("========= INTERPOL LEXEMES/TOKENS TABLE =========")
    print("LINE NO.\t\tTOKENS\t\t\t\tLEXEMES")
  
    with open(self.filename, "r") as f:
      count = 1
      last_line = ""

      for line in f:
        self.parse_line(line, count)
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
      # syntaxChecker = SyntaxChecker(filename)
      # syntaxChecker.execute()

      tokenTable = TokenTable(filename)
      tokenTable.display_table()



# Starts the program
interpreter = Interpreter()
interpreter.execute()