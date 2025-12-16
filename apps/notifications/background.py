import threading


def send_email_async(func, *args, **kwargs):
    threading.Thread(
        target=func,
        args=args,
        kwargs=kwargs,
        daemon=True,
    ).start()
