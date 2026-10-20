#!/usr/bin/env python3
"""Replay the frozen native complete-record Info/price applications.

Immutable expected scientific evidence is never regenerated. Every JSON field
is compared, with explicit numerical tolerances only for floating diagnostics;
all original checker inequalities remain active under -O. The recovered
437-check packet has its separate ordinary certificate; this entrypoint
checks its unchanged bytes but does not repeat that older computation.
No compulsory Book Info, full payment, all40+2 source or GR closure is claimed.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]

INPUTS = ['02_REGISTRY/research/A4D_NATIVE_CLOCK_PRESSURE_AND_COMPLETE_PRICE_SYNTHESIS_2026_10_20.md',
 '02_REGISTRY/research/A4D_NATIVE_COMPLETE_RECORD_INFO_PRICE_SELECTION_2026_10_20.md',
 '02_REGISTRY/research/certificates/a4d_native_clock_price_source_check.py',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/FULL128_COHERENT_LIMIT_AND_INFO_PRICE.md',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/FULL128_COHERENT_RESULT.json',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/INDEPENDENT_ANALYTICAL_REVIEW.md',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/MATCHED_COMPLETE_LIKELIHOOD_SOURCE.md',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/MATCHED_LIKELIHOOD_RESULT.json',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/NATIVE_BINARY_RESULT.json',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/NATIVE_BINARY_TASK_MINIMUM.md',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/README.md',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/RECOVERED_PACKET.json',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/RECOVERED_REPLAY.json',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/RECOVERED_REPLAY.log',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/SOURCE_INPUTS.json',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/TASK_INVARIANCE_AND_TERMINAL_MINIMUM.md',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/TASK_INVARIANCE_RESULT.json',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/check_full128_coherent_info_price.py',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/check_matched_complete_likelihood_source.py',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/check_native_binary_task.py',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/check_task_invariance.py',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL128_RELATIVE_TRANSFER_AND_CONDENSED_DESCENT.md',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/A4D_P25_NATIVE_COST_FLOOR_PSD_MIXED_PALATINI_VACUUM_NO_GO_2026_10_20.md',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/MINIMAL_GOLDEN_COMPLETE_SOURCE.md',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/return_cost_and_stopping.md',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_relative_history_first_jet_2026-10-20/RESULT.md',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_relative_history_first_jet_2026-10-20/check_relative_history_first_jet.py',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_relative_transfer_2026-10-17/check_native_relative_transfer.py',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_triz_reference_2026-10-20/TRIZ_MATCHED_LOOP_VOID_SOURCE.md',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_triz_reference_2026-10-20/check_matched_feedback_poisson.py',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/INPUT_SNAPSHOTS.json',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/README.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/VALIDATION.json',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/VALIDATION.log',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/COHERENT_RETURN_PRESSURE_AND_PAID_MOMENTS.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/GEOMETRY_REVIEW.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/INPUTS.json',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/RESULT.json',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/STOPPED_CLOCK_REVIEW.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/check_coherent_return_pressure.py',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/check_finite_closed_record.py',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/finite_closed_record.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/BOOK_PRICE_REVIEW.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/CENTRAL_GEOMETRY_REVIEW.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/SOURCE_MOMENT_RESULT.json',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/check_source_moment_collapse.py',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/source_moment_collapse.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_COMPLETE_EXIT_ACTION_AND_SECOND_SOURCE.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_EXACT_GR_COMMON_CARRIER_HJR_SCALE_SOURCE_GAP_2026_10_20.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL128_JONES_OBSERVER_SO3_QUOTIENT_2026_10_20.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_PROSPECTIVE_BOOK_FINITE_FUTURE_LAW_Q8_VERIFICATION_2026_10_20.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/return_cost_and_stopping.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/FULL128_HEAT_PRICE_RECYCLING_BRIDGE.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/CENTRAL_COMPOSITION_REVIEW.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/FINITE_CUT_REVIEW.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/INPUTS.json',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/RESULT.json',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/STOPPED_CLOCK_SOURCE.md',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/check_stopped_clock_source.py']

PINNED_SHA256 = {'02_REGISTRY/research/A4D_NATIVE_CLOCK_PRESSURE_AND_COMPLETE_PRICE_SYNTHESIS_2026_10_20.md': '823d527dbe61050a9c3f81109691839e1bc9de0855e5435e08259049db1a06ed',
 '02_REGISTRY/research/A4D_NATIVE_COMPLETE_RECORD_INFO_PRICE_SELECTION_2026_10_20.md': '93d530eaa84df942bafb174006210047adb6588ec017d14d22bfa91ce800eaeb',
 '02_REGISTRY/research/certificates/a4d_native_clock_price_source_check.py': '7c6715937ab4ab5e0f9efff54ce42e8d8fbce2005e8c07242c76f87fd871407f',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/FULL128_COHERENT_LIMIT_AND_INFO_PRICE.md': '755fb3b181bfdc989235f54c518372404e72c008a70fbe9071a400da389b2530',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/FULL128_COHERENT_RESULT.json': '90e1883afd6227f76fc48bdec9249c6c279e5c6e09e4fd9a466c065cbb771833',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/INDEPENDENT_ANALYTICAL_REVIEW.md': '57169a1c0b09e4c3dfe79872114335c55742e7ae6934c92a4c7fbc2fdb62dded',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/MATCHED_COMPLETE_LIKELIHOOD_SOURCE.md': '4b08d0786a8a8ac39676e4912e00708548412cdacfaa96cf369b921e485d8c4d',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/MATCHED_LIKELIHOOD_RESULT.json': '2c139731204d5708a11853e606fd93a18c7ea5d024d2966e851d49ce30dcec66',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/NATIVE_BINARY_RESULT.json': '2c141eeddf6bf830df57d10f939efbc3f641e4368c91888ad193a501201c6773',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/NATIVE_BINARY_TASK_MINIMUM.md': 'fe1bd6a907ad13ff454de7e22b323b0065b7eecf75c127f74243df26ea435284',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/README.md': '3bc62334dcd9661527112a8a8a404dea1cce3373ddf026bbc81f48f21741d9bf',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/RECOVERED_PACKET.json': '06bd4041db9ce0273136c3854ac05ca389afeba903aee1a54ab9484e94a77797',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/RECOVERED_REPLAY.json': '6f2c752d2b1d779c4c34a623a04a1397bf8df80fb920d1b20a639822dfac03be',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/RECOVERED_REPLAY.log': '6f4c9e7152d2d14c2840904a3398f16e305d9aefa9119944fba89ca0a015a307',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/SOURCE_INPUTS.json': 'e83d6b96345a79e3f7040fee39a5625efd40f47f646e53cbf4dc9ed120d168e0',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/TASK_INVARIANCE_AND_TERMINAL_MINIMUM.md': '59ad221195a386b037a615c8275989d4b3d9782009b14179c2c324a3159e9949',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/TASK_INVARIANCE_RESULT.json': '7613c8240c47d818041cc2643d2b1511000baea2e6ea37a186ee612bf6e60e6d',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/check_full128_coherent_info_price.py': '60f70c32d9f67c09eee8cccb160b3ebc2299735a0fd7b471d1bb712af9e8a03c',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/check_matched_complete_likelihood_source.py': '4fd9ab1258cd0bef67e3236a8c46f206d944c6737ae6b07d949bbf2bc1129901',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/check_native_binary_task.py': 'ba4a4c069dba2d13a3740c0f1b8d7ee44d5fc9226d4118a8ff1b3dbb55856171',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/check_task_invariance.py': 'da839c7947989b7d2637bbb3d6fceb9b2aef3b7906341502dc7af7a44e580322',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL128_RELATIVE_TRANSFER_AND_CONDENSED_DESCENT.md': '577cbc909f766468fbef8ab38a5986ae761d348b075c2f38b2e1a88b704d4b3e',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/A4D_P25_NATIVE_COST_FLOOR_PSD_MIXED_PALATINI_VACUUM_NO_GO_2026_10_20.md': '1a2e52a67f6e707aa49f51c85d1af124eeee915f586687e683bec3214bd12131',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/MINIMAL_GOLDEN_COMPLETE_SOURCE.md': 'f6a5724e087c58b4294020a59532b7117f55247013181bcd4fd30d069a649330',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/return_cost_and_stopping.md': '29e30b35170c8ab1d4d324dd0f7aaa6e588cb1a32f023ad529947dc8639b9faa',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_relative_history_first_jet_2026-10-20/RESULT.md': 'd1c3cff174b2e4d03481ca6b3d18a1da2d3b65baba1f2dbf886324d8ce7f607d',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_relative_history_first_jet_2026-10-20/check_relative_history_first_jet.py': '0c69dc21fd66e06eefacf9ab047f186ff1e4e93818aff38aca4187968a70b468',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_relative_transfer_2026-10-17/check_native_relative_transfer.py': 'dfa8fffb08d421f2a2a0fa91a3044492ab94bfd6bd7d1e86b110b52c2e0ff065',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_triz_reference_2026-10-20/TRIZ_MATCHED_LOOP_VOID_SOURCE.md': '360e05c5f4825ea197d19e33669b2df1eb7017e11999d5f1f460eb88e982b477',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_triz_reference_2026-10-20/check_matched_feedback_poisson.py': '403ed4a5b68dbe4be56fd72a16a5c45d8ccdc5ca13eb5e2249d2722f68957b66',
 '02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md': 'ef69c2052237fbe8e916acf16691f9b14b4c1c2465a7837e838db2baeb95449d',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/INPUT_SNAPSHOTS.json': 'c3bd0f9a64d7bc2a0dfc912de6411f515b680574fa132add5a4056356ecc4b46',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/README.md': '70b05ec1b04c8b4f71d46dcc1b9c99dd76abaf006c3942384796ce0165ee298b',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/VALIDATION.json': '755622e853fc480259c07f5fb92537e23ce925db21b301aa1130a0cb4ab4cec3',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/VALIDATION.log': '6f4c9e7152d2d14c2840904a3398f16e305d9aefa9119944fba89ca0a015a307',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/COHERENT_RETURN_PRESSURE_AND_PAID_MOMENTS.md': '8001997f869a2ed86e78b6222e881d9ed67014ac0dc18573808df12b3592b7de',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/GEOMETRY_REVIEW.md': 'de105b644d2e5a7458587eddac49393c486d5f14b0c584d534141dd1db75d13e',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/INPUTS.json': '26674fa2e66b3534fe0361c2acdae0994d6d03d2f732210fb92719d6ef7782ae',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/RESULT.json': '163bb6d85e7b7deb626cf56486e0117da9e126d4fcdbf8dbf021c449c8b1f138',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/STOPPED_CLOCK_REVIEW.md': '5f8f459577450c4959fd16b1a460805a394827f80244585dbf38578ca5d56f6a',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/book_price/check_coherent_return_pressure.py': 'e3388349e9c6cbba37a05ac3a05b607ad34d2135aaca958e1265c3cca16e8db1',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/check_finite_closed_record.py': 'aa6d603038129139e0d944610d722123b776f01e52d72b3c8178636df4bd7b19',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/finite_closed_record.md': '44e3f7844dc40c99c5218c7223fabc485e63fc251517c53f1d424dab222bfe28',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/BOOK_PRICE_REVIEW.md': '862099aac7349fa31e30546141537420fa817e809b3c636f23b13a92555442a7',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/CENTRAL_GEOMETRY_REVIEW.md': '841683dbcbed32f75ed36a415f91b2c8c511f8bece57da328c2c0605d4d030ae',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/SOURCE_MOMENT_RESULT.json': '283d3f92890644469482f1f4de0c9885d380e9dff2ef8825fea40796400f7c08',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/check_source_moment_collapse.py': 'fd4edf0649492910eecf649fb1c133dafd2eb1b3d4b8df801a6e62a0f30691b8',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/geometry/source_moment_collapse.md': '9bfb61897324d438bff3458209f3fda321b2876af41b6178b96fdf04490773c4',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md': 'dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_COMPLETE_EXIT_ACTION_AND_SECOND_SOURCE.md': '482cf99f280620e7aa6120432cd7b9764671c5ef3fb1c0c3b50d7228d66e08b3',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md': '2128009802edff3e111a26961f050320fd878d7412ed93bfad5d5c9e4219db79',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_EXACT_GR_COMMON_CARRIER_HJR_SCALE_SOURCE_GAP_2026_10_20.md': 'c5b2f1021e8da573221f4327bacae67934470a368966456bf328b19fc51555fb',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL128_JONES_OBSERVER_SO3_QUOTIENT_2026_10_20.md': '610a6688f8f1ea91c93462d4cedf716eec321dd5032ba35a0d2ffb7262ffca61',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_FULL_LORENTZ_ADJOINT_SOURCE.md': 'a0a8a0b7389c7a6120ebbe402d111bf55cd2a00730403a00ffceca73548e7915',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md': 'd92aabf2d46d9ac7d8d9aa3bf5ed66a58f25bb83ca4460d66d25648c62f7e10b',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/A4D_PROSPECTIVE_BOOK_FINITE_FUTURE_LAW_Q8_VERIFICATION_2026_10_20.md': 'bd3f1ab51599b0efe17af03e40c59a606200cd1912f801e4bd57e0eb77a6b014',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/return_cost_and_stopping.md': '29e30b35170c8ab1d4d324dd0f7aaa6e588cb1a32f023ad529947dc8639b9faa',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/FULL128_HEAT_PRICE_RECYCLING_BRIDGE.md': 'a8cdbd52e52275cb7e41aa84b8bd69e9fb36170f75d8481c6568fb3ea1a2bce0',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/inputs/02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md': 'ef69c2052237fbe8e916acf16691f9b14b4c1c2465a7837e838db2baeb95449d',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/CENTRAL_COMPOSITION_REVIEW.md': '73cef0764bf733a340df15835d6add01df6740545acae5d7ec4b3d11778c32dd',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/FINITE_CUT_REVIEW.md': 'e70dae15cbc0ead0565b16464818bc21fabee8583a705d98cf889e39e5142e85',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/INPUTS.json': '8de593a2da6afe859e86f5b42a212b53705dcf5ce3def77ae15c22c02c4ea733',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/RESULT.json': 'b226373c813903af983ac1f438c4b7d6485d81dda32f13f2225284d20d0ee35f',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/STOPPED_CLOCK_SOURCE.md': '75845813d20ecf7b585fb7b7a7bef8b8170a711e94a56bb0df0cc3546622a036',
 '02_REGISTRY/research/sources/d0_native_minimality_closure_2026-10-20/prospective/check_stopped_clock_source.py': 'bdab1158efc863a8d631c50ae7f30f7c3780df744e74441a88ed298bc059f0c9'}

PACKET = ROOT / "02_REGISTRY/research/sources/d0_native_complete_price_selection_2026-10-20"
SNAPSHOT = PACKET / "inputs"


def verify_inputs():
    if set(INPUTS) != set(PINNED_SHA256):
        raise RuntimeError("Declared scientific inputs differ from immutable pins")
    for path, expected in PINNED_SHA256.items():
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise RuntimeError("Frozen scientific evidence changed: " + path)
    for item in json.loads((PACKET / "SOURCE_INPUTS.json").read_text())["inputs"]:
        if PINNED_SHA256.get(item["snapshot_path"]) != item["sha256"]:
            raise RuntimeError("Owner snapshot differs from its declared input: " + item["path"])
    for item in json.loads((PACKET / "RECOVERED_PACKET.json").read_text())["files"]:
        if PINNED_SHA256.get(item["path"]) != item["sha256"]:
            raise RuntimeError("Recovered prior packet differs from historical bytes")


def compare(actual, expected, *, path="result", atol=1e-12, rtol=1e-12):
    if type(actual) is not type(expected):
        raise RuntimeError("Result type differs: " + path)
    if isinstance(expected, dict):
        if set(actual) != set(expected):
            raise RuntimeError("Scientific result keys differ: " + path)
        for key in expected:
            compare(actual[key], expected[key], path=path+"."+key, atol=atol, rtol=rtol)
    elif isinstance(expected, list):
        if len(actual) != len(expected):
            raise RuntimeError("Scientific result length differs: " + path)
        for index, (left, right) in enumerate(zip(actual, expected)):
            compare(left, right, path=path+"["+str(index)+"]", atol=atol, rtol=rtol)
    elif isinstance(expected, float):
        if not math.isfinite(actual) or not math.isfinite(expected) or not math.isclose(actual, expected, abs_tol=atol, rel_tol=rtol):
            raise RuntimeError("Numerical scientific diagnostic differs: " + path)
    elif actual != expected:
        raise RuntimeError("Exact scientific result differs: " + path)


def replay(checker, receipt, *args, atol=1e-12, rtol=1e-12):
    command=[sys.executable, "-O", "-B", "-W", "error", str(PACKET / checker), *args]
    result=subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                          check=False, timeout=150)
    if result.returncode or result.stderr:
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise RuntimeError("Narrow scientific replay failed: " + checker)
    actual=json.loads(result.stdout)
    expected=json.loads((PACKET / receipt).read_text())
    if actual.get("status") != "PASS":
        raise RuntimeError("Checker did not pass: " + checker)
    compare(actual, expected, atol=atol, rtol=rtol)
    count=actual.get("check_count", actual.get("checks"))
    suffix=(str(count)+" active controls; ") if count is not None else "exact symbolic source groups; "
    print("PASS "+checker+": "+suffix+"every scientific receipt field agrees")


def main():
    verify_inputs()
    replay("check_full128_coherent_info_price.py", "FULL128_COHERENT_RESULT.json",
           atol=1e-9, rtol=1e-10)
    replay("check_matched_complete_likelihood_source.py", "MATCHED_LIKELIHOOD_RESULT.json",
           "--root", str(SNAPSHOT))
    replay("check_task_invariance.py", "TASK_INVARIANCE_RESULT.json")
    replay("check_native_binary_task.py", "NATIVE_BINARY_RESULT.json")
    verify_inputs()
    print("PASS "+str(len(INPUTS))+" immutable input/proof/checker/review/receipt pins before and after")
    print("SCOPE: original complete record; specified limiting entropy-price and paid binary-task minima; compulsory full Book price and physical GR remain open.")


if __name__ == "__main__":
    main()
