> **DUPLICATE working copy — not the original.**
> Original: https://github.com/zivzancoeli-commits/Open-MI250X-Carrier
> Marked duplicate: 2026-08-21

# Open MI250X Carrier

## Purpose
This project collects public evidence needed to design a minimal open-source carrier board for surplus AMD Instinct MI250X OAM modules. It is organized as a reverse-engineering knowledge base: public documentation is collected first, facts are extracted into notes, and unknown or proprietary behavior is tracked instead of assumed.

## Workflow
- Collect public links and local reference copies in [02_AMD_Docs](02_AMD_Docs/) and [13_Reference_Docs](13_Reference_Docs/).
- Extract design-relevant facts into [09_AI_Notes](09_AI_Notes/), separating verified information from questions.
- Use research in [08_Research_Papers](08_Research_Papers/) to understand topology, bandwidth, and system context before design decisions.
- Carry verified mechanical, PCIe, power, cooling, firmware, and software assumptions into schematic, layout, prototype, and validation work.

## Top-Level Folders
- [02_AMD_Docs](02_AMD_Docs/): upstream public links for OAM, AMD matrix cores, ROCm compatibility, and MI250X software support.
- [08_Research_Papers](08_Research_Papers/): architecture and data-movement research, currently focused on topology and bandwidth.
- [09_AI_Notes](09_AI_Notes/): topic notes for architecture, PCIe, power, cooling, clocking, management, ideas, questions, and unknowns.
- [13_Reference_Docs](13_Reference_Docs/): local indexes and reference material for AMD, ROCm, OAM/OCP, Molex, cooling, firmware, memory, and components.

## Known Information
- Manual project status items: gather public documentation, understand OAM, identify undocumented interfaces, create architecture, draw schematic, PCB layout, prototype.
- Manual note: undocumented behavior should be tracked as an open question rather than assumed.
- `Wanted_Documents.rtf` tracks OAM, AMD, PCIe, power, cooling, and photo references; no image files are currently present.
- MP2975 is listed as believed present on MI250X, but not visually confirmed.

## Project Roadmap
1. Documentation Collection
2. Knowledge Extraction
3. Reverse Engineering
4. Schematic Design
5. PCB Layout
6. Prototype
7. Bring-up and Validation

## Open Questions
- Mechanical, baseboard, connector, PCIe routing, REFCLK, PMBus, VRM, and OAM thermal references are listed as missing or incomplete.
- Three local PDFs could not be read because they report invalid PDF structure.

## TODO
- Keep `Wanted_Documents.rtf` aligned with files added under `13_Reference_Docs`.
- Move verified findings into `09_AI_Notes` with clear evidence and uncertainty labels.