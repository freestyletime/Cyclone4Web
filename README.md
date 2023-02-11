# Cyclone4Web

## 1. Goals of this project
This project is my final homework of <em><strong>CS642[A] — Msc Computer Science (Applied) Project </strong></em>. 

The whole project adopts `Flask` framework, this is a micro web framework written in Python and depends on the `Jinja` template engine and the `Werkzeug WSGI` toolkit, to constructing a simple online integrated development environment for **[Cyclone](https://classicwuhao.github.io/cyclone_tutorial/tutorial-content.html)**. Cyclone is designed to provide a general solution to problems that can be described as a graph. Cyclone provides a specification language that allows users to describe a graphical structure along with conditions to be met and automatically solves them for you.

## 2. Before running
We need to install some softwares and tools to support the project.
* [Install Python 3.10.5](https://www.python.org/downloads/release/python-3105/) in your machine first.
* Clone `Cyclone4Web` to your machine.
* (Optional) Open CMD/Terminal and install the `virtualenv` by using the following command (this is a type of library that allows us to create a virtual environment and use it):
    ```
    > pip install virtualenv
    ```
* (Optional) Enter the project folder running the following command to create a virtual environment:
    ```
    > Python3 -m venv env  
    ```
* Install all the [dependencies](requirements.txt) by using the following command: 
    ```
    (env) > pip install -r requirements.txt
    ```
* Make sure you have java (64 bit is recommended) installed on your machine.
* [Download Cyclone](https://classicwuhao.github.io/cyclone_tutorial/installation.html) and Unzip it to a folder called `Cyclone`.
* Copy the entire `Cyclone` folder to the root of the project

This is the well-configured project structure.
<div><img alt="project structure" src='screenshots/projectStructure.png' width=350></div>

## 3. Run project
Open CMD/Terminal and execute the following command:
```
(env) > python3 app.py
    * Serving Flask app 'flaskr'
    * Debug mode: on
    * Running on http://127.0.0.1:8080 (Press CTRL+C to quit)
    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: nnn-nnn-nnn
```
And then, you can visit the project by clicking the [local link](http://127.0.0.1:8080).

This is the screenshot of `HomePage`:
<div>
<img src='screenshots/homePage.png' width=750>
</div>

## 4. Project layout

```
./Cyclone4Web
├── flaskr/
│   ├── __init__.py
│   ├── config.py
│   ├── unit_test.sql
│   ├── src/
│   │   ├── __init__.py
│   │   └── editor_view.py
│   ├── templates/
│   │   ├── about.html
│   │   ├── error.html
│   │   ├── index.html
│   │   └── _layouts/
│   │       ├── default.html
│   │       ├── footer.html
│   │       ├── head.html
│   │       ├── header.html
│   │       └── script.html
│   └── static/
│       ├── js/
│       ├── css/
│       └── img/
├── Cyclone/
├── tests/
├── venv/
├── doc/
├── tmp/
├── ex.sh
├── app.py
├── MANIFEST.in
├── LICENSE
└── .gitignore

```
## 5. Functions
1. HomePage(`http://localhost/editor`)
    - authorization (user isolation)
    - integrate an online code editor
        - syntax highlight
        - simple code complementation
        - the flexible size
        - various themes
    - integrate an output console
        - the flexible size
    - complie the online code and run it
    - save the online code as a local file
    - clear the code in the online code editor
    - upload a `.cyclone` file to the online code editor(Maximum 10KB)
    - a switch of `option-trace`
    - a switch of `option-timeout`
    - a loading covering when doing request
    - support to download the `.trace` file after runing
    - list the examples in the `Cyclone` folder
    - put the example code onto the online code editor when clicking
    - a link to the official website of the **[Cyclone Tutorial](https://classicwuhao.github.io/cyclone_tutorial/tutorial-content.html)**
    - a link to the **[Cyclone author](https://github.com/classicwuhao)**
2. AboutPage(`http://localhost/about`)
3. ErrorPage(`http://localhost/error`)
    - 404 Error handler
    - 405 Error handler

## LICENSE
[Apache License Version 2.0](License) © [freestyletime](https://github.com/freestyletime)