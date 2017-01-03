# coding: utf-8
#遗留问题：IP会变：54.193.59.55


from datetime import datetime
import json
from flask import Flask
from flask import render_template
from flask_sockets import Sockets
import random
from views.todos import todos_view
from flask import request
import leancloud
import requests


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


@app.route('/', methods=["Post"])
def index():
    androidIdRepeat = AndroidIdRepeat()
    androidId = AndroidId()
    headers = request.headers
    #print headers.get('X-Forwarded-For')
    header = headers.get('Key')
    if header == '123321123':
        #获取IP
        ip = headers.get('X-Forwarded-For')
        # 获取提交的表单
        if request.content_type == "text/plain;charset=UTF-8":
            args = json.loads(request.get_data())
        else:
            args = request.form
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
                androidId.set('on', on)
                androidId.set('pkg', pkg)
                androidId.set('me', me)
                androidId.set('ms', ms)
                androidId.set('cn', countryName)
                androidId.save()
                query = leancloud.Query(CloudControl)
                query.equal_to('versionName', '1.0.0')
                query_list = query.find()
                percentage = query_list[0].get('Percentage')
                ran = random.randint(1, 100)
                ran = float(ran)

                print str(percentage) + '||' + str(ran)
                if ran > percentage and countryName != 'China':
                    #post hasoffers
                    r = requests.post(
                        "http://postback.mobisummer.com/aff_lsr?offer_id=gootube&affiliate_id="
                        "Mobisummer&transaction_id=apk&sub_id=apk1&ip=" + ip + "&country=" + countryName + "&install_time=" + str(datetime.today()))
                    print r.text
                    #Post Test
                    postTest = PostTest()
                    postTest.set('country', countryName)
                    postTest.set('ip', ip)
                    postTest.set('installTime', datetime.today())
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
                androidIdRepeat.set('on', on)
                androidIdRepeat.set('pkg', pkg)
                androidIdRepeat.set('me', me)
                androidIdRepeat.set('ms', ms)
                androidIdRepeat.set('cn', countryName)
                androidIdRepeat.save()
                return '安卓Id已存在，已添加至androidIdRepeat表'
        else:
            androidIdRepeat.set('ai', 'missing androidId')
            androidIdRepeat.save()
            return 'androidId missing'
    else:
        return "服务器错误"


@app.route('/time')
def time():
    return str(datetime.now())


@sockets.route('/echo')
def echo_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)


if __name__ == '__main__':
    app.run()
