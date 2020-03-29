from ota_update.ota_updater import OTAUpdater


def download_and_install_update_if_available():
    ota_updater = OTAUpdater('https://github.com/perbu/bandwidth-monitor')
    # This could be a cron job or something.
    ota_updater.check_for_update_to_install_during_next_reboot()
    ota_updater.download_and_install_update_if_available()



def start():
    # your custom code goes here. Something like this: ...
    from main.rainbow import RainbowMonitor
    r = RainbowMonitor()
    r.listen(666)
    r.superloop()


def boot():
    download_and_install_update_if_available()
    start()


boot()