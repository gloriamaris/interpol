import os

class SyntaxChecker:
    def __init__(self, filename):
        self.filename = filename
        self.count = 0
        self.line = ""
        self.is_valid_program = True

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
        
        self.terminals = {
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
        
        self.non_recursive_grammars = {
            "BASIC_OP_EXPR": "BASIC_OP int int",
            "ADV1_OP_EXPR": "ADV1_OP int int",
            "ADV2_OP_EXPR": "ADV2_OP int",
            "ADV3_OP_EXPR": "ADV3_OP int int ADV3_OP_CONN int int",
            "DECLARE_INT_EXPR": "DECLARE_INT identifier",
            "DECLARE_STR_EXPR": "DECLARE_STR identifier",
            "OUTPUT_INT_EXPR": "OUTPUT str",
            "OUTPUT_STR_EXPR": "OUTPUT int",
            "OUTPUT_EXPR": "OUTPUT identifier",
            "INPUT_EXPR": "INPUT identifier",
            "STORE_INT_EXPR": "ASSIGN int ASSIGN_CONN identifier",
            "STORE_STR_EXPR": "ASSIGN str ASSIGN_CONN identifier",
            "MARKER_EXPR": "MARKER"
        }
        
        self.recursive_grammars = {
            "BASIC_OP_EXPR": [
                "BASIC_OP int BASIC_OP_EXPR",
                "BASIC_OP BASIC_OP_EXPR int"
            ],
            "DECLARE_INT_EXPR": [
                "DECLARE_INT DECLARE_CONN int",
                "DECLARE_INT DECLARE_CONN identifier"
            ],
            "DECLARE_STR_EXPR": [
                "DECLARE_STR DECLARE_CONN str",
                "DECLARE_STR DECLARE_CONN identifier"
            ],
            "OUTPUT_INT_EXPR": [
                "OUTPUT BASIC_OP_EXPR"
            ],
            # "STORE_EXPR": [
            #     "ASSIGN BASIC_OPERATION_EXPR ASSIGN_CONN identifier",
            # ]
        }
    
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

    # find the operation where the keyword belongs.
    # otherwise, return false
    def get_terminal_key(self, token):
        result = False

        for key in self.terminals:
            result = key if token in self.terminals[key] else False 
            
            if (result != False):
                break
        
        return result
    
    # returns the valid grammars for the keyword
    def get_valid_grammar(self, keyword):
        grammar_list = []
        grammar_key = ""

        # get the operation the keyword belongs to
        operation = self.get_terminal_key(keyword)
        
        # get the grammar list
        try:
            for key in self.non_recursive_grammars:
                found = self.non_recursive_grammars[key].find(operation)

                # get key from non_recursive, and use the key to return the valid recursive grammars
                if (found >= 0):
                    grammar_key = key
                    grammar_list.append(self.non_recursive_grammars[key])
                    grammar_list += self.recursive_grammars[grammar_key]       
                    break
        except KeyError:
            pass
        
        return {
            grammar_key: grammar_list
        }

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
    
    def get_literal(self, token):
        if (self.is_number(token) == True):
            return "int"
        elif (self.is_string(token) == True):
            return "str"
        else:
            return False
    
    def validate_nonrecursive_grammar(self, tokens, base_grammar):
        generated_lexemes = []
        produced_grammar = ""
        
        for token in tokens:
            lexeme_literal = self.get_literal(token)
            lexeme_keyword = self.get_terminal_key(token)

            if (lexeme_literal != False):
                generated_lexemes.append(lexeme_literal)
            elif (lexeme_keyword != False):
                generated_lexemes.append(lexeme_keyword)
        
        produced_grammar = " ".join(generated_lexemes)
        print(produced_grammar)
        return True if (produced_grammar == base_grammar) else False
        
    def process_line(self, line):
        tokens = self.clean_up_line(line)

        # get the valid grammars for the line based on the first keyword
        valid_grammars = self.get_valid_grammar(tokens[0])

        for key in valid_grammars.keys():
            nonterminal_key = key
        
        is_valid_nonrecursive = self.validate_nonrecursive_grammar(tokens, valid_grammars[nonterminal_key][0])
        print("is_valid_nonrecursive")
        print(is_valid_nonrecursive)
    
    def throw_error(self, message, count, line):
        print("{} at Line number [{}]".format(message, count))
        print("{}".format(line))
    
    def execute(self): 
        is_section = True
        last_line = ""

        while (is_section == True):
            with open(self.filename, "r") as f:
                self.count = 0
                
                for line in f: 
                    self.count += 1
                    
                    # check if complete section
                    if (self.count == 1 and line != "BEGIN"):
                        is_section = False
                    else:
                        self.line = line
                        self.process_line(line)
                    
                    # stores the last statement
                    if (line != ""):
                        last_line = line
                    
                    
                    
                
        
        # if the last line is not END, the section is not a valid program
        if (last_line != "END"):
            is_section = False 
            print("Error at Line {}: {}".format(self.count-1, self.error_messages["INVALID_EOF"]))




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

        #   tokenTable = TokenTable(filename)
        #   tokenTable.display_table()



# Starts the program
interpreter = Interpreter()
interpreter.execute()