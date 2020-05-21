# pypjlink2

Implementation of the PJLink Class 1 protocol to control projectors.

Fork of pypjlink which is no longer maintained, with support for Optoma projectors

## Usage
```python
from pypjlink import Projector

with Projector.from_address('projector_host') as projector:
    projector.authenticate()
    projector.set_power('on')
```
