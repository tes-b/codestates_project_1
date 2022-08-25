# Wikipedia Crawler Authored by Geek Yogurt 2022-08-25
"""
데이터 프레임 형태로 찾은 결측치가 채워져서 나옵니다.(shape 동일)
못찾은 것들은 'unknown'으로 표시됩니다.
Year 결과값은 string 타입 입니다.
찾는동안 찾은 결과들이 아래에 프린트됩니다.
마지막 줄에는 찾은개수(gotcha) 못찾은 개수(failed) 못찾은 인덱스 번호 (indexes) 가 출력됩니다.
"""
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import re
import wikipediaapi
    

class WikiCrawler:
    
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia('en', extract_format=wikipediaapi.ExtractFormat.WIKI);
        if self.wiki != NULL:
            print(self.wiki);
        
    def fill_all(self, data):
        
        rt_data = data.copy();
        gotcha = 0;
        failure = [];
        for index, row in rt_data.iterrows():            # get row
            dic_values = self.search_values(row.Name);   # search_values 함수 실행

            if (dic_values['result']): 
                # 성공적으로 받아왔으면 데이터프레임에 입력
                if 'Year' in rt_data.columns :
                    rt_data.loc[index,'Year'] = int(dic_values['year']);
                if 'Genre' in rt_data.columns :
                    rt_data.loc[index,'Genre'] = dic_values['genre'];
                if 'Publisher' in rt_data.columns :
                    rt_data.loc[index,'Publisher'] = dic_values['publisher'];
                gotcha += 1;
                print(index,"/",row.Name,"/",dic_values['year'],"/",dic_values['genre'],"/",dic_values['publisher']);
            else: 
                failure.append(index);
                print(index,"/",row.Name,"/",dic_values['msg']);
        
        # 결과 출력
        print("gotcha : ", gotcha);
        print("failed : ", len(failure),"\n indexes : ",failure);
        return rt_data;
     
    
    def search_values(self,name):
        """
        위키 문서 이름을 넣으면 데이터를 담은 dictionary를 반환합니다.
        """
        name_vg = name + " (video game)";   # (video game) 이름뒤에 추가
        page = self.wiki.page(name_vg);     # 위키에 검색
        url = "empty";
        dic_values = { 
                    'result' : False, 
                    'msg' : 'unknown',
                    'year':'unknown',
                    'genre': 'unknown',
                    'publisher': 'unknown'};
        
        if page.exists():                   # 페이지 존재 확인
            url = page.fullurl;             # url 
        else:                               
            page = self.wiki.page(name);    # 이름으로 위키 페이지 검색
            if page.exists():
                if 'game' in page.summary:           # 비디오 게임이 맞는지 확인
                    url = page.fullurl;         # url
                else : 
                    dic_values['msg'] = 'not a game...'
                    # dic_values['result'] = False;
            else: 
                dic_values['msg'] = 'page not exist'
                # dic_values['result'] = False;
            
        if url != "empty":
            response = requests.get(url);           # url로 html 페이지 가져오기
            if response :
                
                soup = bs(response.text, "html.parser");
                    
                tr = soup.find_all('tr')  # tr 태그 가져오기
                if tr :
                    for ele in tr:
                        if "Release" in ele.text: # 출시일
                            list_temp = re.findall(r'\d{4}', ele.text); # 년도
                            if list_temp:
                                dic_values['year'] = list_temp[0]; 
                                dic_values['result'] = True;
                        
                        if "Genre" in ele.text: # 장르
                            td = ele.find('td');
                            if td:
                                list_temp = list(td.stripped_strings); # td 태그 내용
                                if list_temp:
                                    dic_values['genre'] = list_temp[0]; 
                                    dic_values['result'] = True;
                        
                        if "Publisher" in ele.text: # 퍼블리셔
                            td = ele.find('td');
                            if td:
                                list_temp = list(td.stripped_strings); # td 태그 내용
                                if list_temp:
                                    dic_values['publisher'] = list_temp[0]; 
                                    dic_values['result'] = True;
                        
                        if (dic_values['year'] != "unknown") & (dic_values['genre'] != "unknown") & (dic_values['publisher'] != "unknown"):
                            break;  # 세가지 항목 채워지면 break;
                        
                else : dic_values['msg'] = 'cannot get the tr tag';        
                
            else : dic_values['msg'] = 'cannot get the page';
        # print(dic_values);
        return dic_values;
        
            
           
