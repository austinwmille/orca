__version__ = '0.17.0+cpu'
git_version = '9c7fb73ff9e8d6882734ad5cb2012884cb09c152'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
