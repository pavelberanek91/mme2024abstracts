from jinja2 import Environment, FileSystemLoader
import pandas as pd

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('template.tex')

df = pd.read_csv("submissions.csv", sep=";")

for index, row in df.iterrows():
    with open(f"chapters/abstracts/abs{row['ID']}.tex", "w", encoding="utf-8") as f:
        abstract_papername = row['Title']
        abstract_authoremail = row['Email']
        abstract_abstract = row['Abstract'].replace("{{newline}}", r"\newline ").replace("&", r"\&")
        abstract_keywords = ", ".join(row['Keywords'].replace("&", r"\&").split(","))
        abstract_author = row['Author']
        abstract_authors = []
        abstract_authors_info = []
        for author in row['Authors'].split("ˇ"):
            #print(author)
            authorinfos = author.split("%")
            author_firstname = authorinfos[0].strip()
            author_lastname = authorinfos[1].strip()
            author_affiliation = authorinfos[2].strip()
            if len(authorinfos) > 2:
                author_country = authorinfos[3].strip()
            if len(authorinfos) > 3:
                author_email = authorinfos[4].strip()
            if author_firstname + " " + author_lastname != abstract_author:
                abstract_authors.append(author_firstname + " " + author_lastname)
                abstract_authors_info.append(author_affiliation + ", " + author_country)
            else:
                abstract_author_info = author_affiliation + ", " + author_country
        abstract_authors_info.insert(0, abstract_author_info)
        abstract_authors_info = r"\newline ".join(abstract_authors_info)
        abstract_authors = ", ".join(abstract_authors)

        f.write(template.render(
            papername=abstract_papername,
            author=abstract_author,
            authoremail=abstract_authoremail,
            keywords=abstract_keywords,
            abstract=abstract_abstract,
            authorsinfo=abstract_authors_info,
            authors=abstract_authors
        ))

        # print(f"Created chapter {row['ID']}")
        # print(f"{abstract_papername=}")
        # print(f"{abstract_author=}")
        # print(f"{abstract_authoremail=}")
        # print(f"{abstract_keywords=}")
        # print(f"{abstract_abstract=}")
        # print(f"{abstract_authors=}")
        # print(f"{abstract_authors_info=}")
        # print("")
        # input()