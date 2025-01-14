import yaml


class Config:
    _instance = None
    def __new__(cls, config_file: str = 'config.yaml', *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.__load_config(config_file)
        return cls._instance

    def __load_config(self, config_file: str) -> None:
        with open(config_file, "r") as file:
            self._config = yaml.safe_load(file)

    def get(self, key: str, default=None) -> str:
        keys = key.split(".")
        value = self._config
        try:
            for k in keys:
                value = value[k]
        except KeyError:
            value = default
        return value


waiting_typing = lambda x:  len(x) / 8


