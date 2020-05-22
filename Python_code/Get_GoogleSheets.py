# -*- coding: utf-8 -*-
"""
Created on Wed May 20 14:00:57 2020

@author: alex.messina
"""
import pandas as pd
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
from df2gspread import df2gspread as d2g

#%%

def open_fds_from_google_sheet():
    spreadsheet_key = "1ZMTjYRMhaFI8j8c2kwXKMlmz02XYZqM0Ge8agov1g6g"
    
    scope = ['https://spreadsheets.google.com/feeds'] 
    ## credential from file
    #credentials = ServiceAccountCredentials.from_json_keyfile_name(maindir+'Python_code/Jupyter notebook/quickstart-1590008023256-4b34bad3d0b0.json', scope) 
    
    ## Hardcode credential
    cred_dict = {"type": "service_account",  "project_id": "quickstart-1590008023256",  "private_key_id": "4b34bad3d0b0e750f195e558a5a2a0fb9f366011",  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDV05fI5+1g+clF\nsUPqrvjCpIFcDSjFIw8LF+pClOZsA9sUFf/jv5waobjPYSfNic2PiATF3i4Rr4dO\nkATYIlweI1lyS95dk+OJi/5sPVNPGdhBbTTzCIq5YDnLbcux0dYB3H0LH4PCcyo1\n34prgaVx7du/xix0lfOQlCCvYygFtR/ffVIgTtiG+KssCqp91G9RT4NdB+DKmNUs\nslx7ZFCLn7LS6jzVJ7CCfAalCNe3Bq6uYdoyngDmd+kn3A+3KVydX01oZ+cHEfT0\nGsOskey6jO+iJb0I/3l17WyPBqczOwgrsx4MNqGw5LUxOUGgqkz0RWJmJPH83x6g\nvuucXf7RAgMBAAECggEALnPU1jcYeUhaovLTM+FGNpbhaXuMX2Nx6bGM2WEau92M\nkw0CddpTEfAPQ7IyIPNufl+I1emiLYJqDTW5b7DrPTrlvDBiQwcVV/TbVW1vM1CE\njBYq+h9hb8tJUvnr1holeWsKmUeD6tL1GRYSrq9QH3OSmVN2pe9Lph2gCioq8C4W\n70QS1fTc4G9f19KVgD5gXkQu5ADAFGsLchc0C5ewTKzqAux0aXBFdGjKWVwNTh5m\n1ZOgmcgFuiJLK3XW1MfIG33tZwbKnsIYp8vhL5LGP3aIZJZrNhZNaMiFa2UMfrjT\nk5KTx7MCcxBL7bJS7pKswmJ6oT+u+d7XzFEE4cG+PwKBgQDtYmPhz1NXSh2cP1XH\npbuaF4XbztlRUqrnpfBGzTu5vSN33N/+VhcarxUAqRj4Nq1jRRFabSuOW4wJFh6T\ndE/hwGOAvtUs7AOeGGWnsJOg5ht9yFMYRhGSbYBi8JZkv1vUu/Dn4wr9qnKAqDtk\nsej43hY8NWishO+EqhDukjHB6wKBgQDmmESeFevbC771Xtu39E1KH+UErtmpwx9V\nDDng6SGImrJynT42FVN5rsoTBsNeLmOdyAKqoT/uOFFYA42iMHG7wCaj7ZBJt24d\nbgrp2JcQNeud+SqivQ7xKdpv+bfQ0Z4NMYZUXQfSDe4+v475TIysz6/GFFs1JBz9\nmcbX2cjXMwKBgHEiTTwXVT7qwcXvoXAvGoPL5i3mHUhWv8D7ItJ7iZVyAO9lQxOx\n7/z1qGrSLGZPmL8Q8b5I/VMxakICWrwn2NJcoI+BY5OvP+Ie+oO68gDi6gM+b+vH\nqSRCL8f3pZWKZbezgpLhcCGJFF0g0H2jFMdXAP3c7nAaQxTVAJDS+AfVAoGBAIqV\nuq9zp0MHJSXcc5pzxbulvYL5/rCrJvp7FZHZKqEpr9N4MzpXyMpZxPJ4XxQMNyxN\nV2Tq8jweNqz5vbZa/Q+EZPSiQtQ63H/tcbumwusoLMnNRNV3YDKKH9CqONHUGPP+\n7qdnHdsdKjEl+SxU2DrHuvEFrOccJBw5vipdpfnHAoGAUKvylmT++IK0MZI15oxr\n8L2J1W98RIXGoZdLfpRQobkschUNnGY/iFSDLEQSbN5Y0Kw4zzpYPJIJV8pCBKkr\nGQCFXPlaMC+cAKZSVvzkKQ6yYDFcCu7617ZQ1qoJsCj9tluyNfg7SqlTKl9zj/tI\nLv8i2/rCpHnk6ulp5IsHeXs=\n-----END PRIVATE KEY-----\n",  "client_email": "google-sheets@quickstart-1590008023256.iam.gserviceaccount.com",  "client_id": "101700187155636285485",  "auth_uri": "https://accounts.google.com/o/oauth2/auth",  "token_uri": "https://oauth2.googleapis.com/token",  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/google-sheets%40quickstart-1590008023256.iam.gserviceaccount.com"} 
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict,scope)
    gc = gspread.authorize(credentials)
    ## Open spreadsheet
    book = gc.open_by_key(spreadsheet_key) 
    worksheet = book.worksheet("Form Responses 1") 
    table = worksheet.get_all_values()
    ##Convert table data into a dataframe 
    fds = pd.DataFrame(table[1:], columns=table[0]) 
    ##Convert number strings to floats and ints 
    fds = fds.apply(pd.to_numeric, errors='ignore') 
    ##Convert date strings to datetime format 
    fds['Timestamp'] = pd.to_datetime(fds['Timestamp'],infer_datetime_format=True) 
    fds['Date and Time'] = pd.to_datetime(fds['Date and Time'],infer_datetime_format=True) 
    ##show Field Data Sheet
    #print fds
    return fds

#fds = open_fds_from_google_sheet()

def open_2020_ClipsOffsets():
    ## Google Sheets params
    spreadsheet_key = "1U0UnBJrpMNEtDYctO2GW0fuobdc8vJfdLIWbvSr--ss"    
    scope = ['https://spreadsheets.google.com/feeds'] 
    
    ## Authorize Hardcoded credential
    cred_dict = {"type": "service_account",  "project_id": "quickstart-1590008023256",  "private_key_id": "4b34bad3d0b0e750f195e558a5a2a0fb9f366011",  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDV05fI5+1g+clF\nsUPqrvjCpIFcDSjFIw8LF+pClOZsA9sUFf/jv5waobjPYSfNic2PiATF3i4Rr4dO\nkATYIlweI1lyS95dk+OJi/5sPVNPGdhBbTTzCIq5YDnLbcux0dYB3H0LH4PCcyo1\n34prgaVx7du/xix0lfOQlCCvYygFtR/ffVIgTtiG+KssCqp91G9RT4NdB+DKmNUs\nslx7ZFCLn7LS6jzVJ7CCfAalCNe3Bq6uYdoyngDmd+kn3A+3KVydX01oZ+cHEfT0\nGsOskey6jO+iJb0I/3l17WyPBqczOwgrsx4MNqGw5LUxOUGgqkz0RWJmJPH83x6g\nvuucXf7RAgMBAAECggEALnPU1jcYeUhaovLTM+FGNpbhaXuMX2Nx6bGM2WEau92M\nkw0CddpTEfAPQ7IyIPNufl+I1emiLYJqDTW5b7DrPTrlvDBiQwcVV/TbVW1vM1CE\njBYq+h9hb8tJUvnr1holeWsKmUeD6tL1GRYSrq9QH3OSmVN2pe9Lph2gCioq8C4W\n70QS1fTc4G9f19KVgD5gXkQu5ADAFGsLchc0C5ewTKzqAux0aXBFdGjKWVwNTh5m\n1ZOgmcgFuiJLK3XW1MfIG33tZwbKnsIYp8vhL5LGP3aIZJZrNhZNaMiFa2UMfrjT\nk5KTx7MCcxBL7bJS7pKswmJ6oT+u+d7XzFEE4cG+PwKBgQDtYmPhz1NXSh2cP1XH\npbuaF4XbztlRUqrnpfBGzTu5vSN33N/+VhcarxUAqRj4Nq1jRRFabSuOW4wJFh6T\ndE/hwGOAvtUs7AOeGGWnsJOg5ht9yFMYRhGSbYBi8JZkv1vUu/Dn4wr9qnKAqDtk\nsej43hY8NWishO+EqhDukjHB6wKBgQDmmESeFevbC771Xtu39E1KH+UErtmpwx9V\nDDng6SGImrJynT42FVN5rsoTBsNeLmOdyAKqoT/uOFFYA42iMHG7wCaj7ZBJt24d\nbgrp2JcQNeud+SqivQ7xKdpv+bfQ0Z4NMYZUXQfSDe4+v475TIysz6/GFFs1JBz9\nmcbX2cjXMwKBgHEiTTwXVT7qwcXvoXAvGoPL5i3mHUhWv8D7ItJ7iZVyAO9lQxOx\n7/z1qGrSLGZPmL8Q8b5I/VMxakICWrwn2NJcoI+BY5OvP+Ie+oO68gDi6gM+b+vH\nqSRCL8f3pZWKZbezgpLhcCGJFF0g0H2jFMdXAP3c7nAaQxTVAJDS+AfVAoGBAIqV\nuq9zp0MHJSXcc5pzxbulvYL5/rCrJvp7FZHZKqEpr9N4MzpXyMpZxPJ4XxQMNyxN\nV2Tq8jweNqz5vbZa/Q+EZPSiQtQ63H/tcbumwusoLMnNRNV3YDKKH9CqONHUGPP+\n7qdnHdsdKjEl+SxU2DrHuvEFrOccJBw5vipdpfnHAoGAUKvylmT++IK0MZI15oxr\n8L2J1W98RIXGoZdLfpRQobkschUNnGY/iFSDLEQSbN5Y0Kw4zzpYPJIJV8pCBKkr\nGQCFXPlaMC+cAKZSVvzkKQ6yYDFcCu7617ZQ1qoJsCj9tluyNfg7SqlTKl9zj/tI\nLv8i2/rCpHnk6ulp5IsHeXs=\n-----END PRIVATE KEY-----\n",  "client_email": "google-sheets@quickstart-1590008023256.iam.gserviceaccount.com",  "client_id": "101700187155636285485",  "auth_uri": "https://accounts.google.com/o/oauth2/auth",  "token_uri": "https://oauth2.googleapis.com/token",  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/google-sheets%40quickstart-1590008023256.iam.gserviceaccount.com"}
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict,scope)
    gc = gspread.authorize(credentials)
    ## Open spreadsheet
    book = gc.open_by_key(spreadsheet_key) 
    
    ## Open Sheet - Special Offsets
    worksheet = book.worksheet("SpecialOffsets") 
    table = worksheet.get_all_values()
    ##Convert table data into a dataframe 
    spec_offsets = pd.DataFrame(table[1:], columns=table[0]) 
    spec_offsets.index = spec_offsets['Site']
    ##Convert number strings to floats and ints 
    spec_offsets = spec_offsets.apply(pd.to_numeric, errors='ignore')
    ## Special formatting
    spec_offsets['Start'] = pd.to_datetime(spec_offsets['Start'],infer_datetime_format=True) 
    spec_offsets['End'] = pd.to_datetime(spec_offsets['End'],infer_datetime_format=True) 
    
    ## Open Sheet - Global Offsets
    worksheet = book.worksheet("GlobalOffsets") 
    table = worksheet.get_all_values()
    ##Convert table data into a dataframe 
    glob_offsets = pd.DataFrame(table[1:], columns=table[0]) 
    glob_offsets.index = glob_offsets['Site']
    ##Convert number strings to floats and ints 
    glob_offsets = glob_offsets.apply(pd.to_numeric, errors='ignore')
    glob_offsets = pd.DataFrame(glob_offsets['GlobalOffset_in'])

    ## Open Sheet - Clip Bad Data
    worksheet = book.worksheet("ClipBadData") 
    table = worksheet.get_all_values()
    ##Convert table data into a dataframe 
    clips = pd.DataFrame(table[1:], columns=table[0]) 
    clips.index = clips['Site']
    ##Convert number strings to floats and ints 
    clips = clips.apply(pd.to_numeric, errors='ignore')
    ## Special formatting
    clips['Start'] = pd.to_datetime(clips['Start'],infer_datetime_format=True) 
    clips['End'] = pd.to_datetime(clips['End'],infer_datetime_format=True) 
    return spec_offsets, glob_offsets, clips

#spec_offsets, glob_offsets, clips = open_2020_ClipsOffsets()

def open_2020_FinalOffsets():
    ## Google Sheets params
    spreadsheet_key = "1U0UnBJrpMNEtDYctO2GW0fuobdc8vJfdLIWbvSr--ss"    
    scope = ['https://spreadsheets.google.com/feeds'] 
    
    ## Authorize Hardcoded credential
    cred_dict = {"type": "service_account",  "project_id": "quickstart-1590008023256",  "private_key_id": "4b34bad3d0b0e750f195e558a5a2a0fb9f366011",  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDV05fI5+1g+clF\nsUPqrvjCpIFcDSjFIw8LF+pClOZsA9sUFf/jv5waobjPYSfNic2PiATF3i4Rr4dO\nkATYIlweI1lyS95dk+OJi/5sPVNPGdhBbTTzCIq5YDnLbcux0dYB3H0LH4PCcyo1\n34prgaVx7du/xix0lfOQlCCvYygFtR/ffVIgTtiG+KssCqp91G9RT4NdB+DKmNUs\nslx7ZFCLn7LS6jzVJ7CCfAalCNe3Bq6uYdoyngDmd+kn3A+3KVydX01oZ+cHEfT0\nGsOskey6jO+iJb0I/3l17WyPBqczOwgrsx4MNqGw5LUxOUGgqkz0RWJmJPH83x6g\nvuucXf7RAgMBAAECggEALnPU1jcYeUhaovLTM+FGNpbhaXuMX2Nx6bGM2WEau92M\nkw0CddpTEfAPQ7IyIPNufl+I1emiLYJqDTW5b7DrPTrlvDBiQwcVV/TbVW1vM1CE\njBYq+h9hb8tJUvnr1holeWsKmUeD6tL1GRYSrq9QH3OSmVN2pe9Lph2gCioq8C4W\n70QS1fTc4G9f19KVgD5gXkQu5ADAFGsLchc0C5ewTKzqAux0aXBFdGjKWVwNTh5m\n1ZOgmcgFuiJLK3XW1MfIG33tZwbKnsIYp8vhL5LGP3aIZJZrNhZNaMiFa2UMfrjT\nk5KTx7MCcxBL7bJS7pKswmJ6oT+u+d7XzFEE4cG+PwKBgQDtYmPhz1NXSh2cP1XH\npbuaF4XbztlRUqrnpfBGzTu5vSN33N/+VhcarxUAqRj4Nq1jRRFabSuOW4wJFh6T\ndE/hwGOAvtUs7AOeGGWnsJOg5ht9yFMYRhGSbYBi8JZkv1vUu/Dn4wr9qnKAqDtk\nsej43hY8NWishO+EqhDukjHB6wKBgQDmmESeFevbC771Xtu39E1KH+UErtmpwx9V\nDDng6SGImrJynT42FVN5rsoTBsNeLmOdyAKqoT/uOFFYA42iMHG7wCaj7ZBJt24d\nbgrp2JcQNeud+SqivQ7xKdpv+bfQ0Z4NMYZUXQfSDe4+v475TIysz6/GFFs1JBz9\nmcbX2cjXMwKBgHEiTTwXVT7qwcXvoXAvGoPL5i3mHUhWv8D7ItJ7iZVyAO9lQxOx\n7/z1qGrSLGZPmL8Q8b5I/VMxakICWrwn2NJcoI+BY5OvP+Ie+oO68gDi6gM+b+vH\nqSRCL8f3pZWKZbezgpLhcCGJFF0g0H2jFMdXAP3c7nAaQxTVAJDS+AfVAoGBAIqV\nuq9zp0MHJSXcc5pzxbulvYL5/rCrJvp7FZHZKqEpr9N4MzpXyMpZxPJ4XxQMNyxN\nV2Tq8jweNqz5vbZa/Q+EZPSiQtQ63H/tcbumwusoLMnNRNV3YDKKH9CqONHUGPP+\n7qdnHdsdKjEl+SxU2DrHuvEFrOccJBw5vipdpfnHAoGAUKvylmT++IK0MZI15oxr\n8L2J1W98RIXGoZdLfpRQobkschUNnGY/iFSDLEQSbN5Y0Kw4zzpYPJIJV8pCBKkr\nGQCFXPlaMC+cAKZSVvzkKQ6yYDFcCu7617ZQ1qoJsCj9tluyNfg7SqlTKl9zj/tI\nLv8i2/rCpHnk6ulp5IsHeXs=\n-----END PRIVATE KEY-----\n",  "client_email": "google-sheets@quickstart-1590008023256.iam.gserviceaccount.com",  "client_id": "101700187155636285485",  "auth_uri": "https://accounts.google.com/o/oauth2/auth",  "token_uri": "https://oauth2.googleapis.com/token",  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/google-sheets%40quickstart-1590008023256.iam.gserviceaccount.com"}
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict,scope)
    gc = gspread.authorize(credentials)
    ## Open spreadsheet
    book = gc.open_by_key(spreadsheet_key) 
    
    ## Open Sheet - Special Offsets
    worksheet = book.worksheet("FinalOffsets") 
    table = worksheet.get_all_values()
    ##Convert table data into a dataframe 
    fin_offsets = pd.DataFrame(table[1:], columns=table[0]) 
    fin_offsets.index = fin_offsets['Site']
    ##Convert number strings to floats and ints 
    fin_offsets = fin_offsets.apply(pd.to_numeric, errors='ignore')
    return fin_offsets[['CalculatedOffset_in','GlobalOffset_in','FinalOffset_in']]

#fin_offsets = open_2020_FinalOffsets()
#print fin_offsets

def open_HvF_90degweir():
    ## Google Sheets params
    spreadsheet_key = "1-JCewTSGX1YDoHi_xC35Y29e-YrOArfZwwUn7wB8IWc"    
    scope = ['https://spreadsheets.google.com/feeds'] 
    ## Authorize Hardcoded credential
    cred_dict = {"type": "service_account",  "project_id": "quickstart-1590008023256",  "private_key_id": "4b34bad3d0b0e750f195e558a5a2a0fb9f366011",  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDV05fI5+1g+clF\nsUPqrvjCpIFcDSjFIw8LF+pClOZsA9sUFf/jv5waobjPYSfNic2PiATF3i4Rr4dO\nkATYIlweI1lyS95dk+OJi/5sPVNPGdhBbTTzCIq5YDnLbcux0dYB3H0LH4PCcyo1\n34prgaVx7du/xix0lfOQlCCvYygFtR/ffVIgTtiG+KssCqp91G9RT4NdB+DKmNUs\nslx7ZFCLn7LS6jzVJ7CCfAalCNe3Bq6uYdoyngDmd+kn3A+3KVydX01oZ+cHEfT0\nGsOskey6jO+iJb0I/3l17WyPBqczOwgrsx4MNqGw5LUxOUGgqkz0RWJmJPH83x6g\nvuucXf7RAgMBAAECggEALnPU1jcYeUhaovLTM+FGNpbhaXuMX2Nx6bGM2WEau92M\nkw0CddpTEfAPQ7IyIPNufl+I1emiLYJqDTW5b7DrPTrlvDBiQwcVV/TbVW1vM1CE\njBYq+h9hb8tJUvnr1holeWsKmUeD6tL1GRYSrq9QH3OSmVN2pe9Lph2gCioq8C4W\n70QS1fTc4G9f19KVgD5gXkQu5ADAFGsLchc0C5ewTKzqAux0aXBFdGjKWVwNTh5m\n1ZOgmcgFuiJLK3XW1MfIG33tZwbKnsIYp8vhL5LGP3aIZJZrNhZNaMiFa2UMfrjT\nk5KTx7MCcxBL7bJS7pKswmJ6oT+u+d7XzFEE4cG+PwKBgQDtYmPhz1NXSh2cP1XH\npbuaF4XbztlRUqrnpfBGzTu5vSN33N/+VhcarxUAqRj4Nq1jRRFabSuOW4wJFh6T\ndE/hwGOAvtUs7AOeGGWnsJOg5ht9yFMYRhGSbYBi8JZkv1vUu/Dn4wr9qnKAqDtk\nsej43hY8NWishO+EqhDukjHB6wKBgQDmmESeFevbC771Xtu39E1KH+UErtmpwx9V\nDDng6SGImrJynT42FVN5rsoTBsNeLmOdyAKqoT/uOFFYA42iMHG7wCaj7ZBJt24d\nbgrp2JcQNeud+SqivQ7xKdpv+bfQ0Z4NMYZUXQfSDe4+v475TIysz6/GFFs1JBz9\nmcbX2cjXMwKBgHEiTTwXVT7qwcXvoXAvGoPL5i3mHUhWv8D7ItJ7iZVyAO9lQxOx\n7/z1qGrSLGZPmL8Q8b5I/VMxakICWrwn2NJcoI+BY5OvP+Ie+oO68gDi6gM+b+vH\nqSRCL8f3pZWKZbezgpLhcCGJFF0g0H2jFMdXAP3c7nAaQxTVAJDS+AfVAoGBAIqV\nuq9zp0MHJSXcc5pzxbulvYL5/rCrJvp7FZHZKqEpr9N4MzpXyMpZxPJ4XxQMNyxN\nV2Tq8jweNqz5vbZa/Q+EZPSiQtQ63H/tcbumwusoLMnNRNV3YDKKH9CqONHUGPP+\n7qdnHdsdKjEl+SxU2DrHuvEFrOccJBw5vipdpfnHAoGAUKvylmT++IK0MZI15oxr\n8L2J1W98RIXGoZdLfpRQobkschUNnGY/iFSDLEQSbN5Y0Kw4zzpYPJIJV8pCBKkr\nGQCFXPlaMC+cAKZSVvzkKQ6yYDFcCu7617ZQ1qoJsCj9tluyNfg7SqlTKl9zj/tI\nLv8i2/rCpHnk6ulp5IsHeXs=\n-----END PRIVATE KEY-----\n",  "client_email": "google-sheets@quickstart-1590008023256.iam.gserviceaccount.com",  "client_id": "101700187155636285485",  "auth_uri": "https://accounts.google.com/o/oauth2/auth",  "token_uri": "https://oauth2.googleapis.com/token",  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/google-sheets%40quickstart-1590008023256.iam.gserviceaccount.com"}
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict,scope)
    gc = gspread.authorize(credentials)
    ## Open spreadsheet
    book = gc.open_by_key(spreadsheet_key) 
    ## Open Sheet - Manual Offsets
    worksheet = book.worksheet("HvF-90degweir") 
    table = worksheet.get_all_values()
    ##Convert table data into a dataframe 
    HvF = pd.DataFrame(table[1:], columns=table[0]) 
    HvF.index = HvF['Level (in)']
    ##Convert number strings to floats and ints 
    HvF = HvF.apply(pd.to_numeric, errors='ignore')
    return pd.DataFrame(HvF['Q (GPM)'])


#HvF = open_HvF_90degweir()

def open_weir_dims():
    ## Google Sheets params
    spreadsheet_key = "1-JCewTSGX1YDoHi_xC35Y29e-YrOArfZwwUn7wB8IWc"    
    scope = ['https://spreadsheets.google.com/feeds'] 
    ## Authorize Hardcoded credential
    cred_dict = {"type": "service_account",  "project_id": "quickstart-1590008023256",  "private_key_id": "4b34bad3d0b0e750f195e558a5a2a0fb9f366011",  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDV05fI5+1g+clF\nsUPqrvjCpIFcDSjFIw8LF+pClOZsA9sUFf/jv5waobjPYSfNic2PiATF3i4Rr4dO\nkATYIlweI1lyS95dk+OJi/5sPVNPGdhBbTTzCIq5YDnLbcux0dYB3H0LH4PCcyo1\n34prgaVx7du/xix0lfOQlCCvYygFtR/ffVIgTtiG+KssCqp91G9RT4NdB+DKmNUs\nslx7ZFCLn7LS6jzVJ7CCfAalCNe3Bq6uYdoyngDmd+kn3A+3KVydX01oZ+cHEfT0\nGsOskey6jO+iJb0I/3l17WyPBqczOwgrsx4MNqGw5LUxOUGgqkz0RWJmJPH83x6g\nvuucXf7RAgMBAAECggEALnPU1jcYeUhaovLTM+FGNpbhaXuMX2Nx6bGM2WEau92M\nkw0CddpTEfAPQ7IyIPNufl+I1emiLYJqDTW5b7DrPTrlvDBiQwcVV/TbVW1vM1CE\njBYq+h9hb8tJUvnr1holeWsKmUeD6tL1GRYSrq9QH3OSmVN2pe9Lph2gCioq8C4W\n70QS1fTc4G9f19KVgD5gXkQu5ADAFGsLchc0C5ewTKzqAux0aXBFdGjKWVwNTh5m\n1ZOgmcgFuiJLK3XW1MfIG33tZwbKnsIYp8vhL5LGP3aIZJZrNhZNaMiFa2UMfrjT\nk5KTx7MCcxBL7bJS7pKswmJ6oT+u+d7XzFEE4cG+PwKBgQDtYmPhz1NXSh2cP1XH\npbuaF4XbztlRUqrnpfBGzTu5vSN33N/+VhcarxUAqRj4Nq1jRRFabSuOW4wJFh6T\ndE/hwGOAvtUs7AOeGGWnsJOg5ht9yFMYRhGSbYBi8JZkv1vUu/Dn4wr9qnKAqDtk\nsej43hY8NWishO+EqhDukjHB6wKBgQDmmESeFevbC771Xtu39E1KH+UErtmpwx9V\nDDng6SGImrJynT42FVN5rsoTBsNeLmOdyAKqoT/uOFFYA42iMHG7wCaj7ZBJt24d\nbgrp2JcQNeud+SqivQ7xKdpv+bfQ0Z4NMYZUXQfSDe4+v475TIysz6/GFFs1JBz9\nmcbX2cjXMwKBgHEiTTwXVT7qwcXvoXAvGoPL5i3mHUhWv8D7ItJ7iZVyAO9lQxOx\n7/z1qGrSLGZPmL8Q8b5I/VMxakICWrwn2NJcoI+BY5OvP+Ie+oO68gDi6gM+b+vH\nqSRCL8f3pZWKZbezgpLhcCGJFF0g0H2jFMdXAP3c7nAaQxTVAJDS+AfVAoGBAIqV\nuq9zp0MHJSXcc5pzxbulvYL5/rCrJvp7FZHZKqEpr9N4MzpXyMpZxPJ4XxQMNyxN\nV2Tq8jweNqz5vbZa/Q+EZPSiQtQ63H/tcbumwusoLMnNRNV3YDKKH9CqONHUGPP+\n7qdnHdsdKjEl+SxU2DrHuvEFrOccJBw5vipdpfnHAoGAUKvylmT++IK0MZI15oxr\n8L2J1W98RIXGoZdLfpRQobkschUNnGY/iFSDLEQSbN5Y0Kw4zzpYPJIJV8pCBKkr\nGQCFXPlaMC+cAKZSVvzkKQ6yYDFcCu7617ZQ1qoJsCj9tluyNfg7SqlTKl9zj/tI\nLv8i2/rCpHnk6ulp5IsHeXs=\n-----END PRIVATE KEY-----\n",  "client_email": "google-sheets@quickstart-1590008023256.iam.gserviceaccount.com",  "client_id": "101700187155636285485",  "auth_uri": "https://accounts.google.com/o/oauth2/auth",  "token_uri": "https://oauth2.googleapis.com/token",  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/google-sheets%40quickstart-1590008023256.iam.gserviceaccount.com"}
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict,scope)
    gc = gspread.authorize(credentials)
    ## Open spreadsheet
    book = gc.open_by_key(spreadsheet_key) 
    ## Open Sheet - Manual Offsets
    worksheet = book.worksheet("WeirDims2020") 
    table = worksheet.get_all_values()
    ##Convert table data into a dataframe 
    df = pd.DataFrame(table[2:], columns=table[1]) 
    df.index = df['Site']
    ##Convert number strings to floats and ints 
    df = df.apply(pd.to_numeric, errors='ignore')
    return df
#weir_dims = open_weir_dims()    
#print weir_dims

#%%

def save_df_to_GoogleSheets(df, spreadsheet_key, worksheet_name):
    cred_dict = {"type": "service_account",  "project_id": "quickstart-1590008023256",  "private_key_id": "4b34bad3d0b0e750f195e558a5a2a0fb9f366011",  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDV05fI5+1g+clF\nsUPqrvjCpIFcDSjFIw8LF+pClOZsA9sUFf/jv5waobjPYSfNic2PiATF3i4Rr4dO\nkATYIlweI1lyS95dk+OJi/5sPVNPGdhBbTTzCIq5YDnLbcux0dYB3H0LH4PCcyo1\n34prgaVx7du/xix0lfOQlCCvYygFtR/ffVIgTtiG+KssCqp91G9RT4NdB+DKmNUs\nslx7ZFCLn7LS6jzVJ7CCfAalCNe3Bq6uYdoyngDmd+kn3A+3KVydX01oZ+cHEfT0\nGsOskey6jO+iJb0I/3l17WyPBqczOwgrsx4MNqGw5LUxOUGgqkz0RWJmJPH83x6g\nvuucXf7RAgMBAAECggEALnPU1jcYeUhaovLTM+FGNpbhaXuMX2Nx6bGM2WEau92M\nkw0CddpTEfAPQ7IyIPNufl+I1emiLYJqDTW5b7DrPTrlvDBiQwcVV/TbVW1vM1CE\njBYq+h9hb8tJUvnr1holeWsKmUeD6tL1GRYSrq9QH3OSmVN2pe9Lph2gCioq8C4W\n70QS1fTc4G9f19KVgD5gXkQu5ADAFGsLchc0C5ewTKzqAux0aXBFdGjKWVwNTh5m\n1ZOgmcgFuiJLK3XW1MfIG33tZwbKnsIYp8vhL5LGP3aIZJZrNhZNaMiFa2UMfrjT\nk5KTx7MCcxBL7bJS7pKswmJ6oT+u+d7XzFEE4cG+PwKBgQDtYmPhz1NXSh2cP1XH\npbuaF4XbztlRUqrnpfBGzTu5vSN33N/+VhcarxUAqRj4Nq1jRRFabSuOW4wJFh6T\ndE/hwGOAvtUs7AOeGGWnsJOg5ht9yFMYRhGSbYBi8JZkv1vUu/Dn4wr9qnKAqDtk\nsej43hY8NWishO+EqhDukjHB6wKBgQDmmESeFevbC771Xtu39E1KH+UErtmpwx9V\nDDng6SGImrJynT42FVN5rsoTBsNeLmOdyAKqoT/uOFFYA42iMHG7wCaj7ZBJt24d\nbgrp2JcQNeud+SqivQ7xKdpv+bfQ0Z4NMYZUXQfSDe4+v475TIysz6/GFFs1JBz9\nmcbX2cjXMwKBgHEiTTwXVT7qwcXvoXAvGoPL5i3mHUhWv8D7ItJ7iZVyAO9lQxOx\n7/z1qGrSLGZPmL8Q8b5I/VMxakICWrwn2NJcoI+BY5OvP+Ie+oO68gDi6gM+b+vH\nqSRCL8f3pZWKZbezgpLhcCGJFF0g0H2jFMdXAP3c7nAaQxTVAJDS+AfVAoGBAIqV\nuq9zp0MHJSXcc5pzxbulvYL5/rCrJvp7FZHZKqEpr9N4MzpXyMpZxPJ4XxQMNyxN\nV2Tq8jweNqz5vbZa/Q+EZPSiQtQ63H/tcbumwusoLMnNRNV3YDKKH9CqONHUGPP+\n7qdnHdsdKjEl+SxU2DrHuvEFrOccJBw5vipdpfnHAoGAUKvylmT++IK0MZI15oxr\n8L2J1W98RIXGoZdLfpRQobkschUNnGY/iFSDLEQSbN5Y0Kw4zzpYPJIJV8pCBKkr\nGQCFXPlaMC+cAKZSVvzkKQ6yYDFcCu7617ZQ1qoJsCj9tluyNfg7SqlTKl9zj/tI\nLv8i2/rCpHnk6ulp5IsHeXs=\n-----END PRIVATE KEY-----\n",  "client_email": "google-sheets@quickstart-1590008023256.iam.gserviceaccount.com",  "client_id": "101700187155636285485",  "auth_uri": "https://accounts.google.com/o/oauth2/auth",  "token_uri": "https://oauth2.googleapis.com/token",  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/google-sheets%40quickstart-1590008023256.iam.gserviceaccount.com"}
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict,scope)
    d2g.upload(df,spreadsheet_key, worksheet_name, credentials=credentials,col_names=True,start_cell='A1',clean=False)
    return 'spreadsheet uploaded'

#save_df_to_GoogleSheets(fin_offsets, "1U0UnBJrpMNEtDYctO2GW0fuobdc8vJfdLIWbvSr--ss", 'FinalOffsets')   

#%%

