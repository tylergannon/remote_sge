from sge.config_base import ConfigBase, Sections, Settings, Defaults

class ServerSettings(object):
    WORK_ROOT = r'work_root'
    COMPLETED_FILES_ROOT = r'completed_files_root'

class ServerConfig(ConfigBase):
    "Server App Configuration"
    def __init__(self, configparser):
        """
        Args:
            configparser (:class:`configparser.ConfigParser`): configuration settings.
        """

        super().__init__(configparser)
        self.qsub_settings = configparser[Sections.QSUB_SETTINGS]
        server_settings = configparser[Sections.SERVER]
        self.work_root = server_settings[ServerSettings.WORK_ROOT]
        self.completed_files_root = server_settings[ServerSettings.COMPLETED_FILES_ROOT]
        self.script_env = configparser[Sections.ENVIRONMENT]
