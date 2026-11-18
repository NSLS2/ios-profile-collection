"""Check xas_edge_ascan, xas_pd_ascan and the edge_ascan wrapper without any hardware.

The plans are run as plain generators against stand-in devices, and the messages they yield are
compared. The most important check: the new ``edge_ascan`` (a wrapper around ``xas_edge_ascan``)
yields the same messages, in the same order, as the original (reference/legacy_edge_ascan.py).

Run from the repository root with the bluesky packages, for example::

    pixi exec --spec bluesky-base --spec pytest --spec pandas --spec numpy \\
        -- python -m pytest acceptance_tests/test_xas_edge_plans.py
"""

import ast
import collections
import pathlib

import bluesky.plan_stubs as bps
import bluesky.plans as bp
import bluesky.preprocessors as bpp
import pytest
from bluesky.utils import Msg

ROOT = pathlib.Path(__file__).resolve().parents[1]


class Fake:
    """A stand-in for a device or signal. Attributes are fake too (xs3.channel01.mcaroi04.min_x)."""

    def __init__(self, name):
        self.name = name

    def __getattr__(self, attr):
        if attr.startswith("__"):
            raise AttributeError(attr)
        if "." in attr:  # ophyd devices accept a dotted name, as in getattr(sclr, "channels.chan2")
            node = self
            for part in attr.split("."):
                node = getattr(node, part)
            return node
        child = Fake(f"{self.name}.{attr}")
        object.__setattr__(self, attr, child)
        return child

    def __repr__(self):
        return self.name


def _functions(path, names):
    """The source of the named top-level functions of a file."""
    text = (ROOT / path).read_text()
    tree = ast.parse(text)
    wanted = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in wanted} == set(names)
    return "\n\n".join(ast.get_source_segment(text, n) for n in wanted)


@pytest.fixture
def ns():
    space = {
        "bps": bps,
        "bp": bp,
        "bpp": bpp,
        "ChainMap": collections.ChainMap,
        "save_csv": lambda name, doc: None,
    }
    for name in (
        "ioxas_x diag3_y au_mesh feedback pgm_energy epu1table epu1offset m1b1_setpoint "
        "vortex_x sample_sclr_gain sample_sclr_decade aumesh_sclr_gain aumesh_sclr_decade "
        "pd_sclr_gain pd_sclr_decade sclr_time xs3 sclr norm_ch4 ring_curr "
        "valve_diag3_close valve_mir3_close"
    ).split():
        space[name] = Fake(name)
    space["all_valves"] = [Fake("valve_a"), Fake("valve_b")]

    def E_ramp(dets, start, stop, velocity, time=None, *, streamname="primary", deadband=8, md=None):
        yield Msg(
            "E_ramp",
            None,
            [getattr(d, "name", d) for d in dets],
            start,
            stop,
            velocity,
            deadband=deadband,
            md=dict(md or {}),
        )
        return ["uid"]

    space["E_ramp"] = E_ramp
    exec(_functions("startup/99-settings.py", ["open_all_valves", "edge_ascan"]), space)
    exec((ROOT / "startup/99-xas-edge-plans.py").read_text(), space)
    exec((ROOT / "acceptance_tests/reference/legacy_edge_ascan.py").read_text(), space)
    space["EDGE_MAP"] = {
        "Fe_L": {
            "start": 698, "stop": 740, "velocity": 0.1, "deadband": 8.5, "epu1offset": -0.2,
            "epu_table": 4, "scan_count": 3, "intervals": 0.2, "au_mesh": -130.2, "e_align": 709,
            "m1b1_sp": 386,
        }
    }
    space["DET_SETTINGS"] = {
        "Fe_L": {
            "samplegain": "5", "sampledecade": "100 pA/V", "aumeshgain": "2",
            "aumeshdecade": "1 nA/V", "pd_gain": "5", "pd_decade": "1 uA/V", "vortex_low": 620,
            "vortex_high": 800, "IPFY_low": 450, "IPFY_high": 600, "vortex_pos": -280,
            "vortex_time": 0.5, "sclr_time": 0.5,
        }
    }
    space["SAMPLE_MAP"] = {"JW1": {"name": "JW1", "pos": 336.9, "diag3_y": 49}}
    return space


def run(plan, throw_at=None):
    """Drive a plan like the RunEngine does and return (messages, return value, exception).

    ``throw_at`` is a command name: the first message with it gets a RuntimeError instead of a result.
    """
    messages = []
    groups = {}

    def norm(value):
        if isinstance(value, str) and len(value) == 36 and value.count("-") == 4:
            return groups.setdefault(value, f"group{len(groups)}")
        if callable(value):
            return getattr(value, "__name__", "callable")
        if isinstance(value, collections.ChainMap):
            return dict(value)
        return value

    try:
        msg = next(plan)
        while True:
            messages.append(
                (
                    msg.command,
                    getattr(msg.obj, "name", msg.obj),
                    tuple(norm(a) for a in msg.args),
                    {k: norm(v) for k, v in msg.kwargs.items()},
                )
            )
            if throw_at == msg.command:
                throw_at = None
                msg = plan.throw(RuntimeError("stopped"))
            else:
                msg = plan.send(None)
    except StopIteration as stop:
        return messages, stop.value, None
    except RuntimeError as exc:
        return messages, None, exc


def sets(messages, obj):
    return [m[2][0] for m in messages if m[0] == "set" and m[1] == obj]


def test_edge_ascan_runs_the_same_steps_as_the_original(ns):
    new, new_ret, _ = run(ns["edge_ascan"]("JW1", "Fe_L", md={"user": "x"}))
    old, old_ret, _ = run(ns["legacy_edge_ascan"]("JW1", "Fe_L", md={"user": "x"}))
    assert len(old) > 100
    assert new == old
    assert new_ret == old_ret == ["uid", "uid", "uid"]


def test_the_edge_ascan_wrapper_leaves_the_valves_open_as_before(ns):
    messages, _, _ = run(ns["edge_ascan"]("JW1", "Fe_L"))
    assert sets(messages, "valve_diag3_close") == []


def test_core_plan_with_the_same_values_is_the_same_as_the_original_for_one_repeat(ns):
    ns["EDGE_MAP"]["Fe_L"]["scan_count"] = 1
    old, _, _ = run(ns["legacy_edge_ascan"]("JW1", "Fe_L"))
    kw = dict(
        start=698, stop=740, velocity=0.1, deadband=8.5, e_align=709, epu_table=4, epu_offset=-0.2,
        m1b1_sp=386, au_mesh_pos=-130.2, sample_pos=336.9, diag3_pos=49, vortex_pos=-280,
        samplegain="5", sampledecade="100 pA/V", aumeshgain="2", aumeshdecade="1 nA/V",
        pd_gain="5", pd_decade="1 uA/V", dwell_s=0.5, pfy_min_x=620, pfy_size_x=180,
        ipfy_min_x=450, ipfy_size_x=150, close_valves_after=False, save_csv_on_stop=True,
    )
    new, _, _ = run(ns["xas_edge_ascan"](**kw, md={"plan_name": "edge_ascan", "edge": "Fe_L",
                                                   "name": "JW1", "pos": 336.9, "diag3_y": 49}))
    # only the run metadata differs: the original also gives the sample's other properties
    strip = lambda ms: [m for m in ms if m[0] != "E_ramp"]  # noqa: E731
    assert strip(new) == strip(old)


def test_the_ramp_goes_from_stop_down_to_start(ns):
    messages, _, _ = run(ns["edge_ascan"]("JW1", "Fe_L"))
    ramps = [m for m in messages if m[0] == "E_ramp"]
    assert len(ramps) == 3
    assert ramps[0][2][1:4] == (740, 698, 0.1)  # start of the ramp is the stop energy


def test_repeats_are_spread_around_the_sample_position(ns):
    messages, _, _ = run(ns["edge_ascan"]("JW1", "Fe_L"))
    positions = sets(messages, "ioxas_x")
    assert positions[0] == 336.9  # the position of the sample
    assert positions[1:] == pytest.approx([336.7, 336.9, 337.1])


def test_an_interval_of_zero_stays_on_one_spot(ns):
    ns["EDGE_MAP"]["Fe_L"]["intervals"] = 0
    messages, _, _ = run(ns["edge_ascan"]("JW1", "Fe_L"))
    assert set(sets(messages, "ioxas_x")) == {336.9}


def test_valves_are_closed_when_the_plan_is_aborted_or_fails(ns):
    plan = ns["xas_edge_ascan"](
        start=1, stop=2, velocity=0.1, deadband=1, e_align=1, epu_table=4, epu_offset=0,
        m1b1_sp=1, au_mesh_pos=0, sample_pos=1,
    )
    messages, value, error = run(plan, throw_at="E_ramp")
    assert isinstance(error, RuntimeError) and value is None
    last_ramp = max(i for i, m in enumerate(messages) if m[0] == "E_ramp")
    after = [m for m in messages[last_ramp + 1:] if m[0] == "set"]
    # nothing but the valves is set between the failure and the end
    assert [(m[1], m[2]) for m in after] == [("valve_diag3_close", (1,)), ("valve_mir3_close", (1,))]


def test_the_core_plan_closes_the_valves_after_it_completes_unless_told_not_to(ns):
    base = dict(start=1, stop=2, velocity=0.1, deadband=1, e_align=1, epu_table=4, epu_offset=0,
                m1b1_sp=1, au_mesh_pos=0)
    messages, _, _ = run(ns["xas_edge_ascan"](**base))
    assert sets(messages, "valve_diag3_close") == [1] and sets(messages, "valve_mir3_close") == [1]
    messages, _, _ = run(ns["xas_edge_ascan"](**base, close_valves_after=False))
    assert sets(messages, "valve_diag3_close") == []


def test_values_that_are_not_given_are_not_set(ns):
    messages, _, _ = run(ns["xas_edge_ascan"](
        start=1, stop=2, velocity=0.1, deadband=1, e_align=1, epu_table=4, epu_offset=0,
        m1b1_sp=1, au_mesh_pos=0,
    ))
    for obj in ("ioxas_x", "diag3_y", "vortex_x", "sample_sclr_gain", "sclr_time",
                "xs3.channel01.mcaroi04.min_x"):
        assert sets(messages, obj) == [], obj
    assert sets(messages, "m1b1_setpoint") == [1, 1]  # alignment before and in the repeat


def test_the_photodiode_plan_retracts_the_sample_and_uses_the_photodiode_detectors(ns):
    messages, value, _ = run(ns["xas_pd_ascan"](
        start=698, stop=740, velocity=0.1, deadband=8.5, e_align=709, epu_table=4, epu_offset=-0.2,
        m1b1_sp=386, au_mesh_pos=-130.2, pd_diag3_pos=16.3, sample_out_x=90.0,
        pd_gain="5", pd_decade="1 uA/V", aumeshgain="2", aumeshdecade="1 nA/V", dwell_s=0.5,
    ))
    first = [m for m in messages if m[0] == "set"][:2]
    assert [(m[1], m[2][0]) for m in first] == [("ioxas_x", 90.0), ("diag3_y", 16.3)]
    assert sets(messages, "pd_sclr_gain") == ["5"] and sets(messages, "sample_sclr_gain") == []
    assert not any(m[1].startswith("xs3") for m in messages if m[1])  # no fluorescence detector
    (ramp,) = [m for m in messages if m[0] == "E_ramp"]
    assert ramp[2][0] == ["sclr", "ring_curr"] and ramp[2][1:4] == (740, 698, 0.1)
    assert sets(messages, "valve_diag3_close") == [1] and value == ["uid"]
    assert ns["sclr"].channels.chan3.kind == "hinted" and ns["sclr"].channels.chan4.kind == "normal"
