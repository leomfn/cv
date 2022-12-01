import json
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
                jobinfo, jobtasks = job2html(j)
                element.append(jobinfo)
                element.append(jobtasks)
        elif element.attrib["id"] == "education":
            for e in edu:
                eduinfo, edudesc = edu2html(e)
                element.append(eduinfo)
                element.append(edudesc)
        elif element.attrib["id"] == "skills":
            nrows = ceil(len(skills.keys())/2)
            skillrows = [DIV(CLASS("skillrow")) for i in range(nrows)]
            # DIV(CLASS("skillrow"))
            # len(skillrows)
            i = 0
            for s in skills:
                
                # if i == 1:
                # skillrow = DIV(CLASS("skillrow"))
                # if i == 2:
                #     skillrows.append(DIV(CLASS("skillrow")))
                #     i = 1
                skillset = skill2html(s)
                skillrows[i].append(skillset)
                # print(len(skillset))
                # if i == 2:
                    # skillrows = skillrows.append()
                    # element.append(skillrow)
                    # print("skillrow appended")
                    # print(type(DIV()))
                    # i = 1
                if len(skillrows[i]) == 2:
                    i += 1
            for r in skillrows:
                element.append(r)
                

# print(etree.tostring(employment, pretty_print=True).decode())

with open("print.html", "w", encoding="utf-8") as f:
    f.write(etree.tostring(employment, pretty_print=True).decode())
