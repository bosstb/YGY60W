# coding: utf-8

from datetime import datetime

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


@app.route('/')
def index():
    androidIdRepeat = AndroidIdRepeat()
    androidId = AndroidId()
    args = request.args
    ip = request.remote_addr
    #取Get参数
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
            androidId.save()
            query = leancloud.Query(CloudControl)
            query.equal_to('versionName', vn)
            query_list = query.find()
            percentage = query_list[0]
            ran = random.randint(1, 100)
            ran = float(ran)/100
            #取国家
            # r = requests.post(
            #          'http://api.ipinfodb.com/v3/ip-country/?key=<your_api_key>&ip=' + ip + '&format=json')
            # country = r.text
            print percentage
            if ran < percentage:
                # r = requests.post(
                #     "http://postback.mobisummer.com/aff_lsr?offer_id=gootube&affiliate_id="
                #     "Mobisummer&transaction_id=apk&sub_id=apk1&ip=xxx&country=xxx&install_time=xxx")
                postTest = PostTest()
                postTest.set('country', '未知')
                postTest.set('ip', ip)
                postTest.set('installTime', datetime.today())
                postTest.save()
                return '已Post'
            else:
                return '不Post'
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
            androidIdRepeat.save()
            return '安卓Id已存在'
    else:
        androidIdRepeat.set('ai', 'missing androidId')
        androidIdRepeat.save()
        return 'androidId missing'


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
