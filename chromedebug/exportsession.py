import pychrome
import json
import textwrap

# Connect to the browser
browser = pychrome.Browser(url="http://127.0.0.1:9223")

# List tabs
tabs = browser.list_tab()
tab = tabs[0]  # pick the first tab

tab.start()  # start the tab session

# Evaluate JavaScript to get sessionStorage
# NOTE: The browser's sessionStorage is tied to the origin of the current tab.
result = tab.Runtime.evaluate(expression="JSON.stringify(sessionStorage)")

# Parse JSON string into Python dictionary
# This dictionary now holds the data to be imported elsewhere
session_storage = json.loads(result['result']['value'])

# Stop the tab session
tab.stop()

# --- Console Command Generation ---

print("\n=== Session Storage Export ===\n")

if not session_storage:
    print("Session storage was empty. No import command generated.\n")
else:
    # 1. Create a JavaScript string representing the object to import
    # This ensures proper JSON formatting for the data
    import_data_js = json.dumps(session_storage, indent=2)

    # 2. Wrap the data and logic into a single console command
    # The command clears existing sessionStorage and then sets all key/value pairs.
    js_command = f"""
        (function() {{
            const importData = {import_data_js};
            const sStorage = window.sessionStorage;

            console.group("Session Storage Import");
            console.log("Clearing existing storage...");
            sStorage.clear();

            let importCount = 0;
            for (const key in importData) {{
                if (Object.hasOwnProperty.call(importData, key)) {{
                    sStorage.setItem(key, importData[key]);
                    importCount++;
                }}
            }}
            console.log(`Successfully imported ${{importCount}} item(s).`);
            console.log("New Session Storage:", sStorage);
            console.groupEnd();
        }})();
    """

    # 3. Clean up the command for easy copy/paste and printing
    # We use textwrap.dedent to remove leading whitespace
    clean_command = textwrap.dedent(js_command).strip()

    print("Copy and paste the command below into your browser's console:\n")
    print("--------------------------------------------------------------------------------")
    print(clean_command)
    print("--------------------------------------------------------------------------------\n")

# --- End of Script ---
