import re
def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ").replace('"', " ")
    s = s.split()
    if len(text) == 0:
        return text
    return s[0] + ''.join(i.capitalize() for i in s[1:])

with open("redirects_clean.txt", "r") as file:
    for line in file:
        line=line.strip()
        article=to_camel_case(re.search(r'(?<=\[\[).*?(?=\])', line).group(0))
        redirect=to_camel_case(re.search(r'(?<=Articles/).*(?=.txt)', line).group(0))
        owl="owl:sameAs"
        if article != redirect:
            print("<{}> {} <{}> .".format(article,owl,redirect))