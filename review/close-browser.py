from browser import Browser
try: Browser().call('Browser.close')
except (ConnectionError,OSError,TimeoutError): pass
