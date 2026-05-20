from __future__ import annotations

from dataclasses import dataclass, asdict


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


LESSON_BLUEPRINTS = [
    {
        "category": "Day 01 - Racket Setup and REPL Thinking",
        "title": "从编译运行切换到交互式求值",
        "goal": "安装并理解 Racket 的运行方式，习惯在 DrRacket 或命令行 REPL 中快速试验表达式。",
        "cpp_bridge": "C++ 通常写完 main、编译、运行；Racket 鼓励你把每个表达式直接送进 REPL 观察结果。",
        "explanation": "今天不追求写大程序，而是建立学习环境和求值直觉。Racket 程序由表达式组成，表达式会产生值。你要习惯把小问题拆成小表达式，先验证，再组合成函数。",
        "racket_focus": ["DrRacket interactions window", "racket 命令", "表达式求值", "注释"],
        "code": "#lang racket\n\n(+ 1 2 3)\n(* 6 7)\n(string-append \"Hello, \" \"Racket\")\n\n; 运行：racket day01.rkt",
        "practice": ["安装 Racket 并运行一个 .rkt 文件。", "在 REPL 中分别计算整数、字符串和布尔表达式。", "写 5 个表达式并预测结果，再运行验证。"],
        "assignment": "提交一个 day01.rkt，包含 10 个表达式和每个表达式的注释预测。",
    },
    {
        "category": "Day 02 - Prefix Notation",
        "title": "前缀表达式：把运算符放在最前面",
        "goal": "熟练阅读和编写 Racket 的前缀语法。",
        "cpp_bridge": "C++ 写 `a + b * c`，Racket 写 `(+ a (* b c))`。括号不是分组装饰，而是函数调用结构。",
        "explanation": "Racket 的语法非常一致：`(函数 参数1 参数2 ...)`。一开始你会觉得括号多，但一致性会让后面的宏、列表处理和函数组合更容易。",
        "racket_focus": ["前缀调用", "嵌套表达式", "算术函数", "求值顺序"],
        "code": "#lang racket\n\n(+ 10 20)\n(- 20 3 2)\n(* (+ 2 3) (- 10 4))\n(/ (+ 8 4) 3)",
        "practice": ["把 5 个 C++ 算术表达式改写成 Racket。", "画出一个嵌套表达式的树形结构。", "故意删掉一个括号，观察错误信息。"],
        "assignment": "提交一组 C++ 表达式和对应 Racket 表达式，至少 12 组。",
    },
    {
        "category": "Day 03 - Values and Types",
        "title": "数字、字符串、布尔值和符号",
        "goal": "掌握 Racket 常见基本值，并理解动态类型和谓词函数。",
        "cpp_bridge": "C++ 变量有静态类型；Racket 值有运行时类型，并常用 `number?`、`string?` 这类谓词检查。",
        "explanation": "Racket 不需要提前声明变量类型，但这不等于没有类型。每个值都有类型，错误通常发生在函数收到不合适的值时。谓词函数以问号结尾，是 Racket 习惯命名。",
        "racket_focus": ["number?", "string?", "boolean?", "symbol?", "动态类型"],
        "code": "#lang racket\n\n(number? 42)\n(string? \"cpp\")\n(boolean? #t)\n(symbol? 'racket)\n(equal? 'racket \"racket\")",
        "practice": ["为 8 个值写出对应谓词测试。", "比较 symbol 和 string 的不同。", "写一个表达式故意触发类型错误并解释。"],
        "assignment": "提交一个类型观察表：值、预测类型、谓词验证、说明。",
    },
    {
        "category": "Day 04 - Defining Names",
        "title": "define：给值和函数命名",
        "goal": "理解 `define` 绑定值和函数的两种常见形式。",
        "cpp_bridge": "C++ 的变量赋值常可修改；Racket 的 `define` 更像给一个值起名字，默认强调不可变。",
        "explanation": "命名是抽象的第一步。你会用 `define` 保存常量，也会用它定义函数。函数定义不是特殊魔法，本质上也是给一个函数值绑定名字。",
        "racket_focus": ["define 值", "define 函数", "命名规范", "不可变思维"],
        "code": "#lang racket\n\n(define tax-rate 0.13)\n(define price 100)\n\n(define (add-tax amount)\n  (* amount (+ 1 tax-rate)))\n\n(add-tax price)",
        "practice": ["定义 5 个常量。", "写 3 个一参数函数。", "把重复表达式抽成名字。"],
        "assignment": "写一个小型账单计算器，包含 subtotal、tax、tip 和 total 函数。",
    },
    {
        "category": "Day 05 - Function Design Recipe",
        "title": "函数设计流程：签名、目的、例子、实现",
        "goal": "学习系统化设计函数，而不是直接写代码。",
        "cpp_bridge": "C++ 中你可能先写函数体再调试；Racket 学习传统强调先写合同、例子和测试。",
        "explanation": "今天开始使用设计流程：写函数签名、说明输入输出、给出样例，再实现。这个流程会让你的递归和数据结构题目稳定很多。",
        "racket_focus": ["函数签名注释", "purpose statement", "check-expect 思维", "小步实现"],
        "code": "#lang racket\n\n; fahrenheit->celsius : Number -> Number\n; Convert Fahrenheit temperature to Celsius.\n(define (fahrenheit->celsius f)\n  (* (- f 32) 5/9))\n\n(fahrenheit->celsius 212)",
        "practice": ["为 4 个函数写签名和目的说明。", "先写例子，再实现函数。", "检查边界值，例如 0、负数、小数。"],
        "assignment": "实现 6 个单位转换函数，每个都有签名、说明和至少 2 个例子。",
    },
    {
        "category": "Day 06 - Conditionals",
        "title": "if 和 cond：表达选择逻辑",
        "goal": "掌握 Racket 的条件表达式，并和 C++ if/else 对照。",
        "cpp_bridge": "C++ 的 if 是语句；Racket 的 if/cond 是表达式，会产生值。",
        "explanation": "条件表达式是 Racket 风格的重要部分。你不是在某个分支里修改外部变量，而是让整个条件表达式计算出一个结果。",
        "racket_focus": ["if", "cond", "else", "比较函数"],
        "code": "#lang racket\n\n(define (grade-score score)\n  (cond\n    [(>= score 90) \"A\"]\n    [(>= score 80) \"B\"]\n    [(>= score 70) \"C\"]\n    [else \"Needs practice\"]))",
        "practice": ["用 if 写绝对值函数。", "用 cond 写成绩等级函数。", "解释每个分支的返回值类型。"],
        "assignment": "写一个 `racket-level` 函数，根据学习天数返回 beginner/intermediate/advanced。",
    },
    {
        "category": "Day 07 - Boolean Logic",
        "title": "布尔组合：and、or、not",
        "goal": "用布尔表达式表达复杂条件。",
        "cpp_bridge": "C++ 使用 `&&`、`||`、`!`；Racket 使用 `(and ...)`、`(or ...)`、`(not ...)`。",
        "explanation": "布尔表达式应该尽量直接表达规则。Racket 的 `and` 和 `or` 可以接多个参数，也会短路求值。",
        "racket_focus": ["and", "or", "not", "短路求值", "谓词组合"],
        "code": "#lang racket\n\n(define (valid-score? score)\n  (and (number? score) (>= score 0) (<= score 100)))\n\n(define (pass? score)\n  (and (valid-score? score) (>= score 60)))",
        "practice": ["写一个检查年龄是否合理的谓词。", "组合 number? 和范围判断。", "测试非法输入。"],
        "assignment": "实现 `valid-password-shape?`，检查长度、是否字符串、是否非空。",
    },
    {
        "category": "Day 08 - Local Bindings with let",
        "title": "let：局部命名和中间结果",
        "goal": "用 `let` 管理中间计算，避免重复表达式。",
        "cpp_bridge": "C++ 中常用局部变量保存中间结果；Racket 用 `let` 建立局部绑定。",
        "explanation": "`let` 让你在表达式内部定义局部名字。它不会修改状态，只是让复杂表达式更可读。",
        "racket_focus": ["let", "let*", "作用域", "中间结果"],
        "code": "#lang racket\n\n(define (circle-report r)\n  (let ([area (* pi r r)]\n        [diameter (* 2 r)])\n    (string-append \"area=\" (number->string area)\n                   \", diameter=\" (number->string diameter))))",
        "practice": ["把重复计算改写为 let。", "比较 let 和 let* 的求值区别。", "解释局部变量的作用域。"],
        "assignment": "写一个订单总价函数，用 let 保存折扣、税和最终价格。",
    },
    {
        "category": "Day 09 - Lists as Core Data",
        "title": "列表：Racket 的核心数据结构",
        "goal": "理解 list、empty、cons、first、rest。",
        "cpp_bridge": "C++ vector 偏向随机访问；Racket list 偏向递归地处理头和尾。",
        "explanation": "Racket 列表是递归结构：空列表，或一个元素 cons 到另一个列表。理解这一点，是后面递归、map、fold 的基础。",
        "racket_focus": ["list", "empty?", "cons", "first", "rest"],
        "code": "#lang racket\n\n(define nums (list 10 20 30))\n(first nums)\n(rest nums)\n(cons 5 nums)\n(empty? '())",
        "practice": ["构造 5 个不同类型列表。", "用 first/rest 取出元素。", "画出 cons 链结构。"],
        "assignment": "提交一个列表练习文件，包含构造、访问、添加元素和空列表检查。",
    },
    {
        "category": "Day 10 - Recursion on Lists",
        "title": "列表递归：处理 empty 和 cons",
        "goal": "写出第一个结构化列表递归函数。",
        "cpp_bridge": "C++ 常用 for 循环遍历 vector；Racket 常用递归处理 list。",
        "explanation": "列表递归模板很稳定：如果列表为空，返回基本答案；否则处理 first，并递归处理 rest。",
        "racket_focus": ["递归模板", "base case", "recursive case", "结构递归"],
        "code": "#lang racket\n\n(define (sum nums)\n  (cond\n    [(empty? nums) 0]\n    [else (+ (first nums) (sum (rest nums)))]))\n\n(sum (list 1 2 3 4))",
        "practice": ["写 count 函数。", "写 product 函数。", "用模板解释每一行。"],
        "assignment": "实现 sum、count、contains? 三个列表递归函数。",
    },
    {
        "category": "Day 11 - More List Recursion",
        "title": "过滤、转换和查找",
        "goal": "通过递归实现常见列表算法。",
        "cpp_bridge": "C++ 里你可能 push_back 到结果 vector；Racket 里通常用 cons 构造新列表。",
        "explanation": "函数式程序倾向于不修改原列表，而是产生新列表。你会看到每个递归分支都返回一个值。",
        "racket_focus": ["构造结果列表", "filter 模式", "map 模式", "查找"],
        "code": "#lang racket\n\n(define (only-positive nums)\n  (cond\n    [(empty? nums) '()]\n    [(positive? (first nums))\n     (cons (first nums) (only-positive (rest nums)))]\n    [else (only-positive (rest nums))]))",
        "practice": ["实现 double-all。", "实现 only-even。", "实现 any-negative?。"],
        "assignment": "写 4 个列表递归函数，并为每个函数说明 base case 和 recursive case。",
    },
    {
        "category": "Day 12 - Strings and Characters",
        "title": "字符串处理和字符判断",
        "goal": "掌握常用 string 函数，并理解字符串与列表的区别。",
        "cpp_bridge": "C++ string 可用索引和循环；Racket string 也可索引，但很多时候会先转换成 list 处理。",
        "explanation": "字符串是文本数据，列表是结构数据。Racket 提供丰富的字符串函数，也允许你把字符串拆成字符列表，用函数式方式处理。",
        "racket_focus": ["string-length", "substring", "string-ref", "string->list", "char?"],
        "code": "#lang racket\n\n(define word \"racket\")\n(string-length word)\n(string-ref word 0)\n(substring word 1 4)\n(string->list word)",
        "practice": ["写 first-char-safe。", "判断字符串是否以某字符开头。", "把字符串转换成字符列表并计数。"],
        "assignment": "实现一个简单文本分析器：长度、首字符、是否包含空格。",
    },
    {
        "category": "Day 13 - Structs",
        "title": "struct：定义自己的数据类型",
        "goal": "用 struct 表示领域对象。",
        "cpp_bridge": "Racket struct 类似 C++ struct/class 的轻量版本，但默认更适合不可变数据建模。",
        "explanation": "当多个值总是一起出现时，应该定义结构体。Racket 会自动生成构造函数、谓词和访问器。",
        "racket_focus": ["struct", "构造器", "访问器", "透明结构"],
        "code": "#lang racket\n\n(struct student (name score) #:transparent)\n\n(define ada (student \"Ada\" 95))\n(student-name ada)\n(student-score ada)\n(student? ada)",
        "practice": ["定义 book struct。", "定义 point struct。", "写函数处理 struct。"],
        "assignment": "设计一个 `course` struct，并写函数判断课程是否通过。",
    },
    {
        "category": "Day 14 - Review Project 1",
        "title": "两周复盘：小型成绩系统",
        "goal": "整合函数、条件、列表和 struct。",
        "cpp_bridge": "这相当于用 Racket 写一个简化版 C++ 控制台数据处理项目。",
        "explanation": "今天不学新语法，重点是把前 13 天组合起来。你要能把数据建模、函数拆分、递归处理和测试串成一个小项目。",
        "racket_focus": ["综合设计", "数据建模", "列表递归", "清晰命名"],
        "code": "#lang racket\n\n(struct student (name score) #:transparent)\n\n(define roster\n  (list (student \"Ada\" 95)\n        (student \"Grace\" 82)\n        (student \"Linus\" 58)))\n\n(define (passing? s)\n  (>= (student-score s) 60))",
        "practice": ["写 average-score。", "写 passing-students。", "写 best-student。"],
        "assignment": "完成一个成绩系统：输入学生列表，输出平均分、通过名单和最高分学生。",
    },
    {
        "category": "Day 15 - Higher-Order Functions",
        "title": "高阶函数：函数可以当参数",
        "goal": "理解函数值，并使用 map/filter/foldr。",
        "cpp_bridge": "C++ 有函数指针、lambda 和 STL algorithms；Racket 把函数作为普通值使用非常自然。",
        "explanation": "高阶函数让你把遍历模式抽出来，只留下变化的逻辑。map 转换，filter 筛选，fold 汇总。",
        "racket_focus": ["function values", "map", "filter", "foldr"],
        "code": "#lang racket\n\n(map sqr (list 1 2 3 4))\n(filter even? (list 1 2 3 4 5 6))\n(foldr + 0 (list 1 2 3 4))",
        "practice": ["用 map 替代递归 double-all。", "用 filter 替代 only-positive。", "用 foldr 计算总和。"],
        "assignment": "把 Day 11 的递归函数改写为 map/filter/fold 版本。",
    },
    {
        "category": "Day 16 - Lambda",
        "title": "lambda：匿名函数",
        "goal": "写简短函数并传给高阶函数。",
        "cpp_bridge": "C++ lambda `[&](int x){ return x+1; }`，Racket lambda `(lambda (x) (+ x 1))`。",
        "explanation": "当函数只在一个地方使用时，lambda 可以减少命名负担。也要避免过度使用，复杂逻辑仍然应该命名。",
        "racket_focus": ["lambda", "匿名函数", "局部行为", "可读性"],
        "code": "#lang racket\n\n(map (lambda (x) (* x 10)) (list 1 2 3))\n(filter (lambda (name) (> (string-length name) 3))\n        (list \"C\" \"Java\" \"Racket\"))",
        "practice": ["写 5 个 lambda 传给 map。", "写 3 个 lambda 传给 filter。", "判断哪些 lambda 应该改成具名函数。"],
        "assignment": "用 lambda 完成一个学生名单转换和筛选任务。",
    },
    {
        "category": "Day 17 - foldl and foldr",
        "title": "fold：把列表折叠成一个结果",
        "goal": "掌握 fold 的 accumulator 思维。",
        "cpp_bridge": "fold 类似 C++ 中循环累加变量，但不会修改变量，而是把新状态传入下一步。",
        "explanation": "fold 是列表汇总的通用模式。你可以用它求和、拼接字符串、找最大值、构造新结构。",
        "racket_focus": ["foldl", "foldr", "accumulator", "汇总"],
        "code": "#lang racket\n\n(foldl (lambda (x acc) (+ x acc)) 0 (list 1 2 3))\n(foldl max 0 (list 4 9 2 7))\n(foldr cons '() (list 1 2 3))",
        "practice": ["用 foldl 求长度。", "用 foldl 找最大数。", "用 foldr 解释顺序差异。"],
        "assignment": "实现一个 report 函数，用 fold 汇总数量、总分和最高分。",
    },
    {
        "category": "Day 18 - Immutability",
        "title": "不可变数据：不改原值，产生新值",
        "goal": "从修改变量转向构造新数据。",
        "cpp_bridge": "C++ 常原地修改 vector；Racket 常保留旧列表并返回新列表。",
        "explanation": "不可变让程序更容易推理：旧值不会突然变化。代价是你需要学习如何有效构造新值。",
        "racket_focus": ["immutable lists", "pure functions", "无副作用", "数据转换"],
        "code": "#lang racket\n\n(define xs (list 1 2 3))\n(define ys (cons 0 xs))\nxs\nys",
        "practice": ["写 add-one 不改变原列表。", "写 replace-first 返回新列表。", "解释 xs 为什么没变。"],
        "assignment": "实现一个 todo 列表转换函数：添加、完成、筛选未完成，均返回新列表。",
    },
    {
        "category": "Day 19 - Testing with rackunit",
        "title": "rackunit：为函数写测试",
        "goal": "使用 rackunit 编写可运行测试。",
        "cpp_bridge": "类似 C++ 的 GoogleTest 或 Catch2，但 Racket 内置生态更轻量。",
        "explanation": "测试是学习语言最快的反馈方式。每写一个函数，至少给出正常、边界、异常思路的测试。",
        "racket_focus": ["require rackunit", "check-equal?", "check-true", "测试文件"],
        "code": "#lang racket\n(require rackunit)\n\n(define (double x) (* 2 x))\n\n(check-equal? (double 4) 8)\n(check-true (> (double 5) 5))",
        "practice": ["给 Day 10 的 sum 写测试。", "给条件函数写边界测试。", "运行测试并修复失败。"],
        "assignment": "为至少 5 个旧函数补充 rackunit 测试。",
    },
    {
        "category": "Day 20 - Modules and require",
        "title": "模块化：拆分文件和 require",
        "goal": "理解 provide/require，把代码组织成多个文件。",
        "cpp_bridge": "类似 C++ 的 .h/.cpp 分离和 include，但 Racket 模块系统更明确。",
        "explanation": "当程序变大时，必须拆分。Racket 文件通常就是模块，用 provide 导出名字，用 require 导入依赖。",
        "racket_focus": ["provide", "require", "模块边界", "文件组织"],
        "code": "#lang racket\n\n(provide square-area)\n\n(define (square-area side)\n  (* side side))",
        "practice": ["创建 math-utils.rkt。", "从 main.rkt require 它。", "只导出需要的函数。"],
        "assignment": "把成绩系统拆成 model.rkt、logic.rkt、main.rkt 三个文件。",
    },
    {
        "category": "Day 21 - Review Project 2",
        "title": "高阶函数版文本分析器",
        "goal": "使用 map/filter/fold 和模块组织完成项目。",
        "cpp_bridge": "这类似用 STL algorithms 写文本统计工具。",
        "explanation": "今天整合字符串、列表、高阶函数和测试。目标不是代码最长，而是函数拆分清楚、测试覆盖关键逻辑。",
        "racket_focus": ["文本处理", "高阶函数", "模块", "测试"],
        "code": "#lang racket\n(require rackunit)\n\n(define words (string-split \"racket is very expressive\"))\n(map string-length words)\n(filter (lambda (w) (> (string-length w) 3)) words)",
        "practice": ["统计单词数。", "找最长单词。", "筛选长度大于 n 的单词。"],
        "assignment": "完成文本分析器：输入字符串，输出单词数、平均长度、最长单词和关键词出现次数。",
    },
    {
        "category": "Day 22 - Pattern Matching",
        "title": "match：用模式拆数据",
        "goal": "使用 match 简化条件和结构拆解。",
        "cpp_bridge": "C++ switch 只能处理有限情况；Racket match 可以匹配列表、struct 和嵌套结构。",
        "explanation": "match 让你按数据形状写逻辑。对于列表和 struct，它比手写 first/rest 或访问器更清晰。",
        "racket_focus": ["match", "list patterns", "struct patterns", "_ wildcard"],
        "code": "#lang racket\n\n(define (describe xs)\n  (match xs\n    ['() \"empty\"]\n    [(list one) \"one item\"]\n    [(list a b) \"two items\"]\n    [_ \"many items\"]))",
        "practice": ["用 match 重写列表长度分类。", "匹配一个 student struct。", "使用 _ 处理默认情况。"],
        "assignment": "实现命令解析器，匹配 '(add x)、'(done x)、'(list) 三种命令。",
    },
    {
        "category": "Day 23 - Symbols and S-Expressions",
        "title": "符号和 S 表达式",
        "goal": "理解 Racket 代码和数据的统一表示。",
        "cpp_bridge": "C++ 代码和数据分得很开；Lisp/Racket 传统中代码本身也可以表示为列表数据。",
        "explanation": "S-expression 是 Racket 世界的重要概念。符号、列表、数字、字符串都可以组成可处理的数据结构。",
        "racket_focus": ["symbol", "quote", "s-expression", "代码即数据"],
        "code": "#lang racket\n\n'hello\n'(+ 1 2)\n(list '+ 1 2)\n(symbol? '+)",
        "practice": ["比较 '(+ 1 2) 和 (+ 1 2)。", "构造一个命令 S-expression。", "用 match 解析它。"],
        "assignment": "设计 8 条 todo 命令的 S-expression，并写函数解释其中 3 种。",
    },
    {
        "category": "Day 24 - Quasiquote",
        "title": "quasiquote：模板式构造列表",
        "goal": "使用 quasiquote/unquote 构造 S-expression。",
        "cpp_bridge": "类似字符串模板，但生成的是结构化列表，不是纯文本。",
        "explanation": "quasiquote 让大部分结构保持字面量，只在需要的位置插入计算结果。它是理解宏之前的重要准备。",
        "racket_focus": ["quasiquote", "unquote", "unquote-splicing", "模板数据"],
        "code": "#lang racket\n\n(define name 'score)\n(define value 95)\n`(define ,name ,value)\n\n(define fields '(name score))\n`(student ,@fields)",
        "practice": ["用 quasiquote 生成命令列表。", "比较 quote 和 quasiquote。", "使用 unquote-splicing 插入多个元素。"],
        "assignment": "写一个函数，把学生数据生成 S-expression 报告。",
    },
    {
        "category": "Day 25 - Errors and Contracts",
        "title": "错误处理和函数约定",
        "goal": "学习清晰地报告错误，并用 contract 表达接口。",
        "cpp_bridge": "C++ 可用 assert、exception、类型系统约束；Racket 常用 contract 和 error 提供运行时边界。",
        "explanation": "好错误信息能节省大量调试时间。对于模块边界，contract 可以明确说明函数期待什么输入。",
        "racket_focus": ["error", "raise-user-error", "contract-out", "防御式边界"],
        "code": "#lang racket\n\n(define (safe-first xs)\n  (if (empty? xs)\n      (error 'safe-first \"expected a non-empty list\")\n      (first xs)))",
        "practice": ["为除法函数处理除以 0。", "写清楚错误来源名字。", "了解 contract-out 语法。"],
        "assignment": "给你的文本分析器增加输入检查和清晰错误信息。",
    },
    {
        "category": "Day 26 - Tail Recursion",
        "title": "尾递归：递归中的 accumulator",
        "goal": "理解尾递归和 accumulator 版本函数。",
        "cpp_bridge": "尾递归类似循环状态推进；accumulator 就像循环中的累计变量。",
        "explanation": "普通结构递归清晰，尾递归适合长列表和累积计算。重点是理解结果如何保存在 accumulator 中。",
        "racket_focus": ["tail recursion", "accumulator", "helper function", "性能直觉"],
        "code": "#lang racket\n\n(define (sum-tail xs)\n  (define (loop remaining acc)\n    (cond\n      [(empty? remaining) acc]\n      [else (loop (rest remaining) (+ acc (first remaining)))]))\n  (loop xs 0))",
        "practice": ["把 count 改成尾递归。", "把 reverse 用 accumulator 实现。", "解释为什么 helper 是尾调用。"],
        "assignment": "实现 sum-tail、length-tail、reverse-tail，并写测试。",
    },
    {
        "category": "Day 27 - Vectors",
        "title": "vector：接近 C++ vector 的结构",
        "goal": "理解 Racket vector 和 list 的适用场景。",
        "cpp_bridge": "Racket vector 更像 C++ vector：按索引访问，适合固定位置数据。",
        "explanation": "列表适合递归和头部操作，vector 适合随机访问。Racket 有可变 vector，但使用时要明确副作用。",
        "racket_focus": ["vector", "vector-ref", "vector-set!", "list->vector"],
        "code": "#lang racket\n\n(define v (vector 10 20 30))\n(vector-ref v 1)\n(vector-length v)\n(vector-set! v 0 99)\nv",
        "practice": ["创建 vector 并读取元素。", "比较 list-ref 和 vector-ref。", "说明 vector-set! 的副作用。"],
        "assignment": "实现一个简单棋盘 vector 表示，并提供读取/更新函数。",
    },
    {
        "category": "Day 28 - Hash Tables",
        "title": "hash：键值映射",
        "goal": "使用 hash 表示查找表和配置。",
        "cpp_bridge": "类似 C++ unordered_map。",
        "explanation": "hash 适合通过 key 快速取值。Racket 提供不可变和可变 hash；初学阶段优先不可变版本。",
        "racket_focus": ["hash", "hash-ref", "hash-set", "hash-has-key?"],
        "code": "#lang racket\n\n(define scores (hash \"Ada\" 95 \"Grace\" 88))\n(hash-ref scores \"Ada\")\n(hash-set scores \"Linus\" 91)\n(hash-has-key? scores \"Grace\")",
        "practice": ["建立一个课程配置 hash。", "读取不存在 key 并提供默认值。", "用 hash-set 产生新 hash。"],
        "assignment": "写一个单词频率统计器，返回 hash。",
    },
    {
        "category": "Day 29 - File I/O",
        "title": "文件读取和写入",
        "goal": "读取文本文件、处理内容、写出结果。",
        "cpp_bridge": "类似 C++ ifstream/ofstream，但 Racket 有更直接的 read/write helpers。",
        "explanation": "很多真实程序都从文件开始。今天关注文本文件：读取字符串，分析，写出报告。",
        "racket_focus": ["file->string", "call-with-output-file", "displayln", "路径"],
        "code": "#lang racket\n\n(define text (file->string \"input.txt\"))\n(define words (string-split text))\n\n(call-with-output-file \"report.txt\"\n  (lambda (out)\n    (displayln (length words) out))\n  #:exists 'replace)",
        "practice": ["读取一个 txt 文件。", "统计行数和单词数。", "写出 report.txt。"],
        "assignment": "完成文件版文本分析器：读 input.txt，写 report.txt。",
    },
    {
        "category": "Day 30 - Command Line Arguments",
        "title": "命令行程序",
        "goal": "使用 command-line 创建可传参脚本。",
        "cpp_bridge": "类似 C++ main(int argc, char** argv)。",
        "explanation": "脚本能从命令行接收参数后，就能变成真正工具。Racket 的 command-line 提供声明式参数解析。",
        "racket_focus": ["command-line", "flags", "positional args", "脚本化"],
        "code": "#lang racket\n\n(define verbose? (make-parameter #f))\n\n(command-line\n #:once-each\n [(\"-v\" \"--verbose\") \"Show details\" (verbose? #t)]\n #:args (filename)\n (when (verbose?) (displayln \"Verbose mode\"))\n (displayln filename))",
        "practice": ["写一个接收文件名的脚本。", "增加 --verbose 参数。", "处理缺少参数的情况。"],
        "assignment": "把文件版文本分析器改成命令行工具。",
    },
    {
        "category": "Day 31 - Review Project 3",
        "title": "命令行文本工具",
        "goal": "整合 hash、文件 I/O、命令行参数和测试。",
        "cpp_bridge": "这类似实现一个小型 wc/grep 风格工具。",
        "explanation": "今天做一个可运行工具，而不是零散函数。你要考虑输入、输出、错误信息和模块拆分。",
        "racket_focus": ["CLI project", "I/O", "hash frequency", "测试"],
        "code": "#lang racket\n\n(define (word-count text)\n  (length (string-split text)))\n\n(module+ main\n  (command-line\n   #:args (filename)\n   (displayln (word-count (file->string filename)))))",
        "practice": ["支持统计单词数。", "支持最高频单词。", "支持输出到文件。"],
        "assignment": "完成一个 `rkt-text` 命令行工具，支持 --top、--out 和文件输入。",
    },
    {
        "category": "Day 32 - Mutable State",
        "title": "set! 和可变状态",
        "goal": "理解何时使用状态，以及状态带来的复杂度。",
        "cpp_bridge": "C++ 默认大量使用赋值；Racket 可以用 set!，但通常要先考虑纯函数方案。",
        "explanation": "状态不是禁止使用，而是要有理由使用。今天你会看到同一个计数器可以用闭包和 set! 实现。",
        "racket_focus": ["set!", "mutable variables", "副作用", "状态封装"],
        "code": "#lang racket\n\n(define counter\n  (let ([n 0])\n    (lambda ()\n      (set! n (+ n 1))\n      n)))\n\n(counter)\n(counter)",
        "practice": ["写一个计数器。", "说明 set! 修改的是哪个绑定。", "改写成纯函数版本。"],
        "assignment": "实现一个带状态的 quiz scorer，并说明它和纯函数版本的取舍。",
    },
    {
        "category": "Day 33 - Boxes and Mutable Structs",
        "title": "box 和可变结构",
        "goal": "学习 Racket 中显式可变容器。",
        "cpp_bridge": "box 类似一个单槽可变对象；mutable struct 更接近可修改字段的 C++ object。",
        "explanation": "Racket 把可变性标得很明显：set-box!、set-struct-field! 这类名字都带感叹号。感叹号通常表示副作用。",
        "racket_focus": ["box", "unbox", "set-box!", "mutable struct", "! 命名"],
        "code": "#lang racket\n\n(define b (box 10))\n(unbox b)\n(set-box! b 20)\n(unbox b)\n\n(struct player (name [score #:mutable]) #:transparent)",
        "practice": ["用 box 保存当前分数。", "定义 mutable player。", "比较可变和不可变设计。"],
        "assignment": "实现一个小游戏分数模型，分别用纯函数和 mutable struct 写。",
    },
    {
        "category": "Day 34 - Closures",
        "title": "闭包：函数记住环境",
        "goal": "理解函数如何捕获外部绑定。",
        "cpp_bridge": "C++ lambda 可以 capture；Racket 闭包是函数式编程核心工具。",
        "explanation": "闭包让你生成带配置的函数。它也是封装状态、实现工厂函数和回调的基础。",
        "racket_focus": ["closure", "function factory", "captured environment", "封装"],
        "code": "#lang racket\n\n(define (make-adder n)\n  (lambda (x) (+ x n)))\n\n(define add10 (make-adder 10))\n(add10 5)",
        "practice": ["写 make-multiplier。", "写 make-threshold-filter。", "解释被捕获的变量。"],
        "assignment": "实现一个 `make-grader`，根据传入标准生成成绩判断函数。",
    },
    {
        "category": "Day 35 - Continuation of Design",
        "title": "设计大型函数：分解和组合",
        "goal": "把复杂需求拆成小函数管线。",
        "cpp_bridge": "C++ 项目也需要分层；Racket 中函数组合会让数据流更直接。",
        "explanation": "当函数超过一屏，通常说明你没有拆分好。今天练习从需求中提取 helper，并让每个 helper 易测试。",
        "racket_focus": ["helper functions", "composition", "pipeline thinking", "可测试性"],
        "code": "#lang racket\n\n(define (clean-word w)\n  (string-downcase (string-trim w)))\n\n(define (clean-words text)\n  (map clean-word (string-split text)))",
        "practice": ["把一个长函数拆成 4 个 helper。", "为每个 helper 写测试。", "画出数据流。"],
        "assignment": "重构你的文本工具，让核心逻辑没有 I/O，I/O 只在边界。",
    },
    {
        "category": "Day 36 - Typed Racket Intro",
        "title": "Typed Racket：给 Racket 加类型",
        "goal": "了解 Typed Racket 的基本写法。",
        "cpp_bridge": "你熟悉 C++ 静态类型；Typed Racket 让你在 Racket 中逐步引入类型检查。",
        "explanation": "Typed Racket 不是必须，但对有 C++ 背景的人很有帮助。你会看到函数类型标注如何表达输入输出。",
        "racket_focus": ["#lang typed/racket", ": type annotation", "Listof", "类型错误"],
        "code": "#lang typed/racket\n\n(: add1-safe (Integer -> Integer))\n(define (add1-safe x)\n  (+ x 1))\n\n(: total ((Listof Integer) -> Integer))\n(define (total xs)\n  (foldl + 0 xs))",
        "practice": ["给 3 个简单函数加类型。", "故意制造类型错误。", "比较 typed/racket 和 racket。"],
        "assignment": "把 Day 10 的 sum/count 改写为 Typed Racket。",
    },
    {
        "category": "Day 37 - More Typed Racket",
        "title": "结构、联合和可选值类型",
        "goal": "用类型描述更复杂的数据。",
        "cpp_bridge": "类似 C++ struct、std::optional 和 variant 的概念。",
        "explanation": "类型能帮助你明确数据形状。今天关注 struct 类型、U 联合类型和 Maybe 风格设计。",
        "racket_focus": ["typed struct", "U", "Option style", "类型驱动设计"],
        "code": "#lang typed/racket\n\n(struct Student ([name : String] [score : Integer]) #:transparent)\n\n(: letter-grade (Integer -> String))\n(define (letter-grade score)\n  (cond [(>= score 90) \"A\"] [else \"Keep going\"]))",
        "practice": ["定义 typed struct。", "写返回 (U String False) 的查找函数。", "处理可选结果。"],
        "assignment": "用 Typed Racket 重写学生成绩系统核心模型。",
    },
    {
        "category": "Day 38 - Macros Concept",
        "title": "宏的概念：扩展语言",
        "goal": "理解宏解决的是什么问题，不急着写复杂宏。",
        "cpp_bridge": "C++ macro 是文本替换；Racket macro 是语法对象转换，安全且结构化。",
        "explanation": "宏让你创造新的语法模式。今天重点是概念：宏运行在编译/展开阶段，输入输出都是语法结构。",
        "racket_focus": ["macro", "syntax transformation", "define-syntax-rule", "展开阶段"],
        "code": "#lang racket\n\n(define-syntax-rule (when-positive x body ...)\n  (when (> x 0)\n    body ...))\n\n(when-positive 5\n  (displayln \"positive\"))",
        "practice": ["写一个 unless 宏。", "用 macro stepper 观察展开。", "说明宏和函数区别。"],
        "assignment": "实现 2 个简单 define-syntax-rule 宏，并解释展开后的形状。",
    },
    {
        "category": "Day 39 - Syntax Rules",
        "title": "syntax-rules：模式匹配式宏",
        "goal": "用 syntax-rules 写稍复杂的宏。",
        "cpp_bridge": "这比 C++ 预处理器更像对 AST 模式做转换。",
        "explanation": "syntax-rules 通过模式和模板工作。你要把它看作结构化替换，而不是字符串替换。",
        "racket_focus": ["syntax-rules", "macro patterns", "templates", "ellipsis"],
        "code": "#lang racket\n\n(define-syntax my-and\n  (syntax-rules ()\n    [(my-and) #t]\n    [(my-and x) x]\n    [(my-and x y ...)\n     (if x (my-and y ...) #f)]))",
        "practice": ["阅读 my-and 展开逻辑。", "写 my-or 的简化版本。", "解释 ellipsis 的作用。"],
        "assignment": "实现一个 `check-range` 宏，让范围检查语法更简洁。",
    },
    {
        "category": "Day 40 - Mini Languages",
        "title": "小语言思维：DSL 入门",
        "goal": "理解 Racket 为什么适合做语言扩展。",
        "cpp_bridge": "C++ 可以建库；Racket 不仅能建库，还能塑造调用语法。",
        "explanation": "DSL 是为特定问题设计的小语言。你可以先用普通数据结构解释命令，再考虑宏语法。",
        "racket_focus": ["DSL", "interpreter", "commands as data", "language-oriented programming"],
        "code": "#lang racket\n\n(define program\n  '((say \"hello\")\n    (add 1 2)))\n\n(define (run command)\n  (match command\n    [`(say ,msg) msg]\n    [`(add ,a ,b) (+ a b)]))",
        "practice": ["设计 5 条命令。", "用 match 解释命令。", "区分数据 DSL 和宏 DSL。"],
        "assignment": "设计一个 mini quiz DSL，并实现解释器。",
    },
    {
        "category": "Day 41 - Interpreters 1",
        "title": "解释器入门：表达式求值",
        "goal": "写一个能计算数字和加法的小解释器。",
        "cpp_bridge": "类似写一个 AST evaluator；Racket 的 match 让它非常简洁。",
        "explanation": "解释器是理解语言的最佳项目。今天只处理最小表达式：数字、加法、乘法。",
        "racket_focus": ["AST", "eval function", "recursive evaluator", "match"],
        "code": "#lang racket\n\n(define (eval-expr e)\n  (match e\n    [(? number?) e]\n    [`(+ ,a ,b) (+ (eval-expr a) (eval-expr b))]\n    [`(* ,a ,b) (* (eval-expr a) (eval-expr b))]))\n\n(eval-expr '(+ 1 (* 2 3)))",
        "practice": ["增加减法。", "增加除法并处理除 0。", "画出 AST。"],
        "assignment": "实现支持 + - * / 的表达式解释器，并写测试。",
    },
    {
        "category": "Day 42 - Interpreters 2",
        "title": "变量和环境",
        "goal": "为解释器加入变量查找。",
        "cpp_bridge": "环境类似符号表 unordered_map。",
        "explanation": "变量求值需要环境。环境把名字映射到值，解释器遇到符号时从环境中查找。",
        "racket_focus": ["environment", "symbol lookup", "hash env", "错误处理"],
        "code": "#lang racket\n\n(define (eval-expr e env)\n  (match e\n    [(? number?) e]\n    [(? symbol?) (hash-ref env e)]\n    [`(+ ,a ,b) (+ (eval-expr a env) (eval-expr b env))]))\n\n(eval-expr '(+ x 3) (hash 'x 10))",
        "practice": ["增加变量查找默认错误。", "支持多个变量。", "写测试覆盖未知变量。"],
        "assignment": "给解释器加入变量、环境和清晰错误信息。",
    },
    {
        "category": "Day 43 - Interpreters 3",
        "title": "let 表达式和作用域",
        "goal": "解释 let，并理解词法作用域。",
        "cpp_bridge": "类似局部变量作用域，但在解释器中你要显式构造新环境。",
        "explanation": "let 的关键是先计算绑定值，再在扩展后的环境中计算主体。旧环境不能被破坏。",
        "racket_focus": ["let semantics", "lexical scope", "environment extension", "shadowing"],
        "code": "#lang racket\n\n(define (extend env name value)\n  (hash-set env name value))\n\n; `(let ([x 10]) (+ x 2))` 可以设计为 '(let x 10 (+ x 2))",
        "practice": ["设计 let 的 AST 表示。", "实现环境扩展。", "测试变量遮蔽。"],
        "assignment": "解释器支持 `(let name value body)`，并写 6 个测试。",
    },
    {
        "category": "Day 44 - Interpreters 4",
        "title": "函数和调用",
        "goal": "让解释器支持一参数函数。",
        "cpp_bridge": "类似把函数定义、参数绑定和调用栈显式建模。",
        "explanation": "函数值需要保存参数名、函数体和定义时环境。调用时把实参绑定到参数名，然后求函数体。",
        "racket_focus": ["function values", "closure in interpreter", "application", "scope"],
        "code": "#lang racket\n\n(struct closure (param body env) #:transparent)\n\n; 设计表达式：'(fun x (+ x 1)) 和 '(call f 10)\n; 今天重点是模型，完整实现作为作业。",
        "practice": ["设计 closure struct。", "解释为什么要保存 env。", "手工模拟一次函数调用。"],
        "assignment": "扩展解释器，支持 fun 和 call，至少支持一参数函数。",
    },
    {
        "category": "Day 45 - Review Project 4",
        "title": "完成小解释器",
        "goal": "整合表达式、变量、let 和函数。",
        "cpp_bridge": "这是一个小型语言运行时项目，能体现 Racket 的优势。",
        "explanation": "今天专注项目完成度：错误信息、测试、模块组织和 README。解释器项目最能证明你理解了递归数据和环境。",
        "racket_focus": ["interpreter project", "closures", "tests", "documentation"],
        "code": "#lang racket\n\n; Project skeleton:\n; ast.rkt       data definitions\n; eval.rkt      evaluator\n; tests.rkt     rackunit tests\n; main.rkt      examples",
        "practice": ["整理模块。", "补测试。", "写 README 示例。"],
        "assignment": "提交完整 mini interpreter 项目，包含至少 20 个测试。",
    },
    {
        "category": "Day 46 - GUI with racket/gui",
        "title": "GUI 入门：窗口、按钮和回调",
        "goal": "了解 Racket 可以写桌面 GUI。",
        "cpp_bridge": "类似使用 Qt/wxWidgets，但 Racket 回调配合闭包很自然。",
        "explanation": "GUI 编程会引入事件驱动思维。你写好控件和回调，用户操作触发函数。",
        "racket_focus": ["racket/gui", "frame%", "button%", "callbacks"],
        "code": "#lang racket/gui\n\n(define frame (new frame% [label \"Hello Racket\"] [width 300] [height 120]))\n(new button% [parent frame]\n     [label \"Click\"]\n     [callback (lambda (button event) (displayln \"clicked\"))])\n(send frame show #t)",
        "practice": ["创建窗口。", "添加按钮。", "按钮点击时改变 message。"],
        "assignment": "做一个小 GUI：输入分数，点击按钮显示等级。",
    },
    {
        "category": "Day 47 - Web Server Basics",
        "title": "Racket Web Server 入门",
        "goal": "了解用 Racket 写简单网页响应。",
        "cpp_bridge": "类似写 HTTP handler，但 Racket 用 xexpr 表示 HTML 很方便。",
        "explanation": "Racket 的 web-server 库可以直接生成页面。今天只做简单响应，理解 request -> response。",
        "racket_focus": ["web-server/servlet", "xexpr", "response", "serve/servlet"],
        "code": "#lang racket\n(require web-server/servlet\n         web-server/servlet-env)\n\n(define (start req)\n  '(html (body (h1 \"Hello from Racket\"))))\n\n(serve/servlet start #:servlet-regexp #rx\"\")",
        "practice": ["返回一个 h1 页面。", "加入列表。", "显示当前时间或固定数据。"],
        "assignment": "写一个 Racket web 页面，展示你的 5 个学习目标。",
    },
    {
        "category": "Day 48 - Web Forms",
        "title": "表单和用户输入",
        "goal": "处理网页表单提交。",
        "cpp_bridge": "类似服务端读取 HTTP 参数。",
        "explanation": "Web 程序核心是接收输入、验证、返回结果。Racket 可以用 request bindings 读取表单值。",
        "racket_focus": ["forms", "bindings", "request data", "validation"],
        "code": "#lang racket\n\n; 今日建议阅读 web-server 文档中的 request bindings。\n; 作业可先用固定页面模拟输入处理，再逐步完善。",
        "practice": ["设计一个输入分数的表单。", "验证空输入。", "返回计算结果页面。"],
        "assignment": "做一个网页成绩计算器：输入名字和分数，返回等级。",
    },
    {
        "category": "Day 49 - Web Project Planning",
        "title": "Racket Web 小项目规划",
        "goal": "规划一个可完成的 Racket web app。",
        "cpp_bridge": "像 C++ 项目前的模块设计和接口设计。",
        "explanation": "项目先定范围。你要写出数据模型、页面、核心函数、测试和运行方式。",
        "racket_focus": ["project scope", "data model", "routes", "test plan"],
        "code": "#lang racket\n\n(struct task (id title done?) #:transparent)\n\n; Plan:\n; /           list tasks\n; /add        add task\n; /toggle     mark done",
        "practice": ["写项目需求。", "列出 3 个页面。", "设计 struct。"],
        "assignment": "提交 Racket web todo app 的设计文档和数据模型代码。",
    },
    {
        "category": "Day 50 - Web Project Build",
        "title": "实现 Web Todo 核心",
        "goal": "完成 web todo 的核心数据和页面。",
        "cpp_bridge": "把模型和视图分开，类似 MVC 的基础思想。",
        "explanation": "今天重点写代码，不追求完美 UI。先让核心流程跑通：展示、添加、标记完成。",
        "racket_focus": ["state model", "rendering", "handlers", "small app"],
        "code": "#lang racket\n\n(struct task (id title done?) #:transparent)\n\n(define (toggle-task t)\n  (task (task-id t) (task-title t) (not (task-done? t))))",
        "practice": ["实现 add-task。", "实现 toggle-task。", "渲染任务列表。"],
        "assignment": "完成 web todo app 的最小可用版本。",
    },
    {
        "category": "Day 51 - Performance and Big-O",
        "title": "性能直觉和复杂度",
        "goal": "理解 list/vector/hash 操作复杂度。",
        "cpp_bridge": "你熟悉 vector、list、unordered_map 的复杂度；Racket 也需要根据数据结构选择算法。",
        "explanation": "函数式代码不等于不用考虑性能。今天建立基本判断：什么时候 list 很好，什么时候 hash/vector 更合适。",
        "racket_focus": ["Big-O", "list traversal", "vector access", "hash lookup"],
        "code": "#lang racket\n\n; list-ref is O(n)\n; vector-ref is O(1)\n; hash-ref is expected O(1)\n\n(define xs (build-list 1000 values))\n(list-ref xs 999)",
        "practice": ["分析 5 个函数复杂度。", "比较 list-ref 和 vector-ref。", "找出重复遍历。"],
        "assignment": "为你的文本工具写一页性能分析，指出至少 3 个可优化点。",
    },
    {
        "category": "Day 52 - Debugging",
        "title": "调试 Racket 程序",
        "goal": "使用错误信息、displayln、trace 和测试定位问题。",
        "cpp_bridge": "类似 C++ debugger/logging，但 Racket 表达式更适合小步验证。",
        "explanation": "调试不是乱改代码。先复现，再缩小范围，再写测试锁定，再修复。",
        "racket_focus": ["error reading", "displayln", "trace", "minimal examples"],
        "code": "#lang racket\n(require racket/trace)\n\n(define (fact n)\n  (if (= n 0) 1 (* n (fact (- n 1)))))\n\n(trace fact)\n(fact 4)",
        "practice": ["阅读一个错误堆栈。", "给递归函数加 trace。", "构造最小复现。"],
        "assignment": "提交一个 bug 修复报告：问题、复现、原因、修复、测试。",
    },
    {
        "category": "Day 53 - Style and Idioms",
        "title": "Racket 风格：写得像 Racket",
        "goal": "改进命名、函数大小、缩进和惯用写法。",
        "cpp_bridge": "从 C++ 风格迁移到 Racket 风格，重点是表达式、不可变和组合。",
        "explanation": "能运行只是第一步。Racket 代码应该函数短、数据流清晰、命名带语义、谓词用问号、副作用用感叹号。",
        "racket_focus": ["naming", "indentation", "predicate ?", "mutation !", "small functions"],
        "code": "#lang racket\n\n(define (passing-score? score)\n  (>= score 60))\n\n(define (normalize-name name)\n  (string-titlecase (string-trim name)))",
        "practice": ["重命名 5 个函数。", "拆分长函数。", "检查 ? 和 ! 命名。"],
        "assignment": "选一个旧作业重构，提交前后对比和说明。",
    },
    {
        "category": "Day 54 - Capstone Planning",
        "title": "结课项目规划",
        "goal": "确定最终项目范围和验收标准。",
        "cpp_bridge": "像做课程设计：需求、模块、测试、里程碑。",
        "explanation": "最终项目应该展示你两个月的能力：数据建模、递归/高阶函数、I/O 或 web、测试和文档。",
        "racket_focus": ["capstone scope", "milestones", "rubric", "risk control"],
        "code": "#lang racket\n\n; Capstone options:\n; 1. Mini interpreter\n; 2. Text analysis CLI\n; 3. Web todo/quiz app\n; 4. Typed Racket grade system",
        "practice": ["选择项目主题。", "写 5 条验收标准。", "列出模块和测试计划。"],
        "assignment": "提交 capstone proposal，包含目标、功能、数据模型、测试计划和时间安排。",
    },
    {
        "category": "Day 55 - Capstone Build",
        "title": "结课项目实现日",
        "goal": "完成核心功能并补测试。",
        "cpp_bridge": "类似项目冲刺：优先完成主路径，再处理边界。",
        "explanation": "今天只做最关键的功能。不要边做边扩大范围。确保项目能运行、能测试、能展示。",
        "racket_focus": ["implementation", "tests", "integration", "scope discipline"],
        "code": "#lang racket\n\n; Keep a module+ test section close to core logic:\n(module+ test\n  (require rackunit)\n  (check-true #t))",
        "practice": ["完成主流程。", "补 10 个测试。", "写运行说明。"],
        "assignment": "提交 capstone 初版：代码可运行，README 可跟随，测试能通过。",
    },
    {
        "category": "Day 56 - Capstone Review and Next Steps",
        "title": "最终复盘：从学习者到能独立写 Racket",
        "goal": "复盘两个月内容，完成项目展示和后续学习路线。",
        "cpp_bridge": "你现在应能把 C++ 的算法/数据结构经验迁移到 Racket 的函数式和语言构造思维中。",
        "explanation": "最后一天关注质量：代码清晰度、测试、文档、可维护性和下一阶段目标。把项目当成作品整理。",
        "racket_focus": ["review", "presentation", "code quality", "next roadmap"],
        "code": "#lang racket\n\n; Final checklist:\n; - runs from README\n; - tests pass\n; - functions are small\n; - errors are clear\n; - project scope is documented",
        "practice": ["跑完整测试。", "让别人按 README 运行。", "写学习复盘。"],
        "assignment": "提交最终 capstone、演示说明和一页复盘：最难概念、最大收获、下一步计划。",
    },
]


DOCS = {
    "docs_index": {
        "title": "Racket Documentation",
        "url": "https://docs.racket-lang.org/index.html",
    },
    "guide": {
        "title": "The Racket Guide",
        "url": "https://docs.racket-lang.org/guide/index.html",
    },
    "syntax": {
        "title": "Simple Definitions and Expressions",
        "url": "https://docs.racket-lang.org/guide/syntax-overview.html",
    },
    "lambda": {
        "title": "Functions: lambda",
        "url": "https://docs.racket-lang.org/guide/lambda.html",
    },
    "conditionals": {
        "title": "Conditionals",
        "url": "https://docs.racket-lang.org/guide/conditionals.html",
    },
    "let": {
        "title": "Local Binding",
        "url": "https://docs.racket-lang.org/guide/let.html",
    },
    "lists": {
        "title": "Pairs and Lists",
        "url": "https://docs.racket-lang.org/guide/pairs.html",
    },
    "quote": {
        "title": "Quoting",
        "url": "https://docs.racket-lang.org/guide/quote.html",
    },
    "struct": {
        "title": "Programmer-Defined Datatypes",
        "url": "https://docs.racket-lang.org/guide/define-struct.html",
    },
    "modules": {
        "title": "Modules",
        "url": "https://docs.racket-lang.org/guide/modules.html",
    },
    "contracts": {
        "title": "Contracts and Boundaries",
        "url": "https://docs.racket-lang.org/guide/contract-boundaries.html",
    },
    "vectors": {
        "title": "Vectors",
        "url": "https://docs.racket-lang.org/guide/vectors.html",
    },
    "hash": {
        "title": "Hash Tables",
        "url": "https://docs.racket-lang.org/guide/hash-tables.html",
    },
    "match": {
        "title": "Pattern Matching",
        "url": "https://docs.racket-lang.org/guide/match.html",
    },
    "macros": {
        "title": "Macros",
        "url": "https://docs.racket-lang.org/guide/macros.html",
    },
    "pattern_macros": {
        "title": "Pattern-Based Macros",
        "url": "https://docs.racket-lang.org/guide/pattern-macros.html",
    },
    "io": {
        "title": "Input and Output",
        "url": "https://docs.racket-lang.org/reference/input-and-output.html",
    },
    "classes": {
        "title": "Classes and Objects",
        "url": "https://docs.racket-lang.org/guide/classes.html",
    },
    "gui": {
        "title": "Racket GUI Windowing",
        "url": "https://docs.racket-lang.org/gui/windowing-overview.html",
    },
}


BRIDGE_TEMPLATES = {
    "expressions": {
        "concept": "表达式求值：从语句序列转成“每个括号都产生值”",
        "cpp": """int total = 1 + 2 + 3;
std::cout << total << std::endl;""",
        "racket": """#lang racket

(define total (+ 1 2 3))
(displayln total)""",
        "translation_steps": [
            "先找出 C++ 里真正产生值的部分，例如 `1 + 2 + 3`。",
            "把中缀运算改成前缀调用：`(+ 1 2 3)`。",
            "用 `define` 给结果命名；需要输出时再用 `displayln`。",
        ],
        "pitfalls": [
            "不要把每一行都想成会修改机器状态；先问这个表达式产生什么值。",
            "Racket 函数调用统一写成 `(函数 参数 ...)`，包括 `+`、`*` 这种运算符。",
        ],
        "drill": "把 `int area = width * height;`、`double avg = sum / count;` 各改写成 Racket。",
        "docs": ["syntax", "guide"],
    },
    "prefix": {
        "concept": "函数调用统一语法：C++ 的 f(x, y) 和 x + y 在 Racket 都是前缀调用",
        "cpp": """int x = (2 + 3) * (10 - 4);
int y = std::max(3, 9);""",
        "racket": """#lang racket

(define x (* (+ 2 3) (- 10 4)))
(define y (max 3 9))""",
        "translation_steps": [
            "先给 C++ 表达式加上完整括号，确认优先级。",
            "把最里面的运算改成 `(operator arg ...)`。",
            "从内向外重写，直到最外层也变成一个函数调用。",
        ],
        "pitfalls": [
            "Racket 里 `(+ 1 2)` 的第一个位置必须是函数或语法形式。",
            "`(1 + 2)` 会被理解成“调用 1 这个函数”，这是典型初学错误。",
        ],
        "drill": "把 `a + b * c - d` 改写成不丢失优先级的 Racket 表达式。",
        "docs": ["syntax", "lambda"],
    },
    "types": {
        "concept": "类型检查位置变化：从声明变量类型转成用谓词检查值",
        "cpp": """int score = 95;
std::string name = "Ada";
bool passing = score >= 60;""",
        "racket": """#lang racket

(define score 95)
(define name "Ada")
(define passing? (>= score 60))

(number? score)
(string? name)
(boolean? passing?)""",
        "translation_steps": [
            "删掉变量声明中的类型名，把值直接绑定给名字。",
            "需要验证类型时，用 `number?`、`string?`、`boolean?` 这类谓词。",
            "谓词函数名通常以 `?` 结尾，你自己的判断函数也应该遵守这个习惯。",
        ],
        "pitfalls": [
            "动态类型不是没有类型；错误会在函数收到不合适的值时出现。",
            "不要把 `bool passing` 直译成 `passing`，Racket 风格更常写 `passing?`。",
        ],
        "drill": "写 `valid-score?`，先检查是 number，再检查范围是 0 到 100。",
        "docs": ["syntax", "conditionals"],
    },
    "define_function": {
        "concept": "函数定义：从返回类型 + 参数类型，变成名字 + 参数列表 + 表达式主体",
        "cpp": """double addTax(double amount) {
    return amount * 1.13;
}""",
        "racket": """#lang racket

(define (add-tax amount)
  (* amount 1.13))""",
        "translation_steps": [
            "删除返回类型和参数类型，保留函数名和参数名。",
            "把函数名和参数放进 `define` 的左侧：`(define (name arg ...) body)`。",
            "把 `return expr;` 改成函数体最后一个表达式；Racket 自动返回它的值。",
        ],
        "pitfalls": [
            "Racket 函数体不需要 `return`。",
            "函数名推荐用 kebab-case，例如 `add-tax`，不要沿用 C++ 的 camelCase。",
        ],
        "drill": "把 `int square(int x) { return x * x; }` 改写成 Racket。",
        "docs": ["syntax", "lambda"],
    },
    "conditionals": {
        "concept": "条件是表达式：if/cond 直接产生值，不靠修改外部变量",
        "cpp": """std::string grade;
if (score >= 90) {
    grade = "A";
} else if (score >= 80) {
    grade = "B";
} else {
    grade = "Practice";
}""",
        "racket": """#lang racket

(define grade
  (cond
    [(>= score 90) "A"]
    [(>= score 80) "B"]
    [else "Practice"]))""",
        "translation_steps": [
            "先找出每个分支最终想得到的值。",
            "把 `else if` 链改成 `cond` 的多个 clause。",
            "把赋值目标挪到整个 `cond` 外面：`(define grade (cond ...))`。",
        ],
        "pitfalls": [
            "Racket 的 `if` 必须有 then 和 else 两个结果。",
            "除了 `#f`，其他值都被当成 true；不要把 C++ 的 0/非 0 规则照搬过来。",
        ],
        "drill": "把一个 C++ if/else 分数判断改成返回字符串的 Racket `cond`。",
        "docs": ["conditionals", "syntax"],
    },
    "let": {
        "concept": "局部变量：从 block scope 转成 let 绑定",
        "cpp": """double total(double price) {
    double tax = price * 0.13;
    double tip = price * 0.18;
    return price + tax + tip;
}""",
        "racket": """#lang racket

(define (total price)
  (let ([tax (* price 0.13)]
        [tip (* price 0.18)])
    (+ price tax tip)))""",
        "translation_steps": [
            "把只在函数内部使用的临时变量放入 `let`。",
            "每个绑定写成 `[name expr]`。",
            "`let` 的 body 写最终结果表达式。",
        ],
        "pitfalls": [
            "`let` 是并行绑定；后一个绑定默认看不到前一个绑定。需要顺序依赖时用 `let*`。",
            "不要为了保存中间结果使用 `set!`，优先用局部绑定。",
        ],
        "drill": "把有 3 个局部变量的 C++ 面积/税费函数改成 `let`。",
        "docs": ["let", "syntax"],
    },
    "lists_recursion": {
        "concept": "遍历：从 for 循环扫描 vector，转成 empty/first/rest 的结构递归",
        "cpp": """int sum(const std::vector<int>& nums) {
    int acc = 0;
    for (int n : nums) {
        acc += n;
    }
    return acc;
}""",
        "racket": """#lang racket

(define (sum nums)
  (cond
    [(empty? nums) 0]
    [else (+ (first nums)
             (sum (rest nums)))]))""",
        "translation_steps": [
            "把循环的“没有元素了”改成递归的 base case。",
            "把当前元素写成 `(first nums)`，剩余元素写成 `(rest nums)`。",
            "不要修改 accumulator；先写结构递归版本，再学习尾递归 accumulator。",
        ],
        "pitfalls": [
            "Racket list 不是 C++ vector；不要频繁用索引访问 list。",
            "递归分支必须让问题变小，通常是递归处理 `(rest nums)`。",
        ],
        "drill": "把 `countEven(vector<int>)` 改写成递归处理 Racket list 的函数。",
        "docs": ["lists", "conditionals"],
    },
    "strings": {
        "concept": "字符串处理：从索引循环转成字符串函数和字符列表处理",
        "cpp": """bool startsWithA(const std::string& s) {
    return !s.empty() && s[0] == 'A';
}""",
        "racket": """#lang racket

(define (starts-with-a? s)
  (and (non-empty-string? s)
       (char=? (string-ref s 0) #\\A)))""",
        "translation_steps": [
            "先检查空字符串，避免越界。",
            "用 `string-ref` 取字符，用 `char=?` 比较字符。",
            "如果要逐字符转换，可以先用 `string->list`。",
        ],
        "pitfalls": [
            "Racket 字符写作 `#\\A`，字符串写作 `\"A\"`，不要混用。",
            "字符串可索引，但复杂遍历常转成列表再用 map/filter。",
        ],
        "drill": "写 `has-space?`，判断字符串是否包含空格字符。",
        "docs": ["syntax", "lists"],
    },
    "structs": {
        "concept": "数据建模：从 C++ struct/class 字段，转成 Racket struct 和访问器",
        "cpp": """struct Student {
    std::string name;
    int score;
};""",
        "racket": """#lang racket

(struct student (name score) #:transparent)

(define ada (student "Ada" 95))
(student-name ada)
(student-score ada)""",
        "translation_steps": [
            "把类型名改成 Racket 风格的小写名字。",
            "字段列表放在 struct 后面：`(struct student (name score))`。",
            "使用自动生成的构造器、谓词和访问器。",
        ],
        "pitfalls": [
            "初学阶段加 `#:transparent`，方便打印和测试。",
            "不要马上模拟 C++ class 的 setter；优先用不可变数据和返回新值。",
        ],
        "drill": "把一个 C++ `Book` struct 改成 Racket `book` struct，并写 `expensive?`。",
        "docs": ["struct", "match"],
    },
    "higher_order": {
        "concept": "算法抽象：从 STL algorithm/lambda，转成 map/filter/fold",
        "cpp": """std::vector<int> out;
std::copy_if(nums.begin(), nums.end(), std::back_inserter(out),
             [](int n) { return n % 2 == 0; });""",
        "racket": """#lang racket

(define out
  (filter even? nums))""",
        "translation_steps": [
            "先识别循环目的：转换用 `map`，筛选用 `filter`，汇总用 `foldl`/`foldr`。",
            "把循环体中变化的判断或计算提成函数。",
            "让高阶函数负责遍历，你只写元素级逻辑。",
        ],
        "pitfalls": [
            "不要在 `map` 里靠副作用构造结果；`map` 本身会返回新列表。",
            "`foldl` 的初始值要代表空输入时的答案。",
        ],
        "drill": "把一个 C++ for 循环筛选正数的代码改成 Racket `filter`。",
        "docs": ["lambda", "lists"],
    },
    "immutability": {
        "concept": "更新数据：从原地修改，转成构造新值",
        "cpp": """nums.insert(nums.begin(), 0);
student.score = 100;""",
        "racket": """#lang racket

(define nums2 (cons 0 nums))
(struct student (name score) #:transparent)
(define improved (student (student-name s) 100))""",
        "translation_steps": [
            "先明确旧值是否还需要保留；函数式代码通常保留旧值。",
            "list 头部添加用 `cons`，结构更新通常构造一个新 struct。",
            "把“修改动作”改写成“返回更新后的值”。",
        ],
        "pitfalls": [
            "带 `!` 的函数通常有副作用，初学时先少用。",
            "不要为了像 C++ 一样方便就过早引入 mutable struct。",
        ],
        "drill": "写 `complete-task`，输入一个 task，返回 done? 为 #t 的新 task。",
        "docs": ["lists", "struct"],
    },
    "tests_modules": {
        "concept": "工程组织：从 header/source/test 分离，转成 provide/require/module+ test",
        "cpp": """// math_utils.h
int square(int x);

// math_utils.cpp
int square(int x) { return x * x; }""",
        "racket": """#lang racket

(provide square)

(define (square x)
  (* x x))

(module+ test
  (require rackunit)
  (check-equal? (square 4) 16))""",
        "translation_steps": [
            "一个 `.rkt` 文件天然是模块。",
            "用 `provide` 明确导出，用 `require` 导入其他模块。",
            "测试可以放在 `module+ test` 或单独测试文件里。",
        ],
        "pitfalls": [
            "不要把所有文件互相 require，先设计清楚导出边界。",
            "模块边界是 contracts 和测试最自然的位置。",
        ],
        "drill": "把一个单文件作业拆成 `model.rkt`、`logic.rkt`、`tests.rkt`。",
        "docs": ["modules", "contracts"],
    },
    "match_symbols": {
        "concept": "数据驱动分支：从 enum/switch 或 if 链，转成 quote + match",
        "cpp": """enum class Command { Add, Done, List };
switch (cmd) {
    case Command::Add: return "add";
    case Command::List: return "list";
}""",
        "racket": """#lang racket

(define (run cmd)
  (match cmd
    [`(add ,title) (string-append "add " title)]
    ['(list) "list"]
    [_ "unknown"]))""",
        "translation_steps": [
            "把命令表示成符号或 S-expression，例如 `'(list)`。",
            "用 `match` 按数据形状拆分，不必手动取 first/rest。",
            "模式里的逗号用于 quasiquote 中插入变量位置。",
        ],
        "pitfalls": [
            "`'add` 是 symbol，`\"add\"` 是 string；两者用途不同。",
            "`'(+ 1 2)` 是数据，不会计算；`(+ 1 2)` 才会调用函数。",
        ],
        "drill": "设计 3 条 todo 命令，用 `match` 返回不同说明文字。",
        "docs": ["quote", "match"],
    },
    "vectors_hash_io": {
        "concept": "容器选择：vector 对应随机访问，hash 对应 unordered_map，I/O 放在边界",
        "cpp": """std::unordered_map<std::string, int> freq;
freq[word] += 1;
std::ifstream in("input.txt");""",
        "racket": """#lang racket

(define text (file->string "input.txt"))
(define freq (hash-set (hash) "racket" 1))
(hash-ref freq "racket" 0)""",
        "translation_steps": [
            "需要按索引访问时考虑 vector；需要键值查找时考虑 hash。",
            "不可变 hash 的 `hash-set` 返回新 hash，不改变旧 hash。",
            "把文件读取放在程序边界，核心分析函数接收字符串或列表。",
        ],
        "pitfalls": [
            "不要用 list 模拟所有容器；数据结构选择会影响复杂度。",
            "文件 I/O 会失败，真实项目要处理路径和错误。",
        ],
        "drill": "读入字符串，分词后用 hash 统计一个单词出现次数。",
        "docs": ["vectors", "hash", "io"],
    },
    "state_closure": {
        "concept": "状态封装：从对象字段或静态变量，转成闭包捕获环境",
        "cpp": """auto makeAdder(int n) {
    return [n](int x) { return x + n; };
}""",
        "racket": """#lang racket

(define (make-adder n)
  (lambda (x)
    (+ x n)))""",
        "translation_steps": [
            "识别哪些值是配置，哪些值是调用时输入。",
            "外层函数接收配置，返回内层 lambda。",
            "内层 lambda 可以使用外层绑定，这就是闭包。",
        ],
        "pitfalls": [
            "闭包不一定意味着可变状态；先理解捕获不可变配置。",
            "使用 `set!` 时要明确它修改的是哪个词法绑定。",
        ],
        "drill": "写 `make-threshold-filter`，生成一个按阈值筛选数字的函数。",
        "docs": ["lambda", "let"],
    },
    "typed_racket": {
        "concept": "类型标注：把 C++ 的静态类型经验迁移到 Typed Racket",
        "cpp": """int total(const std::vector<int>& xs);
struct Student { std::string name; int score; };""",
        "racket": """#lang typed/racket

(: total ((Listof Integer) -> Integer))
(define (total xs)
  (foldl + 0 xs))

(struct Student ([name : String] [score : Integer]) #:transparent)""",
        "translation_steps": [
            "切换到 `#lang typed/racket`。",
            "用 `(: name (Type -> Type))` 给函数写类型。",
            "列表类型写作 `(Listof Integer)`，结构字段在 struct 中标注。",
        ],
        "pitfalls": [
            "Typed Racket 是逐步类型系统，不需要把所有旧代码一次性改完。",
            "类型能帮你发现设计问题，但不能替代测试。",
        ],
        "drill": "把 `sum` 和 `student` 模型改写成 Typed Racket。",
        "docs": ["guide", "struct"],
    },
    "macros_dsl": {
        "concept": "语法扩展：从 C++ 预处理器宏，升级到结构化语法转换",
        "cpp": """#define WHEN_POSITIVE(x, body) if ((x) > 0) { body }""",
        "racket": """#lang racket

(define-syntax-rule (when-positive x body ...)
  (when (> x 0)
    body ...))""",
        "translation_steps": [
            "先用普通函数或数据解释器确认你真的需要新语法。",
            "简单宏从 `define-syntax-rule` 开始。",
            "把宏看作 syntax 到 syntax 的转换，不是字符串替换。",
        ],
        "pitfalls": [
            "能用函数解决时不要先写宏。",
            "宏运行在展开阶段，调试方式和普通函数不同。",
        ],
        "drill": "写一个 `unless-zero` 宏，并说明它展开成什么。",
        "docs": ["macros", "pattern_macros"],
    },
    "interpreter": {
        "concept": "解释器：从 C++ AST visitor，转成 match + 递归求值",
        "cpp": """int eval(Node* n) {
    if (n->kind == Number) return n->value;
    if (n->kind == Add) return eval(n->left) + eval(n->right);
}""",
        "racket": """#lang racket

(define (eval-expr e)
  (match e
    [(? number?) e]
    [`(+ ,a ,b) (+ (eval-expr a)
                   (eval-expr b))]))""",
        "translation_steps": [
            "把 AST 节点表示成 struct 或 S-expression。",
            "用 `match` 根据节点形状分派。",
            "每个复合表达式递归求子表达式，再组合结果。",
        ],
        "pitfalls": [
            "环境 env 不要用全局变量；把它作为参数传给 eval。",
            "函数值需要保存定义时环境，才能正确实现词法作用域。",
        ],
        "drill": "给解释器增加 `(- a b)`，并写未知表达式的错误分支。",
        "docs": ["match", "quote", "hash"],
    },
    "gui_web": {
        "concept": "事件和请求：从回调/handler 思维进入 Racket GUI 与 Web",
        "cpp": """button.onClick([] {
    std::cout << "clicked";
});""",
        "racket": """#lang racket/gui

(define frame (new frame% [label "Example"]))
(new button%
     [parent frame]
     [label "Click"]
     [callback (lambda (_button _event)
                 (displayln "clicked"))])
(send frame show #t)""",
        "translation_steps": [
            "GUI 和 Web 都是“事件/请求触发函数”。",
            "回调通常写成 lambda，参数由框架传入。",
            "核心逻辑仍然保持纯函数，边界层负责显示或响应。",
        ],
        "pitfalls": [
            "不要把所有业务逻辑塞进 callback。",
            "GUI 类名常以 `%` 结尾，方法调用使用 `send`。",
        ],
        "drill": "把分数转等级函数写成纯函数，再从 GUI 按钮或 Web handler 调用它。",
        "docs": ["classes", "gui"],
    },
    "capstone": {
        "concept": "项目迁移：把 C++ 项目设计习惯转成 Racket 模块、数据和测试",
        "cpp": """// Model + logic + IO are often mixed while prototyping.
int main() {
    readInput();
    compute();
    printReport();
}""",
        "racket": """#lang racket

; model.rkt   data definitions
; logic.rkt   pure functions
; main.rkt    command-line or UI boundary
; tests.rkt   rackunit coverage""",
        "translation_steps": [
            "先定义数据形状，再写纯函数，再接 I/O。",
            "模块边界用 `provide` 明确暴露的函数。",
            "README 里写清楚运行命令、测试命令和设计取舍。",
        ],
        "pitfalls": [
            "最终项目不要每天换题；范围稳定比功能膨胀重要。",
            "把难点拆成可测试小函数，而不是只靠手动运行 main。",
        ],
        "drill": "为最终项目写 5 个模块级函数签名和 10 个测试用例标题。",
        "docs": ["modules", "contracts", "guide"],
    },
}


def _bridge_key(day: int) -> str:
    if day == 1:
        return "expressions"
    if day == 2:
        return "prefix"
    if day == 3:
        return "types"
    if 4 <= day <= 5:
        return "define_function"
    if 6 <= day <= 7:
        return "conditionals"
    if day == 8:
        return "let"
    if 9 <= day <= 11:
        return "lists_recursion"
    if day == 12:
        return "strings"
    if 13 <= day <= 14:
        return "structs"
    if 15 <= day <= 17:
        return "higher_order"
    if day == 18:
        return "immutability"
    if 19 <= day <= 21:
        return "tests_modules"
    if 22 <= day <= 24:
        return "match_symbols"
    if day == 25:
        return "tests_modules"
    if day == 26:
        return "lists_recursion"
    if 27 <= day <= 31:
        return "vectors_hash_io"
    if 32 <= day <= 35:
        return "state_closure"
    if 36 <= day <= 37:
        return "typed_racket"
    if 38 <= day <= 40:
        return "macros_dsl"
    if 41 <= day <= 45:
        return "interpreter"
    if 46 <= day <= 50:
        return "gui_web"
    return "capstone"


TARGET_LANGUAGES = {
    "racket": {
        "id": "racket",
        "name": "Racket",
        "file_ext": "rkt",
        "runner": "racket day01.rkt",
        "docs": [
            {"title": "Racket Documentation", "url": "https://docs.racket-lang.org/index.html"},
            {"title": "The Racket Guide", "url": "https://docs.racket-lang.org/guide/index.html"},
        ],
    },
    "python": {
        "id": "python",
        "name": "Python",
        "file_ext": "py",
        "runner": "python3 day01.py",
        "docs": [
            {"title": "Python Tutorial", "url": "https://docs.python.org/3/tutorial/"},
            {"title": "Python Standard Library", "url": "https://docs.python.org/3/library/"},
        ],
    },
    "c": {
        "id": "c",
        "name": "C",
        "file_ext": "c",
        "runner": "cc day01.c -o day01 && ./day01",
        "docs": [
            {"title": "C Reference", "url": "https://en.cppreference.com/w/c"},
            {"title": "C Language", "url": "https://en.cppreference.com/w/c/language"},
        ],
    },
    "java": {
        "id": "java",
        "name": "Java",
        "file_ext": "java",
        "runner": "javac Day01.java && java Day01",
        "docs": [
            {"title": "Dev.java Learn", "url": "https://dev.java/learn/"},
            {"title": "Java API", "url": "https://docs.oracle.com/en/java/javase/"},
        ],
    },
}


LANGUAGE_BRIDGES = {
    "python": {
        "expressions": {
            "concept": "表达式和脚本：从 C++ main/编译步骤转成 Python 解释执行",
            "cpp": """int total = 1 + 2 + 3;
std::cout << total << std::endl;""",
            "target": """total = 1 + 2 + 3
print(total)""",
            "steps": ["去掉类型声明和分号。", "用缩进表示代码块，不用大括号。", "用 `print()` 输出，先用解释器快速试验。"],
            "pitfalls": ["Python 变量是名字绑定，不是固定静态类型槽位。", "缩进是语法，不能随意对齐。"],
            "drill": "把 5 个 C++ 算术表达式改成 Python，并用 `print()` 验证。",
        },
        "prefix": {
            "concept": "表达式优先级：Python 仍是中缀，但函数调用更轻量",
            "cpp": """int x = (2 + 3) * (10 - 4);
int y = std::max(3, 9);""",
            "target": """x = (2 + 3) * (10 - 4)
y = max(3, 9)""",
            "steps": ["保留熟悉的中缀算术。", "标准函数直接调用，例如 `max(a, b)`。", "用 REPL 检查每个子表达式。"],
            "pitfalls": ["整数除法如果要取整，用 `//`，普通 `/` 返回浮点。", "不要写 C++ 的 `std::` 命名空间。"],
            "drill": "把 `a + b * c - d` 写成 Python，并解释优先级。",
        },
        "types": {
            "concept": "动态类型：从声明类型转成运行时值和 type hints",
            "cpp": """int score = 95;
std::string name = "Ada";
bool passing = score >= 60;""",
            "target": """score: int = 95
name: str = "Ada"
passing: bool = score >= 60""",
            "steps": ["类型提示写在变量名后面，是辅助工具，不是运行时强制。", "字符串、数字、布尔值直接绑定。", "需要检查类型时用 `isinstance()`。"],
            "pitfalls": ["type hints 不会自动阻止错误赋值。", "Python 的 `True/False` 首字母大写。"],
            "drill": "写 `valid_score(score: int) -> bool`。",
        },
        "define_function": {
            "concept": "函数定义：从返回类型和大括号转成 def、冒号、缩进",
            "cpp": """double addTax(double amount) {
    return amount * 1.13;
}""",
            "target": """def add_tax(amount: float) -> float:
    return amount * 1.13""",
            "steps": ["用 `def name(args):` 开头。", "参数和返回类型可写 type hints。", "函数体必须缩进。"],
            "pitfalls": ["不要忘记冒号。", "Python 风格函数名用 snake_case。"],
            "drill": "把 `int square(int x)` 改成 Python 函数。",
        },
        "conditionals": {
            "concept": "条件：从 if/else if/else 转成 if/elif/else",
            "cpp": """if (score >= 90) grade = "A";
else if (score >= 80) grade = "B";
else grade = "Practice";""",
            "target": """if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "Practice" """,
            "steps": ["`else if` 改成 `elif`。", "条件后写冒号。", "分支内容靠缩进确定范围。"],
            "pitfalls": ["不要写括号和大括号。", "`and/or/not` 不是 `&&/||/!`。"],
            "drill": "把成绩判断函数改写为 Python `if/elif/else`。",
        },
        "let": {
            "concept": "局部变量：Python 函数内赋值天然是局部绑定",
            "cpp": """double tax = price * 0.13;
double tip = price * 0.18;
return price + tax + tip;""",
            "target": """tax = price * 0.13
tip = price * 0.18
return price + tax + tip""",
            "steps": ["函数体内直接创建局部名字。", "按数据流从上到下阅读。", "复杂中间值用清晰变量名。"],
            "pitfalls": ["在函数内给外部变量赋值会创建局部变量，除非声明 `global/nonlocal`。", "不要滥用全局变量。"],
            "drill": "写一个 Python 订单总价函数。",
        },
        "lists_recursion": {
            "concept": "列表遍历：从 vector for 循环转成 for、列表推导或递归",
            "cpp": """int acc = 0;
for (int n : nums) acc += n;""",
            "target": """total = 0
for n in nums:
    total += n

# or
total = sum(nums)""",
            "steps": ["`for (T x : xs)` 改成 `for x in xs:`。", "优先使用内置函数 `sum/len/any/all`。", "转换列表时考虑 list comprehension。"],
            "pitfalls": ["不要用索引循环处理所有列表。", "可变默认参数是 Python 常见陷阱。"],
            "drill": "用 for 和列表推导各写一次筛选偶数。",
        },
        "strings": {
            "concept": "字符串：从 std::string 转成 str、切片和方法",
            "cpp": """s.size();
s[0];
s.substr(1, 3);""",
            "target": """len(s)
s[0]
s[1:4]
s.strip().lower()""",
            "steps": ["长度用 `len(s)`。", "子串用切片 `[start:end]`。", "常用清洗用字符串方法链。"],
            "pitfalls": ["切片 end 不包含。", "字符串不可变，方法返回新字符串。"],
            "drill": "写一个文本分析函数：长度、首字符、是否有空格。",
        },
        "structs": {
            "concept": "数据建模：从 struct/class 转成 dataclass",
            "cpp": """struct Student {
    std::string name;
    int score;
};""",
            "target": """from dataclasses import dataclass

@dataclass
class Student:
    name: str
    score: int""",
            "steps": ["简单数据对象优先用 `@dataclass`。", "字段写类型提示。", "方法放进 class，纯逻辑也可以写成独立函数。"],
            "pitfalls": ["不要把所有东西都写成 class；Python 允许模块级函数。", "可变字段要用 `default_factory`。"],
            "drill": "定义 `Book` dataclass，并写 `expensive(book)`。",
        },
        "higher_order": {
            "concept": "高阶处理：从 STL algorithms 转成 comprehension、map/filter 或生成器",
            "cpp": """std::copy_if(nums.begin(), nums.end(), out, pred);""",
            "target": """evens = [n for n in nums if n % 2 == 0]
squares = [n * n for n in nums]""",
            "steps": ["筛选和转换优先用 comprehension。", "聚合用 `sum/max/min`。", "复杂逻辑先命名函数。"],
            "pitfalls": ["过度嵌套 comprehension 会降低可读性。", "`map/filter` 返回迭代器，不是 list。"],
            "drill": "把一个 C++ STL algorithm 练习改成 Python 列表推导。",
        },
        "capstone": {
            "concept": "Python 项目：从 C++ 编译项目转成模块、包和测试",
            "cpp": """src/
include/
tests/""",
            "target": """racket_tutor/
  model.py
  logic.py
tests/
  test_logic.py""",
            "steps": ["按模块分文件。", "核心逻辑写纯函数。", "用 `pytest` 或 `unittest` 测试。"],
            "pitfalls": ["不要把脚本、I/O、核心逻辑全部混在顶层。", "注意虚拟环境和 requirements。"],
            "drill": "规划一个 Python CLI 或文本分析项目。",
        },
    },
    "c": {
        "expressions": {
            "concept": "从 C++ 到 C：更接近机器模型，少了 iostream 和 class",
            "cpp": """int total = 1 + 2 + 3;
std::cout << total << std::endl;""",
            "target": """#include <stdio.h>

int main(void) {
    int total = 1 + 2 + 3;
    printf("%d\\n", total);
    return 0;
}""",
            "steps": ["使用 `stdio.h` 和 `printf`。", "`main` 返回 int。", "编译运行通常用 `cc file.c -o file`。"],
            "pitfalls": ["C 没有 `std::cout`。", "字符串和数组需要更手动地管理。"],
            "drill": "把 5 个 C++ 输出表达式改成 C `printf`。",
        },
        "define_function": {
            "concept": "函数：语法接近 C++，但没有重载和引用默认语义",
            "cpp": """int square(int x) {
    return x * x;
}""",
            "target": """int square(int x) {
    return x * x;
}""",
            "steps": ["保留返回类型、参数类型和 `return`。", "函数声明通常放在使用前或头文件里。", "没有函数重载，名字必须唯一。"],
            "pitfalls": ["数组参数会退化为指针。", "没有 C++ 引用和模板。"],
            "drill": "写 `double add_tax(double amount)`。",
        },
        "conditionals": {
            "concept": "条件：语法相似，但布尔和字符串处理更底层",
            "cpp": """if (score >= 90) grade = "A";""",
            "target": """const char *grade;
if (score >= 90) {
    grade = "A";
} else {
    grade = "Practice";
}""",
            "steps": ["if/else 大体相同。", "字符串字面量用 `const char *` 指向。", "C99 后可用 `_Bool` 或 `stdbool.h`。"],
            "pitfalls": ["不要用 `==` 比较字符串内容，用 `strcmp`。", "C 的 true/false 需要 `stdbool.h`。"],
            "drill": "写 C 版成绩等级函数。",
        },
        "lists_recursion": {
            "concept": "数组遍历：从 vector 转成数组 + 长度参数",
            "cpp": """int sum(const std::vector<int>& nums);""",
            "target": """int sum(const int nums[], size_t len) {
    int total = 0;
    for (size_t i = 0; i < len; i++) {
        total += nums[i];
    }
    return total;
}""",
            "steps": ["数组函数必须传长度。", "用 `size_t` 表示索引/长度。", "需要动态大小时学习 `malloc/free`。"],
            "pitfalls": ["C 数组不知道自己的长度。", "越界访问是未定义行为。"],
            "drill": "实现 `count_even(const int nums[], size_t len)`。",
        },
        "strings": {
            "concept": "字符串：从 std::string 转成以 NUL 结尾的 char 数组",
            "cpp": """std::string s = "Ada";
s.size();""",
            "target": """#include <string.h>

char s[] = "Ada";
size_t n = strlen(s);""",
            "steps": ["C 字符串是 `char*`/`char[]`。", "长度用 `strlen`。", "复制/拼接用 `strcpy/strncpy/snprintf` 等。"],
            "pitfalls": ["必须留出结尾 `\\0`。", "缓冲区溢出是 C 的核心风险。"],
            "drill": "写函数判断字符串是否包含空格。",
        },
        "structs": {
            "concept": "struct：C 的核心聚合类型，没有成员函数",
            "cpp": """struct Student { std::string name; int score; };""",
            "target": """typedef struct {
    const char *name;
    int score;
} Student;""",
            "steps": ["字段放进 struct。", "行为写成接收指针/值的普通函数。", "用 typedef 简化类型名。"],
            "pitfalls": ["struct 不自动管理资源。", "字符串字段的所有权要说清楚。"],
            "drill": "定义 `Book` struct 和 `is_expensive` 函数。",
        },
        "capstone": {
            "concept": "C 项目：头文件、源文件、Makefile 和内存边界",
            "cpp": """class + vector + string""",
            "target": """include/model.h
src/model.c
src/main.c
Makefile""",
            "steps": ["头文件放声明，`.c` 放实现。", "明确每块内存谁分配谁释放。", "用编译警告和 sanitizer 检查。"],
            "pitfalls": ["忘记初始化和释放内存。", "头文件缺少 include guard。"],
            "drill": "规划一个 C 文本统计工具，写出 `.h/.c` 文件边界。",
        },
    },
    "java": {
        "expressions": {
            "concept": "从 C++ main 转成 Java class + static main",
            "cpp": """int total = 1 + 2 + 3;
std::cout << total << std::endl;""",
            "target": """public class Day01 {
    public static void main(String[] args) {
        int total = 1 + 2 + 3;
        System.out.println(total);
    }
}""",
            "steps": ["代码放在 class 里。", "入口是 `public static void main(String[] args)`。", "输出用 `System.out.println`。"],
            "pitfalls": ["文件名通常要和 public class 同名。", "Java 没有头文件。"],
            "drill": "写一个 Java Day01，输出 10 个表达式结果。",
        },
        "define_function": {
            "concept": "方法：从自由函数转成 class 里的 static 或实例方法",
            "cpp": """double addTax(double amount) {
    return amount * 1.13;
}""",
            "target": """static double addTax(double amount) {
    return amount * 1.13;
}""",
            "steps": ["工具函数可先写 `static`。", "返回类型和参数类型保留。", "命名常用 lowerCamelCase。"],
            "pitfalls": ["Java 没有顶层函数。", "基本类型和对象类型有区别。"],
            "drill": "写 `static int square(int x)`。",
        },
        "conditionals": {
            "concept": "条件：语法接近 C++，但字符串比较用 equals",
            "cpp": """if (name == "Ada") { ... }""",
            "target": """if (name.equals("Ada")) {
    System.out.println("match");
}""",
            "steps": ["if/else 结构基本相同。", "字符串内容比较用 `.equals`。", "布尔运算符仍是 `&& || !`。"],
            "pitfalls": ["不要用 `==` 比较 String 内容。", "空引用调用方法会 NPE。"],
            "drill": "写 Java 成绩等级方法。",
        },
        "lists_recursion": {
            "concept": "集合遍历：从 vector 转成 array 或 List<T>",
            "cpp": """for (int n : nums) total += n;""",
            "target": """int total = 0;
for (int n : nums) {
    total += n;
}""",
            "steps": ["数组和 `List<Integer>` 都支持 enhanced for。", "泛型用 `List<Integer>`。", "流式处理可用 Stream API。"],
            "pitfalls": ["`List<int>` 不存在，要用 `List<Integer>`。", "装箱类型可能有 null。"],
            "drill": "用 for 和 stream 各写一次筛选偶数。",
        },
        "structs": {
            "concept": "数据建模：从 struct 转成 class 或 record",
            "cpp": """struct Student { std::string name; int score; };""",
            "target": """public record Student(String name, int score) {}""",
            "steps": ["不可变数据优先用 record。", "需要行为和状态时用 class。", "字段访问由 accessor 方法生成。"],
            "pitfalls": ["Java 对象是引用语义。", "record 适合数据，不适合复杂可变对象。"],
            "drill": "定义 `Book` record，并写 `isExpensive(Book book)`。",
        },
        "higher_order": {
            "concept": "高阶处理：从 STL algorithm 转成 Stream API",
            "cpp": """copy_if(nums.begin(), nums.end(), out, pred);""",
            "target": """List<Integer> evens = nums.stream()
    .filter(n -> n % 2 == 0)
    .toList();""",
            "steps": ["用 `stream()` 建立管线。", "lambda 写成 `x -> expr`。", "终端操作如 `toList/sum/count` 产生结果。"],
            "pitfalls": ["Stream 只能消费一次。", "不要为了简单循环强行使用 stream。"],
            "drill": "用 stream 计算正数平方列表。",
        },
        "capstone": {
            "concept": "Java 项目：包、类、测试和构建工具",
            "cpp": """src/ include/ tests/""",
            "target": """src/main/java/app/Main.java
src/test/java/app/MainTest.java
pom.xml or build.gradle""",
            "steps": ["按 package 组织代码。", "用 Maven/Gradle 管理依赖和测试。", "核心逻辑与 I/O 分离。"],
            "pitfalls": ["类太多会掩盖简单逻辑。", "注意 public class 文件名规则。"],
            "drill": "规划一个 Java CLI 文本分析器。",
        },
    },
}


GENERIC_DOCS = {
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


def get_language_options() -> list[dict]:
    return [
        {"id": item["id"], "name": item["name"], "file_ext": item["file_ext"], "runner": item["runner"]}
        for item in TARGET_LANGUAGES.values()
    ]


def normalize_target_language(target: str | None) -> str:
    value = (target or "racket").strip().lower()
    return value if value in TARGET_LANGUAGES else "racket"


def _language_bridge(day: int, target: str) -> dict:
    key = _bridge_key(day)
    profile = LANGUAGE_BRIDGES.get(target, {})
    template = profile.get(key) or profile.get("capstone")
    if not template:
        return {}
    docs = template.get("docs") or GENERIC_DOCS[target]
    return {
        "concept": template["concept"],
        "cpp": template["cpp"],
        "racket": template["target"],
        "target": template["target"],
        "target_label": TARGET_LANGUAGES[target]["name"],
        "translation_steps": template["steps"],
        "pitfalls": template["pitfalls"],
        "drill": template["drill"],
        "docs": docs,
    }


def _language_focus(target: str, day: int) -> list[str]:
    language = TARGET_LANGUAGES[target]["name"]
    key = _bridge_key(day)
    base = {
        "expressions": ["运行环境", "输出", "表达式", "REPL/编译"],
        "types": ["变量", "类型系统", "布尔值", "字符串"],
        "define_function": ["函数", "参数", "返回值", "命名风格"],
        "conditionals": ["if/else", "布尔逻辑", "比较", "分支设计"],
        "lists_recursion": ["数组/列表", "遍历", "累加", "边界情况"],
        "strings": ["字符串", "索引", "切片/库函数", "文本处理"],
        "structs": ["数据建模", "字段", "构造", "访问"],
        "higher_order": ["集合处理", "lambda", "筛选", "转换"],
        "capstone": ["项目结构", "测试", "文档", "部署/运行"],
    }.get(key, ["语法迁移", "代码风格", "测试", "项目组织"])
    return [f"{language}: {item}" for item in base]


def _line_note_for_racket(line: str, day: int) -> dict[str, str]:
    stripped = line.strip()
    if not stripped:
        return {
            "line": "",
            "plain": "空行，用来分隔代码块。",
            "syntax": "Racket 不依赖空行运行；空行只影响可读性。",
            "cpp": "类似 C++ 中为了分组而空一行。",
        }
    if stripped.startswith(";"):
        return {
            "line": line,
            "plain": "这是注释，给人读，程序不会执行。",
            "syntax": "Racket 单行注释从 `;` 开始，一直到行尾。",
            "cpp": "类似 C++ 的 `// comment`。",
        }
    if stripped.startswith("#lang"):
        return {
            "line": line,
            "plain": "声明这个文件使用哪一种 Racket 语言。",
            "syntax": "`#lang racket` 通常放在文件第一行，告诉解释器后面的语法按 Racket 处理。",
            "cpp": "有点像 C++ 文件开头的编译环境选择，但它比 `#include` 更像“语言模式”。",
        }
    if stripped.startswith("(define ("):
        return {
            "line": line,
            "plain": "定义一个函数。",
            "syntax": "`define` 后面的小括号里，第一个名字是函数名，后面是参数名。函数体写在下一行或后面。",
            "cpp": "类似 `return_type name(args) { ... }`，但 Racket 不写返回类型。",
        }
    if stripped.startswith("(define "):
        return {
            "line": line,
            "plain": "给一个值起名字。",
            "syntax": "`(define name value)` 会把右边的值绑定到左边的名字。默认不要把它想成可反复修改的变量。",
            "cpp": "类似 `const auto name = value;`，更接近命名一个值，而不是先声明再赋值。",
        }
    if stripped.startswith("(struct "):
        return {
            "line": line,
            "plain": "定义一种数据结构。",
            "syntax": "`struct` 后面是类型名，括号里是字段名；`#:transparent` 让打印和测试更清楚。",
            "cpp": "类似 C++ 的 `struct Student { ... };`，但 Racket 会自动生成构造器和访问器。",
        }
    if stripped in {")", "]))", "])", ")))", "))"} or set(stripped) <= {")", "]"}:
        return {
            "line": line,
            "plain": "关闭前面打开的表达式或分支。",
            "syntax": "Racket 用括号表示结构；这一行通常不是新动作，而是结束嵌套层级。",
            "cpp": "类似 C++ 的 `}`，表示一个代码块结束。",
        }
    if stripped.startswith("["):
        return {
            "line": line,
            "plain": "这是 `cond`、`let` 或模式匹配里的一个小分支。",
            "syntax": "方括号在这里主要提升可读性，和小括号一样表达结构；前半段通常是条件或绑定，后半段是结果。",
            "cpp": "类似 `if (...) return ...;` 或局部变量初始化的一项。",
        }
    if stripped.startswith("(cond"):
        return {
            "line": line,
            "plain": "开始多分支判断。",
            "syntax": "`cond` 由多个分支组成，每个分支一般写成 `[条件 结果]`。",
            "cpp": "类似 `if / else if / else` 链。",
        }
    if stripped.startswith("(if"):
        return {
            "line": line,
            "plain": "开始一个二选一判断。",
            "syntax": "`if` 后面依次是条件、为真时的结果、为假时的结果。",
            "cpp": "类似三元表达式 `cond ? a : b`，因为 Racket 的 `if` 本身会产生值。",
        }
    if stripped.startswith("(let"):
        return {
            "line": line,
            "plain": "开始一组局部绑定。",
            "syntax": "`let` 先给中间结果命名，再在 body 中使用这些名字。",
            "cpp": "类似在函数内部声明几个局部变量。",
        }
    if stripped.startswith("(lambda"):
        return {
            "line": line,
            "plain": "创建一个匿名函数。",
            "syntax": "`lambda` 后面的括号是参数列表，后面是函数体。",
            "cpp": "类似 C++ lambda：`[](auto x) { return ...; }`。",
        }
    if stripped.startswith("(match"):
        return {
            "line": line,
            "plain": "开始按数据形状进行匹配。",
            "syntax": "`match` 会看值的结构，然后选择第一个匹配的分支。",
            "cpp": "比 `switch` 更强，因为它能拆列表、结构体和嵌套数据。",
        }
    if stripped.startswith("(require"):
        return {
            "line": line,
            "plain": "导入一个库或模块。",
            "syntax": "`require` 把别的模块提供的名字带进当前文件。",
            "cpp": "类似 `#include`，但 Racket 的模块边界更明确。",
        }
    if stripped.startswith("(provide"):
        return {
            "line": line,
            "plain": "声明这个模块对外开放哪些名字。",
            "syntax": "`provide` 后面的名字可以被其他文件 `require` 使用。",
            "cpp": "类似把函数声明放进 `.h`，明确告诉别人能用什么。",
        }
    if stripped.startswith("(module+"):
        return {
            "line": line,
            "plain": "定义一个附加子模块，常用于测试。",
            "syntax": "`module+ test` 里的代码可以在测试时运行，不干扰主程序。",
            "cpp": "类似把测试代码放到单独 test target。",
        }
    if stripped.startswith("("):
        return {
            "line": line,
            "plain": "这是一次函数调用或特殊语法形式。",
            "syntax": "Racket 的基本形状是 `(函数 参数1 参数2 ...)`。先看括号里的第一个位置，它决定这一整句在做什么。",
            "cpp": "类似 `function(arg1, arg2)`，只是函数名放到最前面；`+`、`*` 也按这个规则写。",
        }
    return {
        "line": line,
        "plain": "这是上一行表达式的一部分。",
        "syntax": "Racket 允许一个表达式跨多行；缩进帮助你看出它属于哪一层括号。",
        "cpp": "类似 C++ 中函数调用参数太长时换行继续写。",
    }


def _racket_line_notes(code: str, day: int) -> list[dict[str, str]]:
    return [_line_note_for_racket(line, day) for line in code.splitlines()]


def _line_note_for_python(line: str) -> dict[str, str]:
    stripped = line.strip()
    if not stripped:
        return {"line": "", "plain": "空行，用来分隔逻辑段。", "syntax": "Python 不靠空行运行；真正决定代码块的是缩进。", "cpp": "类似 C++ 中为了可读性空一行。"}
    if stripped.startswith("#"):
        return {"line": line, "plain": "这是注释。", "syntax": "Python 单行注释从 `#` 开始。", "cpp": "类似 C++ 的 `//`。"}
    if stripped.startswith("import ") or stripped.startswith("from "):
        return {"line": line, "plain": "导入库或库里的名字。", "syntax": "`import` 把模块带进当前文件，`from ... import ...` 只带入指定名字。", "cpp": "类似 `#include`，但 Python 导入的是模块对象。"}
    if stripped.startswith("@"):
        return {"line": line, "plain": "这是装饰器，会修改下一行定义的函数或类。", "syntax": "`@decorator` 写在定义前，常用于 dataclass、路由、测试等场景。", "cpp": "不像 C++ 属性那么简单，它会实际包装对象。"}
    if stripped.startswith("class "):
        return {"line": line, "plain": "定义一个类。", "syntax": "`class Name:` 后面的缩进块属于这个类。", "cpp": "类似 `class Name { ... };`，但用缩进代替大括号。"}
    if stripped.startswith("def "):
        return {"line": line, "plain": "定义一个函数。", "syntax": "`def name(args):` 以冒号结尾；下一层缩进就是函数体。类型提示可选。", "cpp": "类似 `return_type name(args) { ... }`，但 Python 不写大括号。"}
    if stripped.startswith("if "):
        return {"line": line, "plain": "开始条件分支。", "syntax": "`if 条件:` 后面缩进的行在条件为真时执行。", "cpp": "类似 `if (...) { ... }`。"}
    if stripped.startswith("elif "):
        return {"line": line, "plain": "继续判断另一个条件。", "syntax": "`elif` 是 Python 的 `else if`。", "cpp": "等价于 C++ 的 `else if (...)`。"}
    if stripped.startswith("else"):
        return {"line": line, "plain": "处理前面条件都不成立的情况。", "syntax": "`else:` 后面也必须缩进。", "cpp": "类似 C++ 的 `else { ... }`。"}
    if stripped.startswith("for "):
        return {"line": line, "plain": "遍历一个序列。", "syntax": "`for item in items:` 会逐个取出元素。", "cpp": "类似 range-based for：`for (auto item : items)`。"}
    if stripped.startswith("return "):
        return {"line": line, "plain": "返回函数结果。", "syntax": "`return` 会结束当前函数并交出后面的值。", "cpp": "和 C++ 的 `return value;` 很接近。"}
    if "print(" in stripped:
        return {"line": line, "plain": "把结果输出到终端。", "syntax": "`print(...)` 是内置函数，参数放在括号里。", "cpp": "类似 `std::cout << ...`。"}
    if "=" in stripped:
        return {"line": line, "plain": "把右边的值绑定到左边的名字。", "syntax": "Python 变量不需要声明类型；`name = value` 会让名字指向这个值。", "cpp": "更像 `auto name = value;`，但类型在运行时由值决定。"}
    return {"line": line, "plain": "这是一个表达式或上一代码块的一部分。", "syntax": "看缩进判断它属于哪个函数、类或分支。", "cpp": "类似 C++ 中某个 `{}` 代码块内部的一行。"}


def _line_note_for_c(line: str) -> dict[str, str]:
    stripped = line.strip()
    if not stripped:
        return {"line": "", "plain": "空行，用来分隔代码段。", "syntax": "C 不依赖空行运行。", "cpp": "和 C++ 一样，只影响可读性。"}
    if stripped.startswith("//") or stripped.startswith("/*"):
        return {"line": line, "plain": "这是注释。", "syntax": "C 支持 `//` 单行注释和 `/* ... */` 块注释。", "cpp": "和 C++ 基本一样。"}
    if stripped.startswith("#include"):
        return {"line": line, "plain": "引入头文件。", "syntax": "预处理器会在编译前处理 `#include`，让你使用库函数声明。", "cpp": "类似 C++ `#include <iostream>`，但 C 常用 `stdio.h/string.h`。"}
    if "main(" in stripped:
        return {"line": line, "plain": "程序入口函数。", "syntax": "`int main(void)` 表示程序从这里开始执行，并返回一个整数状态码。", "cpp": "和 C++ 的 `int main()` 很接近。"}
    if stripped == "{" or stripped.endswith("{"):
        return {"line": line, "plain": "开始一个代码块。", "syntax": "大括号包住函数、if、for 等结构的主体。", "cpp": "和 C++ 的 `{` 完全类似。"}
    if stripped == "}" or stripped == "};":
        return {"line": line, "plain": "结束一个代码块或结构定义。", "syntax": "`}` 结束作用域；struct 定义后通常还要分号。", "cpp": "和 C++ 的 `}` / `};` 类似。"}
    if stripped.startswith("typedef struct") or stripped.startswith("struct "):
        return {"line": line, "plain": "定义结构体类型。", "syntax": "`struct` 把多个字段组合成一个数据类型。", "cpp": "类似 C++ struct，但没有成员函数和构造器。"}
    if stripped.startswith("for "):
        return {"line": line, "plain": "开始循环。", "syntax": "C 的 for 通常包含初始化、条件、更新三部分。", "cpp": "和经典 C++ for 循环相同。"}
    if stripped.startswith("if "):
        return {"line": line, "plain": "开始条件判断。", "syntax": "括号中是条件；非 0 通常表示真。", "cpp": "和 C++ 的 if 很接近。"}
    if stripped.startswith("return"):
        return {"line": line, "plain": "返回函数结果。", "syntax": "`return` 后面的值必须符合函数返回类型。", "cpp": "和 C++ 的 `return` 一样。"}
    if "printf" in stripped:
        return {"line": line, "plain": "格式化输出。", "syntax": "`printf` 第一个参数是格式字符串，`%d/%s/%f` 等占位符对应后面的值。", "cpp": "类似 `std::cout`，但你必须写清楚格式。"}
    if stripped.endswith(";"):
        return {"line": line, "plain": "一条 C 语句。", "syntax": "C 语句通常以分号结束；类型、指针和数组要写清楚。", "cpp": "和 C++ 的普通语句很接近。"}
    return {"line": line, "plain": "这是声明、表达式或代码块的一部分。", "syntax": "结合上下文看它属于函数、struct 还是控制流。", "cpp": "和 C++ 的块结构阅读方式相同。"}


def _line_note_for_java(line: str) -> dict[str, str]:
    stripped = line.strip()
    if not stripped:
        return {"line": "", "plain": "空行，用来分隔代码段。", "syntax": "Java 不依赖空行运行。", "cpp": "类似 C++ 中为了可读性空行。"}
    if stripped.startswith("//") or stripped.startswith("/*"):
        return {"line": line, "plain": "这是注释。", "syntax": "Java 支持 `//` 和 `/* ... */` 注释。", "cpp": "和 C++ 注释一样。"}
    if stripped.startswith("import "):
        return {"line": line, "plain": "导入类或包里的名字。", "syntax": "`import` 让后面代码可以直接使用某些类名。", "cpp": "不像 `#include` 粘贴文本，更像声明要使用的包名。"}
    if " class " in f" {stripped} " or stripped.startswith("public class"):
        return {"line": line, "plain": "定义一个类。", "syntax": "Java 代码基本都写在 class 里；public class 名通常要和文件名相同。", "cpp": "类似 C++ class，但 Java 没有头文件。"}
    if stripped.startswith("public record") or stripped.startswith("record "):
        return {"line": line, "plain": "定义一个 record 数据类型。", "syntax": "record 适合不可变数据，Java 会自动生成构造器和访问方法。", "cpp": "类似简单 struct，但更自动、更不可变。"}
    if "main(" in stripped:
        return {"line": line, "plain": "Java 程序入口。", "syntax": "`public static void main(String[] args)` 是命令行程序的固定入口签名。", "cpp": "类似 C++ 的 `int main(int argc, char** argv)`。"}
    if stripped == "{" or stripped.endswith("{"):
        return {"line": line, "plain": "开始一个代码块。", "syntax": "大括号定义 class、method、if、for 等结构的范围。", "cpp": "和 C++ 的 `{` 一样。"}
    if stripped == "}":
        return {"line": line, "plain": "结束一个代码块。", "syntax": "这一行关闭最近打开的 `{`。", "cpp": "和 C++ 的 `}` 一样。"}
    if stripped.startswith("if "):
        return {"line": line, "plain": "开始条件判断。", "syntax": "括号中必须是 boolean 表达式。", "cpp": "类似 C++ if，但 Java 不把整数当 boolean。"}
    if stripped.startswith("for "):
        return {"line": line, "plain": "开始循环或增强 for 遍历。", "syntax": "`for (Type x : xs)` 会逐个取集合元素。", "cpp": "类似 C++ range-based for。"}
    if "System.out.println" in stripped:
        return {"line": line, "plain": "输出一行到终端。", "syntax": "`System.out.println(...)` 是 Java 最常见的控制台输出。", "cpp": "类似 `std::cout << value << std::endl;`。"}
    if stripped.startswith("return"):
        return {"line": line, "plain": "返回方法结果。", "syntax": "返回值类型要和方法声明一致；`void` 方法可以不返回值。", "cpp": "和 C++ `return` 很接近。"}
    if stripped.endswith(";"):
        return {"line": line, "plain": "一条 Java 语句。", "syntax": "Java 普通语句以分号结束，变量通常需要声明类型。", "cpp": "和 C++ 的声明/赋值语句相似。"}
    return {"line": line, "plain": "这是类、方法或代码块的一部分。", "syntax": "结合大括号层级判断它属于哪个结构。", "cpp": "和 C++ 读作用域的方式类似。"}


def _line_notes_for_language(code: str, target: str, day: int) -> list[dict[str, str]]:
    if target == "racket":
        return _racket_line_notes(code, day)
    explainers = {
        "python": _line_note_for_python,
        "c": _line_note_for_c,
        "java": _line_note_for_java,
    }
    explainer = explainers.get(target)
    if not explainer:
        return []
    return [explainer(line) for line in code.splitlines()]


def _language_lesson(index: int, item: dict, target: str) -> Lesson:
    language = TARGET_LANGUAGES[target]["name"]
    bridge = _language_bridge(index, target)
    title = item["title"].replace("Racket", language).replace("racket", language.lower())
    category = f"Day {index:02d} - C++ to {language}"
    goal = f"基于 C++ 已有基础，学习 {language} 中与“{title}”对应的语法、运行方式和代码风格。"
    cpp_bridge = f"今天从 C++ 的写法出发，对照 {language} 的惯用写法，重点避免把 {language} 写成 C++ 翻译腔。"
    explanation = (
        f"这一节把原来的主题迁移到 {language}：先确认 C++ 概念，再看 {language} 的语法、标准库和工程习惯。"
        "你应该亲手运行示例，并把语法差异写进笔记。"
    )
    code = bridge.get("target", "")
    practice = [
        f"运行今日 {language} 示例代码：`{TARGET_LANGUAGES[target]['runner']}`。",
        "把 C++ 示例逐行改写成目标语言，并解释每一处语法差异。",
        f"查阅官方文档，补充 3 条 {language} 惯用写法。",
    ]
    assignment = (
        f"提交一个 day{index:02d}.{TARGET_LANGUAGES[target]['file_ext']}，"
        f"完成今日 C++ 到 {language} 的转换练习，并附 5 行学习反思。"
    )
    lesson = Lesson(
        day=index,
        category=category,
        week=((index - 1) // 7) + 1,
        title=title,
        goal=goal,
        cpp_bridge=cpp_bridge,
        explanation=explanation,
        syntax_bridge={
            **bridge,
            "today_angle": f"今天以“{title}”为主题，从 C++ 迁移到 {language}。",
        },
        official_docs=bridge.get("docs", GENERIC_DOCS[target]),
        racket_focus=_language_focus(target, index),
        code=code,
        line_notes=_line_notes_for_language(code, target, index),
        practice=practice,
        checklist=_default_checklist(index, language),
        assignment=assignment,
        grading_rubric=_default_rubric(language),
    )
    data = asdict(lesson)
    data["target_language"] = target
    data["target_language_name"] = language
    return data


def _syntax_bridge(day: int, item: dict) -> dict:
    bridge = dict(BRIDGE_TEMPLATES[_bridge_key(day)])
    bridge["today_angle"] = (
        f"今天的主题是“{item['title']}”。先用你熟悉的 C++ 写法定位概念，"
        "再把控制流、数据流或函数边界改写成 Racket 的表达式风格。"
    )
    bridge["docs"] = [DOCS[key] for key in bridge["docs"]]
    return bridge


def _default_checklist(day: int, language: str = "Racket") -> list[str]:
    return [
        f"阅读 Day {day:02d} 的目标、C++ 对照和 {language} 重点。",
        "打开官方文档链接，至少阅读对应小节的示例。",
        "手动敲一遍示例代码，不要只复制粘贴。",
        "在 REPL 中改 3 个参数，观察输出变化。",
        "完成今日 practice 的所有小练习。",
        "写下一个今天最容易混淆的概念。",
        "提交今日 assignment 到作业区。",
    ]


def _default_rubric(language: str = "Racket") -> list[str]:
    return [
        "正确性：程序是否能运行，结果是否符合题目。",
        f"{language} 风格：是否使用该语言的惯用语法、命名和标准库。",
        f"C++ 迁移：是否避免把 {language} 写成逐字翻译的 C++。",
        "测试：是否覆盖正常情况、边界情况和至少一个异常思路。",
        "解释能力：注释或 README 是否说明了设计选择。",
    ]


def get_lessons(target_language: str | None = None) -> list[dict]:
    target = normalize_target_language(target_language)
    if target != "racket":
        return [_language_lesson(index, item, target) for index, item in enumerate(LESSON_BLUEPRINTS, start=1)]

    lessons: list[Lesson] = []
    for index, item in enumerate(LESSON_BLUEPRINTS, start=1):
        syntax_bridge = _syntax_bridge(index, item)
        lesson = Lesson(
            day=index,
            category=item["category"],
            week=((index - 1) // 7) + 1,
            title=item["title"],
            goal=item["goal"],
            cpp_bridge=item["cpp_bridge"],
            explanation=item["explanation"],
            syntax_bridge=syntax_bridge,
            official_docs=syntax_bridge["docs"],
            racket_focus=item["racket_focus"],
            code=item["code"],
            line_notes=_racket_line_notes(item["code"], index),
            practice=item["practice"],
            checklist=_default_checklist(index),
            assignment=item["assignment"],
            grading_rubric=_default_rubric(),
        )
        lessons.append(lesson)
    result = [asdict(lesson) for lesson in lessons]
    for lesson in result:
        lesson["target_language"] = "racket"
        lesson["target_language_name"] = "Racket"
    return result


def get_lesson(day: int, target_language: str | None = None) -> dict | None:
    lessons = get_lessons(target_language)
    if 1 <= day <= len(lessons):
        return lessons[day - 1]
    return None
