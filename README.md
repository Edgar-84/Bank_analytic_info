# Bank analytic info - Prototype

This prototype is an implementation of part of the [whole task](https://www.upwork.com/att/download/openings/1738322560862203904/attachments/92cfc89d-57fb-457f-8451-7549af00f546/download)

The following functionality is implemented in this prototype:

1) working only with **PRESS_RELEASE** - document type
2) search for articles by specified period
3) downloading PDF files and information about the article and author
4) error logging
5) delay before sending a request, and raising the pause before the request up to 5 minutes in case of site errors (400 - 599).


The rest of the logic will be implemented in the future. In the final report you can see which fields are not realized yet, they will say: **"In progress...".** 

Example:
```
{
            "datetime_accessed": "2023-12-26T15:50:33.138431",
            "language": "In progress...",
            "document_type": "In progress...",
            "document_author": "Viljar Rääsk",
            "document_date": "2023-06-20",
            "document_title": "PROGNOOS. Aeglasem hinnatõus aasta teises pooles toetab majanduskasvu",
            "document_text": "In progress...",
            "document_html": "",
            "document_url": "https://haldus.eestipank.ee/sites/default/files/2023-06/2023.06.20_ep_majandusprognoos_23-2.pdf",
            "document_pdf_encoded": "In progress...",
            "document_tables": "In progress..."
        },
``` 

## Start script

Example code run:

```
from datetime import date
from scraper import run_scrape
start = date.fromisoformat('2022-01-01') # date of first document
end = date.fromisoformat('2022-12-31') # date of last document
document_types = ['PRESS_RELEASE'] # now work only PRESS_RELEASE documents
output = run_scrape(start, end, document_types) 
```

You can find the final report and downloaded PDF files in the folder: `results\`

All logs with information about work script you can find in the folder: `logs\`
