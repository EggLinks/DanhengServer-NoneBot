from pydantic import BaseModel

class Config(BaseModel):
    # The server IP address
    danheng_ip: str = ""
    # The server admin_key
    danheng_admin_key: str = ""
    danheng_assest_dir: str = ""
