from sge.config_base import ConfigBase, Sections, Settings, Defaults

class ClientConfig(ConfigBase):
    "Client App Configuration"
    def __init__(self, configparser):
        """
        Args:
            configparser (:class:`configparser.ConfigParser`): configuration settings.
        """

        super().__init__(configparser)
        self.client_settings = configparser[Sections.CLIENT]

    @property
    def host(self):
        "Host"
        return self.client_settings.get(Settings.HOST, Defaults.HOST)

    @property
    def port(self):
        "Port"
        return self.client_settings.getint(Settings.PORT, Defaults.PORT)

