import json
from lxml import html, etree
from lxml.html.builder import UL, LI, DIV, SPAN, CLASS

with open("employment.json", encoding="utf-8") as f:
    jobs = json.load(f)

with open("education.json", encoding="utf-8") as f:
    edu = json.load(f)


def job2html(job: dict = None):
    jobinfo = DIV(
        DIV(
            SPAN(job["position"], CLASS("stationtitle")),
            SPAN(job["timeframe"]),
            CLASS("stationtitlerow")
            ),
        DIV(
            SPAN(job["employer"]),
            CLASS("stationplacerow")
        ),
        CLASS("stationheader")
        )
    jobtasks = DIV()
    tasks = UL(CLASS("stationdesc"))
    for t in job["description"]:
        tasks.append(LI(t))
    jobtasks.append(tasks)
    return jobinfo, jobtasks


def edu2html(edu: dict = None):
    eduinfo = DIV(
        DIV(
            SPAN(edu["program"], CLASS("stationtitle")),
            SPAN(edu["timeframe"]),
            CLASS("stationtitlerow")
            ),
        DIV(
            SPAN(edu["institute"]),
            CLASS("stationplacerow")
        ),
        CLASS("stationheader")
        )
    edudesc = DIV()
    desc = UL(CLASS("stationdesc"))
    for e in edu["description"]:
        desc.append(LI(e))
    edudesc.append(desc)
    return eduinfo, edudesc


employment = html.parse("print.html")

for element in employment.iter():
    if element.tag == "section":
        if element.attrib["id"] == "employment":
            for j in jobs:
                jobinfo, jobtasks = job2html(j)
                element.append(jobinfo)
                element.append(jobtasks)
        elif element.attrib["id"] == "education":
            for e in edu:
                eduinfo, edudesc = edu2html(e)
                element.append(eduinfo)
                element.append(edudesc)

# print(etree.tostring(employment, pretty_print=True).decode())

with open("print.html", "w", encoding="utf-8") as f:
    f.write(etree.tostring(employment, pretty_print=True).decode())
