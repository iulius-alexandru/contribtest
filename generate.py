# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import logging
import json
import sys
import jinja2

log = logging.getLogger(__name__)

#Functia listeaza adresa fisierelor din care extragem obiectul de tip json si continutul paginii
#si numele fiecarui fisier
def list_files(folder_path):
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        yield os.path.join(folder_path, name),base
#Test list_files
"""
for x,y in list_files(sys.argv[1]):
 print(x,y)
"""
#Functia citeste obiectul de tip json care e pana la --- iar apoi citeste continutul
# paginii care e un sir de caractere
def read_file(file_path):
    with open(file_path, 'r') as f:
        raw_metadata = ""
        for line in f:
            if line.strip() == '---':
                break
            raw_metadata += line
        content = ""
        for line in f:
            content += line
    return json.loads(raw_metadata), content

#Test functie read_file
"""
js,content=read_file(os.path.join(sys.argv[1],'index.rst'))
print(js)
print(content)
"""
#Functia creeaza fisierul de tip html cu numele:name si continutul:html la adresa test/output
def write_output(name, html):
    # TODO should not use sys.argv here, it breaks encapsulation
    with open(os.path.join(os.path.join('Test', sys.argv[2]), name + '.html'), 'w') as f:
        f.write(html)
#Test functie write_output ('fisier_test' il voi genera nu este in momentul asta in folderul output)
"""
write_output('fisier_test','<h1>Fisier Test</h1>')
"""
#Functia generate site  ia ca parametru adresa folderului unde se afla fisierele
#cu informatiile care trebuie trecute in site-urile sablon pentru jinja2 si le trece si completeaza site-urile sabloane
#iar apoi le salveaza in folderul output cu numele fisierelor din care ia informatiile pentru completarea sabloanelor
def generate_site(folder_path):
    log.info("Generating site from %r", folder_path)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(folder_path,'layout')))

    for (file_path,name) in list_files(folder_path):
        metadata, content = read_file(file_path)
        template_name=metadata['layout']
        template = jinja_env.get_template(template_name)
        data = dict(metadata, content=content)
        html = template.render(**data)
        write_output(name, html)
        log.info("Writing %r with template %r", name, template_name)
#Testul functiei  "generate_site" l-am facut pe fisierele din source initiale + unul putin mai complex pe care l-am scris eu

def main():
    generate_site(sys.argv[1])

#creez folderul output daca nu e creat si generez site-urile
if __name__ == '__main__':
    logging.basicConfig()
    if(sys.argv[2] not in os.listdir("test")):
        os.mkdir(os.path.join("test",sys.argv[2]))
    main()
