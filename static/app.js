const SUPPORTED_UI_LANGUAGE_CODES = ["en", "zh", "ja", "ko", "fr"];

function normalizeUiLanguage(language) {
  return SUPPORTED_UI_LANGUAGE_CODES.includes(language) ? language : "en";
}

const state = {
  lessons: [],
  languages: [],
  user: null,
  authMode: "register",
  profileLoaded: false,
  uiLanguage: normalizeUiLanguage(localStorage.getItem("codeBridge.uiLanguage")),
  target: localStorage.getItem("racketTutor.targetLanguage") || "racket",
  knownLanguages: readKnownLanguages(),
  baseLanguage: localStorage.getItem("racketTutor.baseLanguage") || readKnownLanguages()[0] || "",
  languageExperienceChosen: localStorage.getItem("racketTutor.languageExperienceChosen") === "true"
    || localStorage.getItem("racketTutor.baseLanguage") !== null
    || localStorage.getItem("racketTutor.knownLanguages") !== null
    || localStorage.getItem("racketTutor.cppStatus") !== null,
  activeDay: Number(localStorage.getItem("racketTutor.activeDay") || 1),
  query: "",
  unlockedSampleCode: null,
  submittedLessons: new Set(),
  masteryByDay: new Map(),
  weakestDay: null,
  popQuizSchedule: [],
  aiReviewEnabled: false,
};

const UI_LANGUAGES = {
  en: "English",
  zh: "中文",
  ja: "日本語",
  ko: "한국어",
  fr: "Français",
};

const translations = {
  en: {
    htmlLang: "en",
    brandSubtitleDefault: "C++ foundation to multiple languages",
    totalProgress: "Total progress",
    searchPlaceholder: "Search day, topic, or category",
    interfaceLanguage: "Interface language",
    accountSaved: "Your progress is saved to this account.",
    howToUse: "How to Use",
    changePassword: "Change Password",
    adminDashboard: "Admin Dashboard",
    logOut: "Log Out",
    targetLanguage: "Target language",
    changeLanguageExperience: "Change language experience",
    cppFoundations: "C++ Foundations",
    cppTrackNotice: "Finish or switch when you are ready for another language.",
    knowCppNow: "I know C++ now",
    dailyCourseList: "Daily course list",
    account: "Account",
    saveLearningData: "Save your learning data",
    saveLearningDataBody: "Register or log in so your language choices, current day, checklist progress, and submissions stay tied to your own account.",
    accountAction: "Account action",
    register: "Register",
    logIn: "Log in",
    name: "Name",
    password: "Password",
    createAccount: "Create Account",
    languageExperienceCheck: "Language Experience Check",
    languageExperienceTitle: "Which one language can you already use?",
    languageExperienceBody: "Choose one language as your foundation. The course will use that language to teach the other languages. Choose None to start with C++ Foundations.",
    knownProgrammingLanguages: "Known programming languages",
    none: "None",
    continue: "Continue",
    previousDay: "Previous day",
    nextDay: "Next day",
    day: "Day",
    checklist: "Checklist",
    week: "Week",
    knownLanguageBridge: "Known Language Bridge",
    syntaxBridge: "Syntax Bridge",
    knownLanguageSyntax: "Known Language Syntax",
    targetSyntax: "Target Syntax",
    sampleInput: "Sample Input",
    expectedOutput: "Expected Output / Result",
    sameIdeaTranslated: "Same idea translated below",
    translationSteps: "Translation Steps",
    commonPitfalls: "Common Pitfalls",
    todaysTranslationDrill: "Today's Translation Drill",
    officialDocumentation: "Official Documentation",
    detailedExplanation: "Detailed Explanation",
    sampleCodeAfterSubmission: "Sample Code After Submission",
    copyCode: "Copy Code",
    copied: "Copied",
    sampleCodeNote: "Submit your assignment first. After review, use this sample to compare structure, syntax, and style.",
    lineByLineSyntax: "Line-by-Line Syntax",
    lineByLineSyntaxNotes: "Line-by-Line Syntax Notes",
    todaysHomework: "Today's Homework",
    dayByDayGuidance: "Day-by-Day Guidance",
    refresh: "Refresh",
    today: "Today",
    learningHabits: "Learning Habits",
    focusAreas: "Focus Areas",
    nextStudyBlock: "Next Study Block",
    dailyChecklist: "Daily Checklist",
    reset: "Reset",
    todaysAssignment: "Today's Assignment",
    uploadHomework: "Upload Homework for Review",
    optional: "Optional",
    homeworkFile: "Homework file",
    orPasteCode: "Or paste code",
    standardInput: "Standard input for Judge0 runner",
    stdinPlaceholder: "Optional. Put one input value per line when your program reads input.",
    aiFocus: "What should AI focus on?",
    aiFocusPlaceholder: "Example: I am unsure whether my recursion is correct.",
    submitAndReview: "Submit and Review",
    reviewHistory: "Review History",
    feedback: "Feedback",
    siteFeedback: "Site Feedback",
    tellUsFixing: "Tell us what needs fixing",
    closeFeedbackForm: "Close feedback form",
    feedbackType: "Feedback type",
    bugOrBrokenPage: "Bug or broken page",
    lessonOrHomeworkContent: "Lesson or homework content",
    featureRequest: "Feature request",
    other: "Other",
    whatHappened: "What happened?",
    feedbackPlaceholder: "Example: Day 12 homework is unclear because...",
    sendFeedback: "Send Feedback",
    accountSecurity: "Account Security",
    changeYourPassword: "Change your password",
    closePasswordForm: "Close password form",
    currentPassword: "Current password",
    newPassword: "New password",
    confirmNewPassword: "Confirm new password",
    updatePassword: "Update Password",
    skip: "Skip",
    gotIt: "I got it",
    finish: "Finish",
    loading: "Loading",
    loginButton: "Log In",
    creatingAccount: "Creating account...",
    loggingIn: "Logging in...",
    chooseLanguageOrNone: "Choose one language or None before continuing.",
    aiReviewConnected: "AI Review Connected",
    aiReviewConnectedBody: "Submissions receive deeper paragraph-level review and line-by-line improvement suggestions, even for short code.",
    noConsoleOutput: "No console output for this example.",
    homeworkSubmitted: "Homework submitted.",
    finalLessonFinished: "You finished the final lesson for this track.",
    keepMoving: "You can keep moving through the open course.",
    allLessonsUnlocked: "All lessons are unlocked.",
    allLessonsUnlockedBody: "You can study any day now. Submit HW Q1, HW Q2, and HW Q3 when you want feedback and history.",
    submitted: "Submitted",
    lessonLockedTitle: "Submit Day {day} homework before opening this lesson.",
    lessonLockedMessage: "Day {day} is locked. Submit Day {previousDay} homework before moving on.",
    courseLoadFailed: "Course data failed to load",
    knownLanguage: "Known Language",
    target: "Target",
    code: "Code",
    blankLine: "Blank line",
    syntax: "Syntax",
    comparison: "{language} Comparison",
    phraseBreakdown: "Phrase Breakdown",
    noSubmissionsYet: "No submissions yet.",
    noSubmittedProgramSaved: "No submitted program text was saved for this older record.",
    noJudge0Saved: "No Judge0 result saved for this older submission.",
    judge0Unavailable: "Judge0 was not available for this submission.",
    status: "Status",
    unknown: "Unknown",
    time: "Time",
    memory: "Memory",
    stdout: "Stdout",
    stderr: "Stderr",
    compileOutput: "Compile output",
    message: "Message",
    noBuiltInChecker: "No built-in checker result saved for this older submission.",
    assignmentScore: "Assignment score",
    score: "Score",
    nonEmptyLines: "Non-empty lines",
    homeworkLabelsFound: "Homework labels found",
    checks: "Checks",
    pass: "PASS",
    fix: "FIX",
    noneLower: "none",
    mastery: "Mastery",
    masteryRating: "Mastery rating",
    masteryScale: "1 = not mastered, 5 = fully mastered",
    unrated: "Unrated",
    weakestKnowledge: "Weakest knowledge",
    noWeakestKnowledge: "No rated homework yet.",
    popQuizSchedule: "POP Quiz Schedule",
    noPopQuizSchedule: "Submit homework to generate spaced POP quiz dates.",
    quizDue: "Due {date}: Day {day} after {interval} day(s)",
    viewSubmittedProgramAndReview: "View submitted program and review",
    submittedProgram: "Submitted Program",
    judge0RunResult: "Judge0 Run Result",
    builtInCodeChecker: "Built-in Code Checker",
    whatToFixReview: "What to Fix / Review Feedback",
    loadingGuidance: "Loading guidance...",
    noGuidance: "No guidance available yet.",
    guidanceFailed: "Guidance failed to load",
    reviewing: "Reviewing",
    runningCode: "Running code with Judge0, then generating feedback...",
    submissionFailed: "Submission failed",
    sendingFeedback: "Sending feedback...",
    feedbackFailed: "Feedback failed to send",
    feedbackSent: "Feedback sent. Thank you.",
    passwordsNoMatch: "New passwords do not match.",
    passwordTooShort: "New password must be at least 8 characters.",
    updatingPassword: "Updating password...",
    passwordUpdateFailed: "Password update failed",
    passwordUpdated: "Password updated. Use the new password next time you log in.",
    stepOf: "Step {current} of {total}",
    cppFoundationSubtitle: "C++ Foundations · prerequisite track · {days} days",
    targetSubtitle: "{base} foundation to {target} · {days} days",
    syntaxArrow: "{base} Syntax → {target} Syntax",
    languageSyntax: "{language} Syntax",
    languageLineSyntax: "{language} Line-by-Line Syntax",
    accountRequestFailed: "Account request failed",
    linePrefix: "L",
    dayLabel: "Day {day}",
    tourAccountTitle: "Your account tools",
    tourAccountText: "This area saves your progress. You can open this tutorial again, change your password, log out, and admins can check users and feedback.",
    tourFoundationTitle: "Choose your foundation",
    tourFoundationText: "After registering, choose the one language you already know. Choose None if you want to start with C++ Foundations.",
    tourTargetTitle: "Pick a target language",
    tourTargetText: "Use this menu to switch what language CodeBridge teaches you next.",
    tourDayListTitle: "Open a daily lesson",
    tourDayListText: "This is the daily course list. Scroll the left sidebar to reach every day.",
    tourLessonTitle: "Study the lesson",
    tourLessonText: "Read the bridge from your known language, the detailed explanation, line-by-line notes, and official documentation.",
    tourHomeworkTitle: "Do HW Q1, Q2, and Q3",
    tourHomeworkText: "Each day has three concrete programs. Follow the exact numbers, calculation, and output requirements.",
    tourSubmitTitle: "Submit homework",
    tourSubmitText: "Upload a file or paste code here. After submitting, review feedback and compare with sample code.",
    tourFeedbackTitle: "Send website feedback",
    tourFeedbackText: "Use this button if something is broken or confusing. Your message goes to the site owner.",
  },
  zh: {
    htmlLang: "zh-Hans",
    brandSubtitleDefault: "以 C++ 为基础学习多种语言",
    totalProgress: "总进度",
    searchPlaceholder: "搜索天数、主题或类别",
    interfaceLanguage: "界面语言",
    accountSaved: "你的学习进度会保存到这个账号。",
    howToUse: "使用说明",
    changePassword: "修改密码",
    adminDashboard: "管理员面板",
    logOut: "退出登录",
    targetLanguage: "目标语言",
    changeLanguageExperience: "更改已有语言经验",
    cppFoundations: "C++ 基础",
    cppTrackNotice: "学完后，或准备好时，可以切换到另一门语言。",
    knowCppNow: "我现在会 C++ 了",
    dailyCourseList: "每日课程列表",
    account: "账号",
    saveLearningData: "保存你的学习数据",
    saveLearningDataBody: "注册或登录后，你的语言选择、当前天数、清单进度和提交记录都会绑定到自己的账号。",
    accountAction: "账号操作",
    register: "注册",
    logIn: "登录",
    name: "姓名",
    password: "密码",
    createAccount: "创建账号",
    languageExperienceCheck: "语言经验检查",
    languageExperienceTitle: "你已经会哪一门编程语言？",
    languageExperienceBody: "选择一门语言作为基础。课程会用这门语言帮助你学习其他语言。选择 None 则从 C++ 基础开始。",
    knownProgrammingLanguages: "已掌握的编程语言",
    none: "None",
    continue: "继续",
    previousDay: "上一天",
    nextDay: "下一天",
    day: "天",
    checklist: "清单",
    week: "周",
    knownLanguageBridge: "已有语言桥梁",
    syntaxBridge: "语法桥梁",
    knownLanguageSyntax: "已有语言语法",
    targetSyntax: "目标语法",
    sampleInput: "示例输入",
    expectedOutput: "预期输出 / 结果",
    sameIdeaTranslated: "同一个思路在下方翻译",
    translationSteps: "翻译步骤",
    commonPitfalls: "常见错误",
    todaysTranslationDrill: "今日翻译练习",
    officialDocumentation: "官方文档",
    detailedExplanation: "详细解释",
    sampleCodeAfterSubmission: "提交后查看示例代码",
    copyCode: "复制代码",
    copied: "已复制",
    sampleCodeNote: "先提交作业。批改后，用这个示例对比结构、语法和风格。",
    lineByLineSyntax: "逐行语法",
    lineByLineSyntaxNotes: "逐行语法笔记",
    todaysHomework: "今日作业",
    dayByDayGuidance: "每日学习建议",
    refresh: "刷新",
    today: "今天",
    learningHabits: "学习习惯",
    focusAreas: "重点区域",
    nextStudyBlock: "下一段学习",
    dailyChecklist: "每日清单",
    reset: "重置",
    todaysAssignment: "今日任务",
    uploadHomework: "上传作业并批改",
    optional: "可选",
    homeworkFile: "作业文件",
    orPasteCode: "或粘贴代码",
    standardInput: "Judge0 运行器标准输入",
    stdinPlaceholder: "可选。当程序读取输入时，每行放一个输入值。",
    aiFocus: "希望 AI 重点看什么？",
    aiFocusPlaceholder: "例如：我不确定递归写得对不对。",
    submitAndReview: "提交并批改",
    reviewHistory: "批改历史",
    feedback: "反馈",
    siteFeedback: "网站反馈",
    tellUsFixing: "告诉我们哪里需要修复",
    closeFeedbackForm: "关闭反馈表单",
    feedbackType: "反馈类型",
    bugOrBrokenPage: "错误或页面损坏",
    lessonOrHomeworkContent: "课程或作业内容",
    featureRequest: "功能建议",
    other: "其他",
    whatHappened: "发生了什么？",
    feedbackPlaceholder: "例如：第 12 天作业不清楚，因为...",
    sendFeedback: "发送反馈",
    accountSecurity: "账号安全",
    changeYourPassword: "修改你的密码",
    closePasswordForm: "关闭密码表单",
    currentPassword: "当前密码",
    newPassword: "新密码",
    confirmNewPassword: "确认新密码",
    updatePassword: "更新密码",
    skip: "跳过",
    gotIt: "知道了",
    finish: "完成",
    loading: "加载中",
    loginButton: "登录",
    creatingAccount: "正在创建账号...",
    loggingIn: "正在登录...",
    chooseLanguageOrNone: "继续前请选择一门语言或 None。",
    aiReviewConnected: "AI 批改已连接",
    aiReviewConnectedBody: "提交后会收到更深入的段落级批改和逐行改进建议，即使代码很短也会批改。",
    noConsoleOutput: "这个示例没有控制台输出。",
    homeworkSubmitted: "作业已提交。",
    finalLessonFinished: "你已经完成了这个 track 的最后一课。",
    keepMoving: "你可以继续学习开放课程。",
    allLessonsUnlocked: "所有课程已解锁。",
    allLessonsUnlockedBody: "你现在可以学习任意一天。需要反馈和记录时，请提交 HW Q1、HW Q2 和 HW Q3。",
    submitted: "已提交",
    lessonLockedTitle: "请先提交第 {day} 天作业，再打开本课。",
    lessonLockedMessage: "第 {day} 天已锁定。请先提交第 {previousDay} 天作业再继续。",
    courseLoadFailed: "课程数据加载失败",
    knownLanguage: "已有语言",
    target: "目标",
    code: "代码",
    blankLine: "空行",
    syntax: "语法",
    comparison: "{language} 对比",
    phraseBreakdown: "短语拆解",
    noSubmissionsYet: "还没有提交记录。",
    noSubmittedProgramSaved: "这个旧记录没有保存提交的程序文本。",
    noJudge0Saved: "这个旧提交没有保存 Judge0 结果。",
    judge0Unavailable: "这个提交无法使用 Judge0。",
    status: "状态",
    unknown: "未知",
    time: "时间",
    memory: "内存",
    stdout: "标准输出",
    stderr: "标准错误",
    compileOutput: "编译输出",
    message: "消息",
    noBuiltInChecker: "这个旧提交没有保存内置检查器结果。",
    assignmentScore: "作业评分",
    score: "分数",
    nonEmptyLines: "非空代码行",
    homeworkLabelsFound: "找到的作业标签",
    checks: "检查项",
    pass: "通过",
    fix: "需修改",
    noneLower: "无",
    mastery: "掌握度",
    masteryRating: "掌握度评级",
    masteryScale: "1 = 没有掌握，5 = 完全掌握",
    unrated: "未评级",
    weakestKnowledge: "最薄弱知识点",
    noWeakestKnowledge: "还没有评分作业。",
    popQuizSchedule: "POP 小测安排",
    noPopQuizSchedule: "提交作业后会生成间隔复习小测日期。",
    quizDue: "{date} 到期：第 {day} 天，间隔 {interval} 天后",
    viewSubmittedProgramAndReview: "查看提交程序和批改",
    submittedProgram: "提交的程序",
    judge0RunResult: "Judge0 运行结果",
    builtInCodeChecker: "内置代码检查器",
    whatToFixReview: "需要修改 / 批改反馈",
    loadingGuidance: "正在加载学习建议...",
    noGuidance: "暂时没有学习建议。",
    guidanceFailed: "学习建议加载失败",
    reviewing: "批改中",
    runningCode: "正在用 Judge0 运行代码，然后生成反馈...",
    submissionFailed: "提交失败",
    sendingFeedback: "正在发送反馈...",
    feedbackFailed: "反馈发送失败",
    feedbackSent: "反馈已发送，谢谢。",
    passwordsNoMatch: "两次输入的新密码不一致。",
    passwordTooShort: "新密码至少需要 8 个字符。",
    updatingPassword: "正在更新密码...",
    passwordUpdateFailed: "密码更新失败",
    passwordUpdated: "密码已更新。下次登录请使用新密码。",
    stepOf: "第 {current} 步，共 {total} 步",
    cppFoundationSubtitle: "C++ 基础 · 预备课程 · {days} 天",
    targetSubtitle: "以 {base} 为基础学习 {target} · {days} 天",
    syntaxArrow: "{base} 语法 → {target} 语法",
    languageSyntax: "{language} 语法",
    languageLineSyntax: "{language} 逐行语法",
    accountRequestFailed: "账号请求失败",
    linePrefix: "第",
    dayLabel: "第 {day} 天",
    tourAccountTitle: "账号工具",
    tourAccountText: "这里保存你的进度。你可以重新打开教程、修改密码、退出登录，管理员也可以查看用户和反馈。",
    tourFoundationTitle: "选择你的基础语言",
    tourFoundationText: "注册后，选择一门你已经会的语言。如果想从 C++ 基础开始，请选择 None。",
    tourTargetTitle: "选择目标语言",
    tourTargetText: "用这个菜单切换 CodeBridge 接下来教你的语言。",
    tourDayListTitle: "打开每日课程",
    tourDayListText: "这里是每日课程列表。滚动左侧栏可以看到所有天数。",
    tourLessonTitle: "学习课程",
    tourLessonText: "阅读已有语言桥梁、详细解释、逐行笔记和官方文档。",
    tourHomeworkTitle: "完成 HW Q1、Q2、Q3",
    tourHomeworkText: "每天有三个具体程序。按照题目要求的数字、计算和输出完成。",
    tourSubmitTitle: "提交作业",
    tourSubmitText: "上传文件或粘贴代码。提交后查看反馈，并和示例代码对比。",
    tourFeedbackTitle: "发送网站反馈",
    tourFeedbackText: "如果有内容损坏或令人困惑，用这个按钮把信息发给网站 owner。",
  },
  fr: {
    htmlLang: "fr",
    brandSubtitleDefault: "Base C++ vers plusieurs langages",
    totalProgress: "Progression totale",
    searchPlaceholder: "Rechercher un jour, un sujet ou une catégorie",
    interfaceLanguage: "Langue de l'interface",
    accountSaved: "Votre progression est enregistrée dans ce compte.",
    howToUse: "Mode d'emploi",
    changePassword: "Changer le mot de passe",
    adminDashboard: "Tableau d'administration",
    logOut: "Se déconnecter",
    targetLanguage: "Langage cible",
    changeLanguageExperience: "Changer l'expérience linguistique",
    cppFoundations: "Bases C++",
    cppTrackNotice: "Terminez ou changez de langage quand vous êtes prêt.",
    knowCppNow: "Je connais C++ maintenant",
    dailyCourseList: "Liste des cours quotidiens",
    account: "Compte",
    saveLearningData: "Enregistrer vos données d'apprentissage",
    saveLearningDataBody: "Inscrivez-vous ou connectez-vous pour lier vos choix de langue, le jour actuel, la progression des listes et les soumissions à votre compte.",
    accountAction: "Action du compte",
    register: "S'inscrire",
    logIn: "Connexion",
    name: "Nom",
    password: "Mot de passe",
    createAccount: "Créer un compte",
    languageExperienceCheck: "Vérification de l'expérience",
    languageExperienceTitle: "Quel langage savez-vous déjà utiliser ?",
    languageExperienceBody: "Choisissez un langage comme base. Le cours utilisera ce langage pour enseigner les autres. Choisissez None pour commencer par les bases C++.",
    knownProgrammingLanguages: "Langages de programmation connus",
    none: "None",
    continue: "Continuer",
    previousDay: "Jour précédent",
    nextDay: "Jour suivant",
    day: "Jour",
    checklist: "Liste",
    week: "Semaine",
    knownLanguageBridge: "Pont depuis le langage connu",
    syntaxBridge: "Pont syntaxique",
    knownLanguageSyntax: "Syntaxe du langage connu",
    targetSyntax: "Syntaxe cible",
    sampleInput: "Entrée d'exemple",
    expectedOutput: "Sortie / résultat attendu",
    sameIdeaTranslated: "La même idée est traduite ci-dessous",
    translationSteps: "Étapes de traduction",
    commonPitfalls: "Pièges fréquents",
    todaysTranslationDrill: "Exercice de traduction du jour",
    officialDocumentation: "Documentation officielle",
    detailedExplanation: "Explication détaillée",
    sampleCodeAfterSubmission: "Exemple de code après soumission",
    copyCode: "Copier le code",
    copied: "Copié",
    sampleCodeNote: "Soumettez d'abord votre devoir. Après la correction, utilisez cet exemple pour comparer la structure, la syntaxe et le style.",
    lineByLineSyntax: "Syntaxe ligne par ligne",
    lineByLineSyntaxNotes: "Notes de syntaxe ligne par ligne",
    todaysHomework: "Devoir du jour",
    dayByDayGuidance: "Conseils jour par jour",
    refresh: "Actualiser",
    today: "Aujourd'hui",
    learningHabits: "Habitudes d'apprentissage",
    focusAreas: "Points à travailler",
    nextStudyBlock: "Prochaine session",
    dailyChecklist: "Liste quotidienne",
    reset: "Réinitialiser",
    todaysAssignment: "Exercice du jour",
    uploadHomework: "Téléverser le devoir pour correction",
    optional: "Facultatif",
    homeworkFile: "Fichier du devoir",
    orPasteCode: "Ou coller le code",
    standardInput: "Entrée standard pour Judge0",
    stdinPlaceholder: "Facultatif. Mettez une valeur par ligne quand votre programme lit une entrée.",
    aiFocus: "Sur quoi l'IA doit-elle se concentrer ?",
    aiFocusPlaceholder: "Exemple : je ne suis pas sûr que ma récursion soit correcte.",
    submitAndReview: "Soumettre et corriger",
    reviewHistory: "Historique des corrections",
    feedback: "Commentaires",
    siteFeedback: "Commentaires sur le site",
    tellUsFixing: "Dites-nous ce qu'il faut corriger",
    closeFeedbackForm: "Fermer le formulaire de commentaires",
    feedbackType: "Type de commentaire",
    bugOrBrokenPage: "Bug ou page cassée",
    lessonOrHomeworkContent: "Contenu du cours ou du devoir",
    featureRequest: "Demande de fonctionnalité",
    other: "Autre",
    whatHappened: "Que s'est-il passé ?",
    feedbackPlaceholder: "Exemple : le devoir du jour 12 n'est pas clair parce que...",
    sendFeedback: "Envoyer",
    accountSecurity: "Sécurité du compte",
    changeYourPassword: "Changer votre mot de passe",
    closePasswordForm: "Fermer le formulaire de mot de passe",
    currentPassword: "Mot de passe actuel",
    newPassword: "Nouveau mot de passe",
    confirmNewPassword: "Confirmer le nouveau mot de passe",
    updatePassword: "Mettre à jour",
    skip: "Passer",
    gotIt: "J'ai compris",
    finish: "Terminer",
    loading: "Chargement",
    loginButton: "Se connecter",
    creatingAccount: "Création du compte...",
    loggingIn: "Connexion...",
    chooseLanguageOrNone: "Choisissez un langage ou None avant de continuer.",
    aiReviewConnected: "Correction IA connectée",
    aiReviewConnectedBody: "Les soumissions reçoivent une correction plus approfondie et des suggestions ligne par ligne, même pour un code court.",
    noConsoleOutput: "Aucune sortie console pour cet exemple.",
    homeworkSubmitted: "Devoir soumis.",
    finalLessonFinished: "Vous avez terminé la dernière leçon de ce parcours.",
    keepMoving: "Vous pouvez continuer dans le cours ouvert.",
    allLessonsUnlocked: "Toutes les leçons sont déverrouillées.",
    allLessonsUnlockedBody: "Vous pouvez étudier n'importe quel jour. Soumettez HW Q1, HW Q2 et HW Q3 quand vous voulez des commentaires et un historique.",
    submitted: "Soumis",
    lessonLockedTitle: "Soumettez le devoir du jour {day} avant d'ouvrir cette leçon.",
    lessonLockedMessage: "Le jour {day} est verrouillé. Soumettez le devoir du jour {previousDay} avant de continuer.",
    courseLoadFailed: "Échec du chargement du cours",
    knownLanguage: "Langage connu",
    target: "Cible",
    code: "Code",
    blankLine: "Ligne vide",
    syntax: "Syntaxe",
    comparison: "Comparaison avec {language}",
    phraseBreakdown: "Décomposition des expressions",
    noSubmissionsYet: "Aucune soumission pour le moment.",
    noSubmittedProgramSaved: "Aucun texte de programme n'a été enregistré pour cette ancienne soumission.",
    noJudge0Saved: "Aucun résultat Judge0 enregistré pour cette ancienne soumission.",
    judge0Unavailable: "Judge0 n'était pas disponible pour cette soumission.",
    status: "Statut",
    unknown: "Inconnu",
    time: "Temps",
    memory: "Mémoire",
    stdout: "Stdout",
    stderr: "Stderr",
    compileOutput: "Sortie de compilation",
    message: "Message",
    noBuiltInChecker: "Aucun résultat du vérificateur intégré pour cette ancienne soumission.",
    score: "Score",
    nonEmptyLines: "Lignes non vides",
    homeworkLabelsFound: "Étiquettes de devoir trouvées",
    checks: "Vérifications",
    pass: "OK",
    fix: "À corriger",
    noneLower: "aucun",
    assignmentScore: "Note du devoir",
    mastery: "Maîtrise",
    masteryRating: "Niveau de maîtrise",
    masteryScale: "1 = non maîtrisé, 5 = entièrement maîtrisé",
    unrated: "Non évalué",
    weakestKnowledge: "Point le plus faible",
    noWeakestKnowledge: "Aucun devoir noté pour le moment.",
    popQuizSchedule: "Calendrier des quiz POP",
    noPopQuizSchedule: "Soumettez un devoir pour générer des dates de quiz espacées.",
    quizDue: "À faire le {date} : jour {day} après {interval} jour(s)",
    viewSubmittedProgramAndReview: "Voir le programme soumis et la correction",
    submittedProgram: "Programme soumis",
    judge0RunResult: "Résultat Judge0",
    builtInCodeChecker: "Vérificateur intégré",
    whatToFixReview: "À corriger / commentaires",
    loadingGuidance: "Chargement des conseils...",
    noGuidance: "Aucun conseil disponible pour le moment.",
    guidanceFailed: "Échec du chargement des conseils",
    reviewing: "Correction",
    runningCode: "Exécution avec Judge0, puis génération des commentaires...",
    submissionFailed: "Échec de la soumission",
    sendingFeedback: "Envoi des commentaires...",
    feedbackFailed: "Échec de l'envoi",
    feedbackSent: "Commentaires envoyés. Merci.",
    passwordsNoMatch: "Les nouveaux mots de passe ne correspondent pas.",
    passwordTooShort: "Le nouveau mot de passe doit contenir au moins 8 caractères.",
    updatingPassword: "Mise à jour du mot de passe...",
    passwordUpdateFailed: "Échec de la mise à jour du mot de passe",
    passwordUpdated: "Mot de passe mis à jour. Utilisez le nouveau mot de passe lors de votre prochaine connexion.",
    stepOf: "Étape {current} sur {total}",
    cppFoundationSubtitle: "Bases C++ · parcours préalable · {days} jours",
    targetSubtitle: "Base {base} vers {target} · {days} jours",
    syntaxArrow: "Syntaxe {base} → syntaxe {target}",
    languageSyntax: "Syntaxe {language}",
    languageLineSyntax: "Syntaxe {language} ligne par ligne",
    accountRequestFailed: "Échec de la demande de compte",
    linePrefix: "L",
    dayLabel: "Jour {day}",
    tourAccountTitle: "Outils du compte",
    tourAccountText: "Cette zone enregistre votre progression. Vous pouvez rouvrir ce tutoriel, changer le mot de passe, vous déconnecter, et les administrateurs peuvent consulter les utilisateurs et les commentaires.",
    tourFoundationTitle: "Choisir votre base",
    tourFoundationText: "Après l'inscription, choisissez le langage que vous connaissez déjà. Choisissez None si vous voulez commencer par les bases C++.",
    tourTargetTitle: "Choisir un langage cible",
    tourTargetText: "Utilisez ce menu pour changer le langage que CodeBridge vous enseigne ensuite.",
    tourDayListTitle: "Ouvrir une leçon quotidienne",
    tourDayListText: "Voici la liste des cours quotidiens. Faites défiler la barre latérale gauche pour atteindre tous les jours.",
    tourLessonTitle: "Étudier la leçon",
    tourLessonText: "Lisez le pont depuis votre langage connu, l'explication détaillée, les notes ligne par ligne et la documentation officielle.",
    tourHomeworkTitle: "Faire HW Q1, Q2 et Q3",
    tourHomeworkText: "Chaque jour contient trois programmes concrets. Suivez les nombres, le calcul et les exigences de sortie.",
    tourSubmitTitle: "Soumettre le devoir",
    tourSubmitText: "Téléversez un fichier ou collez le code. Après la soumission, consultez les commentaires et comparez avec l'exemple de code.",
    tourFeedbackTitle: "Envoyer un commentaire",
    tourFeedbackText: "Utilisez ce bouton si quelque chose est cassé ou confus. Votre message sera envoyé au propriétaire du site.",
  },
  ko: {
    htmlLang: "ko",
    brandSubtitleDefault: "C++ 기초에서 여러 언어로",
    totalProgress: "전체 진행률",
    searchPlaceholder: "날짜, 주제 또는 카테고리 검색",
    interfaceLanguage: "인터페이스 언어",
    accountSaved: "학습 진행 상황이 이 계정에 저장됩니다.",
    howToUse: "사용 방법",
    changePassword: "비밀번호 변경",
    adminDashboard: "관리자 대시보드",
    logOut: "로그아웃",
    targetLanguage: "목표 언어",
    changeLanguageExperience: "언어 경험 변경",
    cppFoundations: "C++ 기초",
    cppTrackNotice: "다른 언어로 넘어갈 준비가 되면 완료하거나 전환하세요.",
    knowCppNow: "이제 C++를 알아요",
    dailyCourseList: "일일 강의 목록",
    account: "계정",
    saveLearningData: "학습 데이터 저장",
    saveLearningDataBody: "가입하거나 로그인하면 언어 선택, 현재 날짜, 체크리스트 진행률, 제출 기록이 계정에 연결됩니다.",
    accountAction: "계정 작업",
    register: "가입",
    logIn: "로그인",
    name: "이름",
    password: "비밀번호",
    createAccount: "계정 만들기",
    languageExperienceCheck: "언어 경험 확인",
    languageExperienceTitle: "이미 사용할 수 있는 프로그래밍 언어는 무엇인가요?",
    languageExperienceBody: "기초로 삼을 언어 하나를 선택하세요. 이 과정은 그 언어를 사용해 다른 언어를 가르칩니다. C++ 기초부터 시작하려면 None을 선택하세요.",
    knownProgrammingLanguages: "알고 있는 프로그래밍 언어",
    none: "None",
    continue: "계속",
    previousDay: "이전 날짜",
    nextDay: "다음 날짜",
    day: "일",
    checklist: "체크리스트",
    week: "주",
    knownLanguageBridge: "알고 있는 언어 연결",
    syntaxBridge: "문법 연결",
    knownLanguageSyntax: "알고 있는 언어 문법",
    targetSyntax: "목표 문법",
    sampleInput: "예시 입력",
    expectedOutput: "예상 출력 / 결과",
    sameIdeaTranslated: "같은 아이디어를 아래에 번역했습니다",
    translationSteps: "번역 단계",
    commonPitfalls: "자주 하는 실수",
    todaysTranslationDrill: "오늘의 번역 연습",
    officialDocumentation: "공식 문서",
    detailedExplanation: "자세한 설명",
    sampleCodeAfterSubmission: "제출 후 예시 코드",
    copyCode: "코드 복사",
    copied: "복사됨",
    sampleCodeNote: "먼저 과제를 제출하세요. 검토 후 이 예시로 구조, 문법, 스타일을 비교하세요.",
    lineByLineSyntax: "줄별 문법",
    lineByLineSyntaxNotes: "줄별 문법 노트",
    todaysHomework: "오늘의 숙제",
    dayByDayGuidance: "날짜별 학습 안내",
    refresh: "새로고침",
    today: "오늘",
    learningHabits: "학습 습관",
    focusAreas: "집중 영역",
    nextStudyBlock: "다음 학습 블록",
    dailyChecklist: "일일 체크리스트",
    reset: "초기화",
    todaysAssignment: "오늘의 과제",
    uploadHomework: "검토용 숙제 업로드",
    optional: "선택 사항",
    homeworkFile: "숙제 파일",
    orPasteCode: "또는 코드 붙여넣기",
    standardInput: "Judge0 실행기 표준 입력",
    stdinPlaceholder: "선택 사항. 프로그램이 입력을 읽는 경우 한 줄에 입력값 하나를 넣으세요.",
    aiFocus: "AI가 무엇에 집중할까요?",
    aiFocusPlaceholder: "예: 제 재귀가 맞는지 잘 모르겠습니다.",
    submitAndReview: "제출 및 검토",
    reviewHistory: "검토 기록",
    feedback: "피드백",
    siteFeedback: "사이트 피드백",
    tellUsFixing: "수정할 내용을 알려주세요",
    closeFeedbackForm: "피드백 양식 닫기",
    feedbackType: "피드백 유형",
    bugOrBrokenPage: "버그 또는 깨진 페이지",
    lessonOrHomeworkContent: "강의 또는 숙제 내용",
    featureRequest: "기능 요청",
    other: "기타",
    whatHappened: "무슨 일이 있었나요?",
    feedbackPlaceholder: "예: 12일차 숙제가 명확하지 않습니다. 이유는...",
    sendFeedback: "피드백 보내기",
    accountSecurity: "계정 보안",
    changeYourPassword: "비밀번호 변경",
    closePasswordForm: "비밀번호 양식 닫기",
    currentPassword: "현재 비밀번호",
    newPassword: "새 비밀번호",
    confirmNewPassword: "새 비밀번호 확인",
    updatePassword: "비밀번호 업데이트",
    skip: "건너뛰기",
    gotIt: "알겠습니다",
    finish: "완료",
    loading: "로딩 중",
    loginButton: "로그인",
    creatingAccount: "계정 생성 중...",
    loggingIn: "로그인 중...",
    chooseLanguageOrNone: "계속하기 전에 언어 하나 또는 None을 선택하세요.",
    aiReviewConnected: "AI 검토 연결됨",
    aiReviewConnectedBody: "제출물은 짧은 코드라도 더 깊은 문단별 검토와 줄별 개선 제안을 받습니다.",
    noConsoleOutput: "이 예시에는 콘솔 출력이 없습니다.",
    homeworkSubmitted: "숙제가 제출되었습니다.",
    finalLessonFinished: "이 트랙의 마지막 강의를 완료했습니다.",
    keepMoving: "열린 과정에서 계속 진행할 수 있습니다.",
    allLessonsUnlocked: "모든 강의가 잠금 해제되었습니다.",
    allLessonsUnlockedBody: "이제 원하는 날짜를 공부할 수 있습니다. 피드백과 기록이 필요하면 HW Q1, HW Q2, HW Q3를 제출하세요.",
    submitted: "제출됨",
    lessonLockedTitle: "이 강의를 열기 전에 {day}일차 숙제를 제출하세요.",
    lessonLockedMessage: "{day}일차가 잠겨 있습니다. 계속하려면 {previousDay}일차 숙제를 먼저 제출하세요.",
    courseLoadFailed: "과정 데이터를 불러오지 못했습니다",
    knownLanguage: "알고 있는 언어",
    target: "목표",
    code: "코드",
    blankLine: "빈 줄",
    syntax: "문법",
    comparison: "{language} 비교",
    phraseBreakdown: "구문 분석",
    noSubmissionsYet: "아직 제출 기록이 없습니다.",
    noSubmittedProgramSaved: "이전 기록에는 제출한 프로그램 텍스트가 저장되어 있지 않습니다.",
    noJudge0Saved: "이전 제출에는 Judge0 결과가 저장되어 있지 않습니다.",
    judge0Unavailable: "이 제출에는 Judge0을 사용할 수 없었습니다.",
    status: "상태",
    unknown: "알 수 없음",
    time: "시간",
    memory: "메모리",
    stdout: "표준 출력",
    stderr: "표준 오류",
    compileOutput: "컴파일 출력",
    message: "메시지",
    noBuiltInChecker: "이전 제출에는 내장 검사기 결과가 저장되어 있지 않습니다.",
    score: "점수",
    nonEmptyLines: "비어 있지 않은 줄",
    homeworkLabelsFound: "찾은 숙제 라벨",
    checks: "검사 항목",
    pass: "통과",
    fix: "수정",
    noneLower: "없음",
    assignmentScore: "과제 점수",
    mastery: "숙련도",
    masteryRating: "숙련도 평가",
    masteryScale: "1 = 미숙, 5 = 완전 숙련",
    unrated: "평가 없음",
    weakestKnowledge: "가장 약한 지식",
    noWeakestKnowledge: "아직 평가된 숙제가 없습니다.",
    popQuizSchedule: "POP 퀴즈 일정",
    noPopQuizSchedule: "숙제를 제출하면 간격 반복 POP 퀴즈 날짜가 생성됩니다.",
    quizDue: "{date} 마감: {interval}일 후 {day}일차",
    viewSubmittedProgramAndReview: "제출 프로그램 및 검토 보기",
    submittedProgram: "제출한 프로그램",
    judge0RunResult: "Judge0 실행 결과",
    builtInCodeChecker: "내장 코드 검사기",
    whatToFixReview: "수정할 내용 / 검토 피드백",
    loadingGuidance: "안내를 불러오는 중...",
    noGuidance: "아직 사용할 수 있는 안내가 없습니다.",
    guidanceFailed: "안내를 불러오지 못했습니다",
    reviewing: "검토 중",
    runningCode: "Judge0으로 코드를 실행한 뒤 피드백을 생성하는 중...",
    submissionFailed: "제출 실패",
    sendingFeedback: "피드백 보내는 중...",
    feedbackFailed: "피드백 전송 실패",
    feedbackSent: "피드백을 보냈습니다. 감사합니다.",
    passwordsNoMatch: "새 비밀번호가 일치하지 않습니다.",
    passwordTooShort: "새 비밀번호는 최소 8자여야 합니다.",
    updatingPassword: "비밀번호 업데이트 중...",
    passwordUpdateFailed: "비밀번호 업데이트 실패",
    passwordUpdated: "비밀번호가 업데이트되었습니다. 다음 로그인 때 새 비밀번호를 사용하세요.",
    stepOf: "{total}단계 중 {current}단계",
    cppFoundationSubtitle: "C++ 기초 · 선수 과정 · {days}일",
    targetSubtitle: "{base} 기초에서 {target}까지 · {days}일",
    syntaxArrow: "{base} 문법 → {target} 문법",
    languageSyntax: "{language} 문법",
    languageLineSyntax: "{language} 줄별 문법",
    accountRequestFailed: "계정 요청 실패",
    linePrefix: "L",
    dayLabel: "{day}일차",
    tourAccountTitle: "계정 도구",
    tourAccountText: "이 영역은 진행 상황을 저장합니다. 튜토리얼을 다시 열고, 비밀번호를 바꾸고, 로그아웃할 수 있으며 관리자는 사용자와 피드백을 확인할 수 있습니다.",
    tourFoundationTitle: "기초 언어 선택",
    tourFoundationText: "가입 후 이미 알고 있는 언어 하나를 선택하세요. C++ 기초부터 시작하려면 None을 선택하세요.",
    tourTargetTitle: "목표 언어 선택",
    tourTargetText: "이 메뉴로 CodeBridge가 다음에 가르칠 언어를 전환하세요.",
    tourDayListTitle: "일일 강의 열기",
    tourDayListText: "여기는 일일 강의 목록입니다. 왼쪽 사이드바를 스크롤하면 모든 날짜를 볼 수 있습니다.",
    tourLessonTitle: "강의 학습",
    tourLessonText: "알고 있는 언어 연결, 자세한 설명, 줄별 노트, 공식 문서를 읽으세요.",
    tourHomeworkTitle: "HW Q1, Q2, Q3 수행",
    tourHomeworkText: "매일 세 개의 구체적인 프로그램이 있습니다. 정확한 숫자, 계산, 출력 요구사항을 따르세요.",
    tourSubmitTitle: "숙제 제출",
    tourSubmitText: "파일을 업로드하거나 코드를 붙여넣으세요. 제출 후 피드백을 확인하고 예시 코드와 비교하세요.",
    tourFeedbackTitle: "사이트 피드백 보내기",
    tourFeedbackText: "무언가 깨졌거나 혼란스러우면 이 버튼을 사용하세요. 메시지는 사이트 소유자에게 전달됩니다.",
  },
  ja: {
    htmlLang: "ja",
    brandSubtitleDefault: "C++ の基礎から複数の言語へ",
    totalProgress: "全体の進捗",
    searchPlaceholder: "日、トピック、カテゴリを検索",
    interfaceLanguage: "インターフェース言語",
    accountSaved: "学習の進捗はこのアカウントに保存されます。",
    howToUse: "使い方",
    changePassword: "パスワード変更",
    adminDashboard: "管理ダッシュボード",
    logOut: "ログアウト",
    targetLanguage: "目標言語",
    changeLanguageExperience: "言語経験を変更",
    cppFoundations: "C++ 基礎",
    cppTrackNotice: "別の言語に進む準備ができたら、完了または切り替えてください。",
    knowCppNow: "今は C++ がわかります",
    dailyCourseList: "毎日のコース一覧",
    account: "アカウント",
    saveLearningData: "学習データを保存",
    saveLearningDataBody: "登録またはログインすると、言語選択、現在の日、チェックリスト進捗、提出履歴が自分のアカウントに紐づきます。",
    accountAction: "アカウント操作",
    register: "登録",
    logIn: "ログイン",
    name: "名前",
    password: "パスワード",
    createAccount: "アカウント作成",
    languageExperienceCheck: "言語経験チェック",
    languageExperienceTitle: "すでに使えるプログラミング言語はどれですか？",
    languageExperienceBody: "基礎にする言語を 1 つ選んでください。このコースはその言語を使って他の言語を教えます。C++ 基礎から始める場合は None を選んでください。",
    knownProgrammingLanguages: "知っているプログラミング言語",
    none: "None",
    continue: "続ける",
    previousDay: "前の日",
    nextDay: "次の日",
    day: "日",
    checklist: "チェックリスト",
    week: "週",
    knownLanguageBridge: "既知言語ブリッジ",
    syntaxBridge: "構文ブリッジ",
    knownLanguageSyntax: "既知言語の構文",
    targetSyntax: "目標構文",
    sampleInput: "サンプル入力",
    expectedOutput: "期待される出力 / 結果",
    sameIdeaTranslated: "同じ考え方を下に翻訳しています",
    translationSteps: "翻訳手順",
    commonPitfalls: "よくある落とし穴",
    todaysTranslationDrill: "今日の翻訳練習",
    officialDocumentation: "公式ドキュメント",
    detailedExplanation: "詳しい説明",
    sampleCodeAfterSubmission: "提出後のサンプルコード",
    copyCode: "コードをコピー",
    copied: "コピーしました",
    sampleCodeNote: "まず課題を提出してください。レビュー後、このサンプルで構造、構文、スタイルを比較できます。",
    lineByLineSyntax: "行ごとの構文",
    lineByLineSyntaxNotes: "行ごとの構文ノート",
    todaysHomework: "今日の宿題",
    dayByDayGuidance: "日ごとの学習ガイド",
    refresh: "更新",
    today: "今日",
    learningHabits: "学習習慣",
    focusAreas: "重点領域",
    nextStudyBlock: "次の学習ブロック",
    dailyChecklist: "毎日のチェックリスト",
    reset: "リセット",
    todaysAssignment: "今日の課題",
    uploadHomework: "レビュー用に宿題をアップロード",
    optional: "任意",
    homeworkFile: "宿題ファイル",
    orPasteCode: "またはコードを貼り付け",
    standardInput: "Judge0 ランナーの標準入力",
    stdinPlaceholder: "任意。プログラムが入力を読む場合は、1 行に 1 つの入力値を入れてください。",
    aiFocus: "AI は何に注目すべきですか？",
    aiFocusPlaceholder: "例: 再帰が正しいか自信がありません。",
    submitAndReview: "提出してレビュー",
    reviewHistory: "レビュー履歴",
    feedback: "フィードバック",
    siteFeedback: "サイトのフィードバック",
    tellUsFixing: "修正が必要な内容を教えてください",
    closeFeedbackForm: "フィードバックフォームを閉じる",
    feedbackType: "フィードバックの種類",
    bugOrBrokenPage: "バグまたは壊れたページ",
    lessonOrHomeworkContent: "レッスンまたは宿題の内容",
    featureRequest: "機能リクエスト",
    other: "その他",
    whatHappened: "何が起きましたか？",
    feedbackPlaceholder: "例: 12 日目の宿題が不明確です。理由は...",
    sendFeedback: "フィードバックを送信",
    accountSecurity: "アカウントのセキュリティ",
    changeYourPassword: "パスワードを変更",
    closePasswordForm: "パスワードフォームを閉じる",
    currentPassword: "現在のパスワード",
    newPassword: "新しいパスワード",
    confirmNewPassword: "新しいパスワードを確認",
    updatePassword: "パスワードを更新",
    skip: "スキップ",
    gotIt: "わかりました",
    finish: "完了",
    loading: "読み込み中",
    loginButton: "ログイン",
    creatingAccount: "アカウントを作成中...",
    loggingIn: "ログイン中...",
    chooseLanguageOrNone: "続ける前に言語を 1 つ、または None を選んでください。",
    aiReviewConnected: "AI レビュー接続済み",
    aiReviewConnectedBody: "提出物には、短いコードでも段落単位の詳しいレビューと行ごとの改善提案が届きます。",
    noConsoleOutput: "この例にはコンソール出力がありません。",
    homeworkSubmitted: "宿題が提出されました。",
    finalLessonFinished: "このトラックの最後のレッスンを完了しました。",
    keepMoving: "公開されているコースを続けられます。",
    allLessonsUnlocked: "すべてのレッスンが解除されています。",
    allLessonsUnlockedBody: "今はどの日でも学習できます。フィードバックと履歴が必要なときに HW Q1、HW Q2、HW Q3 を提出してください。",
    submitted: "提出済み",
    lessonLockedTitle: "このレッスンを開く前に {day} 日目の宿題を提出してください。",
    lessonLockedMessage: "{day} 日目はロックされています。続ける前に {previousDay} 日目の宿題を提出してください。",
    courseLoadFailed: "コースデータの読み込みに失敗しました",
    knownLanguage: "既知言語",
    target: "目標",
    code: "コード",
    blankLine: "空行",
    syntax: "構文",
    comparison: "{language} との比較",
    phraseBreakdown: "フレーズ分解",
    noSubmissionsYet: "まだ提出はありません。",
    noSubmittedProgramSaved: "この古い記録には提出プログラムの本文が保存されていません。",
    noJudge0Saved: "この古い提出には Judge0 の結果が保存されていません。",
    judge0Unavailable: "この提出では Judge0 を利用できませんでした。",
    status: "状態",
    unknown: "不明",
    time: "時間",
    memory: "メモリ",
    stdout: "標準出力",
    stderr: "標準エラー",
    compileOutput: "コンパイル出力",
    message: "メッセージ",
    noBuiltInChecker: "この古い提出には内蔵チェッカーの結果が保存されていません。",
    score: "スコア",
    nonEmptyLines: "空でない行",
    homeworkLabelsFound: "見つかった宿題ラベル",
    checks: "チェック",
    pass: "合格",
    fix: "修正",
    noneLower: "なし",
    assignmentScore: "課題スコア",
    mastery: "習熟度",
    masteryRating: "習熟度評価",
    masteryScale: "1 = 未習熟、5 = 完全に習熟",
    unrated: "未評価",
    weakestKnowledge: "最も弱い知識",
    noWeakestKnowledge: "まだ評価済みの宿題はありません。",
    popQuizSchedule: "POP クイズ予定",
    noPopQuizSchedule: "宿題を提出すると、間隔復習用の POP クイズ日程が生成されます。",
    quizDue: "{date} 期限: {interval} 日後の {day} 日目",
    viewSubmittedProgramAndReview: "提出プログラムとレビューを見る",
    submittedProgram: "提出プログラム",
    judge0RunResult: "Judge0 実行結果",
    builtInCodeChecker: "内蔵コードチェッカー",
    whatToFixReview: "修正点 / レビューフィードバック",
    loadingGuidance: "ガイドを読み込み中...",
    noGuidance: "まだ利用できるガイドはありません。",
    guidanceFailed: "ガイドの読み込みに失敗しました",
    reviewing: "レビュー中",
    runningCode: "Judge0 でコードを実行し、フィードバックを生成しています...",
    submissionFailed: "提出に失敗しました",
    sendingFeedback: "フィードバックを送信中...",
    feedbackFailed: "フィードバックの送信に失敗しました",
    feedbackSent: "フィードバックを送信しました。ありがとうございます。",
    passwordsNoMatch: "新しいパスワードが一致しません。",
    passwordTooShort: "新しいパスワードは 8 文字以上にしてください。",
    updatingPassword: "パスワードを更新中...",
    passwordUpdateFailed: "パスワード更新に失敗しました",
    passwordUpdated: "パスワードが更新されました。次回ログイン時は新しいパスワードを使用してください。",
    stepOf: "{total} 中 {current} ステップ",
    cppFoundationSubtitle: "C++ 基礎 · 前提トラック · {days} 日",
    targetSubtitle: "{base} の基礎から {target} へ · {days} 日",
    syntaxArrow: "{base} 構文 → {target} 構文",
    languageSyntax: "{language} 構文",
    languageLineSyntax: "{language} 行ごとの構文",
    accountRequestFailed: "アカウントリクエストに失敗しました",
    linePrefix: "L",
    dayLabel: "{day} 日目",
    tourAccountTitle: "アカウントツール",
    tourAccountText: "ここに進捗が保存されます。チュートリアルを再度開いたり、パスワードを変更したり、ログアウトできます。管理者はユーザーとフィードバックを確認できます。",
    tourFoundationTitle: "基礎を選択",
    tourFoundationText: "登録後、すでに知っている言語を 1 つ選んでください。C++ 基礎から始めたい場合は None を選んでください。",
    tourTargetTitle: "目標言語を選択",
    tourTargetText: "このメニューで CodeBridge が次に教える言語を切り替えます。",
    tourDayListTitle: "毎日のレッスンを開く",
    tourDayListText: "これは毎日のコース一覧です。左サイドバーをスクロールするとすべての日にアクセスできます。",
    tourLessonTitle: "レッスンを学習",
    tourLessonText: "既知言語からのブリッジ、詳しい説明、行ごとのノート、公式ドキュメントを読みましょう。",
    tourHomeworkTitle: "HW Q1、Q2、Q3 を行う",
    tourHomeworkText: "毎日 3 つの具体的なプログラムがあります。指定された数値、計算、出力要件に従ってください。",
    tourSubmitTitle: "宿題を提出",
    tourSubmitText: "ファイルをアップロードするかコードを貼り付けてください。提出後、フィードバックを確認し、サンプルコードと比較します。",
    tourFeedbackTitle: "サイトのフィードバックを送信",
    tourFeedbackText: "壊れている箇所やわかりにくい箇所があれば、このボタンを使ってください。メッセージはサイト所有者に送られます。",
  },
  de: {
    htmlLang: "de",
    brandSubtitleDefault: "Von C++-Grundlagen zu mehreren Sprachen",
    totalProgress: "Gesamtfortschritt",
    searchPlaceholder: "Tag, Thema oder Kategorie suchen",
    interfaceLanguage: "Oberflächensprache",
    accountSaved: "Dein Fortschritt wird in diesem Konto gespeichert.",
    howToUse: "Anleitung",
    changePassword: "Passwort ändern",
    adminDashboard: "Admin-Dashboard",
    logOut: "Abmelden",
    targetLanguage: "Zielsprache",
    changeLanguageExperience: "Spracherfahrung ändern",
    cppFoundations: "C++-Grundlagen",
    cppTrackNotice: "Schließe den Kurs ab oder wechsle, wenn du bereit für eine andere Sprache bist.",
    knowCppNow: "Ich kann jetzt C++",
    dailyCourseList: "Tägliche Kursliste",
    account: "Konto",
    saveLearningData: "Lerndaten speichern",
    saveLearningDataBody: "Registriere dich oder melde dich an, damit Sprachwahl, aktueller Tag, Checklistenfortschritt und Abgaben mit deinem Konto verbunden bleiben.",
    accountAction: "Kontoaktion",
    register: "Registrieren",
    logIn: "Anmelden",
    name: "Name",
    password: "Passwort",
    createAccount: "Konto erstellen",
    languageExperienceCheck: "Prüfung der Spracherfahrung",
    languageExperienceTitle: "Welche Programmiersprache kannst du bereits verwenden?",
    languageExperienceBody: "Wähle eine Sprache als Grundlage. Der Kurs nutzt diese Sprache, um die anderen Sprachen zu erklären. Wähle None, um mit C++-Grundlagen zu starten.",
    knownProgrammingLanguages: "Bekannte Programmiersprachen",
    none: "None",
    continue: "Weiter",
    previousDay: "Vorheriger Tag",
    nextDay: "Nächster Tag",
    day: "Tag",
    checklist: "Checkliste",
    week: "Woche",
    knownLanguageBridge: "Brücke aus bekannter Sprache",
    syntaxBridge: "Syntaxbrücke",
    knownLanguageSyntax: "Syntax der bekannten Sprache",
    targetSyntax: "Zielsprache-Syntax",
    sampleInput: "Beispieleingabe",
    expectedOutput: "Erwartete Ausgabe / Ergebnis",
    sameIdeaTranslated: "Dieselbe Idee ist unten übersetzt",
    translationSteps: "Übersetzungsschritte",
    commonPitfalls: "Häufige Fehler",
    todaysTranslationDrill: "Heutige Übersetzungsübung",
    officialDocumentation: "Offizielle Dokumentation",
    detailedExplanation: "Detaillierte Erklärung",
    sampleCodeAfterSubmission: "Beispielcode nach der Abgabe",
    copyCode: "Code kopieren",
    copied: "Kopiert",
    sampleCodeNote: "Reiche zuerst deine Aufgabe ein. Nach der Prüfung kannst du dieses Beispiel nutzen, um Struktur, Syntax und Stil zu vergleichen.",
    lineByLineSyntax: "Syntax Zeile für Zeile",
    lineByLineSyntaxNotes: "Syntaxnotizen Zeile für Zeile",
    todaysHomework: "Heutige Hausaufgabe",
    dayByDayGuidance: "Tägliche Lernhinweise",
    refresh: "Aktualisieren",
    today: "Heute",
    learningHabits: "Lerngewohnheiten",
    focusAreas: "Schwerpunkte",
    nextStudyBlock: "Nächster Lernblock",
    dailyChecklist: "Tägliche Checkliste",
    reset: "Zurücksetzen",
    todaysAssignment: "Heutige Aufgabe",
    uploadHomework: "Hausaufgabe zur Prüfung hochladen",
    optional: "Optional",
    homeworkFile: "Hausaufgabendatei",
    orPasteCode: "Oder Code einfügen",
    standardInput: "Standardeingabe für Judge0",
    stdinPlaceholder: "Optional. Gib pro Zeile einen Eingabewert ein, wenn dein Programm Eingaben liest.",
    aiFocus: "Worauf soll die KI achten?",
    aiFocusPlaceholder: "Beispiel: Ich bin unsicher, ob meine Rekursion korrekt ist.",
    submitAndReview: "Einreichen und prüfen",
    reviewHistory: "Prüfverlauf",
    feedback: "Feedback",
    siteFeedback: "Website-Feedback",
    tellUsFixing: "Sag uns, was korrigiert werden muss",
    closeFeedbackForm: "Feedbackformular schließen",
    feedbackType: "Feedbacktyp",
    bugOrBrokenPage: "Fehler oder defekte Seite",
    lessonOrHomeworkContent: "Lektions- oder Hausaufgabeninhalt",
    featureRequest: "Funktionswunsch",
    other: "Sonstiges",
    whatHappened: "Was ist passiert?",
    feedbackPlaceholder: "Beispiel: Die Hausaufgabe von Tag 12 ist unklar, weil...",
    sendFeedback: "Feedback senden",
    accountSecurity: "Kontosicherheit",
    changeYourPassword: "Passwort ändern",
    closePasswordForm: "Passwortformular schließen",
    currentPassword: "Aktuelles Passwort",
    newPassword: "Neues Passwort",
    confirmNewPassword: "Neues Passwort bestätigen",
    updatePassword: "Passwort aktualisieren",
    skip: "Überspringen",
    gotIt: "Verstanden",
    finish: "Fertig",
    loading: "Lädt",
    loginButton: "Anmelden",
    creatingAccount: "Konto wird erstellt...",
    loggingIn: "Anmeldung läuft...",
    chooseLanguageOrNone: "Wähle eine Sprache oder None, bevor du fortfährst.",
    aiReviewConnected: "KI-Prüfung verbunden",
    aiReviewConnectedBody: "Abgaben erhalten eine tiefere absatzweise Prüfung und zeilenweise Verbesserungsvorschläge, auch bei kurzem Code.",
    noConsoleOutput: "Dieses Beispiel hat keine Konsolenausgabe.",
    homeworkSubmitted: "Hausaufgabe eingereicht.",
    finalLessonFinished: "Du hast die letzte Lektion dieses Tracks abgeschlossen.",
    keepMoving: "Du kannst im offenen Kurs weiterarbeiten.",
    allLessonsUnlocked: "Alle Lektionen sind freigeschaltet.",
    allLessonsUnlockedBody: "Du kannst jetzt jeden Tag lernen. Reiche HW Q1, HW Q2 und HW Q3 ein, wenn du Feedback und Verlauf möchtest.",
    submitted: "Eingereicht",
    lessonLockedTitle: "Reiche die Hausaufgabe von Tag {day} ein, bevor du diese Lektion öffnest.",
    lessonLockedMessage: "Tag {day} ist gesperrt. Reiche zuerst die Hausaufgabe von Tag {previousDay} ein.",
    courseLoadFailed: "Kursdaten konnten nicht geladen werden",
    knownLanguage: "Bekannte Sprache",
    target: "Ziel",
    code: "Code",
    blankLine: "Leerzeile",
    syntax: "Syntax",
    comparison: "{language}-Vergleich",
    phraseBreakdown: "Phrasenaufschlüsselung",
    noSubmissionsYet: "Noch keine Abgaben.",
    noSubmittedProgramSaved: "Für diesen älteren Datensatz wurde kein Programmtext gespeichert.",
    noJudge0Saved: "Für diese ältere Abgabe wurde kein Judge0-Ergebnis gespeichert.",
    judge0Unavailable: "Judge0 war für diese Abgabe nicht verfügbar.",
    status: "Status",
    unknown: "Unbekannt",
    time: "Zeit",
    memory: "Speicher",
    stdout: "Stdout",
    stderr: "Stderr",
    compileOutput: "Compiler-Ausgabe",
    message: "Nachricht",
    noBuiltInChecker: "Für diese ältere Abgabe wurde kein Ergebnis des integrierten Prüfers gespeichert.",
    score: "Punktzahl",
    nonEmptyLines: "Nicht leere Zeilen",
    homeworkLabelsFound: "Gefundene Hausaufgabenlabels",
    checks: "Prüfungen",
    pass: "OK",
    fix: "Korrigieren",
    noneLower: "keine",
    viewSubmittedProgramAndReview: "Eingereichtes Programm und Prüfung ansehen",
    submittedProgram: "Eingereichtes Programm",
    judge0RunResult: "Judge0-Ausführungsergebnis",
    builtInCodeChecker: "Integrierter Codeprüfer",
    whatToFixReview: "Zu korrigieren / Prüfungsfeedback",
    loadingGuidance: "Hinweise werden geladen...",
    noGuidance: "Noch keine Hinweise verfügbar.",
    guidanceFailed: "Hinweise konnten nicht geladen werden",
    reviewing: "Prüfung läuft",
    runningCode: "Code wird mit Judge0 ausgeführt, danach wird Feedback erzeugt...",
    submissionFailed: "Abgabe fehlgeschlagen",
    sendingFeedback: "Feedback wird gesendet...",
    feedbackFailed: "Feedback konnte nicht gesendet werden",
    feedbackSent: "Feedback gesendet. Danke.",
    passwordsNoMatch: "Die neuen Passwörter stimmen nicht überein.",
    passwordTooShort: "Das neue Passwort muss mindestens 8 Zeichen lang sein.",
    updatingPassword: "Passwort wird aktualisiert...",
    passwordUpdateFailed: "Passwortaktualisierung fehlgeschlagen",
    passwordUpdated: "Passwort aktualisiert. Verwende beim nächsten Login das neue Passwort.",
    stepOf: "Schritt {current} von {total}",
    cppFoundationSubtitle: "C++-Grundlagen · Vorkurs · {days} Tage",
    targetSubtitle: "{base}-Grundlage zu {target} · {days} Tage",
    syntaxArrow: "{base}-Syntax → {target}-Syntax",
    languageSyntax: "{language}-Syntax",
    languageLineSyntax: "{language}-Syntax Zeile für Zeile",
    accountRequestFailed: "Kontoanfrage fehlgeschlagen",
    linePrefix: "Z",
    dayLabel: "Tag {day}",
    tourAccountTitle: "Kontowerkzeuge",
    tourAccountText: "Dieser Bereich speichert deinen Fortschritt. Du kannst das Tutorial erneut öffnen, dein Passwort ändern, dich abmelden, und Admins können Nutzer und Feedback prüfen.",
    tourFoundationTitle: "Grundlage wählen",
    tourFoundationText: "Wähle nach der Registrierung eine Sprache, die du bereits kennst. Wähle None, wenn du mit C++-Grundlagen beginnen möchtest.",
    tourTargetTitle: "Zielsprache wählen",
    tourTargetText: "Mit diesem Menü wechselst du, welche Sprache CodeBridge als Nächstes lehrt.",
    tourDayListTitle: "Tägliche Lektion öffnen",
    tourDayListText: "Dies ist die tägliche Kursliste. Scrolle in der linken Seitenleiste, um jeden Tag zu erreichen.",
    tourLessonTitle: "Lektion lernen",
    tourLessonText: "Lies die Brücke aus deiner bekannten Sprache, die detaillierte Erklärung, die Zeilennotizen und die offizielle Dokumentation.",
    tourHomeworkTitle: "HW Q1, Q2 und Q3 bearbeiten",
    tourHomeworkText: "Jeder Tag enthält drei konkrete Programme. Befolge die genauen Zahlen, Berechnungen und Ausgabeanforderungen.",
    tourSubmitTitle: "Hausaufgabe einreichen",
    tourSubmitText: "Lade eine Datei hoch oder füge Code ein. Prüfe nach dem Einreichen das Feedback und vergleiche mit dem Beispielcode.",
    tourFeedbackTitle: "Website-Feedback senden",
    tourFeedbackText: "Nutze diesen Button, wenn etwas defekt oder unklar ist. Deine Nachricht geht an den Website-Betreiber.",
  },
  pt: {
    htmlLang: "pt",
    brandSubtitleDefault: "Da base em C++ para várias linguagens",
    totalProgress: "Progresso total",
    searchPlaceholder: "Pesquisar dia, tópico ou categoria",
    interfaceLanguage: "Idioma da interface",
    accountSaved: "Seu progresso é salvo nesta conta.",
    howToUse: "Como usar",
    changePassword: "Alterar senha",
    adminDashboard: "Painel administrativo",
    logOut: "Sair",
    targetLanguage: "Linguagem alvo",
    changeLanguageExperience: "Alterar experiência com linguagens",
    cppFoundations: "Fundamentos de C++",
    cppTrackNotice: "Conclua ou troque quando estiver pronto para outra linguagem.",
    knowCppNow: "Agora eu sei C++",
    dailyCourseList: "Lista diária do curso",
    account: "Conta",
    saveLearningData: "Salvar seus dados de aprendizagem",
    saveLearningDataBody: "Cadastre-se ou entre para manter escolhas de linguagem, dia atual, progresso da lista e envios vinculados à sua conta.",
    accountAction: "Ação da conta",
    register: "Cadastrar",
    logIn: "Entrar",
    name: "Nome",
    password: "Senha",
    createAccount: "Criar conta",
    languageExperienceCheck: "Verificação de experiência",
    languageExperienceTitle: "Qual linguagem de programação você já sabe usar?",
    languageExperienceBody: "Escolha uma linguagem como base. O curso usará essa linguagem para ensinar as outras. Escolha None para começar pelos fundamentos de C++.",
    knownProgrammingLanguages: "Linguagens de programação conhecidas",
    none: "None",
    continue: "Continuar",
    previousDay: "Dia anterior",
    nextDay: "Próximo dia",
    day: "Dia",
    checklist: "Lista",
    week: "Semana",
    knownLanguageBridge: "Ponte a partir da linguagem conhecida",
    syntaxBridge: "Ponte de sintaxe",
    knownLanguageSyntax: "Sintaxe da linguagem conhecida",
    targetSyntax: "Sintaxe alvo",
    sampleInput: "Entrada de exemplo",
    expectedOutput: "Saída / resultado esperado",
    sameIdeaTranslated: "A mesma ideia traduzida abaixo",
    translationSteps: "Etapas de tradução",
    commonPitfalls: "Erros comuns",
    todaysTranslationDrill: "Exercício de tradução de hoje",
    officialDocumentation: "Documentação oficial",
    detailedExplanation: "Explicação detalhada",
    sampleCodeAfterSubmission: "Código de exemplo após o envio",
    copyCode: "Copiar código",
    copied: "Copiado",
    sampleCodeNote: "Envie sua tarefa primeiro. Depois da revisão, use este exemplo para comparar estrutura, sintaxe e estilo.",
    lineByLineSyntax: "Sintaxe linha por linha",
    lineByLineSyntaxNotes: "Notas de sintaxe linha por linha",
    todaysHomework: "Tarefa de hoje",
    dayByDayGuidance: "Orientação dia a dia",
    refresh: "Atualizar",
    today: "Hoje",
    learningHabits: "Hábitos de estudo",
    focusAreas: "Áreas de foco",
    nextStudyBlock: "Próximo bloco de estudo",
    dailyChecklist: "Lista diária",
    reset: "Redefinir",
    todaysAssignment: "Atividade de hoje",
    uploadHomework: "Enviar tarefa para revisão",
    optional: "Opcional",
    homeworkFile: "Arquivo da tarefa",
    orPasteCode: "Ou cole o código",
    standardInput: "Entrada padrão para o executor Judge0",
    stdinPlaceholder: "Opcional. Coloque um valor por linha quando seu programa ler entrada.",
    aiFocus: "Em que a IA deve focar?",
    aiFocusPlaceholder: "Exemplo: não tenho certeza se minha recursão está correta.",
    submitAndReview: "Enviar e revisar",
    reviewHistory: "Histórico de revisões",
    feedback: "Feedback",
    siteFeedback: "Feedback do site",
    tellUsFixing: "Diga o que precisa ser corrigido",
    closeFeedbackForm: "Fechar formulário de feedback",
    feedbackType: "Tipo de feedback",
    bugOrBrokenPage: "Erro ou página quebrada",
    lessonOrHomeworkContent: "Conteúdo da lição ou tarefa",
    featureRequest: "Pedido de recurso",
    other: "Outro",
    whatHappened: "O que aconteceu?",
    feedbackPlaceholder: "Exemplo: a tarefa do Dia 12 não está clara porque...",
    sendFeedback: "Enviar feedback",
    accountSecurity: "Segurança da conta",
    changeYourPassword: "Alterar sua senha",
    closePasswordForm: "Fechar formulário de senha",
    currentPassword: "Senha atual",
    newPassword: "Nova senha",
    confirmNewPassword: "Confirmar nova senha",
    updatePassword: "Atualizar senha",
    skip: "Pular",
    gotIt: "Entendi",
    finish: "Concluir",
    loading: "Carregando",
    loginButton: "Entrar",
    creatingAccount: "Criando conta...",
    loggingIn: "Entrando...",
    chooseLanguageOrNone: "Escolha uma linguagem ou None antes de continuar.",
    aiReviewConnected: "Revisão por IA conectada",
    aiReviewConnectedBody: "Envios recebem revisão mais profunda por parágrafo e sugestões linha por linha, mesmo para códigos curtos.",
    noConsoleOutput: "Não há saída de console neste exemplo.",
    homeworkSubmitted: "Tarefa enviada.",
    finalLessonFinished: "Você concluiu a última lição desta trilha.",
    keepMoving: "Você pode continuar no curso aberto.",
    allLessonsUnlocked: "Todas as lições estão desbloqueadas.",
    allLessonsUnlockedBody: "Agora você pode estudar qualquer dia. Envie HW Q1, HW Q2 e HW Q3 quando quiser feedback e histórico.",
    submitted: "Enviado",
    lessonLockedTitle: "Envie a tarefa do Dia {day} antes de abrir esta lição.",
    lessonLockedMessage: "O Dia {day} está bloqueado. Envie a tarefa do Dia {previousDay} antes de continuar.",
    courseLoadFailed: "Falha ao carregar os dados do curso",
    knownLanguage: "Linguagem conhecida",
    target: "Alvo",
    code: "Código",
    blankLine: "Linha em branco",
    syntax: "Sintaxe",
    comparison: "Comparação com {language}",
    phraseBreakdown: "Detalhamento de frases",
    noSubmissionsYet: "Ainda não há envios.",
    noSubmittedProgramSaved: "Nenhum texto do programa foi salvo para este registro antigo.",
    noJudge0Saved: "Nenhum resultado do Judge0 foi salvo para este envio antigo.",
    judge0Unavailable: "O Judge0 não estava disponível para este envio.",
    status: "Status",
    unknown: "Desconhecido",
    time: "Tempo",
    memory: "Memória",
    stdout: "Stdout",
    stderr: "Stderr",
    compileOutput: "Saída de compilação",
    message: "Mensagem",
    noBuiltInChecker: "Nenhum resultado do verificador interno foi salvo para este envio antigo.",
    score: "Pontuação",
    nonEmptyLines: "Linhas não vazias",
    homeworkLabelsFound: "Rótulos de tarefa encontrados",
    checks: "Verificações",
    pass: "PASSOU",
    fix: "CORRIGIR",
    noneLower: "nenhum",
    viewSubmittedProgramAndReview: "Ver programa enviado e revisão",
    submittedProgram: "Programa enviado",
    judge0RunResult: "Resultado da execução Judge0",
    builtInCodeChecker: "Verificador de código interno",
    whatToFixReview: "O que corrigir / feedback da revisão",
    loadingGuidance: "Carregando orientação...",
    noGuidance: "Ainda não há orientação disponível.",
    guidanceFailed: "Falha ao carregar orientação",
    reviewing: "Revisando",
    runningCode: "Executando código com Judge0 e gerando feedback...",
    submissionFailed: "Falha no envio",
    sendingFeedback: "Enviando feedback...",
    feedbackFailed: "Falha ao enviar feedback",
    feedbackSent: "Feedback enviado. Obrigado.",
    passwordsNoMatch: "As novas senhas não coincidem.",
    passwordTooShort: "A nova senha deve ter pelo menos 8 caracteres.",
    updatingPassword: "Atualizando senha...",
    passwordUpdateFailed: "Falha ao atualizar senha",
    passwordUpdated: "Senha atualizada. Use a nova senha no próximo login.",
    stepOf: "Etapa {current} de {total}",
    cppFoundationSubtitle: "Fundamentos de C++ · trilha prévia · {days} dias",
    targetSubtitle: "Base em {base} para {target} · {days} dias",
    syntaxArrow: "Sintaxe {base} → sintaxe {target}",
    languageSyntax: "Sintaxe de {language}",
    languageLineSyntax: "Sintaxe de {language} linha por linha",
    accountRequestFailed: "Falha na solicitação da conta",
    linePrefix: "L",
    dayLabel: "Dia {day}",
    tourAccountTitle: "Ferramentas da conta",
    tourAccountText: "Esta área salva seu progresso. Você pode abrir este tutorial novamente, alterar sua senha, sair, e administradores podem verificar usuários e feedback.",
    tourFoundationTitle: "Escolha sua base",
    tourFoundationText: "Depois de se registrar, escolha a linguagem que você já conhece. Escolha None se quiser começar pelos fundamentos de C++.",
    tourTargetTitle: "Escolha uma linguagem alvo",
    tourTargetText: "Use este menu para trocar a linguagem que o CodeBridge ensinará em seguida.",
    tourDayListTitle: "Abrir uma lição diária",
    tourDayListText: "Esta é a lista diária do curso. Role a barra lateral esquerda para chegar a todos os dias.",
    tourLessonTitle: "Estudar a lição",
    tourLessonText: "Leia a ponte a partir da linguagem conhecida, a explicação detalhada, as notas linha por linha e a documentação oficial.",
    tourHomeworkTitle: "Fazer HW Q1, Q2 e Q3",
    tourHomeworkText: "Cada dia tem três programas concretos. Siga os números, cálculos e requisitos de saída exatamente.",
    tourSubmitTitle: "Enviar tarefa",
    tourSubmitText: "Envie um arquivo ou cole o código. Depois de enviar, revise o feedback e compare com o código de exemplo.",
    tourFeedbackTitle: "Enviar feedback do site",
    tourFeedbackText: "Use este botão se algo estiver quebrado ou confuso. Sua mensagem vai para o proprietário do site.",
  },
  es: {
    htmlLang: "es",
    brandSubtitleDefault: "Base de C++ hacia varios lenguajes",
    totalProgress: "Progreso total",
    searchPlaceholder: "Buscar día, tema o categoría",
    interfaceLanguage: "Idioma de la interfaz",
    accountSaved: "Tu progreso se guarda en esta cuenta.",
    howToUse: "Cómo usar",
    changePassword: "Cambiar contraseña",
    adminDashboard: "Panel de administración",
    logOut: "Cerrar sesión",
    targetLanguage: "Lenguaje objetivo",
    changeLanguageExperience: "Cambiar experiencia de lenguaje",
    cppFoundations: "Fundamentos de C++",
    cppTrackNotice: "Termina o cambia cuando estés listo para otro lenguaje.",
    knowCppNow: "Ahora sé C++",
    dailyCourseList: "Lista diaria del curso",
    account: "Cuenta",
    saveLearningData: "Guardar tus datos de aprendizaje",
    saveLearningDataBody: "Regístrate o inicia sesión para que tus elecciones de lenguaje, día actual, progreso de listas y entregas queden vinculados a tu cuenta.",
    accountAction: "Acción de cuenta",
    register: "Registrarse",
    logIn: "Iniciar sesión",
    name: "Nombre",
    password: "Contraseña",
    createAccount: "Crear cuenta",
    languageExperienceCheck: "Revisión de experiencia",
    languageExperienceTitle: "¿Qué lenguaje de programación ya sabes usar?",
    languageExperienceBody: "Elige un lenguaje como base. El curso usará ese lenguaje para enseñar los demás. Elige None para empezar con fundamentos de C++.",
    knownProgrammingLanguages: "Lenguajes de programación conocidos",
    none: "None",
    continue: "Continuar",
    previousDay: "Día anterior",
    nextDay: "Día siguiente",
    day: "Día",
    checklist: "Lista",
    week: "Semana",
    knownLanguageBridge: "Puente desde el lenguaje conocido",
    syntaxBridge: "Puente de sintaxis",
    knownLanguageSyntax: "Sintaxis del lenguaje conocido",
    targetSyntax: "Sintaxis objetivo",
    sampleInput: "Entrada de ejemplo",
    expectedOutput: "Salida / resultado esperado",
    sameIdeaTranslated: "La misma idea traducida abajo",
    translationSteps: "Pasos de traducción",
    commonPitfalls: "Errores comunes",
    todaysTranslationDrill: "Ejercicio de traducción de hoy",
    officialDocumentation: "Documentación oficial",
    detailedExplanation: "Explicación detallada",
    sampleCodeAfterSubmission: "Código de ejemplo después de entregar",
    copyCode: "Copiar código",
    copied: "Copiado",
    sampleCodeNote: "Entrega tu tarea primero. Después de la revisión, usa este ejemplo para comparar estructura, sintaxis y estilo.",
    lineByLineSyntax: "Sintaxis línea por línea",
    lineByLineSyntaxNotes: "Notas de sintaxis línea por línea",
    todaysHomework: "Tarea de hoy",
    dayByDayGuidance: "Guía día por día",
    refresh: "Actualizar",
    today: "Hoy",
    learningHabits: "Hábitos de aprendizaje",
    focusAreas: "Áreas de enfoque",
    nextStudyBlock: "Siguiente bloque de estudio",
    dailyChecklist: "Lista diaria",
    reset: "Reiniciar",
    todaysAssignment: "Actividad de hoy",
    uploadHomework: "Subir tarea para revisión",
    optional: "Opcional",
    homeworkFile: "Archivo de tarea",
    orPasteCode: "O pegar código",
    standardInput: "Entrada estándar para el ejecutor Judge0",
    stdinPlaceholder: "Opcional. Pon un valor de entrada por línea cuando tu programa lea entrada.",
    aiFocus: "¿En qué debe enfocarse la IA?",
    aiFocusPlaceholder: "Ejemplo: no estoy seguro de si mi recursión es correcta.",
    submitAndReview: "Entregar y revisar",
    reviewHistory: "Historial de revisión",
    feedback: "Comentarios",
    siteFeedback: "Comentarios del sitio",
    tellUsFixing: "Dinos qué necesita arreglo",
    closeFeedbackForm: "Cerrar formulario de comentarios",
    feedbackType: "Tipo de comentario",
    bugOrBrokenPage: "Error o página rota",
    lessonOrHomeworkContent: "Contenido de lección o tarea",
    featureRequest: "Solicitud de función",
    other: "Otro",
    whatHappened: "¿Qué pasó?",
    feedbackPlaceholder: "Ejemplo: la tarea del Día 12 no está clara porque...",
    sendFeedback: "Enviar comentarios",
    accountSecurity: "Seguridad de la cuenta",
    changeYourPassword: "Cambiar tu contraseña",
    closePasswordForm: "Cerrar formulario de contraseña",
    currentPassword: "Contraseña actual",
    newPassword: "Nueva contraseña",
    confirmNewPassword: "Confirmar nueva contraseña",
    updatePassword: "Actualizar contraseña",
    skip: "Omitir",
    gotIt: "Entendido",
    finish: "Finalizar",
    loading: "Cargando",
    loginButton: "Iniciar sesión",
    creatingAccount: "Creando cuenta...",
    loggingIn: "Iniciando sesión...",
    chooseLanguageOrNone: "Elige un lenguaje o None antes de continuar.",
    aiReviewConnected: "Revisión de IA conectada",
    aiReviewConnectedBody: "Las entregas reciben revisión más profunda por párrafo y sugerencias línea por línea, incluso con código corto.",
    noConsoleOutput: "No hay salida de consola para este ejemplo.",
    homeworkSubmitted: "Tarea entregada.",
    finalLessonFinished: "Terminaste la última lección de esta ruta.",
    keepMoving: "Puedes seguir avanzando por el curso abierto.",
    allLessonsUnlocked: "Todas las lecciones están desbloqueadas.",
    allLessonsUnlockedBody: "Ahora puedes estudiar cualquier día. Entrega HW Q1, HW Q2 y HW Q3 cuando quieras comentarios e historial.",
    submitted: "Entregado",
    lessonLockedTitle: "Entrega la tarea del Día {day} antes de abrir esta lección.",
    lessonLockedMessage: "El Día {day} está bloqueado. Entrega la tarea del Día {previousDay} antes de continuar.",
    courseLoadFailed: "No se pudieron cargar los datos del curso",
    knownLanguage: "Lenguaje conocido",
    target: "Objetivo",
    code: "Código",
    blankLine: "Línea en blanco",
    syntax: "Sintaxis",
    comparison: "Comparación con {language}",
    phraseBreakdown: "Desglose de frases",
    noSubmissionsYet: "Todavía no hay entregas.",
    noSubmittedProgramSaved: "No se guardó texto del programa para este registro antiguo.",
    noJudge0Saved: "No se guardó resultado de Judge0 para esta entrega antigua.",
    judge0Unavailable: "Judge0 no estuvo disponible para esta entrega.",
    status: "Estado",
    unknown: "Desconocido",
    time: "Tiempo",
    memory: "Memoria",
    stdout: "Stdout",
    stderr: "Stderr",
    compileOutput: "Salida de compilación",
    message: "Mensaje",
    noBuiltInChecker: "No se guardó resultado del verificador interno para esta entrega antigua.",
    score: "Puntuación",
    nonEmptyLines: "Líneas no vacías",
    homeworkLabelsFound: "Etiquetas de tarea encontradas",
    checks: "Revisiones",
    pass: "APROBADO",
    fix: "CORREGIR",
    noneLower: "ninguno",
    viewSubmittedProgramAndReview: "Ver programa entregado y revisión",
    submittedProgram: "Programa entregado",
    judge0RunResult: "Resultado de ejecución Judge0",
    builtInCodeChecker: "Verificador de código integrado",
    whatToFixReview: "Qué corregir / comentarios de revisión",
    loadingGuidance: "Cargando guía...",
    noGuidance: "Aún no hay guía disponible.",
    guidanceFailed: "No se pudo cargar la guía",
    reviewing: "Revisando",
    runningCode: "Ejecutando código con Judge0 y generando comentarios...",
    submissionFailed: "Falló la entrega",
    sendingFeedback: "Enviando comentarios...",
    feedbackFailed: "No se pudieron enviar los comentarios",
    feedbackSent: "Comentarios enviados. Gracias.",
    passwordsNoMatch: "Las nuevas contraseñas no coinciden.",
    passwordTooShort: "La nueva contraseña debe tener al menos 8 caracteres.",
    updatingPassword: "Actualizando contraseña...",
    passwordUpdateFailed: "No se pudo actualizar la contraseña",
    passwordUpdated: "Contraseña actualizada. Usa la nueva contraseña la próxima vez que inicies sesión.",
    stepOf: "Paso {current} de {total}",
    cppFoundationSubtitle: "Fundamentos de C++ · ruta previa · {days} días",
    targetSubtitle: "Base de {base} a {target} · {days} días",
    syntaxArrow: "Sintaxis de {base} → sintaxis de {target}",
    languageSyntax: "Sintaxis de {language}",
    languageLineSyntax: "Sintaxis de {language} línea por línea",
    accountRequestFailed: "Falló la solicitud de cuenta",
    linePrefix: "L",
    dayLabel: "Día {day}",
    tourAccountTitle: "Herramientas de cuenta",
    tourAccountText: "Esta área guarda tu progreso. Puedes abrir este tutorial de nuevo, cambiar tu contraseña, cerrar sesión, y los administradores pueden revisar usuarios y comentarios.",
    tourFoundationTitle: "Elige tu base",
    tourFoundationText: "Después de registrarte, elige el lenguaje que ya sabes. Elige None si quieres empezar con fundamentos de C++.",
    tourTargetTitle: "Elige un lenguaje objetivo",
    tourTargetText: "Usa este menú para cambiar qué lenguaje te enseñará CodeBridge a continuación.",
    tourDayListTitle: "Abrir una lección diaria",
    tourDayListText: "Esta es la lista diaria del curso. Desplázate por la barra lateral izquierda para llegar a todos los días.",
    tourLessonTitle: "Estudiar la lección",
    tourLessonText: "Lee el puente desde tu lenguaje conocido, la explicación detallada, las notas línea por línea y la documentación oficial.",
    tourHomeworkTitle: "Hacer HW Q1, Q2 y Q3",
    tourHomeworkText: "Cada día tiene tres programas concretos. Sigue los números, cálculos y requisitos de salida exactos.",
    tourSubmitTitle: "Entregar tarea",
    tourSubmitText: "Sube un archivo o pega código. Después de entregar, revisa los comentarios y compara con el código de ejemplo.",
    tourFeedbackTitle: "Enviar comentarios del sitio",
    tourFeedbackText: "Usa este botón si algo está roto o confuso. Tu mensaje irá al propietario del sitio.",
  },
};

function t(key, replacements = {}) {
  const dictionary = translations[state.uiLanguage] || translations.en;
  const fallback = translations.en[key] || key;
  let value = dictionary[key] || fallback;
  for (const [name, replacement] of Object.entries(replacements)) {
    value = value.replaceAll(`{${name}}`, replacement);
  }
  return value;
}

function setText(selector, key, replacements = {}) {
  const element = document.querySelector(selector);
  if (element) element.textContent = t(key, replacements);
}

function setPlaceholder(selector, key) {
  const element = document.querySelector(selector);
  if (element) element.placeholder = t(key);
}

function setAriaLabel(selector, key) {
  const element = document.querySelector(selector);
  if (element) element.setAttribute("aria-label", t(key));
}

function applyStaticTranslations() {
  document.documentElement.lang = t("htmlLang");
  if (els.interfaceLanguageSelect) {
    for (const option of els.interfaceLanguageSelect.options) {
      option.textContent = UI_LANGUAGES[option.value] || option.textContent;
    }
    els.interfaceLanguageSelect.value = state.uiLanguage;
  }

  setText("#brandSubtitle", "brandSubtitleDefault");
  setText(".progress-row span", "totalProgress");
  setPlaceholder("#searchInput", "searchPlaceholder");
  setText(".interface-language-picker label", "interfaceLanguage");
  setText("#userPanel > span", "accountSaved");
  setText("#tutorialButton", "howToUse");
  setText("#changePasswordButton", "changePassword");
  setText(".admin-link", "adminDashboard");
  setText("#logoutButton", "logOut");
  setText(".language-picker label", "targetLanguage");
  setText("#resetPrerequisite", "changeLanguageExperience");
  setText("#cppTrackNotice strong", "cppFoundations");
  setText("#cppTrackNotice span", "cppTrackNotice");
  setText("#markCppKnown", "knowCppNow");
  setAriaLabel("#dayList", "dailyCourseList");

  setText("#authPanel .eyebrow", "account");
  setText("#authPanel h2", "saveLearningData");
  setText("#authPanel .onboarding-inner > p:not(.eyebrow):not(.access-message)", "saveLearningDataBody");
  setAriaLabel(".auth-tabs", "accountAction");
  setText("#showRegister", "register");
  setText("#showLogin", "logIn");
  setText('label span:has(+ #authName)', "name");
  setText('label span:has(+ #authPassword)', "password");

  setText("#onboardingPanel .eyebrow", "languageExperienceCheck");
  setText("#onboardingPanel h2", "languageExperienceTitle");
  setText("#onboardingPanel .onboarding-inner > p:not(.eyebrow):not(.access-message)", "languageExperienceBody");
  setAriaLabel(".language-experience-grid", "knownProgrammingLanguages");
  setText(".none-card span", "none");
  setText("#continueFromExperience", "continue");

  setAriaLabel("#prevDay", "previousDay");
  setAriaLabel("#nextDay", "nextDay");
  const metricLabels = document.querySelectorAll(".metric-strip span");
  if (metricLabels[0]) metricLabels[0].textContent = t("day");
  if (metricLabels[1]) metricLabels[1].textContent = t("checklist");
  if (metricLabels[2]) metricLabels[2].textContent = t("week");
  if (metricLabels[3]) metricLabels[3].textContent = t("mastery");

  const mainHeadings = document.querySelectorAll(".lesson-main > .panel .section-heading h3");
  const headingKeys = [
    "knownLanguageBridge",
    "syntaxBridge",
    "detailedExplanation",
    "sampleCodeAfterSubmission",
    "lineByLineSyntaxNotes",
    "todaysHomework",
  ];
  mainHeadings.forEach((heading, index) => {
    if (headingKeys[index]) heading.textContent = t(headingKeys[index]);
  });
  setText("#baseSyntaxLabel", "knownLanguageSyntax");
  setText("#targetSyntaxLabel", "targetSyntax");
  [els.baseExampleIo, els.targetExampleIo, els.sampleExampleIo].forEach((wrapper) => {
    if (!wrapper) return;
    const blocks = wrapper.querySelectorAll(".example-io-block");
    if (blocks[0]?.querySelector("span")) blocks[0].querySelector("span").textContent = t("sampleInput");
    if (blocks[1]?.querySelector("span")) blocks[1].querySelector("span").textContent = t("expectedOutput");
  });
  setText(".syntax-compare-divider span", "sameIdeaTranslated");
  const bridgeDetailHeadings = document.querySelectorAll(".bridge-detail-grid h4");
  if (bridgeDetailHeadings[0]) bridgeDetailHeadings[0].textContent = t("translationSteps");
  if (bridgeDetailHeadings[1]) bridgeDetailHeadings[1].textContent = t("commonPitfalls");
  setText(".drill-box strong", "todaysTranslationDrill");
  const bridgeHeadings = document.querySelectorAll(".bridge-panel h4");
  if (bridgeHeadings[2]) bridgeHeadings[2].textContent = t("officialDocumentation");
  setText("#copyCode", "copyCode");
  setText(".sample-code-note", "sampleCodeNote");
  setText("#lineNotesEyebrow", "lineByLineSyntax");

  const workHeadings = document.querySelectorAll(".work-panel .section-heading h3");
  const workHeadingKeys = [
    "dayByDayGuidance",
    "dailyChecklist",
    "todaysAssignment",
    "uploadHomework",
    "reviewHistory",
  ];
  workHeadings.forEach((heading, index) => {
    if (workHeadingKeys[index]) heading.textContent = t(workHeadingKeys[index]);
  });
  setText("#refreshGuidance", "refresh");
  setText("#resetChecklist", "reset");
  setText("#refreshSubmissions", "refresh");
  const guidanceHeadings = document.querySelectorAll(".guidance-section h4");
  const guidanceKeys = ["today", "learningHabits", "focusAreas", "nextStudyBlock"];
  guidanceHeadings.forEach((heading, index) => {
    if (guidanceKeys[index]) heading.textContent = t(guidanceKeys[index]);
  });
  setText('label span:has(+ #studentName)', "name");
  setPlaceholder("#studentName", "optional");
  setText('label span:has(+ #fileInput)', "homeworkFile");
  setText('label span:has(+ #codeInput)', "orPasteCode");
  setText('label span:has(+ #stdinInput)', "standardInput");
  setPlaceholder("#stdinInput", "stdinPlaceholder");
  setText('label span:has(+ #studentNote)', "aiFocus");
  setPlaceholder("#studentNote", "aiFocusPlaceholder");
  setText("#submitButton", "submitAndReview");

  setText("#feedbackButton", "feedback");
  setText("#feedbackModal .eyebrow", "siteFeedback");
  setText("#feedbackTitle", "tellUsFixing");
  setAriaLabel("#closeFeedback", "closeFeedbackForm");
  setText('label span:has(+ #feedbackCategory)', "feedbackType");
  const feedbackOptions = document.querySelectorAll("#feedbackCategory option");
  const feedbackOptionKeys = ["bugOrBrokenPage", "lessonOrHomeworkContent", "featureRequest", "other"];
  feedbackOptions.forEach((option, index) => {
    if (feedbackOptionKeys[index]) option.textContent = t(feedbackOptionKeys[index]);
  });
  setText('label span:has(+ #feedbackMessage)', "whatHappened");
  setPlaceholder("#feedbackMessage", "feedbackPlaceholder");
  setText("#sendFeedback", "sendFeedback");

  setText("#passwordModal .eyebrow", "accountSecurity");
  setText("#passwordTitle", "changeYourPassword");
  setAriaLabel("#closePasswordModal", "closePasswordForm");
  setText('label span:has(+ #currentPassword)', "currentPassword");
  setText('label span:has(+ #newPassword)', "newPassword");
  setText('label span:has(+ #confirmPassword)', "confirmNewPassword");
  setText("#savePasswordButton", "updatePassword");
  setText("#tourSkip", "skip");
  setText("#tourNext", "gotIt");

  setAuthMode(state.authMode);
}

function setUiLanguage(language) {
  state.uiLanguage = normalizeUiLanguage(language);
  localStorage.setItem("codeBridge.uiLanguage", state.uiLanguage);
  applyStaticTranslations();
  renderAiReviewStatus();
  renderOnboarding();
  if (state.lessons.length) renderLesson();
  if (hasExperienceProfile()) {
    loadCourse().catch((error) => {
      els.lessonTitle.textContent = error.message;
    });
  }
  if (els.submissionList && els.submissionList.children.length) {
    loadSubmissions();
  }
  if (els.guidancePanel && !els.guidancePanel.hidden) {
    loadGuidance();
  }
  if (els.tourLayer && !els.tourLayer.hidden) {
    renderTourStep();
  }
  if (els.feedbackBox && !els.feedbackBox.hidden && els.feedbackBox.dataset.statusKey) {
    els.feedbackBox.textContent = t(els.feedbackBox.dataset.statusKey);
  }
  if (state.user) {
    scheduleProfileSave();
  }
}

function accessHeaders() {
  const code = localStorage.getItem("racketTutor.accessCode");
  return code ? { "X-Access-Code": code } : {};
}

const els = {
  dayList: document.querySelector("#dayList"),
  authPanel: document.querySelector("#authPanel"),
  authForm: document.querySelector("#authForm"),
  authName: document.querySelector("#authName"),
  authPassword: document.querySelector("#authPassword"),
  authSubmit: document.querySelector("#authSubmit"),
  authMessage: document.querySelector("#authMessage"),
  showRegister: document.querySelector("#showRegister"),
  showLogin: document.querySelector("#showLogin"),
  userPanel: document.querySelector("#userPanel"),
  userNameLabel: document.querySelector("#userNameLabel"),
  interfaceLanguageSelect: document.querySelector("#interfaceLanguageSelect"),
  tutorialButton: document.querySelector("#tutorialButton"),
  changePasswordButton: document.querySelector("#changePasswordButton"),
  logoutButton: document.querySelector("#logoutButton"),
  onboardingPanel: document.querySelector("#onboardingPanel"),
  continueFromExperience: document.querySelector("#continueFromExperience"),
  languageExperienceInputs: document.querySelectorAll("[data-language-experience]"),
  noneExperience: document.querySelector("#noneExperience"),
  experienceMessage: document.querySelector("#experienceMessage"),
  brandSubtitle: document.querySelector("#brandSubtitle"),
  languagePicker: document.querySelector(".language-picker"),
  languageSelect: document.querySelector("#languageSelect"),
  resetPrerequisite: document.querySelector("#resetPrerequisite"),
  cppTrackNotice: document.querySelector("#cppTrackNotice"),
  markCppKnown: document.querySelector("#markCppKnown"),
  progressBlock: document.querySelector(".progress-block"),
  searchBox: document.querySelector(".search-box"),
  searchInput: document.querySelector("#searchInput"),
  progressText: document.querySelector("#progressText"),
  progressFill: document.querySelector("#progressFill"),
  weekLabel: document.querySelector("#weekLabel"),
  lessonTitle: document.querySelector("#lessonTitle"),
  prevDay: document.querySelector("#prevDay"),
  nextDay: document.querySelector("#nextDay"),
  categoryLabel: document.querySelector("#categoryLabel"),
  goalTitle: document.querySelector("#goalTitle"),
  goalText: document.querySelector("#goalText"),
  dayMetric: document.querySelector("#dayMetric"),
  checkMetric: document.querySelector("#checkMetric"),
  weekMetric: document.querySelector("#weekMetric"),
  masteryMetric: document.querySelector("#masteryMetric"),
  unlockNotice: document.querySelector("#unlockNotice"),
  cppBridge: document.querySelector("#cppBridge"),
  bridgeEyebrow: document.querySelector("#bridgeEyebrow"),
  bridgeConcept: document.querySelector("#bridgeConcept"),
  bridgeAngle: document.querySelector("#bridgeAngle"),
  baseSyntaxLabel: document.querySelector("#baseSyntaxLabel"),
  cppSyntaxBlock: document.querySelector("#cppSyntaxBlock"),
  baseExampleIo: document.querySelector("#baseExampleIo"),
  baseExampleInputBlock: document.querySelector("#baseExampleInputBlock"),
  baseExampleInput: document.querySelector("#baseExampleInput"),
  baseExampleOutput: document.querySelector("#baseExampleOutput"),
  targetSyntaxLabel: document.querySelector("#targetSyntaxLabel"),
  targetSyntaxBlock: document.querySelector("#targetSyntaxBlock"),
  targetExampleIo: document.querySelector("#targetExampleIo"),
  targetExampleInputBlock: document.querySelector("#targetExampleInputBlock"),
  targetExampleInput: document.querySelector("#targetExampleInput"),
  targetExampleOutput: document.querySelector("#targetExampleOutput"),
  translationSteps: document.querySelector("#translationSteps"),
  pitfallList: document.querySelector("#pitfallList"),
  bridgeDrill: document.querySelector("#bridgeDrill"),
  docsList: document.querySelector("#docsList"),
  explanation: document.querySelector("#explanation"),
  focusList: document.querySelector("#focusList"),
  codePanel: document.querySelector("#codePanel"),
  codeBlock: document.querySelector("#codeBlock"),
  sampleExampleIo: document.querySelector("#sampleExampleIo"),
  sampleExampleInputBlock: document.querySelector("#sampleExampleInputBlock"),
  sampleExampleInput: document.querySelector("#sampleExampleInput"),
  sampleExampleOutput: document.querySelector("#sampleExampleOutput"),
  lineNotesEyebrow: document.querySelector("#lineNotesEyebrow"),
  lineNotesPanel: document.querySelector("#lineNotesPanel"),
  lineNotesList: document.querySelector("#lineNotesList"),
  copyCode: document.querySelector("#copyCode"),
  practiceList: document.querySelector("#practiceList"),
  checklist: document.querySelector("#checklist"),
  resetChecklist: document.querySelector("#resetChecklist"),
  guidancePanel: document.querySelector("#guidancePanel"),
  guidanceSummary: document.querySelector("#guidanceSummary"),
  guidanceToday: document.querySelector("#guidanceToday"),
  guidanceHabits: document.querySelector("#guidanceHabits"),
  guidanceFocus: document.querySelector("#guidanceFocus"),
  guidanceNext: document.querySelector("#guidanceNext"),
  refreshGuidance: document.querySelector("#refreshGuidance"),
  assignmentText: document.querySelector("#assignmentText"),
  rubricList: document.querySelector("#rubricList"),
  aiReviewStatus: document.querySelector("#aiReviewStatus"),
  submissionForm: document.querySelector("#submissionForm"),
  submitButton: document.querySelector("#submitButton"),
  feedbackBox: document.querySelector("#feedbackBox"),
  refreshSubmissions: document.querySelector("#refreshSubmissions"),
  submissionList: document.querySelector("#submissionList"),
  feedbackButton: document.querySelector("#feedbackButton"),
  feedbackModal: document.querySelector("#feedbackModal"),
  closeFeedback: document.querySelector("#closeFeedback"),
  siteFeedbackForm: document.querySelector("#siteFeedbackForm"),
  feedbackCategory: document.querySelector("#feedbackCategory"),
  feedbackMessage: document.querySelector("#feedbackMessage"),
  sendFeedback: document.querySelector("#sendFeedback"),
  siteFeedbackStatus: document.querySelector("#siteFeedbackStatus"),
  passwordModal: document.querySelector("#passwordModal"),
  closePasswordModal: document.querySelector("#closePasswordModal"),
  passwordForm: document.querySelector("#passwordForm"),
  currentPassword: document.querySelector("#currentPassword"),
  newPassword: document.querySelector("#newPassword"),
  confirmPassword: document.querySelector("#confirmPassword"),
  savePasswordButton: document.querySelector("#savePasswordButton"),
  passwordStatus: document.querySelector("#passwordStatus"),
  tourLayer: document.querySelector("#tourLayer"),
  tourSpotlight: document.querySelector("#tourSpotlight"),
  tourTooltip: document.querySelector("#tourTooltip"),
  tourStepCount: document.querySelector("#tourStepCount"),
  tourTitle: document.querySelector("#tourTitle"),
  tourText: document.querySelector("#tourText"),
  tourSkip: document.querySelector("#tourSkip"),
  tourNext: document.querySelector("#tourNext"),
};

const tourSteps = [
  {
    selector: "#userPanel",
    titleKey: "tourAccountTitle",
    textKey: "tourAccountText",
    placement: "right",
  },
  {
    selector: "#onboardingPanel",
    titleKey: "tourFoundationTitle",
    textKey: "tourFoundationText",
    placement: "bottom",
  },
  {
    selector: ".language-picker",
    titleKey: "tourTargetTitle",
    textKey: "tourTargetText",
    placement: "right",
  },
  {
    selector: "#dayList",
    titleKey: "tourDayListTitle",
    textKey: "tourDayListText",
    placement: "right",
  },
  {
    selector: ".lesson-main",
    titleKey: "tourLessonTitle",
    textKey: "tourLessonText",
    placement: "left",
  },
  {
    selector: "#practiceList",
    titleKey: "tourHomeworkTitle",
    textKey: "tourHomeworkText",
    placement: "left",
  },
  {
    selector: ".submission-panel",
    titleKey: "tourSubmitTitle",
    textKey: "tourSubmitText",
    placement: "left",
  },
  {
    selector: "#feedbackButton",
    titleKey: "tourFeedbackTitle",
    textKey: "tourFeedbackText",
    placement: "top",
  },
];

let activeTourIndex = 0;

function readKnownLanguages() {
  const raw = localStorage.getItem("racketTutor.knownLanguages");
  if (raw) {
    try {
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  }
  const legacyStatus = localStorage.getItem("racketTutor.cppStatus");
  if (legacyStatus === "knows_cpp") return ["cpp"];
  if (legacyStatus === "needs_cpp") return [];
  return [];
}

function writeKnownLanguages(values) {
  const unique = [...new Set(values.filter((value) => value !== "none"))].slice(0, 1);
  state.knownLanguages = unique;
  state.baseLanguage = unique[0] || "";
  state.languageExperienceChosen = true;
  localStorage.setItem("racketTutor.knownLanguages", JSON.stringify(unique));
  localStorage.setItem("racketTutor.baseLanguage", state.baseLanguage);
  localStorage.setItem("racketTutor.languageExperienceChosen", "true");
  localStorage.setItem("racketTutor.cppStatus", state.baseLanguage ? "knows_cpp" : "needs_cpp");
}

function profilePayload() {
  return {
    knownLanguages: state.knownLanguages,
    baseLanguage: state.baseLanguage,
    languageExperienceChosen: state.languageExperienceChosen,
    targetLanguage: state.target,
    uiLanguage: state.uiLanguage,
    activeDay: state.activeDay,
    checklists: collectChecklistState(),
  };
}

function emptyProfilePayload() {
  return {
    knownLanguages: [],
    baseLanguage: "",
    languageExperienceChosen: false,
    targetLanguage: "racket",
    uiLanguage: state.uiLanguage,
    activeDay: 1,
    checklists: {},
  };
}

function collectChecklistState() {
  const checklists = {};
  for (let index = 0; index < localStorage.length; index += 1) {
    const key = localStorage.key(index);
    const prefix = "racketTutor.checklist.";
    if (!key || !key.startsWith(prefix)) continue;
    checklists[key.slice(prefix.length)] = JSON.parse(localStorage.getItem(key) || "[]");
  }
  return checklists;
}

let profileSaveTimer = null;

function scheduleProfileSave() {
  if (!state.user || !state.profileLoaded) return;
  clearTimeout(profileSaveTimer);
  profileSaveTimer = setTimeout(saveProfile, 350);
}

async function saveProfile() {
  if (!state.user) return;
  await fetch("/api/profile", {
    method: "POST",
    headers: { ...accessHeaders(), "Content-Type": "application/json" },
    body: JSON.stringify(profilePayload()),
  });
}

function applyProfile(profile) {
  if (!profile) return;
  const base = profile.baseLanguage || (profile.knownLanguages || [])[0] || "";
  if (profile.languageExperienceChosen) {
    writeKnownLanguages(base ? [base] : []);
  } else {
    state.knownLanguages = [];
    state.baseLanguage = "";
    state.languageExperienceChosen = false;
    localStorage.removeItem("racketTutor.knownLanguages");
    localStorage.removeItem("racketTutor.baseLanguage");
    localStorage.removeItem("racketTutor.languageExperienceChosen");
    localStorage.removeItem("racketTutor.cppStatus");
  }
  state.target = profile.targetLanguage || state.target;
  state.uiLanguage = normalizeUiLanguage(profile.uiLanguage || state.uiLanguage);
  localStorage.setItem("codeBridge.uiLanguage", state.uiLanguage);
  if (state.baseLanguage && state.target === state.baseLanguage) {
    state.target = chooseDefaultTarget();
  }
  state.activeDay = Number(profile.activeDay || 1);
  localStorage.setItem("racketTutor.targetLanguage", state.target);
  localStorage.setItem("racketTutor.activeDay", String(state.activeDay));
  for (const [key, value] of Object.entries(profile.checklists || {})) {
    localStorage.setItem(`racketTutor.checklist.${key}`, JSON.stringify(value));
  }
  state.profileLoaded = true;
}

function padDay(day) {
  return String(day).padStart(2, "0");
}

function checklistKey(day) {
  return `racketTutor.checklist.${state.target}.${day}`;
}

function submissionKey(target, day) {
  return `${target}:${day}`;
}

function hasSubmitted(day, target = state.target) {
  return state.submittedLessons.has(submissionKey(target, day));
}

function assignmentScoreLabel(item) {
  if (item.assignmentScoreLabel) return item.assignmentScoreLabel;
  const score = item.assignmentScore ?? item.score ?? item.codeCheck?.score;
  if (score === undefined || score === null || score === "") return t("unknown");
  const numeric = Number(score);
  return Number.isFinite(numeric) ? `${numeric.toFixed(1).replace(/\.0$/, "")}/10` : `${score}/10`;
}

function masteryRatingLabel(item) {
  const rating = item.masteryRating ?? item.codeCheck?.masteryRating;
  const label = item.masteryLabel || item.codeCheck?.masteryLabel;
  if (rating === undefined || rating === null || rating === "") return t("unknown");
  return label ? `${rating}/5 · ${label}` : `${rating}/5`;
}

function isLessonUnlocked(day) {
  return day >= 1;
}

function readChecklist(day) {
  const raw = localStorage.getItem(checklistKey(day));
  if (!raw) return [];
  try {
    return JSON.parse(raw);
  } catch {
    return [];
  }
}

function writeChecklist(day, values) {
  localStorage.setItem(checklistKey(day), JSON.stringify(values));
  scheduleProfileSave();
}

function checkedCount(day) {
  return readChecklist(day).filter(Boolean).length;
}

function activeLesson() {
  return state.lessons.find((lesson) => lesson.day === state.activeDay) || state.lessons[0];
}

function isCppFoundationMode() {
  return !state.baseLanguage;
}

function hasExperienceProfile() {
  return state.languageExperienceChosen
    || localStorage.getItem("racketTutor.languageExperienceChosen") === "true"
    || localStorage.getItem("racketTutor.baseLanguage") !== null
    || localStorage.getItem("racketTutor.knownLanguages") !== null
    || localStorage.getItem("racketTutor.cppStatus") !== null;
}

function isAuthenticated() {
  return Boolean(state.user);
}

function setMainContentHidden(hidden) {
  document.querySelector(".topbar").hidden = hidden;
  document.querySelector(".lesson-layout").hidden = hidden;
}

function renderOnboarding() {
  const needsAuth = !isAuthenticated();
  const needsChoice = !hasExperienceProfile();
  if (els.authPanel) {
    els.authPanel.hidden = !needsAuth;
  }
  for (const input of els.languageExperienceInputs || []) {
    input.checked = state.baseLanguage === input.value;
  }
  if (els.noneExperience) {
    els.noneExperience.checked = !state.baseLanguage && hasExperienceProfile();
  }
  if (els.onboardingPanel) {
    els.onboardingPanel.hidden = needsAuth || !needsChoice;
  }
  setMainContentHidden(needsAuth || needsChoice);
  for (const item of [els.progressBlock, els.searchBox, els.dayList]) {
    if (item) item.hidden = needsAuth || needsChoice;
  }
  if (els.userPanel) {
    els.userPanel.hidden = needsAuth;
  }
  if (els.languagePicker) {
    els.languagePicker.hidden = needsAuth || needsChoice || isCppFoundationMode();
  }
  if (els.cppTrackNotice) {
    els.cppTrackNotice.hidden = needsAuth || needsChoice || !isCppFoundationMode();
  }
  if (els.userNameLabel && state.user) {
    els.userNameLabel.textContent = state.user.name;
  }
}

function setCppStatus(status) {
  writeKnownLanguages(status === "knows_cpp" ? ["cpp"] : []);
  state.activeDay = 1;
  localStorage.setItem("racketTutor.activeDay", "1");

  if (!state.baseLanguage) {
    state.target = "cpp";
  } else if (state.target === "cpp") {
    state.target = "racket";
  }
  localStorage.setItem("racketTutor.targetLanguage", state.target);
  renderOnboarding();
  scheduleProfileSave();
  loadCourse().catch((error) => {
    els.lessonTitle.textContent = error.message;
  });
}

function resetPrerequisiteChoice() {
  state.knownLanguages = [];
  state.baseLanguage = "";
  state.languageExperienceChosen = false;
  localStorage.removeItem("racketTutor.knownLanguages");
  localStorage.removeItem("racketTutor.baseLanguage");
  localStorage.removeItem("racketTutor.languageExperienceChosen");
  localStorage.removeItem("racketTutor.cppStatus");
  renderOnboarding();
  scheduleProfileSave();
}

function chooseDefaultTarget() {
  const candidates = ["cpp", "python", "java", "c", "racket", "r"];
  return candidates.find((id) => id !== state.baseLanguage) || "cpp";
}

function continueFromLanguageExperience() {
  const checkedLanguage = [...els.languageExperienceInputs].find((input) => input.checked);
  if (!els.noneExperience?.checked && !checkedLanguage) {
    if (els.experienceMessage) els.experienceMessage.textContent = t("chooseLanguageOrNone");
    return;
  }
  if (els.experienceMessage) els.experienceMessage.textContent = "";
  const selected = els.noneExperience?.checked ? "" : (checkedLanguage?.value || "");
  writeKnownLanguages(selected ? [selected] : []);
  state.activeDay = 1;
  localStorage.setItem("racketTutor.activeDay", "1");
  state.target = state.baseLanguage ? (state.target === state.baseLanguage ? chooseDefaultTarget() : state.target) : "cpp";
  localStorage.setItem("racketTutor.targetLanguage", state.target);
  renderOnboarding();
  scheduleProfileSave();
  loadCourse()
    .then(() => {
      if (localStorage.getItem("codeBridge.pendingCourseTour") === "true") {
        localStorage.removeItem("codeBridge.pendingCourseTour");
        setTimeout(openTutorialModal, 250);
      }
    })
    .catch((error) => {
      els.lessonTitle.textContent = error.message;
    });
}

function setAuthMode(mode) {
  state.authMode = mode;
  const register = mode === "register";
  els.showRegister.classList.toggle("active", register);
  els.showLogin.classList.toggle("active", !register);
  els.authSubmit.textContent = register ? t("createAccount") : t("loginButton");
  els.authPassword.autocomplete = register ? "new-password" : "current-password";
  els.authMessage.textContent = "";
}

function renderAiReviewStatus(enabled = state.aiReviewEnabled) {
  if (!els.aiReviewStatus) return;
  if (!enabled) {
    els.aiReviewStatus.hidden = true;
    els.aiReviewStatus.innerHTML = "";
    return;
  }
  els.aiReviewStatus.hidden = false;
  els.aiReviewStatus.classList.toggle("enabled", enabled);
  els.aiReviewStatus.innerHTML = `<strong>${t("aiReviewConnected")}</strong><span>${t("aiReviewConnectedBody")}</span>`;
}

async function loadSession() {
  const response = await fetch("/api/me", { headers: accessHeaders() });
  if (!response.ok) {
    renderAiReviewStatus(false);
    renderOnboarding();
    return;
  }
  const data = await response.json();
  state.aiReviewEnabled = Boolean(data.openaiFeedbackEnabled);
  renderAiReviewStatus();
  state.user = data.user;
  if (state.user) {
    applyProfile(data.profile);
    applyStaticTranslations();
  }
  renderOnboarding();
  if (state.user && hasExperienceProfile()) {
    await loadCourse();
  }
  await loadSubmissions();
  await loadGuidance();
}

async function submitAuth(event) {
  event.preventDefault();
  const wasRegistering = state.authMode === "register";
  els.authSubmit.disabled = true;
  els.authMessage.textContent = state.authMode === "register" ? t("creatingAccount") : t("loggingIn");
  try {
    const response = await fetch(`/api/${state.authMode}`, {
      method: "POST",
      headers: { ...accessHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify({
        name: els.authName.value,
        password: els.authPassword.value,
        profile: state.authMode === "register" ? emptyProfilePayload() : profilePayload(),
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || t("accountRequestFailed"));
    state.user = data.user;
    applyProfile(data.profile);
    applyStaticTranslations();
    els.authForm.reset();
    els.authMessage.textContent = "";
    renderOnboarding();
    if (hasExperienceProfile()) {
      await loadCourse();
    }
    await loadSubmissions();
    await loadGuidance();
    if (wasRegistering) {
      localStorage.removeItem("codeBridge.tutorialSeen");
      localStorage.setItem("codeBridge.pendingCourseTour", "true");
      openTutorialModal();
    }
  } catch (error) {
    els.authMessage.textContent = error.message;
  } finally {
    els.authSubmit.disabled = false;
  }
}

async function logout() {
  await fetch("/api/logout", { method: "POST", headers: accessHeaders() });
  state.user = null;
  state.profileLoaded = false;
  state.lessons = [];
  state.submittedLessons = new Set();
  state.unlockedSampleCode = null;
  state.knownLanguages = [];
  state.baseLanguage = "";
  state.languageExperienceChosen = false;
  state.target = "racket";
  state.activeDay = 1;
  localStorage.removeItem("racketTutor.knownLanguages");
  localStorage.removeItem("racketTutor.baseLanguage");
  localStorage.removeItem("racketTutor.languageExperienceChosen");
  localStorage.removeItem("racketTutor.cppStatus");
  localStorage.removeItem("racketTutor.targetLanguage");
  localStorage.removeItem("racketTutor.activeDay");
  for (const key of Object.keys(localStorage)) {
    if (key.startsWith("racketTutor.checklist.")) {
      localStorage.removeItem(key);
    }
  }
  if (els.submissionList) els.submissionList.innerHTML = "";
  if (els.guidancePanel) els.guidancePanel.hidden = true;
  if (els.feedbackBox) {
    els.feedbackBox.hidden = true;
    els.feedbackBox.textContent = "";
    els.feedbackBox.classList.remove("error");
  }
  if (els.authPanel) els.authPanel.hidden = false;
  setAuthMode("login");
  renderOnboarding();
}

function renderDayList() {
  const query = state.query.trim().toLowerCase();
  const lessons = state.lessons.filter((lesson) => {
    if (!query) return true;
    return [
      lesson.day,
      lesson.category,
      lesson.title,
      lesson.goal,
      lesson.syntax_bridge?.concept || "",
      lesson.syntax_bridge?.today_angle || "",
      lesson.syntax_bridge?.docs?.map((doc) => doc.title).join(" ") || "",
      lesson.racket_focus.join(" "),
      lesson.target_language_name || "",
    ]
      .join(" ")
      .toLowerCase()
      .includes(query);
  });

  els.dayList.innerHTML = "";
  for (const lesson of lessons) {
    const done = checkedCount(lesson.day) === lesson.checklist.length;
    const submitted = hasSubmitted(lesson.day);
    const unlocked = isLessonUnlocked(lesson.day);
    const button = document.createElement("button");
    button.type = "button";
    button.disabled = !unlocked;
    button.title = unlocked ? "" : t("lessonLockedTitle", { day: padDay(lesson.day - 1) });
    button.className = `day-card${lesson.day === state.activeDay ? " active" : ""}${!unlocked ? " locked" : ""}`;
    button.innerHTML = `
      <span class="day-number">${padDay(lesson.day)}</span>
      <span>
        <strong>${lesson.title}</strong>
        <span>${lesson.category}${submitted ? ` · ${t("submitted")}` : ""}</span>
      </span>
      <span class="done-dot${done || submitted ? " complete" : ""}" aria-hidden="true"></span>
    `;
    button.addEventListener("click", () => selectDay(lesson.day));
    els.dayList.appendChild(button);
  }
}

function renderProgress() {
  const total = state.lessons.reduce((sum, lesson) => sum + lesson.checklist.length, 0);
  const done = state.lessons.reduce((sum, lesson) => sum + checkedCount(lesson.day), 0);
  els.progressText.textContent = `${done} / ${total}`;
  els.progressFill.style.width = total ? `${Math.round((done / total) * 100)}%` : "0%";
}

function renderLesson() {
  const lesson = activeLesson();
  if (!lesson) return;

  const checks = readChecklist(lesson.day);
  const done = checks.filter(Boolean).length;

  localStorage.setItem("racketTutor.activeDay", String(lesson.day));
  els.weekLabel.textContent = `${t("week")} ${lesson.week}`;
  document.title = "CodeBridge";
  document.querySelector(".brand h1").textContent = "CodeBridge";
  if (els.brandSubtitle) {
    const dayCount = state.lessons.length || 56;
    els.brandSubtitle.textContent = isCppFoundationMode()
      ? t("cppFoundationSubtitle", { days: dayCount })
      : t("targetSubtitle", {
        base: lesson.base_language_name || t("knownLanguage"),
        target: lesson.target_language_name || t("target"),
        days: dayCount,
      });
  }
  els.lessonTitle.textContent = lesson.title;
  els.categoryLabel.textContent = lesson.category;
  els.goalTitle.textContent = lesson.title;
  els.goalText.textContent = lesson.goal;
  els.dayMetric.textContent = padDay(lesson.day);
  els.checkMetric.textContent = `${done}/${lesson.checklist.length}`;
  els.weekMetric.textContent = lesson.week;
  if (els.unlockNotice) {
    const submittedToday = hasSubmitted(lesson.day);
    const finalDay = lesson.day === state.lessons.length;
    els.unlockNotice.classList.toggle("complete", submittedToday);
    els.unlockNotice.innerHTML = submittedToday
      ? `<strong>${t("homeworkSubmitted")}</strong><span>${finalDay ? t("finalLessonFinished") : t("keepMoving")}</span>`
      : `<strong>${t("allLessonsUnlocked")}</strong><span>${t("allLessonsUnlockedBody")}</span>`;
  }
  els.cppBridge.textContent = lesson.cpp_bridge;
  renderSyntaxBridge(lesson);
  els.explanation.textContent = lesson.explanation;
  els.codePanel.hidden = state.unlockedSampleCode?.day !== lesson.day || state.unlockedSampleCode?.target !== state.target;
  els.codeBlock.textContent = els.codePanel.hidden ? "" : state.unlockedSampleCode.code;
  renderExampleIo(
    els.sampleExampleIo,
    els.sampleExampleInputBlock,
    els.sampleExampleInput,
    els.sampleExampleOutput,
    els.codePanel.hidden ? null : lesson.syntax_bridge?.target_io,
  );
  renderLineNotes(lesson);
  els.assignmentText.textContent = lesson.assignment;

  els.prevDay.disabled = lesson.day === 1;
  els.nextDay.disabled = lesson.day === state.lessons.length;
  els.nextDay.title = "";

  els.focusList.innerHTML = "";
  for (const focus of lesson.racket_focus) {
    const tag = document.createElement("span");
    tag.className = "tag";
    tag.textContent = focus;
    els.focusList.appendChild(tag);
  }

  els.practiceList.innerHTML = "";
  for (const item of lesson.practice) {
    const li = document.createElement("li");
    li.textContent = item;
    els.practiceList.appendChild(li);
  }

  els.rubricList.innerHTML = "";
  for (const item of lesson.grading_rubric) {
    const li = document.createElement("li");
    li.textContent = item;
    els.rubricList.appendChild(li);
  }

  renderChecklist(lesson);
  renderDayList();
  renderProgress();
}

function renderExampleIo(wrapper, inputBlock, inputElement, outputElement, io) {
  if (!wrapper || !outputElement) return;
  const output = String(io?.output || "").trim();
  const input = String(io?.input || "").trim();
  wrapper.hidden = !output && !input;
  if (wrapper.hidden) {
    if (inputElement) inputElement.textContent = "";
    outputElement.textContent = "";
    return;
  }
  if (inputBlock && inputElement) {
    inputBlock.hidden = !input;
    inputElement.textContent = input;
  }
  outputElement.textContent = output || t("noConsoleOutput");
}

function renderSyntaxBridge(lesson) {
  const bridge = lesson.syntax_bridge;
  if (!bridge) return;
  const targetName = lesson.target_language_name || bridge.target_label || t("target");
  const baseName = lesson.base_language_name || bridge.base_label || t("knownLanguage");

  els.bridgeEyebrow.textContent = t("syntaxArrow", { base: baseName, target: targetName });
  els.bridgeConcept.textContent = bridge.concept;
  els.bridgeAngle.textContent = bridge.today_angle;
  els.baseSyntaxLabel.textContent = t("languageSyntax", { language: baseName });
  els.cppSyntaxBlock.textContent = bridge.cpp;
  renderExampleIo(els.baseExampleIo, els.baseExampleInputBlock, els.baseExampleInput, els.baseExampleOutput, bridge.base_io);
  els.targetSyntaxLabel.textContent = t("languageSyntax", { language: targetName });
  els.targetSyntaxBlock.textContent = bridge.target || bridge.racket;
  renderExampleIo(els.targetExampleIo, els.targetExampleInputBlock, els.targetExampleInput, els.targetExampleOutput, bridge.target_io);
  els.bridgeDrill.textContent = bridge.drill;

  els.translationSteps.innerHTML = "";
  for (const step of bridge.translation_steps) {
    const li = document.createElement("li");
    li.textContent = step;
    els.translationSteps.appendChild(li);
  }

  els.pitfallList.innerHTML = "";
  for (const pitfall of bridge.pitfalls) {
    const li = document.createElement("li");
    li.textContent = pitfall;
    els.pitfallList.appendChild(li);
  }

  els.docsList.innerHTML = "";
  for (const doc of bridge.docs || lesson.official_docs || []) {
    const link = document.createElement("a");
    link.href = doc.url;
    link.target = "_blank";
    link.rel = "noreferrer";
    link.textContent = doc.title;
    els.docsList.appendChild(link);
  }
}

function renderLineNotes(lesson) {
  const notes = lesson.line_notes || [];
  const show = notes.length > 0;
  els.lineNotesPanel.hidden = !show;
  els.lineNotesList.innerHTML = "";
  if (!show) return;
  els.lineNotesEyebrow.textContent = t("languageLineSyntax", { language: lesson.target_language_name || t("code") });

  notes.forEach((note, index) => {
    const row = document.createElement("article");
    row.className = "line-note";
    const codeText = note.line || t("blankLine");
    row.innerHTML = `
      <div class="line-note-index">${t("linePrefix")}${index + 1}</div>
      <div class="line-note-body">
        <pre><code></code></pre>
        <p></p>
        <dl>
          <div><dt>${t("syntax")}</dt><dd></dd></div>
          <div><dt>${t("comparison", { language: lesson.base_language_name || t("knownLanguage") })}</dt><dd></dd></div>
        </dl>
        <div class="phrase-breakdown" hidden>
          <h4>${t("phraseBreakdown")}</h4>
          <ul></ul>
        </div>
      </div>
    `;
    row.querySelector("code").textContent = codeText;
    row.querySelector("p").textContent = note.plain;
    const descriptions = row.querySelectorAll("dd");
    descriptions[0].textContent = note.syntax;
    descriptions[1].textContent = note.cpp;
    const phraseBox = row.querySelector(".phrase-breakdown");
    const phraseList = phraseBox.querySelector("ul");
    if (Array.isArray(note.phrases) && note.phrases.length) {
      phraseBox.hidden = false;
      for (const item of note.phrases) {
        const li = document.createElement("li");
        const phrase = document.createElement("code");
        phrase.textContent = item.phrase;
        const meaning = document.createElement("span");
        meaning.textContent = item.meaning;
        li.append(phrase, meaning);
        phraseList.appendChild(li);
      }
    }
    els.lineNotesList.appendChild(row);
  });
}

function renderChecklist(lesson) {
  const values = readChecklist(lesson.day);
  els.checklist.innerHTML = "";

  lesson.checklist.forEach((item, index) => {
    const id = `day-${lesson.day}-check-${index}`;
    const label = document.createElement("label");
    label.className = `check-item${values[index] ? " done" : ""}`;
    label.htmlFor = id;

    const input = document.createElement("input");
    input.id = id;
    input.type = "checkbox";
    input.checked = Boolean(values[index]);
    input.addEventListener("change", () => {
      const next = readChecklist(lesson.day);
      next[index] = input.checked;
      writeChecklist(lesson.day, next);
      renderLesson();
      loadGuidance();
    });

    const span = document.createElement("span");
    span.textContent = item;

    label.append(input, span);
    els.checklist.appendChild(label);
  });
}

function selectDay(day) {
  const nextDay = Math.max(1, Math.min(day, state.lessons.length));
  if (!isLessonUnlocked(nextDay)) {
    els.feedbackBox.hidden = false;
    els.feedbackBox.classList.add("error");
    els.feedbackBox.textContent = t("lessonLockedMessage", { day: padDay(nextDay), previousDay: padDay(nextDay - 1) });
    renderDayList();
    return;
  }
  state.activeDay = nextDay;
  state.unlockedSampleCode = null;
  localStorage.setItem("racketTutor.activeDay", String(state.activeDay));
  scheduleProfileSave();
  renderLesson();
  loadGuidance();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

async function loadCourse() {
  if (!hasExperienceProfile()) {
    renderOnboarding();
    return;
  }
  if (isCppFoundationMode()) {
    state.target = "cpp";
    localStorage.setItem("racketTutor.targetLanguage", state.target);
  } else if (state.target === state.baseLanguage) {
    state.target = chooseDefaultTarget();
    localStorage.setItem("racketTutor.targetLanguage", state.target);
  }
  const params = new URLSearchParams({
    target: state.target,
    base: state.baseLanguage || "cpp",
    uiLanguage: state.uiLanguage,
  });
  const response = await fetch(`/api/course?${params.toString()}`, { headers: accessHeaders() });
  if (response.status === 401) {
    window.location.href = "/";
    return;
  }
  if (!response.ok) throw new Error(t("courseLoadFailed"));
  const data = await response.json();
  state.languages = data.languages || state.languages;
  state.target = data.target || state.target;
  state.lessons = data.lessons;
  renderOnboarding();
  renderLanguageOptions();
  if (!state.lessons.some((lesson) => lesson.day === state.activeDay)) {
    state.activeDay = 1;
  }
  while (state.activeDay > 1 && !isLessonUnlocked(state.activeDay)) {
    state.activeDay -= 1;
  }
  renderLesson();
  loadGuidance();
}

function renderLanguageOptions() {
  if (!els.languageSelect || !state.languages.length) return;
  els.languageSelect.innerHTML = "";
  for (const language of state.languages) {
    if (language.id === state.baseLanguage) continue;
    const option = document.createElement("option");
    option.value = language.id;
    option.textContent = language.name;
    option.selected = language.id === state.target;
    els.languageSelect.appendChild(option);
  }
}

async function loadSubmissions() {
  const response = await fetch("/api/submissions", { headers: accessHeaders() });
  if (!response.ok) return;
  const data = await response.json();
  state.submittedLessons = new Set(
    data.submissions.map((item) => submissionKey(item.target || "racket", item.day)),
  );
  els.submissionList.innerHTML = "";
  if (state.lessons.length) {
    renderDayList();
    renderProgress();
  }

  if (!data.submissions.length) {
    const empty = document.createElement("p");
    empty.className = "body-text";
    empty.textContent = t("noSubmissionsYet");
    els.submissionList.appendChild(empty);
    return;
  }

  data.submissions.slice(0, 12).forEach((item) => {
    const created = new Date(item.createdAt).toLocaleString();
    const div = document.createElement("div");
    div.className = "submission-item";
    div.innerHTML = `
      <strong>${item.targetLanguage || "Racket"} · ${t("dayLabel", { day: padDay(item.day) })} · ${item.title}</strong>
      <span>${item.studentName} · ${created}${item.filename ? ` · ${item.filename}` : ""}</span>
      <div class="submission-score-row" aria-label="${t("assignmentScore")}">
        <span><b>${t("assignmentScore")}</b>${assignmentScoreLabel(item)}</span>
        <span><b>${t("masteryRating")}</b>${masteryRatingLabel(item)}</span>
      </div>
      <details>
        <summary>${t("viewSubmittedProgramAndReview")}</summary>
        <div class="submission-detail">
          <h4>${t("submittedProgram")}</h4>
          <pre data-submission-content></pre>
          <h4>${t("judge0RunResult")}</h4>
          <pre data-submission-execution></pre>
          <h4>${t("builtInCodeChecker")}</h4>
          <pre data-submission-code-check></pre>
          <h4>${t("whatToFixReview")}</h4>
          <pre data-submission-feedback></pre>
        </div>
      </details>
    `;
    div.querySelector("[data-submission-content]").textContent =
      item.content || item.contentPreview || t("noSubmittedProgramSaved");
    div.querySelector("[data-submission-execution]").textContent = formatExecutionHistory(item.execution);
    div.querySelector("[data-submission-code-check]").textContent = formatCodeCheckHistory(item.codeCheck);
    div.querySelector("[data-submission-feedback]").textContent = item.feedback;
    els.submissionList.appendChild(div);
  });
}

function formatExecutionHistory(execution) {
  if (!execution) return t("noJudge0Saved");
  if (!execution.available) return execution.message || t("judge0Unavailable");
  const parts = [`${t("status")}: ${execution.status || t("unknown")}`];
  if (execution.time) parts.push(`${t("time")}: ${execution.time}s`);
  if (execution.memory) parts.push(`${t("memory")}: ${execution.memory} KB`);
  if (execution.stdout) parts.push(`${t("stdout")}:\n${execution.stdout}`);
  if (execution.stderr) parts.push(`${t("stderr")}:\n${execution.stderr}`);
  if (execution.compileOutput) parts.push(`${t("compileOutput")}:\n${execution.compileOutput}`);
  if (execution.message) parts.push(`${t("message")}:\n${execution.message}`);
  return parts.join("\n");
}

function formatCodeCheckHistory(codeCheck) {
  if (!codeCheck) return t("noBuiltInChecker");
  const lines = [
    `${t("score")}: ${codeCheck.score ?? 0}/10`,
    `${t("masteryRating")}: ${codeCheck.masteryRating ?? 1}/5 (${codeCheck.masteryLabel || t("unrated")})`,
    `${t("nonEmptyLines")}: ${codeCheck.nonEmptyLines ?? 0}`,
    `${t("homeworkLabelsFound")}: ${(codeCheck.programLabelsFound || []).join(", ") || t("noneLower")}`,
    "",
    `${t("checks")}:`,
  ];
  for (const check of codeCheck.checks || []) {
    lines.push(`${check.passed ? t("pass") : t("fix")} - ${check.name}${check.passed ? "" : ` | ${check.fix}`}`);
  }
  return lines.join("\n");
}

function renderGuidanceList(element, items) {
  if (!element) return;
  element.innerHTML = "";
  for (const item of items || []) {
    const li = document.createElement("li");
    li.textContent = item;
    element.appendChild(li);
  }
}

async function loadGuidance() {
  if (!els.guidancePanel) return;
  if (!state.user || !state.lessons.length) {
    els.guidancePanel.hidden = true;
    return;
  }
  els.guidancePanel.hidden = false;
  els.guidanceSummary.textContent = t("loadingGuidance");
  try {
    const params = new URLSearchParams({
      day: String(state.activeDay),
      target: state.target,
      base: state.baseLanguage || "cpp",
    });
    const response = await fetch(`/api/guidance?${params.toString()}`, { headers: accessHeaders() });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || t("guidanceFailed"));
    const guidance = data.guidance || {};
    els.guidanceSummary.textContent = guidance.summary || t("noGuidance");
    renderGuidanceList(els.guidanceToday, guidance.today);
    renderGuidanceList(els.guidanceHabits, guidance.habits);
    renderGuidanceList(els.guidanceFocus, guidance.focusAreas);
    renderGuidanceList(els.guidanceNext, guidance.nextSteps);
  } catch (error) {
    els.guidanceSummary.textContent = error.message;
    renderGuidanceList(els.guidanceToday, []);
    renderGuidanceList(els.guidanceHabits, []);
    renderGuidanceList(els.guidanceFocus, []);
    renderGuidanceList(els.guidanceNext, []);
  }
}

async function submitAssignment(event) {
  event.preventDefault();
  const lesson = activeLesson();
  const formData = new FormData(els.submissionForm);
  formData.set("day", lesson.day);
  formData.set("target", state.target);
  formData.set("base", state.baseLanguage || "cpp");

  els.submitButton.disabled = true;
  els.submitButton.textContent = t("reviewing");
  els.feedbackBox.hidden = false;
  els.feedbackBox.classList.remove("error");
  els.feedbackBox.dataset.statusKey = "runningCode";
  els.feedbackBox.textContent = t("runningCode");

  try {
    const response = await fetch("/api/submit", {
      method: "POST",
      headers: accessHeaders(),
      body: formData,
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || t("submissionFailed"));
    }
    const scoreLine = `${t("assignmentScore")}: ${assignmentScoreLabel(data.submission)}\n${t("masteryRating")}: ${masteryRatingLabel(data.submission)}`;
    delete els.feedbackBox.dataset.statusKey;
    els.feedbackBox.textContent = `${scoreLine}\n\n${data.submission.feedback}`;
    if (data.sampleCode) {
      state.unlockedSampleCode = {
        day: data.submission.day,
        target: data.submission.target,
        code: data.sampleCode,
      };
      state.submittedLessons.add(submissionKey(data.submission.target, data.submission.day));
      renderLesson();
    }
    els.submissionForm.reset();
    await loadSubmissions();
    await loadGuidance();
  } catch (error) {
    els.feedbackBox.classList.add("error");
    delete els.feedbackBox.dataset.statusKey;
    els.feedbackBox.textContent = error.message;
  } finally {
    els.submitButton.disabled = false;
    els.submitButton.textContent = t("submitAndReview");
  }
}

function openFeedbackModal() {
  if (!els.feedbackModal) return;
  els.feedbackModal.hidden = false;
  if (els.siteFeedbackStatus) els.siteFeedbackStatus.textContent = "";
  requestAnimationFrame(() => els.feedbackMessage?.focus());
}

function closeFeedbackModal() {
  if (!els.feedbackModal) return;
  els.feedbackModal.hidden = true;
}

async function submitSiteFeedback(event) {
  event.preventDefault();
  const lesson = activeLesson();
  els.sendFeedback.disabled = true;
  els.siteFeedbackStatus.textContent = t("sendingFeedback");
  try {
    const response = await fetch("/api/feedback", {
      method: "POST",
      headers: { ...accessHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify({
        category: els.feedbackCategory.value,
        message: els.feedbackMessage.value,
        page: window.location.href,
        day: lesson?.day || null,
        target: state.target,
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || t("feedbackFailed"));
    els.siteFeedbackForm.reset();
    els.siteFeedbackStatus.textContent = t("feedbackSent");
    setTimeout(closeFeedbackModal, 900);
  } catch (error) {
    els.siteFeedbackStatus.textContent = error.message;
  } finally {
    els.sendFeedback.disabled = false;
  }
}

function openPasswordModal() {
  if (!els.passwordModal) return;
  els.passwordModal.hidden = false;
  if (els.passwordStatus) {
    els.passwordStatus.textContent = "";
    els.passwordStatus.classList.remove("success");
  }
  requestAnimationFrame(() => els.currentPassword?.focus());
}

function closePasswordModal() {
  if (!els.passwordModal) return;
  els.passwordModal.hidden = true;
  els.passwordForm?.reset();
  if (els.passwordStatus) {
    els.passwordStatus.textContent = "";
    els.passwordStatus.classList.remove("success");
  }
}

async function submitPasswordChange(event) {
  event.preventDefault();
  const currentPassword = els.currentPassword.value;
  const newPassword = els.newPassword.value;
  const confirmPassword = els.confirmPassword.value;

  els.passwordStatus.classList.remove("success");
  if (newPassword !== confirmPassword) {
    els.passwordStatus.textContent = t("passwordsNoMatch");
    return;
  }
  if (newPassword.length < 8) {
    els.passwordStatus.textContent = t("passwordTooShort");
    return;
  }

  els.savePasswordButton.disabled = true;
  els.passwordStatus.textContent = t("updatingPassword");
  try {
    const response = await fetch("/api/account/password", {
      method: "POST",
      headers: { ...accessHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify({ currentPassword, newPassword }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || t("passwordUpdateFailed"));
    els.passwordForm.reset();
    els.passwordStatus.classList.add("success");
    els.passwordStatus.textContent = t("passwordUpdated");
  } catch (error) {
    els.passwordStatus.classList.remove("success");
    els.passwordStatus.textContent = error.message;
  } finally {
    els.savePasswordButton.disabled = false;
  }
}

function visibleTourSteps() {
  return tourSteps.filter((step) => {
    const target = document.querySelector(step.selector);
    return target && !target.hidden && target.offsetParent !== null;
  });
}

function openTutorialModal() {
  if (!els.tourLayer) return;
  activeTourIndex = 0;
  els.tourLayer.hidden = false;
  renderTourStep();
}

function closeTutorialModal() {
  if (!els.tourLayer) return;
  els.tourLayer.hidden = true;
  document.querySelectorAll(".tour-target").forEach((item) => item.classList.remove("tour-target"));
  localStorage.setItem("codeBridge.tutorialSeen", "true");
}

function clampTooltip(left, top, width, height) {
  const margin = 14;
  return {
    left: Math.max(margin, Math.min(left, window.innerWidth - width - margin)),
    top: Math.max(margin, Math.min(top, window.innerHeight - height - margin)),
  };
}

function placeTourTooltip(target, placement) {
  const rect = target.getBoundingClientRect();
  const tooltip = els.tourTooltip;
  const gap = 16;
  const width = tooltip.offsetWidth || 320;
  const height = tooltip.offsetHeight || 180;
  let left = rect.right + gap;
  let top = rect.top;

  if (placement === "left") {
    left = rect.left - width - gap;
    top = rect.top;
  } else if (placement === "top") {
    left = rect.left + rect.width / 2 - width / 2;
    top = rect.top - height - gap;
  } else if (placement === "bottom") {
    left = rect.left + rect.width / 2 - width / 2;
    top = rect.bottom + gap;
  }

  const next = clampTooltip(left, top, width, height);
  tooltip.style.left = `${next.left}px`;
  tooltip.style.top = `${next.top}px`;
  tooltip.dataset.placement = placement;

  els.tourSpotlight.style.left = `${rect.left - 8}px`;
  els.tourSpotlight.style.top = `${rect.top - 8}px`;
  els.tourSpotlight.style.width = `${rect.width + 16}px`;
  els.tourSpotlight.style.height = `${rect.height + 16}px`;
}

function renderTourStep() {
  if (!els.tourLayer || els.tourLayer.hidden) return;
  const steps = visibleTourSteps();
  if (!steps.length) {
    closeTutorialModal();
    return;
  }
  activeTourIndex = Math.min(activeTourIndex, steps.length - 1);
  const step = steps[activeTourIndex];
  const target = document.querySelector(step.selector);
  if (!target) {
    activeTourIndex += 1;
    renderTourStep();
    return;
  }

  document.querySelectorAll(".tour-target").forEach((item) => item.classList.remove("tour-target"));
  target.classList.add("tour-target");
  target.scrollIntoView({ behavior: "smooth", block: "center", inline: "nearest" });

  els.tourStepCount.textContent = t("stepOf", { current: activeTourIndex + 1, total: steps.length });
  els.tourTitle.textContent = t(step.titleKey);
  els.tourText.textContent = t(step.textKey);
  els.tourNext.textContent = activeTourIndex === steps.length - 1 ? t("finish") : t("gotIt");

  setTimeout(() => {
    placeTourTooltip(target, step.placement || "right");
    els.tourNext.focus();
  }, 180);
}

function nextTourStep() {
  const steps = visibleTourSteps();
  if (activeTourIndex >= steps.length - 1) {
    closeTutorialModal();
    return;
  }
  activeTourIndex += 1;
  renderTourStep();
}

els.searchInput.addEventListener("input", (event) => {
  state.query = event.target.value;
  renderDayList();
});

els.languageSelect.addEventListener("change", (event) => {
  state.target = event.target.value;
  state.unlockedSampleCode = null;
  localStorage.setItem("racketTutor.targetLanguage", state.target);
  state.activeDay = 1;
  localStorage.setItem("racketTutor.activeDay", "1");
  scheduleProfileSave();
  loadCourse().catch((error) => {
    els.lessonTitle.textContent = error.message;
  });
});

els.interfaceLanguageSelect?.addEventListener("change", (event) => {
  setUiLanguage(event.target.value);
});

els.authForm.addEventListener("submit", submitAuth);
els.showRegister.addEventListener("click", () => setAuthMode("register"));
els.showLogin.addEventListener("click", () => setAuthMode("login"));
els.tutorialButton?.addEventListener("click", openTutorialModal);
els.changePasswordButton?.addEventListener("click", openPasswordModal);
els.logoutButton.addEventListener("click", logout);

els.noneExperience.addEventListener("change", () => {
  if (els.noneExperience.checked) writeKnownLanguages([]);
});

for (const input of els.languageExperienceInputs) {
  input.addEventListener("change", () => {
    if (input.checked) writeKnownLanguages([input.value]);
  });
}

els.continueFromExperience.addEventListener("click", continueFromLanguageExperience);
els.resetPrerequisite.addEventListener("click", resetPrerequisiteChoice);
els.markCppKnown.addEventListener("click", () => setCppStatus("knows_cpp"));

els.prevDay.addEventListener("click", () => selectDay(state.activeDay - 1));
els.nextDay.addEventListener("click", () => selectDay(state.activeDay + 1));

els.copyCode.addEventListener("click", async () => {
  if (els.codePanel.hidden || !state.unlockedSampleCode) return;
  await navigator.clipboard.writeText(state.unlockedSampleCode.code);
  els.copyCode.textContent = t("copied");
  setTimeout(() => {
    els.copyCode.textContent = t("copyCode");
  }, 1200);
});

els.resetChecklist.addEventListener("click", () => {
  writeChecklist(state.activeDay, []);
  renderLesson();
  loadGuidance();
});

els.submissionForm.addEventListener("submit", submitAssignment);
els.refreshSubmissions.addEventListener("click", loadSubmissions);
els.refreshGuidance?.addEventListener("click", loadGuidance);
els.feedbackButton?.addEventListener("click", openFeedbackModal);
els.closeFeedback?.addEventListener("click", closeFeedbackModal);
els.feedbackModal?.addEventListener("click", (event) => {
  if (event.target === els.feedbackModal) closeFeedbackModal();
});
els.siteFeedbackForm?.addEventListener("submit", submitSiteFeedback);
els.closePasswordModal?.addEventListener("click", closePasswordModal);
els.passwordModal?.addEventListener("click", (event) => {
  if (event.target === els.passwordModal) closePasswordModal();
});
els.passwordForm?.addEventListener("submit", submitPasswordChange);
els.tourSkip?.addEventListener("click", closeTutorialModal);
els.tourNext?.addEventListener("click", nextTourStep);
window.addEventListener("resize", renderTourStep);
window.addEventListener("scroll", renderTourStep, true);
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !els.feedbackModal?.hidden) {
    closeFeedbackModal();
  }
  if (event.key === "Escape" && !els.passwordModal?.hidden) {
    closePasswordModal();
  }
  if (event.key === "Escape" && !els.tourLayer?.hidden) {
    closeTutorialModal();
  }
});

applyStaticTranslations();
renderOnboarding();
loadSession().catch((error) => {
  els.authMessage.textContent = error.message;
});
