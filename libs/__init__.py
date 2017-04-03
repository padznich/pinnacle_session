import sys
import os

route = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../")

if route not in sys.path:
    sys.path.append(route)
