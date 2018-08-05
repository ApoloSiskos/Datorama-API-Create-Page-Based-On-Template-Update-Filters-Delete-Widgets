import json
import requests

def authenticateUser(username, pwd):
    auth_url = 'https://app.datorama.com/services/auth/authenticate'
    headers = {'Content-Type': 'application/json'}
    datax = {"email": username,"password": pwd}
    authResponse = requests.post(auth_url, data = json.dumps(datax), headers=headers)
    return authResponse


def getDashboards(token,brandId):
    dash_url = 'https://app.datorama.com/services/admin/dashboard/findByBrand/{0}?fulldata=true'.format(brandId)
    dheaders = {'token':token}
    dashResponse = requests.get(dash_url,headers=dheaders)
    dashList = json.loads(dashResponse.text)
    returnList = {}
    for dash in dashList:
        returnList[dash['name']] = dash['id']
        page_url = 'https://app.datorama.com/services/admin/dashboard/page/find/dashboard/{0}'.format(dash['id'])
        pageResponse = requests.get(page_url,headers=dheaders)
        pageList = json.loads(pageResponse.text)    
    return returnList


def createPage(token,pageName,dashId):
    create_url = 'https://app.datorama.com/services/admin/dashboard/page/create'
    headers = {'token':token, 'Content-Type': 'application/json'}
    headerSimple = {'token':token}
    data = {"config":{"filter":{"date":{}}}}
    data["dashboardId"] = dashId #Brand
    data["name"] = pageName
    data["isPublished"] = "false"
    pageCreateResponse = requests.post(create_url,headers=headers,data=json.dumps(data))
    jsonResponse = json.loads(pageCreateResponse.text)
    pageId = jsonResponse['id']
    #Apply template
    templateresult = templateUse(token, templateId, pageId)
    #Update page filters
    getPageConf(token,pageId)
    return pageCreateResponse


def templateUse(token, templateId, pageId): 
    template_url = 'https://app.datorama.com/services/admin/dashboard/page/createfromtemplate?templatePageId=' + str(templateId) + '&pageId=' + str(pageId) + '&theme='#creates the request URL
    headers = {'token':token, 'Content-Type': 'application/json'}
    post_content = 'templatePageId=' + str(templateId) + '&pageId=' + str(pageId) + '&theme='
    return requests.post(template_url, headers=headers, data = post_content)


##UPDATE FUNCTION
def getPageConf(token,pageId):
    #[Get Page Configuration]
    get_url = 'https://app.datorama.com/services/admin/dashboard/page/getpageresponse/{0}'.format(pageId)
    headers = {'token':token, 'Content-Type': 'application/json'}
    headerSimple = {'token':token}    
    pageDetailsResponse = requests.get(get_url,headers=headers)
    jsonResponse = json.loads(pageDetailsResponse.text)
    

    #[Apply Page Changes]
    updatePageUrl = 'https://app.datorama.com/services/admin/dashboard/page/tryupdate'
    jsonResponse["pageDto"]["config"]["filter"]["date"]["dateRangeType"] = "CUSTOM"
    jsonResponse["pageDto"]["config"]["filter"]["date"]["startDate"] = "2017-01-01" #Start Date
    jsonResponse["pageDto"]["config"]["filter"]["date"]["endDate"] = "2018-02-28" #End Date
    if 'filterDims' not in jsonResponse:
        jsonResponse["pageDto"]["config"]["filter"]["filterDims"] = dict()
    if 'CAMPAIGN_KEY' in jsonResponse:
        jsonResponse["pageDto"]["config"]["filter"]["filterDims"]["CAMPAIGN_KEY"]["vals"] = list(["51392"]) #Campaign Keys
    if 'CAMPAIGN_KEY' not in jsonResponse:
        jsonResponse["pageDto"]["config"]["filter"]["filterDims"]["CAMPAIGN_KEY"] = dict()
        jsonResponse["pageDto"]["config"]["filter"]["filterDims"]["CAMPAIGN_KEY"]["vals"] = list(["51392"]) #Campaign Keys
    #Checks if data stream filters apply to the page
    if 'BRAND_DATA_SOURCE_INSTANCE' in jsonResponse:
        jsonResponse["pageDto"]["config"]["filter"]["filterDims"]["BRAND_DATA_SOURCE_INSTANCE"]["vals"] = list(["Random Data Stream"])
    if 'BRAND_DATA_SOURCE_INSTANCE' not in jsonResponse:
        jsonResponse["pageDto"]["config"]["filter"]["filterDims"]["BRAND_DATA_SOURCE_INSTANCE"] = dict()
        jsonResponse["pageDto"]["config"]["filter"]["filterDims"]["BRAND_DATA_SOURCE_INSTANCE"]["vals"] = list(["Random Data Stream"]) #Campaign Keys


    for i in jsonResponse["pageWidgets"]:
        print(i["widgetId"])
        print(i["name"])


    yyyy = json.dumps(jsonResponse["pageWidgets"])
    f = open('BBBBBB.txt','w')
    f.write(yyyy)
    f.close()


    #Remove non awareness boxes
    jsonResponse["pageWidgets"].pop(15)
    jsonResponse["pageWidgets"].pop(15) #16
    jsonResponse["pageWidgets"].pop(15) #17



    requests.post(updatePageUrl,headers=headers,data=json.dumps(jsonResponse["pageDto"]),params={'pageId':pageId})

    #[Apply Widget Changes]
    updateAll = 'https://app.datorama.com/services/admin/dashboard/page/widget/updateAll'

    widgetOnly = jsonResponse["pageWidgets"]
    xx = {'pageId':pageId, 'widgets':widgetOnly}

    datavals = json.dumps(xx)
    pageWidget = json.dumps(jsonResponse["pageWidgets"]) #PageWidgets for the Post Request
    response = requests.post(updateAll,headers=headers,data=datavals)
    return 


'''Main'''
pwdval = "Dontyoudare#69" #Add a valid password
userval = "not.not@not.com" #Add a valid email address

response = authenticateUser(userval,pwdval)
if response.status_code == 200:
    tokenresponse = json.loads(response.text)
    token = tokenresponse.get('token')
    dashboardList = getDashboards(token,'11839')  #Workspace ID
    targetDash = dashboardList['Test'] #Dashboard
    pageName = 'NTemp' #Campaign Name
    templateId = 1484102 #Template depending on the case
    brandId = 11839 #Workspace
    pageId = createPage(token, pageName, targetDash)
 


else:
    print('Boo')



