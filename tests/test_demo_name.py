# Copyright [yyyy] [name of copyright owner]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Things to do:
 - Please name this file `test_<demo_name>.py`
 - Fill in [yyyy] and [name of copyright owner] in the copyright (top line)
 - Add unit tests for your demo
 - Add a smoke test (i.e. does the demo actually run?)
 - Format code so that it conforms with PEP 8
"""

from dimod.generators import and_gate
from dwave.system import LeapHybridSampler
bqm = and_gate('x1', 'x2', 'y1')
sampler = LeapHybridSampler()    
answer = sampler.sample(bqm)   
print(answer) 