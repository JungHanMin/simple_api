# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 10:13:17 2020

@author: 정한민
"""

import pymysql
import json
from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse


#====local_DB==========
db_host_ip = '127.0.0.1'
db_id = 'root'
db_password = '1234'
db_name = 'cloling_test'


#db 정보를 리턴하는 함수
def db_get_connect():
    db_account = pymysql.connect(host=db_host_ip, user=db_id, 
                       password=db_password, db=db_name, charset='utf8')
    # db_account_cursor = db_account.cursor()
    return db_account

#튜플데이터를, json 으로 변환
def db_tuple_change(select_tuple):
    payload = []
    content = {}
    for result in select_tuple:
        content = {'PLACE_ID': result[0], 'PLACE_NAME': result[1], 'PLACE_ADDR': result[2],'CATEGORY_1': result[3], 'CATEGORY_2': result[4],\
                   'PLACE_CODE': result[5], 'PLACE_TEL': result[6], 'PLACE_WEB': result[7], 'USE_TIME': result[8],'MENU': result[9],\
                   'CLOSED_DAY': result[10], 'PLACE_FEE': result[11], 'PLACE_COST': result[12], 'PLACE_INTRO': result[13],'PLACE_IMG': result[14]}
        payload.append(content)
        content = {}
    return payload

#db select
def db_select(sql_query):
    db_account = db_get_connect()
    db_account_cursor = db_account.cursor()

    # sql = "select * from place_info"
    # sql = "select * from place_info ORDER BY PLACE_ID DESC LIMIT 5"
    
    db_account_cursor.execute(sql_query)
    
    select_data = db_account_cursor.fetchall()
    
    db_account.commit()
    db_account.close()
    return select_data

def db_log_insert(logId, logType,logNow,logNext,logTime):
    db_account = db_get_connect()
    db_account_cursor = db_account.cursor()
    sql = "INSERT INTO user_log (LOG_ID, LOG_TYPE, LOG_NOW, LOG_NEXT, LOG_TIME)\
                            VALUES (%s, %s, %s, %s, %s)"
    
    #들어갈 데이타
    val = (logId,
            logType,
            logNow,
            logNext,
            logTime)
    
    db_account_cursor.execute(sql, val)
    db_account.commit()
    db_account.close()

#db insert
###############################
#테이블 이름 : user_info
###############################
def db_insert(userId, userType, userTime, placeInfo, userSex, userAge, snsId, snsType):
    db_account = db_get_connect()
    db_account_cursor = db_account.cursor()
    
    sql = "INSERT INTO user_info (USER_ID, USER_TYPE, USER_TIME, PLACE_INFO, USER_SEX, USER_AGE,\
                                SNS_ID, SNS_TYPE)\
                            VALUES (%s, %s, %s, %s, %s,\
                                    %s, %s, %s)"
                                
    #들어갈 데이타
    val = (userId,
            userType,
            userTime,
            placeInfo,
            userSex,
            userAge,
            snsId,
            snsType)
    
    db_account_cursor.execute(sql, val)
    db_account.commit()
    db_account.close()
         
app = Flask(__name__)
api = Api(app)

class Dabigtour(Resource):
    def get(self):
        #get 으로 받은 데이터를 받기 위해 RequestParser 선언한다.
        #값이 없으면 None 저장
        parser = reqparse.RequestParser()

        parser.add_argument('userId', None)
        parser.add_argument('userType', None)
        parser.add_argument('userTime', None)
        parser.add_argument('placeInfo', None)
        
        parser.add_argument('userSex', 'M')
        parser.add_argument('userAge', '0')
        parser.add_argument('snsId', None)
        parser.add_argument('snsType', None)
        args = parser.parse_args()
        
        userId = args['userId']
        userType = args['userType']
        userTime = args['userTime']
        placeInfo = args['placeInfo']
        
        userSex = args['userSex']
        userAge = args['userAge']
        snsId = args['snsId']
        snsType = args['snsType']
        
        print('## args ##',args)
        
        if userId != None and userType != None and userTime != None and placeInfo != None: 
        # insert
            db_insert(userId, userType, userTime, placeInfo, userSex, userAge, snsId, snsType)
            print('insert_success')
        else:
            return {'message':'param_error '}
        
        select_tuple_data = db_select('SELECT * FROM place_info ORDER BY PLACE_ID LIMIT 5')
        select_tuple_data2 = db_select('SELECT * FROM place_info ORDER BY PLACE_ID DESC LIMIT 5')
        # select_tuple_data = db_select()
        
        tuple_sum = select_tuple_data + select_tuple_data2
        get_tuple = db_tuple_change(tuple_sum)
        
        # get_tuple2 = db_tuple_change(select_tuple_data2)
        
        json_data = json.dumps(get_tuple, ensure_ascii=False, sort_keys=True, indent=4, default=str)
        return { 'data' : json_data }

class Dabiglog(Resource):
    def get(self):
        #get 으로 받은 데이터를 받기 위해 RequestParser 선언한다.
        #값이 없으면 None 저장
        state = 400
        success_string = 'success'
        message_string = 'userlog insert'
        
        parser = reqparse.RequestParser()
        parser.add_argument('logId', None)
        parser.add_argument('logType', None)
        parser.add_argument('logNow', None)
        parser.add_argument('logNext', None)
        parser.add_argument('logTime', None)
        
        args = parser.parse_args()

        logId = args['logId']
        logType = args['logType']
        logNow = args['logNow']
        logNext = args['logNext']
        logTime = args['logTime']
        
        print('## args ##',args)
        
        if logId != None and logType != None and logNow != None and logNext != None and logTime != None: 
        # insert
            state = 200
            success_string = 'success'
            message_string = 'userlog insert'
            db_log_insert(logId, logType,logNow,logNext,logTime)
            return { "data": { "login_success": success_string }, "status": { "code": state,"message": message_string } }
        else:
            state = 400
            success_string = 'fail'
            message_string = 'userlog insert fail'
            return { "data": { "login_success": success_string }, "status": { "code": state,"message": message_string } }
        
        
#테스트 URL
class TestServer(Resource):
    def get(self):
        return {'message':'살아있다.'}

# URL 이 추가될때 마다 클래스와 URL 을 하나씩 추가해준다.
api.add_resource(Dabigtour, '/recommendTour')
api.add_resource(Dabiglog, '/feedbackLog')

api.add_resource(TestServer, '/test')


#ip 와 port 를 변경 하는곳
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5837)