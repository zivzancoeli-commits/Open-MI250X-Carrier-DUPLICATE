# Official 2x+ AMD Instinct MI250 / MI250X host platforms

**Count of official platforms that host at least two MI250 or MI250X modules: 3.**

This folder is a verified public-document pack, not a pin map, overlay, or cold-plate BOM. Nothing here invents connector maps, Infinity Fabric routing, or cold-plate manufacturer part numbers. MI250 and MI250X are OCP Accelerator Module (OAM) products. CEM / PCIe MI210-only boxes are excluded.

| # | Vendor | Model | GPU count / form | Cooling | Official product URL |
| --- | --- | --- | --- | --- | --- |
| 1 | Super Micro Computer (SMCI) | A+ Server **AS-4124GQ-TNMI** (4U; optional 5U kit) | **4x AMD Instinct MI250 OAM** on a UBB | Air (4U up to 560 W/GPU; 5U kit claims 700 W headroom) | https://www.supermicro.com/en/products/system/gpu/4u/as-4124gq-tnmi |
| 2 | GIGABYTE | **G262-ZO0** Rev. A00 | **4x AMD Instinct MI250 OAM** (pre-installed) | Air, 2U | https://www.gigabyte.com/Enterprise/GPU-Server/G262-ZO0-rev-A00 |
| 3 | Hewlett Packard Enterprise | **HPE Cray EX235a** accelerator blade | **4x AMD Instinct MI250X OAM per node; 2 nodes per blade = 8x MI250X OAM** | Direct liquid / cold plate (blade) | Product is EOL in current HPE Cray EX QuickSpecs (removed 05-May-2025, Version 20). Still named as the Frontier / LUMI / Adastra blade. See PDFs below. |

AMD’s 2026 Instinct partner catalog lists exactly these three as the 2x+ MI250/MI250X hosts (Gigabyte G262-ZO0, HPE Cray EX235a, SuperMicro AS-4124GQ-TNMI). SuperMicro’s own manuals state OAM, not PCIe CEM; the AMD catalog row that labels AS-4124GQ-TNMI as “PCIe” is a catalog form-factor error.

---

## 1. Super Micro AS-4124GQ-TNMI — 4x MI250 OAM

- **Vendor:** Super Micro Computer, Inc.
- **Model / SKU:** AS-4124GQ-TNMI (A+ Server 4124GQ-TNMI). Same SKU in 4U and with an optional 1U expansion kit as “AS-4124GQ-TNMI (in 5U)”.
- **Motherboard / chassis:** H12DGQ-NT6 / CSE-458GTS (manual: CSE-458GTS-R000NDP; product page: CSE-458GTS-R3K06P).
- **GPU:** 4x AMD Instinct MI250 **OAM** on universal baseboard `AOM-MCM-Q-P`. Not CEM. Not MI210. Not MI300.
- **Interconnect (as published):** AMD Infinity Fabric Link GPU–GPU; PCIe 4.0 x16 CPU–GPU.
- **Product pages:**
  - 4U: https://www.supermicro.com/en/products/system/gpu/4u/as-4124gq-tnmi
  - HTML datasheet: https://www.supermicro.com/en/products/system/datasheet/as-4124gq-tnmi
  - 5U HTML datasheet: https://www.supermicro.com/en/products/system/datasheet/as%20-4124gq-tnmi%20%28in%205u%29
  - Motherboard: https://www.supermicro.com/en/products/motherboard/h12dgq-nt6

### Downloaded PDFs

| File | What it is |
| --- | --- |
| `supermicro_AS-4124GQ-TNMI/MNL-2507_AS-4124GQ-TNMI_user_manual.pdf` | Official user manual (Rev 1.0, 134 pp). Contains 4U main parts list, **MI250 GPU kit spare list with SMCI MPNs**, 5U AIOM/PCIe kit parts, **system/motherboard block diagrams**, GPU UBB location, OAM replacement procedure, environmental/thermal operating range. Source: https://www.supermicro.com/manuals/superserver/4U/MNL-2507.pdf (this copy retrieved via Internet Archive snapshot `20221219130003` after live supermicro.com returned HTTP 403 from this environment). |
| `supermicro_AS-4124GQ-TNMI/datasheet_H12_UniversalGPU.pdf` | Official H12 Universal GPU datasheet (Sep 2022). Names AS-4124GQ-TNMI, **4x MI250 OAM**, Infinity Fabric, 4U/5U thermal headroom (560 W / 700 W). Source: https://www.supermicro.com/datasheet/datasheet_H12_UniversalGPU.pdf (Wayback). |
| `supermicro_AS-4124GQ-TNMI/datasheet_Universal_GPU.pdf` | Official Universal GPU Systems datasheet (Mar 2022). Compatibility table: **4x AMD MI250** on AS-4124GQ-TNMI vs NVIDIA HGX A100-4 on SYS-420GU-TNXR. Source: https://www.supermicro.com/datasheet/datasheet_Universal_GPU.pdf (Wayback `20220322023737`). |

Manual spare-list MPNs that **are** in MNL-2507 (copied, not invented): `GPU-AMDMI250-OAM-0029H` (qty 4), `AOM-MCM-Q-P` (UBB), `MCP-310-45802-0B` (GPU air shroud), `MCP-240-45801-0N` (stiffener), `CBL-MCIO-1278S5FYB1/B2`, `CBL-PWEX-1280`, `PWS-3K06G-2R` (qty 4). No cold-plate MPN appears; this chassis is air-cooled.

### Public but not downloaded here

- Motherboard user manual **MNL-2482** (H12DGQ-NT6), live URL https://www.supermicro.com/manuals/motherboard/EPYC7000/MNL-2482.pdf — indexed publicly and contains an H12DGQ-NT6 block diagram labeled “AMD MI200 UBB”. Live fetch from this environment returned HTTP 403; no Internet Archive snapshot of this exact PDF was found. Do not treat the missing file as a pin map.
- SuperMicro store PSU spec for `PWS-3K06G-2R` (https://store.supermicro.com/media/wysiwyg/productspecs/PWS-3K06G-2R/PWS-3K06G-2R_datasheet_08152022.pdf) — also 403 here. PSU electrical limits are already in the 4U product page and MNL-2507.

---

## 2. GIGABYTE G262-ZO0 — 4x MI250 OAM

- **Vendor:** GIGA-BYTE TECHNOLOGY CO., LTD.
- **Model:** G262-ZO0 Rev. A00. Barebone P/N `6NG262ZO0MR-00-A*`. Motherboard MZ62-HD5 Rev. 3.0.
- **GPU:** **4x AMD Instinct MI250 OAM**, 128 GB HBM2e per OAM, up to 6x GPU–GPU Infinity Links at 25 Gbps. Pre-installed. Not CEM. Not MI210.
- **Product page:** https://www.gigabyte.com/Enterprise/GPU-Server/G262-ZO0-rev-A00

### Downloaded PDFs

| File | What it is |
| --- | --- |
| `gigabyte_G262-ZO0/G262-ZO0_datasheet_v1.1.pdf` | Official 1-page datasheet. 4x MI250 OAM, dimensions, fans, dual 3000 W PSU, packaging/part numbers. Source: https://download.gigabyte.com/FileList/DataSheet/G262-ZO0_datasheet_v1.1.pdf |
| `gigabyte_G262-ZO0/server_manual_e_G262-ZO0_A00.pdf` | Official user manual Rev 1.0 (149 pp). Specs, **system block diagram** (Ch. 1-3), GPU-module removal, thermal operating range 10–35 °C. Source: https://download.gigabyte.com/FileList/Manual/server_manual_e_G262-ZO0_A00.pdf |
| `gigabyte_G262-ZO0/server_qvl_G262-ZO0.pdf` | Official QVL (CPU/memory/device qualification). Source: https://download.gigabyte.com/FileList/QVL/server_qvl_G262-ZO0.pdf |

Datasheet / product-page part numbers that **are** published (not invented): motherboard `9MZ62HD5NR-00*`, rail kit `25HB2-A86102-K0R`, CPU fansinks `25ST1-3532G0-M1R` / `25ST1-3532G1-M1R`, backplane COBP540 `9COBP540NR-00*`, front panel CFP1000 `9CFP1000NR-00*`, fans `25ST2-667630-S1R`, `25ST2-808034-S1R`, `25ST2-808035-S1R`, PSU `25EP0-230003-D0S`. No OAM cold-plate MPN (air-cooled).

The G262-ZR0 manual is NVIDIA HGX A100 Redstone, **not** MI250 — excluded.

---

## 3. HPE Cray EX235a — 4x MI250X OAM per node (8x per blade)

- **Vendor:** Hewlett Packard Enterprise (HPE Cray).
- **Model:** HPE Cray EX235a accelerator blade (also written EX235A). Water/DLC blade for HPE Cray EX cabinets (EX2500 / EX3000 / EX4000 class).
- **GPU:** **4x AMD Instinct MI250X OAM per compute node.** Two nodes per blade ⇒ **8x MI250X OAM per blade.** Coherent Infinity Fabric to an optimized 3rd Gen EPYC (“Trento”) CPU. Not CEM. Not MI210. Not MI300A (that is EX255a).
- **Status:** Discontinued in HPE Cray Supercomputing EX QuickSpecs Version 20 (05-May-2025): “Deleted discontinued blades EX425, EX235a and EX235n.” Current QuickSpecs HTML: https://www.hpe.com/us/en/collaterals/collateral.a00094635enw.html (document a00094635enw). A live PDF of an older QuickSpecs revision that still listed EX235a could not be downloaded from hpe.com/psnow from this environment (timeout / HTTP 2 RST).
- **Deployments that name this blade:** Frontier (OLCF), LUMI (EuroHPC/CSC), Adastra (GENCI/CINES), and other Top500 EX235a systems.

No public HPE EX235a **user manual** or **spare-parts catalog** was found. Do not invent blade FRUs or cold-plate MPNs. The CUG 2024 HPE/LRZ slides show GPU cold plates photographically but do not publish a vendor MPN.

### Downloaded public PDFs (architecture / thermal; not an HPE spare list)

| File | What it is |
| --- | --- |
| `hpe_cray_EX235a/OLCF_Frontier-System-Architecture-public-v7.pdf` | OLCF public Frontier architecture (Joe Glenski, 15 Feb 2023). **EX235A blade**, cabinet/blade/node design, 4x MI250X, Infinity Fabric, Slingshot. https://www.olcf.ornl.gov/wp-content/uploads/2-15-23-Frontier-System-Architecture-public-v7.pdf |
| `hpe_cray_EX235a/OLCF_Frontier-Architecture-Overview_Abraham.pdf` | OLCF Frontier Architecture Overview (Subil Abraham, 28 Feb 2024). Node block-level description, 4x MI250X / 8 GCD. https://www.olcf.ornl.gov/wp-content/uploads/Frontier-Architecture-Overview_Abraham.pdf |
| `hpe_cray_EX235a/ICL-UT-22-05_Frontier-report.pdf` | ICL-UT-22-05 (Dongarra/Geist, 30 May 2022). Names the Frontier node as HPE Cray EX235a, 1x optimized EPYC + 4x MI250X, fully connected XGMI. https://icl.utk.edu/files/publications/2022/icl-utk-1570-2022.pdf |
| `hpe_cray_EX235a/LUMI_Service_Description.pdf` | CSC/LUMI service description. LUMI is HPE Cray EX with AMD MI250X GPU nodes (LUMI-G: 4 GPUs/node). https://www.lumi-supercomputer.eu/wp-content/uploads/2025/06/LUMI_Service_Description.pdf |
| `hpe_cray_EX235a/CUG2024_pres106s2_EX235a_cooling.pdf` | HPE + LRZ CUG 2024 slides: cooling-temperature impact on MI250X EX235A nodes (DLC, cold plates, HBM/junction thermal reporting). https://cug.org/proceedings/cug2024_proceedings/includes/files/pres106s2.pdf |
| `hpe_cray_EX235a/CUG2024_pres127s2_HPE_Cray_PM_Counters.pdf` | HPE CUG 2024 PM Counters slides. EX235a described as AMD Trento + 4x AMD MI250 GPUs (HPE’s slide text; Frontier public docs specify MI250X). https://cug.org/proceedings/cug2024_proceedings/includes/files/pres127s2.pdf |

Also see shared AMD PDFs: journey-to-exascale brochure (photographs the EX235a blade and states 2 nodes × 4 MI250X) and Hot Chips 34 MI200 node-architecture slides (HPE Cray EX235A topology).

HTML (not copied as PDF): LUMI hardware overview https://docs.lumi-supercomputer.eu/hardware/ and OLCF Frontier user guide https://docs.olcf.ornl.gov/systems/frontier_user_guide.html.

---

## Shared GPU / partner documents

These are not chassis products. They confirm OAM form factor and the partner list.

| File | What it is |
| --- | --- |
| `shared/amd-instinct-solution-catalog.pdf` | AMD Instinct GPU-Powered Servers solution catalog (2026). Partner table: G262-ZO0 = 4x MI250 OAM; Cray EX235a = 4x MI250X OAM per node; AS-4124GQ-TNMI = 4x MI250. https://www.amd.com/content/dam/amd/en/documents/products/accelerators/instinct/amd-instinct-solution-catalog.pdf |
| `shared/amd-instinct-mi200-datasheet.pdf` | AMD Instinct MI200 series datasheet. MI250 and MI250X are **OAM**, 500/560 W, passive & liquid. MI210 is the PCIe CEM card. https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/instinct-mi200-datasheet.pdf |
| `shared/amd-cdna2-white-paper.pdf` | AMD CDNA 2 white paper. MI250/MI250X = dual-GCD OAM; MI210 = single-GCD PCIe. https://www.amd.com/content/dam/amd/en/documents/instinct-business-docs/white-papers/amd-cdna2-white-paper.pdf |
| `shared/amd-journey-to-exascale-brochure.pdf` | AMD “Journey to Exascale” brochure. Frontier = HPE Cray EX235a, two nodes/blade, 4x MI250X each. https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/solution-briefs/journey-to-exascale-brochure.pdf |
| `shared/HC2022-AMD-MI200-AlanSmith.pdf` | Hot Chips 34 (22 Aug 2022) AMD Instinct MI200 accelerator and node architectures. Shows EX235A HPC topology and G262-ZO0 / AS-4124GQ-TNMI mainstream topologies. https://hc34.hotchips.org/assets/program/conference/day1/GPU%20HPC/HC2022.AMD.AlanSmith.v14.Final.20220820.pdf |
| `shared/amd-mi200-press-release-2021-11-08.pdf` | AMD launch PR: MI250X/MI250 are OAM; MI210 is PCIe; MI250X “currently available from HPE in the HPE Cray EX Supercomputer”; OEM list (ASUS, Atos, Dell, Gigabyte, HPE, Lenovo, Penguin, SuperMicro) is a forward-looking Q1 2022 statement, not a product table. |

SHA256 hashes of every PDF in this folder: `SHA256SUMS.txt`.

---

## Searched and excluded (not 2x+ MI250/MI250X OAM hosts)

AMD catalog + vendor pages were checked. These are **1x-only, MI210 PCIe/CEM, or MI300-only**. They are not in this pack.

| Vendor | Models checked | Why excluded |
| --- | --- | --- |
| SuperMicro | AS-2014CS-TR, AS-2024US-TRT, AS-2114GT-DNR, SBA-4119SG SuperBlade, **AS-4124GS-TNR**, AS-2115HV-TNRT, SYS-740GP-TNRT | MI210 PCIe only. AS-4124GS-TNR is a different 8x PCIe GPU box, not MI250 OAM. |
| SuperMicro | AS-4124GO-NART / NART+, AS-2124GQ-NART | NVIDIA HGX A100 SXM, not MI250. |
| SuperMicro | AS-8125GS-TNMR2, AS-4125GS-TNMR2-LCC, AS-8126GS-TNMR, MI300A GH boxes | MI300/MI325/MI350/MI355 only. |
| GIGABYTE | G242-Z12, G292-Z40/Z43/Z44/Z45, G482-Z54, R282-Z93 | MI210 PCIe. |
| GIGABYTE | G262-ZR0 | NVIDIA HGX A100 4-GPU, not MI250. |
| GIGABYTE | G593 / G893 / G4L3 MI300/MI325/MI350/MI355 SKUs | Later OAM generations only. |
| HPE | ProLiant XL675d / XL645d Gen10 Plus | MI210 PCIe. |
| HPE | Cray EX255a | MI300A, not MI250X. |
| Penguin Solutions | Altus XE2214GT (2U, 4x), Altus XE4218GT (4U, 8x) | **MI210 PCIe only** in the AMD catalog. Relion/Altus XE5318GTO is **MI300X**. No public Penguin datasheet listing 2x+ MI250/MI250X was found. |
| ASUS | ESC4000A-E11, ESC8000A-E11 | MI210 PCIe (4x / 8x). |
| Dell | PowerEdge R750XA, R7525, R7515 | MI210 PCIe; 1x–4x. |
| Lenovo | ThinkSystem SR655, SR665, SR670 v2 | MI210 PCIe. |
| Eviden / Bull | BullSequana AI 221/222/621/622 | MI210 PCIe. XH3000 current public material is MI300A, not a documented 2x+ MI250X SKU. |
| GigaIO | SuperNODE | Catalog lists 32x **MI210** on OAM UBB, not MI250. |
| Advantech, AEWIN, AMAX, Cancon, Cisco UCS C245 M8, Compal SG220, Exxact TensorEX MI210 SKUs, KOI XG23/EG21, MiTAC TN83/TN85, Nor-Tech | MI210 PCIe as catalogued. |

Launch-era OEM names (ASUS, Atos, Dell, Lenovo, Penguin) appear in the 2021 AMD press release as *expected Q1 2022* MI200-series systems. Without a vendor datasheet that actually lists **MI250 or MI250X at count ≥ 2**, they are not counted.

---

## What this pack does **not** contain

- No reconstructed OAM pin maps, MEZZ/UBB overlays, or xGMI pairwise wiring beyond what the vendor PDFs already print as *block diagrams*.
- No invented cold-plate, TIM, or hose MPNs. Air-cooled SMCI/Gigabyte docs list air shrouds/fansinks only. EX235a liquid plates are photographed in CUG slides without an MPN.
- No CEM MI210 card mechanicals.
- No MI300/MI325/MI350/MI355 UBB chassis.

If a later vendor PDF is published for EX235a spares or for a Penguin/ASUS/Dell MI250 OAM box, add it here only after the document itself names MI250/MI250X and a GPU count ≥ 2.
