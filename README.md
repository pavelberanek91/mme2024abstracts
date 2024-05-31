# MME2024 Book of abstracts generator

## Latex files and folders description

* chapters: contains chapters of book of abstract. From these partial files the whole document is created.
* chapters/abstracts/absX.tex: represents generated abstract from script
* chapters/invited/abs00X.tex: represents manualy created abstract of invited speaker
* templates/template.tex: file that is filled with jinja2 marks. These marks are replaced by submission data.
* abstraktik.tex: latex file that is filled with custom commands that are used in templates/template.tex file.
* main.text: latex file that represent the main tex file for book of abstracts. It is compiled to PDF. You change structure of generated document by changing content of this file.

## Scripts file descriptions

* downloader.py: script that was used to download all the data from easychair webpage (not needed anymore), output of script can be seen in file submissions.csv
* tex_creator.py: script that is used to create all the abstract abs*.tex files in chapters/abstracts folder. It uses jinja2 template language to fill data from python to latex template.
* requirements.txt: used to install all dependencies for python to run scripts (pandas, requests, beautifulsoup4).

## Data files descriptions

* submissons.csv: all the data about abstract submissions to easychair. Submissions are separated by newline character (rows), submission data are separated by ";" symbol (cells of row). Multiple authors in one submission are separated by "ˇ" symbol and their partial informations (firstname, lastname, email, affiliation, country) are separated by "%" symbol.