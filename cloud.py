# coding: utf-8

from leancloud import Engine
from leancloud import LeanEngineError
import leancloud

from app import app


engine = Engine(app)


class AndroidId(leancloud.Object):
    pass


@engine.define
def Hello(**params):
    androidId = AndroidId()
    if 'androidId' in params:
        aid = params['androidId']
        query = leancloud.Query(AndroidId)
        query.equal_to('androidId', aid)
        query_list = query.find()
        if len(query_list) == 0:
            ret = androidId.set('androidId', params['androidId'])
            return '添加成功' + ret
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
