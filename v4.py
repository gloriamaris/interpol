import os, re, math


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
        self.tokens_table = []

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
    
    def calculate_dist(self, x1, y1, x2, y2):
        x = int(x2 - x1)
        y = int(y2 - y1)

        distance = math.hypot(x, y)
        return int(distance)

    def calculate_exponents(self, val1, val2, op):
        if (op == "RAISE"):
            return val1 ** val2 
        
        if (op == "ROOT"):
            return int(val2 ** (1/val1))

    def check_globals_for_duplicate(self, variable_name, data_type):
        for key in self.global_variables[data_type]:
            if (key == variable_name):
                return True
            
        return False

    # store global variables
    def store_variable(self, data_type, variable_name, value, should_replace = False):
        exists_int = False
        exists_str = False

        if (data_type == "hold"):
            self.global_variables["hold"] = value
        else:
            if (len(self.global_variables["int"]) > 0):
                exists_int = self.check_globals_for_duplicate(variable_name, "int")
            
            if (len(self.global_variables["str"]) > 0):
                exists_str = self.check_globals_for_duplicate(variable_name, "str")
            
            if ((exists_int == True or exists_str == True) and should_replace == False):
                self.throw_error("Duplicate variable declaration")
            
            self.global_variables[data_type][variable_name] = value
            self.global_variables["last_declared"].clear()
            self.global_variables["last_declared"][data_type] = variable_name

            
    def get_variable(self, data_type = "", variable_name = ""):
        if (data_type == ""):
            exists_int = self.check_globals_for_duplicate(variable_name, "int")
            data_type = "int" if exists_int == True else "str"

        value = self.global_variables[data_type][variable_name] if data_type == "int" else self.global_variables[data_type][variable_name].replace('"', "")
        return value
    
    def get_hold_value(self):
        hold_value = self.global_variables["hold"]
        self.global_variables["hold"] = ""

        return hold_value
    
    def throw_error(self, message):
        line = " ".join(self.tokens)
        print("\n{} at Line number [{}]".format(message, self.line_num))
        print("{}\n\n".format(line))

        raise Exception(message)
    
    def push_to_tokens_table(self, token_type, lexeme_value):
        row = str(self.line_num) + "\t\t" + str(token_type) + str(lexeme_value)
        self.tokens_table.append(row)
    
    def execute(self):
        self.push_tokens(self.tokens)
        token_stack = []
        token_stack_type = ""      # if int and str values are detected in a line, no bueno in INTERPOL
        
        if (len(self.tokens) == 0):
            self.push_to_tokens_table("END_OF_STATEMENT\t\t", "EOS")

        else:
        
            last_item = self.peek_token(len(self.expr_stack) - 1)
            
            if (self.validate_lexeme(last_item) == "MARKER"):
                self.expr_stack = []
            else:
                while len(self.expr_stack) >= 1:
                    value = self.pop_token()
                    literal_type = self.validate_literal(value)
                    lexeme_type = self.validate_lexeme(value)
                    is_identifier = self.is_identifier(value)

                    # processing literal values
                    if (literal_type == "int"):
                        if (len(token_stack) > 0 and token_stack_type == "str"):
                            self.throw_error("Invalid arithmetic operation")
                        else:
                            if (len(token_stack) == 0):
                                token_stack_type = literal_type
                            
                            token_stack.append(value)
                            self.push_to_tokens_table("NUMBER\t\t\t\t", value)
                    elif (literal_type == "str"):
                        if (len(token_stack) > 0 and token_stack_type == "int"):
                            self.throw_error("Invalid expression")
                        else:
                            if (len(token_stack) == 0):
                                token_stack_type = literal_type

                            token_stack.append(value)
                            self.push_to_tokens_table("STRING\t\t\t\t", value)
                    # processing lexemes
                    elif (lexeme_type != False):
                        # asking for user input
                        if (lexeme_type == "INPUT"):
                            variable_name = token_stack.pop()
                            exists_int = self.check_globals_for_duplicate(variable_name, "int")
                            exists_str = self.check_globals_for_duplicate(variable_name, "str")
                            
                            if (exists_int == False and exists_str == False):
                                self.throw_error("Variable is not declared")
                            else:
                                data_type = "int" if exists_int == True else "str"
                                should_replace = True
                                value = input()
                                
                                self.store_variable(data_type, variable_name, value, should_replace)
                                self.push_to_tokens_table("INPUT\t\t\t\t", value)
                                self.push_to_tokens_table("IDENTIFIER\t\t\t", variable_name)
                            
                        # when assign connector (IN) is detected, store the variable name to HOLD
                        if (lexeme_type == "ASSIGN_CONNt"):
                            variable_name = token_stack.pop()
                            exists_int = self.check_globals_for_duplicate(variable_name, "int")
                            exists_str = self.check_globals_for_duplicate(variable_name, "str")
                            
                            if (exists_int == False and exists_str == False):
                                self.throw_error("Variable is not declared")
                            else:
                                self.store_variable("hold", "", variable_name)
                                self.push_to_tokens_table("ASSIGN_VAR_KEY\t\t", value)
        
                        # assigning value to a variable
                        if (lexeme_type == "ASSIGN"):
                            value = token_stack.pop()
                            variable_name = self.get_hold_value()
                            
                            # wrong syntax or someth
                            if (variable_name == ""):
                                self.throw_error("Invalid syntax")

                            # only checks if type is int. INTERPOL only has 2 data types anyway
                            exists_int = self.check_globals_for_duplicate(variable_name, "int")
                            data_type = "int" if exists_int == True else "str"
                            should_replace = True

                            self.store_variable(data_type, variable_name, value, should_replace)
                            self.push_to_tokens_table("ASSIGN_KEY\t\t\t\t", value)

                        #declaring with initial value
                        if (lexeme_type == "DECLARE_CONN"):
                            value = token_stack.pop()
                            self.store_variable("hold", "", value)
                            self.push_to_tokens_table("DECLARATION_ASSIGN_WITH_KEY\t", value)
                            
                        #declaring int no initial value
                        if (lexeme_type == "DECLARE_INT" or lexeme_type == "DECLARE_STR"):
                            data_type = "int" if lexeme_type == "DECLARE_INT" else "str"
                            variable_name = token_stack.pop()
                            value = ""
                            
                            value = self.get_hold_value()
                            
                            self.store_variable(data_type, variable_name, value)
                            key = "DECLARATION_INT\t\t\t" if lexeme_type == "DECLARE_INT" else "DECLARATION_STRING\t\t"
                            self.push_to_tokens_table(key, value)

                        # distance between two points
                        if (lexeme_type == "ADV3_OP"):
                            y2 = int(token_stack.pop())
                            x2 = int(token_stack.pop())
                            y1 = int(token_stack.pop())
                            x1 = int(token_stack.pop())

                            result = self.calculate_dist(x1, y1, x2, y2)
                            token_stack.append(str(result))
                            self.push_to_tokens_table("ADVANCED_OPERATOR_DIST\t\t", value)
                        
                        # detecting the distance connector lexeme AND
                        # and not sure what to do with it
                        if (lexeme_type == "ADV3_OP_CONN"):
                            self.push_to_tokens_table("DISTANCE_OPERATOR\t\t", value)
                            pass
                        
                        # mean
                        if (lexeme_type == "ADV2_OP"):
                            result = self.calculate_mean(token_stack)
                            token_stack.clear()
                            token_stack.append(str(result))
                            self.push_to_tokens_table("ADVANCED_OPERATOR_AVE\t\t", value)
                        
                        # dealing with exponents
                        if (lexeme_type == "ADV1_OP"):
                            val_1 = token_stack.pop()
                            val_2 = token_stack.pop()
                            result = self.calculate_exponents(int(val_1), int(val_2), value)
                            token_stack.append(str(result))
                            
                            key = "ADVANCED_OPERATOR_EXP\t\t" if value == "RAISE" else "ADVANCED_OPERATOR_ROOT\t\t"
                            self.push_to_tokens_table(key, value)
                        
                        # basic operations
                        if (lexeme_type == "BASIC_OP"):
                            val_1 = token_stack.pop()
                            val_2 = token_stack.pop()
                            result = self.calculate_basic_math(int(val_1), int(val_2), value)
                            token_stack.append(str(result))
                            
                            self.push_to_tokens_table("BASIC_OPERATOR" + value + "\t\t", value)
                            
                        if (lexeme_type == "OUTPUT"):
                            should_display = True
                            
                            new_token = token_stack.pop()

                            if (self.is_number == False and  self.is_identifier(new_token) == True):
                                new_token = self.get_variable("", new_token)

                            token_stack.append(new_token)
                            new_token = new_token.replace('"', "")

                            if (value == "PRINTLN"):
                                self.push_to_tokens_table("OUTPUT_WITH_LINE\t\t", value)
                                print(new_token)
                            else:
                                self.push_to_tokens_table("OUTPUT\t\t\t\t", value)
                                print(new_token, end = "")
                            
                    elif (is_identifier == True):
                        token_stack.append(value)
                        self.push_to_tokens_table("IDENTIFIER\t\t\t", value)
                        
                    self.push_to_tokens_table("END_OF_STATEMENT\t\t", "EOS")
        
        return self.tokens_table

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
        #   check for computations with:
        #   string_val int_val
        #
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
        self.global_variables = {
            "last_declared": {},
            "hold": "",
            "int": {},
            "str": {}
        }
        
        self.lexemes_tokens_list = []

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
        output = list(filter(None, output_list))
        output = "".join(output)
        print(output)
    
    def display_tokens_table(self, accumulated_tokens):
        print("\n\n========= INTERPOL LEXEMES/TOKENS TABLE =========")
        print("\n\nLINE NO.\tTOKENS\t\t\t\tLEXEMES")
        
        print("1\t\tPROGRAM_BEGIN\t\t\tBEGIN")
        print("1\t\tEND_OF_STATEMENT\t\tEOS")

        line_count = 0

        for item in accumulated_tokens:
            index = 0

            while index < len(item):
                print(item[index])
                tokens = item[index].split("\t")
                line_count = int(tokens[0])
                index += 1

        line_count += 1
        print(str(line_count) + "\t\tPROGRAM_END\t\t\tEND")
        line_count += 1
        print(str(line_count) + "\t\tEND_OF_FILE\t\t\tEOF")
    
    def display_symbols_table(self):
        print("\n\n================= SYMBOLS TABLE =================")
        print("\n\nVARIABLE_NAME\t\tTYPE\t\t\tVALUE")
        
        intVariables = self.global_variables["int"]
        strVariables = self.global_variables["str"]

        if (len(intVariables) > 0):
            for key in intVariables:
                print(key + "\t\t\t" + "INTEGER\t\t\t" + intVariables[key])
        
        if (len(strVariables) > 0):
            for key in strVariables:
                print(key + "\t\t\t" + "STRING\t\t\t" + strVariables[key])

    def throw_error(self, message, line, line_num):
        print("\n{} at Line number [{}]".format(message, line_num))
        print("{}\n\n".format(line))

        raise Exception(message)

    # Runs the program and asks for a file input to evalute
    def execute(self):
        filename = ""
        count = 0
        accumulated_tokens = []

        print("========  INTERPOL INTERPRETER STARTED   ========\n")

        #
        #   @TODO: Add runtime errors
        #
        filename = input("Enter INTERPOL file: ")
        is_valid_program = self.validate_file(filename)

        print("\n================ INTERPOL OUTPUT ================\n")

        print("----------------  OUTPUT START  ---------------->\n")
        with open(filename, "r") as f:
            for line in f:
                count += 1
                
                #
                #   TODO: Add error trap here if the program does not start with BEGIN
                #

                if (count == 1 and line.strip() != "BEGIN"):
                    self.throw_error("Invalid file", line, count)
                else:
                    tokenGenerator = TokenGenerator()
                    tokens = tokenGenerator.execute(line)

                    # BUGGY ang pag parse sa string ;(
                    
                    evaluator = ExpressionsEvaluator(tokens, count, self.global_variables)
                    tokens = evaluator.execute()
                    accumulated_tokens.append(tokens)
            
        print("\n<----------------- OUTPUT END -------------------")
        
        #   printing of the lexemes table
        self.display_tokens_table(accumulated_tokens)
        # printing of symbols table
        self.display_symbols_table()
            
        
        print("\n\n======== INTERPOL INTERPRETER TERMINATED ========")

# Starts the program
interpreter = Interpreter()
interpreter.execute()