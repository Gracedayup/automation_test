from common.handle_log import HandleLog
import pytest

@pytest.fixture(scope="session")
def testcase_data():
    logger = HandleLog().handle_log()
    yield logger
