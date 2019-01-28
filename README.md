# sample

A simple project to show how gradescope works.

There are two halves of the project

## p1-gradescope

This contains all of the infrastructure to grade the project.  

Gradescope's documentation is excellent and can be found here:
https://gradescope-autograders.readthedocs.io/en/latest/

setup.sh is run only once when you setup the grader in gradescope.  It installs any packages you may need for grading, such as a compiler, python etc.  It is best to do as much setup here as possible to make grading fast.

run_autograder is what runs when grading a student submission.

/autograder/source contains the extracted contents of your autograder zip file.

This script must produce a file called /autograder/results/results.json, which contains the results of grading in json format.  The json format is described here:
https://gradescope-autograders.readthedocs.io/en/latest/specs/#output-format

## p1-student

This is the the starter code you distribute to students.  It only contains the Makefile etc, but not the grading infrastructure or the solution.  
