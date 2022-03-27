import requests
import bs4
import tweepy
from engineering_scrapper import main_func2
import time

class JobMagScraper:

    def __init__(self):
        print('Loading page...')
        self.url=f'https://www.myjobmag.co.ke/search/jobs?q=&field=Engineering+%2F+Technical'

        #CONSUMER'''
        self.API_KEY = "Pru9XrC0q7bjLzPJMyeXg3hqc"
        self.API_SECRET = 'sVnYQgrMod2En78FYEdYZIsCy1aa39IE6tZx7kDdIrzZ2ElZNW'
        #TOKENS
        self.ACCESS_TOK  = "1507185827352395779-PJ2XNO3aq5dtPFULerWjzoIrfX2xZI"
        self.ACCESS_SEC = "Fr0XPbwVe3ga1iJxMsdwpwprROuy5GzWHq72UPqCi3hk0"
        self.new_content = []

    def getJobtitle(self,soup):
        title=soup.select('section h1')
        return str(title[0].getText())


    def getDescription(self,soup):
        Description=soup.select('.job-details p')
        return str(Description[0].getText())


    def getAcademics(self,soup):
        Academics=soup.select('.job-key-info span')
        return str(Academics[3].getText())


    def getExperience(self,soup):
        Experience=soup.select('.job-key-info span')
        return str(Experience[5].getText())


    def save_job_info(self,JobTitle,JobDescription,JobAcademics,JobExp,job_Link):
        print('Saving job specifications...')
        jobfile=open('C:\\Users\\peter\\Desktop\\TwitterBot\\Jobmag scrapped.txt','a')
        job_details = f'Title:{JobTitle}' +'\n'+'Academics:{JobAcademics}'+'\n'+'Experience:'+JobExp+'\n'+job_Link
        jobfile.write(job_details)
        jobfile.write(job_Link+'\n'+'*'*70)
        jobfile.close()  
        if len(job_details) > 280:
            job_details='Title: {JobTitle}'+'\n'+'Academics:{JobAcademics}'+"\n"+job_Link

    
        if job_details not in self.new_content:
            self.new_content.append(job_details)

    def  bot(self,new_content):
        auth = tweepy.OAuthHandler (self.API_KEY, self.API_SECRET)
        auth.set_access_token(self.ACCESS_TOK, self.ACCESS_SEC)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        print('BOT running.....')
        print('-'* 70)
        for cont in new_content:
            api.update_status("#ikoKaziKE #careeropportunities\n" + cont)

        eng_contents = main_func2()
        if len(eng_contents)>0:
            for eng_cont in eng_contents:
                api.update_status("#ikoKaziKE #careeropportunities\n" + eng_cont)
                time.sleep(10)
                

    def mainfunc(self):
        res=requests.get(self.url)
        res.raise_for_status()
        soup=bs4.BeautifulSoup(res.text,'html.parser')
        elems=soup.select('section a')
        for i in range (1,35,2):
            jobUrl=requests.get('https://www.myjobmag.co.ke'+elems[i].get('href'))
            job_Link='https://www.myjobmag.co.ke'+elems[i].get('href')
            jobUrl.raise_for_status()
            soup=bs4.BeautifulSoup(jobUrl.text,'html.parser')
            print('Getting job specifications...')
            JobTitle = self.getJobtitle(soup)
            file = open('C:\\Users\\peter\\Desktop\\TwitterBot\\Jobmag scrapped.txt','r')
            file_read = file.read()
            file.close()
            if JobTitle and job_Link  in file_read:
                print("GOT A TWIN")
                continue
            else:
                
                JobDescription= self.getDescription(soup)
                JobAcademics= self.getAcademics(soup)
                JobExp= self.getExperience(soup)

                self.save_job_info(JobTitle,JobDescription,JobAcademics,JobExp,job_Link)
        print('Done.....')
        print('Proceeding to posting stage......')
        new_content = self.new_content
        self.bot(new_content)
        
scrapper = JobMagScraper()
new_cont = scrapper.mainfunc()









