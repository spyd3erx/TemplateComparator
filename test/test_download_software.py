from src.core.utils.setup import setup_software

def test_download_software():
    from src.config import INSTALLERS_PATH
    import os
    setup_software()

    assert (INSTALLERS_PATH / 'gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe').exists()
    assert any("pandoc-" in filename for filename in os.listdir(INSTALLERS_PATH))
