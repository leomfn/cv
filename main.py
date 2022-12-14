import json
import re
from math import ceil
from lxml import html, etree
from lxml.html.builder import P, UL, LI, DIV, SPAN, CLASS

with open("employment.json", encoding="utf-8") as f:
    jobs = json.load(f)

with open("education.json", encoding="utf-8") as f:
    edu = json.load(f)

with open("skills.json", encoding="utf-8") as f:
    skills = json.load(f)


def job2html(job: dict = None):
    jobbox = DIV(CLASS("jobbox"))

    jobinfo = DIV(CLASS("jobinfo"))
    jobinfo.append(DIV(job["employer"], CLASS("institute")))
    jobinfo.append(DIV(job["timeframe"], CLASS("timeframe")))
    jobbox.append(jobinfo)

    jobdescription = DIV(CLASS("jobdescription"))
    jobdescription.append(DIV(job["position"], CLASS("stationtitle")))
    jobtasks = UL(CLASS("jobtasklist"))
    for t in job["description"]:
        jobtasks.append(LI(t))
    jobdescription.append(jobtasks)
    jobbox.append(jobdescription)
    return jobbox


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


def skill2html(skill: dict = None) -> html.HtmlElement:
    skillset = DIV(CLASS("skillset"))
    skillset.append(P(skill, CLASS("skilltitle")))
    skilllist = UL(CLASS("skilllist"))
    for key, value in skills[skill].items():
        skillentry = LI(CLASS("skillentry"))
        skillentry.append(SPAN(key, CLASS("skillname")))
        if len(value) > 0:
            skillentry.append(SPAN(f": {', '.join(value)}", CLASS("skilldesc")))
        skilllist.append(skillentry)
    skillset.append(skilllist)
    return skillset


employment = html.parse("print.html")

for element in employment.iter():
    if element.tag == "section":
        if element.attrib["id"] == "employment":
            for j in jobs:
                element.append(job2html(j))
        elif element.attrib["id"] == "education":
            for e in edu:
                eduinfo, edudesc = edu2html(e)
                element.append(eduinfo)
                element.append(edudesc)
        elif element.attrib["id"] == "skills":
            nrows = ceil(len(skills.keys())/2)
            skillrows = [DIV(CLASS("skillrow")) for i in range(nrows)]
            i = 0
            for s in skills:
                skillset = skill2html(s)
                skillrows[i].append(skillset)
                if len(skillrows[i]) == 2:
                    i += 1
            for r in skillrows:
                element.append(r)

printstring = re.sub(r"\[(.*)\]", r"<mark>\1</mark>",
                     etree.tostring(employment, pretty_print=True).decode())

with open("print.html", "w", encoding="utf-8") as f:
    f.write(printstring)
