import os


#
#   ExpressionsEvaluator class
#   - checks the tokens if they are valid elements
#   - evaluates using the operation specified
#
class ExpressionsEvaluator:
    def __init__(self, tokens, line_num):
        self.tokens = tokens
        self.line_num = line_num
        self.expr_stack = []

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
        
        self.lexemes = {
            "COMMENT": ["#string"],
            "MARKER": ["BEGIN", "END"],
            "BASIC_OP": ["ADD", "SUB", "MUL", "DIV", "MOD"],
            "ADV1_OP": ["RAISE", "ROOT"],
            "ADV2_OP": ["MEAN"],
            "ADV3_OP": ["DIST"],
            "ADV3_OP_CONN": ["AND"],
            "ASSIGN": ["STORE"],
            "ASSIGN_CONN": ["IN"],
            "DECLARE_INT": ["VARINT"],
            "DECLARE_STR": ["VARSTR"],
            "DECLARE_CONN": ["WITH"],
            "OUTPUT": ["PRINT", "PRINTLN"],
            "INPUT": ["INPUT"],
        }
    
    def validate_lexeme(self, token):
        for key in self.lexemes:
            if (token in self.lexemes[key]):
                return key
            
        return False

    def is_int(self, token):
        try:
            int(token)
            return True
        except ValueError:
            return False
        
    def is_number(self, token):
        return True if (self.check_ascii(token) and self.is_int(token)) else False

    def is_string(self, token): 
        return True if (token[0] == '"' and token[len(token) - 1] == '"' and self.check_ascii(token)) else False
    
    def check_ascii(self, token):
        return True if len(token) == len(token.encode()) else False
    
    def validate_literal(self, token):
        if (self.is_number(token) == True):
            return "int"
        elif (self.is_string(token) == True):
            return "str"
        else:
            return False
    
    def push_tokens(self, tokens):
        token_list = []

        for token in tokens:
            lexeme_value = self.validate_lexeme(token)
            literal_value = self.validate_literal(token)
            
            # if the tokens are valid elements in the program
            if (lexeme_value != False or literal_value != False):
                token_list.append(token)
        
        return token_list
    
    def pop_stack(self):
        last_index = len(self.expr_stack) - 1
        return self.expr_stack.pop(last_index)

    def peek_stack(self):
        last_index = len(self.expr_stack) - 1
        return self.expr_stack.pop[last_index]
    
    def calculate_basic_math(self, val1, val2, operation):
        
    
    def throw_error(self, )
    
    def execute(self):
        self.expr_stack = self.push_tokens(self.tokens)
        is_processing = True
        val_1 = ""
        val_2 = ""
        method = ""
        
        while (is_processing == True):
            val_1 = self.pop_stack()
            val_2 = self.pop_stack()
            # CASE 1. MATHEMATICAL OPERATIONS ======
            
            # returns an error of val1 is an int BUT val2 is not
            if (self.validate_literal(val_1) == "int" and self.validate_literal(val_1) == "int"):
                method = self.pop_stack()
                
                

            val_2 = self.pop_stack()
            

        print(self.expr_stack)
                
#
#   TokenGenerator Class
#   - used to clean comments annd generate tokens
#
class TokenGenerator:
    # removes and ignores comments
    def filter_comments(self, tokens): 
        new_tokens = []
        index = 0
        commentIndex = 0

        # Find comments and ignore them
        for token in tokens:
            index += 1
            commentIndex = index

            if (token[0] == '#'):
                commentIndex -= 1
                break

        new_tokens = tokens[:commentIndex]
        return new_tokens

    # groups parenthesis together e.g. strings
    def group_parentheses(self, tokens):
        new_tokens = []
        count = 0
        processed_string = ""
        
        if (len(tokens) == 2):
            second_token = tokens[1]
            if(second_token[0] == '"' and second_token[len(second_token)-1] == '"'):
                return tokens

        # groups the strings by parenthesis
        for token in tokens:
            
            if (token[0] == '"' or token[len(token)-1] == '"'):
                count += 1

            if (count == 1 or count == 2):
                processed_string += token + " "

            if (count == 0 or count == 3):
                new_tokens.append(token)
            
            if (count == 2):
                new_tokens.append(processed_string[:len(processed_string)-1])
                count += 1
    
        return new_tokens
    
    # does clean up for code
    def clean_up_line(self, line_of_code):
        tokens = line_of_code.split()

        if (len(tokens) == 1):
            return tokens

        # remove comments first, then group the parentheses
        new_tokens = self.filter_comments(tokens)

        if (len(new_tokens) > 1):
            new_tokens = self.group_parentheses(new_tokens)

        return new_tokens
    
    def execute(self, line_of_code):
        tokens = line_of_code.split()

        if (len(tokens) == 1):
            return tokens

        # remove comments first, then group the parentheses
        new_tokens = self.filter_comments(tokens)

        if (len(new_tokens) > 1):
            new_tokens = self.group_parentheses(new_tokens)

        return new_tokens
    
# 
#   Main class for the program
#
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
  def validate_file(self, filename):
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
    count = 0

    filename = input("Enter INTERPOL file: ")
    is_valid_program = self.validate_file(filename)

    if (is_valid_program == True):
        with open(filename, "r") as f:
            for line in f:
                count += 1
                
                if (count == 1 and line != "BEGIN"):
                    is_valid_program = False
                else:
                    tokenGenerator = TokenGenerator()
                    tokens = tokenGenerator.execute(line)

                    evaluator = ExpressionsEvaluator(tokens)
                    evaluator.execute()

        #   tokenTable = TokenTable(filename)
        #   tokenTable.display_table()



# Starts the program
interpreter = Interpreter()
interpreter.execute()