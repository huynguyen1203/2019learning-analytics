# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 02:25:07 2019

@author: Analytics Team
"""

import nest_asyncio
import pandas as pd
import discord
client = discord.Client()

import requests
import json

from canvasapi import Canvas
nest_asyncio.apply()

# Canvas API URL
API_URL = "https://ubc.instructure.com/api/v1/search/all_courses"
# Canvas API key

API_KEY = "11224~Ax5Fr4jGE4Y3pUYr4OzOQ4PmHQdM2vZSuz6735u4Pw4zy255S4HdqfajGTyUmWIJ"
from nltk.corpus import wordnet as wn

# Courses based on interest, keyword is a list of strings
def interest(keywords):
    similarwords = []
    similarwords.extend(keywords)
    for keyword in keywords:
        synsets = wn.synsets(keyword)
        for synset in synsets:
            for item in synset.hypernyms():
                similarwords.extend(item.lemma_names())       
            for item in synset.hyponyms():
                list1 = (i for i in item.lemma_names() if i not in similarwords)  
                similarwords.extend(list1)
                list2 = (i for i in synset.lemma_names() if i not in similarwords)
                similarwords.extend(list2)
    print(similarwords)
    
    with open('C:/Users/Huy/ubc_course_calendar_data.csv') as file:
        data = pd.read_csv(file)
    description_list = list(data.loc[:,'COURSE_DESCRIPTION'])
    
    suggested_courses = [] 
    suggested_courses_id = []
    suggested_courses_prereq = []
    suggested_courses_des = []
    index = -1
    for description in description_list:
        index += 1
        count = 0
        for similarword in similarwords:
            try:
                if similarword in description:
                    count += 1
            except:
                continue
        if count > len(keywords) - 1 :
            if data.iloc[index,1] not in suggested_courses:
                suggested_courses.append(data.iloc[index,1])
                suggested_courses_id.append(data.iloc[index,4] + ' ' + data.iloc[index,5])
                suggested_courses_prereq.append(data.iloc[index,9])
                suggested_courses_des.append(data.iloc[index,2])
    suggestion = pd.DataFrame()
    suggestion['Suggested Courses'] = suggested_courses
    suggestion['Course ID'] = suggested_courses_id
    suggestion['Prerequisite'] = suggested_courses_prereq
    suggestion['Course Description'] = suggested_courses_des
    suggestion.to_csv('suggestion.csv')
    out = ''
    for i in range(0,6):
        try: 
            out = suggestion['Suggested Courses'][i].lower() + ", " + out
        except:
            continue
    return out + ' etc.'
# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)
def course_enrollment():
    user = canvas.get_user('self')
    courses = user.get_courses()
    output = []
    for course in courses:
        try:
            output.append(str(course))
        except:
            continue
    return output

# Course rating:
    
def rmp(professorname):
    class RateMyProfScraper:
            def __init__(self,schoolid):
                self.UniversityId = schoolid
                self.professorlist = self.createprofessorlist()
                self.indexnumber = False
    
            def createprofessorlist(self):#creates List object that include basic information on all Professors from the IDed University
                tempprofessorlist = []
                num_of_prof = self.GetNumOfProfessors(self.UniversityId)
                num_of_pages = math.ceil(num_of_prof / 20)
                i = 1
                while (i <= num_of_pages):# the loop insert all professor into list
                    page = requests.get("http://www.ratemyprofessors.com/filter/professor/?&page=" + str(
                        i) + "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                        self.UniversityId))
                    temp_jsonpage = json.loads(page.content)
                    temp_list = temp_jsonpage['professors']
                    tempprofessorlist.extend(temp_list)
                    i += 1
                return tempprofessorlist
    
            def GetNumOfProfessors(self,id):  # function returns the number of professors in the university of the given ID.
                page = requests.get(
                    "http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                        id))  # get request for page
                temp_jsonpage = json.loads(page.content)
                num_of_prof = temp_jsonpage[
                                  'remaining'] + 20  # get the number of professors at William Paterson University
                return num_of_prof
    
            def SearchProfessor(self, ProfessorName):
                self.indexnumber = self.GetProfessorIndex(ProfessorName)
                self.PrintProfessorInfo()
                return self.indexnumber
    
            def GetProfessorIndex(self,ProfessorName):  # function searches for professor in list
                for i in range(0, len(self.professorlist)):
                    if (ProfessorName == (self.professorlist[i]['tFname'] + " " + self.professorlist[i]['tLname'])):
                        return i
                return False  # Return False is not found
    
            def PrintProfessorInfo(self):  # print search professor's name and RMP score
                if self.indexnumber == False:
                    print("error")
                else:
                    print(self.professorlist[self.indexnumber])
    
            def PrintProfessorDetail(self,key):  # print search professor's name and RMP score
                if self.indexnumber == False:
                    print("professor not found")
                    return "professor not found"
                else:
                    print(self.professorlist[self.indexnumber][key])
                    return self.professorlist[self.indexnumber][key]
            
    
    Name = professorname
    UniversityofBritishColumbia = RateMyProfScraper(1413)
    UniversityofBritishColumbia.SearchProfessor(Name)
    a = UniversityofBritishColumbia.PrintProfessorDetail("overall_rating")
    return a


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    
@client.event
async def on_message(message):
    if message.content.startswith('disconnect bot'):
        await message.channel.send('bot disconnected')
        await client.close()
    elif message.content.startswith('Hello'):
        await message.channel.send('Hi!')
    elif message.content.startswith('get courses'):
        items = course_enrollment() 
        for item in items:
            await message.channel.send(item)
    elif message.content.startswith('interest:'):
        a = message.content[10:].split()
        examples = interest(a)
        name = 'suggestion_' + message.content[10:] + '.csv'
        file = discord.File(u"suggestion.csv", filename = name)
        await message.channel.send('Here are courses related to your interest:')
        await message.channel.send(examples)
        await message.channel.send('Please check with your advisor and student service center for more information', file = file)
    elif message.content.startswith('trend NURS 337 434'):
        file = discord.File(r'C:\Users\Huy\NURS 337 434.png', filename = 'NURS 337 434.png')
        await message.channel.send('', file = file)
    elif message.content.startswith('trend PATH 404 1'):
        file = discord.File(r'C:\Users\Huy\PATH 404 1.png', filename = 'PATH 404 1.png')
        await message.channel.send('', file = file)
    elif message.content.startswith('help'):
        await message.channel.send('You can type in: get courses, trend + course id, interest:, disconnect bot, rmp, etc.')
    elif message.content.startswith('rmp '):
        a = rmp(message.content[4:])
        await message.channel.send(a)
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to our Analytics server!')
token = 'NjQwMzEyNzAxNDgyMDQxMzU0.Xb5GxQ.FFYyQWPKL3-geub6nFGAKV1hKvw'



client.run(token)