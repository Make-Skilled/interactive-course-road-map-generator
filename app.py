from flask import Flask, render_template, request, redirect, url_for, session, send_file
from pymongo import MongoClient
from xhtml2pdf import pisa
import io
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production

# MongoDB Atlas connection
client = MongoClient('mongodb+srv://gnana1313:Gnana1212@dbs.8wngtib.mongodb.net/?retryWrites=true&w=majority&appName=DBs')
db = client['roadmapdb']
users = db['users']

@app.route('/')
def home():
    # List of all supported languages/technologies (update this list as you add new ones)
    roadmap_languages = [
        'Python', 'Java', 'C++', 'C#', 'C', 'JavaScript', 'TypeScript', 'Go', 'Rust', 'Kotlin', 'Swift', 'Ruby', 'PHP', 'Dart', 'R Programming', 'Scala', 'Haskell', 'Shell Scripting', 'PowerShell', 'Perl', 'Lua', 'Assembly', 'Objective-C', 'Elixir', 'Fortran', 'COBOL', 'Ada', 'Groovy', 'F#', 'GDScript', 'HCL (Terraform)', 'YAML', 'JSON', 'XML', 'VHDL', 'Verilog', 'Solidity', 'Move', 'Clarity', 'OCaml', 'Nim', 'Crystal', 'Zig', 'Tcl', 'Makefile', 'ReScript', 'PureScript', 'CoffeeScript', 'LiveScript', 'ActionScript', 'Q#', 'Shader Languages', 'Racket', 'Scheme', 'Common Lisp', 'Prolog', 'Mercury', 'Smalltalk', 'Vala', 'Pony', 'Ballerina', 'Red', 'Hack', 'Apex', 'ABAP', 'LabVIEW', 'Scratch', 'Blockly', 'WebAssembly', 'ColdFusion', 'REXX', 'Pike', 'Eiffel', 'Inform', 'Nimrod', 'Xojo', 'Dlang', 'Genie', 'Io', 'Agda', 'Idris', 'Terra', 'Chapel', 'Ring', 'Oz', 'Boo', 'Janus', 'PL/I', 'ALGOL', 'Simula', 'Modula', 'Oberon', 'ML/SML/Caml', 'BCPL', 'Forth', 'PostScript', 'Handlebars', 'Mustache', 'FreeMarker', 'AWK', 'Sed'
    ]
    roadmap_count = len(roadmap_languages)
    return render_template('home.html', roadmap_languages=roadmap_languages, roadmap_count=roadmap_count)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if users.find_one({'email': email}):
            return render_template('signup.html', error='Email already exists!')
        users.insert_one({'name': name, 'email': email, 'password': password})
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.find_one({'email': email, 'password': password})
        if user:
            session['user'] = user['email']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials!')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    roadmap = None
    if request.method == 'POST':
        topic = request.form['topic']
        roadmap = generate_roadmap(topic)
    return render_template('dashboard.html', roadmap=roadmap)

def generate_roadmap(topic):
    topic_lower = topic.lower()
    # Python Example
    if re.search(r'\bpython\b', topic_lower):
        return {
            'title': '🐍 Python Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn the Basics - Syntax, Variables, Data Types, Conditionals'},
                {'title': 'Step 2', 'desc': 'Loops, Functions, Built-in Functions'},
                {'title': 'Step 3', 'desc': 'Data Structures - Lists, Tuples, Sets, Dictionaries'},
                {'title': 'Step 4', 'desc': 'OOP - Classes, Inheritance, Objects'},
                {'title': 'Step 5', 'desc': 'Advance Topics 1 - RegEx, Decorators, Lambda'},
                {'title': 'Step 6', 'desc': 'Advanced Topics 2 - Modules, Iterators'},
                {'title': 'Step 7', 'desc': 'Learn Python Libraries'},
                {'title': 'Step 8', 'desc': 'Learn Version Control Systems'},
                {'title': 'Step 9', 'desc': 'Build Python Apps'}
            ]
        }
    # Java Example
    if re.search(r'\bjava\b', topic_lower):
        return {
            'title': '☕ Java Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn the Basics - Syntax, Variables, Data Types, Conditionals'},
                {'title': 'Step 2', 'desc': 'Loops, Methods, Built-in Functions'},
                {'title': 'Step 3', 'desc': 'OOP - Classes, Inheritance, Objects, Interfaces'},
                {'title': 'Step 4', 'desc': 'Collections - Lists, Sets, Maps'},
                {'title': 'Step 5', 'desc': 'Exception Handling & File I/O'},
                {'title': 'Step 6', 'desc': 'Multithreading & Concurrency'},
                {'title': 'Step 7', 'desc': 'Java Libraries & Frameworks'},
                {'title': 'Step 8', 'desc': 'Version Control & Build Tools'},
                {'title': 'Step 9', 'desc': 'Build Java Apps'}
            ]
        }
    # C++ Example
    if re.search(r'\bc\+\+\b', topic_lower):
        return {
            'title': '💻 C++ Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Syntax, Variables, Data Types, and Operators'},
                {'title': 'Step 2', 'desc': 'Control Flow - If-Else, Loops, Switch'},
                {'title': 'Step 3', 'desc': 'Functions and Scope'},
                {'title': 'Step 4', 'desc': 'Pointers and Memory Management'},
                {'title': 'Step 5', 'desc': 'OOP - Classes, Objects, Inheritance, Polymorphism'},
                {'title': 'Step 6', 'desc': 'STL - Vectors, Maps, Sets, Queues'},
                {'title': 'Step 7', 'desc': 'File Handling and Exception Handling'},
                {'title': 'Step 8', 'desc': 'Build Projects using C++'},
                {'title': 'Step 9', 'desc': 'Data Structures & Algorithms in C++'}
            ]
        }
    # C# Example
    if re.search(r'\bc#\b', topic_lower):
        return {
            'title': '🎯 C# Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn Syntax, Variables, Data Types, Operators'},
                {'title': 'Step 2', 'desc': 'Control Structures - Loops, Conditionals'},
                {'title': 'Step 3', 'desc': 'OOP - Classes, Interfaces, Inheritance'},
                {'title': 'Step 4', 'desc': 'Collections and LINQ'},
                {'title': 'Step 5', 'desc': 'Exception Handling & File I/O'},
                {'title': 'Step 6', 'desc': 'Asynchronous Programming - async/await'},
                {'title': 'Step 7', 'desc': '.NET Libraries & Frameworks'},
                {'title': 'Step 8', 'desc': 'Build C# Applications (Desktop/Web)'},
                {'title': 'Step 9', 'desc': 'Version Control and Deployment'}
            ]
        }
    # C Example (not C++)
    if re.search(r'\bc\b', topic_lower) and not re.search(r'\bc\+\+\b', topic_lower):
        return {
            'title': '🔧 C Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Syntax, Variables, Data Types, Operators'},
                {'title': 'Step 2', 'desc': 'Control Statements - If, Loops, Switch'},
                {'title': 'Step 3', 'desc': 'Functions and Recursion'},
                {'title': 'Step 4', 'desc': 'Pointers and Arrays'},
                {'title': 'Step 5', 'desc': 'Structures and Unions'},
                {'title': 'Step 6', 'desc': 'File Handling and Preprocessor Directives'},
                {'title': 'Step 7', 'desc': 'Dynamic Memory Allocation'},
                {'title': 'Step 8', 'desc': 'Mini Projects with C'},
                {'title': 'Step 9', 'desc': 'Debugging and Optimization'}
            ]
        }
    # JavaScript/TypeScript Example
    if re.search(r'\bjavascript\b', topic_lower) or re.search(r'\btypescript\b', topic_lower):
        return {
            'title': '🌐 JavaScript/TypeScript Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn the Basics - Syntax, Variables, Data Types, Conditionals'},
                {'title': 'Step 2', 'desc': 'Functions, Loops, Scope, Hoisting'},
                {'title': 'Step 3', 'desc': 'DOM Manipulation & Events'},
                {'title': 'Step 4', 'desc': 'OOP - Prototypes, Classes, Inheritance'},
                {'title': 'Step 5', 'desc': 'Async Programming - Callbacks, Promises, Async/Await'},
                {'title': 'Step 6', 'desc': 'TypeScript Features (If applicable)'},
                {'title': 'Step 7', 'desc': 'Tooling - npm, Webpack, Babel'},
                {'title': 'Step 8', 'desc': 'Frameworks - React, Vue, Angular'},
                {'title': 'Step 9', 'desc': 'Build JS/TS Apps'}
            ]
        }
    # Go Example
    if re.search(r'\bgo\b', topic_lower) or re.search(r'\bgolang\b', topic_lower):
        return {
            'title': '🐹 Go (Golang) Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Install Go and Set Up Environment'},
                {'title': 'Step 2', 'desc': 'Basics - Variables, Types, Control Structures'},
                {'title': 'Step 3', 'desc': 'Functions, Error Handling, and Packages'},
                {'title': 'Step 4', 'desc': 'Go Routines and Channels'},
                {'title': 'Step 5', 'desc': 'Structs, Interfaces, and Methods'},
                {'title': 'Step 6', 'desc': 'File I/O and Testing'},
                {'title': 'Step 7', 'desc': 'Build Web Servers using net/http'},
                {'title': 'Step 8', 'desc': 'Learn Popular Libraries'},
                {'title': 'Step 9', 'desc': 'Build Go Projects'}
            ]
        }
    # Rust Example
    if "rust" in topic_lower:
        return {
            'title': '🦀 Rust Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Install Rust and Learn Cargo Basics'},
                {'title': 'Step 2', 'desc': 'Syntax, Variables, Ownership and Borrowing'},
                {'title': 'Step 3', 'desc': 'Data Types, Functions, and Control Flow'},
                {'title': 'Step 4', 'desc': 'Structs, Enums, and Pattern Matching'},
                {'title': 'Step 5', 'desc': 'Collections and Iterators'},
                {'title': 'Step 6', 'desc': 'Error Handling and Lifetimes'},
                {'title': 'Step 7', 'desc': 'Concurrency and Channels'},
                {'title': 'Step 8', 'desc': 'Build CLI and Web Projects'},
                {'title': 'Step 9', 'desc': 'Testing and Performance Optimization'}
            ]
        }
    # Kotlin Example
    if "kotlin" in topic_lower:
        return {
            'title': '📱 Kotlin Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn the Basics - Syntax, Data Types, Variables'},
                {'title': 'Step 2', 'desc': 'Control Flow, Functions, Null Safety'},
                {'title': 'Step 3', 'desc': 'OOP - Classes, Inheritance, Interfaces'},
                {'title': 'Step 4', 'desc': 'Collections and Lambdas'},
                {'title': 'Step 5', 'desc': 'Coroutines and Concurrency'},
                {'title': 'Step 6', 'desc': 'Kotlin Standard Library'},
                {'title': 'Step 7', 'desc': 'Android Development with Kotlin'},
                {'title': 'Step 8', 'desc': 'Build Tools and Testing'},
                {'title': 'Step 9', 'desc': 'Projects and Deployment'}
            ]
        }
    # Swift Example
    if "swift" in topic_lower:
        return {
            'title': '🍎 Swift Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Syntax, Variables, Constants, and Data Types'},
                {'title': 'Step 2', 'desc': 'Control Flow - If, Switch, Loops'},
                {'title': 'Step 3', 'desc': 'Functions, Closures, and Scope'},
                {'title': 'Step 4', 'desc': 'OOP - Classes, Structs, Inheritance'},
                {'title': 'Step 5', 'desc': 'Error Handling and Optionals'},
                {'title': 'Step 6', 'desc': 'Collections and Generics'},
                {'title': 'Step 7', 'desc': 'Protocols and Extensions'},
                {'title': 'Step 8', 'desc': 'SwiftUI Basics and Views'},
                {'title': 'Step 9', 'desc': 'iOS App Development Workflow'},
                {'title': 'Step 10', 'desc': 'Testing and Publishing Apps to App Store'}
            ]
        }
    # Ruby Example
    if "ruby" in topic_lower:
        return {
            'title': '💎 Ruby Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn Syntax, Data Types, Variables'},
                {'title': 'Step 2', 'desc': 'Control Structures - If, Loops, Case'},
                {'title': 'Step 3', 'desc': 'Methods, Blocks, and Lambdas'},
                {'title': 'Step 4', 'desc': 'OOP - Classes, Modules, Inheritance'},
                {'title': 'Step 5', 'desc': 'Exception Handling'},
                {'title': 'Step 6', 'desc': 'Gems and Bundler'},
                {'title': 'Step 7', 'desc': 'File I/O and Databases'},
                {'title': 'Step 8', 'desc': 'Intro to Rails Framework'},
                {'title': 'Step 9', 'desc': 'Build Full-stack Ruby on Rails App'},
                {'title': 'Step 10', 'desc': 'Testing and Deployment'}
            ]
        }
    # PHP Example
    if "php" in topic_lower:
        return {
            'title': '🐘 PHP Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Basic Syntax, Variables, Data Types'},
                {'title': 'Step 2', 'desc': 'Operators, Control Flow - If, Switch, Loops'},
                {'title': 'Step 3', 'desc': 'Functions and Scope'},
                {'title': 'Step 4', 'desc': 'Forms, $_GET, $_POST'},
                {'title': 'Step 5', 'desc': 'Sessions, Cookies, and File Uploads'},
                {'title': 'Step 6', 'desc': 'OOP - Classes, Interfaces, Traits'},
                {'title': 'Step 7', 'desc': 'Database Integration - MySQLi, PDO'},
                {'title': 'Step 8', 'desc': 'Frameworks - Laravel, Symfony'},
                {'title': 'Step 9', 'desc': 'REST API Development with PHP'},
                {'title': 'Step 10', 'desc': 'Security, Testing, and Deployment'}
            ]
        }
    # Dart Example
    if "dart" in topic_lower:
        return {
            'title': '🎯 Dart Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Syntax, Variables, Data Types'},
                {'title': 'Step 2', 'desc': 'Control Flow, Functions, Collections'},
                {'title': 'Step 3', 'desc': 'OOP - Classes, Inheritance, Mixins'},
                {'title': 'Step 4', 'desc': 'Async Programming - Futures, Streams'},
                {'title': 'Step 5', 'desc': 'Error Handling and Null Safety'},
                {'title': 'Step 6', 'desc': 'Dart Packages and Pub'},
                {'title': 'Step 7', 'desc': 'Intro to Flutter and Widgets'},
                {'title': 'Step 8', 'desc': 'State Management in Flutter'},
                {'title': 'Step 9', 'desc': 'Building Cross-Platform Apps'},
                {'title': 'Step 10', 'desc': 'Testing and App Deployment'}
            ]
        }
    # R Example
    if re.search(r'\br programming\b', topic_lower):
        return {
            'title': '📊 R Programming Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Install R and RStudio'},
                {'title': 'Step 2', 'desc': 'Data Types, Vectors, Lists, Matrices'},
                {'title': 'Step 3', 'desc': 'Functions and Control Structures'},
                {'title': 'Step 4', 'desc': 'Data Manipulation with dplyr'},
                {'title': 'Step 5', 'desc': 'Data Visualization with ggplot2'},
                {'title': 'Step 6', 'desc': 'Working with Data Frames & Tibbles'},
                {'title': 'Step 7', 'desc': 'Statistical Analysis & Hypothesis Testing'},
                {'title': 'Step 8', 'desc': 'Time Series and Forecasting'},
                {'title': 'Step 9', 'desc': 'Machine Learning in R'},
                {'title': 'Step 10', 'desc': 'Report Building with RMarkdown & Shiny'}
            ]
        }
    # Julia Example
    if "julia" in topic_lower:
        return {
            'title': '🚀 Julia Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Install Julia and Setup Environment'},
                {'title': 'Step 2', 'desc': 'Learn Basic Syntax, Types, and Variables'},
                {'title': 'Step 3', 'desc': 'Control Structures, Loops, Functions'},
                {'title': 'Step 4', 'desc': 'Packages and Modules'},
                {'title': 'Step 5', 'desc': 'Array and Matrix Operations'},
                {'title': 'Step 6', 'desc': 'Plotting with Plots.jl or Makie.jl'},
                {'title': 'Step 7', 'desc': 'DataFrames.jl for Data Analysis'},
                {'title': 'Step 8', 'desc': 'Numerical Computation and Linear Algebra'},
                {'title': 'Step 9', 'desc': 'Machine Learning with Flux.jl'},
                {'title': 'Step 10', 'desc': 'Performance Optimization and Parallelism'}
            ]
        }
    # MATLAB Example
    if "matlab" in topic_lower:
        return {
            'title': '📐 MATLAB Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'MATLAB Environment and Syntax Basics'},
                {'title': 'Step 2', 'desc': 'Variables, Scripts, and Functions'},
                {'title': 'Step 3', 'desc': 'Vectors, Matrices, and Array Operations'},
                {'title': 'Step 4', 'desc': 'Plotting and Visualization'},
                {'title': 'Step 5', 'desc': 'Conditional Statements and Loops'},
                {'title': 'Step 6', 'desc': 'File I/O and Data Importing'},
                {'title': 'Step 7', 'desc': 'Simulink Introduction'},
                {'title': 'Step 8', 'desc': 'Toolboxes for Image, Signal, and Control'},
                {'title': 'Step 9', 'desc': 'Optimization and Curve Fitting'},
                {'title': 'Step 10', 'desc': 'Modeling and Simulation Projects'}
            ]
        }
    # Scala Example
    if "scala" in topic_lower:
        return {
            'title': '🔷 Scala Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Scala Syntax and Functional Concepts'},
                {'title': 'Step 2', 'desc': 'Variables, Functions, and Expressions'},
                {'title': 'Step 3', 'desc': 'OOP - Classes, Traits, Inheritance'},
                {'title': 'Step 4', 'desc': 'Collections and Pattern Matching'},
                {'title': 'Step 5', 'desc': 'Higher-Order Functions and Closures'},
                {'title': 'Step 6', 'desc': 'Error Handling and Futures'},
                {'title': 'Step 7', 'desc': 'Build Tools - sbt, IntelliJ Setup'},
                {'title': 'Step 8', 'desc': 'Big Data with Spark (Scala API)'},
                {'title': 'Step 9', 'desc': 'Test Frameworks - ScalaTest, Specs2'},
                {'title': 'Step 10', 'desc': 'Scala Projects and Deployment'}
            ]
        }
    # Haskell Example
    if "haskell" in topic_lower:
        return {
            'title': '📐 Haskell Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn Pure Functional Programming Basics'},
                {'title': 'Step 2', 'desc': 'Syntax, Variables, and Functions'},
                {'title': 'Step 3', 'desc': 'Recursion and Pattern Matching'},
                {'title': 'Step 4', 'desc': 'Lists, Tuples, and Higher-Order Functions'},
                {'title': 'Step 5', 'desc': 'Type System and Type Classes'},
                {'title': 'Step 6', 'desc': 'Monads and Functors'},
                {'title': 'Step 7', 'desc': 'I/O in Haskell'},
                {'title': 'Step 8', 'desc': 'Modules and Lazy Evaluation'},
                {'title': 'Step 9', 'desc': 'Concurrency and STM'},
                {'title': 'Step 10', 'desc': 'Real Projects and Performance'}
            ]
        }
    # Shell Scripting Example
    if "shell" in topic_lower or "bash" in topic_lower or "zsh" in topic_lower:
        return {
            'title': '🐚 Shell Scripting Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Basics of Terminal, Bash/Zsh, and CLI'},
                {'title': 'Step 2', 'desc': 'Variables, Quotes, and Escape Characters'},
                {'title': 'Step 3', 'desc': 'Conditional Statements and Loops'},
                {'title': 'Step 4', 'desc': 'Functions and Script Arguments'},
                {'title': 'Step 5', 'desc': 'Input/Output Redirection and Pipes'},
                {'title': 'Step 6', 'desc': 'Working with Files and Directories'},
                {'title': 'Step 7', 'desc': 'Crontab and Scheduling Tasks'},
                {'title': 'Step 8', 'desc': 'System Commands and Process Management'},
                {'title': 'Step 9', 'desc': 'Debugging and Logging'},
                {'title': 'Step 10', 'desc': 'Advanced Bash Features and Real Scripts'}
            ]
        }
    # PowerShell Example
    if "powershell" in topic_lower:
        return {
            'title': '🪟 PowerShell Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand PowerShell Basics and Cmdlets'},
                {'title': 'Step 2', 'desc': 'Variables, Data Types, and Operators'},
                {'title': 'Step 3', 'desc': 'Conditional Logic and Loops'},
                {'title': 'Step 4', 'desc': 'Functions and Parameters'},
                {'title': 'Step 5', 'desc': 'Working with Files, Directories, and Registry'},
                {'title': 'Step 6', 'desc': 'Modules, Importing and Exporting'},
                {'title': 'Step 7', 'desc': 'Object-Oriented Features and Pipelining'},
                {'title': 'Step 8', 'desc': 'Error Handling and Debugging'},
                {'title': 'Step 9', 'desc': 'Scheduled Tasks and Automation Scripts'},
                {'title': 'Step 10', 'desc': 'Remote Management and Active Directory'}
            ]
        }
    # Perl Example
    if "perl" in topic_lower:
        return {
            'title': '🧬 Perl Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Basic Syntax, Variables, and Operators'},
                {'title': 'Step 2', 'desc': 'Control Structures - If, Loops'},
                {'title': 'Step 3', 'desc': 'Subroutines and Arguments'},
                {'title': 'Step 4', 'desc': 'Data Structures - Arrays, Hashes'},
                {'title': 'Step 5', 'desc': 'Regular Expressions and Pattern Matching'},
                {'title': 'Step 6', 'desc': 'File Handling and I/O'},
                {'title': 'Step 7', 'desc': 'Modules and CPAN'},
                {'title': 'Step 8', 'desc': 'Object-Oriented Perl'},
                {'title': 'Step 9', 'desc': 'Perl for Web and Scripting Tasks'},
                {'title': 'Step 10', 'desc': 'Debugging, Testing, and Best Practices'}
            ]
        }
    # Lua Example
    if "lua" in topic_lower:
        return {
            'title': '🌙 Lua Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Syntax, Variables, Data Types'},
                {'title': 'Step 2', 'desc': 'Control Structures and Loops'},
                {'title': 'Step 3', 'desc': 'Functions and Closures'},
                {'title': 'Step 4', 'desc': 'Tables - Core Data Structure'},
                {'title': 'Step 5', 'desc': 'Metatables and Metamethods'},
                {'title': 'Step 6', 'desc': 'Modules and Libraries'},
                {'title': 'Step 7', 'desc': 'Coroutines and Concurrency'},
                {'title': 'Step 8', 'desc': 'Embedding Lua in Applications'},
                {'title': 'Step 9', 'desc': 'Game Development with Lua (e.g. Love2D)'},
                {'title': 'Step 10', 'desc': 'Performance Optimization'}
            ]
        }
    # Assembly Example
    if "assembly" in topic_lower:
        return {
            'title': '💾 Assembly Language Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand CPU Architectures (x86, ARM, RISC-V)'},
                {'title': 'Step 2', 'desc': 'Assembly Syntax and Registers'},
                {'title': 'Step 3', 'desc': 'Data Movement Instructions'},
                {'title': 'Step 4', 'desc': 'Arithmetic and Logical Operations'},
                {'title': 'Step 5', 'desc': 'Branching, Loops, and Jumps'},
                {'title': 'Step 6', 'desc': 'Subroutines and Stack Usage'},
                {'title': 'Step 7', 'desc': 'Memory Addressing Modes'},
                {'title': 'Step 8', 'desc': 'Interrupts and System Calls'},
                {'title': 'Step 9', 'desc': 'Debugging with GDB/objdump'},
                {'title': 'Step 10', 'desc': 'Build and Run OS-Level or Bootloader Projects'}
            ]
        }
    # SQL Example
    if "sql" in topic_lower:
        return {
            'title': '🗃️ SQL Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn Relational Database Concepts'},
                {'title': 'Step 2', 'desc': 'Basic Queries - SELECT, WHERE, ORDER BY'},
                {'title': 'Step 3', 'desc': 'INSERT, UPDATE, DELETE Commands'},
                {'title': 'Step 4', 'desc': 'Filtering, Pattern Matching (LIKE, IN, BETWEEN)'},
                {'title': 'Step 5', 'desc': 'Joins - INNER, LEFT, RIGHT, FULL'},
                {'title': 'Step 6', 'desc': 'Group By, Aggregations, HAVING'},
                {'title': 'Step 7', 'desc': 'Subqueries and Nested Queries'},
                {'title': 'Step 8', 'desc': 'Constraints, Indexes, and Views'},
                {'title': 'Step 9', 'desc': 'Stored Procedures, Triggers, Functions'},
                {'title': 'Step 10', 'desc': 'Normalization and Query Optimization'}
            ]
        }
    # NoSQL Example
    if "nosql" in topic_lower or "mongodb" in topic_lower or "cql" in topic_lower:
        return {
            'title': '🧩 NoSQL Query Language Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand NoSQL Types - Document, Column, Key-Value, Graph'},
                {'title': 'Step 2', 'desc': 'MongoDB Query Language - CRUD Operations'},
                {'title': 'Step 3', 'desc': 'Working with BSON Documents'},
                {'title': 'Step 4', 'desc': 'Indexes and Aggregation Framework'},
                {'title': 'Step 5', 'desc': 'CQL (Cassandra Query Language) - Basics'},
                {'title': 'Step 6', 'desc': 'Create/Update Tables in CQL'},
                {'title': 'Step 7', 'desc': 'Query with SELECT, WHERE, ORDER in CQL'},
                {'title': 'Step 8', 'desc': 'Schema Design for NoSQL'},
                {'title': 'Step 9', 'desc': 'Transactions and Consistency Models'},
                {'title': 'Step 10', 'desc': 'Best Practices and Performance Tuning'}
            ]
        }
    # Objective-C Example
    if "objective-c" in topic_lower:
        return {
            'title': '🍏 Objective-C Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Syntax, Variables, and Data Types'},
                {'title': 'Step 2', 'desc': 'Control Flow - If, Loops, Switch'},
                {'title': 'Step 3', 'desc': 'Functions and Methods'},
                {'title': 'Step 4', 'desc': 'OOP - Classes, Inheritance, and Categories'},
                {'title': 'Step 5', 'desc': 'Memory Management and ARC'},
                {'title': 'Step 6', 'desc': 'Foundation and UIKit Frameworks'},
                {'title': 'Step 7', 'desc': 'Interface Builder and Xcode Integration'},
                {'title': 'Step 8', 'desc': 'Event Handling and Delegates'},
                {'title': 'Step 9', 'desc': 'iOS App Architecture and MVC'},
                {'title': 'Step 10', 'desc': 'Debugging and App Submission'}
            ]
        }
    # Elixir Example
    if "elixir" in topic_lower:
        return {
            'title': '💡 Elixir Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Syntax, Variables, Pattern Matching'},
                {'title': 'Step 2', 'desc': 'Functions, Modules, and Recursion'},
                {'title': 'Step 3', 'desc': 'Immutable Data and Enum Module'},
                {'title': 'Step 4', 'desc': 'Concurrency with Processes'},
                {'title': 'Step 5', 'desc': 'OTP - GenServer, Supervisors'},
                {'title': 'Step 6', 'desc': 'Mix Tool and Project Structure'},
                {'title': 'Step 7', 'desc': 'Phoenix Framework Basics'},
                {'title': 'Step 8', 'desc': 'LiveView and Real-Time Apps'},
                {'title': 'Step 9', 'desc': 'Testing with ExUnit'},
                {'title': 'Step 10', 'desc': 'Deployment and Releases'}
            ]
        }
    # VBScript Example
    if "vbscript" in topic_lower:
        return {
            'title': '📝 VBScript Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Syntax, Variables, and Data Types'},
                {'title': 'Step 2', 'desc': 'Control Structures - If, For, While'},
                {'title': 'Step 3', 'desc': 'Functions, Subroutines, and Scope'},
                {'title': 'Step 4', 'desc': 'Working with theFileSystemObject'},
                {'title': 'Step 5', 'desc': 'Windows Script Host (WSH) Integration'},
                {'title': 'Step 6', 'desc': 'Error Handling and Debugging'},
                {'title': 'Step 7', 'desc': 'Working with COM Objects'},
                {'title': 'Step 8', 'desc': 'Automating Tasks via Scripts'},
                {'title': 'Step 9', 'desc': 'Security and Script Signing'},
                {'title': 'Step 10', 'desc': 'Legacy Support and Migration Tips'}
            ]
        }
    # VB.NET Example
    if "vb.net" in topic_lower or "visual basic .net" in topic_lower:
        return {
            'title': '🧮 Visual Basic .NET Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'VB.NET Syntax and .NET Framework Basics'},
                {'title': 'Step 2', 'desc': 'Variables, Data Types, and Operators'},
                {'title': 'Step 3', 'desc': 'Control Flow - If, Select, Loops'},
                {'title': 'Step 4', 'desc': 'Object-Oriented Programming'},
                {'title': 'Step 5', 'desc': 'Windows Forms and GUI Design'},
                {'title': 'Step 6', 'desc': 'File I/O and Error Handling'},
                {'title': 'Step 7', 'desc': 'ADO.NET and Database Access'},
                {'title': 'Step 8', 'desc': 'LINQ and XML Processing'},
                {'title': 'Step 9', 'desc': 'Web Applications using ASP.NET'},
                {'title': 'Step 10', 'desc': 'Publishing, Deployment, and Debugging'}
            ]
        }
    # Fortran Example
    if "fortran" in topic_lower:
        return {
            'title': '📐 Fortran Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Fortran History and Modern Versions (90/95/2003)'},
                {'title': 'Step 2', 'desc': 'Basic Syntax, Data Types, and Variables'},
                {'title': 'Step 3', 'desc': 'Control Flow - IF, DO, SELECT'},
                {'title': 'Step 4', 'desc': 'Arrays and Intrinsic Functions'},
                {'title': 'Step 5', 'desc': 'Modules, Procedures, and Functions'},
                {'title': 'Step 6', 'desc': 'I/O Statements and File Handling'},
                {'title': 'Step 7', 'desc': 'Memory Management and Pointers'},
                {'title': 'Step 8', 'desc': 'Parallel Programming with OpenMP/MPI'},
                {'title': 'Step 9', 'desc': 'Numerical Methods and Libraries'},
                {'title': 'Step 10', 'desc': 'Build Scientific Applications'}
            ]
        }
    # COBOL Example
    if "cobol" in topic_lower:
        return {
            'title': '📄 COBOL Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand COBOL Structure and Data Division'},
                {'title': 'Step 2', 'desc': 'Basic Syntax and Variables'},
                {'title': 'Step 3', 'desc': 'PERFORM Loops and IF Statements'},
                {'title': 'Step 4', 'desc': 'File Handling - SEQUENTIAL, RELATIVE, INDEXED'},
                {'title': 'Step 5', 'desc': 'Tables and OCCURS Clause'},
                {'title': 'Step 6', 'desc': 'Working-Storage and Data Validation'},
                {'title': 'Step 7', 'desc': 'Subprograms and Linkage Section'},
                {'title': 'Step 8', 'desc': 'Integration with JCL and Mainframes'},
                {'title': 'Step 9', 'desc': 'COBOL in Banking and Finance Systems'},
                {'title': 'Step 10', 'desc': 'Debugging and Modernization Tools'}
            ]
        }
    # Ada Example
    if "ada" in topic_lower:
        return {
            'title': '🚀 Ada Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': "Understand Ada's Safety and Mission-Critical Use"},
                {'title': 'Step 2', 'desc': 'Basic Syntax, Packages, and Variables'},
                {'title': 'Step 3', 'desc': 'Control Statements and Loops'},
                {'title': 'Step 4', 'desc': 'Procedures, Functions, and Parameters'},
                {'title': 'Step 5', 'desc': 'Strong Typing and Type Declarations'},
                {'title': 'Step 6', 'desc': 'Concurrency - Tasks and Protected Objects'},
                {'title': 'Step 7', 'desc': 'Exception Handling'},
                {'title': 'Step 8', 'desc': 'Generics and Modular Design'},
                {'title': 'Step 9', 'desc': 'Project with GNAT and SPARK'},
                {'title': 'Step 10', 'desc': 'Critical System Certification & Testing'}
            ]
        }
    # Groovy Example
    if "groovy" in topic_lower:
        return {
            'title': '🎶 Groovy Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Groovy Syntax and Dynamic Nature'},
                {'title': 'Step 2', 'desc': 'Variables, Strings, and Collections'},
                {'title': 'Step 3', 'desc': 'Closures and Functional Programming'},
                {'title': 'Step 4', 'desc': 'OOP and Meta-Programming'},
                {'title': 'Step 5', 'desc': 'File and XML Processing'},
                {'title': 'Step 6', 'desc': 'Build Automation with Gradle'},
                {'title': 'Step 7', 'desc': 'Groovy in Jenkins Pipelines'},
                {'title': 'Step 8', 'desc': 'Groovy Web Frameworks (e.g. Grails)'},
                {'title': 'Step 9', 'desc': 'Unit Testing with Spock'},
                {'title': 'Step 10', 'desc': 'Deployment and Automation Scripts'}
            ]
        }
    # F# Example
    if "f#" in topic_lower:
        return {
            'title': '♻️ F# Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand F# and Functional Concepts'},
                {'title': 'Step 2', 'desc': 'Data Types, Immutability, and Pattern Matching'},
                {'title': 'Step 3', 'desc': 'Functions and Pipelining'},
                {'title': 'Step 4', 'desc': 'Discriminated Unions and Records'},
                {'title': 'Step 5', 'desc': 'OOP Support in F#'},
                {'title': 'Step 6', 'desc': 'Working with Collections and Lists'},
                {'title': 'Step 7', 'desc': 'F# Interactive and Scripting'},
                {'title': 'Step 8', 'desc': 'Data Analysis with FSharp.Data'},
                {'title': 'Step 9', 'desc': 'Testing and Debugging'},
                {'title': 'Step 10', 'desc': 'Building Apps with .NET and F#'}
            ]
        }
    # GDScript Example
    if "gdscript" in topic_lower:
        return {
            'title': '🎮 GDScript Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Install Godot and Understand Scene System'},
                {'title': 'Step 2', 'desc': 'Learn GDScript Syntax and Basics'},
                {'title': 'Step 3', 'desc': 'Signals and Input Handling'},
                {'title': 'Step 4', 'desc': '2D Game Physics and Animation'},
                {'title': 'Step 5', 'desc': 'Node Hierarchies and Scripting'},
                {'title': 'Step 6', 'desc': 'TileMaps, UI, and Audio'},
                {'title': 'Step 7', 'desc': 'Export Settings and Optimization'},
                {'title': 'Step 8', 'desc': '3D Game Basics (if needed)'},
                {'title': 'Step 9', 'desc': 'Project Architecture'},
                {'title': 'Step 10', 'desc': 'Publish Game to Web/Desktop/Mobile'}
            ]
        }
    # HCL (Terraform) Example
    if "hcl" in topic_lower or "terraform" in topic_lower:
        return {
            'title': '🌍 HCL (Terraform) Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Infrastructure as Code Concepts'},
                {'title': 'Step 2', 'desc': 'Learn Terraform Syntax and Providers'},
                {'title': 'Step 3', 'desc': 'Variables, Outputs, and Resources'},
                {'title': 'Step 4', 'desc': 'Modules and Workspaces'},
                {'title': 'Step 5', 'desc': 'State Files and Backend Configuration'},
                {'title': 'Step 6', 'desc': 'Loops and Conditional Expressions'},
                {'title': 'Step 7', 'desc': 'Remote State and State Locking'},
                {'title': 'Step 8', 'desc': 'Terraform Cloud and CI/CD Integration'},
                {'title': 'Step 9', 'desc': 'Security and Secrets Management'},
                {'title': 'Step 10', 'desc': 'Deploy Infrastructure Projects'}
            ]
        }
    # YAML Example
    if "yaml" in topic_lower:
        return {
            'title': '📘 YAML Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn YAML Syntax and Structure'},
                {'title': 'Step 2', 'desc': 'Scalars, Lists, and Mappings'},
                {'title': 'Step 3', 'desc': 'Anchors, Aliases, and References'},
                {'title': 'Step 4', 'desc': 'Multiline Strings and Comments'},
                {'title': 'Step 5', 'desc': 'YAML Validation Tools'},
                {'title': 'Step 6', 'desc': 'Use in Docker Compose'},
                {'title': 'Step 7', 'desc': 'Kubernetes Configuration Files'},
                {'title': 'Step 8', 'desc': 'CI/CD Pipelines in YAML (GitHub Actions)'},
                {'title': 'Step 9', 'desc': 'Environment Configurations'},
                {'title': 'Step 10', 'desc': 'Secure and Readable YAML Practices'}
            ]
        }
    # JSON Example
    if "json" in topic_lower:
        return {
            'title': '🔧 JSON Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn JSON Syntax and Structure'},
                {'title': 'Step 2', 'desc': 'Key-Value Pairs and Data Types'},
                {'title': 'Step 3', 'desc': 'Arrays and Nested Structures'},
                {'title': 'Step 4', 'desc': 'JSON Parsing and Stringification'},
                {'title': 'Step 5', 'desc': 'Using JSON in JavaScript/Python/Java'},
                {'title': 'Step 6', 'desc': 'APIs and JSON Responses'},
                {'title': 'Step 7', 'desc': 'Working with JSON Schema'},
                {'title': 'Step 8', 'desc': 'Validation and Error Handling'},
                {'title': 'Step 9', 'desc': 'Large File Processing'},
                {'title': 'Step 10', 'desc': 'Security and Injection Protection'}
            ]
        }
    # XML Example
    if "xml" in topic_lower:
        return {
            'title': '🗂️ XML Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn XML Tags, Attributes, and Structure'},
                {'title': 'Step 2', 'desc': 'Nested Elements and Comments'},
                {'title': 'Step 3', 'desc': 'DTD and XML Schema (XSD)'},
                {'title': 'Step 4', 'desc': 'XPath for Querying XML'},
                {'title': 'Step 5', 'desc': 'XSLT for Transformations'},
                {'title': 'Step 6', 'desc': 'Parsing XML in Python/Java/JS'},
                {'title': 'Step 7', 'desc': 'Namespaces and Validation'},
                {'title': 'Step 8', 'desc': 'Web Services - SOAP & WSDL'},
                {'title': 'Step 9', 'desc': 'Storing and Indexing XML'},
                {'title': 'Step 10', 'desc': 'Security and Large File Optimization'}
            ]
        }
    # VHDL Example
    if "vhdl" in topic_lower:
        return {
            'title': '🔌 VHDL Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Digital Design and FPGA Basics'},
                {'title': 'Step 2', 'desc': 'VHDL Syntax - Entity and Architecture'},
                {'title': 'Step 3', 'desc': 'Data Types and Signals'},
                {'title': 'Step 4', 'desc': 'Processes, Variables, and Signals'},
                {'title': 'Step 5', 'desc': 'Concurrent vs Sequential Statements'},
                {'title': 'Step 6', 'desc': 'Finite State Machines (FSMs)'},
                {'title': 'Step 7', 'desc': 'Test Benches and Simulation'},
                {'title': 'Step 8', 'desc': 'Synthesis and Timing Constraints'},
                {'title': 'Step 9', 'desc': 'Implement on FPGA Boards'},
                {'title': 'Step 10', 'desc': 'HDL Design Best Practices'}
            ]
        }
    # Verilog Example
    if "verilog" in topic_lower:
        return {
            'title': '📐 Verilog Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Verilog Syntax and Modules'},
                {'title': 'Step 2', 'desc': 'Ports, Wires, and Registers'},
                {'title': 'Step 3', 'desc': 'Always Blocks and Timing Control'},
                {'title': 'Step 4', 'desc': 'Data Flow and Behavioral Modeling'},
                {'title': 'Step 5', 'desc': 'FSMs and Sequential Circuits'},
                {'title': 'Step 6', 'desc': 'Simulation with Test Benches'},
                {'title': 'Step 7', 'desc': 'Synthesis and Constraints'},
                {'title': 'Step 8', 'desc': 'Toolchains and FPGA Tool Setup'},
                {'title': 'Step 9', 'desc': 'RTL Design Best Practices'},
                {'title': 'Step 10', 'desc': 'ASIC Design and Verification'}
            ]
        }
    # Solidity Example
    if "solidity" in topic_lower:
        return {
            'title': '🪙 Solidity Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Ethereum and Blockchain Basics'},
                {'title': 'Step 2', 'desc': 'Solidity Syntax and Data Types'},
                {'title': 'Step 3', 'desc': 'Smart Contract Functions'},
                {'title': 'Step 4', 'desc': 'Modifiers and Events'},
                {'title': 'Step 5', 'desc': 'Storage, Memory, and Gas'},
                {'title': 'Step 6', 'desc': 'Deploy with Remix and Truffle'},
                {'title': 'Step 7', 'desc': 'Interacting via Web3.js/Ethers.js'},
                {'title': 'Step 8', 'desc': 'Smart Contract Security'},
                {'title': 'Step 9', 'desc': 'Testing with Hardhat'},
                {'title': 'Step 10', 'desc': 'Deploy DApps to Ethereum Networks'}
            ]
        }
    # Move Example
    if "move" in topic_lower:
        return {
            'title': '🚚 Move Language Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Aptos/Sui Blockchain'},
                {'title': 'Step 2', 'desc': 'Move Syntax and Modules'},
                {'title': 'Step 3', 'desc': "Resources and Move's Ownership Model"},
                {'title': 'Step 4', 'desc': 'Functions and Structs'},
                {'title': 'Step 5', 'desc': 'Move Packages and Testing'},
                {'title': 'Step 6', 'desc': 'Publish and Upgrade Modules'},
                {'title': 'Step 7', 'desc': 'Interacting with CLI and SDKs'},
                {'title': 'Step 8', 'desc': 'Security and Audit Tools'},
                {'title': 'Step 9', 'desc': 'Build DApps with Move'},
                {'title': 'Step 10', 'desc': 'Contribute to Aptos/Sui Ecosystem'}
            ]
        }
    # Clarity Example
    if "clarity" in topic_lower:
        return {
            'title': '🔐 Clarity Language Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Stacks Blockchain'},
                {'title': 'Step 2', 'desc': 'Clarity Syntax and Types'},
                {'title': 'Step 3', 'desc': 'Smart Contracts and Functions'},
                {'title': 'Step 4', 'desc': 'Maps, Lists, and Data Structures'},
                {'title': 'Step 5', 'desc': 'Assertions and Conditions'},
                {'title': 'Step 6', 'desc': 'Blockchain Calls and Events'},
                {'title': 'Step 7', 'desc': 'Testing with Clarinet'},
                {'title': 'Step 8', 'desc': 'Integrate with Stacks.js'},
                {'title': 'Step 9', 'desc': 'Deploy on Stacks Testnet/Mainnet'},
                {'title': 'Step 10', 'desc': 'Security Auditing and Upgrades'}
            ]
        }
    # OCaml Example
    if "ocaml" in topic_lower:
        return {
            'title': '🧠 OCaml Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'OCaml Syntax and Functional Concepts'},
                {'title': 'Step 2', 'desc': 'Pattern Matching and Recursion'},
                {'title': 'Step 3', 'desc': 'Lists, Arrays, and Tuples'},
                {'title': 'Step 4', 'desc': 'Modules and Functors'},
                {'title': 'Step 5', 'desc': 'OOP Features in OCaml'},
                {'title': 'Step 6', 'desc': 'Polymorphism and Type Inference'},
                {'title': 'Step 7', 'desc': 'OCaml Toolchain and Dune'},
                {'title': 'Step 8', 'desc': 'Parsing and Lexing with Menhir'},
                {'title': 'Step 9', 'desc': 'Web or Native Apps with OCaml'},
                {'title': 'Step 10', 'desc': 'Testing, Debugging, and Profiling'}
            ]
        }
    # Nim Example
    if "nim" in topic_lower:
        return {
            'title': '🧬 Nim Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Nim Syntax and Compilation Basics'},
                {'title': 'Step 2', 'desc': 'Types, Variables, and Procedures'},
                {'title': 'Step 3', 'desc': 'Control Flow and Error Handling'},
                {'title': 'Step 4', 'desc': 'OOP and Macros'},
                {'title': 'Step 5', 'desc': 'Modules and Packages'},
                {'title': 'Step 6', 'desc': 'Asynchronous Programming'},
                {'title': 'Step 7', 'desc': 'FFI and C Interop'},
                {'title': 'Step 8', 'desc': 'Web Development (Jester/NimHTTP)'},
                {'title': 'Step 9', 'desc': 'GUI and Cross-Platform Apps'},
                {'title': 'Step 10', 'desc': 'Optimize and Deploy Nim Projects'}
            ]
        }
    # Crystal Example
    if "crystal" in topic_lower:
        return {
            'title': '💎 Crystal Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Crystal Syntax and Static Typing'},
                {'title': 'Step 2', 'desc': 'Variables, Methods, and Control Flow'},
                {'title': 'Step 3', 'desc': 'Classes, Structs, and Modules'},
                {'title': 'Step 4', 'desc': 'Macros and Meta Programming'},
                {'title': 'Step 5', 'desc': 'Collections and Iterators'},
                {'title': 'Step 6', 'desc': 'Concurrency with Fibers'},
                {'title': 'Step 7', 'desc': 'Shards (Package Manager)'},
                {'title': 'Step 8', 'desc': 'Web Development with Amber'},
                {'title': 'Step 9', 'desc': 'Testing and Benchmarking'},
                {'title': 'Step 10', 'desc': 'Compile and Distribute Apps'}
            ]
        }
    # Zig Example
    if "zig" in topic_lower:
        return {
            'title': '⚡ Zig Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Zig Language Basics and Philosophy'},
                {'title': 'Step 2', 'desc': 'Variables, Pointers, and Control Flow'},
                {'title': 'Step 3', 'desc': 'Functions and Error Handling'},
                {'title': 'Step 4', 'desc': 'Memory Management and Safety'},
                {'title': 'Step 5', 'desc': 'Compile-time Execution and Generics'},
                {'title': 'Step 6', 'desc': 'Interop with C'},
                {'title': 'Step 7', 'desc': 'Build System and Projects'},
                {'title': 'Step 8', 'desc': 'Systems Programming'},
                {'title': 'Step 9', 'desc': 'Cross Compilation'},
                {'title': 'Step 10', 'desc': 'Contribute to Zig Ecosystem'}
            ]
        }
    # Tcl Example
    if "tcl" in topic_lower:
        return {
            'title': '🌀 Tcl Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Tcl Syntax and Interpreter'},
                {'title': 'Step 2', 'desc': 'Variables, Lists, and Arrays'},
                {'title': 'Step 3', 'desc': 'Procedures and Flow Control'},
                {'title': 'Step 4', 'desc': 'File I/O and Error Handling'},
                {'title': 'Step 5', 'desc': 'Regular Expressions and String Ops'},
                {'title': 'Step 6', 'desc': 'GUI with Tk Toolkit'},
                {'title': 'Step 7', 'desc': 'Embedding and Extending Tcl'},
                {'title': 'Step 8', 'desc': 'Event-Driven Programming'},
                {'title': 'Step 9', 'desc': 'Debugging and Tools'},
                {'title': 'Step 10', 'desc': 'Use in EDA and Legacy Apps'}
            ]
        }
    # AWK Example
    if "awk" in topic_lower:
        return {
            'title': '🗂 AWK Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn Basic AWK Syntax and Field Separators'},
                {'title': 'Step 2', 'desc': 'Patterns and Actions'},
                {'title': 'Step 3', 'desc': 'Built-in Variables (FS, OFS, NR, NF)'},
                {'title': 'Step 4', 'desc': 'String and Math Functions'},
                {'title': 'Step 5', 'desc': 'Control Flow – if, loops'},
                {'title': 'Step 6', 'desc': 'User-defined Functions'},
                {'title': 'Step 7', 'desc': 'Working with Files and Input Redirection'},
                {'title': 'Step 8', 'desc': 'Advanced Text Processing'},
                {'title': 'Step 9', 'desc': 'Reporting and Formatting Output'},
                {'title': 'Step 10', 'desc': 'Integration in Shell Scripts/Makefiles'}
            ]
        }
    # Sed Example
    if "sed" in topic_lower:
        return {
            'title': '✂️ Sed Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Basic sed Syntax and Command Structure'},
                {'title': 'Step 2', 'desc': 'Line Addressing and Patterns'},
                {'title': 'Step 3', 'desc': 'Substitution with s///'},
                {'title': 'Step 4', 'desc': 'Deletion, Insertion, and Transformation'},
                {'title': 'Step 5', 'desc': 'Flags and Regular Expressions'},
                {'title': 'Step 6', 'desc': 'Hold Space Techniques'},
                {'title': 'Step 7', 'desc': 'Advanced Script Files'},
                {'title': 'Step 8', 'desc': 'In-place Editing'},
                {'title': 'Step 9', 'desc': 'Combining sed with Shell Pipelines'},
                {'title': 'Step 10', 'desc': 'Performance Optimization for Large Files'}
            ]
        }
    # Makefile Example
    if "make" in topic_lower or "makefile" in topic_lower:
        return {
            'title': '🛠 Makefile Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand make and Makefile Basics'},
                {'title': 'Step 2', 'desc': 'Targets, Prerequisites, and Recipes'},
                {'title': 'Step 3', 'desc': 'Variables and Macros'},
                {'title': 'Step 4', 'desc': 'Implicit Rules and Pattern Matching'},
                {'title': 'Step 5', 'desc': 'Phony Targets and Clean Rules'},
                {'title': 'Step 6', 'desc': 'Conditional Execution and Functions'},
                {'title': 'Step 7', 'desc': 'Including Other Makefiles'},
                {'title': 'Step 8', 'desc': 'Dependency Tracking'},
                {'title': 'Step 9', 'desc': 'Parallel Builds with -j'},
                {'title': 'Step 10', 'desc': 'Debugging Makefiles and Best Practices'}
            ]
        }
    # ReScript Example
    if "rescript" in topic_lower:
        return {
            'title': '🔵 ReScript Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Install ReScript and Setup Tooling'},
                {'title': 'Step 2', 'desc': 'ReScript Syntax and Types'},
                {'title': 'Step 3', 'desc': 'Functions and Pattern Matching'},
                {'title': 'Step 4', 'desc': 'Modules and Records'},
                {'title': 'Step 5', 'desc': 'Interop with JavaScript'},
                {'title': 'Step 6', 'desc': 'Variants and Enums'},
                {'title': 'Step 7', 'desc': 'Build & Config with bsconfig.json'},
                {'title': 'Step 8', 'desc': 'Error Handling and Effects'},
                {'title': 'Step 9', 'desc': 'React Binding'},
                {'title': 'Step 10', 'desc': 'Project Setup and Deployment'}
            ]
        }
    # PureScript Example
    if "purescript" in topic_lower:
        return {
            'title': '🌿 PureScript Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Setup PureScript Toolchain (psc-package/spago)'},
                {'title': 'Step 2', 'desc': 'Language Syntax and Types'},
                {'title': 'Step 3', 'desc': 'Functions and Immutability'},
                {'title': 'Step 4', 'desc': 'Algebraic Data Types and Type Classes'},
                {'title': 'Step 5', 'desc': 'Effect System and Monads'},
                {'title': 'Step 6', 'desc': 'Arrays and Records'},
                {'title': 'Step 7', 'desc': 'FFI with JavaScript'},
                {'title': 'Step 8', 'desc': 'Project Build & Bundling'},
                {'title': 'Step 9', 'desc': 'React/DOM Integration with Halogen'},
                {'title': 'Step 10', 'desc': 'Testing and Best Practices'}
            ]
        }
    # CoffeeScript Example
    if "coffeescript" in topic_lower:
        return {
            'title': '☕ CoffeeScript Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn CoffeeScript Syntax and Indentation'},
                {'title': 'Step 2', 'desc': 'Variables and Functions'},
                {'title': 'Step 3', 'desc': 'Arrays, Objects, and Destructuring'},
                {'title': 'Step 4', 'desc': 'Comprehensions'},
                {'title': 'Step 5', 'desc': 'Classes and Inheritance'},
                {'title': 'Step 6', 'desc': 'Splat Operator and String Interpolation'},
                {'title': 'Step 7', 'desc': 'Interop with JavaScript'},
                {'title': 'Step 8', 'desc': 'Build Tools and Compilation'},
                {'title': 'Step 9', 'desc': 'Source Maps and Debugging'},
                {'title': 'Step 10', 'desc': 'Integrate into Web Projects'}
            ]
        }
    # LiveScript Example
    if "livescript" in topic_lower:
        return {
            'title': '🎵 LiveScript Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'LiveScript Syntax and Repl'},
                {'title': 'Step 2', 'desc': 'Function and Arrow Syntax'},
                {'title': 'Step 3', 'desc': 'Pattern Matching'},
                {'title': 'Step 4', 'desc': 'Strings, Regex, and Interpolation'},
                {'title': 'Step 5', 'desc': 'Arrays, Objects, and List Comprehensions'},
                {'title': 'Step 6', 'desc': 'Classes and Inheritance'},
                {'title': 'Step 7', 'desc': 'JS Interop and Modules'},
                {'title': 'Step 8', 'desc': 'Build Setup with LSC'},
                {'title': 'Step 9', 'desc': 'CLI Tools and Scripts'},
                {'title': 'Step 10', 'desc': 'Web Development Integration'}
            ]
        }
    # ActionScript Example
    if "actionscript" in topic_lower:
        return {
            'title': '🕹 ActionScript Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'ActionScript Version 3 Basics'},
                {'title': 'Step 2', 'desc': 'Variables, Functions, and Classes'},
                {'title': 'Step 3', 'desc': 'Display List API and Events'},
                {'title': 'Step 4', 'desc': 'MovieClips and Graphics'},
                {'title': 'Step 5', 'desc': 'OOP Principles and Packages'},
                {'title': 'Step 6', 'desc': 'Flash Player and AIR Integration'},
                {'title': 'Step 7', 'desc': 'Animations and Timelines'},
                {'title': 'Step 8', 'desc': 'Network & File I/O'},
                {'title': 'Step 9', 'desc': 'Debugging in Flash Builder'},
                {'title': 'Step 10', 'desc': 'Deployment to Web/Desktop/Mobile via AIR'}
            ]
        }
    # Q# Example
    if "q#" in topic_lower:
        return {
            'title': '🔶 Q# Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Quantum Computing Basics'},
                {'title': 'Step 2', 'desc': 'Install QDK and Workspace Setup'},
                {'title': 'Step 3', 'desc': 'Q# Syntax – Qubits, Operations'},
                {'title': 'Step 4', 'desc': 'Creating and Using Qubits'},
                {'title': 'Step 5', 'desc': 'Control Flow and Measurement'},
                {'title': 'Step 6', 'desc': 'Built-in Operations and Libraries'},
                {'title': 'Step 7', 'desc': 'Write and Run Quantum Algorithms'},
                {'title': 'Step 8', 'desc': 'Classical–Quantum Interop with Python/ .NET'},
                {'title': 'Step 9', 'desc': 'Testing and Simulation'},
                {'title': 'Step 10', 'desc': 'Work with Azure Quantum / Quantum Hardware'}
            ]
        }
    # Shader Language Example
    if "glsl" in topic_lower or "hlsl" in topic_lower or "metal" in topic_lower:
        return {
            'title': '🎨 Shader Language Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand GPU Pipelines and Shader Stages'},
                {'title': 'Step 2', 'desc': 'GLSL/HLSL/Metal Syntax Basics'},
                {'title': 'Step 3', 'desc': 'Vectors, Matrices, and Uniforms'},
                {'title': 'Step 4', 'desc': 'Writing Vertex Shaders'},
                {'title': 'Step 5', 'desc': 'Writing Fragment (Pixel) Shaders'},
                {'title': 'Step 6', 'desc': 'Lighting, Texturing, and Samplers'},
                {'title': 'Step 7', 'desc': 'Shader Compilation and Debugging'},
                {'title': 'Step 8', 'desc': 'Advanced Effects (Shadows, Post-Processing)'},
                {'title': 'Step 9', 'desc': 'Optimization and precision'},
                {'title': 'Step 10', 'desc': 'Integration with Engines (Unity/MetalKit)'}
            ]
        }
    # Racket Example
    if "racket" in topic_lower:
        return {
            'title': '🍵 Racket Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn Racket Syntax and DrRacket IDE'},
                {'title': 'Step 2', 'desc': 'Scheme-like Functions and Recursion'},
                {'title': 'Step 3', 'desc': 'Lists, Pairs, and Data Types'},
                {'title': 'Step 4', 'desc': 'Macros and Language Extensions'},
                {'title': 'Step 5', 'desc': 'Modules and Structs'},
                {'title': 'Step 6', 'desc': 'Contracts and Testing'},
                {'title': 'Step 7', 'desc': "GUI with Racket's GUI Lib"},
                {'title': 'Step 8', 'desc': 'Web Apps with Racket/Continuations'},
                {'title': 'Step 9', 'desc': 'DSL Design in Racket'},
                {'title': 'Step 10', 'desc': 'Deploy Racket Applications'}
            ]
        }
    # Scheme Example
    if "scheme" in topic_lower:
        return {
            'title': '🔗 Scheme Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Scheme Syntax and REPL'},
                {'title': 'Step 2', 'desc': 'S-Expressions and Lists'},
                {'title': 'Step 3', 'desc': 'Recursion and Higher-Order Functions'},
                {'title': 'Step 4', 'desc': 'Lambda and Closures'},
                {'title': 'Step 5', 'desc': 'Macros and hygienic macros'},
                {'title': 'Step 6', 'desc': 'Continuations (call/cc)'},
                {'title': 'Step 7', 'desc': 'Modules and Libraries'},
                {'title': 'Step 8', 'desc': 'Functional Patterns'},
                {'title': 'Step 9', 'desc': 'Implementing Interpreters/DSLs'},
                {'title': 'Step 10', 'desc': 'Scheme Projects and Deployment'}
            ]
        }
    # Common Lisp Example
    if "common lisp" in topic_lower:
        return {
            'title': '📜 Common Lisp Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn Lisp Syntax and S-Expressions'},
                {'title': 'Step 2', 'desc': 'Symbols, Lists, and Functions'},
                {'title': 'Step 3', 'desc': 'Macros and Code-as-Data'},
                {'title': 'Step 4', 'desc': 'Condition System and Error Handling'},
                {'title': 'Step 5', 'desc': 'CLOS (OOP in Lisp)'},
                {'title': 'Step 6', 'desc': 'Package System and Modules'},
                {'title': 'Step 7', 'desc': 'Stream I/O and Files'},
                {'title': 'Step 8', 'desc': 'Using SLIME/Emacs for Development'},
                {'title': 'Step 9', 'desc': 'Build Tools and ASDF'},
                {'title': 'Step 10', 'desc': 'Deploying CLI and Web Apps'}
            ]
        }
    # Prolog Example
    if "prolog" in topic_lower:
        return {
            'title': '🔍 Prolog Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Logic Programming Concepts'},
                {'title': 'Step 2', 'desc': 'Syntax, Facts, and Rules'},
                {'title': 'Step 3', 'desc': 'Queries and Backtracking'},
                {'title': 'Step 4', 'desc': 'Lists and Recursion'},
                {'title': 'Step 5', 'desc': 'Unification and Pattern Matching'},
                {'title': 'Step 6', 'desc': 'Cut, Fail, and Control Constructs'},
                {'title': 'Step 7', 'desc': 'Definite Clause Grammars (DCG)'},
                {'title': 'Step 8', 'desc': 'Modules and Libraries'},
                {'title': 'Step 9', 'desc': 'Constraint Logic Programming'},
                {'title': 'Step 10', 'desc': 'AI Projects and Integration'}
            ]
        }
    # Mercury Example
    if "mercury" in topic_lower:
        return {
            'title': '☀️ Mercury Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Logic/Functional Hybrid Concepts'},
                {'title': 'Step 2', 'desc': 'Syntax, Modes, and Determinism'},
                {'title': 'Step 3', 'desc': 'Types and Module System'},
                {'title': 'Step 4', 'desc': 'Predicates and Goal Declarations'},
                {'title': 'Step 5', 'desc': 'List/Tree Processing'},
                {'title': 'Step 6', 'desc': 'Modes & IO'},
                {'title': 'Step 7', 'desc': 'DCGs and Parsing'},
                {'title': 'Step 8', 'desc': 'Foreign Language Interface'},
                {'title': 'Step 9', 'desc': 'Static Analysis & Debugging'},
                {'title': 'Step 10', 'desc': 'Concurrent & Deterministic Programming'}
            ]
        }
    # Smalltalk Example
    if "smalltalk" in topic_lower:
        return {
            'title': '🐦 Smalltalk Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Image-Based Development'},
                {'title': 'Step 2', 'desc': 'Smalltalk Syntax and Messages'},
                {'title': 'Step 3', 'desc': 'Classes, Objects, and Inheritance'},
                {'title': 'Step 4', 'desc': 'Workspace, Transcript, and Explorers'},
                {'title': 'Step 5', 'desc': 'Collections and Iteration'},
                {'title': 'Step 6', 'desc': 'Morph and GUI Development'},
                {'title': 'Step 7', 'desc': 'Debugging in the IDE'},
                {'title': 'Step 8', 'desc': 'Unit Testing with SUnit'},
                {'title': 'Step 9', 'desc': 'Open-source via Monticello/Metacello'},
                {'title': 'Step 10', 'desc': 'Web or Desktop App with Pharo or Seaside'}
            ]
        }
    # Vala Example
    if "vala" in topic_lower:
        return {
            'title': '🔷 Vala Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Vala Syntax and GNOME Integration'},
                {'title': 'Step 2', 'desc': 'Classes, Interfaces, and Properties'},
                {'title': 'Step 3', 'desc': 'Memory Management and GObjects'},
                {'title': 'Step 4', 'desc': 'Signals and Events'},
                {'title': 'Step 5', 'desc': 'GLib and GIO Usage'},
                {'title': 'Step 6', 'desc': 'Building with Meson/Autotools'},
                {'title': 'Step 7', 'desc': 'Developing GUI Apps for Linux'},
                {'title': 'Step 8', 'desc': 'Bindings and C Interop'},
                {'title': 'Step 9', 'desc': 'Debugging and Packaging'},
                {'title': 'Step 10', 'desc': 'Deployment and Distribution'}
            ]
        }
    # Pony Example
    if "pony" in topic_lower:
        return {
            'title': '🦄 Pony Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Pony Syntax and Actor Model Overview'},
                {'title': 'Step 2', 'desc': 'Actors, Message Passing, and Concurrency'},
                {'title': 'Step 3', 'desc': 'Types, Options, and Reference Capabilities'},
                {'title': 'Step 4', 'desc': 'Classes, Primitives, and Traits'},
                {'title': 'Step 5', 'desc': 'Error Handling and Recovery'},
                {'title': 'Step 6', 'desc': 'Collections and Data Structures'},
                {'title': 'Step 7', 'desc': 'Makefiles and Build System'},
                {'title': 'Step 8', 'desc': 'Interop with C Library'},
                {'title': 'Step 9', 'desc': 'Testing and Static Analysis'},
                {'title': 'Step 10', 'desc': 'Build Concurrent Applications'}
            ]
        }
    # Ballerina Example
    if "ballerina" in topic_lower:
        return {
            'title': '🎯 Ballerina Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Install Ballerina and Setup Workspace'},
                {'title': 'Step 2', 'desc': 'Syntax, Variables, and Data Types'},
                {'title': 'Step 3', 'desc': 'Functions, Connectors, and Modules'},
                {'title': 'Step 4', 'desc': 'REST and gRPC Service Creation'},
                {'title': 'Step 5', 'desc': 'Error Handling and Types'},
                {'title': 'Step 6', 'desc': 'Data Streaming and Transactions'},
                {'title': 'Step 7', 'desc': 'Testing and Observability'},
                {'title': 'Step 8', 'desc': 'Deployment with Ballerina Cloud/Service Mesh'},
                {'title': 'Step 9', 'desc': 'Security, OAuth, and JWT'},
                {'title': 'Step 10', 'desc': 'Microservices and Integration Patterns'}
            ]
        }
    # Red Example
    if "red" in topic_lower:
        return {
            'title': '🔴 Red Language Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn Red Syntax and Rebol Heritage'},
                {'title': 'Step 2', 'desc': 'Values, Blocks, and Series'},
                {'title': 'Step 3', 'desc': 'Functions and Input Handling'},
                {'title': 'Step 4', 'desc': 'GUI with Red/View'},
                {'title': 'Step 5', 'desc': 'Types and Structs'},
                {'title': 'Step 6', 'desc': 'Red/System for Low‑Level Coding'},
                {'title': 'Step 7', 'desc': 'Cross‑Platform Compilation'},
                {'title': 'Step 8', 'desc': 'Networking and File I/O'},
                {'title': 'Step 9', 'desc': 'GUI & CLI App Projects'},
                {'title': 'Step 10', 'desc': 'Deploy and Package Red Apps'}
            ]
        }
    # Hack Example
    if "hack" in topic_lower:
        return {
            'title': '⚙️ Hack Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand HHVM and Hack ecosystem'},
                {'title': 'Step 2', 'desc': 'Hack syntax – types, functions'},
                {'title': 'Step 3', 'desc': 'Type annotations and typechecker'},
                {'title': 'Step 4', 'desc': 'Collections – Vectors, Maps, Sets'},
                {'title': 'Step 5', 'desc': 'Asynchronous constructs (await)'},
                {'title': 'Step 6', 'desc': 'Traits, Namespaces, and Generics'},
                {'title': 'Step 7', 'desc': 'Type-safe APIs and code style'},
                {'title': 'Step 8', 'desc': 'Writing tests with Hack Test Framework'},
                {'title': 'Step 9', 'desc': 'Interoperability with PHP'},
                {'title': 'Step 10', 'desc': 'HHVM deployment best practices'}
            ]
        }
    # Apex Example
    if "apex" in topic_lower:
        return {
            'title': '💼 Apex (Salesforce) Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn Salesforce data model and architecture'},
                {'title': 'Step 2', 'desc': 'Apex syntax – classes, triggers'},
                {'title': 'Step 3', 'desc': 'SObjects and SOQL queries'},
                {'title': 'Step 4', 'desc': 'Triggers, batch Apex, and schedulers'},
                {'title': 'Step 5', 'desc': 'Controller logic in Visualforce/LWC'},
                {'title': 'Step 6', 'desc': 'Error handling and governor limits'},
                {'title': 'Step 7', 'desc': 'Testing – unit tests and mocks'},
                {'title': 'Step 8', 'desc': 'Deployment with metadata API/CI'},
                {'title': 'Step 9', 'desc': 'Integration using REST and SOAP'},
                {'title': 'Step 10', 'desc': 'Optimizing performance & best practices'}
            ]
        }
    # ABAP Example
    if "abap" in topic_lower:
        return {
            'title': '🧩 ABAP Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand SAP system landscape'},
                {'title': 'Step 2', 'desc': 'ABAP syntax, data dictionary, variables'},
                {'title': 'Step 3', 'desc': 'Reports and Module Pool Programming'},
                {'title': 'Step 4', 'desc': 'Internal tables and field symbols'},
                {'title': 'Step 5', 'desc': 'Forms and SmartForms'},
                {'title': 'Step 6', 'desc': 'User-exits, BADI, and enhancements'},
                {'title': 'Step 7', 'desc': 'ALV, OData services, and RFC'},
                {'title': 'Step 8', 'desc': 'Performance tuning and buffering'},
                {'title': 'Step 9', 'desc': 'Unit tests and Code Inspector'},
                {'title': 'Step 10', 'desc': 'Transport and Deployment in SAP'}
            ]
        }
    # LabVIEW Example
    if "labview" in topic_lower:
        return {
            'title': '🔬 LabVIEW Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Familiarize with G graphical data flow paradigm'},
                {'title': 'Step 2', 'desc': 'Create basic VI with controls and indicators'},
                {'title': 'Step 3', 'desc': 'Structures: loops and case'},
                {'title': 'Step 4', 'desc': 'Dataflow and variable wiring'},
                {'title': 'Step 5', 'desc': 'DAQmx hardware integration'},
                {'title': 'Step 6', 'desc': 'Error clusters and handling'},
                {'title': 'Step 7', 'desc': 'State machines with VI scripting'},
                {'title': 'Step 8', 'desc': 'Testing and debugging VIs'},
                {'title': 'Step 9', 'desc': 'Package and build executables'},
                {'title': 'Step 10', 'desc': 'Advanced topics: RT, FPGA, NI integration'}
            ]
        }
    # Scratch Example
    if "scratch" in topic_lower:
        return {
            'title': '🌈 Scratch Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Scratch blocks and sprites'},
                {'title': 'Step 2', 'desc': 'Motion, looks, and event blocks'},
                {'title': 'Step 3', 'desc': 'Control structures and loops'},
                {'title': 'Step 4', 'desc': 'Broadcast messages for interaction'},
                {'title': 'Step 5', 'desc': 'Variables and simple data'},
                {'title': 'Step 6', 'desc': 'Sound effects and basic animation'},
                {'title': 'Step 7', 'desc': 'Pen, sensing, and operators'},
                {'title': 'Step 8', 'desc': 'Simple game logic'},
                {'title': 'Step 9', 'desc': 'User interface and feedback'},
                {'title': 'Step 10', 'desc': "Share projects and remix others' work"}
            ]
        }
    # Blockly Example
    if "blockly" in topic_lower:
        return {
            'title': '🔲 Blockly Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Embed Blockly in a web page'},
                {'title': 'Step 2', 'desc': 'Define custom blocks and fields'},
                {'title': 'Step 3', 'desc': 'Wire blocks to generate code'},
                {'title': 'Step 4', 'desc': 'Integrate event handlers'},
                {'title': 'Step 5', 'desc': 'Code generation in JS/Python'},
                {'title': 'Step 6', 'desc': 'Toolbox and UI customization'},
                {'title': 'Step 7', 'desc': 'Translate blocks to multiple languages'},
                {'title': 'Step 8', 'desc': 'Write user interaction logic'},
                {'title': 'Step 9', 'desc': 'Save/load workspace state'},
                {'title': 'Step 10', 'desc': 'Deploy block-based learning apps'}
            ]
        }
    # WebAssembly Example
    if "webassembly" in topic_lower or "wat" in topic_lower:
        return {
            'title': '🚀 WebAssembly Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn WebAssembly basics and WAT syntax'},
                {'title': 'Step 2', 'desc': 'Types, functions, and memory'},
                {'title': 'Step 3', 'desc': 'Compile C/Rust to WASM'},
                {'title': 'Step 4', 'desc': 'Import/Export functions'},
                {'title': 'Step 5', 'desc': 'Linear memory and tables'},
                {'title': 'Step 6', 'desc': 'JS–WASM integration'},
                {'title': 'Step 7', 'desc': 'Async and multi‑threading proposals'},
                {'title': 'Step 8', 'desc': 'Debugging and tooling'},
                {'title': 'Step 9', 'desc': 'Security and sandboxing'},
                {'title': 'Step 10', 'desc': 'Building real-world WASM apps'}
            ]
        }
    # ColdFusion Example
    if "coldfusion" in topic_lower or "cfml" in topic_lower:
        return {
            'title': '❄️ ColdFusion (CFML) Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'CFML syntax and tags'},
                {'title': 'Step 2', 'desc': 'Variables, data types, scopes'},
                {'title': 'Step 3', 'desc': 'CFQUERY and database integration'},
                {'title': 'Step 4', 'desc': 'CFSCRIPT and control structures'},
                {'title': 'Step 5', 'desc': 'Custom tags and user-defined functions'},
                {'title': 'Step 6', 'desc': 'CF Components (CFCs)'},
                {'title': 'Step 7', 'desc': 'Sessions, application scope, and caching'},
                {'title': 'Step 8', 'desc': 'REST and SOAP web services'},
                {'title': 'Step 9', 'desc': 'Security best practices'},
                {'title': 'Step 10', 'desc': 'Building and deploying CFML apps'}
            ]
        }
    # REXX Example
    if "rexx" in topic_lower:
        return {
            'title': '🧵 REXX Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'REXX syntax and data types'},
                {'title': 'Step 2', 'desc': 'Control flow and loops'},
                {'title': 'Step 3', 'desc': 'Subroutines and functions'},
                {'title': 'Step 4', 'desc': 'String and file operations'},
                {'title': 'Step 5', 'desc': 'Interactive I/O and dialogs'},
                {'title': 'Step 6', 'desc': 'Error handling and diagnostics'},
                {'title': 'Step 7', 'desc': 'REXX in mainframes and OS scripts'},
                {'title': 'Step 8', 'desc': 'External function interface (XFI)'},
                {'title': 'Step 9', 'desc': 'GUI scripting (Regina REXX)'},
                {'title': 'Step 10', 'desc': 'Writing maintainable REXX scripts'}
            ]
        }
    # Pike Example
    if "pike" in topic_lower:
        return {
            'title': '🛡 Pike Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Pike syntax, types, and functions'},
                {'title': 'Step 2', 'desc': 'Objects and inheritance'},
                {'title': 'Step 3', 'desc': 'Arrays, mappings, and streams'},
                {'title': 'Step 4', 'desc': 'Error handling and regular expressions'},
                {'title': 'Step 5', 'desc': 'Modules and packages'},
                {'title': 'Step 6', 'desc': 'Embedding Pike in apps'},
                {'title': 'Step 7', 'desc': 'Networking and sockets'},
                {'title': 'Step 8', 'desc': 'Database connectivity'},
                {'title': 'Step 9', 'desc': 'Testing with PikeUnit'},
                {'title': 'Step 10', 'desc': 'Building network/server applications'}
            ]
        }
    # Eiffel Example
    if "eiffel" in topic_lower:
        return {
            'title': '🏛 Eiffel Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Eiffel syntax and Design by Contract'},
                {'title': 'Step 2', 'desc': 'Classes, inheritance, features'},
                {'title': 'Step 3', 'desc': 'Assertions and contracts'},
                {'title': 'Step 4', 'desc': 'Generics and multiple inheritance'},
                {'title': 'Step 5', 'desc': 'EiffelStudio and compilation'},
                {'title': 'Step 6', 'desc': 'Agents and event handling'},
                {'title': 'Step 7', 'desc': 'Collections and iteration'},
                {'title': 'Step 8', 'desc': 'Concurrency with SCOOP'},
                {'title': 'Step 9', 'desc': 'Design patterns with contracts'},
                {'title': 'Step 10', 'desc': 'Compile and deploy Eiffel libraries'}
            ]
        }
    # Inform Example
    if "inform" in topic_lower:
        return {
            'title': '📘 Inform Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand interactive fiction concepts'},
                {'title': 'Step 2', 'desc': 'Inform syntax and world model'},
                {'title': 'Step 3', 'desc': 'Objects, properties, and rules'},
                {'title': 'Step 4', 'desc': 'Actions and player commands'},
                {'title': 'Step 5', 'desc': 'Text generation templates'},
                {'title': 'Step 6', 'desc': 'Scenes and story flow control'},
                {'title': 'Step 7', 'desc': 'Testing and playthrough debug'},
                {'title': 'Step 8', 'desc': 'Writing expressive narrative'},
                {'title': 'Step 9', 'desc': 'Compiling to Z-code or Glulx'},
                {'title': 'Step 10', 'desc': 'Publishing interactive fiction games'}
            ]
        }
    # Nimrod Example
    if "nimrod" in topic_lower:
        return {
            'title': '🧩 Nimrod (old Nim) Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Legacy Nimrod syntax and toolchain'},
                {'title': 'Step 2', 'desc': 'Data types and modules'},
                {'title': 'Step 3', 'desc': 'Procedures and control flow'},
                {'title': 'Step 4', 'desc': 'Memory and pointer management'},
                {'title': 'Step 5', 'desc': 'Compiling standalone executables'},
                {'title': 'Step 6', 'desc': 'Interop with C'},
                {'title': 'Step 7', 'desc': 'Templates and generics'},
                {'title': 'Step 8', 'desc': 'Building GUI with legacy libs'},
                {'title': 'Step 9', 'desc': 'Testing and debugging old Nimrod'},
                {'title': 'Step 10', 'desc': 'Porting code to modern Nim'}
            ]
        }
    # Xojo Example
    if "xojo" in topic_lower:
        return {
            'title': '💻 Xojo Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn Xojo IDE and RAD environment'},
                {'title': 'Step 2', 'desc': 'Syntax, controls, and events'},
                {'title': 'Step 3', 'desc': 'Forms and UI design'},
                {'title': 'Step 4', 'desc': 'Classes and inheritance'},
                {'title': 'Step 5', 'desc': 'Database connections and SQL'},
                {'title': 'Step 6', 'desc': 'Web vs Desktop project scopes'},
                {'title': 'Step 7', 'desc': 'Error handling and debugger'},
                {'title': 'Step 8', 'desc': 'File I/O and filesystem access'},
                {'title': 'Step 9', 'desc': 'Build & deployment (mac, win, web, raspberry)'},
                {'title': 'Step 10', 'desc': 'Packaging & updates'}
            ]
        }
    # Dlang Example
    if "dlang" in topic_lower or "d " in topic_lower:
        return {
            'title': '🔷 D (Dlang) Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn D syntax and module system'},
                {'title': 'Step 2', 'desc': 'Data types and arrays'},
                {'title': 'Step 3', 'desc': 'Functions, templates, and UFCS'},
                {'title': 'Step 4', 'desc': 'Compile-time code (CTFE)'},
                {'title': 'Step 5', 'desc': 'Memory safety and GC'},
                {'title': 'Step 6', 'desc': 'Object-oriented D'},
                {'title': 'Step 7', 'desc': 'Concurrency and fibers'},
                {'title': 'Step 8', 'desc': 'C interop and extern(C)'},
                {'title': 'Step 9', 'desc': 'Unit testing and benchmarking'},
                {'title': 'Step 10', 'desc': 'Build & cross-platform deployment'}
            ]
        }
    # Genie Example
    if "genie" in topic_lower:
        return {
            'title': '🔧 Genie (Vala dialect) Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Genie syntax (Python-like Vala)'},
                {'title': 'Step 2', 'desc': 'Types, functions, and loops'},
                {'title': 'Step 3', 'desc': 'Classes and GObject binding'},
                {'title': 'Step 4', 'desc': 'Signals, properties, and events'},
                {'title': 'Step 5', 'desc': 'Genie in GNOME ecosystem'},
                {'title': 'Step 6', 'desc': 'Building with vala-compiler'},
                {'title': 'Step 7', 'desc': 'GUI development with GTK'},
                {'title': 'Step 8', 'desc': 'Interop with C libraries'},
                {'title': 'Step 9', 'desc': 'Debugging and packaging'},
                {'title': 'Step 10', 'desc': 'Deploy GNOME desktop apps'}
            ]
        }
    # Io Example
    if "io" in topic_lower:
        return {
            'title': '🌐 Io Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn Io prototype-based syntax'},
                {'title': 'Step 2', 'desc': 'Objects as delegates'},
                {'title': 'Step 3', 'desc': 'Slots, messages, and contexts'},
                {'title': 'Step 4', 'desc': 'Tables and iteration'},
                {'title': 'Step 5', 'desc': 'Coroutines and concurrency'},
                {'title': 'Step 6', 'desc': 'String and regex features'},
                {'title': 'Step 7', 'desc': 'FFI and embedding Io'},
                {'title': 'Step 8', 'desc': 'Error handling and debugging'},
                {'title': 'Step 9', 'desc': 'Build CLI and network apps'},
                {'title': 'Step 10', 'desc': 'Community libs and tooling'}
            ]
        }
    # Agda Example
    if "agda" in topic_lower:
        return {
            'title': '🔖 Agda Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand dependently typed programming'},
                {'title': 'Step 2', 'desc': 'Agda syntax and basic types'},
                {'title': 'Step 3', 'desc': 'Inductive types and pattern matching'},
                {'title': 'Step 4', 'desc': 'Equality and proof constructs'},
                {'title': 'Step 5', 'desc': 'Modules and abstraction'},
                {'title': 'Step 6', 'desc': 'Interactive proofs in Emacs'},
                {'title': 'Step 7', 'desc': 'Totality and termination checking'},
                {'title': 'Step 8', 'desc': 'Libraries and tactics'},
                {'title': 'Step 9', 'desc': 'Formalizing mathematics'},
                {'title': 'Step 10', 'desc': 'Publishing proofs and verified code'}
            ]
        }
    # Idris Example
    if "idris" in topic_lower:
        return {
            'title': '🧠 Idris Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn dependently typed programming'},
                {'title': 'Step 2', 'desc': 'Idris syntax and total functions'},
                {'title': 'Step 3', 'desc': 'Types, type classes, and records'},
                {'title': 'Step 4', 'desc': 'Pattern matching and recursion'},
                {'title': 'Step 5', 'desc': 'Effects and I/O'},
                {'title': 'Step 6', 'desc': 'Proofs and interactive editing'},
                {'title': 'Step 7', 'desc': 'Dependent pattern matching'},
                {'title': 'Step 8', 'desc': 'Interop with C/JS'},
                {'title': 'Step 9', 'desc': 'Building CLI/GUI apps'},
                {'title': 'Step 10', 'desc': 'Release and documentation support'}
            ]
        }
    # Terra Example
    if "terra" in topic_lower:
        return {
            'title': '🛠 Terra Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Setup Terra (Lua-based DSL)'},
                {'title': 'Step 2', 'desc': 'Terra syntax and types'},
                {'title': 'Step 3', 'desc': 'Mixing Lua and Terra code'},
                {'title': 'Step 4', 'desc': 'Low-level memory and pointers'},
                {'title': 'Step 5', 'desc': 'Compile-time metaprogramming'},
                {'title': 'Step 6', 'desc': 'LLVM interop and codegen'},
                {'title': 'Step 7', 'desc': 'Building fast numerical kernels'},
                {'title': 'Step 8', 'desc': 'Testing and benchmarking'},
                {'title': 'Step 9', 'desc': 'Coupling with Lua-based apps'},
                {'title': 'Step 10', 'desc': 'Deploy high-performance libraries'}
            ]
        }
    # Chapel Example
    if "chapel" in topic_lower:
        return {
            'title': '🚀 Chapel Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn Chapel basics and parallel execution model'},
                {'title': 'Step 2', 'desc': 'Data types, domains, and ranges'},
                {'title': 'Step 3', 'desc': 'Variables, arrays, and records'},
                {'title': 'Step 4', 'desc': 'Control flow and iterators'},
                {'title': 'Step 5', 'desc': 'Locales and data distribution'},
                {'title': 'Step 6', 'desc': 'Task parallelism and sync variables'},
                {'title': 'Step 7', 'desc': 'Remote access and synchronization'},
                {'title': 'Step 8', 'desc': 'Locales and memory optimization'},
                {'title': 'Step 9', 'desc': 'Interfacing with C/C++'},
                {'title': 'Step 10', 'desc': 'Build parallel HPC applications'}
            ]
        }
    # Ring Example
    if "ring" in topic_lower:
        return {
            'title': '💍 Ring Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Install Ring and setup environment'},
                {'title': 'Step 2', 'desc': 'Syntax, variables, and data types'},
                {'title': 'Step 3', 'desc': 'Control flow and loops'},
                {'title': 'Step 4', 'desc': 'Functions, libraries, and modules'},
                {'title': 'Step 5', 'desc': 'Metaprogramming and signals'},
                {'title': 'Step 6', 'desc': 'OOP and object system'},
                {'title': 'Step 7', 'desc': 'GUI with RingQt or RingGUI'},
                {'title': 'Step 8', 'desc': 'Database connectivity (SQLite etc.)'},
                {'title': 'Step 9', 'desc': 'Web apps via RingWebServer'},
                {'title': 'Step 10', 'desc': 'Compile executable and packaging'}
            ]
        }
    # Oz Example
    if "oz" in topic_lower:
        return {
            'title': '🧩 Oz Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand Oz multiparadigm model'},
                {'title': 'Step 2', 'desc': 'Syntax, data types, and variables'},
                {'title': 'Step 3', 'desc': 'Functions, procedures, and pattern matching'},
                {'title': 'Step 4', 'desc': 'Lazy evaluation and dataflow concurrency'},
                {'title': 'Step 5', 'desc': 'Objects and classes'},
                {'title': 'Step 6', 'desc': 'LVars and futures'},
                {'title': 'Step 7', 'desc': 'Distributed programming support'},
                {'title': 'Step 8', 'desc': 'Constraint programming in Oz'},
                {'title': 'Step 9', 'desc': 'Debugging with Mozart environment'},
                {'title': 'Step 10', 'desc': 'Build real-world Oz applications'}
            ]
        }
    # Boo Example
    if "boo" in topic_lower:
        return {
            'title': '🔧 Boo Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn Boo syntax and .NET integration'},
                {'title': 'Step 2', 'desc': 'Variables, control flow, and types'},
                {'title': 'Step 3', 'desc': 'Type inference and duck typing'},
                {'title': 'Step 4', 'desc': 'Closures and generators'},
                {'title': 'Step 5', 'desc': 'List comprehensions and metaprogramming'},
                {'title': 'Step 6', 'desc': 'OOP support (classes, inheritance)'},
                {'title': 'Step 7', 'desc': '.NET interop and assemblies'},
                {'title': 'Step 8', 'desc': 'Scripting and REPL usage'},
                {'title': 'Step 9', 'desc': 'Testing and packaging'},
                {'title': 'Step 10', 'desc': 'Deploy .NET apps with Boo'}
            ]
        }
    # Janus Example
    if "janus" in topic_lower:
        return {
            'title': '🔄 Janus Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand reversible programming principles'},
                {'title': 'Step 2', 'desc': 'Janus syntax and reversible constructs'},
                {'title': 'Step 3', 'desc': 'Variables and reversible assignment'},
                {'title': 'Step 4', 'desc': 'Control flow – reversible loops/conditionals'},
                {'title': 'Step 5', 'desc': 'Procedures and call/rev-call'},
                {'title': 'Step 6', 'desc': 'State inversion and bidirectional dataflow'},
                {'title': 'Step 7', 'desc': 'Memory and garbage reversal techniques'},
                {'title': 'Step 8', 'desc': 'Debugging reversible programs'},
                {'title': 'Step 9', 'desc': 'Applications in reversible computing'},
                {'title': 'Step 10', 'desc': 'Performance & correctness in reversible systems'}
            ]
        }
    # PL/I Example
    if "pli" in topic_lower or "pl/i" in topic_lower:
        return {
            'title': '💼 PL/I Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'PL/I syntax and multiparadigm setup'},
                {'title': 'Step 2', 'desc': 'Data types, arrays, and pointers'},
                {'title': 'Step 3', 'desc': 'Control flow and structures'},
                {'title': 'Step 4', 'desc': 'File handling and I/O'},
                {'title': 'Step 5', 'desc': 'Subprograms and entry points'},
                {'title': 'Step 6', 'desc': 'Concurrency and multitasking'},
                {'title': 'Step 7', 'desc': 'Error handling and condition handlers'},
                {'title': 'Step 8', 'desc': 'Macros and compile-time features'},
                {'title': 'Step 9', 'desc': 'Interfacing with C/Assembly'},
                {'title': 'Step 10', 'desc': 'Deploy PL/I for enterprise systems'}
            ]
        }
    # ALGOL Example
    if "algol" in topic_lower:
        return {
            'title': '📚 ALGOL Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn ALGOL history and syntax structure'},
                {'title': 'Step 2', 'desc': 'Block structure and scope'},
                {'title': 'Step 3', 'desc': 'Variables and data types'},
                {'title': 'Step 4', 'desc': 'Control statements and loops'},
                {'title': 'Step 5', 'desc': 'Procedures and recursion'},
                {'title': 'Step 6', 'desc': 'Arrays and multidimensional arrays'},
                {'title': 'Step 7', 'desc': 'Pass-by-name/value semantics'},
                {'title': 'Step 8', 'desc': 'Writing standard ALGOL 60 code'},
                {'title': 'Step 9', 'desc': 'Understand ALGOL 68 extensions'},
                {'title': 'Step 10', 'desc': 'Historical implementations and compilers'}
            ]
        }
    # Simula Example
    if "simula" in topic_lower:
        return {
            'title': '🎞 Simula Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Simula as the first OOP language'},
                {'title': 'Step 2', 'desc': 'Classes, objects, and inheritance'},
                {'title': 'Step 3', 'desc': 'Coroutines and simulation support'},
                {'title': 'Step 4', 'desc': 'Data structures and records'},
                {'title': 'Step 5', 'desc': 'Input/output and text formatting'},
                {'title': 'Step 6', 'desc': 'Simula process scheduling'},
                {'title': 'Step 7', 'desc': 'Discrete event simulation basics'},
                {'title': 'Step 8', 'desc': 'Debugging with Simula environment'},
                {'title': 'Step 9', 'desc': 'Porting Simula to modern systems'},
                {'title': 'Step 10', 'desc': 'Legacy simulation applications'}
            ]
        }
    # Modula Example
    if "modula-2" in topic_lower or "modula-3" in topic_lower:
        return {
            'title': '🛠 Modula Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn module-based syntax and design'},
                {'title': 'Step 2', 'desc': 'Data types, records, and sets'},
                {'title': 'Step 3', 'desc': 'Procedures, functions, and recursion'},
                {'title': 'Step 4', 'desc': 'Interface and implementation modules'},
                {'title': 'Step 5', 'desc': 'Coroutines (Modula-2) or concurrency (Modula-3)'},
                {'title': 'Step 6', 'desc': 'Exception handling (Modula-3)'},
                {'title': 'Step 7', 'desc': 'Generic modules (Modula-3)'},
                {'title': 'Step 8', 'desc': 'Compilation and development tools'},
                {'title': 'Step 9', 'desc': 'System programming and low-level I/O'},
                {'title': 'Step 10', 'desc': 'Building modular systems'}
            ]
        }
    # Oberon Example
    if "oberon" in topic_lower:
        return {
            'title': '🏗 Oberon Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Study Oberon syntax and simplicity'},
                {'title': 'Step 2', 'desc': 'Modules and scope control'},
                {'title': 'Step 3', 'desc': 'Types, records, and pointers'},
                {'title': 'Step 4', 'desc': 'Procedures and control flow'},
                {'title': 'Step 5', 'desc': 'Exception handling and garbage collection'},
                {'title': 'Step 6', 'desc': 'Oberon System design'},
                {'title': 'Step 7', 'desc': 'GUI via Blackbox or native systems'},
                {'title': 'Step 8', 'desc': 'Compilation with Oberon toolchain'},
                {'title': 'Step 9', 'desc': 'System/Oberon OS development'},
                {'title': 'Step 10', 'desc': 'Maintainable platform stacks'}
            ]
        }
    # ML/SML/Caml Example
    if "ml" in topic_lower or "sml" in topic_lower or "caml" in topic_lower:
        return {
            'title': '🧠 ML/SML/Caml Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Study ML family syntax and functional foundations'},
                {'title': 'Step 2', 'desc': 'Pattern matching and algebraic data types'},
                {'title': 'Step 3', 'desc': 'Modules, functors, signatures'},
                {'title': 'Step 4', 'desc': 'References, arrays, and mutable state'},
                {'title': 'Step 5', 'desc': 'Exception handling'},
                {'title': 'Step 6', 'desc': 'Parsing with ML tools'},
                {'title': 'Step 7', 'desc': 'Compiler toolchains (ocamlc, mlton, SML/NJ)'},
                {'title': 'Step 8', 'desc': 'Project structure & build systems'},
                {'title': 'Step 9', 'desc': 'Interfacing with C'},
                {'title': 'Step 10', 'desc': 'Functional projects and deployment'}
            ]
        }
    # BCPL Example
    if "bcpl" in topic_lower:
        return {
            'title': '📼 BCPL Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'BCPL history and syntax basics'},
                {'title': 'Step 2', 'desc': 'Data types and operators'},
                {'title': 'Step 3', 'desc': 'Procedures and parameter passing'},
                {'title': 'Step 4', 'desc': 'Control flow and jumps'},
                {'title': 'Step 5', 'desc': 'Global and local variable scope'},
                {'title': 'Step 6', 'desc': 'Memory representation and pointers'},
                {'title': 'Step 7', 'desc': 'Write simple BCPL programs'},
                {'title': 'Step 8', 'desc': 'Study influence on C language'},
                {'title': 'Step 9', 'desc': 'Legacy compilation on modern systems'},
                {'title': 'Step 10', 'desc': 'Read and maintain BCPL code'}
            ]
        }
    # Forth Example
    if "forth" in topic_lower:
        return {
            'title': '🛠 Forth Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn stack-based execution model'},
                {'title': 'Step 2', 'desc': 'Vocabulary, words, and definitions'},
                {'title': 'Step 3', 'desc': 'Control structures and loops'},
                {'title': 'Step 4', 'desc': 'Memory and I/O in Forth'},
                {'title': 'Step 5', 'desc': 'Colon definitions and parameters'},
                {'title': 'Step 6', 'desc': 'Blocks and file structures'},
                {'title': 'Step 7', 'desc': 'Build applications interactively'},
                {'title': 'Step 8', 'desc': 'Extend Forth with new words'},
                {'title': 'Step 9', 'desc': 'System-level scripting and tooling'},
                {'title': 'Step 10', 'desc': 'Embed Forth in embedded systems'}
            ]
        }
    # PostScript Example
    if "postscript" in topic_lower:
        return {
            'title': '🎨 PostScript Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand PostScript stack and drawing model'},
                {'title': 'Step 2', 'desc': 'Graphics operators and paths'},
                {'title': 'Step 3', 'desc': 'Text drawing and fonts'},
                {'title': 'Step 4', 'desc': 'Loops, procedures, and conditionals'},
                {'title': 'Step 5', 'desc': 'Working with PostScript files'},
                {'title': 'Step 6', 'desc': 'Procedural graphics scripting'},
                {'title': 'Step 7', 'desc': 'Interactive PS programming'},
                {'title': 'Step 8', 'desc': 'Embedding in PDF workflows'},
                {'title': 'Step 9', 'desc': 'Debugging and optimization'},
                {'title': 'Step 10', 'desc': 'Build print-ready graphics'}
            ]
        }
    # Handlebars Example
    if "handlebars" in topic_lower:
        return {
            'title': '📄 Handlebars Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Learn Mustache-like templating syntax'},
                {'title': 'Step 2', 'desc': 'Variables, context and escaping'},
                {'title': 'Step 3', 'desc': 'Helpers and block helpers'},
                {'title': 'Step 4', 'desc': 'Partials and layouts'},
                {'title': 'Step 5', 'desc': 'Expression evaluation and subexpression'},
                {'title': 'Step 6', 'desc': 'Register custom helpers'},
                {'title': 'Step 7', 'desc': 'Precompile templates'},
                {'title': 'Step 8', 'desc': 'Integrate with JS/Node apps'},
                {'title': 'Step 9', 'desc': 'Testing templates'},
                {'title': 'Step 10', 'desc': 'Optimize and deploy templates'}
            ]
        }
    # Mustache Example
    if "mustache" in topic_lower:
        return {
            'title': '📄 Mustache Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Understand logic-less templating syntax'},
                {'title': 'Step 2', 'desc': 'Variables, sections, and iteration'},
                {'title': 'Step 3', 'desc': 'Partials and nested templates'},
                {'title': 'Step 4', 'desc': 'Context pushing and lambda sections'},
                {'title': 'Step 5', 'desc': 'Working with HTML/JSON outputs'},
                {'title': 'Step 6', 'desc': 'Implement in JS/Python/etc.'},
                {'title': 'Step 7', 'desc': 'Testing consistency'},
                {'title': 'Step 8', 'desc': 'Integrate with web frameworks'},
                {'title': 'Step 9', 'desc': 'Precompilation and caching'},
                {'title': 'Step 10', 'desc': 'Deployment and performance tuning'}
            ]
        }
    # FreeMarker Example
    if "freemarker" in topic_lower:
        return {
            'title': '🖋 FreeMarker Roadmap',
            'steps': [
                {'title': 'Step 1', 'desc': 'Setup FreeMarker with Java'},
                {'title': 'Step 2', 'desc': 'Template syntax and expressions'},
                {'title': 'Step 3', 'desc': 'Directives, loops, and conditions'},
                {'title': 'Step 4', 'desc': 'Includes and macros'},
                {'title': 'Step 5', 'desc': 'Custom directives and functions'},
                {'title': 'Step 6', 'desc': 'Data models and object wrappers'},
                {'title': 'Step 7', 'desc': 'Using API in Spring/Servlets'},
                {'title': 'Step 8', 'desc': 'Template caching and performance'},
                {'title': 'Step 9', 'desc': 'Testing and error recovery'},
                {'title': 'Step 10', 'desc': 'Deploy in production templates.'}
            ]
        }

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))
    roadmap = request.form.get('roadmap_html')
    pdf = io.BytesIO()
    pisa_status = pisa.CreatePDF(roadmap, dest=pdf)
    if pisa_status.err:
        return "PDF generation failed", 500
    pdf.seek(0)
    return send_file(pdf, download_name='roadmap.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True) 