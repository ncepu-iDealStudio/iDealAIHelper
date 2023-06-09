import uvicorn
from config.globals import config
from utils.logger import get_log_config
from app import create_app

app = create_app()
if __name__ == "__main__":
    uvicorn.run(app,
                host=config.get("host"),
                port=int(config.get("port")),
                proxy_headers=True,
                forwarded_allow_ips='*',
                log_config=get_log_config(),
                )
