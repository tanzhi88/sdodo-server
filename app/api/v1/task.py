from flask import jsonify, request

from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.spider import Spider
# from app.libs.task import scheduler, go, remove_task, p, r
from app.libs.task import Task
from app.libs.token_auth import auth

api = Redprint('task')

# @api.route('/pause')
# def pause(id):#暂停
#     scheduler.pause_job(id)
#     return "Success!"
# @api.route('/resume')
# def resume(id):#恢复
#     scheduler.resume_job(id)
#     return "Success!"
# @api.route('/get')
# def  get(id) :#获取
#     jobs=scheduler.get_jobs()
#     print(jobs)
#     return '111'
# def remove(id):#移除
#     scheduler.delete_job(id)
#     return 111
@api.route('')
@auth.login_required
def get_coupon():
    data = request.json
    q = data['q']
    page = data['page']
    size = data['size']
    task = Task(q=q, page=page, size=size)
    coupons = task.go()
    return jsonify(coupons)
    return Success()

# @api.route('/p', methods=['DELETE'])
# def remove():
#     p()
#     return Success()
#
# @api.route('/r', methods=['DELETE'])
# def resume():
#     r()
#     return Success()