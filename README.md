# pypjlink3

Implementation of the PJLink Class 1 protocol to control projectors.

Fork of pypjlink which is no longer maintained, switching to asyncio

## Usage
```python
from pypjlink import Projector

with Projector.from_address('projector_host') as projector:
    projector.authenticate()
    projector.set_power('on')
```
