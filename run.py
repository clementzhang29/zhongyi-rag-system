import uvicorn, yaml, os
_ROOT = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(_ROOT, 'config.yaml')
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

import numpy as np
if not hasattr(np, "sctypes"):
    np.sctypes = {"float": [np.float16, np.float32, np.float64],
                   "int": [np.int8, np.int16, np.int32, np.int64],
                   "uint": [np.uint8, np.uint16, np.uint32, np.uint64],
                   "complex": [np.complex64, np.complex128]}

from src.api.server import app
host = config.get("server", {}).get("host", "0.0.0.0")
port = int(config.get("server", {}).get("port", 8000))
print(f"[run] 启动服务 http://{host}:{port}")
uvicorn.run(app, host=host, port=port, log_level="info")
