#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : task_apscheduler.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/10


from .sys_schedule import scheduler
from .deps import get_db
from core.logger import logger
from apps.monitor.models.job import Job


# 注册scheduler
def scheduler_register():
    scheduler.init_scheduler()  # noqa 去掉不合理提示
    JobInit().init_jobs_pause()  # noqa


def cron_pattern(expression):
    ''' 将cron表达式转换为 ApScheduler接收的字典格式

    :param expression: cron表达式
    :return: 字典格式cron表达式
    '''
    args = {}
    if expression is None:
        return args
    # 以空格为分隔符拆分字符串输出列表，拆分结果 ['0/2', '*', '*', '*', '*', '?']
    expression = expression.split(' ')
    if expression[0] != '?':
        args['second'] = expression[0]
    if expression[1] != '?':
        args['minute'] = expression[1]
    if expression[2] != '?':
        args['hour'] = expression[2]
    if expression[3] != '?':
        args['day'] = expression[3]
    if expression[4] != '?':
        args['month'] = expression[4]
    if expression[5] != '?':
        args['day_of_week'] = expression[5]
    return args


def add_job(func=None, args=None, kwargs=None, id=None, name=None, trigger='cron', coalesce=False, cron=None):
    '''将需要运行的函数添加到任务存储器中，并启动任务。

    :param func: 待运行的函数
    :param args: 函数参数
    :param kwargs: 函数参数
    :param id: 任务id
    :param name: 任务名称
    :param trigger: 触发器类型
    :param coalesce: 是否合并任务运行
    :param cron: 任务运行计划表达式
    :return:
    '''
    scheduler.add_job(func=func, args=args, kwargs=kwargs, id=str(id), name=name, trigger=trigger,
                      coalesce=coalesce, **cron_pattern(cron))


def del_job(job_id):
    ''' 删除ApScheduler存储器中已存在的任务

    :param job_id: 任务id
    :return:
    '''
    scheduler.remove_job(str(job_id))


def modify_job(func=None, args=None, kwargs=None, id=None, name=None, trigger='cron', coalesce=False,
               cron=None):
    ''' 删除已存在的任务，然后使用已删除的任务id创建新任务，实现修改任务功能

    :param func: 待运行的函数
    :param args: 函数参数
    :param kwargs: 函数参数
    :param id: 任务id
    :param name: 任务名称
    :param trigger: 触发器类型
    :param coalesce: 是否合并任务运行
    :param cron: 任务运行计划表达式
    :return:
    '''
    del_job(id)
    add_job(func=func, args=args, kwargs=kwargs, id=str(id), name=name, trigger=trigger, coalesce=coalesce,
            **cron_pattern(cron))


def query_job_id(job_id):
    ''' 根据id查询任务信息

    :param job_id: 任务id
    :return: 任务信息
    '''
    return scheduler.get_job(str(job_id))


def query_job_all():
    ''' 查询所有任务信息

    :return:任务信息列表
    '''
    return scheduler.get_jobs()


def pause_job(job_id):
    ''' 暂停ApScheduler存储器中已存在的任务,返回任务状态

    :param job_id: 任务id
    :return: 返回任务状态
    '''
    job_info = scheduler.pause_job(str(job_id))

    return get_job_status(job_info)


def start_job(job_id):
    ''' 启动ApScheduler存储器中已存在且暂停的任务，返回任务状态

    :param job_id: 任务id
    :return: 返回任务状态
    '''
    job_info = scheduler.resume_job(str(job_id))
    return get_job_status(job_info)


def get_job_status(job_data):
    ''' 从job信息中提炼出状态值

    :param job_data: 任务信息
    :return: 任务状态
    '''
    return str(job_data).split(",")[-1].strip(")")


def check_cron_pattern(cron_expression):
    if len(cron_expression.strip().split(' ')) != 6:
        raise 'cron格式错误'


class JobInit:

    def __init__(self):
        self.db = next(get_db())  # type: SessionLocal

    def init_jobs_pause(self):
        '''每次重启项目后APScheduler中的任务就会从内存中删除，导致APScheduler中的任务和数据库任务状态不一致，
        所以项目启动时将数据库中任务状态初始化为暂停状态
        :return:
        '''
        try:
            if (tasks := self.query_started_job()) is not None:
                self.set_pause_task(tasks)
            else:
                logger.info('数据库中没有已启动定时任务，不需要初始化任务')

        except Exception as e:
            logger.error('初始化定时任务状态失败信息：', e)

    def query_started_job(self):
        return self.db.query(Job).filter(Job.status == 1)

    def set_pause_task(self, tasks):
        try:
            obj = tasks.update({'status': 0})
            self.db.commit()
            if isinstance(obj, int):
                logger.info(f'初始化定时任务状态成功')
                return obj
        except:
            raise
