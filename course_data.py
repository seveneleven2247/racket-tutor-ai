from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Lesson:
    day: int
    category: str
    week: int
    title: str
    goal: str
    cpp_bridge: str
    explanation: str
    syntax_bridge: dict
    official_docs: list[dict[str, str]]
    racket_focus: list[str]
    code: str
    line_notes: list[dict]
    practice: list[str]
    checklist: list[str]
    assignment: str
    grading_rubric: list[str]


TARGET_LANGUAGES = {
    "cpp": {"id": "cpp", "name": "C++", "file_ext": "cpp", "runner": "c++ day01.cpp -std=c++17 -o day01 && ./day01"},
    "racket": {"id": "racket", "name": "Racket", "file_ext": "rkt", "runner": "racket day01.rkt"},
    "python": {"id": "python", "name": "Python", "file_ext": "py", "runner": "python3 day01.py"},
    "c": {"id": "c", "name": "C", "file_ext": "c", "runner": "cc day01.c -o day01 && ./day01"},
    "java": {"id": "java", "name": "Java", "file_ext": "java", "runner": "javac Day01.java && java Day01"},
}


DOCS = {
    "cpp": [
        {"title": "C++ Reference", "url": "https://en.cppreference.com/w/cpp"},
        {"title": "C++ Language", "url": "https://en.cppreference.com/w/cpp/language"},
    ],
    "racket": [
        {"title": "Racket Documentation", "url": "https://docs.racket-lang.org/index.html"},
        {"title": "The Racket Guide", "url": "https://docs.racket-lang.org/guide/index.html"},
    ],
    "python": [
        {"title": "Python Tutorial", "url": "https://docs.python.org/3/tutorial/"},
        {"title": "Python Language Reference", "url": "https://docs.python.org/3/reference/"},
    ],
    "c": [
        {"title": "C Reference", "url": "https://en.cppreference.com/w/c"},
        {"title": "C Language", "url": "https://en.cppreference.com/w/c/language"},
    ],
    "java": [
        {"title": "Dev.java Learn", "url": "https://dev.java/learn/"},
        {"title": "Java API Documentation", "url": "https://docs.oracle.com/en/java/javase/"},
    ],
}


TOPICS = [
    ("Output", "output"),
    ("Input", "input"),
    ("Math Calculation", "math"),
    ("Declare and Initialize a Variable", "variable"),
    ("If Statement", "if_statement"),
    ("Else-If Statement", "else_if"),
    ("Error Check", "error_check"),
    ("While Loops", "while_loop"),
    ("Do-While Loop", "do_while"),
    ("Random Number", "random_number"),
    ("For Loops", "for_loop"),
    ("Nested For Loops", "nested_for"),
    ("What Is a Method or Function?", "function_intro"),
    ("Create Functions", "create_function"),
    ("Use and Call Functions", "call_function"),
    ("What Is an Array?", "arrays_intro"),
    ("Different Kinds of Arrays", "array_kinds"),
    ("Declare and Initialize Arrays", "array_declare"),
    ("Create Strings", "strings"),
    ("Character Arrays", "char_arrays"),
    ("Classes", "classes"),
    ("Switch Statement", "switch_statement"),
    ("Multiple Dimensions of Arrays", "multi_arrays"),
    ("Vectors", "vectors"),
    ("Objects and Classes", "objects_classes"),
    ("Recursion", "recursion"),
    ("Search and Float Values", "search_float"),
    ("Combine Conditions with If", "combined_if"),
    ("Nested If Statement", "nested_if"),
    ("Combine For Loops with Arrays", "for_arrays"),
    ("Combine Nested For Loops with Multi-Dimensional Arrays", "nested_for_multi"),
    ("Combine While Loops with Input Validation", "while_validation"),
    ("Combine Do-While Loops with Menus", "do_while_menu"),
    ("Review: Output, Input, Variables, and Math", "review_basics"),
    ("Review: Conditions and Error Checks", "review_conditions"),
    ("Review: Loop Patterns", "review_loops"),
    ("Review: Functions and Calls", "review_functions"),
    ("Review: Arrays and Strings", "review_arrays_strings"),
    ("Review: Classes and Objects", "review_objects"),
    ("Review: Search, Float, and Recursion", "review_search_recursion"),
    ("Mini Project: Number Guessing Game", "project_guess"),
    ("Mini Project: Grade Calculator", "project_grade"),
    ("Mini Project: Pattern Printer", "project_pattern"),
    ("Mini Project: Array Statistics", "project_array_stats"),
    ("Mini Project: Text Analyzer", "project_text"),
    ("Mini Project: Student Class", "project_student"),
    ("Mini Project: Menu-Driven App", "project_menu"),
    ("Debugging: Output, Input, and Types", "debug_io_types"),
    ("Testing: Math and Conditions", "testing_math_conditions"),
    ("Testing: Loops and Error Checks", "testing_loops"),
    ("Testing: Functions", "testing_functions"),
    ("Testing: Arrays, Strings, and Vectors", "testing_collections"),
    ("Integrated Practice: Data Table", "integrated_table"),
    ("Integrated Practice: Searchable Records", "integrated_records"),
    ("Capstone Build", "capstone_build"),
    ("Capstone Review and Next Steps", "capstone_review"),
]


KIND_SUMMARIES = {
    "output": "Start with visible program behavior. You print values first so every later topic has a quick feedback loop.",
    "input": "Read text first, then convert it when the program needs a number, boolean, character, decimal, or array/list.",
    "math": "Use arithmetic expressions for totals, averages, remainders, and grouped calculations.",
    "variable": "Bind a name to a value and learn which parts of the syntax are type, name, value, and initialization.",
    "if_statement": "Use one condition to choose whether a block or expression should run.",
    "else_if": "Handle several ordered cases without writing separate unrelated if statements.",
    "error_check": "Reject invalid input before the main logic depends on it.",
    "while_loop": "Repeat while a condition remains true, usually when you do not know the exact count beforehand.",
    "do_while": "Run the body once before checking whether another iteration is needed.",
    "random_number": "Generate unpredictable values for games, tests, and simulations.",
    "for_loop": "Repeat a known number of times with an index or sequence.",
    "nested_for": "Place one loop inside another to work with grids, tables, and repeated patterns.",
    "function_intro": "Understand a function as a named, reusable block that accepts input and returns output.",
    "create_function": "Write your own function with parameters, a body, and a clear result.",
    "call_function": "Use a function by passing arguments and storing or printing the returned value.",
    "arrays_intro": "Store many related values under one name and access elements by position or sequence.",
    "array_kinds": "Compare fixed arrays, dynamic arrays, lists, vectors, and language-specific collection choices.",
    "array_declare": "Create an array-like collection and fill it with starting values.",
    "strings": "Represent text, combine text, and inspect characters or substrings.",
    "char_arrays": "Understand text as a sequence of characters when a language exposes that representation.",
    "classes": "Group data and behavior into a named type.",
    "switch_statement": "Choose one branch from many exact-match cases.",
    "multi_arrays": "Represent rows and columns with nested arrays, vectors, or lists.",
    "vectors": "Use a resizable sequence when the number of elements can grow or shrink.",
    "objects_classes": "Create object values from class definitions and call methods on those objects.",
    "recursion": "Solve a problem by reducing it to a smaller version of itself.",
    "search_float": "Search collections and use floating-point values for measurements and averages.",
    "combined_if": "Combine conditions with and, or, and not so rules read clearly.",
    "nested_if": "Put one if inside another when a decision depends on a previous decision.",
    "for_arrays": "Use for loops to process every element of an array-like collection.",
    "nested_for_multi": "Use nested loops to visit every cell in a multi-dimensional structure.",
    "while_validation": "Keep asking for input until the value passes validation.",
    "do_while_menu": "Show a menu at least once, then continue until the user chooses to stop.",
}


DEFAULT_SUMMARY = "Combine earlier skills into a small program. Keep the code short, testable, and easy to explain line by line."


RACKET_KIND_DETAILS = {
    "output": (
        "`displayln` is Racket's basic output function for beginner programs. "
        "`display` means show a value, and `ln` means add a newline after it. "
        "`(displayln 42)` means: call `displayln` with the numeric value `42`, print `42`, then move to the next line. "
        "The parentheses are required because Racket uses prefix expression syntax: the first item after `(` is the function or operation, and the following items are arguments. "
        "This replaces the C++ habit `std::cout << 42 << std::endl;`. "
        "`#lang racket` is also required at the top of the file because it tells Racket which language rules to use when reading the file."
    ),
    "input": (
        "`display` prints a prompt without moving to a new line. `read-line` waits for the user to type text and press Enter. "
        "`(define name (read-line))` runs `read-line`, then binds the typed text to `name`. "
        "For numbers, Racket usually reads text first and converts it with `string->number`: `(define age (string->number (read-line)))`. "
        "For a boolean, compare the typed text: `(equal? answer \"true\")`. For a character, read a string and take the first character with `string-ref`. "
        "For an array-like input, read one line, split it with `string-split`, then convert each piece with `map string->number`. "
        "To output a sentence with variables, use `format`, for example `(format \"~a is ~a\" name age)`. "
        "Watch out: `read-line` gives a string, `string->number` can return `#f` for bad input, and `string-ref` fails on an empty string."
    ),
    "math": (
        "Racket writes arithmetic in prefix form: `(+ subtotal tax)` means `subtotal + tax`. "
        "The operator comes first, then the numbers or names. Parentheses are required because they mark the exact expression and its arguments."
    ),
    "variable": (
        "`define` binds a name to a value. For a beginner, read `(define count 3)` as `const auto count = 3;` in C++. "
        "Racket usually builds new values instead of repeatedly changing the same variable."
    ),
}


INPUT_TYPE_DETAILS = {
    "cpp": (
        "C++ uses `std::cin >> variable` for simple input. The variable type controls how the text is interpreted: `int` reads an integer, "
        "`double` reads a decimal, `bool` reads `true` or `false` when `std::boolalpha` is used, `char` reads one character, and `std::string` reads one word. "
        "For array/vector input, read one element at a time, such as `scores[0]`, `scores[1]`, and `scores[2]`. "
        "To output a sentence with variables, chain text and values with `<<`. Be careful that `std::cin >> name` stops at whitespace; use `std::getline` later when you need a full sentence."
    ),
    "python": (
        "Python's `input()` always returns a string. Convert it when needed: `int(input(...))` for integers, `float(input(...))` for decimals, "
        "`input(...).lower() == \"true\"` for a boolean, `input(...)[0]` for a character, and `[int(x) for x in input(...).split()]` for a list of numbers. "
        "To output a sentence with variables, an f-string is usually clearest: `f\"{name} is {age}\"`. Be careful: invalid numeric text causes a conversion error, and `[0]` fails on an empty string."
    ),
    "c": (
        "C uses `scanf` with format specifiers. `%d` reads an integer, `%lf` reads a double, `%c` reads one character, `%s` reads a word into a character array, "
        "and arrays are read one element at a time with addresses like `&scores[0]`. C has no beginner-friendly built-in boolean input, so use `int member` with 1 for true and 0 for false. "
        "To output a sentence with variables, use matching `printf` placeholders. Be careful: every `scanf` target except character arrays usually needs `&`, and `scanf(\" %c\", &initial)` uses a leading space to skip old whitespace."
    ),
    "java": (
        "Java commonly uses `Scanner`. Use `nextInt()` for integers, `nextDouble()` for decimals, `nextBoolean()` for booleans, `next().charAt(0)` for one character, "
        "`next()` for one word string, and `int[] scores` with separate `nextInt()` calls for array elements. "
        "To output a sentence with variables, join text and values with `+` or use `System.out.printf`. Be careful mixing `nextLine()` with `nextInt()` later because leftover newline characters can be read accidentally."
    ),
    "racket": RACKET_KIND_DETAILS["input"],
}

SNIPPETS = {
    "output": {
        "cpp": """#include <iostream>

int main() {
    std::cout << "Hello, C++!" << std::endl;
    std::cout << 42 << std::endl;
}""",
        "racket": """#lang racket

(displayln "Hello, Racket!")
(displayln 42)""",
        "python": """print("Hello, Python!")
print(42)""",
        "c": """#include <stdio.h>

int main(void) {
    printf("Hello, C!\\n");
    printf("%d\\n", 42);
    return 0;
}""",
        "java": """public class Day01 {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
        System.out.println(42);
    }
}""",
    },
    "input": {
        "cpp": """#include <iostream>
#include <string>
#include <vector>

int main() {
    std::string name;
    int age;
    double price;
    bool member;
    char initial;
    std::vector<int> scores(3);

    std::cout << "Name: ";
    std::cin >> name;
    std::cout << "Age integer: ";
    std::cin >> age;
    std::cout << "Price decimal: ";
    std::cin >> price;
    std::cout << "Member true/false: ";
    std::cin >> std::boolalpha >> member;
    std::cout << "Initial character: ";
    std::cin >> initial;
    std::cout << "Three integer scores: ";
    std::cin >> scores[0] >> scores[1] >> scores[2];

    std::cout << name << " is " << age << " years old. Price: "
              << price << ". Member: " << std::boolalpha << member
              << ". Initial: " << initial << ". First score: "
              << scores[0] << std::endl;
}""",
        "racket": """#lang racket
(require racket/string)

(display "Name: ")
(define name (read-line))
(display "Age integer: ")
(define age (string->number (read-line)))
(display "Price decimal: ")
(define price (string->number (read-line)))
(display "Member true/false: ")
(define member? (equal? (read-line) "true"))
(display "Initial character: ")
(define initial (string-ref (read-line) 0))
(display "Three integer scores separated by spaces: ")
(define scores (map string->number (string-split (read-line))))

(displayln
 (format "~a is ~a years old. Price: ~a. Member: ~a. Initial: ~a. First score: ~a"
         name age price member? initial (first scores)))""",
        "python": """name = input("Name: ")
age = int(input("Age integer: "))
price = float(input("Price decimal: "))
member = input("Member true/false: ").lower() == "true"
initial = input("Initial character: ")[0]
scores = [int(piece) for piece in input("Three integer scores: ").split()]

print(f"{name} is {age} years old. Price: {price}. Member: {member}. Initial: {initial}. First score: {scores[0]}")""",
        "c": """#include <stdio.h>

int main(void) {
    char name[40];
    int age;
    double price;
    int member;
    char initial;
    int scores[3];

    printf("Name: ");
    scanf("%39s", name);
    printf("Age integer: ");
    scanf("%d", &age);
    printf("Price decimal: ");
    scanf("%lf", &price);
    printf("Member 1/0: ");
    scanf("%d", &member);
    printf("Initial character: ");
    scanf(" %c", &initial);
    printf("Three integer scores: ");
    scanf("%d %d %d", &scores[0], &scores[1], &scores[2]);

    printf("%s is %d years old. Price: %.2f. Member: %d. Initial: %c. First score: %d\\n",
           name, age, price, member, initial, scores[0]);
    return 0;
}""",
        "java": """import java.util.Scanner;

public class Day02 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Name: ");
        String name = input.next();
        System.out.print("Age integer: ");
        int age = input.nextInt();
        System.out.print("Price decimal: ");
        double price = input.nextDouble();
        System.out.print("Member true/false: ");
        boolean member = input.nextBoolean();
        System.out.print("Initial character: ");
        char initial = input.next().charAt(0);
        int[] scores = new int[3];
        System.out.print("Three integer scores: ");
        scores[0] = input.nextInt();
        scores[1] = input.nextInt();
        scores[2] = input.nextInt();

        System.out.println(name + " is " + age + " years old. Price: " + price
            + ". Member: " + member + ". Initial: " + initial
            + ". First score: " + scores[0]);
    }
}""",
    },
    "math": {
        "cpp": """int subtotal = 80;
int tax = 10;
double total = subtotal + tax;""",
        "racket": """#lang racket

(define subtotal 80)
(define tax 10)
(define total (+ subtotal tax))
(define average (/ total 2.0))""",
        "python": """subtotal = 80
tax = 10
total = subtotal + tax
average = total / 2""",
        "c": """int subtotal = 80;
int tax = 10;
double total = subtotal + tax;
double average = total / 2.0;""",
        "java": """int subtotal = 80;
int tax = 10;
double total = subtotal + tax;
double average = total / 2.0;""",
    },
    "variable": {
        "cpp": """int count = 3;
double price = 9.99;
std::string label = "book";""",
        "racket": """#lang racket

(define count 3)
(define price 9.99)
(define label "book")""",
        "python": """count = 3
price = 9.99
label = "book" """,
        "c": """int count = 3;
double price = 9.99;
char label[] = "book";""",
        "java": """int count = 3;
double price = 9.99;
String label = "book";""",
    },
    "if_statement": {
        "cpp": """if (score >= 60) {
    std::cout << "pass";
}""",
        "racket": """#lang racket

(define score 72)
(if (>= score 60)
    (displayln "pass")
    (displayln "try again"))""",
        "python": """score = 72
if score >= 60:
    print("pass")""",
        "c": """int score = 72;
if (score >= 60) {
    printf("pass\\n");
}""",
        "java": """int score = 72;
if (score >= 60) {
    System.out.println("pass");
}""",
    },
    "else_if": {
        "cpp": """if (score >= 90) grade = "A";
else if (score >= 80) grade = "B";
else grade = "Practice";""",
        "racket": """#lang racket

(define score 84)
(define grade
  (cond
    [(>= score 90) "A"]
    [(>= score 80) "B"]
    [else "Practice"]))
(displayln grade)""",
        "python": """score = 84
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "Practice"
print(grade)""",
        "c": """int score = 84;
const char *grade;
if (score >= 90) grade = "A";
else if (score >= 80) grade = "B";
else grade = "Practice";""",
        "java": """int score = 84;
String grade;
if (score >= 90) grade = "A";
else if (score >= 80) grade = "B";
else grade = "Practice";""",
    },
    "error_check": {
        "cpp": """if (count <= 0) {
    throw std::invalid_argument("count must be positive");
}""",
        "racket": """#lang racket

(define (average total count)
  (if (<= count 0)
      (error 'average "count must be positive")
      (/ total count)))""",
        "python": """def average(total, count):
    if count <= 0:
        raise ValueError("count must be positive")
    return total / count""",
        "c": """double average(double total, int count) {
    if (count <= 0) {
        return -1.0;
    }
    return total / count;
}""",
        "java": """static double average(double total, int count) {
    if (count <= 0) {
        throw new IllegalArgumentException("count must be positive");
    }
    return total / count;
}""",
    },
    "while_loop": {
        "cpp": """int n = 3;
while (n > 0) {
    std::cout << n << std::endl;
    n--;
}""",
        "racket": """#lang racket

(let loop ([n 3])
  (when (> n 0)
    (displayln n)
    (loop (- n 1))))""",
        "python": """n = 3
while n > 0:
    print(n)
    n -= 1""",
        "c": """int n = 3;
while (n > 0) {
    printf("%d\\n", n);
    n--;
}""",
        "java": """int n = 3;
while (n > 0) {
    System.out.println(n);
    n--;
}""",
    },
    "do_while": {
        "cpp": """int choice;
do {
    std::cin >> choice;
} while (choice != 0);""",
        "racket": """#lang racket

(let loop ()
  (displayln "menu")
  (define choice "0")
  (unless (string=? choice "0")
    (loop)))""",
        "python": """while True:
    choice = input("0 to quit: ")
    if choice == "0":
        break""",
        "c": """int choice;
do {
    scanf("%d", &choice);
} while (choice != 0);""",
        "java": """int choice;
do {
    choice = input.nextInt();
} while (choice != 0);""",
    },
    "random_number": {
        "cpp": """int number = rand() % 10 + 1;""",
        "racket": """#lang racket

(define number (+ 1 (random 10)))
(displayln number)""",
        "python": """import random

number = random.randint(1, 10)
print(number)""",
        "c": """#include <stdlib.h>

int number = rand() % 10 + 1;""",
        "java": """import java.util.Random;

Random random = new Random();
int number = random.nextInt(10) + 1;""",
    },
    "for_loop": {
        "cpp": """for (int i = 0; i < 5; i++) {
    std::cout << i << std::endl;
}""",
        "racket": """#lang racket

(for ([i (in-range 5)])
  (displayln i))""",
        "python": """for i in range(5):
    print(i)""",
        "c": """for (int i = 0; i < 5; i++) {
    printf("%d\\n", i);
}""",
        "java": """for (int i = 0; i < 5; i++) {
    System.out.println(i);
}""",
    },
    "nested_for": {
        "cpp": """for (int row = 0; row < 3; row++) {
    for (int col = 0; col < 3; col++) {
        std::cout << row << "," << col << std::endl;
    }
}""",
        "racket": """#lang racket

(for* ([row (in-range 3)]
       [col (in-range 3)])
  (displayln (format "~a,~a" row col)))""",
        "python": """for row in range(3):
    for col in range(3):
        print(row, col)""",
        "c": """for (int row = 0; row < 3; row++) {
    for (int col = 0; col < 3; col++) {
        printf("%d,%d\\n", row, col);
    }
}""",
        "java": """for (int row = 0; row < 3; row++) {
    for (int col = 0; col < 3; col++) {
        System.out.println(row + "," + col);
    }
}""",
    },
    "function_intro": {
        "cpp": """int square(int x) {
    return x * x;
}""",
        "racket": """#lang racket

(define (square x)
  (* x x))""",
        "python": """def square(x):
    return x * x""",
        "c": """int square(int x) {
    return x * x;
}""",
        "java": """static int square(int x) {
    return x * x;
}""",
    },
    "create_function": {
        "cpp": """double addTax(double amount) {
    return amount * 1.13;
}""",
        "racket": """#lang racket

(define (add-tax amount)
  (* amount 1.13))""",
        "python": """def add_tax(amount):
    return amount * 1.13""",
        "c": """double add_tax(double amount) {
    return amount * 1.13;
}""",
        "java": """static double addTax(double amount) {
    return amount * 1.13;
}""",
    },
    "call_function": {
        "cpp": """int result = square(5);
std::cout << result;""",
        "racket": """#lang racket

(define (square x) (* x x))
(define result (square 5))
(displayln result)""",
        "python": """def square(x):
    return x * x

result = square(5)
print(result)""",
        "c": """int result = square(5);
printf("%d\\n", result);""",
        "java": """int result = square(5);
System.out.println(result);""",
    },
    "arrays_intro": {
        "cpp": """int scores[3] = {90, 85, 100};
std::cout << scores[0];""",
        "racket": """#lang racket

(define scores (vector 90 85 100))
(displayln (vector-ref scores 0))""",
        "python": """scores = [90, 85, 100]
print(scores[0])""",
        "c": """int scores[3] = {90, 85, 100};
printf("%d\\n", scores[0]);""",
        "java": """int[] scores = {90, 85, 100};
System.out.println(scores[0]);""",
    },
    "array_kinds": {
        "cpp": """std::array<int, 3> fixed = {1, 2, 3};
std::vector<int> dynamic = {1, 2, 3};""",
        "racket": """#lang racket

(define fixed (vector 1 2 3))
(define linked (list 1 2 3))
(define lookup (hash "one" 1))""",
        "python": """fixed_like = (1, 2, 3)
dynamic = [1, 2, 3]
lookup = {"one": 1}""",
        "c": """int fixed[3] = {1, 2, 3};
int dynamic_count = 3;""",
        "java": """int[] fixed = {1, 2, 3};
java.util.ArrayList<Integer> dynamic = new java.util.ArrayList<>();""",
    },
    "array_declare": {
        "cpp": """int values[4] = {0, 1, 2, 3};""",
        "racket": """#lang racket

(define values (vector 0 1 2 3))
(define names (vector "Ada" "Grace"))""",
        "python": """values = [0, 1, 2, 3]
names = ["Ada", "Grace"]""",
        "c": """int values[4] = {0, 1, 2, 3};
char names[2][10] = {"Ada", "Grace"};""",
        "java": """int[] values = {0, 1, 2, 3};
String[] names = {"Ada", "Grace"};""",
    },
    "strings": {
        "cpp": """std::string first = "Ada";
std::string message = "Hi " + first;""",
        "racket": """#lang racket

(define first "Ada")
(define message (string-append "Hi " first))
(displayln message)""",
        "python": """first = "Ada"
message = "Hi " + first
print(message)""",
        "c": """char first[] = "Ada";
printf("Hi %s\\n", first);""",
        "java": """String first = "Ada";
String message = "Hi " + first;
System.out.println(message);""",
    },
    "char_arrays": {
        "cpp": """char word[] = {'c', 'o', 'd', 'e', '\\0'};""",
        "racket": """#lang racket

(define chars (string->list "code"))
(define word (list->string chars))""",
        "python": """chars = list("code")
word = "".join(chars)""",
        "c": """char word[] = {'c', 'o', 'd', 'e', '\\0'};
printf("%s\\n", word);""",
        "java": """char[] chars = {'c', 'o', 'd', 'e'};
String word = new String(chars);""",
    },
    "classes": {
        "cpp": """class Student {
public:
    std::string name;
    int score;
};""",
        "racket": """#lang racket

(struct student (name score) #:transparent)
(define ada (student "Ada" 95))""",
        "python": """class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score""",
        "c": """typedef struct {
    const char *name;
    int score;
} Student;""",
        "java": """class Student {
    String name;
    int score;
}""",
    },
    "switch_statement": {
        "cpp": """switch (choice) {
    case 1: label = "start"; break;
    default: label = "quit";
}""",
        "racket": """#lang racket

(define choice 1)
(define label
  (case choice
    [(1) "start"]
    [else "quit"]))""",
        "python": """choice = 1
match choice:
    case 1:
        label = "start"
    case _:
        label = "quit" """,
        "c": """switch (choice) {
    case 1: label = "start"; break;
    default: label = "quit";
}""",
        "java": """String label = switch (choice) {
    case 1 -> "start";
    default -> "quit";
};""",
    },
    "multi_arrays": {
        "cpp": """int grid[2][3] = {{1, 2, 3}, {4, 5, 6}};""",
        "racket": """#lang racket

(define grid (vector (vector 1 2 3)
                     (vector 4 5 6)))
(vector-ref (vector-ref grid 1) 2)""",
        "python": """grid = [[1, 2, 3], [4, 5, 6]]
print(grid[1][2])""",
        "c": """int grid[2][3] = {{1, 2, 3}, {4, 5, 6}};
printf("%d\\n", grid[1][2]);""",
        "java": """int[][] grid = {{1, 2, 3}, {4, 5, 6}};
System.out.println(grid[1][2]);""",
    },
    "vectors": {
        "cpp": """std::vector<int> nums = {1, 2};
nums.push_back(3);""",
        "racket": """#lang racket

(define nums (vector 1 2 3))
(vector-length nums)
(vector-ref nums 2)""",
        "python": """nums = [1, 2]
nums.append(3)
print(nums)""",
        "c": """int nums[10] = {1, 2};
int size = 2;
nums[size++] = 3;""",
        "java": """java.util.ArrayList<Integer> nums = new java.util.ArrayList<>();
nums.add(1);
nums.add(2);
nums.add(3);""",
    },
    "objects_classes": {
        "cpp": """Student ada;
ada.name = "Ada";
ada.score = 95;""",
        "racket": """#lang racket

(define student%
  (class object%
    (init-field name score)
    (super-new)
    (define/public (passing?) (>= score 60))))

(define ada (new student% [name "Ada"] [score 95]))
(send ada passing?)""",
        "python": """ada = Student("Ada", 95)
print(ada.score)""",
        "c": """Student ada = {"Ada", 95};
printf("%d\\n", ada.score);""",
        "java": """Student ada = new Student();
ada.name = "Ada";
ada.score = 95;""",
    },
    "recursion": {
        "cpp": """int fact(int n) {
    if (n == 0) return 1;
    return n * fact(n - 1);
}""",
        "racket": """#lang racket

(define (fact n)
  (if (= n 0)
      1
      (* n (fact (- n 1)))))""",
        "python": """def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)""",
        "c": """int fact(int n) {
    if (n == 0) return 1;
    return n * fact(n - 1);
}""",
        "java": """static int fact(int n) {
    if (n == 0) return 1;
    return n * fact(n - 1);
}""",
    },
    "search_float": {
        "cpp": """double target = 3.5;
for (double x : values) {
    if (x == target) found = true;
}""",
        "racket": """#lang racket

(define values (vector 2.5 3.5 4.0))
(define target 3.5)
(for/or ([x (in-vector values)])
  (= x target))""",
        "python": """values = [2.5, 3.5, 4.0]
target = 3.5
found = target in values""",
        "c": """double values[] = {2.5, 3.5, 4.0};
int found = 0;
for (int i = 0; i < 3; i++) {
    if (values[i] == 3.5) found = 1;
}""",
        "java": """double[] values = {2.5, 3.5, 4.0};
boolean found = false;
for (double x : values) {
    if (x == 3.5) found = true;
}""",
    },
    "combined_if": {
        "cpp": """if (age >= 13 && age <= 19) {
    teen = true;
}""",
        "racket": """#lang racket

(define age 16)
(define teen? (and (>= age 13) (<= age 19)))""",
        "python": """age = 16
teen = age >= 13 and age <= 19""",
        "c": """int age = 16;
int teen = age >= 13 && age <= 19;""",
        "java": """int age = 16;
boolean teen = age >= 13 && age <= 19;""",
    },
    "nested_if": {
        "cpp": """if (loggedIn) {
    if (isAdmin) {
        showAdminPanel();
    }
}""",
        "racket": """#lang racket

(define logged-in? #t)
(define admin? #t)
(if logged-in?
    (if admin? "admin" "user")
    "guest")""",
        "python": """if logged_in:
    if is_admin:
        role = "admin"
    else:
        role = "user"
else:
    role = "guest" """,
        "c": """if (logged_in) {
    if (is_admin) role = "admin";
    else role = "user";
} else {
    role = "guest";
}""",
        "java": """if (loggedIn) {
    if (isAdmin) role = "admin";
    else role = "user";
} else {
    role = "guest";
}""",
    },
    "for_arrays": {
        "cpp": """for (int i = 0; i < size; i++) {
    total += scores[i];
}""",
        "racket": """#lang racket

(define scores (vector 90 80 100))
(define total
  (for/sum ([score (in-vector scores)])
    score))""",
        "python": """scores = [90, 80, 100]
total = 0
for score in scores:
    total += score""",
        "c": """int scores[] = {90, 80, 100};
int total = 0;
for (int i = 0; i < 3; i++) {
    total += scores[i];
}""",
        "java": """int[] scores = {90, 80, 100};
int total = 0;
for (int score : scores) {
    total += score;
}""",
    },
    "nested_for_multi": {
        "cpp": """for (int r = 0; r < rows; r++) {
    for (int c = 0; c < cols; c++) {
        total += grid[r][c];
    }
}""",
        "racket": """#lang racket

(define grid (vector (vector 1 2) (vector 3 4)))
(define total
  (for*/sum ([row (in-vector grid)]
             [value (in-vector row)])
    value))""",
        "python": """grid = [[1, 2], [3, 4]]
total = 0
for row in grid:
    for value in row:
        total += value""",
        "c": """int grid[2][2] = {{1, 2}, {3, 4}};
int total = 0;
for (int r = 0; r < 2; r++) {
    for (int c = 0; c < 2; c++) {
        total += grid[r][c];
    }
}""",
        "java": """int[][] grid = {{1, 2}, {3, 4}};
int total = 0;
for (int[] row : grid) {
    for (int value : row) {
        total += value;
    }
}""",
    },
    "while_validation": {
        "cpp": """while (score < 0 || score > 100) {
    std::cin >> score;
}""",
        "racket": """#lang racket

(define (valid-score? score)
  (and (number? score) (<= 0 score 100)))

(let loop ([score -1])
  (if (valid-score? score)
      score
      (loop 80)))""",
        "python": """score = -1
while score < 0 or score > 100:
    score = int(input("Score: "))""",
        "c": """int score = -1;
while (score < 0 || score > 100) {
    scanf("%d", &score);
}""",
        "java": """int score = -1;
while (score < 0 || score > 100) {
    score = input.nextInt();
}""",
    },
    "do_while_menu": {
        "cpp": """do {
    showMenu();
    std::cin >> choice;
} while (choice != 0);""",
        "racket": """#lang racket

(let loop ()
  (displayln "1) Play  0) Quit")
  (define choice "0")
  (unless (string=? choice "0")
    (loop)))""",
        "python": """while True:
    print("1) Play  0) Quit")
    choice = input("> ")
    if choice == "0":
        break""",
        "c": """int choice;
do {
    printf("1) Play  0) Quit\\n");
    scanf("%d", &choice);
} while (choice != 0);""",
        "java": """int choice;
do {
    System.out.println("1) Play  0) Quit");
    choice = input.nextInt();
} while (choice != 0);""",
    },
}


PROJECT_ALIASES = {
    "review_basics": "math",
    "review_conditions": "combined_if",
    "review_loops": "do_while_menu",
    "review_functions": "call_function",
    "review_arrays_strings": "for_arrays",
    "review_objects": "objects_classes",
    "review_search_recursion": "search_float",
    "project_guess": "random_number",
    "project_grade": "else_if",
    "project_pattern": "nested_for",
    "project_array_stats": "for_arrays",
    "project_text": "strings",
    "project_student": "objects_classes",
    "project_menu": "do_while_menu",
    "debug_io_types": "input",
    "testing_math_conditions": "error_check",
    "testing_loops": "while_validation",
    "testing_functions": "create_function",
    "testing_collections": "for_arrays",
    "integrated_table": "nested_for_multi",
    "integrated_records": "search_float",
    "capstone_build": "project_menu",
    "capstone_review": "review_functions",
}


def _base_kind(kind: str) -> str:
    seen: set[str] = set()
    current = kind
    while current not in SNIPPETS:
        if current in seen:
            return "for_arrays"
        seen.add(current)
        current = PROJECT_ALIASES.get(current, "for_arrays")
    return current


def get_language_options() -> list[dict]:
    return [
        {"id": item["id"], "name": item["name"], "file_ext": item["file_ext"], "runner": item["runner"]}
        for item in TARGET_LANGUAGES.values()
    ]


def normalize_target_language(target: str | None) -> str:
    value = (target or "racket").strip().lower()
    return value if value in TARGET_LANGUAGES else "racket"


def normalize_base_language(base: str | None) -> str:
    value = (base or "cpp").strip().lower()
    return value if value in TARGET_LANGUAGES else "cpp"


def _docs_for(target: str) -> list[dict[str, str]]:
    return DOCS[target]


def _summary(kind: str) -> str:
    return KIND_SUMMARIES.get(kind) or KIND_SUMMARIES.get(_base_kind(kind)) or DEFAULT_SUMMARY


def _code(kind: str, target: str) -> str:
    return SNIPPETS[_base_kind(kind)][target]


def _cpp(kind: str) -> str:
    return SNIPPETS[_base_kind(kind)]["cpp"]


def _example_io(kind: str, target: str) -> dict[str, str]:
    base_kind = _base_kind(kind)
    language = TARGET_LANGUAGES[target]["name"]
    no_input = ""
    examples = {
        "output": {"input": no_input, "output": f"Hello, {language}!\n42"},
        "input": {
            "input": "Code\n16\n19.50\ntrue\nA\n88 91 84",
            "output": "Name: Age integer: Price decimal: Member true/false: Initial character: Three integer scores:\nCode is 16 years old. Price: 19.5. Member: true. Initial: A. First score: 88",
        },
        "math": {"input": no_input, "output": "No console output yet.\nComputed values: subtotal = 80, tax = 10, total = 90, average = 45.0"},
        "variable": {"input": no_input, "output": "No console output yet.\nStored values: count = 3, price = 9.99, label = book"},
        "if_statement": {"input": no_input, "output": "pass"},
        "else_if": {"input": no_input, "output": "grade = B"},
        "error_check": {
            "input": "Example call: average(total = 90, count = 0)",
            "output": "Invalid count path runs.\nRacket/Python/Java/C++ raise an error; C returns -1.0 in this simplified sample.",
        },
        "while_loop": {"input": no_input, "output": "3\n2\n1"},
        "do_while": {"input": "0", "output": "Body runs once, then stops because choice is 0."},
        "random_number": {"input": no_input, "output": "Random output from 1 to 10.\nExample: 7"},
        "for_loop": {"input": no_input, "output": "0\n1\n2\n3\n4"},
        "nested_for": {"input": no_input, "output": "0 0\n0 1\n0 2\n1 0\n1 1\n1 2\n2 0\n2 1\n2 2"},
        "function_intro": {"input": "Example call: square(5)", "output": "25"},
        "create_function": {"input": "Example call: addTax(100)", "output": "113.0"},
        "call_function": {"input": no_input, "output": "25"},
        "arrays_intro": {"input": no_input, "output": "90"},
        "array_kinds": {"input": no_input, "output": "No console output yet.\nFixed sequence: 1, 2, 3\nDynamic sequence starts as 1, 2, 3"},
        "array_declare": {"input": no_input, "output": "No console output yet.\nvalues = 0, 1, 2, 3\nnames = Ada, Grace"},
        "strings": {"input": no_input, "output": "Hi Ada"},
        "char_arrays": {"input": no_input, "output": "code"},
        "classes": {"input": no_input, "output": "Student object/record stores name and score."},
        "switch_statement": {"input": no_input, "output": "label = start"},
        "multi_arrays": {"input": no_input, "output": "6"},
        "vectors": {"input": no_input, "output": "nums = 1, 2, 3"},
        "objects_classes": {"input": no_input, "output": "95"},
        "recursion": {"input": "Example call: fact(5)", "output": "120"},
        "search_float": {"input": no_input, "output": "found = true"},
        "combined_if": {"input": no_input, "output": "teen = true"},
        "nested_if": {"input": no_input, "output": "role = admin"},
        "for_arrays": {"input": no_input, "output": "total = 270"},
        "nested_for_multi": {"input": no_input, "output": "total = 10"},
        "while_validation": {"input": "-1\n105\n88", "output": "Invalid values are rejected.\nAccepted score = 88"},
        "do_while_menu": {"input": "0", "output": "1) Play  0) Quit\nThen the loop stops."},
    }
    result = dict(examples.get(base_kind, {"input": no_input, "output": "Result depends on the values printed by this practice fragment."}))
    if base_kind == "input":
        if target == "c":
            result["input"] = "Code\n16\n19.50\n1\nA\n88 91 84"
            result["output"] = "Name: Age integer: Price decimal: Member 1/0: Initial character: Three integer scores:\nCode is 16 years old. Price: 19.50. Member: 1. Initial: A. First score: 88"
        elif target == "racket":
            result["output"] = "Name: Age integer: Price decimal: Member true/false: Initial character: Three integer scores separated by spaces:\nCode is 16 years old. Price: 19.5. Member: #t. Initial: A. First score: 88"
    return result


def _focus(title: str, kind: str, target: str, base: str = "cpp") -> list[str]:
    language = TARGET_LANGUAGES[target]["name"]
    base_language = TARGET_LANGUAGES[base]["name"]
    base_kind = _base_kind(kind)
    base = base_kind.replace("_", " ")
    focus = [
        f"{language} syntax",
        f"{base_language} comparison: {base}",
        "line-by-line explanation",
        "small runnable example",
    ]
    if target == "racket":
        focus.insert(1, "Racket expression shape: (function argument ...)")
        if base_kind == "output":
            focus.insert(2, "`displayln` prints a value and then a newline")
            focus.insert(3, "`#lang racket` selects the language for the file")
    return focus


def _syntax_bridge(title: str, kind: str, target: str, base: str = "cpp") -> dict:
    language = TARGET_LANGUAGES[target]["name"]
    base_language = TARGET_LANGUAGES[base]["name"]
    base_code = _code(kind, base)
    base_kind = _base_kind(kind)
    if target == base:
        translation_steps = [
            f"Read the {base_language} example from top to bottom and identify the output, input, and processing lines.",
            "Mark the syntax pieces: header, main function, declarations, statements, blocks, and semicolons.",
            "Run the smallest version first, then change one value and predict the new result.",
            f"Write one short note per important line so later languages have a clear {base_language} baseline.",
        ]
        pitfalls = [
            "Do not skip main, headers, or semicolons until you can explain why they are there.",
            "Do not memorize syntax alone; connect each line to a concrete program action.",
            "Keep examples small enough that compiler errors point to one concept at a time.",
        ]
        if base_kind == "input":
            translation_steps = [
                f"Identify each input variable and its type in the {base_language} sample: string, integer, decimal, boolean, character, and array/list.",
                "Mark where text input becomes a typed value. In some languages the variable type controls parsing; in others you call a conversion function.",
                "Mark the final output sentence and point to every variable inserted into that sentence.",
                "Run with the given test inputs, then change one input and predict the changed output.",
            ]
            pitfalls = [
                "Do not assume all input is already a number. Many languages read text first or need a format/parser.",
                "Do not mix full-line input and token input until you understand leftover newline behavior.",
                "When outputting a sentence, convert or format values cleanly instead of building unreadable concatenation.",
            ]
        return {
            "concept": f"{base_language} foundation: {title}.",
            "cpp": base_code,
            "base": base_code,
            "base_label": base_language,
            "base_io": _example_io(kind, base),
            "racket": _code(kind, target),
            "target": _code(kind, target),
            "target_label": language,
            "target_io": _example_io(kind, target),
            "translation_steps": translation_steps,
            "pitfalls": pitfalls,
            "drill": f"Type the {base_language} snippet, run it, then explain every non-blank line in plain English.",
            "today_angle": f"Prerequisite {base_language} topic: {title}. Build the baseline before moving to another language.",
            "docs": _docs_for(target),
        }
    translation_steps = [
        f"First identify what the {base_language} code is doing, not just which symbols it uses.",
        f"Write the same idea using normal {language} syntax and naming.",
        "Run the smallest version, then change one value and predict the output.",
        f"Add one short note per important line explaining the {base_language} comparison.",
    ]
    pitfalls = [
        f"Do not copy {base_language} punctuation when the target language has a different block style.",
        f"Use the standard {language} library or idiom instead of forcing a literal translation.",
        "Keep input, calculation, and output separated when the example grows.",
    ]
    if target == "racket" and base_kind == "output":
        translation_steps = [
            f"Read `{BASE_COMPARISON_EXAMPLES['output'][base]}` as the familiar {base_language} way to print a value.",
            "In Racket, use `(displayln value)`: `displayln` is the output function and `value` is what you want printed.",
            "Read `(displayln 42)` aloud as: call `displayln` with argument `42`; print 42; add a newline.",
            "`#lang racket` must stay at the top because it tells Racket how to read every expression in the file.",
            "Do not add C++ semicolons. Racket expression boundaries come from parentheses and line structure.",
        ]
        pitfalls = [
            "Do not write `displayln(42)`. Racket calls use prefix parentheses: `(displayln 42)`.",
            "Do not delete `#lang racket`; most Racket files need it as the first line.",
            "Do not confuse `display` and `displayln`: `displayln` adds the newline for you.",
        ]
    elif base_kind == "input":
        translation_steps = [
            f"Start from the {base_language} input variable: name its data type before translating the syntax.",
            f"Write the {language} input form for string, integer, decimal, boolean, character, and array/list values.",
            "For number input, show exactly where conversion happens, such as a parser, format specifier, scanner method, or typed input stream.",
            "For output, build one sentence that includes text plus every variable, then check spacing and formatting.",
        ]
        pitfalls = [
            "Input from a keyboard starts as characters; do not use it in math until the language has parsed it as a number.",
            "Boolean input spelling matters. Decide whether the test input is `true/false`, `1/0`, or another form.",
            "Character input should handle empty input or old whitespace carefully.",
            "Array/list input usually needs repeated reads or splitting one line into pieces.",
        ]
    return {
        "concept": f"{title}: translate the {base_language} pattern into {language}.",
        "cpp": base_code,
        "base": base_code,
        "base_label": base_language,
        "base_io": _example_io(kind, base),
        "racket": _code(kind, target),
        "target": _code(kind, target),
        "target_label": language,
        "target_io": _example_io(kind, target),
        "translation_steps": translation_steps,
        "pitfalls": pitfalls,
        "drill": f"Rewrite the {base_language} snippet in {language}, then explain every non-blank line.",
        "today_angle": f"Day topic: {title}. Start from {base_language}, then write the target-language version.",
        "docs": _docs_for(target),
    }


def _goal(title: str, target: str, base: str = "cpp") -> str:
    language = TARGET_LANGUAGES[target]["name"]
    base_language = TARGET_LANGUAGES[base]["name"]
    if target == base:
        return f"Build the {base_language} foundation for {title.lower()} before starting another target language."
    return f"Learn {title.lower()} in {language} by comparing it directly with the {base_language} version you already understand."


def _explanation(title: str, kind: str, target: str, base: str = "cpp") -> str:
    language = TARGET_LANGUAGES[target]["name"]
    base_language = TARGET_LANGUAGES[base]["name"]
    base_kind = _base_kind(kind)
    if target == base:
        extra = f" {INPUT_TYPE_DETAILS[target]}" if base_kind == "input" else ""
        return (
            f"{_summary(kind)} This prerequisite track teaches the {base_language} version first. "
            "Focus on what each line does, where the syntax boundaries are, and how the compiler reads the program. "
            "Once this baseline is comfortable, the other language tracks can compare against it directly."
            f"{extra}"
        )
    if target == "racket":
        detail = RACKET_KIND_DETAILS.get(
            base_kind,
            "Racket programs are built from expressions. In a parenthesized expression, the first item decides the action and the remaining items are inputs to that action. "
            "Read each line by asking: what function or special form is first, what values are passed in, and what result or effect happens?"
        )
        return (
            f"{_summary(kind)} Start from the {base_language} snippet, then read the Racket code as expressions instead of C++ statements. "
            f"{detail} "
            f"After that, compare each Racket line with the closest {base_language} line so the syntax feels connected, not memorized."
        )
    return (
        f"{_summary(kind)} In this lesson, read the {base_language} snippet first and name the exact idea. "
        f"Then study the {language} code line by line. Keep the explanation short: what the line does, "
        f"what syntax it uses, and which {base_language} habit it matches or replaces. "
        f"{INPUT_TYPE_DETAILS.get(target, '') if base_kind == 'input' else ''}"
    )


def _concrete_homework_prompts(kind: str, day: int) -> list[str]:
    base_kind = _base_kind(kind)
    a = day + 12
    b = day * 2 + 7
    c = (day % 5) + 3
    d = (day % 4) + 2
    price = 8 + day
    quantity = (day % 3) + 3
    subtotal = price * quantity
    discount = (day % 4) + 5
    after_discount = subtotal - discount
    tax_rate = 13
    tax = round(after_discount * tax_rate / 100, 2)
    final_total = round(after_discount + tax, 2)
    score = 55 + day
    bonus = (day % 6) + 4
    final_score = score + bonus
    width = (day % 4) + 4
    height = (day % 3) + 3
    area = width * height
    values = [day + 3, day + 8, day + 1, day + 12, day + 5]
    value_list = ", ".join(str(value) for value in values)
    value_sum = sum(values)
    value_avg = round(value_sum / len(values), 2)
    rows = (day % 3) + 3
    cols = (day % 4) + 4
    cells = rows * cols
    name = f"Student{day:02d}"

    prompts = {
        "output": [
            f"Print three lines exactly: `Course Day {day}`, `Sum {a} + {b} = {a + b}`, and `Product {c} * {d} = {c * d}`. Do not use input; hard-code the numbers and show both formulas.",
            f"Print a mini receipt using price {price} and quantity {quantity}. Calculate {price} * {quantity} = {subtotal}, then print `Subtotal: {subtotal}`.",
            f"Print a score report. Start with score {score}, add bonus {bonus}, calculate {score} + {bonus} = {final_score}, and print the final score on its own line.",
        ],
        "input": [
            f"Ask the user for one integer age. Test input: {a}. Add {b}, calculate {a} + {b} = {a + b}, and print one sentence such as `Age plus {b} is {a + b}`.",
            f"Ask for a string item, decimal price, integer quantity, and boolean member flag. Test input: item `notebook`, price {price}.50, quantity {quantity}, member true/1. Calculate subtotal {price}.50 * {quantity} and print one receipt sentence containing all four variables.",
            f"Ask for one character initial and three integer scores as an array/list. Test input: initial `A`, scores {values[0]}, {values[1]}, {values[2]}. Calculate sum {values[0] + values[1] + values[2]} and print a sentence containing the character, the array/list values, and the sum.",
        ],
        "math": [
            f"Create variables subtotal = {subtotal}, discount = {discount}, and taxRate = {tax_rate}. Calculate afterDiscount = {subtotal} - {discount} = {after_discount}, tax = afterDiscount * {tax_rate}/100 = {tax}, and finalTotal = {final_total}. Print all three results.",
            f"Calculate the average of {values[0]}, {values[1]}, and {values[2]}. Show the formula ({values[0]} + {values[1]} + {values[2]}) / 3 and print the decimal average.",
            f"Calculate a rectangle perimeter with width {width} and height {height}. Use 2 * ({width} + {height}) = {2 * (width + height)} and print the perimeter.",
        ],
        "variable": [
            f"Declare and initialize integer variables apples = {a}, oranges = {b}, and boxes = {c}. Calculate totalFruit = apples + oranges = {a + b} and fruitPerBox = totalFruit / boxes.",
            f"Declare price = {price}, quantity = {quantity}, and discount = {discount}. Calculate subtotal = {subtotal} and totalAfterDiscount = {after_discount}.",
            f"Declare name = `{name}`, score = {score}, bonus = {bonus}, and finalScore = {final_score}. Print one sentence containing all four values.",
        ],
        "if_statement": [
            f"Set score = {final_score}. If score is at least 60, print `Pass`. Since {final_score} >= 60 is true, your output should show `Pass`.",
            f"Set temperature = {18 + day}. If temperature is greater than 25, print `Hot day`; otherwise print nothing. Add a comment predicting whether the message appears.",
            f"Set inventory = {quantity}. If inventory is less than 5, print `Restock needed`. Explain in one comment why {quantity} triggers or does not trigger the message.",
        ],
        "else_if": [
            f"Set score = {final_score}. Use else-if rules: 90+ gives A, 80-89 gives B, 70-79 gives C, 60-69 gives D, below 60 gives F. Print the grade for {final_score}.",
            f"Set orderTotal = {subtotal}. If it is 100 or more, discount is 20; else if 50 or more, discount is 10; otherwise discount is 0. Calculate and print final amount.",
            f"Set monthNumber = {(day % 12) + 1}. Use else-if to print Winter for 12/1/2, Spring for 3/4/5, Summer for 6/7/8, and Fall for 9/10/11.",
        ],
        "error_check": [
            f"Read an age. In your test run, enter {day - 3}. If age is below 0 or above 120, print `Invalid age`; otherwise print `Valid age`.",
            f"Read quantity. In your test run, enter {quantity}. If quantity is 0 or negative, print an error; otherwise calculate {price} * quantity and print total.",
            f"Read a denominator. In your test run, enter {c}. If it is 0, print `Cannot divide`; otherwise calculate {b} / denominator and print the quotient.",
        ],
        "while_loop": [
            f"Start count = 1 and total = 0. While count is at most {c}, add count to total. Print each count and print final total {sum(range(1, c + 1))}.",
            f"Start balance = {subtotal}. While balance is greater than 0, subtract {price} each loop and print the new balance until it reaches 0 or below.",
            f"Start number = {a}. While number is greater than 0, subtract {c} and print each value. Stop when number is 0 or negative.",
        ],
        "do_while": [
            f"Make a loop that runs at least once. Start attempts = 0, add 1 each time, and stop after {d} attempts. Print `Attempt 1` through `Attempt {d}`.",
            f"Create a menu loop with choices 1, 2, and 0. Simulate choices 1, 2, 0. Choice 1 adds {a}, choice 2 adds {b}, and choice 0 quits. Print final total {a + b}.",
            f"Start value = {price}. In a do-while style loop, print value, subtract {c}, and continue while value is positive.",
        ],
        "random_number": [
            f"Generate or simulate a random number from 1 to 10. For testing, force the value to {c}. If the guess is {c}, print `Correct`; otherwise print the distance from {c}.",
            f"Generate or simulate two dice values. For testing, use {d} and {c}. Calculate sum {d} + {c} = {d + c} and print whether the sum is at least 7.",
            f"Generate or simulate a random discount from 5 to 15. For testing, use {discount}. Apply it to subtotal {subtotal} and print {subtotal} - {discount} = {after_discount}.",
        ],
        "for_loop": [
            f"Use a for loop to print the multiplication table for {c}: {c} * 1 through {c} * 10. Each line must show the full formula and result.",
            f"Use a for loop from 1 to {b}. Add only even numbers to total and print the final even total.",
            f"Use a for loop to calculate factorial {d}! by multiplying 1 through {d}. Print each intermediate product and the final answer.",
        ],
        "nested_for": [
            f"Use nested loops to print a rectangle with {height} rows and {width} columns of `*`. Also calculate and print total characters {height} * {width} = {area}.",
            f"Use nested loops to print a {c} by {c} multiplication grid. Each cell should contain row * column.",
            f"Use nested loops for {rows} students and {cols} quizzes. Print labels like `Student 1 Quiz 1` and count total entries {cells}.",
        ],
        "function_intro": [
            f"Explain a function by writing a small program that calls a built-in or simple helper to calculate {a} + {b} = {a + b}. Print the input values and result.",
            f"Write a program with one reusable calculation idea: area = width * height. Use width {width} and height {height}, then print area {area}.",
            f"Show why functions avoid repeated work: calculate tax for totals {subtotal} and {subtotal + 20} using tax rate {tax_rate}%. Print both tax values.",
        ],
        "create_function": [
            f"Create a function `addBonus` that takes score {score} and bonus {bonus}, returns {final_score}, and prints the returned value.",
            f"Create a function `rectangleArea` that takes width {width} and height {height}, returns {area}, and prints the formula.",
            f"Create a function `finalPrice` that takes subtotal {subtotal} and discount {discount}, returns {after_discount}, and prints the result.",
        ],
        "call_function": [
            f"Write a function that multiplies two numbers, then call it with {a} and {c}. Print returned result {a * c}.",
            f"Write a function that converts minutes to seconds. Call it with {b} minutes and print {b} * 60 = {b * 60}.",
            f"Write a function that finds the larger of {a} and {b}. Call it, store the returned value, and print the larger number.",
        ],
        "arrays_intro": [
            f"Create a collection containing {value_list}. Print the first value {values[0]}, the last value {values[-1]}, and the number of values {len(values)}.",
            f"Create a collection of quiz scores {value_list}. Add the first two values: {values[0]} + {values[1]} = {values[0] + values[1]}, then print the result.",
            f"Create a collection of prices {price}, {price + 2}, and {price + 5}. Print each price with its index or position.",
        ],
        "array_kinds": [
            f"Create one fixed-size or plain array/list with values {value_list}. Print all values and explain in a comment whether its size should change.",
            f"Create a resizable collection with starting values {values[0]}, {values[1]}, {values[2]}. Add {values[3]} and print the new size.",
            f"Create a two-item collection of names and a numeric collection of scores {score} and {final_score}. Print each name with one score.",
        ],
        "array_declare": [
            f"Declare and initialize an array/list with {value_list}. Calculate sum {value_sum} by accessing each element or looping over it.",
            f"Declare an array/list of 4 prices: {price}, {price + 3}, {price + 6}, {price + 9}. Calculate and print their average.",
            f"Declare an array/list of 3 quantities: {quantity}, {quantity + 1}, {quantity + 2}. Multiply each by price {price} and print each subtotal.",
        ],
        "strings": [
            f"Create firstName = `Code` and lastName = `Bridge{day}`. Join them with a space and print `Code Bridge{day}`.",
            f"Create item = `apple` and count = {quantity}. Print `apple x {quantity}` and also print the length of `apple`.",
            f"Create text = `Day{day}Score{final_score}`. Print the first character, last character, and total length.",
        ],
        "char_arrays": [
            f"Create a character array/list for `CODE{day}`. Print each character on its own line and count total characters.",
            f"Create characters `A`, `B`, `C`, and `{c}` as text. Combine them into one string and print it.",
            f"Store the word `LEVEL` as characters. Count how many characters match the first character `L` and print the count.",
        ],
        "classes": [
            f"Create a `Rectangle` data type or class with width {width} and height {height}. Add or write logic to calculate area {area}.",
            f"Create a `Student` data type or class with name `{name}` and score {score}. Print `{name}: {score}`.",
            f"Create a `BankAccount` data type or class with starting balance {subtotal}. Deposit {price}, withdraw {discount}, and print final balance {subtotal + price - discount}.",
        ],
        "switch_statement": [
            f"Set menuChoice = {(day % 4) + 1}. Use switch/case or the closest target-language equivalent: 1 adds {a}, 2 subtracts {c}, 3 multiplies by {d}, 4 quits. Print the selected result.",
            f"Set gradeLetter based on score {final_score}: A, B, C, D, or F. Use switch/case where available, or an equivalent exact-match branch, to print a message for the grade.",
            f"Set dayNumber = {(day % 7) + 1}. Use switch/case or equivalent to print Monday through Sunday, then print whether it is a school day.",
        ],
        "multi_arrays": [
            f"Create a 2D grid with {rows} rows and {cols} columns. Fill each cell with row + column and print the grid.",
            f"Create a 2D score table for {rows} students and {cols} quizzes. Fill each score with 70 + row + quiz and print each student total.",
            f"Create a {height} by {width} grid of numbers. Count and print total cells {area}.",
        ],
        "vectors": [
            f"Create a resizable vector/list with {values[0]}, {values[1]}, and {values[2]}. Add {values[3]}, remove or ignore the first value, and print the final contents.",
            f"Create a vector/list of prices {price}, {price + 4}, and {price + 8}. Add tax rate {tax_rate}% to each and print each final price.",
            f"Create an empty vector/list, add numbers 1 through {c}, then calculate and print their sum {sum(range(1, c + 1))}.",
        ],
        "objects_classes": [
            f"Create two `Student` objects/records: `{name}` with score {score}, and `StudentB` with score {final_score}. Print the higher score.",
            f"Create a `Product` object/record with price {price} and quantity {quantity}. Add a method/function or external helper to calculate subtotal {subtotal}.",
            f"Create a `Point` object/record with x = {width} and y = {height}. Calculate distance squared = x*x + y*y = {width * width + height * height}.",
        ],
        "recursion": [
            f"Write a recursive function to calculate the sum from 1 to {c}. The result should be {sum(range(1, c + 1))}. Print each recursive step or final result.",
            f"Write a recursive function to calculate factorial {d}! = {math.factorial(d)}. Print the final value.",
            f"Write a recursive countdown from {c} to 0. Print every number and then print `Done`.",
        ],
        "search_float": [
            f"Search the list {value_list} for target {values[3]}. Print its index/position if found; otherwise print `Not found`.",
            f"Use floating-point values {price}.5, {price + 2}.25, and {price + 4}.75. Calculate and print their average.",
            f"Search scores {value_list} for the first value greater than {score}. Print the value if it exists; otherwise print `No score above {score}`.",
        ],
        "combined_if": [
            f"Set age = {18 + day} and score = {final_score}. Print `Eligible` only if age is at least 18 and score is at least 70.",
            f"Set subtotal = {subtotal} and memberYears = {day % 5}. Give a discount only if subtotal is at least 50 or memberYears is at least 3. Print discount amount.",
            f"Set temperature = {18 + day} and raining = {day % 2 == 0}. Print `Practice outside` only if temperature is between 18 and 28 and it is not raining.",
        ],
        "nested_if": [
            f"Set score = {final_score} and attendance = {80 + (day % 20)}. First check score >= 60; inside that branch, check attendance >= 85 to print `Full pass` or `Academic pass only`.",
            f"Set balance = {subtotal} and withdrawal = {price}. First check withdrawal > 0; inside that, check balance >= withdrawal and print the new balance.",
            f"Set age = {14 + (day % 8)} and permission = {day % 2 == 0}. If age is under 18, check permission before printing whether the student can join.",
        ],
        "for_arrays": [
            f"Loop through array/list {value_list}. Add every value to total and print sum {value_sum}.",
            f"Loop through prices {price}, {price + 2}, {price + 4}, {price + 6}. For each price, multiply by quantity {quantity} and print the subtotal.",
            f"Loop through scores {value_list}. Count how many scores are at least {values[2]} and print the count.",
        ],
        "nested_for_multi": [
            f"Use nested loops to process a {rows} by {cols} table. Put row * column in each cell and print the table.",
            f"Use nested loops for {rows} students and {cols} assignments. Each grade is 70 + student + assignment; print each student average.",
            f"Use nested loops to count border cells in a {height} by {width} rectangle. Print total cells {area} and border count.",
        ],
        "while_validation": [
            f"Keep asking for a quantity until it is between 1 and 10. Simulate inputs -1, 0, and {quantity}. Accept {quantity}, then calculate {quantity} * {price} = {quantity * price}.",
            f"Keep asking for a password length until it is at least 8. Simulate lengths 4, 7, and {8 + (day % 5)}. Print the accepted length.",
            f"Keep asking for a denominator until it is not 0. Simulate 0, 0, and {c}. Calculate {b} / {c} and print the result.",
        ],
        "do_while_menu": [
            f"Build a menu that runs at least once. Simulate choices 1, 1, 2, 0. Choice 1 adds {price}, choice 2 subtracts {discount}. Print final total {price + price - discount}.",
            f"Build a calculator menu. Simulate choice 1 to add {a} + {b}, choice 2 to multiply {c} * {d}, then choice 0 to quit. Print both results.",
            f"Build a point menu. Simulate adding points {c}, {d}, and then quitting. Print total points {c + d}.",
        ],
    }
    return prompts.get(
        base_kind,
        [
            f"Use the numbers {a}, {b}, and {c}. Calculate {a} + {b} - {c} = {a + b - c}, then print the formula and result.",
            f"Use price {price}, quantity {quantity}, and discount {discount}. Calculate {price} * {quantity} - {discount} = {after_discount}, then print the result.",
            f"Use values {value_list}. Calculate their sum {value_sum} and average {value_avg}, then print both.",
        ],
    )


def _practice(day: int, title: str, kind: str, target: str, base: str = "cpp") -> list[str]:
    language = TARGET_LANGUAGES[target]["name"]
    base_language = TARGET_LANGUAGES[base]["name"]
    ext = TARGET_LANGUAGES[target]["file_ext"]
    comparison_note = (
        f"Include one short comment comparing the main syntax with {base_language}."
        if target != base
        else f"Include one short comment explaining the most important {language} syntax line."
    )
    prompts = _concrete_homework_prompts(kind, day)
    return [
        f"HW Q1: Program 1 file day{day:02d}_q1.{ext}. Goal: solve only this prompt. Required task: {prompts[0]} Required output: print labelled inputs, the formula or decision, and the final result. Syntax requirement: use normal {language} syntax for today's topic. {comparison_note}",
        f"HW Q2: Program 2 file day{day:02d}_q2.{ext}. Goal: write a different program from Q1. Required task: {prompts[1]} Required output: print enough labels that another student can see each value and result. Syntax requirement: use the Day {day:02d} concept directly. {comparison_note}",
        f"HW Q3: Program 3 file day{day:02d}_q3.{ext}. Goal: add one extra explanation habit. Required task: {prompts[2]} Before the final output, include a brief prediction in a comment and then print the actual result. Required output: labelled prediction plus labelled actual result. {comparison_note}",
    ]


def _checklist(day: int, title: str, target: str, base: str = "cpp") -> list[str]:
    language = TARGET_LANGUAGES[target]["name"]
    base_language = TARGET_LANGUAGES[base]["name"]
    compare_or_explain = (
        f"Compare the {base_language} snippet with the {language} snippet."
        if target != base
        else f"Read the {language} snippet and explain every important line."
    )
    notes_request = (
        f"concise {base_language} comparison notes"
        if target != base
        else f"concise {language} line-by-line notes"
    )
    return [
        f"Read Day {day:02d}: {title}.",
        compare_or_explain,
        "Type the sample by hand and run it.",
        "Mark the input, processing, and output lines if they exist.",
        "Complete the three concrete homework programs: HW Q1, HW Q2, and HW Q3.",
        f"Submit all three programs plus {notes_request}.",
    ]


def _rubric(target: str, base: str = "cpp") -> list[str]:
    language = TARGET_LANGUAGES[target]["name"]
    base_language = TARGET_LANGUAGES[base]["name"]
    transfer_or_baseline = (
        f"{base_language} transfer: the notes clearly explain what changed from {base_language}."
        if target != base
        else f"{language} baseline: the notes clearly explain what each important line does."
    )
    return [
        "Correctness: the code runs and matches the assignment.",
        f"{language} syntax: the code uses normal {language} structure and naming.",
        transfer_or_baseline,
        "Completeness: all three separate homework programs are included.",
        "Clarity: line-by-line comments are concise and accurate.",
    ]


def _assignment(day: int, title: str, target: str, base: str = "cpp") -> str:
    ext = TARGET_LANGUAGES[target]["file_ext"]
    base_language = TARGET_LANGUAGES[base]["name"]
    notes_request = (
        f"include concise notes comparing the target-language syntax with {base_language}"
        if target != base
        else f"include concise notes explaining the important {base_language} syntax line by line"
    )
    return (
        f"Submit three different programs: day{day:02d}_q1.{ext}, day{day:02d}_q2.{ext}, and day{day:02d}_q3.{ext}. "
        "If you paste code instead of uploading files, paste all three programs in order with clear labels: HW Q1, HW Q2, HW Q3. "
        f"Each program must solve its exact numbered homework prompt for '{title}', run successfully by itself, print labelled input values, calculation or decision steps, and the requested result. "
        f"Add short line notes for important syntax and {notes_request}. If your program reads input, put the test input values in the Standard input box before submitting."
    )


BASE_COMPARISON_EXAMPLES = {
    "comment": {
        "cpp": "// note",
        "c": "// note",
        "java": "// note",
        "python": "# note",
        "racket": "; note",
    },
    "language_directive": {
        "cpp": "the compiler mode and .cpp file",
        "c": "the compiler mode and .c file",
        "java": "the .java file and class name",
        "python": "the .py file and Python interpreter",
        "racket": "#lang racket",
    },
    "import": {
        "cpp": "#include <iostream>",
        "c": "#include <stdio.h>",
        "java": "import java.util.Scanner;",
        "python": "import math",
        "racket": "(require racket/list)",
    },
    "entry": {
        "cpp": "int main() { ... }",
        "c": "int main(void) { ... }",
        "java": "public static void main(String[] args) { ... }",
        "python": "top-level code or if __name__ == '__main__':",
        "racket": "top-level expressions after #lang racket",
    },
    "function_def": {
        "cpp": "return_type name(args) { ... }",
        "c": "return_type name(args) { ... }",
        "java": "static returnType name(args) { ... }",
        "python": "def name(args):",
        "racket": "(define (name args) ...)",
    },
    "variable": {
        "cpp": "auto name = value;",
        "c": "int name = value;",
        "java": "var name = value;",
        "python": "name = value",
        "racket": "(define name value)",
    },
    "if": {
        "cpp": "if (condition) { ... }",
        "c": "if (condition) { ... }",
        "java": "if (condition) { ... }",
        "python": "if condition:",
        "racket": "(if condition then-value else-value)",
    },
    "else_if": {
        "cpp": "else if (condition) { ... }",
        "c": "else if (condition) { ... }",
        "java": "else if (condition) { ... }",
        "python": "elif condition:",
        "racket": "(cond [condition result] [else result])",
    },
    "multi_case": {
        "cpp": "switch (value) { case x: ... }",
        "c": "switch (value) { case x: ... }",
        "java": "switch (value) { case x -> ... }",
        "python": "match value:",
        "racket": "(case value [(x) result] [else result])",
    },
    "for_loop": {
        "cpp": "for (int i = 0; i < n; ++i) { ... }",
        "c": "for (int i = 0; i < n; ++i) { ... }",
        "java": "for (int i = 0; i < n; i++) { ... }",
        "python": "for item in items:",
        "racket": "(for ([item items]) ...)",
    },
    "while_loop": {
        "cpp": "while (condition) { ... }",
        "c": "while (condition) { ... }",
        "java": "while (condition) { ... }",
        "python": "while condition:",
        "racket": "a named let or recursive helper",
    },
    "local_binding": {
        "cpp": "{ auto name = value; ... }",
        "c": "{ int name = value; ... }",
        "java": "{ var name = value; ... }",
        "python": "a local name inside an indented block",
        "racket": "(let ([name value]) ...)",
    },
    "data_shape": {
        "cpp": "struct Name { ... };",
        "c": "struct Name { ... };",
        "java": "class Name { ... } or record Name(...)",
        "python": "class Name:",
        "racket": "(struct name (fields))",
    },
    "class": {
        "cpp": "class Name { ... };",
        "c": "a struct plus related functions",
        "java": "class Name { ... }",
        "python": "class Name:",
        "racket": "(class object% ...)",
    },
    "function_call": {
        "cpp": "name(arg1, arg2)",
        "c": "name(arg1, arg2)",
        "java": "name(arg1, arg2)",
        "python": "name(arg1, arg2)",
        "racket": "(name arg1 arg2)",
    },
    "block_start": {
        "cpp": "{",
        "c": "{",
        "java": "{",
        "python": "an indented block after :",
        "racket": "nested parentheses",
    },
    "block_end": {
        "cpp": "}",
        "c": "}",
        "java": "}",
        "python": "dedenting back to the previous level",
        "racket": "closing parentheses",
    },
    "return": {
        "cpp": "return value;",
        "c": "return value;",
        "java": "return value;",
        "python": "return value",
        "racket": "the last expression in a function",
    },
    "output": {
        "cpp": "std::cout << value;",
        "c": "printf(\"%d\\n\", value);",
        "java": "System.out.println(value);",
        "python": "print(value)",
        "racket": "(displayln value)",
    },
    "statement": {
        "cpp": "statement;",
        "c": "statement;",
        "java": "statement;",
        "python": "one logical line, usually no semicolon",
        "racket": "one expression",
    },
}

TOKEN_RE = re.compile(
    r"System\.out\.println|std::boolalpha|std::vector|std::string|std::cout|std::cin|string->number|racket/string|#include|#lang|//|/\*|\*/|==|!=|<=|>=|&&|\|\||::|->|"
    r'"(?:\\.|[^"])*"|\'(?:\\.|[^\'])*\'|<[^>\s]+>|[A-Za-z_][A-Za-z0-9_!?-]*|'
    r"[0-9]+(?:\.[0-9]+)?|[(){}\[\],;:+\-*/%=<>.]"
)

RACKET_PHRASES = {
    "#lang": "Reader directive. It must be first so Racket knows which language rules read this file.",
    "racket": "Language name. It selects normal Racket libraries and syntax.",
    "(": "Starts one Racket expression. In a call, the function name comes right after it.",
    ")": "Ends the current Racket expression.",
    "displayln": "Output function. It prints one value and then adds a newline.",
    "display": "Output function. It prints without adding a newline.",
    "define": "Creates a name for a value or function.",
    "read-line": "Reads one line of text from standard input.",
    "require": "Imports a Racket library.",
    "racket/string": "Library that provides string helpers such as `string-split`.",
    "string->number": "Converts typed text into a number, or returns `#f` if conversion fails.",
    "string-ref": "Takes one character from a string by index.",
    "string-split": "Splits one text line into smaller string pieces.",
    "map": "Applies one function to every item in a list.",
    "format": "Builds a string by inserting values into placeholders.",
    "first": "Gets the first item from a list.",
    "equal?": "Compares two values for equality.",
    "string-append": "Builds one string by joining smaller strings.",
    "if": "Two-way choice: test, then-value, else-value.",
    "cond": "Multi-branch choice. It is Racket's common else-if replacement.",
    "case": "Exact-value branch, closest to a switch statement.",
    "for": "Loop over a sequence.",
    "for*": "Nested sequence loop.",
    "let": "Creates local names; named let can behave like a loop.",
    "struct": "Creates a data shape with fields.",
    "class": "Creates a class value.",
    "random": "Produces a random value.",
    "+": "Prefix addition operator. `(+ a b)` means `a + b`.",
    "-": "Prefix subtraction operator. `(- a b)` means `a - b`.",
    "*": "Prefix multiplication operator. `(* a b)` means `a * b`.",
    "/": "Prefix division operator. `(/ a b)` means `a / b`.",
}

PYTHON_PHRASES = {
    "import": "Makes a module available.",
    "def": "Starts a function definition.",
    "class": "Starts a class definition.",
    "if": "Starts a conditional block.",
    "elif": "Else-if branch.",
    "else": "Fallback branch.",
    "for": "Loop keyword.",
    "while": "Repeat while a condition is true.",
    "in": "Connects a loop variable to a sequence.",
    "return": "Sends a value back from a function.",
    "print": "Built-in output function.",
    "input": "Reads text from the user.",
    "range": "Creates a countable sequence for loops.",
    "int": "Converts text to an integer, or names an integer idea in context.",
    "float": "Converts text to a decimal number, or names a decimal idea in context.",
    "lower": "Converts text to lowercase before comparing it.",
    "split": "Splits a text line into pieces by whitespace.",
    ":": "Starts an indented block.",
    "=": "Binds or updates a name.",
    "(": "Starts function arguments or grouping.",
    ")": "Ends function arguments or grouping.",
    "[": "Starts a list or index access.",
    "]": "Ends a list or index access.",
}

C_LIKE_PHRASES = {
    "#include": "Imports a header/library before compilation.",
    "<stdio.h>": "C standard input/output header.",
    "<iostream>": "C++ stream input/output header.",
    "import": "Imports Java library support.",
    "public": "Java access modifier.",
    "static": "Belongs to the class, so main can run without an object.",
    "void": "Function returns no value.",
    "int": "Integer type.",
    "double": "Decimal number type.",
    "float": "Decimal number type.",
    "char": "Character type.",
    "String": "Java text type.",
    "main": "Program entry point.",
    "printf": "C output function.",
    "scanf": "C input function.",
    "System.out.println": "Java output call that prints and adds a newline.",
    "std::cout": "C++ output stream.",
    "std::cin": "C++ input stream.",
    "std::string": "C++ text type.",
    "std::vector": "C++ resizable array-like sequence.",
    "std::boolalpha": "C++ I/O flag that reads or prints booleans as `true` and `false`.",
    "return": "Ends a function and can send back a value.",
    "bool": "Boolean type. It stores true or false.",
    "boolean": "Boolean type. It stores true or false.",
    "next": "Scanner method that reads one word token.",
    "nextInt": "Scanner method that reads an integer.",
    "nextDouble": "Scanner method that reads a decimal number.",
    "nextBoolean": "Scanner method that reads true or false.",
    "charAt": "String method that gets one character by index.",
    "if": "Starts a condition.",
    "else": "Fallback or else-if branch.",
    "for": "Counted or sequence loop.",
    "while": "Repeats while condition is true.",
    "do": "Starts a loop body that runs before the condition check.",
    "switch": "Exact-value branching.",
    "case": "One switch branch.",
    "class": "Defines a type with fields and methods.",
    "struct": "Defines a grouped data shape.",
    "{": "Starts a block.",
    "}": "Ends a block.",
    ";": "Ends a statement.",
    "=": "Initializes or assigns a value.",
    "(": "Starts parameters, arguments, or a condition.",
    ")": "Ends parameters, arguments, or a condition.",
}

def _is_number_token(token: str) -> bool:
    return bool(re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", token))

def _phrase_meaning(token: str, target: str, index: int, tokens: list[str]) -> str:
    if token.startswith('"') or token.startswith("'"):
        return "String/text literal. The program uses these exact characters."
    if _is_number_token(token):
        return "Number literal. The program uses this exact numeric value."
    if target == "racket":
        if token in RACKET_PHRASES:
            return RACKET_PHRASES[token]
        if index == 1 and tokens[:1] == ["("]:
            return "Function or special-form name. It decides what this expression does."
        return "Name or value used by this Racket expression."
    if target == "python":
        if token in PYTHON_PHRASES:
            return PYTHON_PHRASES[token]
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):
            return "Name for a value, function, class, or module."
        return "Python syntax symbol."
    if token in C_LIKE_PHRASES:
        return C_LIKE_PHRASES[token]
    if token in {"+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">=", "&&", "||"}:
        return "Operator. It calculates or compares values."
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):
        return "Identifier: a variable, function, type, or class name."
    return "Syntax symbol that helps structure this line."

def _phrase_breakdown(line: str, target: str) -> list[dict[str, str]]:
    stripped = line.strip()
    if not stripped:
        return []
    if target == "racket" and stripped.startswith(";"):
        return [
            {"phrase": ";", "meaning": "Starts a Racket comment. Racket ignores the rest of the line."},
            {"phrase": stripped[1:].strip() or "comment text", "meaning": "Human note for the reader, not code that runs."},
        ]
    if target == "python" and stripped.startswith("#"):
        return [
            {"phrase": "#", "meaning": "Starts a Python comment."},
            {"phrase": stripped[1:].strip() or "comment text", "meaning": "Human note for the reader, not code that runs."},
        ]
    if target in {"c", "cpp", "java"} and stripped.startswith("//"):
        return [
            {"phrase": "//", "meaning": "Starts a line comment."},
            {"phrase": stripped[2:].strip() or "comment text", "meaning": "Human note for the reader, not code that runs."},
        ]

    tokens = TOKEN_RE.findall(stripped)
    phrases = [
        {"phrase": token, "meaning": _phrase_meaning(token, target, index, tokens)}
        for index, token in enumerate(tokens[:16])
    ]
    if len(tokens) > 16:
        phrases.append({"phrase": "...", "meaning": "More tokens continue the same line pattern."})
    return phrases


def _base_comparison(note: dict[str, str], target: str, base: str) -> str:
    base_language = TARGET_LANGUAGES[base]["name"]
    target_language = TARGET_LANGUAGES[target]["name"]
    line = note.get("line", "").strip()
    plain = note.get("plain", "").lower()
    syntax = note.get("syntax", "").lower()

    if not line:
        concept = "blank"
    elif line.startswith("#lang"):
        concept = "language_directive"
    elif "comment" in plain:
        concept = "comment"
    elif "imports" in plain or "include" in line or line.startswith("import "):
        concept = "import"
    elif "entry point" in plain or "main(" in line:
        concept = "entry"
    elif "defines a function" in plain or line.startswith("def "):
        concept = "function_def"
    elif "binds" in plain or "updates a name" in plain or " = " in line:
        concept = "variable"
    elif "two-way choice" in plain or "starts a condition" in plain or line.startswith("if "):
        concept = "if"
    elif "else-if" in syntax or line.startswith("elif ") or line.startswith("else"):
        concept = "else_if"
    elif "multi-case" in plain or "exact-value" in plain or "switch" in plain:
        concept = "multi_case"
    elif "for loop" in plain or line.startswith("for "):
        concept = "for_loop"
    elif "while loop" in plain or line.startswith("while ") or line.startswith("do "):
        concept = "while_loop"
    elif "local names" in plain or line.startswith("(let"):
        concept = "local_binding"
    elif "data shape" in plain or line.startswith("(struct"):
        concept = "data_shape"
    elif "class" in plain:
        concept = "class"
    elif "starts a block" in plain:
        concept = "block_start"
    elif "ends a block" in plain:
        concept = "block_end"
    elif "returns" in plain or line.startswith("return"):
        concept = "return"
    elif "prints" in plain or "displayln" in line or "print(" in line or "printf" in line or "System.out.println" in line:
        concept = "output"
    elif "function call" in plain or line.startswith("("):
        concept = "function_call"
    elif "statement" in plain:
        concept = "statement"
    else:
        concept = "normal"

    if concept == "blank":
        return f"Blank lines serve the same readability role in {base_language}."
    if target == base:
        return f"This is the {base_language} baseline form; explain what this line does before moving to another language."
    if concept == "normal":
        return f"Read this {target_language} line by its surrounding structure, then match the same program role in {base_language}."

    example = BASE_COMPARISON_EXAMPLES.get(concept, {}).get(base)
    if not example:
        return f"In {base_language}, use the normal {base_language} form for the same program role."
    return f"In {base_language}, the closest shape is `{example}`."


def _line_note_for_racket(line: str) -> dict[str, str]:
    stripped = line.strip()
    if not stripped:
        return {"line": "", "plain": "Blank line for readability.", "syntax": "Racket ignores blank lines.", "cpp": "Like a blank line between C++ blocks."}
    if stripped.startswith("#lang"):
        return {
            "line": line,
            "plain": "Selects the Racket language for this file before any code runs.",
            "syntax": "`#lang racket` is required at the top of a normal Racket file so the reader knows which grammar and libraries to use.",
            "cpp": "Closest to choosing the .cpp compiler mode plus standard language rules before compiling.",
        }
    if stripped.startswith(";"):
        return {"line": line, "plain": "A comment for the reader.", "syntax": "A semicolon starts a Racket line comment.", "cpp": "Like // in C++."}
    if stripped == "(displayln 42)":
        return {
            "line": line,
            "plain": "Prints the number 42, then moves to the next output line.",
            "syntax": "`displayln` is the function. `42` is the argument. The parentheses are required because Racket writes calls as `(function argument ...)`.",
            "cpp": "Closest to `std::cout << 42 << std::endl;`.",
        }
    if stripped.startswith("(displayln "):
        return {
            "line": line,
            "plain": "Prints one value and adds a newline after it.",
            "syntax": "`displayln` means display plus newline. The first item after `(` is the function; everything after it is the value expression to print.",
            "cpp": "Closest to `std::cout << value << std::endl;`.",
        }
    if stripped.startswith("(display "):
        return {
            "line": line,
            "plain": "Prints text without automatically moving to the next line.",
            "syntax": "`display` is like `displayln`, but without the newline. It is useful for prompts before input.",
            "cpp": "Closest to `std::cout << \"prompt\";` without `std::endl`.",
        }
    if stripped.startswith("(define ("):
        return {
            "line": line,
            "plain": "Defines a reusable function.",
            "syntax": "After `define`, the inner parentheses contain the function name first and then its parameters.",
            "cpp": "Similar to `return_type name(args)`, but plain Racket has no parameter types here.",
        }
    if stripped.startswith("(define "):
        if "(read-line)" in stripped:
            return {
                "line": line,
                "plain": "Reads one line of user input and stores it in a name.",
                "syntax": "`(read-line)` runs first because it is nested inside `define`; then `define` binds that result to the name.",
                "cpp": "Closest to declaring a string and then using `std::cin` or `std::getline` to fill it.",
            }
        if any(operator in stripped for operator in ("(+ ", "(- ", "(* ", "(/ ")):
            return {
                "line": line,
                "plain": "Binds a name to the result of a calculation.",
                "syntax": "Racket math is prefix form: `(+ a b)` means `a + b`. The calculation expression produces the value that `define` names.",
                "cpp": "Closest to `auto name = a + b;`, but the operator goes before the inputs in Racket.",
            }
        return {
            "line": line,
            "plain": "Binds a name to a value.",
            "syntax": "`define` names the value produced by the expression. It is usually a binding, not a repeated assignment statement.",
            "cpp": "Closer to `const auto name = value;` than repeated assignment.",
        }
    if stripped.startswith("(if"):
        return {"line": line, "plain": "Starts a two-way choice.", "syntax": "Racket if has a test, then result, and else result.", "cpp": "Closest to condition ? a : b."}
    if stripped.startswith("(cond"):
        return {"line": line, "plain": "Starts a multi-case choice.", "syntax": "cond checks branches in order.", "cpp": "Like if / else if / else."}
    if stripped.startswith("(case"):
        return {"line": line, "plain": "Starts exact-value branching.", "syntax": "case chooses a branch based on a matching value.", "cpp": "Similar to switch."}
    if stripped.startswith("(for"):
        return {"line": line, "plain": "Starts a loop over a sequence.", "syntax": "for and for* bind loop variables from sequences.", "cpp": "Similar to for loops, but sequence-driven."}
    if stripped.startswith("(let"):
        return {"line": line, "plain": "Creates local names or a named loop.", "syntax": "A named let can express while-style repetition.", "cpp": "Similar to a loop with local state."}
    if stripped.startswith("(struct"):
        return {"line": line, "plain": "Defines a data shape.", "syntax": "struct creates a constructor, predicate, and accessors.", "cpp": "Similar to a C++ struct or simple class."}
    if stripped.startswith("(class"):
        return {"line": line, "plain": "Defines a class expression.", "syntax": "Racket classes are values created with class.", "cpp": "Similar goal to class definitions, but expression-based."}
    if stripped.startswith("("):
        return {"line": line, "plain": "A function call or special form.", "syntax": "The first item after the opening parenthesis controls the form.", "cpp": "Like function(arg1, arg2), but the function name comes first."}
    return {"line": line, "plain": "Continuation of a larger expression.", "syntax": "Indentation shows which parentheses this line belongs to.", "cpp": "Like continuing a long C++ statement on the next line."}


def _line_note_for_python(line: str) -> dict[str, str]:
    stripped = line.strip()
    if not stripped:
        return {"line": "", "plain": "Blank line for readability.", "syntax": "Python ignores blank lines.", "cpp": "Like a blank line in C++."}
    if stripped.startswith("#"):
        return {"line": line, "plain": "A comment.", "syntax": "Python line comments start with #.", "cpp": "Like // in C++."}
    if stripped.startswith("import "):
        return {"line": line, "plain": "Imports a module.", "syntax": "import makes library code available.", "cpp": "Similar purpose to #include."}
    if stripped.startswith("def "):
        return {"line": line, "plain": "Defines a function.", "syntax": "def starts a function block and ends with a colon.", "cpp": "Similar to return_type name(args) {."}
    if stripped.startswith("class "):
        return {"line": line, "plain": "Defines a class.", "syntax": "The indented block belongs to the class.", "cpp": "Similar to class Name { ... }."}
    if stripped.startswith("if "):
        return {"line": line, "plain": "Starts a condition.", "syntax": "The indented block runs when the condition is true.", "cpp": "Similar to if (...) { ... }."}
    if stripped.startswith("elif "):
        return {"line": line, "plain": "Checks another condition.", "syntax": "elif means else-if.", "cpp": "Like else if."}
    if stripped.startswith("else"):
        return {"line": line, "plain": "Handles the remaining case.", "syntax": "else also owns an indented block.", "cpp": "Like else { ... }."}
    if stripped.startswith("while "):
        return {"line": line, "plain": "Starts a while loop.", "syntax": "The loop repeats while the condition is true.", "cpp": "Same idea as C++ while."}
    if stripped.startswith("for "):
        return {"line": line, "plain": "Starts a for loop.", "syntax": "Python loops over a sequence directly.", "cpp": "Similar to range-based for."}
    if stripped.startswith("return"):
        return {"line": line, "plain": "Returns a value from a function.", "syntax": "return exits the current function.", "cpp": "Same role as C++ return."}
    if "print(" in stripped:
        return {"line": line, "plain": "Prints output.", "syntax": "print is a built-in function.", "cpp": "Similar purpose to std::cout."}
    if "=" in stripped:
        return {"line": line, "plain": "Binds or updates a name.", "syntax": "Python names do not need declared types.", "cpp": "Similar to auto name = value, but dynamically typed."}
    return {"line": line, "plain": "A normal Python line.", "syntax": "Use indentation to see the owning block.", "cpp": "Like reading inside C++ braces."}


def _line_note_for_c_like(line: str, language: str) -> dict[str, str]:
    stripped = line.strip()
    if not stripped:
        return {"line": "", "plain": "Blank line for readability.", "syntax": f"{language} ignores blank lines.", "cpp": "Same as C++."}
    if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
        return {"line": line, "plain": "A comment.", "syntax": f"{language} supports line and block comments.", "cpp": "Same comment style as C++."}
    if stripped.startswith("#include") or stripped.startswith("import "):
        return {"line": line, "plain": "Imports library support.", "syntax": "This makes external names available.", "cpp": "Same purpose as preparing headers or libraries in C++."}
    if stripped.startswith("class ") or " class " in stripped or stripped.startswith("public class"):
        return {"line": line, "plain": "Defines a class.", "syntax": f"{language} class bodies group fields, methods, and constructors.", "cpp": "Similar goal to class Name { ... }."}
    if stripped.startswith("struct ") or " struct " in stripped:
        return {"line": line, "plain": "Defines a data shape.", "syntax": f"{language} uses this form to group related fields.", "cpp": "Similar to a C++ struct or simple class."}
    if "main(" in stripped:
        return {"line": line, "plain": "Program entry point.", "syntax": "Execution starts here for this sample.", "cpp": "Same role as C++ main."}
    if stripped.startswith("if "):
        return {"line": line, "plain": "Starts a condition.", "syntax": "The condition controls whether the block runs.", "cpp": "Same if shape as C++."}
    if stripped.startswith("else if") or stripped.startswith("else"):
        return {"line": line, "plain": "Continues a condition chain.", "syntax": "This handles a later branch.", "cpp": "Same else-if or else idea as C++."}
    if stripped.startswith("for "):
        return {"line": line, "plain": "Starts a for loop.", "syntax": "The loop controls repetition.", "cpp": "Same core loop idea as C++."}
    if stripped.startswith("while ") or stripped.startswith("do "):
        return {"line": line, "plain": "Starts or continues a repetition loop.", "syntax": "The condition decides when repetition stops.", "cpp": "Same loop family as C++."}
    if stripped.startswith("switch "):
        return {"line": line, "plain": "Starts exact-case branching.", "syntax": "A switch compares one value against cases.", "cpp": "Same switch idea as C++."}
    if stripped.startswith("return"):
        return {"line": line, "plain": "Returns from a function.", "syntax": "The current function exits here.", "cpp": "Same role as C++ return."}
    if "printf" in stripped or "System.out.println" in stripped:
        return {"line": line, "plain": "Prints output.", "syntax": "This writes a value to the console.", "cpp": "Similar purpose to std::cout."}
    if stripped.endswith("{"):
        return {"line": line, "plain": "Starts a block.", "syntax": "Braces group statements.", "cpp": "Same as C++ braces."}
    if stripped in {"}", "};"}:
        return {"line": line, "plain": "Ends a block.", "syntax": "This closes the nearest open brace.", "cpp": "Same as C++."}
    if stripped.endswith(";"):
        return {"line": line, "plain": "A statement.", "syntax": f"Most {language} statements end with a semicolon.", "cpp": "Very close to C++ syntax."}
    return {"line": line, "plain": "A normal code line.", "syntax": "Read it with the surrounding braces and declarations.", "cpp": "Use the same scope-reading habit as C++."}


def _line_notes(code: str, target: str, base: str = "cpp") -> list[dict]:
    if target == "racket":
        notes = [_line_note_for_racket(line) for line in code.splitlines()]
    elif target == "python":
        notes = [_line_note_for_python(line) for line in code.splitlines()]
    else:
        language = TARGET_LANGUAGES[target]["name"]
        notes = [_line_note_for_c_like(line, language) for line in code.splitlines()]
    return [
        {
            **note,
            "cpp": _base_comparison(note, target, base),
            "phrases": _phrase_breakdown(note.get("line", ""), target),
        }
        for note in notes
    ]


def _lesson(day: int, target: str, base: str = "cpp") -> dict:
    title, kind = TOPICS[day - 1]
    language = TARGET_LANGUAGES[target]["name"]
    base_language = TARGET_LANGUAGES[base]["name"]
    code = _code(kind, target)
    bridge = _syntax_bridge(title, kind, target, base)
    lesson = Lesson(
        day=day,
        category=f"Day {day:02d} - {title}",
        week=((day - 1) // 7) + 1,
        title=title,
        goal=_goal(title, target, base),
        cpp_bridge=(
            f"This is the prerequisite {base_language} baseline for later language comparison."
            if target == base
            else f"Use the {base_language} snippet as the familiar baseline. Then compare how {language} expresses "
            "the same idea through its own syntax, naming, and standard library."
        ),
        explanation=_explanation(title, kind, target, base),
        syntax_bridge=bridge,
        official_docs=bridge["docs"],
        racket_focus=_focus(title, kind, target, base),
        code=code,
        line_notes=_line_notes(code, target, base),
        practice=_practice(day, title, kind, target, base),
        checklist=_checklist(day, title, target, base),
        assignment=_assignment(day, title, target, base),
        grading_rubric=_rubric(target, base),
    )
    data = asdict(lesson)
    data["target_language"] = target
    data["target_language_name"] = language
    data["base_language"] = base
    data["base_language_name"] = base_language
    data["topic_kind"] = kind
    data["base_kind"] = _base_kind(kind)
    return data


def get_lessons(target_language: str | None = None, base_language: str | None = None) -> list[dict]:
    target = normalize_target_language(target_language)
    base = normalize_base_language(base_language)
    return [_lesson(day, target, base) for day in range(1, len(TOPICS) + 1)]


def get_lesson(day: int, target_language: str | None = None, base_language: str | None = None) -> dict | None:
    lessons = get_lessons(target_language, base_language)
    if 1 <= day <= len(lessons):
        return lessons[day - 1]
    return None
