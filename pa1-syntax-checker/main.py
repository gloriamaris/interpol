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

    # Lexicon checkers
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
    
    def check_ascii(self, token):
        return len(token) == len(token.encode())

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
        
        return False
    
    def check_syntax(self, line_of_code):
        tokens = line_of_code.split()
        index = 0
        is_valid_syntax = True
        is_valid_grammar = False
        produced_grammar = []

        print("tokens", tokens)

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

syntaxChecker = SyntaxChecker()
syntaxChecker.execute()