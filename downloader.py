from bs4 import BeautifulSoup
import requests
import pandas as pd

#initialize empty dataframe
df = pd.DataFrame(columns=['ID', 'Author', 'Title', 'Link'])

cookies = {
    'cool1': '093f10ae85e67f3d3e2f9',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'cs-CZ,cs;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'cool1=2f1aa0376dc05348210cf',
    'Referer': 'https://easychair.org/account2/signin',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}

response = requests.get("https://easychair.org/conferences2/submissions?a=32726078", cookies=cookies, headers=headers)

soup = BeautifulSoup(response.content, "html.parser") 
table_rows = soup.find_all("tr", class_="green")
for row in table_rows:
    table_cells = row.find_all("td")
    id = table_cells[0].text
    #author = table_cells[1].text
    title = table_cells[2].text
    link = "https://easychair.org" + table_cells[3].find("a")["href"]

    soup2 = BeautifulSoup(requests.get(link, cookies=cookies, headers=headers).content, "html.parser")
    tables = soup2.find_all("div", class_="ct_tbl")
    table_submissions = tables[0]
    table_authors = tables[1]

    for row in table_submissions.find_all("tr"):
        tds = row.find_all("td")
        if "Author keywords" in tds[0].text:
            keywords_row = row
        if "Abstract" in tds[0].text:
            abstract_row = row

    keywords_cell = keywords_row.find("td", class_="value")
    keywords = keywords_cell.find_all("div")
    keywords = ",".join([keyword.text for keyword in keywords])

    abstract_cell = abstract_row.find("td", class_="value")
    abstract = abstract_cell.text.strip().replace("<br>", "").replace("\n", "")

    authors_rows = table_authors.find_all("tr")[2:]
    authors = []
    main_author_name = None
    main_author_email = None
    for row in authors_rows:
        cells = row.find_all("td")
        first_name = cells[0].text
        last_name = cells[1].text
        email = cells[2].text
        if main_author_name is None:
            main_author_name = first_name + " " + last_name
            main_author_email = email
        country = cells[3].text
        affiliation = cells[4].text
        author_with_afill = "%".join([first_name, last_name, affiliation, country, email])
        authors.append(author_with_afill)
    authors = "ˇ".join(authors)

    df = df._append({
        'ID': id, 
        'Author': main_author_name, 
        'Email': main_author_email,
        'Title': title, 
        'Link': link, 
        "Keywords": keywords, 
        "Abstract": abstract,
        "Authors": authors
        }, ignore_index=True)
    
print(df)
df.to_csv("submissions.csv", index=False, sep=";")