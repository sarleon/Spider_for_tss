#coding:utf-8
import requests
import re
import os
import urllib

headers={'referer':'http://218.94.159.102/tss/en/c1025/assignment/uploadHomework?id=101',}
cookies=dict(JSESSIONID='D86092B07DCF7179571E06FAC3BD8C2D',
             __utma='71084115.1598426284.1459420135.1465092253.1465263402.57',
             __utmb='71084115',
             __utmc='71084115',
             __utmz='71084115.1459420135.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none)',
             course_order='0',
             slide_order='0')

#get the list of course
course_list_url="http://218.94.159.102/tss/en/home/courselist.html"



course_list_request=requests.get(url=course_list_url,cookies=cookies)
course_block_pattern=re.compile("<a href=\"/tss/en/c\d{4}/index\.html\">\s*.*\s*</a>")
course_list_string=course_block_pattern.findall(course_list_request.text)
course_list={}
course_string_pattern=re.compile("<a href=\"/tss/en/(c\d{4})/index\.html\">\s*(.*)\s*</a>")
for item in course_list_string:
    course_matcher=course_string_pattern.search(item)
    course_number=course_matcher.group(1)
    course_name= course_matcher.group(2).strip()
    course_list[course_number]=course_name

    #making directorys of course
    try:
        os.mkdir(course_name)
    except OSError:
        print "[mkdir]"+str(OSError)
    try:
            os.mkdir(course_name+"/"+course_number)
    except OSError:
        print "[mkdir]"+str(OSError)



    #downloading files
    base_file_url="http://218.94.159.102/tss/en/"+course_number+"/slide/viewSlides/"
    file_absloute_path="http://218.94.159.102"

    def download_files_recrucial(dir_url):
        dir_request=requests.get(url=dir_url,cookies=cookies)

        file_pattern=re.compile("<a href=\"/tss/en/"+course_number+"/slide/downloadSlides/(.*)\" target=\"_blank\">\s*(.*)\s*</a>")
        file_name_list=file_pattern.findall(dir_request.text)
        for file_item in file_name_list:

            temp1=file_item[0].strip().encode("gbk")
            temp2=urllib.unquote(temp1)
            temp3=temp2.decode("gbk")
            print temp3
            print type(temp3)
            file_url=file_absloute_path+"/tss/en/"+course_number+"/slide/downloadSlides/"+file_item[0]
            print "file_url"+file_url

            f=open(course_name+"/"+course_number+"/"+temp3,"wb")
            try:
                f.write(requests.get(url=file_url,cookies=cookies).content)
            except requests.ConnectionError:
                print requests.ConnectionError
            except requests.HTTPError:
                print  requests.HTTPError
        directory_pattern=re.compile("<a href=\"(/tss/en/c\d{4}/slide/viewSlides/.*)\" >")
        directory_matcher=directory_pattern.findall(dir_request.text)
        for dir_item in directory_matcher:
            if(len(file_absloute_path+dir_item)>len(dir_url)):

                dir_str=course_name+"/"+course_number+"/"+urllib.unquote(dir_item[31:dir_item.rfind("/")].strip().encode("gbk")).decode("gbk")

                print dir_str
                try:
                    os.mkdir(dir_str)
                except OSError:
                    print "[download]"+str(OSError)
                print "[dir_item]"+dir_item
                download_files_recrucial(file_absloute_path+dir_item)
    download_files_recrucial(base_file_url)
