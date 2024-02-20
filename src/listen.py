
import asyncio
import hlog
from hlog import log_info, log_debug, log_error, log_warn
from ok_api import public_info


if __name__ == "__main__":
    hlog.init("log/listen.log")
    log_info("Starting listen")
    asyncio.run(public_info.common_api(public_info.liquidation, public_info.handle_huge_liquidation))
