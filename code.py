#!/usr/bin/env python
# coding: utf-8
import web
import os
import urllib
import json
import xlwt
import StringIO
from config.settings import urls
from web import utils
from include.dnspod import dnspod
from include.writexls import writexls

web.config.debug = False

r = web.template.render(os.path.join(os.path.dirname(__file__), 'templates/'))

siteName = 'dnsapi'

header = r.header(siteName)

recordDomainName = {'www':'www','@':'@','*':'*'}

recordType = {'A':'A','CNNAME':'CNNAME','MX':'MX','TXT':'TXT','NS':'NS','AAAA':'AAAA'}

recordLineType = ['默认','电信','联通','教育网','百度','搜索引擎']

exportColums = {'is_mark':'星标','name':'域名','created_on':'创建时间','updated_on':'更新时间'}

exportRecordsColums = {'name':'主机记录','type':'记录类型','line':'线路类型','value':'记录值','ttl':'ttl'}

baseUrl = 'https://dnsapi.cn/'

userInfoApi = baseUrl + 'User.Detail' #用户信息
domainCreate = baseUrl + 'Domain.Create' #添加域名
domainList = baseUrl + 'Domain.List' #域名列表
domainDelete = baseUrl + 'Domain.Remove' #删除域名
domainRecordList = baseUrl + 'Record.List' #记录列表
domainRecordAdd = baseUrl + 'Record.Create'#添加记录
domainRecordDelete = baseUrl + 'Record.Remove'#删除记录

xlsExportPath = '/Users/jumei/test/'
xlsExportDomainListFileName = 'domain_list.xls'
xlsExportDomainRecordsFileName = 'domain_records_list.xls'




#登陆
class Login:
    def GET(self):
        loginPageChkLogin()
        i = web.input()
        errorMsg = ''
        if  i and int(i.error) == 1:
            errorMsg = errorMsgMethod('please check your email or password!')
        return r.login(errorMsg)
    def POST(self):
        i = web.input()
        if not i.email:
            return 'please check your email'
        if not i.pwd:
            return 'please check your password'
        else:

            api = dnspod(str(i.email),str(i.pwd),userInfoApi)
            returnData = api.apiPost()
            returnData = json.loads(returnData,encoding="utf8")
            if returnData['status']:
                if int(returnData['status']['code']) == 1:
                    session.login = True
                    session.email =  str(i.email)
                    session.pwd = str(i.pwd)
                    web.seeother('/list')
                else:
                    web.redirect('/login?error=1')

#域名列表
class List:
    def GET(self):
        domianListDict = dict()
        chkLogin()
        if session.get('login',False):
            email = session.get('email',False)
            pwd = session.get('pwd',False)

            errorMsg = ''
            successMsg = ''

            i = web.input()
            try:
                if i and  i.domainId:
                    api = dnspod(email,pwd,domainDelete,domain_id = i.domainId)
                    returnData = api.apiPost()
                    returnData = json.loads(returnData,encoding="utf8")
                    if returnData['status']:
                        if int(returnData['status']['code']) == 1:
                            web.redirect('/list?success=2')
            except:
                pass

            try:
                if i and  int(i.error) == 1:
                    errorMsg = errorMsgMethod('something error!')
            except:
                pass

            try:
                if i and  int(i.success) == 1:
                    successMsg = successMsgMethod('created domain succesed!')
                elif i and int(i.success) == 2:
                    successMsg = successMsgMethod('deleted domain succesed!')
            except:
                pass

            api = dnspod(email,pwd,domainList)
            returnData = api.apiPost()
            returnData = json.loads(returnData,encoding="utf8")
            if returnData['status']:
                if int(returnData['status']['code']) == 1:
                    domianListDict = returnData['domains']



            try:
                if i and i.export:
                    wxls = writexls()
                    filename = xlsExportPath+xlsExportDomainListFileName
                    rowsData = wxls.formateData(exportColums,domianListDict)
                    wxls.writeToExcel(filename,exportColums,rowsData)
            except:
                pass

            return r.list(header,errorMsg,successMsg,domianListDict)

#退出登陆
class Logout:
    def GET(self):
        session.kill()
        web.seeother('/login')


#添加域名
class AddDomian:
    def GET(self):
        chkLogin()
        a = ''
        return r.add(a,header)

    def POST(self):
        chkLogin()
        email = session.get('email',False)
        pwd = session.get('pwd',False)
        isMark = 'no'
        i = web.input()
        if  i.domain:
            if i.light:
                isMark ='yes'
            api = dnspod(email,pwd,domainCreate,domain=i.domain,is_mark=isMark)
            returnData = api.apiPost()
            returnData = json.loads(returnData,encoding="utf8")
            if returnData['status']:
                if int(returnData['status']['code']) == 1:
                    web.seeother('/list?success=1')
                else:
                    web.redirect('/add?error=1')
#域名记录列表
class Records:
    def GET(self):
        chkLogin()
        email = session.get('email',False)
        pwd = session.get('pwd',False)
        domainInfo = ''
        recordsInfo = ''
        successMsg = ''
        recordId = 0
        i = web.input()
        try:
            if i and i.domainId:
                api = dnspod(email,pwd,domainRecordList,domain_id=i.domainId)
                returnData = api.apiPost()
                returnData = json.loads(returnData,encoding="utf8")
                if returnData['status']:
                    if int(returnData['status']['code']) == 1:
                        domainInfo = returnData['domain']
                        recordsInfo = returnData['records']
        except:
            pass

        try:
            if i and i.recordId:
                recordId = i.recordId
                api = dnspod(email,pwd,domainRecordDelete,domain_id=i.domainId,record_id=recordId)
                returnData = api.apiPost()
                returnData = json.loads(returnData,encoding="utf8")
                if returnData['status']:
                    if int(returnData['status']['code']) == 1:
                        web.seeother("/records?domainId="+i.domainId+"&success=2")
        except:
            pass


        try:
            if i and i.success:
                successMsg = successMsgMethod('删除记录成功!')
        except:
            pass

        try:
            if i and i.export:
                wxls = writexls()
                filename = xlsExportPath+xlsExportDomainRecordsFileName
                rowsData = wxls.formateData(exportRecordsColums,recordsInfo)
                wxls.writeToExcel(filename,exportRecordsColums,rowsData)

        except:
            pass
        return r.records(header,domainInfo,recordsInfo,successMsg)

#添加域名记录
class RecordAdd:
    def GET(self):
        chkLogin()
        i = web.input()
        domainId = 0

        try:
            if i and i.domainId:
                domainId = i.domainId
        except:
            pass


        return r.record_add(header,recordDomainName,recordType,recordLineType,domainId)

    def POST(self):
        chkLogin()
        email = session.get('email',False)
        pwd = session.get('pwd',False)
        i = web.input()
        rdn = 'www'
        rtype = 'A'
        line = '默认'
        value = ''
        mx = 5
        ttl = 600
        domain_id = 0
        try:
            if i and i.domain_id:
                domain_id =  i.domain_id
        except:
            pass


        try:
            if i and i.rdn:
                rdn =  i.rdn
        except:
            pass

        try:
            if i and i.rtype:
                rtype = i.rtype
        except:
            pass

        try:
            if i and i.line:
                line = i.line
        except:
            pass

        try:
            if i and i.value:
                value = i.value
        except:
            pass


        try:
            if i and rtype == 'MX':
                if i and i.mx:
                    mx = i.mx
        except:
            pass

        try:
            if i and i.ttl:
                ttl = i.ttl
        except:
            pass

        if rtype == 'MX':
            api = dnspod(email,pwd,domainRecordAdd,domain_id=domain_id,sub_domain=rdn,record_type=rtype,record_line=line,value=value,ttl=ttl,mx=mx)
        else:
            api = dnspod(email,pwd,domainRecordAdd,domain_id=domain_id,sub_domain=rdn,record_type=rtype,record_line=line,value=value,ttl=ttl)

        returnData = api.apiPost()
        returnData = json.loads(returnData,encoding="utf8")
        if returnData['status']:
            if int(returnData['status']['code']) == 1:
                web.redirect("/records?domainId"+domain_id+"&success=1")
            else:
                web.redirect("/records?domainId"+domain_id+"&error=1")



def chkLogin():
    if not session.get('login',False):
        web.redirect('/login')


def loginPageChkLogin():
    if session.get('login',False):
        web.redirect('/list')


def errorMsgMethod(msg):
    return '<div class="alert alert-danger">'+msg+'</div>'

def successMsgMethod(msg):
    return '<div class="alert alert-success">'+msg+'</div>'




def isset(v):
    try:
        type(eval(v))
    except:
        return 0
    else:
        return 1


app = web.application(urls, globals())
curdir = os.path.dirname(__file__)
session = web.session.Session(app, web.session.DiskStore(curdir + '/' + 'sessions'),)
application = app.wsgifunc()


