#!/usr/bin/env python3
"""Synchronise agenda source with browser data and the legacy event feed."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
agenda=json.loads((root/'data/agenda.json').read_text())
(root/'data/agenda-data.js').write_text('window.HTL_AGENDA = '+json.dumps(agenda,ensure_ascii=False,indent=2)+';\n')
(root/'data/events.json').write_text(json.dumps(agenda['events'],ensure_ascii=False,indent=2)+'\n')
p=root/'data/site-data.js';s=p.read_text();data=json.loads(s[s.index('{'):s.rindex('}')+1]);data['events']=agenda['events'];p.write_text('window.HTL_DATA = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n')
print('Agenda browser data and dated feeds synchronised.')
