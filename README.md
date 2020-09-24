# Glints Job Extraction

Glints job extraction is an python app to extracts jobs from www.glints.com automatically from the newest job posted. To run the program, you need to parse two arguments: 
1. The first argument is the 'category' argument. It is used as the main keyword filter based on the job posted on glints. For example python, frontend, database, etc.
2. The second argument is 'total' argument. The program will fetch the total data based on the second arguments. So if the second argument is 10 then your total data will be 10. If you want scrape all of data just type 'all'.

The output file can be in JSON, xlsx, and CSV format.

To run the program, you need to use this format: "scrapy crawl glints -a category=python -a total=20 -o data.json"
