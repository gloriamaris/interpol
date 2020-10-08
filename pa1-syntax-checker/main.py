class SyntaxChecker:
    # Keywords and reserved words are listed here.
    # ASCII printable characters will be checked through ord() 
    def __init__(self):
        self.lexicons = {
            "MARKER": ["BEGIN", "END"],
            "DISPLAY": ["PRINT", "PRINTLN"],
            "OPERATOR": ["ADD", "SUB", "MUL", "DIV", "MOD"]
        }

        self.grammar = {
            "COMMENT": "#string",
            "OPERATOR": "OP int int",
            "DISPLAY": "DIS string",
            "MARKER": "MARK"
        }

    # token     <string>
    # order     "start", "end"
    def check_if_marker(self, token, order):
        return True if token in self.lexicons["MARKER"] else False

    # Display welcome message
    def display_welcome_message(self):
        print("INTERPOL Syntax Checker")
        print("Input BEGIN to begin. Input END to end.\n")

    # type      "correct", "incorrect"
    def display_output(self, message_type):
        return "The syntax is " + message_type + "."

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

    # Lexicon checkers
    def check_lexicon(self, token):
        if (self.is_start_marker(token) == True):
            return "MARK"
        if (self.is_operator(token) == True):
            return "OP"
        if (self.is_display_method(token) == True):
            return "DIS"
        if (self.is_number(token) == True):
            return "int"
        if (self.is_string_literal(token) == True):
            return "string"
        if (self.is_comment(token) == True):
            return "#string"

        return False
    
    def filter_comments(self, tokens): 
        new_tokens = []
        index = 0
        commentIndex = 0

        # Find comments and ignore them
        for token in tokens:
            print('token ', token[0])
            if (token[0] == '#'):
                commentIndex = index
                break
            index += 1
        
        new_tokens = tokens[:commentIndex]

        return tokens if len(new_tokens) == 0 else new_tokens
        
    
    def group_parentheses(self, tokens):
        new_tokens = []
        count = 0 
        index = 0
        processed_string = ""
        
        if (len(tokens) == 2):
            second_token = tokens[1]
            if(second_token[0] == '"' and second_token[len(second_token)-1] == '"'):
                return tokens

        # groups the strings by parenthesis
        for token in tokens:
            if (token[0] == '"' or token[len(token)-1] == '"'):
                count += 1
                print(token)
    
            if (count == 1 or count == 2):
                processed_string += token

            if (count == 0 or count == 3):
                new_tokens.append(token)
            
            if count == 2:
                new_tokens.append(processed_string)
                count += 1

        return new_tokens

    def clean_up_line(self, line_of_code):
        tokens = line_of_code.split()

        if (len(tokens) == 1):
            return tokens

        # remove comments first, then group the parentheses
        new_tokens = self.filter_comments(tokens)
        new_tokens = self.group_parentheses(new_tokens)

        return new_tokens

    def check_syntax(self, line_of_code):
        tokens = self.clean_up_line(line_of_code)
        
        is_valid_syntax = True
        is_valid_grammar = False
        produced_grammar = []

        # the entire line is a comment
        if (len(tokens) == 0):
            return True

        # generate the grammar produced from the line of code
        for token in tokens:
            keyword = self.check_lexicon(token)
            if (keyword == False):
                is_valid_syntax = False
                break
                
            produced_grammar.append(keyword)

        final_grammar = " ".join(produced_grammar) 
        print(final_grammar)
        
        # compare to the list of valid grammars
        for key, val in self.grammar.items():
            if (val == final_grammar):
                is_valid_grammar = True

        return True if (is_valid_grammar and is_valid_syntax) else False

    def execute(self):
        is_valid_program = True
        begin_message_displayed = False
        should_begin = False

        self.display_welcome_message()

        while (is_valid_program):
            line_of_code = input()
            if (line_of_code == "BEGIN"):
                should_begin = True
            
            if (should_begin and line_of_code == "END"):
                is_valid_program = False

            if (should_begin):
                if (begin_message_displayed == False):
                    message = self.display_output("correct")
                    print(message + " Beginning syntax checker.")
                    begin_message_displayed = True
                else:
                    is_syntax_valid = self.check_syntax(line_of_code)
                    message_type = "correct" if is_syntax_valid else "incorrect"
                    print(self.display_output(message_type))

            else:
                self.display_welcome_message()

        print("Thank you for using the syntax checker")

# starts the process
syntaxChecker = SyntaxChecker()
syntaxChecker.execute()