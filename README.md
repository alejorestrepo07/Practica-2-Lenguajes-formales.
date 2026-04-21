# Formal Languages - Assignment 2
# Finite Automata

## Name
Alejandro Restrepo

## System Information
- OS: Windows 11
- Language: Python 3.13.5
- Tools: VS Code / Terminal

## How to Run
1. Open terminal
2. Navigate to project folder
3. Run:
   python main.py
4. The program will display a menu with the following options:
- Test Automaton 1 (Identifier Recognition)
- Test Automaton 2 (Keyword "then")
- Run automatic tests
- Exit

5. Enter a string when prompted to test the automata

## Explanation of the code

### What the program does:

This program simulates two Deterministic Finite Automata (DFA) used in lexical analysis to recognize:

- Identifiers (variables)
- Keywords (specifically the word "then")

Each automaton processes the input string character by character and determines whether it is accepted or rejected based on its transition rules.

---

## DFA 1 – Identifier Recognition

### Structure:

States:
- 9 → Initial state  
- 10 → Reading identifier (loop state)  
- 11 → Accepting state  

Alphabet:
- Letters (a–z, A–Z)  
- Digits (0–9)  
- Other symbols  

Accepting States:
- 10 (valid identifier ends)  
- 11 (identifier followed by non-alphanumeric character)  

---

### Transition Logic:

- From state 9:
  - letter → 10  
- From state 10:
  - letter/digit → 10 (loop)  
  - other → 11  

---

### Program Behavior:

1. Reads input character by character  
2. Validates identifier structure  
3. Assigns token (TOKEN_0, TOKEN_1, ...)  
4. Stores identifier in symbol table  

---

## DFA 2 – Keyword Recognition ("then")

### Structure:

States:
- inicio  
- t  
- h  
- e  
- n  
- accepting  

Accepting States:
- accepting  
- n (if input ends exactly at "then")  

---

### Transition Logic:

- inicio → t  
- t → h  
- h → e  
- e → n  
- n → other → accepting  

---

### Program Behavior:

1. Matches exact sequence "then"  
2. Rejects invalid sequences  
3. Accepts valid keyword  

---

## Program Logic

1. Input is read  
2. Characters are classified  
3. State transitions are applied  
4. Output shows transitions and result  
5. Identifiers are stored with tokens  

---

## Example

Input:
```
variable1
```

Output:
- Accepted identifier
- Token assigned

---

## Conclusion

This program demonstrates how DFA are used in lexical analysis to recognize identifiers and keywords efficiently.
