from importlib_resources import files


class FilesUtils:

    @staticmethod
    def get_instance():
        return FilesUtils()

    @staticmethod
    def get_resource(module: str, name: str) -> str:
        """Load Text file from resources."""
        return files(module).joinpath(name).read_text(encoding="utf-8")
