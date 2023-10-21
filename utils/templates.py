from fastapi.templating import Jinja2Templates


def config_templates():
    _templates = Jinja2Templates(directory="templates")
    return _templates


templates = config_templates()
