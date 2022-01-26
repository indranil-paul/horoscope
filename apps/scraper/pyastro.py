#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# pyastro - Webscrape www.ganeshaspeaks.com website to fetch data
# 
# NOTE: This webscraping process is done absolutely unofficially and purely  
# for the sake of application development only. NO commercial intensions are 
# there behind this development work.
#
# The MIT License (MIT)
# Copyright (c) 2018 Indranil Paul
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE
#

import json
import requests
from bs4 import BeautifulSoup


class Pyastro(object):
    '''
    This class uses HTTP GET method to fetch HTML data from www.ganeshaspeaks.com website,
    then parses the raw HTML to find out actual horoscope data placed within it.

    Attributes: 
        sign        -> (str): Get or Set sign attribute
        frequency   -> (str): Get or set frequency attribute
        horoscope   -> (str): Get the horoscope data
        sunsigns    -> (str): Get the list of all available sunsigns
        timeframes  -> (str): Get the list of all available frequency values
        
    Usage: 
        Method 1:
            obj = Pyastro('cancer', 'today')
            print(obj.horoscope)
        Method 2:
            obj = Pyastro()
            obj.sign = 'cancer'
            obj.frequency = 'today'
            print(obj.horoscope)
    '''
    
    def __init__(self, _sign = None, _freq = None, _json_filepath = None):
        '''
        Initializes the constants and other attributes
        '''
        if not _json_filepath:
            raise Exception('Input zodiac.json file not found!')

        self.__end_point = "https://www.ganeshaspeaks.com/horoscopes"
        self.__content_div_id = "test"
        self.__sunsigns = []
        self.__timeframes = ["yesterday", "today", "tomorrow", "weekly", "monthly", "yearly"]
        self.__timeframes_dict = {
            "yesterday": "yesterday-horoscope",
            "today" : "daily-horoscope",
            "tomorrow" : "tomorrow-horoscope",            
            "weekly": "weekly-horoscope",
            "monthly": "monthly-horoscope",
            "yearly": "yearly-horoscope"            
        }
        self.__load_data_from_json(_json_filepath)
        self.__sign = None
        self.__freq = None
        
        if _sign and _freq:
            self.sign = _sign
            self.frequency = _freq

    
    def __load_data_from_json(self, _json_filepath):
        try:
            with open(_json_filepath) as zodiac_file:
                self.__zodiac_dict = json.load(zodiac_file)

                for zdc in self.__zodiac_dict['zodiac_signs']:
                    self.__sunsigns.append(zdc['name'].lower())

        except Exception as e:
            raise Exception(f'Failed to load {_json_filepath} due to {e}')

        
    def __str__(self):
        '''
        Returns the static API Endpoint
        '''
        return self.__end_point
    
    
    @property
    def sunsigns(self):
        '''
        Returns all the available sunsigns
        '''
        return ', '.join(self.__sunsigns)
    
    
    @property
    def zodiac_details(self):
        '''
        Returns all the Zodiac Dictionary
        '''
        return self.__zodiac_dict['zodiac_signs']

    
    @property
    def timeframes(self):
        '''
        Returns all the available frequency values
        '''
        return ', '.join(self.__timeframes)
    
    
    @property
    def sign(self):
        '''
        Returns the sign attribute
        '''
        return self.__sign
    
    
    @property
    def frequency(self):
        '''
        Returns the frequency attribute
        '''
        return self.__freq
    
    
    @sign.setter
    def sign(self, _sign):
        '''
        Sets the sign attribute
        '''
        if isinstance(_sign, str):   
            if _sign.strip().lower() in self.__sunsigns:
                self.__sign = _sign.strip().capitalize()
            else:
                raise Exception(f'Frequency name {_sign} is not found!')
        else:
            raise TypeError('Sign names should be in String format')
        
        
    @frequency.setter
    def frequency(self, _freq):
        '''
        Sets the frequency attribute
        '''
        if isinstance(_freq, str):   
            if _freq.strip().lower() in self.__timeframes:
                self.__freq = self.__timeframes_dict.get(_freq.strip().lower(), 'None')
                if not self.__freq:
                    raise Exception(f'Frequency name {_freq} is not found!')
            else:
                raise Exception(f'Frequency name {_freq} is not found!')
        else:
            raise TypeError('Frequency names should be in String format')
            
    
    @property     
    def __get_url(self):
        '''
        Sets the URL by using endpoint, frequency & sign
        E.g.: "https://www.ganeshaspeaks.com/horoscopes/yearly-horoscope/cancer/"
        '''        
        return f"{self.__end_point}/{self.__freq}/{self.__sign}"
                
    
    def __scrape_site(self):
        '''
        Scrape the website to reach to the particular DIV where the
        horoscope data is placed in the HTML, and returns it back
        '''
        try:
            _url = self.__get_url
           
            response = requests.get(_url)
            status_code = response.status_code
            
            horoscope_data = None
            
            if status_code == 200:
                raw_site_data = response.content
                soup = BeautifulSoup(raw_site_data, 'html.parser')
                
                data_div = soup.find("div", {"id": self.__content_div_id})
                if data_div:
                    all_horoscope_data = list(str(data_div.text).split('\n'))
                    
                    for row in all_horoscope_data:
                        if self.__sign in row:
                            horoscope_data = row.split('=>')[1].strip()
                            break
                else:
                    raise Exception(f"DIV Id {self.__content_div_id} is not found!")
            else:
                raise Exception(f"Failed to fetch data from website {status_code}")
            
            if not horoscope_data:
                raise Exception(f"No horoscope found for the given sign {self.__sign}")
            
            return horoscope_data
        except Exception as e:
            raise Exception(e)
        

    @property
    def horoscope(self):
        '''
        Returns the horoscope data
        '''
        try:
            if self.__sign and self.__freq:
                horoscope_data = self.__scrape_site()
                return horoscope_data
            else:
                raise Exception('Sign & Frequency are not set properly!')
        except Exception as e:
            raise Exception(f'horoscope: {e}')
