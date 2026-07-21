# customer-care-system

A working telecom customer-care backend — billing, complaints, plan recommendations
and outage notifications. Traditional deterministic code throughout. No AI.

## Structure

```
api/            REST route handlers
services/       Business logic
database/       In-memory data stores (stand-ins for real DB tables)
ui/             (placeholder — not the focus of this exercise)
app.py          Flask entrypoint
```

## Running

```
pip install flask --break-system-packages
python app.py
```

## Status

This is a functioning, five-year-old application. It works. The question this
repository exists to answer is: **where, if anywhere, should AI be introduced?**
See `BMAD_ANALYSIS.md` (added in the next commit) for that analysis.
