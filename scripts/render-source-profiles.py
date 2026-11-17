#!/usr/bin/env python3
"""Render all refreshed provider pages using the maintained profile renderer."""
import importlib.util
from pathlib import Path
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('discovery',root/'scripts/render-discovery-pages.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
for provider in module.FS:
 if provider['id'] not in [6,13]:(root/provider['url'].lstrip('/')/'index.html').write_text(module.profile(provider))
print('Rendered 21 refreshed profiles; Kuara and Sunset retained.')
