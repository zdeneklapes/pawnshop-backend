import os.path
import os
import pdfkit

DIR = os.path.dirname(__file__)
# t1 = os.path.join(DIR, "test.html")
t1 = os.path.join(DIR, "loan_test1.html")
pdfkit.from_file(t1, "foo.pdf")
