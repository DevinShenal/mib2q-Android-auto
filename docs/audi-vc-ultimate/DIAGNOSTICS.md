# Diagnostics and privacy

Diagnostics are useful for understanding AA enumeration, receiver startup,
cluster stream requests, decode/render, standby, teardown and reconnect. A
future collector should record timestamps, session IDs, stream dimensions,
decoder mode, last decoded frame, stalls and bounded-recovery counters without
recording routes or device identities.

## Local scrubber

The initial tool reads a text file and prints a redacted preview to stdout. It
does not change the source, create an archive, transmit data or connect to the car.

```sh
python3 scripts/diagnostic_scrubber.py carplay_logs/aa/aa_cluster_hook.log
cat carplay_logs/aa/aa_cluster_hook.log | python3 scripts/diagnostic_scrubber.py -
```

It redacts common labeled identifiers (VIN, serial, IMEI/IMSI, device names,
MACs, email and route/location fields), standalone VIN/MAC/email patterns,
coordinates, and `navxlate.raw` / navigation payload lines. This is a conservative
first pass, **not a guarantee of anonymization**. Inspect the preview manually
for names, addresses, account identifiers, map traces, phone details and any
unexpected secrets before sharing. Do not upload raw logs to an issue.

The collector itself, preview UI, additional scrubber fixtures and redaction
coverage remain future work. Never commit real vehicle logs or personal routes.
