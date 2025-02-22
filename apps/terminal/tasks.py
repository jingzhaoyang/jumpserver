# -*- coding: utf-8 -*-
#

import datetime

from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.files.storage import default_storage
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ops.celery.decorator import (
    register_as_period_task, after_app_ready_start,
    after_app_shutdown_clean_periodic
)
from orgs.utils import tmp_to_builtin_org
from .backends import server_replay_storage
from .models import (
    Status, Session, Task, AppletHostDeployment, AppletHost
)
from .utils import find_session_replay_local

CACHE_REFRESH_INTERVAL = 10
RUNNING = False
logger = get_task_logger(__name__)


@shared_task(verbose_name=_('Periodic delete terminal status'))
@register_as_period_task(interval=3600)
@after_app_ready_start
@after_app_shutdown_clean_periodic
def delete_terminal_status_period():
    yesterday = timezone.now() - datetime.timedelta(days=7)
    Status.objects.filter(date_created__lt=yesterday).delete()


@shared_task(verbose_name=_('Clean orphan session'))
@register_as_period_task(interval=600)
@after_app_ready_start
@after_app_shutdown_clean_periodic
def clean_orphan_session():
    active_sessions = Session.objects.filter(is_finished=False)
    for session in active_sessions:
        # finished task
        Task.objects.filter(args=str(session.id), is_finished=False).update(
            is_finished=True, date_finished=timezone.now()
        )
        # finished session
        if session.is_active():
            continue
        session.is_finished = True
        session.date_end = timezone.now()
        session.save()


@shared_task(verbose_name=_('Upload session replay to external storage'))
def upload_session_replay_to_external_storage(session_id):
    logger.info(f'Start upload session to external storage: {session_id}')
    session = Session.objects.filter(id=session_id).first()
    if not session:
        logger.error(f'Session db item not found: {session_id}')
        return

    local_path, foobar = find_session_replay_local(session)
    if not local_path:
        logger.error(f'Session replay not found, may be upload error: {local_path}')
        return

    abs_path = default_storage.path(local_path)
    remote_path = session.get_relative_path_by_local_path(abs_path)
    ok, err = server_replay_storage.upload(abs_path, remote_path)
    if not ok:
        logger.error(f'Session replay upload to external error: {err}')
        return

    try:
        default_storage.delete(local_path)
    except:
        pass
    return


@shared_task(
    verbose_name=_('Run applet host deployment'),
    activity_callback=lambda self, did, *args, **kwargs: ([did],)
)
def run_applet_host_deployment(did):
    with tmp_to_builtin_org(system=1):
        deployment = AppletHostDeployment.objects.get(id=did)
        deployment.start()


@shared_task(
    verbose_name=_('Install applet'),
    activity_callback=lambda self, did, applet_id, *args, **kwargs: ([did],)
)
def run_applet_host_deployment_install_applet(did, applet_id):
    with tmp_to_builtin_org(system=1):
        deployment = AppletHostDeployment.objects.get(id=did)
        deployment.install_applet(applet_id)


@shared_task(
    verbose_name=_('Generate applet host accounts'),
    activity_callback=lambda self, host_id, *args, **kwargs: ([host_id],)
)
def applet_host_generate_accounts(host_id):
    applet_host = AppletHost.objects.filter(id=host_id).first()
    if not applet_host:
        return

    with tmp_to_builtin_org(system=1):
        applet_host.generate_accounts()
