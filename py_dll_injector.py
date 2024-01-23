import ctypes
import win32api
import win32con

def open_target_process(target_process):
    hprocess = win32api.OpenProcess(
        win32con.PROCESS_ALL_ACCESS,  # required permissions
        False,                      # don't inherit handles
        target_process)

    if not hprocess:
        raise Exception("Failed to open the process '{}'".format(target_process))

    return hprocess

def load_dll(dll_name):
    hdll = win32api.LoadLibrary(dll_name)

    if not hdll:
        raise Exception("Failed to load the DLL '{}'".format(dll_name))

    return hdll

def get_function_address(hdll, hook_function):
    function_address = ctypes.windll.kernel32.GetProcAddress(hdll, hook_function)

    if not function_address:
        raise Exception("Failed to get the address of '{}' in '{}'".format(hook_function, dll_name))

    return function_address

def create_remote_thread(hprocess, function_address, hook_address):
    thread_handle = win32api.CreateRemoteThread(
        hprocess, None, 0,
        function_address,
        (hook_address,), None)

    if not thread_handle:
        raise Exception("Failed to create a remote thread for DLL injection")

    return thread_handle

def main():
    try:
        # Target process to inject into
        target_process = 'notepad.exe'

        # Name of the DLL to inject
        dll_name = 'injected_dll.dll'

        # Function to hook in the target process
        hook_function = 'HookFunction'

        # Address of the function to hook in the target process
        hook_address = 0x12345678

        # Load the target process
        hprocess = open_target_process(target_process)

        # Load the DLL
        hdll = load_dll(dll_name)

        # Get the address of the exported function in the DLL
        function_address = get_function_address(hdll, hook_function)

        # Create a new thread to inject the DLL
        thread_handle = create_remote_thread(hprocess, function_address, hook_address)

        # Close the handle to the DLL
        win32api.CloseHandle(hdll)

        # Wait for the thread to finish
        win32api.WaitForSingleObject(thread_handle, win32con.INFINITE)

        # Close the handle to the target process
        win32api.CloseHandle(hprocess)

        # Print success message
        print("DLL injection successful!")

    except Exception as e:
        print("Error: {}".format(e))

if __name__ == "__main__":
    main()
