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
    "r": {"id": "r", "name": "R", "file_ext": "R", "runner": "Rscript day01.R"},
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
    "r": [
        {"title": "R Manuals", "url": "https://cran.r-project.org/manuals.html"},
        {"title": "An Introduction to R", "url": "https://cran.r-project.org/doc/manuals/r-release/R-intro.html"},
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


R_STATISTICS_TOPICS = [
    {
        "title": "R Data Analysis: Import and Inspect Data Frames",
        "kind": "r_data_frame",
        "summary": "Start statistics work by putting observations into rows and variables into columns, then inspect the data before calculating anything.",
        "code": """scores <- data.frame(
    student = c("Ava", "Ben", "Chen", "Dia", "Eli"),
    study_hours = c(4, 6, 3, 8, 5),
    exam_score = c(78, 84, 73, 92, 81)
)

cat("Rows:", nrow(scores), "\\n")
cat("Columns:", ncol(scores), "\\n")
print(head(scores, 3))
str(scores)""",
        "output": "Rows: 5\nColumns: 3\nFirst 3 rows show student, study_hours, and exam_score.\nstr() reports column names and data types.",
        "concept": "Data frames store statistics datasets: each row is one case, and each column is one variable.",
        "translation": [
            "Think of a C++ vector of records or a table: each student has related fields.",
            "In R, `data.frame(...)` creates that table directly with named columns.",
            "`nrow`, `ncol`, `head`, and `str` are inspection tools. Use them before trusting calculations.",
        ],
        "pitfalls": [
            "Do not calculate before checking row count, column names, and data types.",
            "Do not confuse rows with columns. In statistics, rows are observations and columns are variables.",
            "R uses 1-based indexing, so row 1 is the first row.",
        ],
    },
    {
        "title": "R Data Analysis: Missing Values and Data Types",
        "kind": "r_missing_types",
        "summary": "Real statistics data often has missing values and wrong types. Clean them before computing means, tests, or models.",
        "code": """raw <- data.frame(
    student = c("Ava", "Ben", "Chen", "Dia", "Eli"),
    study_hours = c(4, NA, 3, 8, 5),
    exam_score = c(78, 84, NA, 92, 81),
    passed = c(TRUE, TRUE, FALSE, TRUE, TRUE)
)

cat("Missing values by column:\\n")
print(colSums(is.na(raw)))

clean <- na.omit(raw)
clean$exam_score <- as.numeric(clean$exam_score)
print(clean)""",
        "output": "Missing values by column:\nstudent 0, study_hours 1, exam_score 1, passed 0\nThe cleaned data keeps complete rows and numeric exam_score values.",
        "concept": "`NA` means missing data. `is.na`, `colSums`, and `na.omit` help you find and handle missing values.",
        "translation": [
            "In C++, you might use a sentinel value or optional field. R uses `NA` as the standard missing marker.",
            "`is.na(raw)` creates TRUE/FALSE checks for every cell.",
            "`colSums(...)` counts TRUE values by column because TRUE behaves like 1 and FALSE behaves like 0.",
        ],
        "pitfalls": [
            "Do not treat missing data as zero unless the assignment says zero is meaningful.",
            "Do not ignore data types. A number stored as text can break statistics functions.",
            "Dropping rows with `na.omit` is simple, but it changes sample size.",
        ],
    },
    {
        "title": "R Data Analysis: Descriptive Statistics",
        "kind": "r_descriptive_stats",
        "summary": "Descriptive statistics summarize one variable with center, spread, and range before any formal inference.",
        "code": """scores <- c(78, 84, 73, 92, 81, 88, 76)

mean_score <- mean(scores)
median_score <- median(scores)
sd_score <- sd(scores)
score_range <- range(scores)

cat(sprintf("Mean: %.2f\\n", mean_score))
cat(sprintf("Median: %.2f\\n", median_score))
cat(sprintf("Standard deviation: %.2f\\n", sd_score))
cat("Range:", score_range[1], "to", score_range[2], "\\n")""",
        "output": "Mean: 81.71\nMedian: 81.00\nStandard deviation: about 6.75\nRange: 73 to 92",
        "concept": "Mean and median describe center. Standard deviation and range describe spread.",
        "translation": [
            "A C++ loop can compute totals manually. R gives direct statistics functions such as `mean`, `median`, and `sd`.",
            "`range(scores)` returns two values: minimum and maximum.",
            "`sprintf` formats decimal output so results look clean in a statistics report.",
        ],
        "pitfalls": [
            "Do not report only the mean when spread matters.",
            "Do not round too early. Calculate first, round when printing.",
            "If data has `NA`, use `mean(scores, na.rm = TRUE)` or clean first.",
        ],
    },
    {
        "title": "R Data Analysis: Grouped Summaries and Tables",
        "kind": "r_grouped_summary",
        "summary": "Statistics often compares groups. Use grouped summaries and cross tables to see patterns before formal tests.",
        "code": """classes <- data.frame(
    section = c("A", "A", "A", "B", "B", "B"),
    exam_score = c(78, 84, 88, 72, 81, 90),
    passed = c(TRUE, TRUE, TRUE, TRUE, TRUE, TRUE)
)

section_mean <- aggregate(exam_score ~ section, data = classes, FUN = mean)
section_sd <- aggregate(exam_score ~ section, data = classes, FUN = sd)
pass_table <- table(classes$section, classes$passed)

print(section_mean)
print(section_sd)
print(pass_table)""",
        "output": "Section A mean is 83.33. Section B mean is 81.00.\nThe table counts passed status inside each section.",
        "concept": "`aggregate` calculates a statistic separately for each group. `table` counts category combinations.",
        "translation": [
            "In C++, grouped statistics usually means loops plus if statements for each category.",
            "In R, formulas like `exam_score ~ section` mean: summarize exam_score by section.",
            "`table(x, y)` builds a contingency table, which is useful for categorical statistics.",
        ],
        "pitfalls": [
            "Do not compare group means without checking group size and spread.",
            "Do not use numeric summaries for purely categorical variables.",
            "Make sure the grouping variable is the correct column.",
        ],
    },
    {
        "title": "R Data Analysis: Statistical Graphics",
        "kind": "r_graphics",
        "summary": "Graphs reveal shape, outliers, group differences, and relationships faster than raw numbers.",
        "code": """scores <- c(78, 84, 73, 92, 81, 88, 76, 95)
group <- c("A", "A", "A", "A", "B", "B", "B", "B")
study_hours <- c(4, 6, 3, 8, 5, 7, 4, 9)

png("day61_plots.png", width = 900, height = 300)
par(mfrow = c(1, 3))
hist(scores, main = "Exam Scores", xlab = "Score", col = "lightblue")
boxplot(scores ~ group, main = "Scores by Group", xlab = "Group", ylab = "Score")
plot(study_hours, scores, main = "Study vs Score", xlab = "Hours", ylab = "Score")
abline(lm(scores ~ study_hours), col = "red")
dev.off()

cat("Saved day61_plots.png\\n")""",
        "output": "Saved day61_plots.png\nThe file contains a histogram, a boxplot, and a scatterplot with a regression line.",
        "concept": "Use histograms for one numeric variable, boxplots for group comparisons, and scatterplots for two numeric variables.",
        "translation": [
            "C++ can print numbers, but statistics needs visual checks. R has plotting functions built in.",
            "`par(mfrow = c(1, 3))` puts three plots in one row.",
            "`abline(lm(...))` adds a fitted regression line to the scatterplot.",
        ],
        "pitfalls": [
            "Do not choose a plot before identifying variable types.",
            "Do not use a line plot for unrelated students unless order matters.",
            "Always label axes so another reader knows what each number means.",
        ],
    },
    {
        "title": "R Data Analysis: Probability Distributions and Simulation",
        "kind": "r_distribution_sim",
        "summary": "Statistics uses distributions to describe randomness. Simulation helps you see sampling variation.",
        "code": """set.seed(11)
sample_means <- replicate(1000, mean(rnorm(30, mean = 70, sd = 10)))

cat(sprintf("Mean of sample means: %.2f\\n", mean(sample_means)))
cat(sprintf("SD of sample means: %.2f\\n", sd(sample_means)))
cat(sprintf("Theoretical standard error: %.2f\\n", 10 / sqrt(30)))
cat(sprintf("97.5th percentile for one score: %.2f\\n", qnorm(0.975, mean = 70, sd = 10)))""",
        "output": "Mean of sample means is near 70.\nSD of sample means is near 1.83.\n97.5th percentile for one score is about 89.60.",
        "concept": "`rnorm` simulates normal data, `replicate` repeats an experiment, and `qnorm` finds normal distribution cutoffs.",
        "translation": [
            "In C++, simulation means writing loops and random-number setup. R gives direct distribution functions.",
            "`set.seed` makes random output reproducible for homework checking.",
            "The standard error is the standard deviation of many sample means.",
        ],
        "pitfalls": [
            "Do not confuse standard deviation of individuals with standard error of a mean.",
            "Do not omit `set.seed` when you need reproducible simulated results.",
            "Simulation supports reasoning; it does not replace the formula when the formula is required.",
        ],
    },
    {
        "title": "R Data Analysis: Confidence Intervals",
        "kind": "r_confidence_interval",
        "summary": "A confidence interval estimates a population mean with uncertainty, not just one single sample average.",
        "code": """scores <- c(78, 84, 73, 92, 81, 88, 76, 95)
n <- length(scores)
mean_score <- mean(scores)
sd_score <- sd(scores)
standard_error <- sd_score / sqrt(n)
margin <- qt(0.975, df = n - 1) * standard_error
lower <- mean_score - margin
upper <- mean_score + margin

cat(sprintf("Mean: %.2f\\n", mean_score))
cat(sprintf("95%% CI: %.2f to %.2f\\n", lower, upper))""",
        "output": "Mean: 83.38\n95% CI: lower bound to upper bound around the sample mean.",
        "concept": "A confidence interval is mean plus or minus a critical value times standard error.",
        "translation": [
            "C++ can calculate the formula step by step. R gives `qt` for the t critical value.",
            "`df = n - 1` is degrees of freedom for a one-sample t interval.",
            "`95%%` in `sprintf` prints a literal percent sign.",
        ],
        "pitfalls": [
            "Do not say there is a 95% probability this exact interval contains the mean after it is computed.",
            "Do not use z critical values for small samples when population SD is unknown.",
            "Always report sample size with the interval.",
        ],
    },
    {
        "title": "R Data Analysis: Hypothesis Testing with t.test",
        "kind": "r_t_test",
        "summary": "A t-test compares a mean or mean difference against a null hypothesis using sample data.",
        "code": """before <- c(72, 75, 78, 70, 74, 77)
after <- c(76, 79, 80, 74, 78, 82)

change <- after - before
test_result <- t.test(after, before, paired = TRUE)

cat("Mean change:", mean(change), "\\n")
print(test_result)""",
        "output": "Mean change: about 3.83\nThe paired t-test output includes t, df, p-value, confidence interval, and mean difference.",
        "concept": "`t.test(..., paired = TRUE)` compares matched before/after measurements for the same subjects.",
        "translation": [
            "C++ can calculate differences, but R's `t.test` also reports p-value and confidence interval.",
            "`paired = TRUE` matters because each before score belongs to the same student as the after score.",
            "The p-value measures how surprising the observed change is if the true mean change were zero.",
        ],
        "pitfalls": [
            "Do not use a paired test for unrelated groups.",
            "Do not write 'proved' when a test is significant. Say the result provides evidence.",
            "Check the direction of subtraction so the mean change has the intended sign.",
        ],
    },
    {
        "title": "R Data Analysis: Correlation and Linear Regression",
        "kind": "r_regression",
        "summary": "Correlation measures association. Linear regression models a numeric response from an explanatory variable.",
        "code": """study_hours <- c(2, 3, 4, 5, 6, 7, 8)
exam_score <- c(68, 72, 78, 81, 85, 89, 94)

cat(sprintf("Correlation: %.3f\\n", cor(study_hours, exam_score)))

model <- lm(exam_score ~ study_hours)
print(summary(model))

new_student <- data.frame(study_hours = 6.5)
prediction <- predict(model, new_student)
cat(sprintf("Predicted score for 6.5 hours: %.2f\\n", prediction))""",
        "output": "Correlation is strongly positive.\nThe regression summary reports slope, intercept, R-squared, and p-values.\nA prediction is printed for 6.5 study hours.",
        "concept": "`lm(y ~ x)` fits a line predicting response y from explanatory variable x.",
        "translation": [
            "In C++, you would manually compute sums for slope and intercept. R's `lm` fits the model directly.",
            "The formula `exam_score ~ study_hours` reads as: model exam_score using study_hours.",
            "`predict` applies the fitted model to a new data frame with the same predictor column name.",
        ],
        "pitfalls": [
            "Correlation is not causation.",
            "Do not predict far outside the data range without warning.",
            "Always inspect a scatterplot before trusting a linear model.",
        ],
    },
    {
        "title": "R Data Analysis: Chi-Square Test and Statistical Report",
        "kind": "r_chi_square_report",
        "summary": "A chi-square test checks whether two categorical variables are associated, then you report the result clearly.",
        "code": """club_table <- matrix(c(18, 12, 10, 20), nrow = 2, byrow = TRUE)
rownames(club_table) <- c("STEM", "Humanities")
colnames(club_table) <- c("Club", "NoClub")

test_result <- chisq.test(club_table)

print(club_table)
print(test_result)
cat("Report sentence: A chi-square test checked whether subject group and club participation were associated.\\n")""",
        "output": "The contingency table is printed.\nchisq.test reports X-squared, df, and p-value.\nA report sentence explains the test purpose.",
        "concept": "`chisq.test` compares observed category counts with expected counts under independence.",
        "translation": [
            "In C++, a 2D array can store counts. R's matrix plus `chisq.test` performs the statistical test.",
            "Rows and columns must have meaningful names so the result is readable.",
            "A statistics report should name the test, variables, result, and conclusion in plain language.",
        ],
        "pitfalls": [
            "Do not run chi-square on raw percentages; use counts.",
            "Do not hide the table. Readers need to see the observed counts.",
            "If expected counts are too small, ask whether Fisher's exact test is more appropriate.",
        ],
    },
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
    "r": (
        "R commonly reads beginner input with `readline()`, which returns text. Convert text with `as.integer(...)` for whole numbers, `as.numeric(...)` for decimals, "
        "`tolower(...) == \"true\"` for booleans, `substr(text, 1, 1)` for one character, and `scan(text = readline(), what = integer(), quiet = TRUE)` for a vector of integers. "
        "To output a sentence with variables, use `cat(sprintf(...))` or `paste(...)`. Be careful: R vectors are 1-indexed, so the first item is `scores[1]`, not `scores[0]`."
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
        "r": """cat("Hello, R!\\n")
cat(42, "\\n")""",
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
        "r": """name <- readline("Name: ")
age <- as.integer(readline("Age integer: "))
price <- as.numeric(readline("Price decimal: "))
member <- tolower(readline("Member true/false: ")) == "true"
initial <- substr(readline("Initial character: "), 1, 1)
scores <- scan(text = readline("Three integer scores: "), what = integer(), quiet = TRUE)

cat(sprintf("%s is %d years old. Price: %.2f. Member: %s. Initial: %s. First score: %d\\n",
            name, age, price, member, initial, scores[1]))""",
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
        "r": """subtotal <- 80
tax <- 10
total <- subtotal + tax
average <- total / 2.0""",
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
        "r": """count <- 3
price <- 9.99
label <- "book" """,
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
        "r": """score <- 72
if (score >= 60) {
    cat("pass\\n")
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
        "r": """score <- 84
if (score >= 90) {
    grade <- "A"
} else if (score >= 80) {
    grade <- "B"
} else {
    grade <- "Practice"
}
cat(grade, "\\n")""",
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
        "r": """average <- function(total, count) {
    if (count <= 0) {
        stop("count must be positive")
    }
    total / count
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
        "r": """n <- 3
while (n > 0) {
    cat(n, "\\n")
    n <- n - 1
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
        "r": """repeat {
    choice <- 0
    if (choice == 0) {
        break
    }
}""",
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
        "r": """number <- sample(1:10, 1)
cat(number, "\\n")""",
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
        "r": """for (i in 0:4) {
    cat(i, "\\n")
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
        "r": """for (row in 0:2) {
    for (col in 0:2) {
        cat(row, ",", col, "\\n", sep = "")
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
        "r": """square <- function(x) {
    x * x
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
        "r": """add_tax <- function(amount) {
    amount * 1.13
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
        "r": """square <- function(x) {
    x * x
}

result <- square(5)
cat(result, "\\n")""",
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
        "r": """scores <- c(90, 85, 100)
cat(scores[1], "\\n")""",
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
        "r": """fixed <- c(1, 2, 3)
dynamic <- list(1, 2, 3)
lookup <- c(one = 1)""",
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
        "r": """values <- c(0, 1, 2, 3)
names <- c("Ada", "Grace")""",
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
        "r": """first <- "Ada"
message <- paste("Hi", first)
cat(message, "\\n")""",
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
        "r": """chars <- strsplit("code", "")[[1]]
word <- paste(chars, collapse = "")""",
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
        "r": """student <- list(name = "Ada", score = 95)
class(student) <- "Student" """,
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
        "r": """choice <- 1
label <- switch(as.character(choice),
                "1" = "start",
                "quit")
cat(label, "\\n")""",
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
        "r": """grid <- matrix(c(1, 2, 3, 4, 5, 6), nrow = 2, byrow = TRUE)
cat(grid[2, 3], "\\n")""",
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
        "r": """nums <- c(1, 2)
nums <- c(nums, 3)
cat(nums, "\\n")""",
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
        "r": """ada <- list(name = "Ada", score = 95)
class(ada) <- "Student"
cat(ada$score, "\\n")""",
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
        "r": """fact <- function(n) {
    if (n == 0) {
        1
    } else {
        n * fact(n - 1)
    }
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
        "r": """values <- c(2.5, 3.5, 4.0)
target <- 3.5
found <- any(values == target)""",
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
        "r": """age <- 16
teen <- age >= 13 && age <= 19""",
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
        "r": """logged_in <- TRUE
is_admin <- TRUE
if (logged_in) {
    if (is_admin) {
        role <- "admin"
    } else {
        role <- "user"
    }
} else {
    role <- "guest"
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
        "r": """scores <- c(90, 80, 100)
total <- 0
for (score in scores) {
    total <- total + score
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
        "r": """grid <- matrix(c(1, 2, 3, 4), nrow = 2, byrow = TRUE)
total <- 0
for (row in 1:nrow(grid)) {
    for (col in 1:ncol(grid)) {
        total <- total + grid[row, col]
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
        "r": """score <- -1
while (score < 0 || score > 100) {
    score <- 80
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
        "r": """repeat {
    cat("1) Play  0) Quit\\n")
    choice <- 0
    if (choice == 0) {
        break
    }
}""",
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


def normalize_ui_language(language: str | None) -> str:
    value = (language or "en").strip().lower()
    return value if value in {"en", "zh", "ja", "ko", "fr"} else "en"


def _docs_for(target: str) -> list[dict[str, str]]:
    return DOCS[target]


def _summary(kind: str) -> str:
    return KIND_SUMMARIES.get(kind) or KIND_SUMMARIES.get(_base_kind(kind)) or DEFAULT_SUMMARY


LOCALIZED_KIND_SUMMARIES = {
    "zh": {
        "output": "先从看得见的程序行为开始。先打印值，让后面每个主题都有快速反馈。",
        "input": "先读取文本，然后在程序需要整数、布尔值、字符、小数或数组/列表时再转换。",
        "math": "使用算术表达式处理总和、平均值、余数和分组计算。",
        "variable": "把名字绑定到值，并分清语法中的类型、名称、值和初始化。",
        "if_statement": "使用一个条件决定某个代码块或表达式是否运行。",
        "else_if": "按顺序处理多个情况，而不是写一堆互不相关的 if。",
        "error_check": "在主逻辑依赖输入之前，先拒绝无效输入。",
        "while_loop": "当事先不知道确切次数时，只要条件仍为真就重复执行。",
        "do_while": "先运行一次循环体，再检查是否需要继续。",
        "random_number": "为游戏、测试和模拟生成不可预测的值。",
        "for_loop": "用索引或序列重复执行已知次数。",
        "nested_for": "把一个循环放进另一个循环，用来处理网格、表格和重复图案。",
        "function_intro": "把函数理解成有名字、可复用、接收输入并返回输出的代码块。",
        "create_function": "编写带参数、函数体和明确结果的自定义函数。",
        "call_function": "通过传入参数来使用函数，并保存或打印返回值。",
        "arrays_intro": "把多个相关值存到同一个名字下，并通过位置或序列访问元素。",
        "array_kinds": "比较固定数组、动态数组、列表、向量以及不同语言的集合选择。",
        "array_declare": "创建类似数组的集合，并填入初始值。",
        "strings": "表示文本、连接文本，并检查字符或子字符串。",
        "char_arrays": "当语言暴露底层表示时，把文本理解成字符序列。",
        "classes": "把数据和行为组合成一个有名字的类型。",
        "switch_statement": "从多个精确匹配的情况中选择一个分支。",
        "multi_arrays": "用嵌套数组、向量或列表表示行和列。",
        "vectors": "当元素数量会增长或缩小时，使用可调整大小的序列。",
        "objects_classes": "从类定义创建对象值，并调用对象上的方法。",
        "recursion": "通过把问题缩小成同类子问题来解决问题。",
        "search_float": "搜索集合，并用浮点值表示测量值和平均值。",
        "combined_if": "用 and、or、not 组合条件，让规则读起来清楚。",
        "nested_if": "当一个决定依赖前一个决定时，把一个 if 放在另一个 if 里面。",
        "for_arrays": "用 for 循环处理数组类集合中的每个元素。",
        "nested_for_multi": "用嵌套循环访问多维结构中的每个单元格。",
        "while_validation": "持续请求输入，直到值通过验证。",
        "do_while_menu": "至少显示一次菜单，然后一直运行到用户选择停止。",
        "default": "把前面学过的技能组合成一个小程序。保持代码简短、可测试，并且容易逐行解释。",
    },
    "ja": {
        "output": "まず目に見えるプログラムの動作から始めます。最初に値を出力すると、後の各トピックで素早く確認できます。",
        "input": "まずテキストを読み、整数、真偽値、文字、小数、配列/リストが必要なときに変換します。",
        "math": "合計、平均、余り、まとまった計算には算術式を使います。",
        "variable": "名前を値に結び付け、型、名前、値、初期化が構文のどこにあるかを学びます。",
        "if_statement": "1 つの条件で、ブロックや式を実行するかどうかを選びます。",
        "else_if": "複数のケースを順番に扱い、無関係な if を並べないようにします。",
        "error_check": "主な処理が入力に依存する前に、無効な入力を拒否します。",
        "while_loop": "正確な回数が事前に分からないとき、条件が真の間くり返します。",
        "do_while": "本体を一度実行してから、もう一度くり返すかを確認します。",
        "random_number": "ゲーム、テスト、シミュレーションのために予測できない値を生成します。",
        "for_loop": "インデックスやシーケンスを使って、決まった回数くり返します。",
        "nested_for": "ループの中にループを置き、グリッド、表、反復パターンを扱います。",
        "function_intro": "関数を、入力を受け取り出力を返す、名前付きで再利用できるブロックとして理解します。",
        "create_function": "引数、本体、明確な結果を持つ自分の関数を書きます。",
        "call_function": "引数を渡して関数を使い、返された値を保存または出力します。",
        "arrays_intro": "関連する複数の値を 1 つの名前の下に保存し、位置や順序で要素にアクセスします。",
        "array_kinds": "固定配列、動的配列、リスト、ベクター、言語ごとのコレクションを比較します。",
        "array_declare": "配列のようなコレクションを作り、初期値を入れます。",
        "strings": "テキストを表し、結合し、文字や部分文字列を調べます。",
        "char_arrays": "言語がその表現を見せる場合、テキストを文字の並びとして理解します。",
        "classes": "データと動作を名前付きの型にまとめます。",
        "switch_statement": "複数の完全一致ケースから 1 つの分岐を選びます。",
        "multi_arrays": "行と列を、ネストした配列、ベクター、リストで表します。",
        "vectors": "要素数が増減する場合は、サイズ変更できるシーケンスを使います。",
        "objects_classes": "クラス定義からオブジェクト値を作り、そのメソッドを呼び出します。",
        "recursion": "問題を同じ形の小さな問題に分解して解きます。",
        "search_float": "コレクションを検索し、測定値や平均には浮動小数点値を使います。",
        "combined_if": "and、or、not で条件を組み合わせ、ルールを読みやすくします。",
        "nested_if": "ある判断が前の判断に依存する場合、if の中に if を置きます。",
        "for_arrays": "for ループで配列のようなコレクションの全要素を処理します。",
        "nested_for_multi": "ネストしたループで多次元構造の各セルを訪問します。",
        "while_validation": "値が検証を通るまで入力を求め続けます。",
        "do_while_menu": "メニューを少なくとも一度表示し、ユーザーが停止を選ぶまで続けます。",
        "default": "これまでの技能を小さなプログラムにまとめます。コードは短く、テストしやすく、行ごとに説明しやすくします。",
    },
    "ko": {
        "output": "먼저 눈에 보이는 프로그램 동작부터 시작합니다. 값을 먼저 출력하면 이후 모든 주제에서 빠르게 확인할 수 있습니다.",
        "input": "먼저 텍스트를 읽고, 정수, 불리언, 문자, 소수, 배열/리스트가 필요할 때 변환합니다.",
        "math": "합계, 평균, 나머지, 묶음 계산에는 산술식을 사용합니다.",
        "variable": "이름을 값에 연결하고, 문법에서 타입, 이름, 값, 초기화가 어디에 있는지 배웁니다.",
        "if_statement": "하나의 조건으로 블록이나 표현식이 실행될지 선택합니다.",
        "else_if": "여러 경우를 순서대로 처리하고, 서로 관련 없는 if를 따로 쓰지 않습니다.",
        "error_check": "주요 로직이 입력에 의존하기 전에 잘못된 입력을 거부합니다.",
        "while_loop": "정확한 반복 횟수를 모를 때 조건이 참인 동안 반복합니다.",
        "do_while": "본문을 한 번 실행한 뒤 다시 반복할지 확인합니다.",
        "random_number": "게임, 테스트, 시뮬레이션에 사용할 예측하기 어려운 값을 생성합니다.",
        "for_loop": "인덱스나 시퀀스로 정해진 횟수만큼 반복합니다.",
        "nested_for": "반복문 안에 반복문을 넣어 격자, 표, 반복 패턴을 다룹니다.",
        "function_intro": "함수를 입력을 받고 출력을 반환하는 이름 있는 재사용 블록으로 이해합니다.",
        "create_function": "매개변수, 본문, 명확한 결과가 있는 직접 만든 함수를 작성합니다.",
        "call_function": "인수를 전달해 함수를 사용하고 반환값을 저장하거나 출력합니다.",
        "arrays_intro": "관련된 여러 값을 하나의 이름 아래 저장하고 위치나 순서로 요소에 접근합니다.",
        "array_kinds": "고정 배열, 동적 배열, 리스트, 벡터, 언어별 컬렉션 선택을 비교합니다.",
        "array_declare": "배열 같은 컬렉션을 만들고 시작 값을 채웁니다.",
        "strings": "텍스트를 표현하고 연결하며 문자나 부분 문자열을 검사합니다.",
        "char_arrays": "언어가 그 표현을 드러낼 때 텍스트를 문자들의 순서로 이해합니다.",
        "classes": "데이터와 동작을 이름 있는 타입으로 묶습니다.",
        "switch_statement": "정확히 일치하는 여러 경우 중 하나의 분기를 선택합니다.",
        "multi_arrays": "중첩 배열, 벡터, 리스트로 행과 열을 표현합니다.",
        "vectors": "요소 개수가 늘거나 줄 수 있을 때 크기 조절 가능한 시퀀스를 사용합니다.",
        "objects_classes": "클래스 정의에서 객체 값을 만들고 그 객체의 메서드를 호출합니다.",
        "recursion": "문제를 더 작은 같은 형태의 문제로 줄여 해결합니다.",
        "search_float": "컬렉션을 검색하고 측정값과 평균에는 부동소수점 값을 사용합니다.",
        "combined_if": "and, or, not으로 조건을 조합해 규칙을 명확하게 읽히게 합니다.",
        "nested_if": "한 결정이 이전 결정에 의존할 때 if 안에 if를 넣습니다.",
        "for_arrays": "for 반복문으로 배열 같은 컬렉션의 모든 요소를 처리합니다.",
        "nested_for_multi": "중첩 반복문으로 다차원 구조의 모든 칸을 방문합니다.",
        "while_validation": "값이 검증을 통과할 때까지 입력을 계속 요청합니다.",
        "do_while_menu": "메뉴를 최소 한 번 보여준 뒤 사용자가 중지를 선택할 때까지 계속합니다.",
        "default": "이전에 배운 기술을 작은 프로그램으로 결합합니다. 코드는 짧고 테스트 가능하며 줄별로 설명하기 쉽게 유지합니다.",
    },
    "fr": {
        "output": "Commencez par un comportement visible du programme. Afficher des valeurs donne une boucle de retour rapide pour tous les sujets suivants.",
        "input": "Lisez d'abord du texte, puis convertissez-le quand le programme a besoin d'un nombre, d'un booléen, d'un caractère, d'un décimal ou d'un tableau/liste.",
        "math": "Utilisez des expressions arithmétiques pour les totaux, moyennes, restes et calculs groupés.",
        "variable": "Associez un nom à une valeur et repérez dans la syntaxe le type, le nom, la valeur et l'initialisation.",
        "if_statement": "Utilisez une condition pour choisir si un bloc ou une expression doit s'exécuter.",
        "else_if": "Traitez plusieurs cas ordonnés sans écrire des if séparés sans lien.",
        "error_check": "Rejetez les entrées invalides avant que la logique principale en dépende.",
        "while_loop": "Répétez tant qu'une condition reste vraie, surtout quand le nombre exact de répétitions n'est pas connu.",
        "do_while": "Exécutez le corps une fois avant de vérifier si une autre itération est nécessaire.",
        "random_number": "Générez des valeurs imprévisibles pour les jeux, tests et simulations.",
        "for_loop": "Répétez un nombre connu de fois avec un index ou une séquence.",
        "nested_for": "Placez une boucle dans une autre pour travailler avec des grilles, tableaux et motifs répétés.",
        "function_intro": "Comprenez une fonction comme un bloc nommé et réutilisable qui accepte une entrée et renvoie une sortie.",
        "create_function": "Écrivez votre propre fonction avec des paramètres, un corps et un résultat clair.",
        "call_function": "Utilisez une fonction en passant des arguments, puis stockez ou affichez la valeur renvoyée.",
        "arrays_intro": "Stockez plusieurs valeurs liées sous un même nom et accédez aux éléments par position ou séquence.",
        "array_kinds": "Comparez tableaux fixes, tableaux dynamiques, listes, vecteurs et choix propres à chaque langage.",
        "array_declare": "Créez une collection de type tableau et remplissez-la avec des valeurs initiales.",
        "strings": "Représentez du texte, combinez du texte et inspectez des caractères ou sous-chaînes.",
        "char_arrays": "Comprenez le texte comme une séquence de caractères quand un langage expose cette représentation.",
        "classes": "Regroupez données et comportements dans un type nommé.",
        "switch_statement": "Choisissez une branche parmi plusieurs cas à correspondance exacte.",
        "multi_arrays": "Représentez lignes et colonnes avec des tableaux, vecteurs ou listes imbriqués.",
        "vectors": "Utilisez une séquence redimensionnable quand le nombre d'éléments peut changer.",
        "objects_classes": "Créez des objets à partir de définitions de classes et appelez leurs méthodes.",
        "recursion": "Résolvez un problème en le ramenant à une version plus petite de lui-même.",
        "search_float": "Recherchez dans des collections et utilisez des nombres flottants pour mesures et moyennes.",
        "combined_if": "Combinez les conditions avec and, or et not pour que les règles restent lisibles.",
        "nested_if": "Placez un if dans un autre quand une décision dépend d'une décision précédente.",
        "for_arrays": "Utilisez des boucles for pour traiter chaque élément d'une collection de type tableau.",
        "nested_for_multi": "Utilisez des boucles imbriquées pour visiter chaque cellule d'une structure multidimensionnelle.",
        "while_validation": "Redemandez l'entrée jusqu'à ce que la valeur passe la validation.",
        "do_while_menu": "Affichez un menu au moins une fois, puis continuez jusqu'à ce que l'utilisateur choisisse d'arrêter.",
        "default": "Combinez les compétences précédentes dans un petit programme. Gardez le code court, testable et facile à expliquer ligne par ligne.",
    },
}


LOCALIZED_INPUT_DETAILS = {
    "zh": {
        "cpp": "C++ 使用 `std::cin >> variable` 读取简单输入。变量类型决定文本如何解释：`int` 读取整数，`double` 读取小数，启用 `std::boolalpha` 时 `bool` 读取 `true` 或 `false`，`char` 读取一个字符，`std::string` 读取一个单词。数组或 vector 输入通常一次读取一个元素，例如 `scores[0]`、`scores[1]`、`scores[2]`。输出带变量的句子时，用 `<<` 串接文本和值。注意：`std::cin >> name` 会在空白处停止；以后需要整句时再用 `std::getline`。",
        "python": "Python 的 `input()` 总是返回字符串。需要时再转换：整数用 `int(input(...))`，小数用 `float(input(...))`，布尔值可用 `input(...).lower() == \"true\"`，字符可用 `input(...)[0]`，数字列表可用 `[int(x) for x in input(...).split()]`。输出带变量的句子时，f-string 通常最清晰，例如 `f\"{name} is {age}\"`。注意：无效数字文本会导致转换错误，空字符串上使用 `[0]` 会失败。",
        "c": "C 使用 `scanf` 和格式说明符。`%d` 读取整数，`%lf` 读取 double，`%c` 读取一个字符，`%s` 读取一个单词到字符数组，数组元素通常用 `&scores[0]` 这样的地址逐个读取。C 没有适合初学者的内置布尔输入，所以可用 `int member`，1 表示 true，0 表示 false。输出带变量的句子时，使用匹配的 `printf` 占位符。注意：除字符数组外，多数 `scanf` 目标需要 `&`，而 `scanf(\" %c\", &initial)` 前面的空格用于跳过旧空白。",
        "java": "Java 常用 `Scanner`。整数用 `nextInt()`，小数用 `nextDouble()`，布尔值用 `nextBoolean()`，一个字符用 `next().charAt(0)`，一个单词字符串用 `next()`，数组元素用 `int[] scores` 加多次 `nextInt()` 读取。输出带变量的句子时，用 `+` 连接文本和值，或使用 `System.out.printf`。注意：以后混用 `nextLine()` 和 `nextInt()` 时，残留换行可能被意外读取。",
        "r": "R 初学输入常用 `readline()`，它返回文本。整数用 `as.integer(...)`，小数用 `as.numeric(...)`，布尔值可用 `tolower(...) == \"true\"`，一个字符可用 `substr(text, 1, 1)`，整数向量可用 `scan(text = readline(), what = integer(), quiet = TRUE)`。输出带变量的句子时，用 `cat(sprintf(...))` 或 `paste(...)`。注意：R 的向量从 1 开始索引，所以第一个元素是 `scores[1]`，不是 `scores[0]`。",
    },
    "ja": {
        "cpp": "C++ は単純な入力に `std::cin >> variable` を使います。変数の型がテキストの解釈を決めます。`int` は整数、`double` は小数、`std::boolalpha` を使うと `bool` は `true` または `false`、`char` は 1 文字、`std::string` は 1 単語を読みます。配列や vector の入力は `scores[0]`、`scores[1]`、`scores[2]` のように 1 要素ずつ読みます。変数を含む文を出力するときは、`<<` でテキストと値をつなぎます。注意: `std::cin >> name` は空白で止まります。文全体が必要なときは後で `std::getline` を使います。",
        "python": "Python の `input()` は常に文字列を返します。必要に応じて変換します。整数は `int(input(...))`、小数は `float(input(...))`、真偽値は `input(...).lower() == \"true\"`、文字は `input(...)[0]`、数値リストは `[int(x) for x in input(...).split()]` です。変数を含む文の出力には f-string が分かりやすく、例は `f\"{name} is {age}\"` です。注意: 数値でない文字列は変換エラーになり、空文字列で `[0]` を使うと失敗します。",
        "c": "C は `scanf` と書式指定子を使います。`%d` は整数、`%lf` は double、`%c` は 1 文字、`%s` は文字配列に 1 単語を読み、配列は `&scores[0]` のようなアドレスで 1 要素ずつ読みます。C には初心者向けの組み込み真偽値入力がないので、`int member` を使い、1 を true、0 を false とします。変数を含む文は対応する `printf` プレースホルダーで出力します。注意: 文字配列以外の多くの `scanf` 先には `&` が必要で、`scanf(\" %c\", &initial)` の先頭空白は古い空白を飛ばします。",
        "java": "Java ではよく `Scanner` を使います。整数は `nextInt()`、小数は `nextDouble()`、真偽値は `nextBoolean()`、1 文字は `next().charAt(0)`、1 単語の文字列は `next()`、配列要素は `int[] scores` に対して複数回 `nextInt()` で読みます。変数を含む文は `+` で連結するか、`System.out.printf` を使います。注意: 後で `nextLine()` と `nextInt()` を混ぜると、残った改行が意図せず読まれることがあります。",
        "r": "R の初学者向け入力では `readline()` をよく使い、これはテキストを返します。整数は `as.integer(...)`、小数は `as.numeric(...)`、真偽値は `tolower(...) == \"true\"`、1 文字は `substr(text, 1, 1)`、整数ベクターは `scan(text = readline(), what = integer(), quiet = TRUE)` に変換します。変数を含む文は `cat(sprintf(...))` または `paste(...)` で出力します。注意: R のベクターは 1 始まりなので、最初の要素は `scores[1]` であり `scores[0]` ではありません。",
    },
    "ko": {
        "cpp": "C++는 간단한 입력에 `std::cin >> variable`을 사용합니다. 변수 타입이 텍스트 해석 방식을 결정합니다. `int`는 정수, `double`은 소수, `std::boolalpha`를 사용한 `bool`은 `true` 또는 `false`, `char`는 한 문자, `std::string`은 한 단어를 읽습니다. 배열/vector 입력은 `scores[0]`, `scores[1]`, `scores[2]`처럼 한 요소씩 읽습니다. 변수가 포함된 문장을 출력할 때는 `<<`로 텍스트와 값을 연결합니다. 주의: `std::cin >> name`은 공백에서 멈추므로, 전체 문장이 필요할 때는 나중에 `std::getline`을 사용합니다.",
        "python": "Python의 `input()`은 항상 문자열을 반환합니다. 필요할 때 변환합니다. 정수는 `int(input(...))`, 소수는 `float(input(...))`, 불리언은 `input(...).lower() == \"true\"`, 문자는 `input(...)[0]`, 숫자 리스트는 `[int(x) for x in input(...).split()]`를 사용합니다. 변수가 포함된 문장을 출력할 때는 f-string이 가장 명확하며 예시는 `f\"{name} is {age}\"`입니다. 주의: 잘못된 숫자 텍스트는 변환 오류를 만들고, 빈 문자열에서 `[0]`은 실패합니다.",
        "c": "C는 `scanf`와 형식 지정자를 사용합니다. `%d`는 정수, `%lf`는 double, `%c`는 한 문자, `%s`는 문자 배열에 한 단어를 읽고, 배열은 `&scores[0]` 같은 주소로 한 요소씩 읽습니다. C에는 초보자에게 쉬운 내장 불리언 입력이 없으므로 `int member`를 사용해 1은 true, 0은 false로 둡니다. 변수가 포함된 문장은 맞는 `printf` 자리표시자로 출력합니다. 주의: 문자 배열을 제외한 대부분의 `scanf` 대상에는 `&`가 필요하고, `scanf(\" %c\", &initial)`의 앞 공백은 이전 공백을 건너뜁니다.",
        "java": "Java는 보통 `Scanner`를 사용합니다. 정수는 `nextInt()`, 소수는 `nextDouble()`, 불리언은 `nextBoolean()`, 한 문자는 `next().charAt(0)`, 한 단어 문자열은 `next()`, 배열 요소는 `int[] scores`와 여러 번의 `nextInt()`로 읽습니다. 변수가 포함된 문장은 `+`로 연결하거나 `System.out.printf`를 사용합니다. 주의: 나중에 `nextLine()`과 `nextInt()`를 섞으면 남은 줄바꿈이 실수로 읽힐 수 있습니다.",
        "r": "R은 초보자 입력에 `readline()`을 자주 사용하며, 이것은 텍스트를 반환합니다. 정수는 `as.integer(...)`, 소수는 `as.numeric(...)`, 불리언은 `tolower(...) == \"true\"`, 한 문자는 `substr(text, 1, 1)`, 정수 벡터는 `scan(text = readline(), what = integer(), quiet = TRUE)`로 변환합니다. 변수가 포함된 문장은 `cat(sprintf(...))` 또는 `paste(...)`로 출력합니다. 주의: R 벡터는 1부터 인덱싱하므로 첫 항목은 `scores[1]`이지 `scores[0]`이 아닙니다.",
    },
    "fr": {
        "cpp": "C++ utilise `std::cin >> variable` pour les entrées simples. Le type de la variable détermine comment le texte est interprété : `int` lit un entier, `double` lit un décimal, `bool` lit `true` ou `false` avec `std::boolalpha`, `char` lit un caractère et `std::string` lit un mot. Pour un tableau/vector, lisez un élément à la fois, par exemple `scores[0]`, `scores[1]` et `scores[2]`. Pour afficher une phrase avec des variables, enchaînez texte et valeurs avec `<<`. Attention : `std::cin >> name` s'arrête aux espaces ; utilisez plus tard `std::getline` quand vous aurez besoin d'une phrase complète.",
        "python": "En Python, `input()` renvoie toujours une chaîne. Convertissez-la au besoin : `int(input(...))` pour les entiers, `float(input(...))` pour les décimaux, `input(...).lower() == \"true\"` pour un booléen, `input(...)[0]` pour un caractère et `[int(x) for x in input(...).split()]` pour une liste de nombres. Pour afficher une phrase avec des variables, une f-string est souvent la plus claire, par exemple `f\"{name} is {age}\"`. Attention : un texte numérique invalide provoque une erreur de conversion, et `[0]` échoue sur une chaîne vide.",
        "c": "C utilise `scanf` avec des spécificateurs de format. `%d` lit un entier, `%lf` lit un double, `%c` lit un caractère, `%s` lit un mot dans un tableau de caractères, et les tableaux se lisent élément par élément avec des adresses comme `&scores[0]`. C n'a pas d'entrée booléenne simple pour débutants, donc utilisez `int member` avec 1 pour true et 0 pour false. Pour afficher une phrase avec des variables, utilisez les bons espaces réservés `printf`. Attention : presque toutes les cibles `scanf`, sauf les tableaux de caractères, ont besoin de `&`, et `scanf(\" %c\", &initial)` utilise l'espace initial pour ignorer les anciens espaces.",
        "java": "Java utilise souvent `Scanner`. Utilisez `nextInt()` pour les entiers, `nextDouble()` pour les décimaux, `nextBoolean()` pour les booléens, `next().charAt(0)` pour un caractère, `next()` pour un mot, et `int[] scores` avec plusieurs appels `nextInt()` pour les éléments de tableau. Pour afficher une phrase avec des variables, joignez texte et valeurs avec `+` ou utilisez `System.out.printf`. Attention en mélangeant plus tard `nextLine()` avec `nextInt()` : les retours à la ligne restants peuvent être lus par accident.",
        "r": "R lit souvent les entrées débutantes avec `readline()`, qui renvoie du texte. Convertissez avec `as.integer(...)` pour les entiers, `as.numeric(...)` pour les décimaux, `tolower(...) == \"true\"` pour les booléens, `substr(text, 1, 1)` pour un caractère et `scan(text = readline(), what = integer(), quiet = TRUE)` pour un vecteur d'entiers. Pour afficher une phrase avec des variables, utilisez `cat(sprintf(...))` ou `paste(...)`. Attention : les vecteurs R sont indexés à partir de 1, donc le premier élément est `scores[1]`, pas `scores[0]`.",
    },
}


LOCALIZED_RACKET_DETAILS = {
    "zh": {
        "output": "`displayln` 是初学 Racket 程序最常用的输出函数。`display` 表示显示一个值，`ln` 表示输出后换行。`(displayln 42)` 的意思是：调用 `displayln`，把数字 `42` 作为参数，打印 `42`，然后移动到下一行。括号是必须的，因为 Racket 使用前缀表达式语法：`(` 后面的第一项是函数或操作，后面的项是参数。这取代了 C++ 中 `std::cout << 42 << std::endl;` 的习惯。`#lang racket` 也必须放在文件顶部，因为它告诉 Racket 用哪套语言规则读取文件。",
        "input": "Racket 详情：`display` 打印提示但不换行，`read-line` 等待用户输入文本并按 Enter。`(define name (read-line))` 会运行 `read-line`，然后把输入文本绑定到 `name`。数字通常先读文本，再用 `string->number` 转换。布尔值可以比较输入文本，例如 `(equal? answer \"true\")`。字符可以先读字符串，再用 `string-ref` 取第一个字符。数组类输入可以读一整行，用 `string-split` 切开，再用 `map string->number` 转换。注意：`read-line` 返回字符串，`string->number` 在坏输入时可能返回 `#f`，空字符串上使用 `string-ref` 会失败。",
        "math": "Racket 用前缀形式写算术：`(+ subtotal tax)` 表示 `subtotal + tax`。运算符放在前面，然后是数字或名字。括号是必须的，因为它们标记了准确的表达式和参数。",
        "variable": "`define` 把名字绑定到值。对初学者来说，可以把 `(define count 3)` 读成 C++ 里的 `const auto count = 3;`。Racket 通常构造新值，而不是反复修改同一个变量。",
        "default": "Racket 程序由表达式组成。在带括号的表达式中，第一项决定动作，后面的项是这个动作的输入。读每一行时先问：最前面的函数或特殊形式是什么，传入了哪些值，会产生什么结果或效果？",
    },
    "ja": {
        "output": "`displayln` は初心者向け Racket プログラムの基本的な出力関数です。`display` は値を表示すること、`ln` はその後に改行することを意味します。`(displayln 42)` は、数値 `42` を引数として `displayln` を呼び出し、`42` を出力して次の行へ移るという意味です。Racket は前置式の構文を使うため、括弧が必要です。`(` の直後の最初の項目が関数または操作で、続く項目が引数です。これは C++ の `std::cout << 42 << std::endl;` という習慣を置き換えます。`#lang racket` もファイル先頭に必要で、Racket にどの言語規則でファイルを読むかを伝えます。",
        "input": "Racket の詳細: `display` は改行せずにプロンプトを表示し、`read-line` はユーザーがテキストを入力して Enter を押すのを待ちます。`(define name (read-line))` は `read-line` を実行し、入力されたテキストを `name` に結び付けます。数値は通常、まずテキストとして読み、`string->number` で変換します。真偽値は `(equal? answer \"true\")` のように入力テキストを比較できます。文字は文字列を読んで `string-ref` で最初の文字を取ります。配列のような入力は 1 行を読み、`string-split` で分割し、`map string->number` で変換します。注意: `read-line` は文字列を返し、`string->number` は不正入力で `#f` を返すことがあり、空文字列で `string-ref` を使うと失敗します。",
        "math": "Racket は算術を前置形式で書きます。`(+ subtotal tax)` は `subtotal + tax` を意味します。演算子が先に来て、その後に数値や名前が続きます。括弧は式と引数の範囲を正確に示すため必須です。",
        "variable": "`define` は名前を値に結び付けます。初心者は `(define count 3)` を C++ の `const auto count = 3;` のように読むと分かりやすいです。Racket は同じ変数を何度も変更するより、新しい値を作ることが多いです。",
        "default": "Racket プログラムは式で構成されます。括弧付きの式では、最初の項目が動作を決め、残りの項目がその動作への入力です。各行を読むときは、最初の関数または特殊形式は何か、どの値が渡されるか、どんな結果や効果が起きるかを確認します。",
    },
    "ko": {
        "output": "`displayln`은 초보 Racket 프로그램의 기본 출력 함수입니다. `display`는 값을 보여 준다는 뜻이고, `ln`은 출력 뒤에 줄바꿈을 추가한다는 뜻입니다. `(displayln 42)`는 숫자 `42`를 인수로 `displayln`을 호출해 `42`를 출력하고 다음 줄로 이동한다는 의미입니다. Racket은 전위 표현식 문법을 사용하므로 괄호가 필요합니다. `(` 바로 뒤의 첫 항목이 함수나 연산이고, 뒤따르는 항목들이 인수입니다. 이는 C++의 `std::cout << 42 << std::endl;` 습관을 대체합니다. `#lang racket`도 파일 맨 위에 필요하며, Racket에게 어떤 언어 규칙으로 파일을 읽을지 알려 줍니다.",
        "input": "Racket 세부사항: `display`는 줄바꿈 없이 프롬프트를 출력하고, `read-line`은 사용자가 텍스트를 입력하고 Enter를 누를 때까지 기다립니다. `(define name (read-line))`은 `read-line`을 실행한 뒤 입력 텍스트를 `name`에 바인딩합니다. 숫자는 보통 먼저 텍스트로 읽고 `string->number`로 변환합니다. 불리언은 `(equal? answer \"true\")`처럼 입력 텍스트를 비교할 수 있습니다. 문자는 문자열을 읽고 `string-ref`로 첫 문자를 가져옵니다. 배열 같은 입력은 한 줄을 읽고 `string-split`으로 나눈 뒤 `map string->number`로 변환합니다. 주의: `read-line`은 문자열을 반환하고, `string->number`는 잘못된 입력에서 `#f`를 반환할 수 있으며, 빈 문자열에서 `string-ref`는 실패합니다.",
        "math": "Racket은 산술을 전위 형태로 씁니다. `(+ subtotal tax)`는 `subtotal + tax`를 의미합니다. 연산자가 먼저 오고 그 뒤에 숫자나 이름이 옵니다. 괄호는 정확한 표현식과 인수 범위를 표시하므로 필수입니다.",
        "variable": "`define`은 이름을 값에 연결합니다. 초보자는 `(define count 3)`을 C++의 `const auto count = 3;`처럼 읽으면 좋습니다. Racket은 같은 변수를 반복해서 바꾸기보다 새 값을 만드는 경우가 많습니다.",
        "default": "Racket 프로그램은 표현식으로 만들어집니다. 괄호가 있는 표현식에서는 첫 항목이 동작을 결정하고 나머지 항목은 그 동작의 입력입니다. 각 줄을 읽을 때는 첫 함수나 특수 형식이 무엇인지, 어떤 값이 전달되는지, 어떤 결과나 효과가 생기는지 확인합니다.",
    },
    "fr": {
        "output": "`displayln` est la fonction de sortie de base pour les programmes Racket débutants. `display` signifie afficher une valeur, et `ln` ajoute un retour à la ligne après. `(displayln 42)` signifie : appeler `displayln` avec la valeur numérique `42`, afficher `42`, puis passer à la ligne suivante. Les parenthèses sont obligatoires parce que Racket utilise une syntaxe préfixe : le premier élément après `(` est la fonction ou l'opération, et les éléments suivants sont les arguments. Cela remplace l'habitude C++ `std::cout << 42 << std::endl;`. `#lang racket` est aussi requis en haut du fichier, car il indique à Racket quelles règles de langage utiliser pour lire le fichier.",
        "input": "Détail Racket : `display` affiche une invite sans passer à la ligne. `read-line` attend que l'utilisateur saisisse du texte puis appuie sur Entrée. `(define name (read-line))` exécute `read-line`, puis associe le texte saisi à `name`. Pour les nombres, Racket lit souvent du texte puis le convertit avec `string->number`. Pour un booléen, comparez le texte saisi, par exemple `(equal? answer \"true\")`. Pour un caractère, lisez une chaîne puis prenez le premier caractère avec `string-ref`. Pour une entrée de type tableau, lisez une ligne, découpez-la avec `string-split`, puis convertissez chaque élément avec `map string->number`. Attention : `read-line` donne une chaîne, `string->number` peut renvoyer `#f` pour une mauvaise entrée, et `string-ref` échoue sur une chaîne vide.",
        "math": "Racket écrit l'arithmétique en forme préfixe : `(+ subtotal tax)` signifie `subtotal + tax`. L'opérateur vient d'abord, puis les nombres ou les noms. Les parenthèses sont obligatoires car elles délimitent exactement l'expression et ses arguments.",
        "variable": "`define` associe un nom à une valeur. Pour débuter, lisez `(define count 3)` comme `const auto count = 3;` en C++. Racket construit souvent de nouvelles valeurs au lieu de modifier plusieurs fois la même variable.",
        "default": "Les programmes Racket sont construits avec des expressions. Dans une expression entre parenthèses, le premier élément décide de l'action et les autres éléments sont les entrées de cette action. Pour lire chaque ligne, demandez-vous quelle fonction ou forme spéciale vient d'abord, quelles valeurs sont passées et quel résultat ou effet se produit.",
    },
}


LOCALIZED_EXPLANATION_TEMPLATES = {
    "zh": {
        "foundation": "{summary} 这个预备课程先教 {base_language} 版本。重点关注每一行做什么、语法边界在哪里，以及编译器如何读取程序。这个基础熟练后，其他语言课程就可以直接和它对比。{extra}",
        "racket": "{summary} 先从 {base_language} 代码片段出发，再把 Racket 代码读成表达式，而不是 C++ 语句。{detail} 之后，把每一行 Racket 和最接近的 {base_language} 行对比，这样语法会形成连接，而不是死记硬背。",
        "target": "{summary} 在本课中，先阅读 {base_language} 片段并说出它表达的准确思想。然后逐行学习 {language} 代码。解释保持简短：这一行做什么、用了什么语法、对应或替代了哪个 {base_language} 习惯。{extra}",
        "r_stats": "{summary} 这是 56 天编程核心之后的 R 统计扩展。重点练习完整分析习惯：检查数据，选择统计量或图表，运行 R 函数，然后用清楚的中文解释结果。",
    },
    "ja": {
        "foundation": "{summary} この前提トラックでは、まず {base_language} 版を学びます。各行が何をするか、構文の境界がどこか、コンパイラがプログラムをどう読むかに集中してください。この基礎に慣れると、他の言語トラックを直接比較できます。{extra}",
        "racket": "{summary} まず {base_language} のスニペットから始め、Racket のコードを C++ の文ではなく式として読みます。{detail} その後、各 Racket 行を最も近い {base_language} 行と比べることで、構文を丸暗記ではなく関連付けて理解できます。",
        "target": "{summary} このレッスンでは、まず {base_language} のスニペットを読み、その正確な考え方に名前を付けます。次に {language} のコードを 1 行ずつ学びます。説明は短く保ち、この行が何をするか、どの構文を使うか、どの {base_language} の習慣に対応または置き換わるかを確認します。{extra}",
        "r_stats": "{summary} これは 56 日間のプログラミング基礎の後に続く R 統計拡張です。データを確認し、統計量やグラフを選び、R 関数を実行し、結果を分かりやすい日本語で説明するという分析の流れに集中します。",
    },
    "ko": {
        "foundation": "{summary} 이 선수 트랙은 먼저 {base_language} 버전을 가르칩니다. 각 줄이 무엇을 하는지, 문법 경계가 어디인지, 컴파일러가 프로그램을 어떻게 읽는지에 집중하세요. 이 기초가 편해지면 다른 언어 트랙을 직접 비교할 수 있습니다.{extra}",
        "racket": "{summary} 먼저 {base_language} 코드 조각에서 시작한 뒤, Racket 코드를 C++ 문장이 아니라 표현식으로 읽습니다. {detail} 그런 다음 각 Racket 줄을 가장 가까운 {base_language} 줄과 비교하면 문법을 암기하는 대신 연결해서 이해할 수 있습니다.",
        "target": "{summary} 이 수업에서는 먼저 {base_language} 코드 조각을 읽고 정확한 아이디어에 이름을 붙입니다. 그런 다음 {language} 코드를 한 줄씩 공부합니다. 설명은 짧게 유지하세요. 그 줄이 무엇을 하는지, 어떤 문법을 쓰는지, 어떤 {base_language} 습관과 대응되거나 대체되는지 확인합니다.{extra}",
        "r_stats": "{summary} 이것은 56일 프로그래밍 핵심 과정 뒤의 R 통계 확장입니다. 데이터를 점검하고, 통계량이나 그래프를 선택하고, R 함수를 실행한 뒤, 결과를 쉬운 한국어로 설명하는 전체 분석 습관에 집중하세요.",
    },
    "fr": {
        "foundation": "{summary} Ce parcours préalable enseigne d'abord la version {base_language}. Concentrez-vous sur ce que fait chaque ligne, où se trouvent les limites syntaxiques et comment le compilateur lit le programme. Une fois cette base confortable, les autres parcours de langue peuvent s'y comparer directement. {extra}",
        "racket": "{summary} Partez d'abord de l'extrait {base_language}, puis lisez le code Racket comme des expressions plutôt que comme des instructions C++. {detail} Ensuite, comparez chaque ligne Racket avec la ligne {base_language} la plus proche afin que la syntaxe soit reliée à ce que vous connaissez, pas simplement mémorisée.",
        "target": "{summary} Dans cette leçon, lisez d'abord l'extrait {base_language} et nommez l'idée exacte. Étudiez ensuite le code {language} ligne par ligne. Gardez l'explication courte : ce que fait la ligne, quelle syntaxe elle utilise et quelle habitude {base_language} elle reprend ou remplace. {extra}",
        "r_stats": "{summary} Cette leçon fait partie de l'extension statistique R après le noyau de programmation de 56 jours. Concentrez-vous sur l'habitude complète d'analyse : inspecter les données, choisir la statistique ou le graphique, lancer la fonction R, puis expliquer le résultat en français clair.",
    },
}


LOCALIZED_R_STATS_SUMMARIES = {
    "zh": {
        "r_data_frame": "先把观测放进行，把变量放进列，用数据框开始统计分析，并在计算前检查数据。",
        "r_missing_types": "真实统计数据经常有缺失值和错误类型；在计算均值、检验或模型前先清理它们。",
        "r_descriptive_stats": "描述性统计先用中心、离散程度和范围概括一个变量，再进入正式推断。",
        "r_grouped_summary": "统计常常比较不同组；先用分组汇总和列联表观察模式，再做正式检验。",
        "r_graphics": "统计图帮助你在正式检验前看清分布、异常值和组间差异。",
        "r_distribution_sim": "概率分布和模拟可以用随机样本展示不确定性和长期模式。",
        "r_confidence_interval": "置信区间用样本估计总体值，并表达估计的不确定性。",
        "r_t_test": "t 检验比较均值，并判断观察到的差异是否可能来自随机波动。",
        "r_regression": "相关和线性回归描述两个数值变量之间的关系。",
        "r_chi_square_report": "卡方检验用计数表检查两个分类变量是否有关联。",
    },
    "ja": {
        "r_data_frame": "観測を行に、変数を列に置き、計算前にデータを確認することから統計分析を始めます。",
        "r_missing_types": "実際の統計データには欠損値や誤った型がよくあるため、平均、検定、モデルの前に整理します。",
        "r_descriptive_stats": "記述統計は、正式な推測の前に中心、ばらつき、範囲で 1 つの変数を要約します。",
        "r_grouped_summary": "統計ではグループ比較が多いため、正式な検定の前にグループ集計や表で傾向を確認します。",
        "r_graphics": "統計グラフは、正式な検定の前に分布、外れ値、グループ差を見つける助けになります。",
        "r_distribution_sim": "確率分布とシミュレーションは、ランダムサンプルで不確実性と長期的なパターンを示します。",
        "r_confidence_interval": "信頼区間は標本から母集団の値を推定し、その不確実性を表します。",
        "r_t_test": "t 検定は平均を比較し、観察された差が偶然の変動で説明できるかを調べます。",
        "r_regression": "相関と線形回帰は、2 つの数値変数の関係を説明します。",
        "r_chi_square_report": "カイ二乗検定は、度数表を使って 2 つのカテゴリ変数に関連があるかを調べます。",
    },
    "ko": {
        "r_data_frame": "관측값은 행에, 변수는 열에 두고 계산 전에 데이터를 점검하며 데이터 프레임으로 통계 분석을 시작합니다.",
        "r_missing_types": "실제 통계 데이터에는 결측값과 잘못된 타입이 자주 있으므로 평균, 검정, 모델 계산 전에 정리합니다.",
        "r_descriptive_stats": "기술통계는 공식 추론 전에 중심, 퍼짐, 범위로 한 변수를 요약합니다.",
        "r_grouped_summary": "통계는 집단 비교가 많으므로 공식 검정 전에 그룹 요약과 표로 패턴을 확인합니다.",
        "r_graphics": "통계 그래프는 공식 검정 전에 분포, 이상값, 집단 차이를 보는 데 도움이 됩니다.",
        "r_distribution_sim": "확률분포와 시뮬레이션은 무작위 표본으로 불확실성과 장기 패턴을 보여 줍니다.",
        "r_confidence_interval": "신뢰구간은 표본으로 모집단 값을 추정하고 그 불확실성을 표현합니다.",
        "r_t_test": "t 검정은 평균을 비교하고 관찰된 차이가 무작위 변동으로 설명될 수 있는지 판단합니다.",
        "r_regression": "상관과 선형회귀는 두 수치 변수 사이의 관계를 설명합니다.",
        "r_chi_square_report": "카이제곱 검정은 빈도표를 사용해 두 범주형 변수가 관련되는지 확인합니다.",
    },
    "fr": {
        "r_data_frame": "Commencez l'analyse statistique avec des data frames : observations en lignes, variables en colonnes, puis inspection avant tout calcul.",
        "r_missing_types": "Les vraies données statistiques contiennent souvent des valeurs manquantes et des types incorrects ; nettoyez-les avant les moyennes, tests ou modèles.",
        "r_descriptive_stats": "Les statistiques descriptives résument une variable par le centre, la dispersion et l'étendue avant toute inférence formelle.",
        "r_grouped_summary": "La statistique compare souvent des groupes ; utilisez d'abord des résumés groupés et des tableaux pour repérer les motifs.",
        "r_graphics": "Les graphiques statistiques aident à voir distributions, valeurs atypiques et différences entre groupes avant les tests formels.",
        "r_distribution_sim": "Les distributions de probabilité et les simulations montrent l'incertitude et les tendances à long terme avec des échantillons aléatoires.",
        "r_confidence_interval": "Un intervalle de confiance estime une valeur de population à partir d'un échantillon et exprime l'incertitude.",
        "r_t_test": "Un test t compare des moyennes et évalue si une différence observée peut venir de la variation aléatoire.",
        "r_regression": "La corrélation et la régression linéaire décrivent la relation entre deux variables numériques.",
        "r_chi_square_report": "Le test du chi carré utilise un tableau de comptes pour vérifier si deux variables catégorielles sont liées.",
    },
}


def _localized_summary(kind: str, ui_language: str = "en") -> str:
    language = normalize_ui_language(ui_language)
    if language == "en":
        return _summary(kind)
    summaries = LOCALIZED_KIND_SUMMARIES.get(language, {})
    base_kind = _base_kind(kind)
    return summaries.get(kind) or summaries.get(base_kind) or summaries.get("default") or _summary(kind)


def _localized_input_detail(target: str, ui_language: str = "en") -> str:
    language = normalize_ui_language(ui_language)
    if language == "en":
        return INPUT_TYPE_DETAILS.get(target, "")
    return LOCALIZED_INPUT_DETAILS.get(language, {}).get(target, INPUT_TYPE_DETAILS.get(target, ""))


def _localized_racket_detail(base_kind: str, ui_language: str = "en") -> str:
    language = normalize_ui_language(ui_language)
    if language == "en":
        return RACKET_KIND_DETAILS.get(
            base_kind,
            "Racket programs are built from expressions. In a parenthesized expression, the first item decides the action and the remaining items are inputs to that action. "
            "Read each line by asking: what function or special form is first, what values are passed in, and what result or effect happens?"
        )
    details = LOCALIZED_RACKET_DETAILS.get(language, {})
    return details.get(base_kind) or details.get("default") or _localized_racket_detail(base_kind, "en")


def _code(kind: str, target: str) -> str:
    return SNIPPETS[_base_kind(kind)][target]


def _cpp(kind: str) -> str:
    return SNIPPETS[_base_kind(kind)]["cpp"]


def get_course_length(target_language: str | None = None) -> int:
    target = normalize_target_language(target_language)
    return len(TOPICS) + len(R_STATISTICS_TOPICS) if target == "r" else len(TOPICS)


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
        elif target == "r":
            result["output"] = "Name: Age integer: Price decimal: Member true/false: Initial character: Three integer scores:\nCode is 16 years old. Price: 19.50. Member: TRUE. Initial: A. First score: 88"
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


def _explanation(title: str, kind: str, target: str, base: str = "cpp", ui_language: str = "en") -> str:
    ui_language = normalize_ui_language(ui_language)
    language = TARGET_LANGUAGES[target]["name"]
    base_language = TARGET_LANGUAGES[base]["name"]
    base_kind = _base_kind(kind)
    if ui_language != "en":
        templates = LOCALIZED_EXPLANATION_TEMPLATES[ui_language]
        summary = _localized_summary(kind, ui_language)
        if target == base:
            extra = f" {_localized_input_detail(target, ui_language)}" if base_kind == "input" else ""
            return templates["foundation"].format(summary=summary, base_language=base_language, extra=extra).strip()
        if target == "racket":
            detail = _localized_racket_detail(base_kind, ui_language)
            return templates["racket"].format(summary=summary, base_language=base_language, detail=detail).strip()
        extra = _localized_input_detail(target, ui_language) if base_kind == "input" else ""
        return templates["target"].format(
            summary=summary,
            base_language=base_language,
            language=language,
            extra=extra,
        ).strip()

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


def _r_statistics_topic(kind: str) -> dict:
    for topic in R_STATISTICS_TOPICS:
        if topic["kind"] == kind:
            return topic
    raise KeyError(kind)


def _statistics_base_code(base: str, kind: str) -> str:
    examples = {
        "cpp": """std::vector<double> scores = {78, 84, 73, 92, 81};
double total = 0;
for (double score : scores) total += score;
double mean = total / scores.size();""",
        "c": """double scores[] = {78, 84, 73, 92, 81};
double total = 0;
for (int i = 0; i < 5; i++) total += scores[i];
double mean = total / 5;""",
        "java": """double[] scores = {78, 84, 73, 92, 81};
double total = 0;
for (double score : scores) total += score;
double mean = total / scores.length;""",
        "python": """scores = [78, 84, 73, 92, 81]
mean_score = sum(scores) / len(scores)
print(mean_score)""",
        "racket": """#lang racket

(define scores '(78 84 73 92 81))
(define mean-score (/ (apply + scores) (length scores)))
(displayln mean-score)""",
        "r": """scores <- c(78, 84, 73, 92, 81)
mean_score <- mean(scores)
cat(mean_score, "\\n")""",
    }
    return examples.get(base, examples["cpp"])


def _r_statistics_bridge(day: int, topic: dict, base: str) -> dict:
    base_language = TARGET_LANGUAGES[base]["name"]
    base_code = _statistics_base_code(base, topic["kind"])
    docs = DOCS["r"] + [
        {"title": "R Data Import/Export", "url": "https://cran.r-project.org/doc/manuals/r-release/R-data.html"},
        {"title": "R stats Package Index", "url": "https://stat.ethz.ch/R-manual/R-devel/library/stats/html/00Index.html"},
    ]
    return {
        "concept": topic["concept"],
        "cpp": base_code,
        "base": base_code,
        "base_label": base_language,
        "base_io": {
            "input": "",
            "output": "Known-language baseline: store values, loop or call helpers, then print a statistic.",
        },
        "racket": topic["code"],
        "target": topic["code"],
        "target_label": "R",
        "target_io": {"input": "", "output": topic["output"]},
        "translation_steps": topic["translation"],
        "pitfalls": topic["pitfalls"],
        "drill": f"Run the R sample, then write a two-sentence statistics interpretation for Day {day:02d}.",
        "today_angle": f"Statistics application: {topic['summary']}",
        "docs": docs,
    }


def _r_statistics_homework_prompts(kind: str) -> list[str]:
    prompts = {
        "r_data_frame": [
            "Create a data frame `sleep_study` with students A-F, sleep hours 6, 7, 5, 8, 6, 9, and quiz scores 72, 80, 68, 88, 75, 91. Print row count, column count, first 4 rows, and `str(sleep_study)`.",
            "Create a data frame `survey` with columns group = Control/Treatment and response = 12, 14, 13, 19, 21, 18. Print the full data frame and explain which column is categorical and which is numeric.",
            "Create a data frame `library_use` with visit counts 2, 4, 1, 5, 3 and final marks 70, 82, 65, 90, 78. Print `summary(library_use)` and one sentence describing the highest mark.",
        ],
        "r_missing_types": [
            "Create a data frame with heights 160, NA, 172, 168, NA and weights 55, 61, NA, 64, 70. Use `is.na` and `colSums` to print missing counts for each column.",
            "Create a vector `raw_scores <- c('78', '84', 'missing', '91')`. Convert valid numeric entries to numbers, mark the bad entry as `NA`, and print the cleaned vector.",
            "Create a data frame with 6 rows and at least two `NA` values. Use `na.omit`, then print before/after row counts and explain how many rows were removed.",
        ],
        "r_descriptive_stats": [
            "Use scores 64, 72, 75, 81, 85, 90, 94. Calculate mean, median, standard deviation, min, max, and range. Print each with a label.",
            "Use commute times 12, 18, 25, 40, 15, 22, 30. Calculate the five-number summary with `summary`, then print one sentence about spread.",
            "Use prices 4.50, 5.25, 6.00, 7.75, 9.10. Calculate average price and sample standard deviation, formatted to two decimals.",
        ],
        "r_grouped_summary": [
            "Create a data frame with classes A/A/A/B/B/B and scores 78, 84, 90, 74, 79, 85. Use `aggregate` to print mean score by class.",
            "Create a data frame with gender labels F, M, F, M, F, M and club TRUE/FALSE values TRUE, TRUE, FALSE, FALSE, TRUE, FALSE. Use `table` to count gender by club.",
            "Create a data frame with treatment Low/Low/High/High and recovery days 8, 7, 5, 6. Print grouped mean and grouped standard deviation.",
        ],
        "r_graphics": [
            "Create scores 55, 61, 70, 72, 80, 85, 91, 96. Save a histogram to `hw_day61_q1.png` with a clear title and x-axis label.",
            "Create group labels A/A/A/B/B/B and scores 72, 75, 78, 82, 88, 91. Save a boxplot comparing groups and print the group medians.",
            "Create hours 1, 2, 3, 4, 5, 6 and marks 60, 65, 70, 78, 85, 88. Save a scatterplot with a red regression line.",
        ],
        "r_distribution_sim": [
            "Set seed 22. Simulate 500 exam scores from a normal distribution with mean 75 and sd 8. Print simulated mean, sd, and the proportion above 85.",
            "Set seed 33. Simulate 1000 sample means where each sample has n = 25 from N(50, 12). Print the mean and sd of the sample means.",
            "Use `qnorm` to find the 90th, 95th, and 99th percentiles for a normal distribution with mean 100 and sd 15. Print labelled results.",
        ],
        "r_confidence_interval": [
            "Use scores 82, 79, 88, 91, 85, 77, 90, 86. Manually calculate a 95% t confidence interval for the mean and print lower/upper bounds.",
            "Use wait times 4.2, 5.1, 3.8, 6.0, 4.9, 5.5. Print sample mean, standard error, margin of error, and 95% confidence interval.",
            "Use a vector of 10 study-hour values. Build a function `mean_ci` that returns mean, lower bound, and upper bound.",
        ],
        "r_t_test": [
            "Use before scores 70, 72, 68, 75, 74 and after scores 76, 78, 70, 79, 80. Run a paired t-test and print mean change.",
            "Use group A scores 82, 85, 88, 90 and group B scores 75, 78, 80, 83. Run a two-sample t-test and explain whether the means look different.",
            "Use sample scores 68, 72, 75, 77, 80, 82. Run a one-sample t-test against mu = 70 and print the p-value with a plain-English conclusion.",
        ],
        "r_regression": [
            "Use hours 2, 3, 4, 5, 6, 7 and marks 65, 70, 76, 82, 86, 91. Fit `lm(marks ~ hours)`, print slope, intercept, and R-squared.",
            "Use ads 10, 15, 20, 25, 30 and sales 100, 125, 150, 168, 190. Fit a regression and predict sales when ads = 22.",
            "Create a scatterplot for temperature 12, 15, 18, 21, 24, 27 and ice cream sales 80, 95, 110, 140, 165, 190. Add a fitted line and print correlation.",
        ],
        "r_chi_square_report": [
            "Create a 2x2 table with counts 24, 16, 12, 28 for Method A/B and Pass/Fail. Run `chisq.test` and print the expected counts.",
            "Create a table for grade level 11/12 and club yes/no with counts 18, 22, 25, 15. Run a chi-square test and write one report sentence.",
            "Create a 3x2 table for study plan Low/Medium/High by pass/fail counts: 10/20, 18/12, 25/5. Run `chisq.test`, print p-value, and explain the conclusion.",
        ],
    }
    return prompts[kind]


def _r_statistics_practice(day: int, title: str, kind: str, base: str) -> list[str]:
    prompts = _r_statistics_homework_prompts(kind)
    base_language = TARGET_LANGUAGES[base]["name"]
    return [
        f"HW Q1: Program 1 file day{day:02d}_q1.R. Required task: {prompts[0]} Required output: labelled R output plus one statistics interpretation sentence. Include one comment comparing the R data-analysis syntax with {base_language}.",
        f"HW Q2: Program 2 file day{day:02d}_q2.R. Required task: {prompts[1]} Required output: labelled R output and a short explanation of the variable types or statistical method used.",
        f"HW Q3: Program 3 file day{day:02d}_q3.R. Required task: {prompts[2]} Required output: labelled R output, a prediction before running the statistic, and a final conclusion after the result.",
    ]


def _r_statistics_checklist(day: int, title: str, base: str) -> list[str]:
    base_language = TARGET_LANGUAGES[base]["name"]
    return [
        f"Read Day {day:02d}: {title}.",
        f"Compare the {base_language} baseline idea with the R data-analysis sample.",
        "Type and run the R sample exactly once before modifying it.",
        "Identify the dataset, variables, sample size, statistic, and output interpretation.",
        "Complete HW Q1, HW Q2, and HW Q3 as three separate R scripts.",
        "Submit the scripts with one plain-English statistics conclusion for each program.",
    ]


def _r_statistics_assignment(day: int, title: str, base: str) -> str:
    base_language = TARGET_LANGUAGES[base]["name"]
    return (
        f"Submit three separate R data-analysis programs: day{day:02d}_q1.R, day{day:02d}_q2.R, and day{day:02d}_q3.R. "
        f"Each program must solve its exact prompt for '{title}', print labelled output, and include one short interpretation written for a statistics class. "
        f"Also include concise line notes explaining the key R functions and how the workflow differs from {base_language}. "
        "If a plot is produced, upload the R script and describe the saved image filename in your note."
    )


def _r_statistics_lesson(day: int, base: str = "cpp", ui_language: str = "en") -> dict:
    ui_language = normalize_ui_language(ui_language)
    topic = R_STATISTICS_TOPICS[day - len(TOPICS) - 1]
    title = topic["title"]
    kind = topic["kind"]
    base_language = TARGET_LANGUAGES[base]["name"]
    code = topic["code"]
    bridge = _r_statistics_bridge(day, topic, base)
    explanation = (
        f"{topic['summary']} This is part of the R statistics extension after the 56-day programming core. "
        "Focus on the full analysis habit: inspect the data, choose the statistic or graph, run the R function, then explain the result in plain English."
    )
    if ui_language != "en":
        summary = LOCALIZED_R_STATS_SUMMARIES.get(ui_language, {}).get(kind, topic["summary"])
        explanation = LOCALIZED_EXPLANATION_TEMPLATES[ui_language]["r_stats"].format(summary=summary)
    lesson = Lesson(
        day=day,
        category=f"Day {day:02d} - {title}",
        week=((day - 1) // 7) + 1,
        title=title,
        goal=f"Apply R to a statistics-style data-analysis task: {topic['summary']}",
        cpp_bridge=(
            f"Use your {base_language} programming foundation for variables, functions, loops, and arrays. "
            "Then let R handle the statistics workflow with data frames, vectors, formulas, models, tests, and clear interpretation."
        ),
        explanation=explanation,
        syntax_bridge=bridge,
        official_docs=bridge["docs"],
        racket_focus=[
            "R statistics workflow",
            f"{base_language} comparison: manual data handling to R analysis functions",
            "data interpretation",
            "reproducible labelled output",
        ],
        code=code,
        line_notes=_line_notes(code, "r", base),
        practice=_r_statistics_practice(day, title, kind, base),
        checklist=_r_statistics_checklist(day, title, base),
        assignment=_r_statistics_assignment(day, title, base),
        grading_rubric=[
            "Correctness: the R code runs and prints the requested labelled output.",
            "Data handling: the dataset, variable types, missing values, or groups are handled correctly.",
            "Statistics method: the selected summary, plot, interval, test, or model matches the question.",
            "Interpretation: the conclusion uses plain English and does not overclaim.",
            "Completeness: HW Q1, HW Q2, and HW Q3 are separate, reproducible R scripts.",
        ],
    )
    data = asdict(lesson)
    data["target_language"] = "r"
    data["target_language_name"] = "R"
    data["base_language"] = base
    data["base_language_name"] = base_language
    data["topic_kind"] = kind
    data["base_kind"] = kind
    return data


BASE_COMPARISON_EXAMPLES = {
    "comment": {
        "cpp": "// note",
        "c": "// note",
        "java": "// note",
        "python": "# note",
        "racket": "; note",
        "r": "# note",
    },
    "language_directive": {
        "cpp": "the compiler mode and .cpp file",
        "c": "the compiler mode and .c file",
        "java": "the .java file and class name",
        "python": "the .py file and Python interpreter",
        "racket": "#lang racket",
        "r": "the .R file and Rscript interpreter",
    },
    "import": {
        "cpp": "#include <iostream>",
        "c": "#include <stdio.h>",
        "java": "import java.util.Scanner;",
        "python": "import math",
        "racket": "(require racket/list)",
        "r": "library(stats)",
    },
    "entry": {
        "cpp": "int main() { ... }",
        "c": "int main(void) { ... }",
        "java": "public static void main(String[] args) { ... }",
        "python": "top-level code or if __name__ == '__main__':",
        "racket": "top-level expressions after #lang racket",
        "r": "top-level expressions in an .R script",
    },
    "function_def": {
        "cpp": "return_type name(args) { ... }",
        "c": "return_type name(args) { ... }",
        "java": "static returnType name(args) { ... }",
        "python": "def name(args):",
        "racket": "(define (name args) ...)",
        "r": "name <- function(args) { ... }",
    },
    "variable": {
        "cpp": "auto name = value;",
        "c": "int name = value;",
        "java": "var name = value;",
        "python": "name = value",
        "racket": "(define name value)",
        "r": "name <- value",
    },
    "if": {
        "cpp": "if (condition) { ... }",
        "c": "if (condition) { ... }",
        "java": "if (condition) { ... }",
        "python": "if condition:",
        "racket": "(if condition then-value else-value)",
        "r": "if (condition) { ... }",
    },
    "else_if": {
        "cpp": "else if (condition) { ... }",
        "c": "else if (condition) { ... }",
        "java": "else if (condition) { ... }",
        "python": "elif condition:",
        "racket": "(cond [condition result] [else result])",
        "r": "else if (condition) { ... }",
    },
    "multi_case": {
        "cpp": "switch (value) { case x: ... }",
        "c": "switch (value) { case x: ... }",
        "java": "switch (value) { case x -> ... }",
        "python": "match value:",
        "racket": "(case value [(x) result] [else result])",
        "r": "switch(as.character(value), \"1\" = result, default)",
    },
    "for_loop": {
        "cpp": "for (int i = 0; i < n; ++i) { ... }",
        "c": "for (int i = 0; i < n; ++i) { ... }",
        "java": "for (int i = 0; i < n; i++) { ... }",
        "python": "for item in items:",
        "racket": "(for ([item items]) ...)",
        "r": "for (item in items) { ... }",
    },
    "while_loop": {
        "cpp": "while (condition) { ... }",
        "c": "while (condition) { ... }",
        "java": "while (condition) { ... }",
        "python": "while condition:",
        "racket": "a named let or recursive helper",
        "r": "while (condition) { ... } or repeat { ...; break }",
    },
    "local_binding": {
        "cpp": "{ auto name = value; ... }",
        "c": "{ int name = value; ... }",
        "java": "{ var name = value; ... }",
        "python": "a local name inside an indented block",
        "racket": "(let ([name value]) ...)",
        "r": "a local name inside a function or block",
    },
    "data_shape": {
        "cpp": "struct Name { ... };",
        "c": "struct Name { ... };",
        "java": "class Name { ... } or record Name(...)",
        "python": "class Name:",
        "racket": "(struct name (fields))",
        "r": "list(field = value) or a small S3 object",
    },
    "class": {
        "cpp": "class Name { ... };",
        "c": "a struct plus related functions",
        "java": "class Name { ... }",
        "python": "class Name:",
        "racket": "(class object% ...)",
        "r": "a list with class(object) <- \"Name\"",
    },
    "function_call": {
        "cpp": "name(arg1, arg2)",
        "c": "name(arg1, arg2)",
        "java": "name(arg1, arg2)",
        "python": "name(arg1, arg2)",
        "racket": "(name arg1 arg2)",
        "r": "name(arg1, arg2)",
    },
    "block_start": {
        "cpp": "{",
        "c": "{",
        "java": "{",
        "python": "an indented block after :",
        "racket": "nested parentheses",
        "r": "{",
    },
    "block_end": {
        "cpp": "}",
        "c": "}",
        "java": "}",
        "python": "dedenting back to the previous level",
        "racket": "closing parentheses",
        "r": "}",
    },
    "return": {
        "cpp": "return value;",
        "c": "return value;",
        "java": "return value;",
        "python": "return value",
        "racket": "the last expression in a function",
        "r": "return(value) or the last expression in a function",
    },
    "output": {
        "cpp": "std::cout << value;",
        "c": "printf(\"%d\\n\", value);",
        "java": "System.out.println(value);",
        "python": "print(value)",
        "racket": "(displayln value)",
        "r": "cat(value, \"\\n\")",
    },
    "statement": {
        "cpp": "statement;",
        "c": "statement;",
        "java": "statement;",
        "python": "one logical line, usually no semicolon",
        "racket": "one expression",
        "r": "one expression, usually no semicolon",
    },
}

TOKEN_RE = re.compile(
    r"System\.out\.println|std::boolalpha|std::vector|std::string|std::cout|std::cin|string->number|racket/string|as\.integer|as\.numeric|#include|#lang|//|/\*|\*/|<-|==|!=|<=|>=|&&|\|\||::|->|"
    r'"(?:\\.|[^"])*"|\'(?:\\.|[^\'])*\'|<[^>\s]+>|[A-Za-z_][A-Za-z0-9_!?-]*|'
    r"[0-9]+(?:\.[0-9]+)?|[(){}\[\],;:+\-*/%=<>.$]"
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

R_PHRASES = {
    "<-": "Assignment operator. It binds the value on the right to the name on the left.",
    "function": "Creates a function value. In `name <- function(x)`, the function is stored in `name`.",
    "cat": "Output function. It prints values without adding a newline unless you include `\"\\n\"`.",
    "sprintf": "Builds formatted text by putting values into placeholders.",
    "readline": "Reads one line of text from standard input.",
    "as.integer": "Converts text or a numeric value into a whole number.",
    "as.numeric": "Converts text into a decimal-capable numeric value.",
    "tolower": "Converts text to lowercase before comparing it.",
    "substr": "Extracts part of a string, such as the first character.",
    "scan": "Reads several values and returns a vector.",
    "TRUE": "Boolean true value in R.",
    "FALSE": "Boolean false value in R.",
    "if": "Starts a conditional branch.",
    "else": "Fallback branch or else-if branch.",
    "for": "Starts a loop over a vector or sequence.",
    "while": "Repeats while a condition is true.",
    "repeat": "Starts a loop that runs until `break` stops it.",
    "break": "Stops the nearest loop.",
    "sample": "Chooses random values from a vector.",
    "c": "Combines values into a vector.",
    "list": "Creates a flexible object with named or unnamed items.",
    "matrix": "Creates a two-dimensional table.",
    "nrow": "Returns the number of rows in a matrix/data frame.",
    "ncol": "Returns the number of columns in a matrix/data frame.",
    "switch": "Chooses one result from exact-match cases.",
    "class": "Gets or sets an object's class label.",
    "return": "Returns a value from a function explicitly.",
    "$": "Accesses a named field inside a list or object.",
    "[": "Starts vector indexing. R indexes from 1.",
    "]": "Ends vector indexing.",
    "{": "Starts a block of expressions.",
    "}": "Ends a block of expressions.",
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
    if target == "r":
        if token in R_PHRASES:
            return R_PHRASES[token]
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):
            return "Name for a value, function, vector, list, or object."
        if token in {"+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">="}:
            return "Operator. It calculates or compares values."
        return "R syntax symbol."
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
    if target == "r" and stripped.startswith("#"):
        return [
            {"phrase": "#", "meaning": "Starts an R comment."},
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
    elif "defines a function" in plain or ("defines" in plain and "function" in plain) or line.startswith("def "):
        concept = "function_def"
    elif "binds" in plain or "updates a name" in plain or " = " in line or "<-" in line:
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


def _line_note_for_r(line: str) -> dict[str, str]:
    stripped = line.strip()
    if not stripped:
        return {"line": "", "plain": "Blank line for readability.", "syntax": "R ignores blank lines.", "cpp": "Like a blank line in C++."}
    if stripped.startswith("#"):
        return {"line": line, "plain": "A comment.", "syntax": "R line comments start with #.", "cpp": "Like // in C++."}
    if stripped.startswith("library("):
        return {"line": line, "plain": "Imports a package.", "syntax": "library makes package functions available in this script.", "cpp": "Similar purpose to #include."}
    if "<- function" in stripped or "function(" in stripped:
        return {"line": line, "plain": "Defines a reusable function.", "syntax": "In R, `name <- function(args)` stores a function in a name.", "cpp": "Similar to return_type name(args) {."}
    if stripped.startswith("if "):
        return {"line": line, "plain": "Starts a condition.", "syntax": "The condition goes in parentheses, and braces hold the branch body.", "cpp": "Very close to if (...) { ... }."}
    if stripped.startswith("} else if") or stripped.startswith("else if"):
        return {"line": line, "plain": "Checks another condition after the first if fails.", "syntax": "R uses `else if` with braces for an else-if chain.", "cpp": "Same idea as C++ else if."}
    if stripped.startswith("} else") or stripped.startswith("else"):
        return {"line": line, "plain": "Handles the remaining case.", "syntax": "The else branch must connect to the previous if block.", "cpp": "Same role as else { ... }."}
    if stripped.startswith("for "):
        return {"line": line, "plain": "Starts a loop over a sequence.", "syntax": "`for (item in values)` takes one value at a time from a vector or sequence.", "cpp": "Similar to a range-based for loop."}
    if stripped.startswith("while "):
        return {"line": line, "plain": "Starts a while loop.", "syntax": "The body repeats while the condition stays TRUE.", "cpp": "Same role as while (...) { ... }."}
    if stripped.startswith("repeat"):
        return {"line": line, "plain": "Starts a loop that runs at least once.", "syntax": "`repeat` continues until a `break` statement stops it.", "cpp": "Closest to a do-while loop pattern."}
    if stripped.startswith("break"):
        return {"line": line, "plain": "Stops the nearest loop.", "syntax": "R uses break inside repeat/while/for when the loop should end early.", "cpp": "Same role as C++ break."}
    if stripped.startswith("return"):
        return {"line": line, "plain": "Returns a value from a function.", "syntax": "R can return explicitly with `return(value)`, though the last expression can also be returned.", "cpp": "Same role as C++ return value;."}
    if "cat(" in stripped or "print(" in stripped:
        return {"line": line, "plain": "Prints output.", "syntax": "`cat` prints clean console text; include `\"\\n\"` when you want a newline.", "cpp": "Similar purpose to std::cout."}
    if "readline(" in stripped:
        return {"line": line, "plain": "Reads user input as text.", "syntax": "`readline` returns a string, so numeric input needs `as.integer` or `as.numeric`.", "cpp": "Closest to reading into a string before converting."}
    if " <- " in stripped or stripped.startswith(("class(", "names(")):
        return {"line": line, "plain": "Binds or updates a name.", "syntax": "`<-` stores the value on the right into the name or field on the left.", "cpp": "Similar to assignment, but R commonly uses `<-` instead of `=`."}
    if stripped in {"}", "};"}:
        return {"line": line, "plain": "Ends a block.", "syntax": "This closes the nearest open brace.", "cpp": "Same as C++."}
    if stripped.endswith("{"):
        return {"line": line, "plain": "Starts a block.", "syntax": "Braces group multiple R expressions under a condition, loop, or function.", "cpp": "Same block-reading habit as C++."}
    return {"line": line, "plain": "A normal R expression.", "syntax": "Read the assignment, function call, or vector operation from left to right.", "cpp": "Use the same role-first reading habit as C++."}


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
    elif target == "r":
        notes = [_line_note_for_r(line) for line in code.splitlines()]
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


def _lesson(day: int, target: str, base: str = "cpp", ui_language: str = "en") -> dict:
    ui_language = normalize_ui_language(ui_language)
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
        explanation=_explanation(title, kind, target, base, ui_language),
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


def get_lessons(target_language: str | None = None, base_language: str | None = None, ui_language: str | None = None) -> list[dict]:
    target = normalize_target_language(target_language)
    base = normalize_base_language(base_language)
    ui_language = normalize_ui_language(ui_language)
    lessons = [_lesson(day, target, base, ui_language) for day in range(1, len(TOPICS) + 1)]
    if target == "r":
        lessons.extend(_r_statistics_lesson(day, base, ui_language) for day in range(len(TOPICS) + 1, get_course_length(target) + 1))
    return lessons


def get_lesson(day: int, target_language: str | None = None, base_language: str | None = None, ui_language: str | None = None) -> dict | None:
    lessons = get_lessons(target_language, base_language, ui_language)
    if 1 <= day <= len(lessons):
        return lessons[day - 1]
    return None
