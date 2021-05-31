'''
from celery.decorators import task
from celery.utils.log import get_task_logger
from time import sleep
from .celery.inform_using_mail import send_mail_to

sleeplogger = get_task_logger(__name__)@task(name='my_first_task')
def my_first_task(duration):
    subject= 'Celery'
    message= 'My task done successfully'
    receiver= 'receiver_mail@gmail.com'
    is_task_completed= False
    error=''
    try:
        sleep(duration)
        is_task_completed= True
    except Exception as err:
        error= str(err)
        logger.error(error)
    if is_task_completed:
        send_mail_to(subject,message,receivers)
    else:
        send_mail_to(subject,error,receivers)
    return('first_task_done')

'''
