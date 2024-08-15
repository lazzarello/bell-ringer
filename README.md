# Ring a Bell

Installation

* RaspberryPi OS "Bookworm" or higher
* System Python 3.11.2
* Internet access via Ethernet or Wifi

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
cp bell-ringer.service /etc/systemd/system/bell-ringer.service
systemctl daemon-reload
systemctl enable bell-ringer.service
systemctl start bell-ringer.service
```

Read PDF manual for hardware requirements.
[Raspberry Pi 3 model B pinouts](https://pinout.xyz/pinout/5v_power#:~:text=The%205v%20power%20pins%20are,Pi%20model%20and%20adapter%20used.)
