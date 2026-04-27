"""Pure-function tests for src.pipeline. No Gemma, no Manim."""

from src.pipeline import derive_hint, extract_code


# extract_code

def test_extract_code_with_python_fence():
    raw = "Some preamble.\n```python\nx = 1\nprint(x)\n```\nTrailing chatter."
    code, fenced = extract_code(raw)
    assert code == "x = 1\nprint(x)"
    assert fenced is True


def test_extract_code_with_unlabeled_fence():
    raw = "```\nx = 1\n```"
    code, fenced = extract_code(raw)
    assert code == "x = 1"
    assert fenced is True


def test_extract_code_without_any_fence_returns_raw_stripped():
    raw = "  x = 1  "
    code, fenced = extract_code(raw)
    assert code == "x = 1"
    assert fenced is False


def test_extract_code_takes_first_fence_when_multiple():
    raw = "```python\nfirst = 1\n```\n```python\nsecond = 2\n```"
    code, _ = extract_code(raw)
    assert code == "first = 1"


# derive_hint

def test_hint_recognises_array_broadcast_error():
    err = "ValueError: could not broadcast input array from shape (50,) into shape (3,)"
    hint = derive_hint(err)
    assert hint is not None
    assert "ax.plot" in hint
    assert "callable" in hint.lower()


def test_hint_recognises_surface_x_range_kwarg():
    err = "TypeError: Mobject.__init__() got an unexpected keyword argument 'x_range'"
    hint = derive_hint(err)
    assert hint is not None
    assert "u_range" in hint and "v_range" in hint


def test_hint_recognises_list_passed_to_animation():
    err = "TypeError: Animation only works on Mobjects"
    hint = derive_hint(err)
    assert hint is not None
    assert "VGroup" in hint or "Mobject" in hint


def test_hint_recognises_self_objects_attribute_error():
    err = "AttributeError: 'MyScene' object has no attribute 'objects'"
    hint = derive_hint(err)
    assert hint is not None
    assert "self.wait" in hint or "FadeOut" in hint


def test_hint_recognises_dot_point_size_kwarg():
    err = "TypeError: Mobject.__init__() got an unexpected keyword argument 'point_size'"
    hint = derive_hint(err)
    assert hint is not None
    assert "radius" in hint


def test_hint_recognises_triangle_points_kwarg():
    err = "TypeError: Mobject.__init__() got an unexpected keyword argument 'points'"
    hint = derive_hint(err)
    assert hint is not None
    assert "Polygon" in hint


def test_hint_returns_none_for_unknown_error():
    err = "ZeroDivisionError: division by zero"
    assert derive_hint(err) is None
