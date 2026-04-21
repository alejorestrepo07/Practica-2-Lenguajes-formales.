class FiniteAutomata1:
    def __init__(self):
        self.current_state = 9
        self.accepting_state = 11
        self.symbol_table = {}  # Maps identifiers to tokens
        self.token_counter = 0
        self.current_identifier = ""
        self.transitions = []  # Log of transitions
    
    def get_next_token(self): #Generate a new token
        
        token = f"TOKEN_{self.token_counter}"
        self.token_counter += 1
        return token
    
    def install_identifier(self, identifier): #add identifier to symbol table and assign token
        
        if identifier not in self.symbol_table:
            token = self.get_next_token()
            self.symbol_table[identifier] = token
        return self.symbol_table[identifier]
    
    def transition(self, char): #Perform state transition based on character. Returns True if transition is valid, False otherwise.
        
        char_type = self._classify_char(char)
        
        if self.current_state == 9:  # Start state
            if char_type == "letter":
                self.current_state = 10
                self.current_identifier = char
                self.transitions.append(f"9 --{char}({char_type})--> 10")
                return True
            else:
                self.transitions.append(f"9 --{char}({char_type})--> REJECT")
                return False
        
        elif self.current_state == 10:  # Reading identifier
            if char_type in ["letter", "digit"]:
                self.current_identifier += char
                self.transitions.append(f"10 --{char}({char_type})--> 10")
                return True
            elif char_type == "other":
                self.current_state = 11
                self.transitions.append(f"10 --{char}({char_type})--> 11")
                return True
            else:
                return False
        
        return False
    
    def process(self, text): #Process input text character by character
        
        self.current_state = 9
        self.current_identifier = ""
        self.transitions = []
        
        for char in text:
            if not self.transition(char):
                break
        
        # Accept if in state 10 (valid identifier) or state 11 (accepting)
        return self.current_state in [10, 11]
    
    def accepted(self): #Check if automaton is in accepting state
        
        return self.current_state == self.accepting_state
    
    def get_identifier(self):
        """Return the identifier that was read"""
        return self.current_identifier
    
    @staticmethod
    def _classify_char(char): #Classify a character as letter, digit, or other

        if char.isalpha():
            return "letter"
        elif char.isdigit():
            return "digit"
        else:
            return "other"


class FiniteAutomata2:
    def __init__(self):
        self.current_state = "inicio"
        self.accepting_state = "accepting"
        self.word_buffer = ""
        self.transitions = []  # Log of transitions
        
        # State transition table
        self.state_transitions = {
            "inicio": {"t": "t"},
            "t": {"h": "h"},
            "h": {"e": "e"},
            "e": {"n": "n"},
            "n": {"other": "accepting"},
            "accepting": {}
        }
    
    def transition(self, char): #Perform state transition based on character. Returns True if transition is valid, False otherwise.
        
        char_type = self._classify_char(char)
        
        if self.current_state == "inicio":
            if char == "t":
                self.current_state = "t"
                self.word_buffer = "t"
                self.transitions.append(f"inicio --t(letter)--> t")
                return True
            else:
                self.transitions.append(f"inicio --{char}({char_type})--> REJECT")
                return False
        
        elif self.current_state == "t":
            if char == "h":
                self.current_state = "h"
                self.word_buffer += "h"
                self.transitions.append(f"t --h(letter)--> h")
                return True
            else:
                self.transitions.append(f"t --{char}({char_type})--> REJECT")
                return False
        
        elif self.current_state == "h":
            if char == "e":
                self.current_state = "e"
                self.word_buffer += "e"
                self.transitions.append(f"h --e(letter)--> e")
                return True
            else:
                self.transitions.append(f"h --{char}({char_type})--> REJECT")
                return False
        
        elif self.current_state == "e":
            if char == "n":
                self.current_state = "n"
                self.word_buffer += "n"
                self.transitions.append(f"e --n(letter)--> n")
                return True
            else:
                self.transitions.append(f"e --{char}({char_type})--> REJECT")
                return False
        
        elif self.current_state == "n":
            if char_type == "other":
                self.current_state = "accepting"
                self.transitions.append(f"n --{char}({char_type})--> accepting")
                return True
            else:
                self.transitions.append(f"n --{char}({char_type})--> REJECT")
                return False
        
        return False
    
    def process(self, text): #Process input text character by character
        
        self.current_state = "inicio"
        self.word_buffer = ""
        self.transitions = []
        last_transition_succeeded = True
        
        for char in text:
            if not self.transition(char):
                last_transition_succeeded = False
                break
        
        # Accept if:
        # - In state "accepting" (completed "then" + non-letter/non-digit), OR
        # - In state "n" (completed "then") AND all characters were processed
        if self.current_state == "accepting":
            return True
        elif self.current_state == "n" and last_transition_succeeded:
            return True
        else:
            return False
    
    def accepted(self): #Check if automaton is in accepting state
        
        return self.current_state == self.accepting_state
    
    @staticmethod
    def _classify_char(char): #Classify a character as letter, digit, or other
        
        if char.isalpha():
            return "letter"
        elif char.isdigit():
            return "digit"
        else:
            return "other"


# Global persistent instances
global_automata1 = FiniteAutomata1()
global_automata2 = FiniteAutomata2()


def test_automata1(): #Test Automaton 1: Identifier Recognition
    
    print("\n" + "=" * 70)
    print("AUTOMATON 1: IDENTIFIER RECOGNITION")
    print("=" * 70)
    
    automata = FiniteAutomata1()
    
    test_cases = [
        "variable1 ",
        "myVar123 ",
        "_invalid",
        "123invalid",
        "test;",
        "x ",
    ]
    
    for test in test_cases:
        automata = FiniteAutomata1()  # Reset for each test
        result = automata.process(test)
        
        print(f"\nInput: '{test}'")
        print(f"Character breakdown: {' + '.join([f'{c}({automata._classify_char(c)})' for c in test])}")
        print("Transitions:")
        for transition in automata.transitions:
            print(f"  {transition}")
        
        if result:
            identifier = automata.get_identifier()
            token = automata.install_identifier(identifier)
            print(f"✅ ACCEPTED")
            print(f"   Identifier: '{identifier}'")
            print(f"   Token: {token}")
            print(f"   Symbol table: {automata.symbol_table}")
        else:
            print(f"❌ REJECTED")


def test_automata2(): #Test Automaton 2: Keyword Recognition ("then")
    
    print("\n" + "=" * 70)
    print("AUTOMATON 2: KEYWORD RECOGNITION ('then')")
    print("=" * 70)
    
    test_cases = [
        "then ",
        "then;",
        "then1",
        "then_var",
        "the ",
        "theme ",
        "thena",
    ]
    
    for test in test_cases:
        automata = FiniteAutomata2()  # Reset for each test
        result = automata.process(test)
        
        print(f"\nInput: '{test}'")
        print(f"Character breakdown: {' + '.join([f'{c}({automata._classify_char(c)})' for c in test])}")
        print("Transitions:")
        for transition in automata.transitions:
            print(f"  {transition}")
        
        if result:
            print(f"✅ ACCEPTED (valid keyword 'then')")
        else:
            print(f"❌ REJECTED")


def interactive_test_automata1(): #Interactive mode for Automaton 1
    
    global global_automata1
    
    print("\n" + "=" * 70)
    print("INTERACTIVE MODE: AUTOMATON 1 (IDENTIFIER RECOGNITION)")
    print("=" * 70)
    print("Enter text to test if it's a valid identifier.")
    print("(Identifier must start with a letter, can contain letters/digits)")
    print("Type 'back' to return to menu.\n")
    
    while True:
        user_input = input("Enter text: ").rstrip('\n')
        
        if user_input.lower() == "back":
            break
        
        if not user_input:
            print("⚠️  Please enter some text.\n")
            continue
        
        # Use persistent global instance
        automata = global_automata1
        result = automata.process(user_input)
        
        print(f"\nInput: '{user_input}'")
        print(f"Character breakdown: {' + '.join([f'{c}({automata._classify_char(c)})' for c in user_input])}")
        print("Transitions:")
        for transition in automata.transitions:
            print(f"  {transition}")
        
        if result:
            identifier = automata.get_identifier()
            token = automata.install_identifier(identifier)
            print(f"✅ ACCEPTED")
            print(f"   Identifier: '{identifier}'")
            print(f"   Token: {token}")
            print(f"   Symbol table: {automata.symbol_table}\n")
        else:
            print(f"❌ REJECTED\n")


def interactive_test_automata2(): #Interactive mode for Automaton 2
    
    global global_automata2
    
    print("\n" + "=" * 70)
    print("INTERACTIVE MODE: AUTOMATON 2 (KEYWORD 'then')")
    print("=" * 70)
    print("Enter text to test if it's the keyword 'then'.")
    print("('then' can end at 'n' or be followed by non-letter/non-digit)")
    print("Type 'back' to return to menu.\n")
    
    while True:
        user_input = input("Enter text: ").rstrip('\n')
        
        if user_input.lower() == "back":
            break
        
        if not user_input:
            print("⚠️  Please enter some text.\n")
            continue
        
        # Use persistent global instance
        automata = global_automata2
        result = automata.process(user_input)
        
        print(f"\nInput: '{user_input}'")
        print(f"Character breakdown: {' + '.join([f'{c}({automata._classify_char(c)})' for c in user_input])}")
        print("Transitions:")
        for transition in automata.transitions:
            print(f"  {transition}")
        
        if result:
            print(f"✅ ACCEPTED (valid keyword 'then')\n")
        else:
            print(f"❌ REJECTED\n")


def menu(): 
    
    while True:
        print("\n" + "=" * 70)
        print("DETERMINISTIC FINITE AUTOMATA (DFA) - LEXICAL ANALYSIS")
        print("=" * 70)
        print("1. Test Automaton 1 (Identifier Recognition) - Interactive")
        print("2. Test Automaton 2 (Keyword 'then') - Interactive")
        print("3. Run automatic tests (Automaton 1)")
        print("4. Run automatic tests (Automaton 2)")
        print("5. Exit")
        print("=" * 70)
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == "1":
            interactive_test_automata1()
        elif choice == "2":
            interactive_test_automata2()
        elif choice == "3":
            test_automata1()
        elif choice == "4":
            test_automata2()
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")


if __name__ == "__main__":
    menu()