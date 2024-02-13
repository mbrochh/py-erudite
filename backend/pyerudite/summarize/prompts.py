CONSISE_SUMMARY = """
Create a bullet point summary of the text that will follow after the heading `TEXT:`. 

Do not just list the general topic, but the actual facts that were shared.

For example, if a speaker claims that "a dosage of X increases Y", do not
just write "the speaker disusses the effects of X", instead write "a dosage 
of X increases Y".

Use '- ' for bullet points:

After you have made all bullet points, add one last bullet point that 
summarizes the main message of the content, like so:

- Main message: [MAIN MESSAGE HERE]

---

TEXT TITLE: {title}

TEXT:
{chunk}
"""
