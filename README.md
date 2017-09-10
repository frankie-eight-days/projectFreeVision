# projectFreeVision
**Purpose**

This is a project I started one weekend after an interesting dinner conversation. It is well-known that Google tracks your browsing activty,
however, it is little known that they tailor search results to match the user's browsing history. The aim of this project is to create a
'graphical' analysis of how these search resluts differ depending on wording. 

---

**What it is**

What this code does is go to various news sources and grab their headlines. These news sources are catagorized by their political affiliation,
for example, Fox news is regarded as more of a conservative news soruce, while Buzzfeed or CNN may be regarded as a liberal news source.
After the script grabs the headlines it scans them for buzzwords and saves them in a database (Actually a google sheet, how meta is that?).
Then the conservative buzzwords are matched with the liberal buzzwords and a Google search is conducted. Finally the search results and 
search keys are stored in a new sheet on the spreadsheet. The spreadsheet can be seen [here](https://docs.google.com/a/mun.ca/spreadsheets/d/1DTDmpP9dlUfZhfm8Bb4AL7-PfqlbjoCEI0FxUFGfjA0/edit?usp=sharing)
(Last updated September 10th)

---

**Moving Forward**

If updated, there are a few things which I would like to do:
* Make buzzword identification better
* Make matching algorithim better
* Add VPN support, so Google doesn't ban my IP so much
* After that, add how search results differ from country to country
