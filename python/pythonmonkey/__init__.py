# Export public PythonMonkey APIs
from .pythonmonkey import *
from .require import *

# Expose the package version
import importlib.metadata
__version__= importlib.metadata.version(__name__)

# Load the module by default to make `console`/`atob`/`btoa` globally available
require("console")
require("base64")

# Add the `.keys()` method on `Object.prototype` to get JSObjectProxy dict() conversion working
# Conversion from a dict-subclass to a strict dict by `dict(subclass)` internally calls the .keys() method to read the dictionary keys, 
# but .keys on a JSObjectProxy can only come from the JS side
pm.eval("""
(makeList) => {
  const keysMethod = {
    get() {
      return () => makeList(...Object.keys(this))
    }
  }
  Object.defineProperty(Object.prototype, "keys", keysMethod)
  Object.defineProperty(Array.prototype, "keys", keysMethod)
}
""")(lambda *args: list(args))
