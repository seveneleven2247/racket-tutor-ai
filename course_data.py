from __future__ import annotations

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
    line_notes: list[dict[str, str]]
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
    "input": "Read a value from the user and store it in a name so the program can react to outside data.",
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


SNIPPETS = {
    "output": {
        "cpp": """#include <iostream>

int main() {
    std::cout << "Hello, C++!" << std::endl;
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
        "cpp": """std::string name;
std::cin >> name;
std::cout << "Hi " << name << std::endl;""",
        "racket": """#lang racket

(display "Name: ")
(define name (read-line))
(displayln (string-append "Hi " name))""",
        "python": """name = input("Name: ")
print("Hi " + name)""",
        "c": """#include <stdio.h>

int main(void) {
    char name[40];
    scanf("%39s", name);
    printf("Hi %s\\n", name);
    return 0;
}""",
        "java": """import java.util.Scanner;

public class Day02 {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        String name = input.nextLine();
        System.out.println("Hi " + name);
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


def _docs_for(target: str) -> list[dict[str, str]]:
    return DOCS[target]


def _summary(kind: str) -> str:
    return KIND_SUMMARIES.get(kind) or KIND_SUMMARIES.get(_base_kind(kind)) or DEFAULT_SUMMARY


def _code(kind: str, target: str) -> str:
    return SNIPPETS[_base_kind(kind)][target]


def _cpp(kind: str) -> str:
    return SNIPPETS[_base_kind(kind)]["cpp"]


def _focus(title: str, kind: str, target: str) -> list[str]:
    language = TARGET_LANGUAGES[target]["name"]
    base = _base_kind(kind).replace("_", " ")
    return [
        f"{language} syntax",
        f"C++ comparison: {base}",
        "line-by-line explanation",
        "small runnable example",
    ]


def _syntax_bridge(title: str, kind: str, target: str) -> dict:
    language = TARGET_LANGUAGES[target]["name"]
    if target == "cpp":
        return {
            "concept": f"C++ foundation: {title}.",
            "cpp": _cpp(kind),
            "racket": _code(kind, target),
            "target": _code(kind, target),
            "target_label": language,
            "translation_steps": [
                "Read the C++ example from top to bottom and identify the output, input, and processing lines.",
                "Mark the syntax pieces: header, main function, declarations, statements, blocks, and semicolons.",
                "Run the smallest version first, then change one value and predict the new result.",
                "Write one short note per important line so later languages have a clear C++ baseline.",
            ],
            "pitfalls": [
                "Do not skip main, headers, or semicolons until you can explain why they are there.",
                "Do not memorize syntax alone; connect each line to a concrete program action.",
                "Keep examples small enough that compiler errors point to one concept at a time.",
            ],
            "drill": f"Type the C++ snippet, run it, then explain every non-blank line in plain English.",
            "today_angle": f"Prerequisite C++ topic: {title}. Build the baseline before moving to another language.",
            "docs": _docs_for(target),
        }
    return {
        "concept": f"{title}: translate the C++ pattern into {language}.",
        "cpp": _cpp(kind),
        "racket": _code(kind, target),
        "target": _code(kind, target),
        "target_label": language,
        "translation_steps": [
            "First identify what the C++ code is doing, not just which symbols it uses.",
            f"Write the same idea using normal {language} syntax and naming.",
            "Run the smallest version, then change one value and predict the output.",
            "Add one short note per important line explaining the C++ comparison.",
        ],
        "pitfalls": [
            "Do not copy C++ punctuation when the target language has a different block style.",
            f"Use the standard {language} library or idiom instead of forcing a literal translation.",
            "Keep input, calculation, and output separated when the example grows.",
        ],
        "drill": f"Rewrite the C++ snippet in {language}, then explain every non-blank line.",
        "today_angle": f"Day topic: {title}. Start from C++, then write the target-language version.",
        "docs": _docs_for(target),
    }


def _goal(title: str, target: str) -> str:
    language = TARGET_LANGUAGES[target]["name"]
    if target == "cpp":
        return f"Build the C++ foundation for {title.lower()} before starting another target language."
    return f"Learn {title.lower()} in {language} by comparing it directly with the C++ version you already understand."


def _explanation(title: str, kind: str, target: str) -> str:
    language = TARGET_LANGUAGES[target]["name"]
    if target == "cpp":
        return (
            f"{_summary(kind)} This prerequisite track teaches the C++ version first. "
            "Focus on what each line does, where the syntax boundaries are, and how the compiler reads the program. "
            "Once this baseline is comfortable, the other language tracks can compare against it directly."
        )
    return (
        f"{_summary(kind)} In this lesson, read the C++ snippet first and name the exact idea. "
        f"Then study the {language} code line by line. Keep the explanation short: what the line does, "
        "what syntax it uses, and which C++ habit it matches or replaces."
    )


def _practice(day: int, title: str, target: str) -> list[str]:
    language = TARGET_LANGUAGES[target]["name"]
    ext = TARGET_LANGUAGES[target]["file_ext"]
    return [
        (
            f"HW Q1: Write Program 1 in day{day:02d}_q1.{ext}. Make a small, original {language} program that demonstrates '{title}'. "
            "This must be a complete standalone program with its own output, not a section inside another answer."
        ),
        (
            f"HW Q2: Write Program 2 in day{day:02d}_q2.{ext}. Create a different program that solves a new example using the same topic. "
            "Use different values, names, and structure from HW Q1, and add at least three short C++ comparison comments."
        ),
        (
            f"HW Q3: Write Program 3 in day{day:02d}_q3.{ext}. Create a third different program that combines today's topic with one earlier idea. "
            "Before the final output, include a brief prediction in a comment and then print the actual result."
        ),
    ]


def _checklist(day: int, title: str, target: str) -> list[str]:
    language = TARGET_LANGUAGES[target]["name"]
    return [
        f"Read Day {day:02d}: {title}.",
        f"Compare the C++ snippet with the {language} snippet.",
        "Type the sample by hand and run it.",
        "Mark the input, processing, and output lines if they exist.",
        "Complete three separate homework programs: HW Q1, HW Q2, and HW Q3.",
        "Submit all three programs plus concise C++ comparison notes.",
    ]


def _rubric(target: str) -> list[str]:
    language = TARGET_LANGUAGES[target]["name"]
    return [
        "Correctness: the code runs and matches the assignment.",
        f"{language} syntax: the code uses normal {language} structure and naming.",
        "C++ transfer: the notes clearly explain what changed from C++.",
        "Completeness: all three separate homework programs are included.",
        "Clarity: line-by-line comments are concise and accurate.",
    ]


def _assignment(day: int, title: str, target: str) -> str:
    ext = TARGET_LANGUAGES[target]["file_ext"]
    return (
        f"Submit three different programs: day{day:02d}_q1.{ext}, day{day:02d}_q2.{ext}, and day{day:02d}_q3.{ext}. "
        "If you paste code instead of uploading files, paste all three programs in order with clear labels: HW Q1, HW Q2, HW Q3. "
        f"Each program must demonstrate '{title}', run successfully by itself, and include concise notes comparing the target-language syntax with C++."
    )


def _line_note_for_racket(line: str) -> dict[str, str]:
    stripped = line.strip()
    if not stripped:
        return {"line": "", "plain": "Blank line for readability.", "syntax": "Racket ignores blank lines.", "cpp": "Like a blank line between C++ blocks."}
    if stripped.startswith("#lang"):
        return {"line": line, "plain": "Selects the Racket language for this file.", "syntax": "#lang usually appears on the first line.", "cpp": "Closest to choosing a compiler language mode."}
    if stripped.startswith(";"):
        return {"line": line, "plain": "A comment for the reader.", "syntax": "A semicolon starts a Racket line comment.", "cpp": "Like // in C++."}
    if stripped.startswith("(define ("):
        return {"line": line, "plain": "Defines a function.", "syntax": "The function name and parameters appear after define.", "cpp": "Similar to return_type name(args), but plain Racket has no parameter types here."}
    if stripped.startswith("(define "):
        return {"line": line, "plain": "Binds a name to a value.", "syntax": "define names the value produced by the expression.", "cpp": "Closer to const auto name = value; than repeated assignment."}
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
    if "main(" in stripped:
        return {"line": line, "plain": "Program entry point.", "syntax": "Execution starts here for this sample.", "cpp": "Same role as C++ main."}
    if stripped.endswith("{"):
        return {"line": line, "plain": "Starts a block.", "syntax": "Braces group statements.", "cpp": "Same as C++ braces."}
    if stripped in {"}", "};"}:
        return {"line": line, "plain": "Ends a block.", "syntax": "This closes the nearest open brace.", "cpp": "Same as C++."}
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
    if stripped.endswith(";"):
        return {"line": line, "plain": "A statement.", "syntax": f"Most {language} statements end with a semicolon.", "cpp": "Very close to C++ syntax."}
    return {"line": line, "plain": "A normal code line.", "syntax": "Read it with the surrounding braces and declarations.", "cpp": "Use the same scope-reading habit as C++."}


def _line_notes(code: str, target: str) -> list[dict[str, str]]:
    if target == "racket":
        return [_line_note_for_racket(line) for line in code.splitlines()]
    if target == "python":
        return [_line_note_for_python(line) for line in code.splitlines()]
    language = TARGET_LANGUAGES[target]["name"]
    return [_line_note_for_c_like(line, language) for line in code.splitlines()]


def _lesson(day: int, target: str) -> dict:
    title, kind = TOPICS[day - 1]
    language = TARGET_LANGUAGES[target]["name"]
    code = _code(kind, target)
    bridge = _syntax_bridge(title, kind, target)
    lesson = Lesson(
        day=day,
        category=f"Day {day:02d} - {title}",
        week=((day - 1) // 7) + 1,
        title=title,
        goal=_goal(title, target),
        cpp_bridge=(
            "This is the prerequisite C++ baseline for later language comparison."
            if target == "cpp"
            else f"Use the C++ snippet as the familiar baseline. Then compare how {language} expresses "
            "the same idea through its own syntax, naming, and standard library."
        ),
        explanation=_explanation(title, kind, target),
        syntax_bridge=bridge,
        official_docs=bridge["docs"],
        racket_focus=_focus(title, kind, target),
        code=code,
        line_notes=_line_notes(code, target),
        practice=_practice(day, title, target),
        checklist=_checklist(day, title, target),
        assignment=_assignment(day, title, target),
        grading_rubric=_rubric(target),
    )
    data = asdict(lesson)
    data["target_language"] = target
    data["target_language_name"] = language
    return data


def get_lessons(target_language: str | None = None) -> list[dict]:
    target = normalize_target_language(target_language)
    return [_lesson(day, target) for day in range(1, len(TOPICS) + 1)]


def get_lesson(day: int, target_language: str | None = None) -> dict | None:
    lessons = get_lessons(target_language)
    if 1 <= day <= len(lessons):
        return lessons[day - 1]
    return None
