HTMLFILE="resume.html"
PDFFILE="resume.pdf"

pipenv run weasyprint $HTMLFILE $PDFFILE

open $PDFFILE