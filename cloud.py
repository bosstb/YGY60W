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
        print aid
        query = leancloud.Query(AndroidId)
        query.equal_to('androidId', aid)
        query_list = query.find()
        print len(query_list)
        if len(query_list) == 0:
            androidId.set('androidId', aid)
            androidId.save()
            return '添加成功'
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
