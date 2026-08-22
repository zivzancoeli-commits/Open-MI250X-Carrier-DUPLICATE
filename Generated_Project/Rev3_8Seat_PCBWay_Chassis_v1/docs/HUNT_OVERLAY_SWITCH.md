# Public-source hunt — MI250X OAM overlay and Switchtec/PEX ball maps

**Date:** 2026-08-22  
**Tree:** `Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/docs/`  
**Scope:** Research only. Re-search patents, GitHub, academia, Wayback, AMD/OCP, Microchip/Broadcom, and distributor/CAD sites for (1) an AMD Instinct MI250X pad-to-OCP overlay / UG1729 PDF and (2) a public ball/pin file for PM8536 / PM8536B-FEI / other 1311-ball Switchtec / PEX8796.  
**Do not:** invent pin maps, guess PE tracks, import r2.0, or route copper from this hunt.

Evidence labels:

| Label | Meaning |
|---|---|
| **Verified** | Direct quote, HTTP retrieval, or machine extraction from a retrieved file this run |
| **Inferred** | Reasonable reading of those sources, not a new pin assignment |
| **Unknown** | Not found in public sources this run |

Full HTTP log: [`HUNT_OVERLAY_SWITCH_URLS.md`](HUNT_OVERLAY_SWITCH_URLS.md) (105 unique URLs).

Prior in-repo hunts this re-check agrees with: `22_Pinmap_Research/REPORT.md` (OCP **generic** v1.0 688+688 map; not AMD overlay); `Generated_Project/Rev2_MI250X_Carrier_ExhaustiveSourceHunt_v1/FINDINGS.md`.

---

## Bottom line

| Target | Result | Label |
|---|---|---|
| AMD Instinct MI250X OAM pad overlay (TEST\*/RFU/GPIO/GCD1/xGMI → Molex pads) | **NOT FOUND** as a public pad-to-OCP map | Verified (absence of public file) |
| UG1729 PDF / design collateral | **NOT FOUND.** UG1729 is still a **TIP landing page** (Document Type = Landing Page, release **2025-01-23**). Instinct docs call it **NDA, login required**. No leaked PDF this run. | Verified |
| OCP v1.x 688-contact map | Exists and is already in-repo (`OAM Pin map rev 1.0.xlsx`). **Generic Intel/Facebook 2019 map, not an MI250X overlay.** | Verified |
| OCP r2.0 pinlist | Exists as a named spreadsheet in the r2.0 spec. **UNUSABLE for MI250X** (P3V3 = 6 vs v1.x P3V3 = 2). Not retrieved this run. | Verified (prior) / not re-downloaded |
| PM8536 / PM8536B-FEI / other 1311-ball Switchtec ball/pin file | **NOT FOUND.** Public files give **package size only** (1311-pin, 37.5×37.5 mm, 1.0 mm). IBIS/board-design slots on microchip.com are empty without myMicrochip. | Verified |
| PEX8796 public ball/pin file | **NOT FOUND** as an authorized Broadcom public pin file. Official public doc is a **5-page product brief**: **1156-ball 35×35 mm FCBGA**, no ball map. Different package from PM8536. | Verified |

**Path that still applies:** AMD sales / NDA Technical Information Portal (UG1729 collateral), with OCP OAI co-lead **Song Kok Hang** (AMD, Instinct Platform Architecture; OCP contact `song-kok.hang@ocproject.net`). Microchip sales / myMicrochip NDA for Switchtec PFX hardware design files. Broadcom support portal for PEX data books.

This hunt does **not** authorize stuffing SW0–SW3, assigning GCD1, routing S1–S7, or drawing PE tracks.

---

## 1) AMD Instinct MI250X OAM pad overlay / UG1729

### 1.1 What would count as a hit

A citable map that names **AMD functions** on the 688+688 Molex pads (especially TEST0–TEST14, TEST_MODE#, RFU, DO_NOT_USE, GPIO, dual-GCD host PE, which S1–S7 are xGMI). The in-repo OCP generic v1.0 spreadsheet is **not** that overlay.

### 1.2 UG1729 — still TIP-only

| Item | Evidence | Label |
|---|---|---|
| Landing URL | https://docs.amd.com/v/u/en-US/ug1729-amd-instinct-accelerators — HTTP **200**, 1489 B SPA shell titled “AMD Technical Information Portal” | Verified |
| Khub HTML | https://docs.amd.com/api/khub/documents/vamCNI5rs9s1e0SNR3xBlw/content — HTTP **200**, 9863 B | Verified |
| Document ID / type / date | Embedded control XML: `Document ID = UG1729`; `Document Type = Landing Page`; `Release Date = 2025-01-23`; `isLatest = true`; `ft:description = This page includes documentation for AMD Instinct accelerators.` | Verified |
| Login wall (quote) | *“Logging into the AMD Technical Information Portal is necessary to access the collateral. If you're signed in but can't find the content you expect, please reach out to your AMD representative.”* | Verified |
| Public cards | Boxes for All MI Series / MI350 / MI325X / MI300X / MI300A / **MI200 Series (MI200, MI210, MI250)** / MI100 and earlier. Each is a **filtered TIP search**, not a PDF. | Verified |
| Instinct docs pointer | https://instinct.docs.amd.com/latest/ and `ROCm/instinct-docs` index: *“Additional **NDA** technical documentation, software, and design collateral for AMD Instinct products; **Login Required**”* linking the same UG1729 URL | Verified |
| Alternate UG1729 paths | `/r/en-US/ug1729-amd-instinct-accelerators` **404**; `/v/u/en-US/ug1729` **404**; AMD.com search **ERR/404**; TIP `/search/all?query=UG1729` **200** but 2598 B Fluid Topics loader (no PDF) | Verified |
| Leaked UG1729 PDF | Web search + GitHub repo search `UG1729` **0** public repos. No `filetype:pdf` hit that is the TIP collateral. | Verified (this run) |

**NOT FOUND:** UG1729 as a retrievable PDF or HTML design guide with pad tables.

### 1.3 Public AMD / Instinct / ROCm (no overlay)

Retrieved or confirmed this run:

| URL | HTTP | What it contains | Overlay? |
|---|---|---|---|
| https://www.amd.com/en/products/accelerators/instinct/mi200/mi250x.html | 200 (retry) | Product page: OAM module, PCIe 4.0 x16, 8 Infinity Fabric links, 100 GB/s, passive OAM | No |
| https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/instinct-mi200-datasheet.pdf | 200, 2 pages, 1 011 276 B | MI200 series datasheet: form factor **OAM**, bus **PCIe Gen 4**, TDP 500/560 W. **Zero** occurrences of “pin”, “overlay”, “connector”, “688” | No |
| https://www.amd.com/content/dam/amd/en/documents/instinct-business-docs/white-papers/amd-cdna2-white-paper.pdf | 200 | Architecture / node diagrams | No |
| https://instinct.docs.amd.com/projects/system-acceptance/en/latest/gpus/mi250.html | 200 | Customer acceptance: dual GCD, xGMI mesh, `1002:740c`. Software/health checks, not pads | No |
| https://instinct.docs.amd.com/projects/MI3XX-reference/latest/index.html | 200 | **MI3XX** cluster networking (fat tree / rail). Not MI250X OAM ICD | No |
| Hot Chips 34 Alan Smith PDF | 200 | Node topologies (2× x16 host links per OAM, xGMI). Block diagrams, not Molex pads | No |
| https://github.com/ROCm/instinct-docs | 200 | Public ops docs + UG1729 NDA card | No |
| https://github.com/ROCm/ROCm `docs/conceptual/gpu-arch/mi250.md` | search hit | Same architecture text: each GCD may attach x16 or x8 | No pad numbers |

Architectural statements that remain **not** a pin map (do not assign S1–S7 from these):

- Each MI250/MI250X OAM has **two GCDs**; each GCD can have its own host x16 (some platforms x8).
- Cross-OAM xGMI is drawn as colored links in public node figures.
- Those figures do not name Conn0/Conn1 pads.

### 1.4 OCP — still generic v1.x; r2.0 UNUSABLE

Live OCP wiki/PDF URLs returned **403** (Cloudflare) this run. Content is already extracted in-repo and in search snippets:

| Source | Pad-to-OCP map? |
|---|---|
| OAM Design Spec v1.5 §8.3: *“The detailed pin mapping to connectors is in the separated spreadsheet.”* Table 4 = **counts** (P3V3 **Required 2 Conn0**) | Counts only |
| `OAM Pin map rev 1.0.xlsx` (in-repo from Level1Techs zip) | **Yes — generic v1.0**, not AMD overlay |
| OAI-OAM r2.0: names `OAI OAM_Pinlist_Pinmap_r2.0_v1.0.xlsx`; P3V3 = **6** | r2.0 **UNUSABLE** for MI250X |
| https://github.com/opencomputeproject/OCP-SVR-OAI-Open_Accelerator_Infrastructure | HTTP 200 project page; **no xlsx** in the public tree |
| Facebook Engineering 2019 OAM announcement | Form factor / power / link counts | No pad table |
| Intel Nervana NNP L-1000 OCP talk (Song Kok Hang) | Vendor **NNP-T** pinmap slides exist for **Intel’s** module, not MI250X | Not AMD overlay |

**NOT FOUND:** any public file titled or functioning as “AMD Instinct MI250X OAM overlay” on top of the generic map.

### 1.5 Patents

Tried Google Patents queries (`OCP Accelerator Module pin map`, `"MI250X" OAM connector`, `Switchtec PM8536 ball`). Search result pages were JS shells (~4 KB) with no extractable hit list from this environment. Specific patents retrieved:

| Patent | HTTP | Overlay? |
|---|---|---|
| [US20230006374A1](https://patents.google.com/patent/US20230006374A1) (CAMM / compression memory) | 200 | Unrelated |
| [CN116166599A](https://patents.google.com/patent/CN116166599A/en) (multi-CPLD SGPIO; mentions UBB `OAM_ALERT` / `OAM_PWRGD`) | 200 | Board-management signals, **not** 688-pad overlay |
| Optical “OAM&P” transceiver patents | 200 | Wrong expansion of OAM |

**NOT FOUND:** a patent that publishes the MI250X 688-pad overlay.

### 1.6 Academia / supercomputer docs

| Source | HTTP | Overlay? |
|---|---|---|
| arXiv [2302.14827](https://arxiv.org/abs/2302.14827) (Sandia / Crusher MI250x interconnect) | 200 PDF | Bandwidth tables; no connector pads |
| arXiv [2410.00801](https://arxiv.org/html/2410.00801) | 200 | Infinity Fabric data movement |
| IEEE `10185224` (MI250X Elevated Fanout Bridge **package**) | 202 empty (paywall) | Title = on-package EFB, not OAM mezz |
| OLCF Frontier user guide | search/GitHub | Node/GCD software model; photo of OAM, no pad table |
| SuperMicro MNL-2507 | cited | AOM-MCM-Q-P UBB presence; **no** OAM mezz pinout |

**NOT FOUND** in academic PDFs this run.

### 1.7 Wayback

All CDX/snapshot requests to `web.archive.org` for UG1729 and OCP pin xlsx returned **HTTP 429** (rate limit) this run. Prior hunt already documented IA CDX **200** hits for the **generic** v1.0/v1.1 OCP xlsx (token `938c61e5b1d3c5c2b5c33f95525b1412`, etc.) and **no** UG1729 PDF original. This re-check did **not** find a new archived UG1729 PDF via web search either.

### 1.8 GitHub

| Query | Result |
|---|---|
| GitHub **code** search (`PM8536B-FEI`, `UG1729`, ball map) | HTML requires **sign-in**; no file list returned |
| `GET https://api.github.com/search/repositories?q=UG1729` | `total_count: 0` |
| `GET ...?q=PM8536` / `PEX8796` | `total_count: 0` |
| `ROCm/instinct-docs` | NDA card only |
| `opencomputeproject/OCP-SVR-OAI-...` + pinmap search | Redirect to GitHub search; no public xlsx |

### 1.9 OEM / community (still no continuity table)

Level1Techs thread https://forum.level1techs.com/t/someone-needs-to-figure-out-how-to-adapt-mi250-gpus-to-pcie/250596 — HTTP 200. Discussion of AOM-MCM-Q, power, EEPROM **0x50**. Prior hunt: post 95 is the **OCP v1.0 zip**, not AMD overlay. SuperMicro/HPE listings name **AOM-MCM-Q-P** / P41933-001. GrabCAD OAM queries **403**.

### 1.10 How to obtain the overlay (unchanged)

| File | Path | Access |
|---|---|---|
| Instinct hardware ICD / OAM overlay / UG1729 collateral | AMD Technical Information Portal (UG1729 landing → MI200/MI250 filters) or AMD sales | **NDA / login** |
| Human contact | Song Kok Hang, Senior Director — Instinct Platform Architecture (AMD); OCP OAI co-lead `song-kok.hang@ocproject.net`; Ahmed AbouAlfotouh `Ahmed.AbouAlfotouh@amd.com` (OCP wiki) | Sales / OCP |
| Generic v1.x pad map | Already in `22_Pinmap_Research/` | Public, **not** overlay |

---

## 2) PM8536 / 1311-ball Switchtec / PEX8796 ball/pin file

### 2.1 What would count as a hit

A citable ball-to-signal table (IBIS `.ibs`, vendor pinlist CSV/xlsx, or datasheet chapter with PETp/n ↔ ball IDs) for:

- **PM8536B-FEI** (PRIMARY DNP on this chassis), or
- another **1311-ball** Switchtec in the same 37.5 mm FCBGA (PM8534/8535/8544/8545/8546/8574/8575/8576 family), or
- **PEX8796** if a public pin file exists (note: public brief says **1156-ball**, not 1311).

Package size alone is **not** a pin file.

### 2.2 Public Microchip / distributor files — package only

| File | HTTP | Pages | Ball map? |
|---|---|---|---|
| http://ww1.microchip.com/downloads/en/DeviceDoc/00002849A.pdf (PFX/PFX-I product brief) | 200, 321 372 B, **2 pages** | Ordering: PM8536B-FEI **37.5 mm × 37.5 mm**. No 1311 count in this brief, no balls | **No** |
| https://media.digikey.com/pdf/data%20sheets/microsemi%20pdfs/pm853x_pfx_pcie_series.pdf (PMC-2152150 product brief) | 200, 180 023 B, **2 pages** | Same family table; keywords include PM8536. **No pin assignment** | **No** |
| Digi-Key / chipsfind “PCIe Solutions Brochure” (same 1 773 917 B PDF) | 200 | Marketing table: **PM8534/8535/8536 = 1311-pin, 37.5×37.5 mm, 1 mm pitch**. Still not a ball map | **No** |
| https://www.microchip.com/en-us/product/pm8536 | **403** here; WebFetch showed empty Documentation table; Design Resources lists IBIS/board-design **slots** with no public files | Login | **No** |
| Mouser / Digi-Key product pages | 200/403 | Distributor copy: “1311-Pin FCBGA”, “PFX 96XG3 1311 BBGA 37.5X37.5” | Size only |
| Ultra Librarian guessed path | **404** | No CAD model | **No** |
| SnapEDA / Component Search Engine | 403 / 404 | No public symbol with named balls | **No** |
| LCSC “Pinout Diagram & Footprint Diagram” C1523236 | 200 | SEO title + **placeholder** `no_goods_pic6.jpg`. No SVG ball grid, no signal names | **No** |
| Gen4/Gen5 PFX briefs `00003356B.pdf` / `00003776.pdf` | public briefs | Different families (40 mm / 29 mm), still briefs | Not this SKU |

Family sharing the **1311-ball 37.5 mm** package (brochure, **Verified** counts, **Unknown** whether ball *functions* match across SKUs — do not assume a map from 8534 applies to 8536 without a vendor file):

PM8534, PM8535, **PM8536**, PM8544, PM8545, PM8546 (and PFX-I PM8574/8575/8576). **No public ball file for any of them this run.**

Eval kit **PM5461-KIT** is mentioned in the brief (96-lane HD kit). Gerbers/schematics were **not** found on GitHub (`Microsemi/switchtec-user` is firmware/userland; device ID `0x8536` = PFX 96xG3, not a BGA map).

### 2.3 PEX8796 — different package; official public file is a brief

| File | HTTP | Ball map? |
|---|---|---|
| https://docs.broadcom.com/doc/12351860 | 200, 576 896 B, **5 pages**, Word 2010, 2013-10-07 | Quote: *“35 x 35mm², **1156-ball FCBGA** package”*. Ordering PEX8796-AB80BI G. **No ball table** |
| https://www.broadcom.com/products/pcie-switches-retimers/pcie-switches/pex8796 | 200 | Spec table: packaging 35×35 mm, 96 lanes, 24 ports. Documentation tab did not yield a public data book this run |
| Digi-Key listing | search | “PCI Express Switch IC … **1156-FBGA (35x35)**” | Size only |
| LCSC C1522693 “pinout” page | 200 | Same placeholder image pattern as PM8536 | **No** |
| GitHub `benmcollins/pex87xx` | 200 | I2C register poking for PEX8724; README asks for docs. **No BGA map** |
| `GET /search/repositories?q=PEX8796` | `total_count: 0` | |

**NOT FOUND:** authorized public PEX8796 pin/ball file. Package is **1156**, not 1311 — it is **not** a drop-in for the PM8536 courtyard even if a map appeared.

### 2.4 Unofficial EasyEDA attachment (recorded, not used)

OSHWLab project https://oshwlab.com/hawaii0707/PEX8796_PCIE_GEN3_24PORT_Switch (HTTP 200) **lists** a file named `PEX_8796-AA_AB_Data_Book_v1_0.pdf` (416 listed downloads).

HEAD of the CDN object `https://image.lceda.cn/attachments/2023/7/Ov33oQ3ldsG4hQzcrd3o403pNCj0aEyzQqPthrDI.pdf`: **200**, `Content-Type: application/pdf`, `Content-Length: 2376101` (~2.3 MB). The EasyEDA alias URL returned **403**.

This hunt **did not download, open, or transcribe** that object. A hobby-site PDF is **not** an authorized Broadcom public pin file for this chassis. Even if it were a data book, it would describe **PEX8796 1156-ball**, not PM8536 1311-ball. **Do not copy balls from it into KiCad.**

### 2.5 Patents / academia for Switchtec balls

No patent or paper retrieved this run that publishes a PM8536 / 1311-ball assignment table. Linux `switchtec` docs are MRPC/firmware, not package pins.

### 2.6 How to obtain a legal pin file

| File | Path | Access |
|---|---|---|
| Switchtec PFX hardware design guide / IBIS / ball map | myMicrochip on https://www.microchip.com/en-us/product/pm8536 (Documentation / Design Resources) | **Account + typically NDA** |
| Eval-kit design files | PM5461-KIT via Microchip sales | Controlled |
| PEX8796 Data Book / layout guide | Broadcom download portal (login); product page “Documentation” | **Account / NDA** — not the 5-page brief |

Until one of those is in hand, **U_SW0–U_SW3 stay DNP courtyards**. Escape of a 1.0 mm 1311-ball is a copper respin, not a silk ECO.

---

## 3) What this does *not* change on the chassis

- Do not assign GCD1, S1–S7, TEST\*, RFU, DO_NOT_USE from architecture diagrams.
- Do not invent PM8536 or PEX8796 balls.
- Do not mix OAM **r2.0** into this MI250X tree.
- Do not treat LCSC “pinout diagram” titles or OSHWLab attachment **filenames** as pin files.
- Named nets and DNP courtyards already on the board stay as late-bind hooks only.

---

## 4) Sources that *were* retrieved (positive, still not the maps)

Useful public facts, none of which close the two blockers:

- UG1729 exists as a **2025-01-23 landing page** that explicitly requires TIP login.
- MI200 datasheet (2 p): OAM + PCIe Gen 4; no pin table.
- OCP v1.x generic 688 map: already in `22_Pinmap_Research/` (P3V3 = Conn0 C1/C2).
- Microchip PFX brief: PM8536B-FEI, 96 lanes, 37.5 mm package.
- Brochure: that package is **1311-pin / 1.0 mm**.
- Broadcom PEX8796 brief: 96 lanes, **1156-ball 35×35 mm**, 18.6 W typical.

---

## 5) Verdict

1. **AMD MI250X OAM pad overlay / UG1729 PDF: NOT FOUND.** UG1729 remains TIP-only (Jan 2025 landing page, NDA). OCP remains generic v1.x. Path: AMD sales/NDA (Song Kok Hang).  
2. **PM8536 / 1311-ball Switchtec / PEX8796 public ball/pin file: NOT FOUND.** Package size only; vendor datasheets NDA. PEX8796 official public file is a 1156-ball product brief. Unofficial CAD-site PDFs were not used.

**Do not guess PE tracks.**
