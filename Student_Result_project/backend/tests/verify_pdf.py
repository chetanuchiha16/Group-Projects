
import sys
import os
# Add backend to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from visuals.student_report import create_student_report
from io import BytesIO

class MockStudent:
    def __init__(self):
        self.name = "John Doe"
        self.usn = "1JS23CS032"
        self.semester = "sem2"
        self.total_marks = 450
        self.percentage = 75.0
        self.sgpa = 8.5
        self.cgpa = 8.2
        self.subject_names = [
            "Mathematics for Computer Science Engineering-II (Long name to test overlap)",
            "Applied Physics for CSE Stream with advanced labs",
            "Principles of Programming using C with embedded systems focus",
            "Computer Aided Engineering Drawing and Visualization Techniques",
            "Basic Electronics and Communication Engineering including VLSI",
            "Introduction to Python Programming and Data Structures",
            "Functional English for Professional Communication",
            "Samskruthika Kannada (Cultural Heritage of Karnataka)"
        ]
        self.subject_codes = ["22MATS21", "22PHYS22", "22POPC23", "22CAED24", "22BECE25", "22PLC26", "22ENG27", "22KSK28"]
        self.ia_marks = [45, 48, 42, 40, 46, 44, 49, 47]
        self.see_marks = [45, 42, 48, 40, 44, 46, 41, 43]
        self.credits = [4, 4, 3, 3, 3, 3, 1, 1]
        self.pass_fail = ["Pass"] * 8

if __name__ == "__main__":
    student = MockStudent()
    try:
        pdf_bytes = create_student_report(student)
        with open("tests/verification.pdf", "wb") as f:
            f.write(pdf_bytes)
        print("Verification PDF created at tests/verification.pdf")
    except Exception as e:
        print(f"Error during PDF generation: {e}")
        sys.exit(1)
