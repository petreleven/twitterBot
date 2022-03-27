import requests
import bs4

new_contents = []

def title_(soup):
    title = soup.find('li',class_="mag-b").getText()
    return title

def desc_(soup):
    descriptioon = soup.find_all('li',class_="job-desc")[0].getText()
    return descriptioon

def location_(soup):
    location = soup.find_all('span',class_="comp-info-desc")
    location = location[-1].getText().strip()
    return location

def save_job_info2(title,description,job_Link,location):
    print('Saving job specifications...')
    jobfile=open('C:\\Users\\peter\\Desktop\\TwitterBot\\Jobmag scrapped.txt','a')
    job_details = f'Title:{title}\n{description.strip()}\nOffices:{location.strip()}\n{job_Link}'
    jobfile.write(job_details)
    jobfile.write(job_Link+'\n'+'*'*70)
    jobfile.close()
    if len(job_details)>280:
        job_details = f'Title:{title}\n{description[0:len(description)-len(description)//2]}..\n{job_Link}'
    new_contents.append(job_details)


def main_func2():
    res=requests.get(f'https://www.myjobmag.co.ke/search/jobs?q=engineer')
    res.raise_for_status()
    soup=bs4.BeautifulSoup(res.text,'html.parser')
    elems=soup.select('section a')
    for i in range (2,37,2):
        jobUrl=requests.get('https://www.myjobmag.co.ke'+elems[i].get('href'))
        job_Link='https://www.myjobmag.co.ke'+elems[i].get('href')
        jobUrl.raise_for_status()
        soup=bs4.BeautifulSoup(jobUrl.text,'html.parser')
        print('Getting job specifications...')
        title = title_(soup)
        file = open('C:\\Users\\peter\\Desktop\\TwitterBot\\Jobmag scrapped.txt','r')
        file_read = file.read()
        file.close()
        if title and job_Link  in file_read:
            print("GOT A TWIN")
            continue
        else:
            description = desc_(soup)
            location = location_(soup)
            save_job_info2(title,description,job_Link,location)  

    print('Done.....')
    print('Proceeding to posting stage......')
    return new_contents

