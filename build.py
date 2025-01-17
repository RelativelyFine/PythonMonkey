# @file        build.py
#              Main PythonMonkey build automation script. Run with `poetry build`.
# @author      Hamada Gasmallah, hamada@distributive.network
# @date        April 2023
#
import subprocess
import os, sys
import platform
from typing import Optional

TOP_DIR = os.path.abspath(os.path.dirname(__file__))
BUILD_DIR = os.path.join(TOP_DIR, "build")

# Get number of CPU cores
CPUS = os.cpu_count() or 1

def execute(cmd: str, cwd: Optional[str] = None):
    popen = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT,
        shell = True, text = True, cwd = cwd )
    for stdout_line in iter(popen.stdout.readline, ""):
        sys.stdout.write(stdout_line)
        sys.stdout.flush()

    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def ensure_spidermonkey():
    # Check if SpiderMonkey libs already exist
    spidermonkey_lib_exist = os.path.exists(os.path.join( TOP_DIR, "_spidermonkey_install/lib" ))
    if spidermonkey_lib_exist:
        return

    # Build SpiderMonkey
    execute("bash ./setup.sh", cwd = TOP_DIR)

def run_cmake_build():
    os.makedirs(BUILD_DIR, exist_ok=True) # mkdir -p
    if platform.system() == "Windows":
        execute("cmake .. -T ClangCL", cwd=BUILD_DIR) # use Clang/LLVM toolset for Visual Studio
    else:
        execute("cmake ..", cwd=BUILD_DIR)
    execute(f"cmake --build . -j{CPUS} --config Release", cwd=BUILD_DIR)

def copy_artifacts():
    if platform.system() == "Windows":
        execute("cp ./build/src/*/pythonmonkey.pyd ./python/pythonmonkey/", cwd=TOP_DIR) # Release or Debug build
        execute("cp ./_spidermonkey_install/lib/mozjs-*.dll ./python/pythonmonkey/", cwd=TOP_DIR)
    else:
        execute("cp ./build/src/pythonmonkey.so ./python/pythonmonkey/", cwd=TOP_DIR)
        execute("cp ./_spidermonkey_install/lib/libmozjs* ./python/pythonmonkey/", cwd=TOP_DIR)

def build():
    execute("git submodule update --init --recursive", cwd=TOP_DIR)
    ensure_spidermonkey()
    run_cmake_build()
    copy_artifacts()

if __name__ == "__main__":
    build()
