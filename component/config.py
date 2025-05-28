import json
# import logging
import os
from typing import Any, Dict, Optional


class ConfigLoader:
    _instance = None
    _config: Dict[str, Any] = {}
    _loaded = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance

    def _init_config(self, config_path):
        """初始化配置加载流程"""
        if not self._loaded:
            self._config = {}

            # 1.加载默认配置文件
            print(config_path)
            self._load_config_file(config_path)

            # 2.加载环境变量
            self._load_environment_vars()

            self._loaded = True

    def _load_config_file(self, file_path: str):
        """加载配置文件"""
        if not os.path.exists(file_path):
            # logging.warning(f"config file {file_path} not found")
            return

        file_ext = os.path.splitext(file_path)[1].lower()
        try:
            if file_ext == ".json":
                with open(file_path, "r", encoding="utf-8") as f:
                    self._config = json.load(f)
            elif file_ext in [".yaml", ".yml"]:
                try:
                    import yaml
                    with open(file_path, "r", encoding="utf-8") as f:
                        self._config = yaml.safe_load(f)
                except ImportError:
                    raise RuntimeError("PyYAML package is required to load YAML config files")
            else:
                raise ValueError(f"Unsupported config file format: {file_ext}")
        except Exception as e:
            # logging.error(f"Failed to load config file {file_path}: {str(e)}")
            raise

    def _load_environment_vars(self):
        """加载环境变量覆盖"""
        for env_key, env_value in os.environ.items():
            if env_key.startswith("APP_"):
                config_key = env_key[4:].lower()
                keys = config_key.split('__')  # 使用双下划线表示层级
                self._set_nested_value(keys, env_value)

    def _set_nested_value(self, keys: list, value: str):
        """递归设置嵌套配置值"""
        current = self._config
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        # 自动转换值类型
        try:
            value = json.loads(value)  # 尝试解析JSON格式的值
        except json.JSONDecodeError:
            pass  # 保持字符串格式

        current[keys[-1]] = value

    def get(self, key_path: str, default: Optional[Any] = None) -> Any:
        """获取配置项"""
        keys = key_path.split('.')
        current = self._config
        try:
            for key in keys:
                if isinstance(current, dict):
                    current = current[key]
                else:
                    return default
        except KeyError:
            return default
        return current

    def __getitem__(self, key: str) -> Any:
        return self.get(key)


# 全局配置实例
Config = ConfigLoader()


def load_configs(config_path):
    global Config
    Config._init_config(config_path)


# 使用示例
if __name__ == "__main__":
    load_configs("config/config_test.yaml")

    # 获取配置值
    app_name = Config["app.name"]

    print(app_name)
