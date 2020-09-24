import scrapy
import json

class glints_scrape(scrapy.Spider):
    name = 'glints'

    api_url = 'https://glints.com/api/marketplace/jobs?type[]=FULL_TIME&CountryCode=ID&sortBy=latest&SearchTerm=%s&limit=%s'

    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
    }

    cookie_string = '_gcl_au=1.1.241398559.1596816768; _ga=GA1.2.348865641.1596816768; G_ENABLED_IDPS=google; MgidSensorHref=https://glints.com/id/signup?id=22354848-7574-422d-8069-f10b6c95b093&title=software-engineer-back-end&next=%2Fopportunities%2Fjobs%2F%5Bid%5D&nextAs=%2Fopportunities%2Fjobs%2Fsoftware-engineer-back-end%2F22354848-7574-422d-8069-f10b6c95b093%2Fapply; MgidSensorNVis=1; __smToken=F4JSw0ImKsbDNNG6oaf3R4pF; __atuvc=9%7C34; __atssc=google%3B4; _hjid=ba756b8d-a8d1-43f6-87e8-8dff0db843d8; _hjDonePolls=284358; _hjMinimizedPolls=497807; session=Fe26.2**03c2bd318858999c10938d971713957efe028bc6d1452d5835b50b7d207f366d*Nap6ozxt2mRvil3yctPYzw*Ix6x8o6fmGkSzKesE5VOLk43rWc5ELLCOcLrMKTqRnExKjvIH56F0EjYEDjWnpKa**b84ec712926603f3e7cf45991b78aec117293b94c622ab32d4175843cff6b5ac*vmroVb2JVvWATCfiYJqNDWS8gziTmOiJxtN0PoqB5r8; _gid=GA1.2.1932203066.1600634343; _hjIncludedInSessionSample=1; _hjAbsoluteSessionInProgress=0; fcaid=2658ef1cbbae141bc7f2670fcf5f1112d0ce573c7e7dc8fa873d31afcf9202a0; fcuid=d7d5becf-fc34-4414-9e4a-83b8989706b9; fccid=f6c7223c-0986-4026-899c-3b2e2ff8ed39; amplitude_id_26bdf4b56b304d7bfc6275ea77f2310cglints.com=eyJkZXZpY2VJZCI6IjFhYTRmN2NkLWI3ZjEtNDk0My05ZTdjLTk3NTc2ZmRmOWFlZFIiLCJ1c2VySWQiOiIxZTYwYzhjNi1iMGVkLTRiNWYtYmY4NC1iZjY5NWI2ODNjZjYiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE2MDA4MzQ0MzgzMDksImxhc3RFdmVudFRpbWUiOjE2MDA4MzQ1Njc1MzgsImV2ZW50SWQiOjQ3MiwiaWRlbnRpZnlJZCI6Mzg4LCJzZXF1ZW5jZU51bWJlciI6ODYwfQ=='

    def start_requests(self):
        cookies = {}

        for cook in self.cookie_string.split('; '):
            try:
                key = cook.split('=')[0]
                val = cook.split('=')[1]

                cookies[key] = val

            except:
                pass

        if self.total == 'all':
            self.total = 1000

        yield scrapy.Request(url=self.api_url % (self.category, self.total), cookies=cookies, headers=self.header, callback=self.parse)

    def parse(self,response):
        res_json = json.loads(response.body)
        if len(res_json['data']) == 0:
            yield{
                'Company Name': '-',
                'Company Location': '-',
                'Website': '-',
                'Working Location': '-',
                'Job Title': '-',
                'Minimal Year Experience': '-',
                'Currency': '-',
                'Minimal Salary': '-',
                'Maximan Salary': '-',
                'Job Description': '-'
            }
        else:
            for ttl_dat in range (len(res_json['data'])):
                currency, min_sal, max_sal = '', '', ''
                if len(res_json['data'][ttl_dat]['links']['jobSalaries']) == 0:
                    currency = '-'
                    min_sal = '-'
                    max_sal = '-'
                else:
                    for sal in res_json['data'][ttl_dat]['links']['jobSalaries']:
                        currency = sal['CurrencyCode']
                        min_sal = sal['minAmount']
                        max_sal = sal['maxAmount']

                desc = []
                for des in res_json['data'][ttl_dat]['descriptionRaw']['blocks']:
                    desc.append(des['text'])

                yield{
                    'Company Name': res_json['data'][ttl_dat]['links']['company']['name'],
                    'Company Location': res_json['data'][ttl_dat]['links']['company']['CountryCode'],
                    'Website': res_json['data'][ttl_dat]['links']['company']['website'],
                    'Working Location': res_json['data'][ttl_dat]['links']['city']['name'],
                    'Job Title': res_json['data'][ttl_dat]['title'],
                    'Minimal Year Experience': res_json['data'][ttl_dat]['minYearsOfExperience'],
                    'Currency': currency,
                    'Minimal Salary': min_sal,
                    'Maximan Salary': max_sal,
                    'Job Description': ' -- '.join(desc)
                }
