from typing import Optional

__all__ = ['__version__', 'debug', 'cuda', 'git_version', 'hip']
__version__ = '2.2.0+cpu'
debug = False
cuda: Optional[str] = None
git_version = '8ac9b20d4b090c213799e81acf48a55ea8d437d6'
hip: Optional[str] = None
