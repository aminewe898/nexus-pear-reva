# Final checks — the receipts

See validation/erc-final.json and drc-final.json for native results, footprint-pad-inventory.json for pads/nets and layout-metrics.json for actual routing counts/lengths. The BOM and placement export are checked against native footprint values, MPNs and coordinates. Manufacturing exports and PDFs are regenerated from this revision.

The schematic power sheet is enlarged to A2 to contain the added protection circuit. Rendered PDF pages, PCB layers and board render are visually inspected. Final delivery-manifest.json records file sizes and SHA256 hashes.

Release remains DO NOT ORDER for the explicit bench, procurement, mechanics and impedance items in DESIGN_REVIEW_REVA.md. Neither a tested prototype nor completed firmware is claimed. Product purpose, legitimate sources and engineering limitations are retained.

Verified result: ERC 0; DRC 0; unconnected 0; schematic parity 0. 117 footprints, 1580 routed segments, 215 vias; 96 placement entries. 106 BOM rows, 96 unpriced. Schematic 11 pages; PCB PDF 5 pages.

The native STEP/render export reported missing component models for U1, U7, J2, F1 and L1. Those components have electrical footprints but their bodies are absent from the 3D files. No enclosure clearance approval is inferred from the render.
