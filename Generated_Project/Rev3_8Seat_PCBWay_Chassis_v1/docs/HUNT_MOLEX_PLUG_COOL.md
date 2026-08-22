# HUNT — Molex current @ 48–59.5 V, host plug 218910→CEM, MI250X cooler FRU

**Tree:** `Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/docs/`  
**Date:** 2026-08-22  
**Scope:** research only. **No pin map invented. No cooler MPN invented. Do not energize P48V.**

Ticket **167157** (Molex current-at-voltage follow-up) stays **OPEN**.

Labels:

| Label | Meaning |
|---|---|
| **Verified** | Quote or file from a URL opened this run (see [URL log](#url-log-opened-this-run)) |
| **Inferred** | Reading of those sources; not a new assignment |
| **Not found** | Hunt target missing after the sources below |

Prior hunts (not re-closed here): Rev2 `ExhaustiveSourceHunt_v1/FINDINGS.md`, `FullSendResearch_v1/docs/RESEARCH_REPORT.md`. This run re-opened catalogs, OCP PDFs, GitHub, patents, and HPE/ORNL/Cray/SuperMicro FRU pages.

---

## Bottom line

| # | Hunt target | Result |
|---|---|---|
| 1 | Written **1.2 A per contact at 48–59.5 V** on Molex **218910-1115** | **Not found** |
| 2 | Catalog path from **218910-1115** to a **CEM x16** slot | **Not found** |
| 3 | Buyable MI250X OAM cold plate / HS **MPN** at **500–560 W** | **Not found** |

Catalog 1.2 A is still a **2 oz copper thermal** line next to **30 V / 29.9 V RMS**. OCP still budgets **~1 A/pin after derating** at **1.5 oz**, and **16 A / 16 P48V pins at 44 V**. That is not a Molex sentence “1.2 A @ 48–59.5 V”. SuperMicro **CBL-MCIO-1278*** is **UBB-only** (MCIO-124p ↔ SlimSAS x8). CoolIT **CP-AMD-MI250-GPU** is a **series name**. SuperMicro **MCP-310-45802-0B** is a **mylar air shroud**. HPE Cray / Frontier DLC is **blade-welded**, not a shoppable FRU.

---

## 1. Molex 218910-1115 current at 48–59.5 V

### Target

A **written** rating of **1.2 A per used power contact at 48–59.5 V** (2 oz copper), from Molex PS/SD, UL/CSA table, patent, OCP, or a catalog line that pairs that current **with that voltage**. Ticket 167157 already has CSA **60 V at OCP P48V** (COFC **80170713**, 2026-08-18); this hunt is the **current-at-voltage** follow-up only.

### What catalogs still print (Verified)

Opened Farnell sheet https://www.farnell.com/datasheets/3919676.pdf (generated 01/05/2023):

> Current - Maximum per Contact **0.75A (1 Oz Cu Trace), 1.0A (1.5 Oz Cu Trace), 1.2A (2 Oz Cu Trace)**  
> Voltage - Maximum **30V AC (RMS)/DC**  
> Product Specification **2189100001-PS-000** · Sales Drawing **2189101115-SD-000**

Opened Molex 15×11 datasheet https://www.content.molex.com/dxresources/3d6e/3d6e8b6f-430d-49cd-b843-a6374232eb3c.pdf (Order No. **987652-0673 Rev. 2**, 2023.08):

> Voltage (max.): **29.9V AC RMS**  
> Current (max. per contact): Mirror Mezz, Mirror Mezz Pro: **1.0A** · Mirror Mezz Enhanced: 0.75A  
> Dielectric Withstanding Voltage: **500V DC**

Opened Molex customer presentation https://www.content.molex.com/dxresources/1b7b/1b7b49e5-2def-4843-a9ed-656713e84952.pdf:

> Voltage **29.9V AC RMS**  
> Current (max. per contact) **0.75A for 1 oz. Copper · 1.2A for 2 oz. Copper**

Opened Molex OCP flyer https://www.content.molex.com/dxresources/7f7b/7f7b6bdf-bb6d-4339-b836-185ec7a3b999.pdf (Order No. **987652-2211 Rev. 1**, 2024.08):

> **1.0A per pin @ 1.5oz. Copper after derating**  
> Supports either **12V or 48V** input · Up to 200W (12V) or **500W (48V)**

The flyer’s **48 V / 500 W** is **marketing for the OAM ecosystem**. It does **not** rewrite the catalog **30 V / 29.9 V RMS** line, and it states **1.0 A @ 1.5 oz after derating**, not **1.2 A @ 48–59.5 V**.

### What OCP writes (Verified)

Opened OAM Design Spec v1.5 https://www.opencompute.org/documents/ocp-accelerator-module-design-specification-v1p5-final-20220223-docx-1-pdf Table 3:

> Current Rating per pin @80C ambient temp, 1.5oz copper **1A/pin after 20% derating**  
> Max Voltage Application **30V AC (OAM supports 60V after Molex’s pin assignment review)**  
> Withstand voltage **500V min**

Same PDF, power table (P48V):

> P48V **44V min to 60V max**, **16** pins, **16A (when at 44V)**

Same PDF, thermal:

> An air-cooled solution recommends TDP equal to or less than **450W** modules. For modules that are over 450W, consider other solutions such as liquid cooling.  
> … maximum module power that air cooling can support is approximately **450W**.

Arithmetic **16 A / 16 pins = 1 A/pin at 44 V** matches Table 3 and the Farnell **1.0 A @ 1.5 oz** cell. It is **not** a written **1.2 A @ 48–59.5 V**. The 60 V clause is still **“after Molex’s pin assignment review”**, not a current table at 48–59.5 V.

OAM r2.0 v1.0 (opened https://www.opencompute.org/documents/oai-oam-base-specification-r2-0-v1-0-20230919-pdf) still names **218910-1115** and **44V–59.5V** input. **r2.0 pinlists remain UNUSABLE** for this chassis (P3V3=6). It does **not** add a 1.2 A @ 48–59.5 V Molex rating.

### Product spec PDF **2189100001-PS-000**

**Not retrieved.** Direct `molex.com/pdm_docs/ps/2189100001-PS*.pdf` and sales-drawing URLs failed this run (`curl` HTTP/2 `INTERNAL_ERROR`, HTTP 000). Internet Archive CDX `molex.com/*2189100001*` returned **`[]`**. Wrong-path guess `content.molex.com/dxresources/9876/987652-0673.pdf` was **404 JSON**; the real **987652-0673** file is the 15×11 datasheet above (still **29.9 V / 1.0 A**).

### Patents (opened)

| Patent | Opened | What it is **not** |
|---|---|---|
| US11955753B2 Molex “Connector assembly” | https://patents.google.com/patent/US11955753B2/en | Hermaphroditic wafers. **No** 218910-1115, **no** 1.2 A, **no** 48 V table. |
| USD994612S1 Molex connector design | https://patents.google.com/patent/USD994612S1/en | Design patent. No electrical ratings. |
| US5035639A / US4330164A / US5718599A | hermaphroditic connectors in general | Not Mirror Mezz Pro, not OCP P48V. |
| US10874032B2 rotatable cold plate | https://patents.google.com/patent/US10874032B2/en | Pluggable-module cooling. Not 218910 current. |
| US7502882B2 AMC adapter | https://patents.google.com/patent/US7502882B2/en | Advanced Mezzanine Card → CEM. **Not** OAM. |

No opened patent writes **1.2 A @ 48–59.5 V** for **218910-1115**.

### GitHub (opened)

| Probe | Result |
|---|---|
| https://github.com/search?q=%22218910-1115%22&type=repositories | **0** repositories |
| https://github.com/search?q=218910-1115&type=code | Sign-in wall (logged-out) |
| `gh search code "218910-1115"` | HTTP **429** |
| https://github.com/opencomputeproject/OCP-SVR-OAI-Open_Accelerator_Infrastructure | Public tree is **LICENSE + README.md only** (API contents opened) |
| README https://raw.githubusercontent.com/opencomputeproject/OCP-SVR-OAI-Open_Accelerator_Infrastructure/main/README.md | Workgroup history. **No** PS table, **no** 1.2 A @ 48 V |

### Verdict — Q1

**Not found.** Catalog **1.2 A** remains a **2 oz copper** current, printed next to **30 V**. OCP **1 A/pin after 20% derating (1.5 oz)** and **16 A @ 44 V on 16 P48V pins** are system budgets, not a Molex “1.2 A @ 48–59.5 V” write-up. Ticket **167157** current-at-voltage stays **OPEN**. **DO NOT ENERGIZE P48V.**

---

## 2. Host plug: catalog path from Molex 218910-1115 to a CEM x16 slot

### Target

A **buyable catalog product** whose **one end is 218910-1115** (or a documented mate of that MPN) and whose **other end is a PCIe CEM x16** edge / slot, with a **published** PE map. Do **not** invent a PE-to-CEM map.

### What 218910-1115 actually mates (Verified)

Farnell sheet (opened): **Mates With 2189101115**. Application **Board-to-Board**. Hermaphroditic PCB header, BGA attach, 688 circuits.

OAM v1.5 §6.2 (opened):

> Molex Mirror Mezz Pro (MPN: **218910-1115**) is the **PCB to PCB interconnect** solution supported by the OAM form factor.

Molex OAI flyer https://www.content.molex.com/dxresources/a1db/a1db6e3c-33dd-42cb-b71b-253427bec4c7.pdf (opened) argues **against** PCIe CEM for accelerators (insertion loss, cabling, topology) and presents Mirror Mezz as the **mezzanine** alternative. Complementary “copper flex” is named in the 1b7b presentation as a **family talking point**, not an orderable **218910-to-CEM** SKU.

There is **no** catalog plug that is 218910-1115 on one end and CEM on the other. The mezz is SMT to the module and SMT to the baseboard.

### Official OAI host path is **not** CEM (Verified)

Opened UBB Design Spec v1.5 https://www.opencompute.org/documents/universal-baseboard-design-specification-v1p5-final-20220223-docx-pdf:

> There are eight x16 SerDes links dedicated for host interface connections. Each OAM module on the UBB routes an x16 link to a dedicated **ExaMAX** connector … which connects to the **Host Interface Board (HIB)**.

That is **218910 (OAM↔UBB) → traces → ExaMAX → HIB**. It is **not** a CEM x16 card. No PE-to-CEM map is taken from this.

### SuperMicro **CBL-MCIO-1278*** is UBB-only (Verified)

Opened SuperMicro MNL-2507 https://www.supermicro.com/manuals/superserver/4U/MNL-2507.pdf optional MI250 GPU kit:

| PN | Description |
|---|---|
| **CBL-MCIO-1278S5FYB1** | MCIO cable for UBB |
| **CBL-MCIO-1278S5FYB2** | MCIO cable for UBB |
| **CBL-PWEX-1280** | Power cable for UBB (not the mezz) |

Opened Wiredzone https://www.wiredzone.com/shop/product/10026108-supermicro-cbl-mcio-1278s5fyb2-cable-kit-for-gpu-mi-200-11130:

> Connectors: **4 MCIO-124p** to **2 SlimSAS X8 E-H** · Compatible With **MI-200**

Opened Tech Standard Solutions parts list https://techstandardsolutions.com/servers/supermicro/4u-5u-universal-gpu-systems/as-4124gq-tnmi-in-5u-2/: same two kits, **A-D** and **E-H**, on the **MI250 GPU Kit** with UBB **AOM-MCM-Q-P**.

**Starts at MCIO-124p, not at 218910-1115.** Other side is **SlimSAS x8**, not a CEM x16 gold finger. X11DPH-T has **no onboard MCIO**. Do not treat this cable as the host plug for this chassis.

### MCIO/SlimSAS ↔ CEM products exist — they start at MCIO/SlimSAS (Verified)

These are real catalog cards. They are **not** a 218910→CEM path. **No PE-to-CEM map is copied from them.**

| Product | Opened | Honest use |
|---|---|---|
| TI **CEM2SLIMSAS-EVM** | https://www.ti.com/tool/CEM2SLIMSAS-EVM | “CEM-to-SlimSAS PCI-Express 4.0 adapter” for **U.2 SSDs** via SlimSAS→U.2 cables. SFF-8654 **storage**. |
| Teledyne/i-wave **PE-G5-MCIO124Pin-X16SLOT-X** | https://i-wave.com/wp-content/uploads/0124-MCIO.pdf | “Allows **MCIO cables** to connect to PCI Express slots” for **test/debug**. Ordering: MCIO **124/148/74/38** pin host adapters. **Starts at MCIO SFF-TA-1016.** |

### Community (supporting only)

Opened https://forum.level1techs.com/t/someone-needs-to-figure-out-how-to-adapt-mi250-gpus-to-pcie/250596 (2026-05/06). Thread asks for a PCIe adaptation; posters state OAM ≠ SXM and that a CEM product is **not** on the shelf. **Not** a catalog path.

### Patents / GitHub

US7502882B2 is an **AMC** (Advanced Mezzanine Card) adapter to a carrier — different standard. GitHub public OCP-OAI tree has **no** adapter gerber/pinout. Repo search for `"218910-1115"` = **0**.

### Verdict — Q2

**Not found.** There is no catalog SKU from **218910-1115** to **CEM x16**. MCIO-to-CEM exists and is documented; it **starts at MCIO**. SuperMicro **CBL-MCIO-1278*** is **UBB MCIO↔SlimSAS**, MI-200 only. **No PE-to-CEM map is invented here.** Host keepout on this chassis stays unnamed.

---

## 3. Buyable MI250X OAM cold plate / HS MPN at 500–560 W

### Target

An **orderable FRU / catalog MPN** that is a **die-mating** cold plate or heatsink for **MI250X OAM** at **500–560 W**. Not a shroud, tray, stiffener, CPU sink, or a marketing series name.

### AMD TDP (prior Verified; product HTML timed out this run)

Instinct MI200 datasheet (prior 200; this-run fetch of https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/instinct-mi200-datasheet.pdf **timed out**): **500 W & 560 W TDP**, Passive OAM. Cooling ICD / bolster MPN **not** in that public sheet (prior hunt).

### OCP air ~450 W (Verified)

OAM v1.5 (opened): air on a shadowed 8× tray **~450 W**. MI250X **500/560 W** is **above** that note. That is a **limit**, not a buyable HS PN.

### SuperMicro FRU list — shroud, not a die HS (Verified)

Opened MNL-2507 + Tech Standard Solutions kit table. MI250 GPU kit thermal/mechanical lines:

| PN | Printed description | Die-mating HS? |
|---|---|---|
| **MCP-310-45802-0B** | “Black **4pcs mylar airshroud** kit for MI200 installion in CSE-458G” / MNL-2507 “GPU Air Shroud for AMD MI250” | **No** — mylar duct |
| **MCP-240-45801-0N** | Metal **stiffener** bracket for MI200 UBB | **No** |
| **MCP-240-45809-0N** | **Sheet-metal tray** for MI200/PVC UBB | **No** |
| **GPU-AMDMI250-OAM-0029H** | AMD Instinct MI250 OAM 64GBx2 **530W** | The **module**, not a cooler |
| **SNK-P1043V** / **SNK-P0063P** | 1U / 2U **CPU** heat sink (SP3) | **No** — CPU |
| **MCP-310-45801-0B** | 4U **plastic air shroud** (motherboard/CPU path) | **No** |

MNL-2507 install text (opened): “Three GPU air shrouds **funnel cooling air** to the GPUs. The GPU air shroud kit contains a sponge … to support the UBB.” That is **air ducting**, not a 500–560 W bolster plate.

### CoolIT **CP-AMD-MI250-GPU** is a series name (Verified)

Opened https://www.coolitsystems.com/amd-coldplates/:

> **CP-AMD-MI250-GPU Series** · ### for MI250  
> Engineered for legacy HPC systems, MI250 coldplates provide reliable cooling for dual-GPU configurations …

**No** orderable SKU, **no** 500/560 W rating, **no** buy/quote MPN, **no** datasheet PDF linked from that page. Same page uses the same “Series” pattern for MI300X / MI355 / SP5. **Do not treat the series title as a shoppable FRU.**

### HPE PartSurfer / ORNL / Cray (Verified)

| Query (opened) | Result |
|---|---|
| https://partsurfer.hpe.com/Search.aspx?searchText=EX235a | **“No additional information for EX235a found in PartSurfer.”** Page is HPE Internal / ASP login. |
| https://partsurfer.hpe.com/Search.aspx?searchText=MI250X | **No additional information.** |
| https://partsurfer.hpe.com/Search.aspx?searchText=P41933-001 | **P41933-001** · **SPS-PCA AMD MI200 ORNL OAM** |

**P41933-001 is the OAM PCA spare** (ORNL / Frontier class module), **not** a cold plate.

Opened HPE Cray Supercomputing EX QuickSpecs https://www.hpe.com/us/en/collaterals/collateral.a00094635enw.html (v20, 05-May-2025):

> direct attached liquid cooled cold plates provide for efficient heat removal from high power devices including processors, **GPUs**, and switches  
> … **Deleted discontinued blades EX425, EX235a and EX235n**  
> HPE provides **critical spare parts** … onsite or regional depots. Customers may elect to **supplement the HPE-owned spare parts inventory**.

No GPU-cold-plate **MPN** is listed. EX235a is **removed** from the current public quickspec. Spares are **depot / ASP**, not a catalog FRU.

Opened OSTI Frontier cooling paper https://www.osti.gov/servlets/purl/3013860:

> The Frontier compute blade uses a **cold-plate design** with tightly controlled impedances …

Opened OLCF Frontier user guide https://docs.olcf.ornl.gov/systems/frontier_user_guide.html: node = 4× MI250X, architecture and programming. **No** cooler FRU.

Opened ICL-UT-22-05 https://icl.utk.edu/files/publications/2022/icl-utk-1570-2022.pdf: EX235a node description, **560W per GPU**. **No** plate MPN.

Opened STH SC21 https://www.servethehome.com/behold-the-amd-instinct-mi250x-oam-at-sc21/:

> One can see the **liquid cooling plates** on all of the main components of the OAM GPUs.

Photographs of **HPE Cray EX235a welded DLC**, not a part number.

CUG 2024 LRZ EX235a slides (search-pipeline text; direct PDF fetch **timed out** this run): “GPU Coldplates”, “Flexible Tubing for Component Serviceability”, “Dripless Quick Disconnects”. Still **no MPN**.

### Patents (opened)

US10874032B2, US12096595B2, US9490188B2, WO2024072853A1 discuss cold plates in general / busbar tiles. **None** assigns an orderable **MI250X OAM 500–560 W** FRU.

### GitHub

OCP-OAI public repo: no mechanical HS files. Repo search `"218910-1115"` = 0. No public “MI250X cold plate” MPN in opened GitHub.

### Verdict — Q3

**Not found.** SuperMicro **MCP-310-45802-0B** is a **mylar shroud**. CoolIT **CP-AMD-MI250-GPU** is a **series name**, not an orderable SKU. HPE/ORNL/Cray DLC is **blade-integrated**; PartSurfer lists **P41933-001** as the **ORNL OAM PCA**, not a plate. OCP air **~450 W** is below MI250X **500/560 W**. **No cooler MPN is invented here.** Do not shop a custom die clamp onto the chassis BOM.

---

## What this hunt did **not** do

- Did **not** invent a 218910 ↔ CEM / SlimSAS / MCIO pin map.
- Did **not** invent a PE lane map onto a CEM edge.
- Did **not** invent a cold-plate or heatsink MPN.
- Did **not** treat catalog **1.2 A (2 oz)** as a 48–59.5 V rating.
- Did **not** treat ticket 167157 CSA 60 V as closing **current**.

Energize remains blocked on Molex **1.2 A/contact at 48–59.5 V**. Host plug stays a keepout. Cooling stays off this PCB.

---

## URL log (opened this run)

| HTTP / note | URL |
|---|---|
| **200** PDF | https://www.farnell.com/datasheets/3919676.pdf |
| **200** PDF | https://www.content.molex.com/dxresources/3d6e/3d6e8b6f-430d-49cd-b843-a6374232eb3c.pdf |
| **200** PDF | https://www.content.molex.com/dxresources/1b7b/1b7b49e5-2def-4843-a9ed-656713e84952.pdf |
| **200** PDF | https://www.content.molex.com/dxresources/7f7b/7f7b6bdf-bb6d-4339-b836-185ec7a3b999.pdf |
| **200** PDF | https://www.content.molex.com/dxresources/a1db/a1db6e3c-33dd-42cb-b71b-253427bec4c7.pdf |
| **404** JSON | https://www.content.molex.com/dxresources/9876/987652-0673.pdf |
| **000** HTTP/2 fail | https://www.molex.com/pdm_docs/ps/2189100001-PS.pdf (and PS-000, SD, part-detail) |
| **200** `[]` | https://web.archive.org/cdx/search/cdx?url=molex.com/*2189100001*&output=json&limit=30 |
| **200** | https://www.opencompute.org/documents/ocp-accelerator-module-design-specification-v1p5-final-20220223-docx-1-pdf |
| **200** | https://www.opencompute.org/documents/oai-oam-base-specification-r2-0-v1-0-20230919-pdf |
| **200** | https://www.opencompute.org/documents/universal-baseboard-design-specification-v1p5-final-20220223-docx-pdf |
| **200** | https://www.scribd.com/document/736152587/ocp-accelerator-module-design-specification-v1p5-Final-20220223-docx-1 |
| **200** PDF | https://www.supermicro.com/manuals/superserver/4U/MNL-2507.pdf |
| **200** | https://www.supermicro.com/en/products/system/datasheet/as-4124gq-tnmi |
| **200** | https://techstandardsolutions.com/servers/supermicro/4u-5u-universal-gpu-systems/as-4124gq-tnmi-in-5u-2/ |
| **200** | https://www.wiredzone.com/shop/product/10026108-supermicro-cbl-mcio-1278s5fyb2-cable-kit-for-gpu-mi-200-11130 |
| timeout | https://www.wiredzone.com/shop/product/10026107-supermicro-cbl-mcio-1278s5fyb1-cable-kit-for-gpu-mi-200-11129 |
| **200** | https://www.ti.com/tool/CEM2SLIMSAS-EVM |
| **200** PDF | https://i-wave.com/wp-content/uploads/0124-MCIO.pdf |
| **200** | https://www.coolitsystems.com/amd-coldplates/ |
| **200** | https://partsurfer.hpe.com/Search.aspx?searchText=EX235a |
| **200** | https://partsurfer.hpe.com/Search.aspx?searchText=MI250X |
| **200** | https://partsurfer.hpe.com/Search.aspx?searchText=P41933-001 |
| **200** | https://www.hpe.com/us/en/collaterals/collateral.a00094635enw.html |
| **200** PDF | https://www.osti.gov/servlets/purl/3013860 |
| **200** | https://docs.olcf.ornl.gov/systems/frontier_user_guide.html |
| **200** PDF | https://icl.utk.edu/files/publications/2022/icl-utk-1570-2022.pdf |
| **200** | https://www.servethehome.com/behold-the-amd-instinct-mi250x-oam-at-sc21/ |
| timeout | https://cug.org/proceedings/cug2024_proceedings/includes/files/pres106s2.pdf (snippets via search pipeline) |
| timeout | https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/instinct-mi200-datasheet.pdf |
| timeout | https://www.amd.com/en/products/accelerators/instinct/mi200/mi250x.html |
| **200** | https://github.com/opencomputeproject/OCP-SVR-OAI-Open_Accelerator_Infrastructure |
| **200** JSON | https://api.github.com/repos/opencomputeproject/OCP-SVR-OAI-Open_Accelerator_Infrastructure/contents |
| **200** | https://raw.githubusercontent.com/opencomputeproject/OCP-SVR-OAI-Open_Accelerator_Infrastructure/main/README.md |
| **200** 0 repos | https://github.com/search?q=%22218910-1115%22&type=repositories |
| sign-in | https://github.com/search?q=218910-1115&type=code |
| **429** | GitHub code search API `218910-1115` |
| **200** | https://patents.google.com/patent/US11955753B2/en |
| **200** | https://patents.google.com/patent/USD994612S1/en |
| **200** | https://patents.google.com/patent/US10874032B2/en |
| **200** | https://patents.google.com/patent/US7502882B2/en |
| **200** | https://patents.google.com/patent/US12096595B2 |
| **200** | https://patents.google.com/patent/US9490188B2/en |
| **200** | https://patents.google.com/patent/WO2024072853A1 |
| **200** | https://forum.level1techs.com/t/someone-needs-to-figure-out-how-to-adapt-mi250-gpus-to-pcie/250596 |
| timeout | https://www.mouser.com/ProductDetail/Molex/218910-1115 |
| timeout | https://www.tti.com/content/ttiinc/en/manufacturers/molex/products/molex-mirror-mezz-pro-connectors.html |
| timeout | https://www.molex.com/en-us/products/connectors/card-edge-connectors/mini-cool-edge |

**DO NOT ENERGIZE. Do not invent a cable pin map or a cooler MPN.**
