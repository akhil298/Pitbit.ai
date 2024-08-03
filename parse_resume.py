
#### `parse_resume.py`

```python
import json

def parse_resume(resume_text):
    lines = resume_text.strip().split('\n')
    json_output = {
        "Personal Information": {},
        "Summary": "",
        "Experience": [],
        "Education": [],
        "Skills": {},
        "Projects": []
    }
    
    section = None
    experience = None
    
    for line in lines:
        if line.strip() == "":
            continue
        
        if line.startswith("Name:"):
            json_output["Personal Information"]["Name"] = line.split(":")[1].strip()
        elif line.startswith("Email:"):
            json_output["Personal Information"]["Email"] = line.split(":")[1].strip()
        elif line.startswith("Phone:"):
            json_output["Personal Information"]["Phone"] = line.split(":")[1].strip()
        elif line.startswith("Location:"):
            json_output["Personal Information"]["Location"] = line.split(":")[1].strip()
        elif line.startswith("Summary:"):
            section = "Summary"
            json_output[section] = line.split("Summary:")[1].strip()
        elif line.startswith("- Company"):
            if section == "Experience" and experience:
                json_output["Experience"].append(experience)
            section = "Experience"
            experience = {
                "Company": line.split("- Company")[1].strip(),
                "Duration": "",
                "Role": "",
                "Responsibilities": []
            }
        elif section == "Experience" and "Role:" in line:
            experience["Role"] = line.split("Role:")[1].strip()
        elif section == "Experience" and " - " in line:
            experience["Responsibilities"].append(line.strip(" - "))
        elif line.startswith("- B.S. in") or line.startswith("- M.S. in"):
            if section == "Experience" and experience:
                json_output["Experience"].append(experience)
            section = "Education"
            education = {
                "Degree": line.split(",")[0].strip("- ").strip(),
                "Institution": line.split(",")[1].strip(),
                "Year": line.split("(")[1].strip(")")
            }
            json_output["Education"].append(education)
        elif line.startswith("Skills:"):
            section = "Skills"
            json_output["Skills"] = {skill.strip().split(":")[0]: [s.strip() for s in skill.strip().split(":")[1].split(",")] for skill in line.split("Skills:")[1].strip().split(";")}
        elif line.startswith("- Project"):
            if section == "Experience" and experience:
                json_output["Experience"].append(experience)
            section = "Projects"
            project = {
                "Name": line.split(":")[0].strip("- "),
                "Description": line.split(":")[1].strip()
            }
            json_output["Projects"].append(project)
    
    if section == "Experience" and experience:
        json_output["Experience"].append(experience)
    
    return json_output

if __name__ == "__main__":
    with open("sample_resume.txt", "r") as file:
        resume_text = file.read()
    
    json_output = parse_resume(resume_text)
    print(json.dumps(json_output, indent=4))
