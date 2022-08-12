"""
2022/08/12
-----------
Not working on Windows10 (64bit).
I haven't Windows11 so I can't test.

"""
import asyncio
import sys
from winsdk.windows.data.xml.dom import XmlDocument
from winsdk.windows.foundation import IPropertyValue
from winsdk.windows.ui.notifications import (
    ToastNotificationManager,
    ToastNotification,
    NotificationData,
    ToastActivatedEventArgs,
    ToastDismissedEventArgs,
    ToastFailedEventArgs
)
import time


toast_xml = """
<toast activationType="protocol" launch="http:">
    <visual>
        <binding template='ToastGeneric'></binding>
    </visual>
</toast>
"""


def add_text(doc, text):
    binding = doc.select_single_node('//binding')
    text_elem = doc.create_element('text')
    text_elem.inner_text = text
    binding.append_child(text_elem)


async def toast(title=None, body=None, app_id='Python'):
    loop = asyncio.get_running_loop()

    doc = XmlDocument()
    doc.load_xml(toast_xml)
    add_text(doc, title)
    add_text(doc, body)
    notif = ToastNotification(doc)

    notifier = ToastNotificationManager.create_toast_notifier(app_id)
    notifier.show(notif)

    failed_future = loop.create_future()
    notif.add_failed(
        lambda _, event_args: loop.call_soon_threadsafe(
            failed_future.set_result, print(ToastFailedEventArgs._from(event_arg).error_code)
        )
    )


def main():
    if len(sys.argv) >= 2 and sys.argv[1] in ('-h', '--help'):
        print('Usage: toast.py [title] [body]')
        sys.exit(0)

    if len(sys.argv) < 3:
        title = 'Example'
        body = 'Hello, World!'
    else:
        title = sys.argv[1]
        body = sys.argv[2]
    
    asyncio.run(toast(title=title, body=body))


if __name__ == '__main__':
    main()
