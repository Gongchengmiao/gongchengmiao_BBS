#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import time
from celery import Celery
from django.core.mail import send_mail, EmailMultiAlternatives, BadHeaderError
from .models import common_member, common_member_email_send_time

celery = Celery('tasks', broker='redis://localhost:6379/0')


@celery.task
def add(x, y):
    return x + y


@celery.task
def run_test_suit(ts_id):
    print("++++++++++++++++++++++++++++++++++++")
    print('jobs[ts_id=%s] running....' % ts_id)
    time.sleep(10.0)
    print('jobs[ts_id=%s] done' % ts_id)
    result = True
    return result


@celery.task
def send_email_1(msg):
    msg.send()

