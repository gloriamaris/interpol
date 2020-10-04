class SyntaxChecker:
    # Keywords and reserved words are listed here.
    # ASCII printable characters will be checked through ord() 
    def __init__(self):
        self.lexicons = {
            "markers": ['BEGIN', 'END'],
            "display_methods": ['PRINT', 'PRINTLN'],
            "operators": ['ADD', 'SUB', 'MUL', 'DIV']
        }

    # token     <string>
    # order     "start", "end"
    def check_if_marker(self, token, order):
        return True if token in self.lexicons["markers"] else False

    # Display welcome message
    def display_welcome_message(self):
        print("INTERPOL Syntax Checker")
        print("Input BEGIN to begin. Input END to end.\n")

    # type      "correct", "incorrect"
    def display_output(self, message_type):
        return "The syntax is " + message_type + "."

    def proceed_execution(self, token):
        return True if self.check_lexicon(token) else False
    # Checks if valid lexicons
    def check_lexicon(self, token):
        is_start_marker = self.check_if_marker(token, 'start')
        is_operator = True if token in self.lexicons["operators"] else False
        is_display_method = True if token in self.lexicons["display_methods"] else False

        return True if (is_start_marker or is_operator or is_display_method) else False

    def execute(self):
        line = 0
        is_valid_program = True
        begin_message_displayed = False
        should_begin = False

        self.display_welcome_message()

        while (is_valid_program):
            line_of_code = input()
            if (line_of_code == 'BEGIN'):
                should_begin = True
            
            if (should_begin and line_of_code == 'END'):
                is_valid_program = False

            if (should_begin):
                if (begin_message_displayed == False):
                    message = self.display_output('correct')
                    print(message + " Beginning syntax checker.")
                    begin_message_displayed = True
                else:
                    is_syntax_valid = self.proceed_execution(line_of_code)
                    message_type = "correct" if is_syntax_valid else "incorrect"
                    print(self.display_output(message_type))

            else:
                self.display_welcome_message()

        print("Thank you for using the syntax checker")

syntaxChecker = SyntaxChecker()
syntaxChecker.execute()