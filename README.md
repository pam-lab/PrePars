
![](https://img.shields.io/github/workflow/status/pam-lab/prepars/CodeQL?label=CodeQL)
![](https://img.shields.io/github/workflow/status/pam-lab/prepars/Upload%20Python%20Package?label=Publish%20to%20PyPI)
![](https://img.shields.io/github/workflow/status/pam-lab/prepars/Python%20Automatic%20Tests?label=Python%20Automatic%20Tests)
[![Documentation Status](https://readthedocs.org/projects/prepars/badge/?version=latest)](https://prepars.readthedocs.io/en/latest/?badge=latest)
![](https://img.shields.io/github/issues/pam-lab/PrePars)
![](	https://img.shields.io/github/stars/pam-lab/PrePars)
![](https://img.shields.io/github/license/pam-lab/PrePars)
![](https://img.shields.io/pypi/pyversions/prepars)

This package is available on [Pip](https://pypi.org/project/prepars/). So you can install the latest version using:
```bash
pip install prepars
```

```python
from prepars.spacing import Spacing

output =Spacing().fix('من مطالب را طوطی وار حفظ می کردم. ')
```

You can see online demo for project [here](https://huggingface.co/spaces/pourmand1376/PrePars).

Online documentation is also available [here](https://prepars.readthedocs.io/en/latest/).

This project is a replacement for `Hazm` and `Parsivar`. 

This will build and push the package to `PyPi` whenever you add a tag starting with `v` to a commit. 
