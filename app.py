# coding: utf-8
#遗留问题：IP会变：54.193.59.55


from datetime import datetime
import json
from flask import Flask,redirect
from flask import render_template
from flask_sockets import Sockets
import random
from views.todos import todos_view
from flask import request
import leancloud
import requests

leancloud.init("96Q4GMOz0VpK4JwfeUjEHNWC-MdYXbMMI", "aCAfwt702pPeubx6tnngUWiu")


clickList = {}
app = Flask(__name__)
sockets = Sockets(app)
# 动态路由
app.register_blueprint(todos_view, url_prefix='/todos')


class AndroidId(leancloud.Object):
    pass


class AndroidIdRepeat(leancloud.Object):
    pass


class PostTest(leancloud.Object):
    pass


class CloudControl(leancloud.Object):
    pass


class ClickRecord(leancloud.Object):
    pass


class AffiliateSetting(leancloud.Object):
    pass


@app.route('/', methods=["GET", "POST"])
def index():
    # 获取IP
    headers = request.headers
    ip = headers.get('X-Forwarded-For')
    #ip = '192.168.1.1'
    ua = request.user_agent
    clickRecord = ClickRecord()
    if request.method == "GET":
        args = request.args
        offer_id = args.get("offer_id")
        affiliate_id = args.get("affiliate_id")
        transaction_id = args.get("transaction_id")
        sub_id = args.get("sub_id")
        clickInfo = {"offer_id": offer_id, "affiliate_id": affiliate_id, "transaction_id": transaction_id,
                     "sub_id": sub_id, "time": datetime.today()}
        clickList[ip + '|' + ua] = clickInfo
        clickRecord.set('ipua', ip + '|' + ua)
        clickRecord.set('clickInfo', clickInfo)
        clickRecord.set('time', datetime.today())
        clickRecord.save()
        print clickList
        return redirect("https://at.umeng.com/LfW9Xb?cid=483", code=302)
    else:
        androidIdRepeat = AndroidIdRepeat()
        androidId = AndroidId()
        #print headers.get('X-Forwarded-For')
        key = headers.get('Key')
        if key == '123321123':
            #关联ClickInfo
            clickInfo = None
            if clickList.has_key(ip + '|' + ua):
                clickInfo = clickList[ip + '|' + ua]
            # 获取提交的表单
            if request.content_type == "text/plain;charset=UTF-8":
                args = json.loads(request.get_data())
            else:
                args = request.form
            affiliate = args.get('af')
            user_androidId = args.get('ai')
            aa =  args.get('aa')
            mo = args.get('mo')
            nt = args.get('nt')
            oc = args.get('oc')
            vn = args.get('vn')
            lang = args.get('vn')
            an = args.get('an')
            on = args.get('on')
            pkg = args.get('pkg')
            me = args.get('me')
            ms = args.get('ms')

            if user_androidId != None:
                print user_androidId
                query = leancloud.Query(AndroidId)
                query.equal_to('ai', user_androidId)
                query_list = query.find()
                # 取国家
                r = requests.post(
                    'http://api.db-ip.com/v2/c6f4413393e0ce3d120471ad41f7d7ad5bf77df0/' + ip)
                country = json.loads(r.text)
                if country["countryCode"] != 'ZZ':
                    countryName = country["countryName"]
                else:
                    countryName = 'Unkown'
                if len(query_list) == 0:
                    #判断安卓Id是否存在
                    androidId.set('ai', user_androidId)
                    androidId.set('aa', aa)
                    androidId.set('mo', mo)
                    androidId.set('nt', nt)
                    androidId.set('oc', oc)
                    androidId.set('vn', vn)
                    androidId.set('lang', lang)
                    androidId.set('an', an)
                    androidId.set('IP', ip)
                    androidId.set('ua', ua)
                    androidId.set('on', on)
                    androidId.set('pkg', pkg)
                    androidId.set('me', me)
                    androidId.set('ms', ms)
                    androidId.set('cn', countryName)
                    androidId.set('clickInfo', clickInfo)
                    androidId.save()

                    #获取扣量比例
                    query = leancloud.Query(CloudControl)
                    query.equal_to('versionName', '1.0.0')
                    query_list = query.find()
                    percentage = query_list[0].get('Percentage')
                    ran = random.randint(1, 100)
                    ran = float(ran)
                    print str(percentage) + '||' + str(ran)
                    #按比例扣量
                    if ran > percentage and countryName != 'China' and clickInfo != None:
                        query = leancloud.Query(AffiliateSetting)
                        query.equal_to('name', affiliate)
                        query_list = query.find()
                        postLink = query_list[0].get('postLink')
                        paras = str(query_list[0].get('parameters')).split(',')
                        #post
                        postPara = ''
                        for para in paras:
                            if para == 'offer_id':
                                postPara = postPara + '&offer_id=' + str(clickInfo['offer_id'])
                            elif para == 'affiliate_id':
                                postPara = postPara + '&affiliate_id=' + str(clickInfo['affiliate_id'])
                            elif para == 'transaction_id':
                                postPara = postPara + '&transaction_id=' + str(clickInfo['transaction_id'])
                            elif para == 'sub_id':
                                postPara = postPara + '&sub_id=' + str(clickInfo['sub_id'])
                            elif para == 'ip':
                                postPara = postPara + '&ip=' + ip
                            elif para == 'country':
                                postPara = postPara + '&country=' + countryName
                            elif para == 'install_time':
                                postPara = postPara + '&install_time=' + str(datetime.today())
                        url = postLink + '?' + postPara[1, len(postPara)]
                        print 'url:' + url
                        r = requests.post(url)
                        print r.text
                        #Post Test
                        postTest = PostTest()
                        postTest.set('country', countryName)
                        postTest.set('ip', ip)
                        postTest.set('installTime', datetime.today())
                        postTest.set('postPara', postPara)
                        postTest.save()
                        return '数据添加成功，已Post'
                    else:
                        return '数据添加成功，不Post'
                else:
                    androidIdRepeat.set('ai', user_androidId)
                    androidIdRepeat.set('aa', aa)
                    androidIdRepeat.set('mo', mo)
                    androidIdRepeat.set('nt', nt)
                    androidIdRepeat.set('oc', oc)
                    androidIdRepeat.set('vn', vn)
                    androidIdRepeat.set('lang', lang)
                    androidIdRepeat.set('an', an)
                    androidIdRepeat.set('IP', ip)
                    androidIdRepeat.set('ua', ua)
                    androidIdRepeat.set('on', on)
                    androidIdRepeat.set('pkg', pkg)
                    androidIdRepeat.set('me', me)
                    androidIdRepeat.set('ms', ms)
                    androidIdRepeat.set('clickInfo', clickInfo)
                    androidIdRepeat.set('cn', countryName)
                    androidIdRepeat.save()
                    return '安卓Id已存在，已添加至androidIdRepeat表'
            else:
                androidIdRepeat.set('ai', 'missing androidId')
                androidIdRepeat.save()
                return 'androidId missing'
        else:
            return "服务器错误"

def clickListInit():
    query = leancloud.Query(ClickRecord)
    query.greater_than('time', datetime.today()-3600)
    query_list = query.find()
    for item in query_list:
        clickList[item.get['ipua']] = dict(item.get['clickInfo'])




@app.route('/time')
def time():
    return str(datetime.now())


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


if __name__ == '__main__':
    app.run('0.0.0.0')
    clickListInit()
