import os, re


#
#   ExpressionsEvaluator class
#   - checks the tokens if they are valid elements
#   - evaluates using the operation specified
#
class ExpressionsEvaluator:
    def __init__(self, tokens, line_num, global_variables):
        self.tokens = tokens
        self.line_num = line_num
        self.global_variables = global_variables
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
    
    def validate_lexeme(self, token, key = ""):
        if (key == ""):
            for key in self.lexemes:
                if (token in self.lexemes[key]):
                    return key

            return False
        else:
            return True if token in self.lexemes[key] else False

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

    def is_identifier(self, token):
        return True if (len(token) > 0 and len(token) <= 50) and re.match('^[a-zA-Z0-9_]+$', token) and self.validate_lexeme(token) == False else False
    
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
            is_identifier = self.is_identifier(token)
            
            # if the tokens are valid elements in the program
            if (lexeme_value != False or literal_value != False or is_identifier == True):
                token_list.append(token)
        
        self.expr_stack = token_list

    def peek_token(self, index):
        return self.expr_stack[index]
    
    def pop_token(self):
        return str(self.expr_stack.pop())
    
    def calculate_basic_math(self, val1, val2, op):
        result = 0

        # adds num1 and num2
        if (op == "ADD"):
            result = val1 + val2
        
        # subtracts num2 from num1
        if (op == "SUB"):
            result = val1 - val2
        
        # multiplies num1 and num2
        if (op == "MUL"):
            result = val1 * val2
        
        # divides num1 by num2
        if (op == "DIV"):
            if (val2 == 0):
                result = "Error: Division by zero"
            else:
                result = int(val1 / val2)

        # gets the remainder of num1/num2
        if (op == "MOD"):
            if (val2 == 0):
                result = "Error: Division by zero"
            else:
                result = int(val1 % val2)

        return result
    
    def calculate_mean(self, tokens):
        amount = 0
        
        for item in tokens:
            amount += int(item)
            
        return int(amount / len(tokens))

    def calculate_exponents(self, val1, val2, op):
        if (op == "RAISE"):
            return val1 ** val2 
        
        if (op == "ROOT"):
            return int(val2 ** (1/val1))

    def check_globals_for_duplicate(self, variable_name, data_type):
        for key in self.global_variables[data_type]:
            if (key == variable_name):
                self.throw_error("Duplicate variable declaration")

    def store_variable(self, data_type, variable_name, value):
        if (len(self.global_variables["int"]) > 0):
            self.check_globals_for_duplicate(variable_name, "int")
        
        if (len(self.global_variables["str"]) > 0):
            self.check_globals_for_duplicate(variable_name, "str")
        
        self.global_variables[data_type][variable_name] = value
    
    def throw_error(self, message):
        line = " ".join(self.tokens)
        print("\n{} at Line number [{}]".format(message, self.line_num))
        print("{}\n\n".format(line))

        raise Exception(message)
    
    def execute(self):
        should_display = False
        
        self.push_tokens(self.tokens)
        token_stack = []
        token_stack_type = ""      # if int and str values are detected in a line, no bueno in INTERPOL

        last_item = self.peek_token(len(self.expr_stack) - 1)

        if (self.validate_lexeme(last_item) == "MARKER"):
            self.expr_stack = []
        else:
            while len(self.expr_stack) >= 1:
                value = self.pop_token()
                literal_type = self.validate_literal(value)
                lexeme_type = self.validate_lexeme(value)
                is_identifier = self.is_identifier(value)

                print(literal_type, lexeme_type, is_identifier)
                # operations
                if (literal_type == "int"):
                    if (len(token_stack) > 0 and token_stack_type == "str"):
                        self.throw_error("Invalid arithmetic operation")
                    else:
                        if (len(token_stack) == 0):
                            token_stack_type = literal_type
                        
                        token_stack.append(value)
                elif (literal_type == "str"):
                    if (len(token_stack) > 0 and token_stack_type == "int"):
                        self.throw_error("Invalid expression")
                    else:
                        if (len(token_stack) == 0):
                            token_stack_type = literal_type

                        token_stack.append(value)
                elif (lexeme_type != False):
                    
                    #declaring int no initial value
                    if (lexeme_type == "DECLARE_INT" or lexeme_type == "DECLARE_STR"):
                        data_type = "int" if lexeme_type == "DECLARE_INT" else "str"
                        variable_name = token_stack.pop()
                        value = ""

                        self.store_variable(data_type, variable_name, value)
                        
                        print("self.global_variables ======")
                        print(self.global_variables)
                    # mean
                    if (lexeme_type == "ADV2_OP"):
                        result = self.calculate_mean(token_stack)
                        token_stack.clear()
                        token_stack.append(str(result))
                    
                    # dealing with exponents
                    if (lexeme_type == "ADV1_OP"):
                        val_1 = token_stack.pop()
                        val_2 = token_stack.pop()
                        result = self.calculate_exponents(int(val_1), int(val_2), value)
                        token_stack.append(str(result))
                    
                    # basic operations
                    if (lexeme_type == "BASIC_OP"):
                        val_1 = token_stack.pop()
                        val_2 = token_stack.pop()
                        result = self.calculate_basic_math(int(val_1), int(val_2), value)
                        token_stack.append(str(result))
                        
                    if (lexeme_type == "OUTPUT"):
                        should_display = True
                        
                        if (value == "PRINTLN"):
                            new_token = token_stack.pop() + "\n"
                            token_stack.append(new_token)
                elif (is_identifier == True):
                    token_stack.append(value)
        
        return token_stack.pop() if should_display == True else None

                
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
        
        #
        #   TODO: BUGGY GROUPING OF STRINGS!!!!!!
        #
        # if (len(new_tokens) > 1):
        #     new_tokens = self.group_parentheses(new_tokens)

        return new_tokens
    
# 
#   Main class for the program
#
class Interpreter:
    # Keywords and reserved words are listed here.
    # ASCII printable characters will be checked through ord() 
    def __init__(self):
        self.global_variables = {
            "int": {},
            "str": {}
        }

        self.error_messages = {
            "INVALID_FILE": "Invalid File",
            "FILE_EMPTY": "File is empty",
            "FILE_NOT_FOUND": "File not found"
        }

    # Checks for file-related errors
    def validate_file(self, filename):
        proceed = True
        error_message = ""

        try:
            if (filename.find(".ipol") == -1):                    # If file is invalid - does not end in .ipol
                error_message = self.error_messages["INVALID_FILE"]
                proceed = False
            elif (os.path.exists(filename) == False):             # If file does not exist - size of the file in bytes is 0
                error_message = self.error_messages["FILE_NOT_FOUND"]
                proceed = False
            elif (os.stat(filename).st_size == 0):                # If file is empty
                error_message = self.error_messages["FILE_EMPTY"]
                proceed = False
            
            if (proceed == False):
                print(error_message + "\n")
                raise(error_message)
        except FileNotFoundError:
            pass

        return True

    def display_output(self, output_list):
        print("----------------  OUTPUT START  ---------------->")
        output = list(filter(None, output_list))
        output = "".join(output)
        print(output)
        print("<----------------- OUTPUT END -------------------")

    # Runs the program and asks for a file input to evalute
    def execute(self):
        filename = ""
        count = 0
        output_list = []

        print("========  INTERPOL INTERPRETER STARTED   ========\n")

        #
        #   @TODO: Add runtime errors
        #
        filename = input("Enter INTERPOL file: ")
        is_valid_program = self.validate_file(filename)

        with open(filename, "r") as f:
            for line in f:
                count += 1
                
                if (count == 1 and line != "BEGIN"):
                    is_valid_program = False
                else:
                    tokenGenerator = TokenGenerator()
                    tokens = tokenGenerator.execute(line)
                    # BUGGY ang pag parse sa string ;(
                    
                    evaluator = ExpressionsEvaluator(tokens, count, self.global_variables)
                    result = evaluator.execute()
                    output_list.append(result)
        
        print("\n================ INTERPOL OUTPUT ================\n")
        self.display_output(output_list)

# Starts the program
interpreter = Interpreter()
interpreter.execute()