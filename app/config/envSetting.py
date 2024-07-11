from app.config.aws.secret import get_secret
import os


def set_environment_by_secret_manager() -> None:
    """
    Secret Manager에서 가져온 환경변수를 설정한다.
    :rtype: None
    """
    secrets_dict = dict(get_secret())
    if not secrets_dict:
        print("환경변수가 없습니다.")

    for k, v in secrets_dict.items():
        if k in os.environ:
            continue
        if v is not None:
            os.environ[k] = v


set_environment_by_secret_manager()
