# coding: utf-8

from leancloud import Engine
from leancloud import LeanEngineError
import leancloud

from app import app
from app import ip
import requests

engine = Engine(app)


class AndroidId(leancloud.Object):
    pass


@engine.define
def Hello(**params):
    print params
    androidId = AndroidId()
    if 'androidId' in params:
        aid = params['androidId']
        print aid
        query = leancloud.Query(AndroidId)
        query.equal_to('androidId', aid)
        query_list = query.find()
        print len(query_list)
        if len(query_list) == 0:
            androidId.set('androidId', aid)
            androidId.set('IP', ip)
            androidId.save()
            r = requests.post(
                "http://postback.mobisummer.com/aff_lsr?offer_id=gootube&affiliate_id="
                "Mobisummer&transaction_id=apk&sub_id=apk1&ip=xxx&country=xxx&install_time=xxx")
            print r.text
            return '添加成功'+ r.text
        else:
            return '安卓Id已存在'
    else:
        return 'androidId missing'


@engine.before_save('Todo')
def before_todo_save(todo):
    content = todo.get('content')
    if not content:
        raise LeanEngineError('内容不能为空')
    if len(content) >= 240:
        todo.set('content', content[:240] + ' ...')
