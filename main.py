import json
from lxml import html, etree
from lxml.html.builder import E, UL, LI, DIV, SPAN, CLASS

with open("employment.json", encoding="utf-8") as f:
    jobs = json.load(f)


def job2html(job: dict = None):
    jobinfo = DIV(
        DIV(
            SPAN(job["position"], CLASS("jobtitle")),
            SPAN(job["timeframe"], CLASS("right")),
            CLASS("tablerow")
            ),
        DIV(
            SPAN(job["employer"]),
            CLASS("tablerow")
        ),
        CLASS("jobtable")
        )
    jobtasks = DIV()
    tasks = UL(CLASS("jobtasks"))
    for t in job["description"]:
        tasks.append(LI(t))
    jobtasks.append(tasks)
    return jobinfo, jobtasks


employment = html.parse("print.html")

for element in employment.iter():
    if element.tag == "section":
        if element.attrib["id"] == "employment":
            for j in jobs:
                jobinfo, jobtasks = job2html(j)
                element.append(jobinfo)
                element.append(jobtasks)

# print(etree.tostring(employment, pretty_print=True).decode())

with open("print.html", "w", encoding="utf-8") as f:
    f.write(etree.tostring(employment, pretty_print=True).decode())

