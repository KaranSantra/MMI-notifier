import os

def notify(title, message):
    os.system(f"terminal-notifier -title '{title}' -message '{message}' -timeout 0")

# Example usage
notify("Persistent Notification", "This notification will stay until you dismiss it.")