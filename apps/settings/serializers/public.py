# coding: utf-8
#

from rest_framework import serializers

__all__ = ['PublicSettingSerializer', 'PrivateSettingSerializer']


class PublicSettingSerializer(serializers.Serializer):
    XPACK_ENABLED = serializers.BooleanField()
    INTERFACE = serializers.DictField()


class PrivateSettingSerializer(PublicSettingSerializer):
    WINDOWS_SKIP_ALL_MANUAL_PASSWORD = serializers.BooleanField()
    OLD_PASSWORD_HISTORY_LIMIT_COUNT = serializers.IntegerField()
    TICKET_AUTHORIZE_DEFAULT_TIME = serializers.IntegerField()
    TICKET_AUTHORIZE_DEFAULT_TIME_UNIT = serializers.CharField()
    AUTH_LDAP_SYNC_ORG_ID = serializers.CharField()
    SECURITY_MAX_IDLE_TIME = serializers.IntegerField()
    SECURITY_VIEW_AUTH_NEED_MFA = serializers.BooleanField()
    SECURITY_MFA_VERIFY_TTL = serializers.IntegerField()
    SECURITY_COMMAND_EXECUTION = serializers.BooleanField()
    SECURITY_PASSWORD_EXPIRATION_TIME = serializers.IntegerField()
    SECURITY_LUNA_REMEMBER_AUTH = serializers.BooleanField()
    SECURITY_WATERMARK_ENABLED = serializers.BooleanField()
    SESSION_EXPIRE_AT_BROWSER_CLOSE = serializers.BooleanField()
    PASSWORD_RULE = serializers.DictField()
    SECURITY_SESSION_SHARE = serializers.BooleanField()
    XPACK_LICENSE_IS_VALID = serializers.BooleanField()
    XPACK_LICENSE_INFO = serializers.DictField()
    HELP_DOCUMENT_URL = serializers.CharField()
    HELP_SUPPORT_URL = serializers.CharField()

    AUTH_WECOM = serializers.BooleanField()
    AUTH_DINGTALK = serializers.BooleanField()
    AUTH_FEISHU = serializers.BooleanField()
    AUTH_TEMP_TOKEN = serializers.BooleanField()

    TERMINAL_RAZOR_ENABLED = serializers.BooleanField()
    TERMINAL_MAGNUS_ENABLED = serializers.BooleanField()
    TERMINAL_KOKO_SSH_ENABLED = serializers.BooleanField()
    TERMINAL_OMNIDB_ENABLED = serializers.BooleanField()

    TERMINAL_GRAPHICAL_RESOLUTION = serializers.CharField()

    ANNOUNCEMENT_ENABLED = serializers.BooleanField()
    ANNOUNCEMENT = serializers.DictField()

    TICKETS_ENABLED = serializers.BooleanField()
    CONNECTION_TOKEN_REUSABLE = serializers.BooleanField()
