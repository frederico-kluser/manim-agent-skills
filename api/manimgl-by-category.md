# API de `manimlib` v1.7.2

1241 símbolos públicos · 51193 métodos indexados · Python 3.12.3

Gerado por `mx api-dump` a partir do pacote instalado. Regenere após atualizar o Manim.

## Categorias

- [`animation/composition`](#animationcomposition) — 6 símbolos
- [`animation/core`](#animationcore) — 9 símbolos
- [`animation/creation`](#animationcreation) — 9 símbolos
- [`animation/fading`](#animationfading) — 12 símbolos
- [`animation/growing`](#animationgrowing) — 5 símbolos
- [`animation/indication`](#animationindication) — 29 símbolos
- [`animation/movement`](#animationmovement) — 6 símbolos
- [`animation/numbers`](#animationnumbers) — 4 símbolos
- [`animation/rotation`](#animationrotation) — 7 símbolos
- [`animation/specialized`](#animationspecialized) — 4 símbolos
- [`animation/transform`](#animationtransform) — 24 símbolos
- [`camera`](#camera) — 23 símbolos
- [`constants`](#constants) — 117 símbolos
- [`mobject/3d`](#mobject3d) — 28 símbolos
- [`mobject/core`](#mobjectcore) — 250 símbolos
- [`mobject/geometry`](#mobjectgeometry) — 53 símbolos
- [`mobject/matrix`](#mobjectmatrix) — 11 símbolos
- [`mobject/svg`](#mobjectsvg) — 115 símbolos
- [`mobject/value_tracker`](#mobjectvalue_tracker) — 4 símbolos
- [`mobject/vector_field`](#mobjectvector_field) — 16 símbolos
- [`other`](#other) — 219 símbolos
- [`renderer`](#renderer) — 61 símbolos
- [`scene`](#scene) — 43 símbolos
- [`typing`](#typing) — 1 símbolos
- [`utils/bezier`](#utilsbezier) — 20 símbolos
- [`utils/color`](#utilscolor) — 24 símbolos
- [`utils/other`](#utilsother) — 74 símbolos
- [`utils/rate_functions`](#utilsrate_functions) — 16 símbolos
- [`utils/space_ops`](#utilsspace_ops) — 44 símbolos
- [`utils/tex`](#utilstex) — 7 símbolos

## animation/composition

### `AnimationGroup(*args: 'AnimationType | Iterable[AnimationType]', run_time: 'float' = -1, lag_ratio: 'float' = 0.0, group: 'Optional[Mobject]' = None, group_type: 'Optional[type]' = None, **kwargs)` ← Animation

<details><summary>métodos próprios (9) · herdados: 18</summary>

- `__init__(self, *args: 'AnimationType | Iterable[AnimationType]', run_time: 'float' = -1, lag_ratio: 'float' = 0.0, group: 'Optional[Mobject]' = None, group_type: 'Optional[type]' = None, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'`
- `build_animations_with_timings(self, lag_ratio: 'float') -> 'None'` — Creates a list of triplets of the form
- `calculate_max_end_time(self) -> 'None'`
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'`
- `finish(self) -> 'None'`
- `get_all_mobjects(self) -> 'Mobject'` — Ordering must match the ording of arguments to interpolate_submobject
- `interpolate(self, alpha: 'float') -> 'None'`
- `update_reference_mobjects(self, dt: 'float', frame_rate: 'float | None' = None) -> 'None'` — Updates things like starting_mobject, and (for

</details>

### `LaggedStart(*animations, lag_ratio: 'float' = 0.05, **kwargs)` ← AnimationGroup

<details><summary>métodos próprios (1) · herdados: 26</summary>

- `__init__(self, *animations, lag_ratio: 'float' = 0.05, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `LaggedStartMap(anim_func: 'Callable[[Mobject], Animation]', group: 'Mobject', run_time: 'float' = 2.0, lag_ratio: 'float' = 0.05, **kwargs)` ← LaggedStart

<details><summary>métodos próprios (1) · herdados: 26</summary>

- `__init__(self, anim_func: 'Callable[[Mobject], Animation]', group: 'Mobject', run_time: 'float' = 2.0, lag_ratio: 'float' = 0.05, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Succession(*animations: 'Animation', lag_ratio: 'float' = 1.0, **kwargs)` ← AnimationGroup

<details><summary>métodos próprios (5) · herdados: 22</summary>

- `__init__(self, *animations: 'Animation', lag_ratio: 'float' = 1.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'`
- `finish(self) -> 'None'`
- `interpolate(self, alpha: 'float') -> 'None'`
- `update_reference_mobjects(self, dt: 'float', frame_rate: 'float | None' = None) -> 'None'` — Updates things like starting_mobject, and (for

</details>

- `DEFAULT_LAGGED_START_LAG_RATIO` = `0.05`
- `TYPE_CHECKING` = `False`

## animation/core

### `Animation(mobject: 'Mobject', run_time: 'float' = 1.0, time_span: 'tuple[float, float] | None' = None, lag_ratio: 'float' = 0, rate_func: 'Callable[[float], float]' = <function smooth at 0x7f6ff39332e0>, name: 'str' = '', remover: 'bool' = False, final_alpha_value: 'float' = 1.0, suspend_mobject_updating: 'bool' = False)`

<details><summary>métodos próprios (25) · herdados: 0</summary>

- `__init__(self, mobject: 'Mobject', run_time: 'float' = 1.0, time_span: 'tuple[float, float] | None' = None, lag_ratio: 'float' = 0, rate_func: 'Callable[[float], float]' = <function smooth at 0x7f6ff39332e0>, name: 'str' = '', remover: 'bool' = False, final_alpha_value: 'float' = 1.0, suspend_mobject_updating: 'bool' = False)` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'`
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'`
- `copy(self)`
- `create_starting_mobject(self) -> 'Mobject'`
- `finish(self) -> 'None'`
- `get_all_families_zipped(self) -> 'zip[tuple[Mobject]]'`
- `get_all_mobjects(self) -> 'tuple[Mobject, Mobject]'` — Ordering must match the ording of arguments to interpolate_submobject
- `get_interpolation_ends(self) -> 'tuple[Mobject, Mobject] | None'` — The two states every blend this animation makes runs between, in the order it blends
- `get_rate_func(self) -> 'Callable[[float], float]'`
- `get_reference_mobjects(self) -> 'list[Mobject]'` — Returns mobjects the Animation tracks other than
- `get_run_time(self) -> 'float'`
- `get_sub_alpha(self, alpha: 'float', index: 'int', num_submobjects: 'int') -> 'float'`
- `interpolate(self, alpha: 'float') -> 'None'`
- `interpolate_mobject(self, alpha: 'float') -> 'None'`
- `interpolate_submobject(self, submobject: 'Mobject', starting_submobject: 'Mobject', alpha: 'float')`
- `is_remover(self) -> 'bool'`
- `prepare_interpolation(self) -> 'None'` — Whatever holds of the two ends for the whole of the animation, settled here rather
- `set_name(self, name: 'str')`
- `set_rate_func(self, rate_func: 'Callable[[float], float]')`
- `set_run_time(self, run_time: 'float')`
- `time_spanned_alpha(self, alpha: 'float') -> 'float'`
- `update(self, alpha: 'float') -> 'None'` — This method shouldn't exist, but it's here to
- `update_rate_info(self, run_time: 'float | None' = None, rate_func: 'Callable[[float], float] | None' = None, lag_ratio: 'float | None' = None)`
- `update_reference_mobjects(self, dt: 'float', frame_rate: 'float | None' = None) -> 'None'` — Updates things like starting_mobject, and (for

</details>

### `MaintainPositionRelativeTo(mobject: 'Mobject', tracked_mobject: 'Mobject', **kwargs)` ← Animation

<details><summary>métodos próprios (2) · herdados: 23</summary>

- `__init__(self, mobject: 'Mobject', tracked_mobject: 'Mobject', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_mobject(self, alpha: 'float') -> 'None'`

</details>

### `UpdateFromAlphaFunc(mobject: 'Mobject', update_function: 'Callable[[Mobject, float], Mobject | None]', suspend_mobject_updating: 'bool' = False, **kwargs)` ← Animation

<details><summary>métodos próprios (2) · herdados: 23</summary>

- `__init__(self, mobject: 'Mobject', update_function: 'Callable[[Mobject, float], Mobject | None]', suspend_mobject_updating: 'bool' = False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_mobject(self, alpha: 'float') -> 'None'`

</details>

### `UpdateFromFunc(mobject: 'Mobject', update_function: 'Callable[[Mobject], Mobject | None]', suspend_mobject_updating: 'bool' = False, **kwargs)` ← Animation
> update_function of the form func(mobject), presumably

<details><summary>métodos próprios (2) · herdados: 23</summary>

- `__init__(self, mobject: 'Mobject', update_function: 'Callable[[Mobject], Mobject | None]', suspend_mobject_updating: 'bool' = False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_mobject(self, alpha: 'float') -> 'None'`

</details>

- `DEFAULT_ANIMATION_LAG_RATIO` = `0`
- `DEFAULT_ANIMATION_RUN_TIME` = `1.0`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- **`prepare_animation(anim: 'Animation | _AnimationBuilder')`**

## animation/creation

### `AddTextWordByWord(string_mobject: 'StringMobject', time_per_word: 'float' = 0.2, run_time: 'float' = -1.0, rate_func: 'Callable[[float], float]' = <function linear at 0x7f6ff3932de0>, **kwargs)` ← ShowIncreasingSubsets

<details><summary>métodos próprios (2) · herdados: 24</summary>

- `__init__(self, string_mobject: 'StringMobject', time_per_word: 'float' = 0.2, run_time: 'float' = -1.0, rate_func: 'Callable[[float], float]' = <function linear at 0x7f6ff3932de0>, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'`

</details>

### `DrawBorderThenFill(vmobject: 'VMobject', run_time: 'float' = 2.0, rate_func: 'Callable[[float], float]' = <function double_smooth at 0x7f6ff3933560>, stroke_width: 'float' = 2.0, stroke_color: 'ManimColor' = None, draw_border_animation_config: 'dict' = {}, fill_animation_config: 'dict' = {}, **kwargs)` ← Animation

<details><summary>métodos próprios (6) · herdados: 20</summary>

- `__init__(self, vmobject: 'VMobject', run_time: 'float' = 2.0, rate_func: 'Callable[[float], float]' = <function double_smooth at 0x7f6ff3933560>, stroke_width: 'float' = 2.0, stroke_color: 'ManimColor' = None, draw_border_animation_config: 'dict' = {}, fill_animation_config: 'dict' = {}, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'`
- `get_all_mobjects(self) -> 'list[Mobject]'` — Ordering must match the ording of arguments to interpolate_submobject
- `get_interpolation_ends(self) -> 'tuple[VMobject, VMobject]'` — The second half blends between these two, and the first half never blends at all: it
- `get_outline(self) -> 'VMobject'`
- `interpolate_submobject(self, submob: 'VMobject', start: 'VMobject', outline: 'VMobject', alpha: 'float') -> 'None'`

</details>

### `ShowCreation(mobject: 'Mobject', lag_ratio: 'float' = 1.0, **kwargs)` ← ShowPartial
> Abstract class for ShowCreation and ShowPassingFlash

<details><summary>métodos próprios (2) · herdados: 24</summary>

- `__init__(self, mobject: 'Mobject', lag_ratio: 'float' = 1.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_bounds(self, alpha: 'float') -> 'tuple[float, float]'`

</details>

### `ShowIncreasingSubsets(group: 'Mobject', int_func: 'Callable[[float], float]' = <function round at 0x7f70bacdce70>, suspend_mobject_updating: 'bool' = False, **kwargs)` ← Animation

<details><summary>métodos próprios (3) · herdados: 23</summary>

- `__init__(self, group: 'Mobject', int_func: 'Callable[[float], float]' = <function round at 0x7f70bacdce70>, suspend_mobject_updating: 'bool' = False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_mobject(self, alpha: 'float') -> 'None'`
- `update_submobject_list(self, index: 'int') -> 'None'`

</details>

### `ShowPartial(mobject: 'Mobject', should_match_start: 'bool' = False, **kwargs)` ← Animation, ABC
> Abstract class for ShowCreation and ShowPassingFlash

<details><summary>métodos próprios (3) · herdados: 23</summary>

- `__init__(self, mobject: 'Mobject', should_match_start: 'bool' = False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_bounds(self, alpha: 'float') -> 'tuple[float, float]'`
- `interpolate_submobject(self, submob: 'Mobject', start_submob: 'Mobject', alpha: 'float') -> 'None'`

</details>

### `ShowSubmobjectsOneByOne(group: 'Mobject', int_func: 'Callable[[float], float]' = <ufunc 'ceil'>, **kwargs)` ← ShowIncreasingSubsets

<details><summary>métodos próprios (2) · herdados: 24</summary>

- `__init__(self, group: 'Mobject', int_func: 'Callable[[float], float]' = <ufunc 'ceil'>, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `update_submobject_list(self, index: 'int') -> 'None'`

</details>

### `Uncreate(mobject: 'Mobject', rate_func: 'Callable[[float], float]' = <function Uncreate.<lambda> at 0x7f6ff2df0540>, remover: 'bool' = True, should_match_start: 'bool' = True, **kwargs)` ← ShowCreation
> Abstract class for ShowCreation and ShowPassingFlash

<details><summary>métodos próprios (1) · herdados: 25</summary>

- `__init__(self, mobject: 'Mobject', rate_func: 'Callable[[float], float]' = <function Uncreate.<lambda> at 0x7f6ff2df0540>, remover: 'bool' = True, should_match_start: 'bool' = True, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Write(vmobject: 'VMobject', run_time: 'float' = -1, lag_ratio: 'float' = -1, rate_func: 'Callable[[float], float]' = <function linear at 0x7f6ff3932de0>, stroke_color: 'ManimColor' = None, **kwargs)` ← DrawBorderThenFill

<details><summary>métodos próprios (3) · herdados: 25</summary>

- `__init__(self, vmobject: 'VMobject', run_time: 'float' = -1, lag_ratio: 'float' = -1, rate_func: 'Callable[[float], float]' = <function linear at 0x7f6ff3932de0>, stroke_color: 'ManimColor' = None, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `compute_lag_ratio(self, family_size: 'int', lag_ratio: 'float')`
- `compute_run_time(self, family_size: 'int', run_time: 'float')`

</details>

- `TYPE_CHECKING` = `False`

## animation/fading

### `Fade(mobject: 'Mobject', shift: 'np.ndarray' = array([0., 0., 0.]), scale: 'float' = 1, **kwargs)` ← Transform

<details><summary>métodos próprios (1) · herdados: 28</summary>

- `__init__(self, mobject: 'Mobject', shift: 'np.ndarray' = array([0., 0., 0.]), scale: 'float' = 1, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `FadeIn(mobject: 'Mobject', shift: 'np.ndarray' = array([0., 0., 0.]), scale: 'float' = 1, **kwargs)` ← Fade

<details><summary>métodos próprios (2) · herdados: 27</summary>

- `create_starting_mobject(self) -> 'Mobject'`
- `create_target(self) -> 'Mobject'`

</details>

### `FadeInFromPoint(mobject: 'Mobject', point: 'Vect3', **kwargs)` ← FadeIn

<details><summary>métodos próprios (1) · herdados: 28</summary>

- `__init__(self, mobject: 'Mobject', point: 'Vect3', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `FadeOut(mobject: 'Mobject', shift: 'Vect3' = array([0., 0., 0.]), remover: 'bool' = True, final_alpha_value: 'float' = 0.0, **kwargs)` ← Fade

<details><summary>métodos próprios (2) · herdados: 27</summary>

- `__init__(self, mobject: 'Mobject', shift: 'Vect3' = array([0., 0., 0.]), remover: 'bool' = True, final_alpha_value: 'float' = 0.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `create_target(self) -> 'Mobject'`

</details>

### `FadeOutToPoint(mobject: 'Mobject', point: 'Vect3', **kwargs)` ← FadeOut

<details><summary>métodos próprios (1) · herdados: 28</summary>

- `__init__(self, mobject: 'Mobject', point: 'Vect3', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `FadeTransform(mobject: 'Mobject', target_mobject: 'Mobject', stretch: 'bool' = True, dim_to_match: 'int' = 1, **kwargs)` ← Transform

<details><summary>métodos próprios (7) · herdados: 23</summary>

- `__init__(self, mobject: 'Mobject', target_mobject: 'Mobject', stretch: 'bool' = True, dim_to_match: 'int' = 1, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'`
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'`
- `get_all_families_zipped(self) -> 'zip[tuple[Mobject]]'`
- `get_all_mobjects(self) -> 'list[Mobject]'` — Ordering must match the ording of arguments to interpolate_submobject
- `get_interpolation_ends(self) -> 'tuple[Mobject, Mobject]'` — The two states every blend this animation makes runs between, in the order it blends
- `ghost_to(self, source: 'Mobject', target: 'Mobject') -> 'None'`

</details>

### `FadeTransformPieces(mobject: 'Mobject', target_mobject: 'Mobject', stretch: 'bool' = True, dim_to_match: 'int' = 1, **kwargs)` ← FadeTransform

<details><summary>métodos próprios (2) · herdados: 28</summary>

- `begin(self) -> 'None'`
- `ghost_to(self, source: 'Mobject', target: 'Mobject') -> 'None'`

</details>

### `VFadeIn(vmobject: 'VMobject', suspend_mobject_updating: 'bool' = False, **kwargs)` ← Animation
> VFadeIn and VFadeOut only work for VMobjects,

<details><summary>métodos próprios (2) · herdados: 23</summary>

- `__init__(self, vmobject: 'VMobject', suspend_mobject_updating: 'bool' = False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_submobject(self, submob: 'VMobject', start: 'VMobject', alpha: 'float') -> 'None'`

</details>

### `VFadeInThenOut(vmobject: 'VMobject', rate_func: 'Callable[[float], float]' = <function there_and_back at 0x7f6ff3933600>, remover: 'bool' = True, final_alpha_value: 'float' = 0.5, **kwargs)` ← VFadeIn
> VFadeIn and VFadeOut only work for VMobjects,

<details><summary>métodos próprios (1) · herdados: 24</summary>

- `__init__(self, vmobject: 'VMobject', rate_func: 'Callable[[float], float]' = <function there_and_back at 0x7f6ff3933600>, remover: 'bool' = True, final_alpha_value: 'float' = 0.5, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `VFadeOut(vmobject: 'VMobject', remover: 'bool' = True, final_alpha_value: 'float' = 0.0, **kwargs)` ← VFadeIn
> VFadeIn and VFadeOut only work for VMobjects,

<details><summary>métodos próprios (2) · herdados: 23</summary>

- `__init__(self, vmobject: 'VMobject', remover: 'bool' = True, final_alpha_value: 'float' = 0.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_submobject(self, submob: 'VMobject', start: 'VMobject', alpha: 'float') -> 'None'`

</details>

- `ORIGIN` = `array([0., 0., 0.])`
- `TYPE_CHECKING` = `False`

## animation/growing

### `GrowArrow(arrow: 'Arrow', **kwargs)` ← GrowFromPoint

<details><summary>métodos próprios (1) · herdados: 28</summary>

- `__init__(self, arrow: 'Arrow', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `GrowFromCenter(mobject: 'Mobject', **kwargs)` ← GrowFromPoint

<details><summary>métodos próprios (1) · herdados: 28</summary>

- `__init__(self, mobject: 'Mobject', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `GrowFromEdge(mobject: 'Mobject', edge: 'np.ndarray', **kwargs)` ← GrowFromPoint

<details><summary>métodos próprios (1) · herdados: 28</summary>

- `__init__(self, mobject: 'Mobject', edge: 'np.ndarray', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `GrowFromPoint(mobject: 'Mobject', point: 'np.ndarray', point_color: 'ManimColor' = None, **kwargs)` ← Transform

<details><summary>métodos próprios (3) · herdados: 26</summary>

- `__init__(self, mobject: 'Mobject', point: 'np.ndarray', point_color: 'ManimColor' = None, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `create_starting_mobject(self) -> 'Mobject'`
- `create_target(self) -> 'Mobject'`

</details>

- `TYPE_CHECKING` = `False`

## animation/indication

### `AnimationOnSurroundingRectangle(mobject: 'Mobject', stroke_width: 'float' = 2.0, stroke_color: 'ManimColor' = '#FFFF00', buff: 'float' = 0.1, **kwargs)` ← AnimationGroup

<details><summary>métodos próprios (1) · herdados: 26</summary>

- `__init__(self, mobject: 'Mobject', stroke_width: 'float' = 2.0, stroke_color: 'ManimColor' = '#FFFF00', buff: 'float' = 0.1, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ApplyWave(mobject: 'Mobject', direction: 'np.ndarray' = array([0., 1., 0.]), amplitude: 'float' = 0.2, run_time: 'float' = 1.0, **kwargs)` ← Homotopy

<details><summary>métodos próprios (1) · herdados: 25</summary>

- `__init__(self, mobject: 'Mobject', direction: 'np.ndarray' = array([0., 1., 0.]), amplitude: 'float' = 0.2, run_time: 'float' = 1.0, **kwargs)` — Homotopy is a function from

</details>

### `CircleIndicate(mobject: 'Mobject', scale_factor: 'float' = 1.2, rate_func: 'Callable[[float], float]' = <function there_and_back at 0x7f6ff3933600>, stroke_color: 'ManimColor' = '#FFFF00', stroke_width: 'float' = 3.0, remover: 'bool' = True, **kwargs)` ← Transform

<details><summary>métodos próprios (1) · herdados: 28</summary>

- `__init__(self, mobject: 'Mobject', scale_factor: 'float' = 1.2, rate_func: 'Callable[[float], float]' = <function there_and_back at 0x7f6ff3933600>, stroke_color: 'ManimColor' = '#FFFF00', stroke_width: 'float' = 3.0, remover: 'bool' = True, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Flash(point: 'np.ndarray | Mobject', color: 'ManimColor' = '#FFFF00', line_length: 'float' = 0.2, num_lines: 'int' = 12, flash_radius: 'float' = 0.3, line_stroke_width: 'float' = 3.0, run_time: 'float' = 1.0, **kwargs)` ← AnimationGroup

<details><summary>métodos próprios (3) · herdados: 26</summary>

- `__init__(self, point: 'np.ndarray | Mobject', color: 'ManimColor' = '#FFFF00', line_length: 'float' = 0.2, num_lines: 'int' = 12, flash_radius: 'float' = 0.3, line_stroke_width: 'float' = 3.0, run_time: 'float' = 1.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `create_line_anims(self) -> 'list[Animation]'`
- `create_lines(self) -> 'VGroup'`

</details>

### `FlashAround(mobject: 'Mobject', time_width: 'float' = 1.0, taper_width: 'float' = 0.0, stroke_width: 'float' = 4.0, color: 'ManimColor' = '#FFFF00', buff: 'float' = 0.1, n_inserted_curves: 'int' = 100, **kwargs)` ← VShowPassingFlash

<details><summary>métodos próprios (2) · herdados: 25</summary>

- `__init__(self, mobject: 'Mobject', time_width: 'float' = 1.0, taper_width: 'float' = 0.0, stroke_width: 'float' = 4.0, color: 'ManimColor' = '#FFFF00', buff: 'float' = 0.1, n_inserted_curves: 'int' = 100, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_path(self, mobject: 'Mobject', buff: 'float') -> 'SurroundingRectangle'`

</details>

### `FlashUnder(mobject: 'Mobject', time_width: 'float' = 1.0, taper_width: 'float' = 0.0, stroke_width: 'float' = 4.0, color: 'ManimColor' = '#FFFF00', buff: 'float' = 0.1, n_inserted_curves: 'int' = 100, **kwargs)` ← FlashAround

<details><summary>métodos próprios (1) · herdados: 26</summary>

- `get_path(self, mobject: 'Mobject', buff: 'float') -> 'Underline'`

</details>

### `FlashyFadeIn(vmobject: 'VMobject', stroke_width: 'float' = 2.0, fade_lag: 'float' = 0.0, time_width: 'float' = 1.0, **kwargs)` ← AnimationGroup

<details><summary>métodos próprios (1) · herdados: 26</summary>

- `__init__(self, vmobject: 'VMobject', stroke_width: 'float' = 2.0, fade_lag: 'float' = 0.0, time_width: 'float' = 1.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `FocusOn(focus_point: 'np.ndarray | Mobject', opacity: 'float' = 0.2, color: 'ManimColor' = '#888888', run_time: 'float' = 2, remover: 'bool' = True, **kwargs)` ← Transform

<details><summary>métodos próprios (3) · herdados: 26</summary>

- `__init__(self, focus_point: 'np.ndarray | Mobject', opacity: 'float' = 0.2, color: 'ManimColor' = '#888888', run_time: 'float' = 2, remover: 'bool' = True, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `create_starting_mobject(self) -> 'Dot'`
- `create_target(self) -> 'Dot'`

</details>

### `Indicate(mobject: 'Mobject', scale_factor: 'float' = 1.2, color: 'ManimColor' = '#FFFF00', rate_func: 'Callable[[float], float]' = <function there_and_back at 0x7f6ff3933600>, **kwargs)` ← Transform

<details><summary>métodos próprios (2) · herdados: 27</summary>

- `__init__(self, mobject: 'Mobject', scale_factor: 'float' = 1.2, color: 'ManimColor' = '#FFFF00', rate_func: 'Callable[[float], float]' = <function there_and_back at 0x7f6ff3933600>, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `create_target(self) -> 'Mobject'`

</details>

### `ShowCreationThenDestruction(vmobject: 'VMobject', time_width: 'float' = 2.0, **kwargs)` ← ShowPassingFlash
> Abstract class for ShowCreation and ShowPassingFlash

<details><summary>métodos próprios (1) · herdados: 25</summary>

- `__init__(self, vmobject: 'VMobject', time_width: 'float' = 2.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ShowCreationThenDestructionAround(mobject: 'Mobject', stroke_width: 'float' = 2.0, stroke_color: 'ManimColor' = '#FFFF00', buff: 'float' = 0.1, **kwargs)` ← AnimationOnSurroundingRectangle

### `ShowCreationThenFadeAround(mobject: 'Mobject', stroke_width: 'float' = 2.0, stroke_color: 'ManimColor' = '#FFFF00', buff: 'float' = 0.1, **kwargs)` ← AnimationOnSurroundingRectangle

### `ShowCreationThenFadeOut(mobject: 'Mobject', remover: 'bool' = True, **kwargs)` ← Succession

<details><summary>métodos próprios (1) · herdados: 26</summary>

- `__init__(self, mobject: 'Mobject', remover: 'bool' = True, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ShowPassingFlash(mobject: 'Mobject', time_width: 'float' = 0.1, remover: 'bool' = True, **kwargs)` ← ShowPartial
> Abstract class for ShowCreation and ShowPassingFlash

<details><summary>métodos próprios (3) · herdados: 23</summary>

- `__init__(self, mobject: 'Mobject', time_width: 'float' = 0.1, remover: 'bool' = True, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `finish(self) -> 'None'`
- `get_bounds(self, alpha: 'float') -> 'tuple[float, float]'`

</details>

### `ShowPassingFlashAround(mobject: 'Mobject', stroke_width: 'float' = 2.0, stroke_color: 'ManimColor' = '#FFFF00', buff: 'float' = 0.1, **kwargs)` ← AnimationOnSurroundingRectangle

### `TurnInsideOut(mobject: 'Mobject', path_arc: 'float' = 1.5707963267948966, **kwargs)` ← Transform

<details><summary>métodos próprios (2) · herdados: 27</summary>

- `__init__(self, mobject: 'Mobject', path_arc: 'float' = 1.5707963267948966, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `create_target(self) -> 'Mobject'`

</details>

### `VShowPassingFlash(vmobject: 'VMobject', time_width: 'float' = 0.3, taper_width: 'float' = 0.05, remover: 'bool' = True, **kwargs)` ← Animation

<details><summary>métodos próprios (5) · herdados: 21</summary>

- `__init__(self, vmobject: 'VMobject', time_width: 'float' = 0.3, taper_width: 'float' = 0.05, remover: 'bool' = True, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'`
- `finish(self) -> 'None'`
- `interpolate_submobject(self, submobject: 'VMobject', starting_sumobject: 'None', alpha: 'float') -> 'None'`
- `taper_kernel(self, x)`

</details>

### `WiggleOutThenIn(mobject: 'Mobject', scale_value: 'float' = 1.1, rotation_angle: 'float' = 0.06283185307179587, n_wiggles: 'int' = 6, scale_about_point: 'np.ndarray | None' = None, rotate_about_point: 'np.ndarray | None' = None, run_time: 'float' = 2, **kwargs)` ← Animation

<details><summary>métodos próprios (4) · herdados: 23</summary>

- `__init__(self, mobject: 'Mobject', scale_value: 'float' = 1.1, rotation_angle: 'float' = 0.06283185307179587, n_wiggles: 'int' = 6, scale_about_point: 'np.ndarray | None' = None, rotate_about_point: 'np.ndarray | None' = None, run_time: 'float' = 2, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_rotate_about_point(self) -> 'np.ndarray'`
- `get_scale_about_point(self) -> 'np.ndarray'`
- `interpolate_submobject(self, submobject: 'Mobject', starting_sumobject: 'Mobject', alpha: 'float') -> 'None'`

</details>

- `DEG` = `0.017453292519943295`
- `FRAME_X_RADIUS` = `7.111111111111111`
- `FRAME_Y_RADIUS` = `4.0`
- `GREY` = `'#888888'`
- `ORIGIN` = `array([0., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `SMALL_BUFF` = `0.1`
- `TAU` = `6.283185307179586`
- `TYPE_CHECKING` = `False`
- `UP` = `array([0., 1., 0.])`
- `YELLOW` = `'#FFFF00'`

## animation/movement

### `ComplexHomotopy(complex_homotopy: 'Callable[[complex, float], complex]', mobject: 'Mobject', **kwargs)` ← Homotopy

<details><summary>métodos próprios (1) · herdados: 25</summary>

- `__init__(self, complex_homotopy: 'Callable[[complex, float], complex]', mobject: 'Mobject', **kwargs)` — Given a function form (z, t) -> w, where z and w

</details>

### `Homotopy(homotopy: 'Callable[[float, float, float, float], Sequence[float]]', mobject: 'Mobject', run_time: 'float' = 3.0, **kwargs)` ← Animation

<details><summary>métodos próprios (3) · herdados: 23</summary>

- `__init__(self, homotopy: 'Callable[[float, float, float, float], Sequence[float]]', mobject: 'Mobject', run_time: 'float' = 3.0, **kwargs)` — Homotopy is a function from
- `function_at_time_t(self, t: 'float') -> 'Callable[[np.ndarray], Sequence[float]]'`
- `interpolate_submobject(self, submob: 'Mobject', start: 'Mobject', alpha: 'float') -> 'None'`

</details>

### `MoveAlongPath(mobject: 'Mobject', path: 'VMobject', suspend_mobject_updating: 'bool' = False, **kwargs)` ← Animation

<details><summary>métodos próprios (2) · herdados: 23</summary>

- `__init__(self, mobject: 'Mobject', path: 'VMobject', suspend_mobject_updating: 'bool' = False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_mobject(self, alpha: 'float') -> 'None'`

</details>

### `PhaseFlow(function: 'Callable[[np.ndarray], np.ndarray]', mobject: 'Mobject', virtual_time: 'float | None' = None, suspend_mobject_updating: 'bool' = False, rate_func: 'Callable[[float], float]' = <function linear at 0x7f6ff3932de0>, run_time: 'float' = 3.0, **kwargs)` ← Animation

<details><summary>métodos próprios (2) · herdados: 23</summary>

- `__init__(self, function: 'Callable[[np.ndarray], np.ndarray]', mobject: 'Mobject', virtual_time: 'float | None' = None, suspend_mobject_updating: 'bool' = False, rate_func: 'Callable[[float], float]' = <function linear at 0x7f6ff3932de0>, run_time: 'float' = 3.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_mobject(self, alpha: 'float') -> 'None'`

</details>

### `SmoothedVectorizedHomotopy(homotopy: 'Callable[[float, float, float, float], Sequence[float]]', mobject: 'Mobject', run_time: 'float' = 3.0, **kwargs)` ← Homotopy

- `TYPE_CHECKING` = `False`

## animation/numbers

### `ChangeDecimalToValue(decimal_mob: 'DecimalNumber', target_number: 'float | complex', **kwargs)` ← ChangingDecimal

<details><summary>métodos próprios (1) · herdados: 24</summary>

- `__init__(self, decimal_mob: 'DecimalNumber', target_number: 'float | complex', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ChangingDecimal(decimal_mob: 'DecimalNumber', number_update_func: 'Callable[[float], float]', suspend_mobject_updating: 'bool' = False, **kwargs)` ← Animation

<details><summary>métodos próprios (2) · herdados: 23</summary>

- `__init__(self, decimal_mob: 'DecimalNumber', number_update_func: 'Callable[[float], float]', suspend_mobject_updating: 'bool' = False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_mobject(self, alpha: 'float') -> 'None'`

</details>

### `CountInFrom(decimal_mob: 'DecimalNumber', source_number: 'float | complex' = 0, **kwargs)` ← ChangingDecimal

<details><summary>métodos próprios (1) · herdados: 24</summary>

- `__init__(self, decimal_mob: 'DecimalNumber', source_number: 'float | complex' = 0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

- `TYPE_CHECKING` = `False`

## animation/rotation

### `Rotate(mobject: 'Mobject', angle: 'float' = 3.141592653589793, axis: 'np.ndarray' = array([0., 0., 1.]), run_time: 'float' = 1, rate_func: 'Callable[[float], float]' = <function smooth at 0x7f6ff39332e0>, about_edge: 'np.ndarray' = array([0., 0., 0.]), **kwargs)` ← Rotating

<details><summary>métodos próprios (1) · herdados: 24</summary>

- `__init__(self, mobject: 'Mobject', angle: 'float' = 3.141592653589793, axis: 'np.ndarray' = array([0., 0., 1.]), run_time: 'float' = 1, rate_func: 'Callable[[float], float]' = <function smooth at 0x7f6ff39332e0>, about_edge: 'np.ndarray' = array([0., 0., 0.]), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Rotating(mobject: 'Mobject', angle: 'float' = 6.283185307179586, axis: 'np.ndarray' = array([0., 0., 1.]), about_point: 'np.ndarray | None' = None, about_edge: 'np.ndarray | None' = None, run_time: 'float' = 5.0, rate_func: 'Callable[[float], float]' = <function linear at 0x7f6ff3932de0>, suspend_mobject_updating: 'bool' = False, **kwargs)` ← Animation

<details><summary>métodos próprios (2) · herdados: 23</summary>

- `__init__(self, mobject: 'Mobject', angle: 'float' = 6.283185307179586, axis: 'np.ndarray' = array([0., 0., 1.]), about_point: 'np.ndarray | None' = None, about_edge: 'np.ndarray | None' = None, run_time: 'float' = 5.0, rate_func: 'Callable[[float], float]' = <function linear at 0x7f6ff3932de0>, suspend_mobject_updating: 'bool' = False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_mobject(self, alpha: 'float') -> 'None'`

</details>

- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `TAU` = `6.283185307179586`
- `TYPE_CHECKING` = `False`

## animation/specialized

### `Broadcast(focal_point: 'np.ndarray', small_radius: 'float' = 0.0, big_radius: 'float' = 5.0, n_circles: 'int' = 5, start_stroke_width: 'float' = 8.0, color: 'ManimColor' = '#FFFFFF', run_time: 'float' = 3.0, lag_ratio: 'float' = 0.2, remover: 'bool' = True, **kwargs)` ← LaggedStart

<details><summary>métodos próprios (1) · herdados: 26</summary>

- `__init__(self, focal_point: 'np.ndarray', small_radius: 'float' = 0.0, big_radius: 'float' = 5.0, n_circles: 'int' = 5, start_stroke_width: 'float' = 8.0, color: 'ManimColor' = '#FFFFFF', run_time: 'float' = 3.0, lag_ratio: 'float' = 0.2, remover: 'bool' = True, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

- `BLACK` = `'#000000'`
- `TYPE_CHECKING` = `False`
- `WHITE` = `'#FFFFFF'`

## animation/transform

### `ApplyComplexFunction(function: 'Callable[[complex], complex]', mobject: 'Mobject', **kwargs)` ← ApplyMethod

<details><summary>métodos próprios (2) · herdados: 28</summary>

- `__init__(self, function: 'Callable[[complex], complex]', mobject: 'Mobject', **kwargs)` — method is a method of Mobject, *args are arguments for
- `init_path_func(self) -> 'None'`

</details>

### `ApplyFunction(function: 'Callable[[Mobject], Mobject]', mobject: 'Mobject', **kwargs)` ← Transform

<details><summary>métodos próprios (2) · herdados: 27</summary>

- `__init__(self, function: 'Callable[[Mobject], Mobject]', mobject: 'Mobject', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `create_target(self) -> 'Mobject'`

</details>

### `ApplyMatrix(matrix: 'npt.ArrayLike', mobject: 'Mobject', **kwargs)` ← ApplyPointwiseFunction

<details><summary>métodos próprios (2) · herdados: 29</summary>

- `__init__(self, matrix: 'npt.ArrayLike', mobject: 'Mobject', **kwargs)` — method is a method of Mobject, *args are arguments for
- `initialize_matrix(self, matrix: 'npt.ArrayLike') -> 'np.ndarray'`

</details>

### `ApplyMethod(method: 'Callable', *args, **kwargs)` ← Transform

<details><summary>métodos próprios (3) · herdados: 27</summary>

- `__init__(self, method: 'Callable', *args, **kwargs)` — method is a method of Mobject, *args are arguments for
- `check_validity_of_input(self, method: 'Callable') -> 'None'`
- `create_target(self) -> 'Mobject'`

</details>

### `ApplyPointwiseFunction(function: 'Callable[[np.ndarray], np.ndarray]', mobject: 'Mobject', run_time: 'float' = 3.0, **kwargs)` ← ApplyMethod

<details><summary>métodos próprios (1) · herdados: 29</summary>

- `__init__(self, function: 'Callable[[np.ndarray], np.ndarray]', mobject: 'Mobject', run_time: 'float' = 3.0, **kwargs)` — method is a method of Mobject, *args are arguments for

</details>

### `ApplyPointwiseFunctionToCenter(function: 'Callable[[np.ndarray], np.ndarray]', mobject: 'Mobject', **kwargs)` ← Transform

<details><summary>métodos próprios (2) · herdados: 27</summary>

- `__init__(self, function: 'Callable[[np.ndarray], np.ndarray]', mobject: 'Mobject', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `create_target(self) -> 'Mobject'`

</details>

### `CyclicReplace(*mobjects: 'Mobject', path_arc=1.5707963267948966, **kwargs)` ← Transform

<details><summary>métodos próprios (2) · herdados: 27</summary>

- `__init__(self, *mobjects: 'Mobject', path_arc=1.5707963267948966, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `create_target(self) -> 'Mobject'`

</details>

### `FadeToColor(mobject: 'Mobject', color: 'ManimColor', **kwargs)` ← ApplyMethod

<details><summary>métodos próprios (1) · herdados: 29</summary>

- `__init__(self, mobject: 'Mobject', color: 'ManimColor', **kwargs)` — method is a method of Mobject, *args are arguments for

</details>

### `MoveToTarget(mobject: 'Mobject', **kwargs)` ← Transform

<details><summary>métodos próprios (2) · herdados: 28</summary>

- `__init__(self, mobject: 'Mobject', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `check_validity_of_input(self, mobject: 'Mobject') -> 'None'`

</details>

### `ReplacementTransform(mobject: 'Mobject', target_mobject: 'Mobject | None' = None, path_arc: 'float | Tuple[float, float]' = 0.0, path_arc_axis: 'np.ndarray' = array([0., 0., 1.]), path_func: 'Callable | None' = None, **kwargs)` ← Transform

### `Restore(mobject: 'Mobject', **kwargs)` ← Transform

<details><summary>métodos próprios (1) · herdados: 28</summary>

- `__init__(self, mobject: 'Mobject', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ScaleInPlace(mobject: 'Mobject', scale_factor: 'npt.ArrayLike', **kwargs)` ← ApplyMethod

<details><summary>métodos próprios (1) · herdados: 29</summary>

- `__init__(self, mobject: 'Mobject', scale_factor: 'npt.ArrayLike', **kwargs)` — method is a method of Mobject, *args are arguments for

</details>

### `ShrinkToCenter(mobject: 'Mobject', **kwargs)` ← ScaleInPlace

<details><summary>métodos próprios (1) · herdados: 29</summary>

- `__init__(self, mobject: 'Mobject', **kwargs)` — method is a method of Mobject, *args are arguments for

</details>

### `Swap(*mobjects: 'Mobject', path_arc=1.5707963267948966, **kwargs)` ← CyclicReplace
> Alternate name for CyclicReplace

### `Transform(mobject: 'Mobject', target_mobject: 'Mobject | None' = None, path_arc: 'float | Tuple[float, float]' = 0.0, path_arc_axis: 'np.ndarray' = array([0., 0., 1.]), path_func: 'Callable | None' = None, **kwargs)` ← Animation

<details><summary>métodos próprios (11) · herdados: 18</summary>

- `__init__(self, mobject: 'Mobject', target_mobject: 'Mobject | None' = None, path_arc: 'float | Tuple[float, float]' = 0.0, path_arc_axis: 'np.ndarray' = array([0., 0., 1.]), path_func: 'Callable | None' = None, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'`
- `check_target_mobject_validity(self) -> 'None'`
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'`
- `create_target(self) -> 'Mobject'`
- `get_all_families_zipped(self) -> 'zip[tuple[Mobject]]'`
- `get_all_mobjects(self) -> 'list[Mobject]'` — Ordering must match the ording of arguments to interpolate_submobject
- `get_interpolation_ends(self) -> 'tuple[Mobject, Mobject]'` — The two states every blend this animation makes runs between, in the order it blends
- `init_path_func(self) -> 'None'`
- `interpolate_submobject(self, submob: 'Mobject', start: 'Mobject', target_copy: 'Mobject', alpha: 'float')`
- `update_config(self, **kwargs) -> 'None'`

</details>

### `TransformFromCopy(mobject: 'Mobject', target_mobject: 'Mobject', **kwargs)` ← Transform

<details><summary>métodos próprios (1) · herdados: 28</summary>

- `__init__(self, mobject: 'Mobject', target_mobject: 'Mobject', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `TransformMatchingParts(source: 'Mobject', target: 'Mobject', matched_pairs: 'Iterable[tuple[Mobject, Mobject]]' = [], match_animation: 'type' = <class 'manimlib.animation.transform.Transform'>, mismatch_animation: 'type' = <class 'manimlib.animation.transform.Transform'>, run_time: 'float' = 2, lag_ratio: 'float' = 0, **kwargs)` ← AnimationGroup

<details><summary>métodos próprios (4) · herdados: 25</summary>

- `__init__(self, source: 'Mobject', target: 'Mobject', matched_pairs: 'Iterable[tuple[Mobject, Mobject]]' = [], match_animation: 'type' = <class 'manimlib.animation.transform.Transform'>, mismatch_animation: 'type' = <class 'manimlib.animation.transform.Transform'>, run_time: 'float' = 2, lag_ratio: 'float' = 0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_transform(self, source: 'Mobject', target: 'Mobject')`
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'`
- `find_pairs_with_matching_shapes(self, chars1: 'list[Mobject]', chars2: 'list[Mobject]') -> 'list[tuple[Mobject, Mobject]]'`

</details>

### `TransformMatchingShapes(source: 'Mobject', target: 'Mobject', matched_pairs: 'Iterable[tuple[Mobject, Mobject]]' = [], match_animation: 'type' = <class 'manimlib.animation.transform.Transform'>, mismatch_animation: 'type' = <class 'manimlib.animation.transform.Transform'>, run_time: 'float' = 2, lag_ratio: 'float' = 0, **kwargs)` ← TransformMatchingParts
> Alias for TransformMatchingParts

### `TransformMatchingStrings(source: 'StringMobject', target: 'StringMobject', matched_keys: 'Iterable[str]' = [], key_map: 'dict[str, str]' = {}, matched_pairs: 'Iterable[tuple[VMobject, VMobject]]' = [], **kwargs)` ← TransformMatchingParts

<details><summary>métodos próprios (2) · herdados: 28</summary>

- `__init__(self, source: 'StringMobject', target: 'StringMobject', matched_keys: 'Iterable[str]' = [], key_map: 'dict[str, str]' = {}, matched_pairs: 'Iterable[tuple[VMobject, VMobject]]' = [], **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `matching_blocks(self, source: 'StringMobject', target: 'StringMobject', matched_keys: 'Iterable[str]', key_map: 'dict[str, str]') -> 'list[tuple[VMobject, VMobject]]'`

</details>

### `TransformMatchingTex(source: 'StringMobject', target: 'StringMobject', matched_keys: 'Iterable[str]' = [], key_map: 'dict[str, str]' = {}, matched_pairs: 'Iterable[tuple[VMobject, VMobject]]' = [], **kwargs)` ← TransformMatchingStrings
> Alias for TransformMatchingStrings

- `DEG` = `0.017453292519943295`
- `OUT` = `array([0., 0., 1.])`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`

## camera

### `Camera(window: 'Optional[Window]' = None, frame_config: 'dict' = {}, resolution=(1920, 1080), fps: 'int' = 30, background_color: 'ManimColor' = '#000000', background_opacity: 'float' = 1.0, light_source_position: 'Vect3' = array([-10,  10,  10]), bundle_draws: 'bool' = True, draw_together: 'bool' = True, samples: 'int' = 0)`

<details><summary>métodos próprios (24) · herdados: 0</summary>

- `__init__(self, window: 'Optional[Window]' = None, frame_config: 'dict' = {}, resolution=(1920, 1080), fps: 'int' = 30, background_color: 'ManimColor' = '#000000', background_opacity: 'float' = 1.0, light_source_position: 'Vect3' = array([-10,  10,  10]), bundle_draws: 'bool' = True, draw_together: 'bool' = True, samples: 'int' = 0)` — Initialize self.  See help(type(self)) for accurate signature.
- `at_output_resolution(self)` — Draws at the resolution frames are written at rather than at the window's size, for
- `capture(self, *mobjects: 'Mobject') -> 'None'`
- `get_aspect_ratio(self)`
- `get_attachments(self) -> 'dict'` — The textures a frame is drawn into, and what to do with what they already hold.
- `get_frame_bytes(self) -> 'memoryview'` — The frame as it stands, four bytes to a pixel, a row at a time from the top, as a view
- `get_frame_center(self) -> 'np.ndarray'`
- `get_frame_height(self) -> 'float'`
- `get_frame_shape(self) -> 'tuple[float, float]'`
- `get_frame_width(self) -> 'float'`
- `get_image(self) -> 'Image.Image'`
- `get_location(self) -> 'tuple[float, float, float]'`
- `get_pixel_height(self) -> 'int'`
- `get_pixel_shape(self) -> 'tuple[int, int]'`
- `get_pixel_size(self) -> 'float'`
- `get_pixel_width(self) -> 'int'`
- `get_target_shape(self) -> 'tuple[int, int]'`
- `init_frame(self, **config) -> 'None'`
- `init_light_source(self) -> 'None'`
- `init_renderer(self) -> 'None'`
- `init_target(self) -> 'None'` — What every frame is drawn into: one color texture and one depth-stencil texture. Where
- `refresh_uniforms(self) -> 'None'` — What every shader reads about where the frame, the camera and the light are,
- `resize_frame_shape(self, fixed_dimension: 'bool' = False) -> 'None'` — Changes frame_shape to match the aspect ratio
- `resize_target(self) -> 'None'` — Makes what a frame is drawn into the size it ought to be, which changes when the

</details>

### `CameraFrame(frame_shape: 'tuple[float, float]' = (14.222222222222221, 8.0), center_point: 'Vect3' = array([0., 0., 0.]), fovy: 'float' = 0.7853981633974483, euler_axes: 'str' = 'zxz', z_index=-1, **kwargs)` ← Mobject
> Mathematical Object

<details><summary>métodos próprios (37) · herdados: 227</summary>

- `__init__(self, frame_shape: 'tuple[float, float]' = (14.222222222222221, 8.0), center_point: 'Vect3' = array([0., 0., 0.]), fovy: 'float' = 0.7853981633974483, euler_axes: 'str' = 'zxz', z_index=-1, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_ambient_rotation(self, angular_speed=0.017453292519943295)`
- `from_fixed_frame_point(self, point: 'Vect3', relative: 'bool' = False)`
- `get_aspect_ratio(self)`
- `get_center(self) -> 'np.ndarray'`
- `get_euler_angles(self) -> 'np.ndarray'`
- `get_field_of_view(self) -> 'float'`
- `get_focal_distance(self) -> 'float'`
- `get_gamma(self)`
- `get_height(self) -> 'float'`
- `get_implied_camera_location(self) -> 'np.ndarray'`
- `get_inv_view_matrix(self)`
- `get_inverse_camera_rotation_matrix(self)`
- `get_orientation(self)`
- `get_phi(self)`
- `get_scale(self)`
- `get_shape(self)`
- `get_theta(self)`
- `get_view_matrix(self, refresh=False)` — Returns a 4x4 for the affine transformation mapping a point
- `get_width(self) -> 'float'`
- `increment_euler_angles(self, dtheta: 'float' = 0, dphi: 'float' = 0, dgamma: 'float' = 0, units: 'float' = 1)`
- `increment_gamma(self, dgamma: 'float', units=1)`
- `increment_phi(self, dphi: 'float', units=1)`
- `increment_theta(self, dtheta: 'float', units=1)`
- `make_orientation_default(self)`
- `reorient(self, theta_degrees: 'float | None' = None, phi_degrees: 'float | None' = None, gamma_degrees: 'float | None' = None, center: 'Vect3 | tuple[float, float, float] | None' = None, height: 'float | None' = None)` — Shortcut for set_euler_angles, defaulting to taking
- `rotate(self, angle: 'float', axis: 'np.ndarray' = array([0., 0., 1.]), **kwargs)`
- `set_euler_angles(self, theta: 'float | None' = None, phi: 'float | None' = None, gamma: 'float | None' = None, units: 'float' = 1)`
- `set_euler_axes(self, seq: 'str')`
- `set_field_of_view(self, field_of_view: 'float')`
- `set_focal_distance(self, focal_distance: 'float')`
- `set_gamma(self, gamma: 'float')`
- `set_orientation(self, rotation: 'Rotation')`
- `set_phi(self, phi: 'float')`
- `set_theta(self, theta: 'float')`
- `to_default_state(self)`
- `to_fixed_frame_point(self, point: 'Vect3', relative: 'bool' = False)`

</details>

### `FrameStream(camera: 'Camera', sink, behind: 'int' = 1)`
> Frames off the gpu and into somewhere they are being written, staying a frame behind so

<details><summary>métodos próprios (4) · herdados: 0</summary>

- `__init__(self, camera: 'Camera', sink, behind: 'int' = 1)` — Initialize self.  See help(type(self)) for accurate signature.
- `drain(self) -> 'None'` — Writes every frame still in flight. Whatever is being written to has to be told this
- `send(self) -> 'None'` — Asks for the frame as it stands, and writes whichever one is ready
- `write_oldest(self) -> 'None'`

</details>

### `ThreeDCamera(samples: 'int' = 4, **kwargs)` ← Camera

<details><summary>métodos próprios (1) · herdados: 23</summary>

- `__init__(self, samples: 'int' = 4, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

- `BLACK` = `'#000000'`
- `COLOR_FORMAT` = `'rgba8unorm'`
- `COMMON_UNIFORMS` = `(('is_fixed_in_frame', 1), ('shading', 3), ('clip_plane0', 4), ('clip_plane1', 4), ('clip_plane2', 4), ('clip_plane3'...`
- `DEFAULT_RESOLUTION` = `(1920, 1080)`
- `DEG` = `0.017453292519943295`
- `DEPTH_STENCIL_FORMAT` = `'depth24plus-stencil8'`
- `DOWN` = `array([ 0., -1.,  0.])`
- `FRAME_HEIGHT` = `8.0`
- `FRAME_SHAPE` = `(14.222222222222221, 8.0)`
- `FRAME_WIDTH` = `14.222222222222221`
- `LEFT` = `array([-1.,  0.,  0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `RADIANS` = `1`
- `RIGHT` = `array([1., 0., 0.])`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `UP` = `array([0., 1., 0.])`

## constants

- `ASPECT_RATIO` = `1.7777777777777777`
- `BLACK` = `'#000000'`
- `BLUE` = `'#58C4DD'`
- `BLUE_A` = `'#C7E9F1'`
- `BLUE_B` = `'#9CDCEB'`
- `BLUE_C` = `'#58C4DD'`
- `BLUE_D` = `'#29ABCA'`
- `BLUE_E` = `'#1C758A'`
- `BOLD` = `'BOLD'`
- `BOTTOM` = `array([ 0., -4.,  0.])`
- `COLORMAP_3B1B` = `['#1C758A', '#83C167', '#FFFF00', '#FC6255']`
- `DARK_BROWN` = `'#8B4513'`
- `DEFAULT_LIGHT_COLOR` = `'#BBBBBB'`
- `DEFAULT_MOBJECT_COLOR` = `'#FFFFFF'`
- `DEFAULT_MOBJECT_TO_EDGE_BUFF` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFF` = `0.25`
- `DEFAULT_PIXEL_HEIGHT` = `1080`
- `DEFAULT_PIXEL_WIDTH` = `1920`
- `DEFAULT_RESOLUTION` = `(1920, 1080)`
- `DEFAULT_STROKE_WIDTH` = `4.0`
- `DEFAULT_VMOBJECT_FILL_COLOR` = `'#888888'`
- `DEFAULT_VMOBJECT_STROKE_COLOR` = `'#DDDDDD'`
- `DEG` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `FRAME_HEIGHT` = `8.0`
- `FRAME_SHAPE` = `(14.222222222222221, 8.0)`
- `FRAME_WIDTH` = `14.222222222222221`
- `FRAME_X_RADIUS` = `7.111111111111111`
- `FRAME_Y_RADIUS` = `4.0`
- `GOLD` = `'#F0AC5F'`
- `GOLD_A` = `'#F7C797'`
- `GOLD_B` = `'#F9B775'`
- `GOLD_C` = `'#F0AC5F'`
- `GOLD_D` = `'#E1A158'`
- `GOLD_E` = `'#C78D46'`
- `GREEN` = `'#83C167'`
- `GREEN_A` = `'#C9E2AE'`
- `GREEN_B` = `'#A6CF8C'`
- `GREEN_C` = `'#83C167'`
- `GREEN_D` = `'#77B05D'`
- `GREEN_E` = `'#699C52'`
- `GREEN_SCREEN` = `'#00FF00'`
- `GREY` = `'#888888'`
- `GREY_A` = `'#DDDDDD'`
- `GREY_B` = `'#BBBBBB'`
- `GREY_BROWN` = `'#736357'`
- `GREY_C` = `'#888888'`
- `GREY_D` = `'#444444'`
- `GREY_E` = `'#222222'`
- `IN` = `array([ 0.,  0., -1.])`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1.0`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT_SIDE` = `array([-7.11111111,  0.        ,  0.        ])`
- `LIGHT_BROWN` = `'#CD853F'`
- `LIGHT_PINK` = `'#DC75CD'`
- `MANIM_COLORS` = `['#1C758A', '#29ABCA', '#58C4DD', '#9CDCEB', '#C7E9F1', '#49A88F', '#55C1A7', '#5CD0B3', '#76DDC0', '#ACEAD7', '#699C...`
- `MAROON` = `'#C55F73'`
- `MAROON_A` = `'#ECABC1'`
- `MAROON_B` = `'#EC92AB'`
- `MAROON_C` = `'#C55F73'`
- `MAROON_D` = `'#A24D61'`
- `MAROON_E` = `'#94424F'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NULL_POINTS` = `array([[0., 0., 0.]])`
- `OBLIQUE` = `'OBLIQUE'`
- `ORANGE` = `'#FF862F'`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `PINK` = `'#D147BD'`
- `PURE_BLUE` = `'#0000FF'`
- `PURE_GREEN` = `'#00FF00'`
- `PURE_RED` = `'#FF0000'`
- `PURPLE` = `'#9A72AC'`
- `PURPLE_A` = `'#CAA3E8'`
- `PURPLE_B` = `'#B189C6'`
- `PURPLE_C` = `'#9A72AC'`
- `PURPLE_D` = `'#715582'`
- `PURPLE_E` = `'#644172'`
- `RADIANS` = `1`
- `RED` = `'#FC6255'`
- `RED_A` = `'#F7A1A3'`
- `RED_B` = `'#FF8080'`
- `RED_C` = `'#FC6255'`
- `RED_D` = `'#E65A4C'`
- `RED_E` = `'#CF5044'`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT_SIDE` = `array([7.11111111, 0.        , 0.        ])`
- `SMALL_BUFF` = `0.1`
- `TAU` = `6.283185307179586`
- `TEAL` = `'#5CD0B3'`
- `TEAL_A` = `'#ACEAD7'`
- `TEAL_B` = `'#76DDC0'`
- `TEAL_C` = `'#5CD0B3'`
- `TEAL_D` = `'#55C1A7'`
- `TEAL_E` = `'#49A88F'`
- `TOP` = `array([0., 4., 0.])`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `WHITE` = `'#FFFFFF'`
- `X_AXIS` = `array([1., 0., 0.])`
- `YELLOW` = `'#FFFF00'`
- `YELLOW_A` = `'#FFF1B6'`
- `YELLOW_B` = `'#FFEA94'`
- `YELLOW_C` = `'#FFFF00'`
- `YELLOW_D` = `'#F4D345'`
- `YELLOW_E` = `'#E8C11C'`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Z_AXIS` = `array([0., 0., 1.])`

## mobject/3d

### `Cone(u_range: 'Tuple[float, float]' = (0, 6.283185307179586), v_range: 'Tuple[float, float]' = (0, 1), *args, **kwargs)` ← Cylinder
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 246</summary>

- `__init__(self, u_range: 'Tuple[float, float]' = (0, 6.283185307179586), v_range: 'Tuple[float, float]' = (0, 1), *args, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `uv_func(self, u: 'float', v: 'float') -> 'np.ndarray'`

</details>

### `Cube(color: 'ManimColor' = '#58C4DD', opacity: 'float' = 1, shading: 'Tuple[float, float, float]' = (0.1, 0.5, 0.1), square_resolution: 'Tuple[int, int]' = (2, 2), side_length: 'float' = 2, **kwargs)` ← Group
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 232</summary>

- `__init__(self, color: 'ManimColor' = '#58C4DD', opacity: 'float' = 1, shading: 'Tuple[float, float, float]' = (0.1, 0.5, 0.1), square_resolution: 'Tuple[int, int]' = (2, 2), side_length: 'float' = 2, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Cylinder(u_range: 'Tuple[float, float]' = (0, 6.283185307179586), v_range: 'Tuple[float, float]' = (-1, 1), resolution: 'Tuple[int, int]' = (101, 11), height: 'float' = 2, radius: 'float' = 1, axis: 'Vect3' = array([0., 0., 1.]), **kwargs)` ← Surface
> Mathematical Object

<details><summary>métodos próprios (3) · herdados: 245</summary>

- `__init__(self, u_range: 'Tuple[float, float]' = (0, 6.283185307179586), v_range: 'Tuple[float, float]' = (-1, 1), resolution: 'Tuple[int, int]' = (101, 11), height: 'float' = 2, radius: 'float' = 1, axis: 'Vect3' = array([0., 0., 1.]), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `init_points(self)`
- `uv_func(self, u: 'float', v: 'float') -> 'np.ndarray'`

</details>

### `Disk3D(radius: 'float' = 1, u_range: 'Tuple[float, float]' = (0, 1), v_range: 'Tuple[float, float]' = (0, 6.283185307179586), resolution: 'Tuple[int, int]' = (2, 100), **kwargs)` ← Surface
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 246</summary>

- `__init__(self, radius: 'float' = 1, u_range: 'Tuple[float, float]' = (0, 1), v_range: 'Tuple[float, float]' = (0, 6.283185307179586), resolution: 'Tuple[int, int]' = (2, 100), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `uv_func(self, u: 'float', v: 'float') -> 'np.ndarray'`

</details>

### `Dodecahedron(fill_color: 'ManimColor' = '#1C758A', fill_opacity: 'float' = 1, stroke_color: 'ManimColor' = '#1C758A', stroke_width: 'float' = 1, shading: 'Tuple[float, float, float]' = (0.2, 0.2, 0.2), **kwargs)` ← VGroup3D
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, fill_color: 'ManimColor' = '#1C758A', fill_opacity: 'float' = 1, stroke_color: 'ManimColor' = '#1C758A', stroke_width: 'float' = 1, shading: 'Tuple[float, float, float]' = (0.2, 0.2, 0.2), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Line3D(start: 'Vect3', end: 'Vect3', width: 'float' = 0.05, resolution: 'Tuple[int, int]' = (21, 25), **kwargs)` ← Cylinder
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 247</summary>

- `__init__(self, start: 'Vect3', end: 'Vect3', width: 'float' = 0.05, resolution: 'Tuple[int, int]' = (21, 25), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Prism(width: 'float' = 3.0, height: 'float' = 2.0, depth: 'float' = 1.0, **kwargs)` ← Cube
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 232</summary>

- `__init__(self, width: 'float' = 3.0, height: 'float' = 2.0, depth: 'float' = 1.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Prismify(vmobject, depth=1.0, direction=array([ 0.,  0., -1.]), **kwargs)` ← VGroup3D
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, vmobject, depth=1.0, direction=array([ 0.,  0., -1.]), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Sphere(u_range: 'Tuple[float, float]' = (0, 6.283185307179586), v_range: 'Tuple[float, float]' = (0, 3.141592653589793), resolution: 'Tuple[int, int]' = (101, 51), radius: 'float' = 1.0, clockwise=False, **kwargs)` ← Surface
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 246</summary>

- `__init__(self, u_range: 'Tuple[float, float]' = (0, 6.283185307179586), v_range: 'Tuple[float, float]' = (0, 3.141592653589793), resolution: 'Tuple[int, int]' = (101, 51), radius: 'float' = 1.0, clockwise=False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `uv_func(self, u: 'float', v: 'float') -> 'np.ndarray'`

</details>

### `Square3D(side_length: 'float' = 2.0, u_range: 'Tuple[float, float]' = (-1, 1), v_range: 'Tuple[float, float]' = (-1, 1), resolution: 'Tuple[int, int]' = (2, 2), **kwargs)` ← Surface
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 246</summary>

- `__init__(self, side_length: 'float' = 2.0, u_range: 'Tuple[float, float]' = (-1, 1), v_range: 'Tuple[float, float]' = (-1, 1), resolution: 'Tuple[int, int]' = (2, 2), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `uv_func(self, u: 'float', v: 'float') -> 'np.ndarray'`

</details>

### `SurfaceMesh(uv_surface: 'Surface', resolution: 'Tuple[int, int]' = (21, 11), stroke_width: 'float' = 1, stroke_color: 'ManimColor' = '#DDDDDD', normal_nudge: 'float' = 0.01, depth_test: 'bool' = True, **kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 318</summary>

- `__init__(self, uv_surface: 'Surface', resolution: 'Tuple[int, int]' = (21, 11), stroke_width: 'float' = 1, stroke_color: 'ManimColor' = '#DDDDDD', normal_nudge: 'float' = 0.01, depth_test: 'bool' = True, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `init_points(self) -> 'None'`

</details>

### `Torus(u_range: 'Tuple[float, float]' = (0, 6.283185307179586), v_range: 'Tuple[float, float]' = (0, 6.283185307179586), r1: 'float' = 3.0, r2: 'float' = 1.0, **kwargs)` ← Surface
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 246</summary>

- `__init__(self, u_range: 'Tuple[float, float]' = (0, 6.283185307179586), v_range: 'Tuple[float, float]' = (0, 6.283185307179586), r1: 'float' = 3.0, r2: 'float' = 1.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `uv_func(self, u: 'float', v: 'float') -> 'np.ndarray'`

</details>

### `VCube(side_length: 'float' = 2.0, fill_color: 'ManimColor' = '#29ABCA', fill_opacity: 'float' = 1, stroke_width: 'float' = 0, **kwargs)` ← VGroup3D
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, side_length: 'float' = 2.0, fill_color: 'ManimColor' = '#29ABCA', fill_opacity: 'float' = 1, stroke_width: 'float' = 0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `VGroup3D(*vmobjects: 'VMobject', depth_test: 'bool' = True, shading: 'Tuple[float, float, float]' = (0.2, 0.2, 0.2), **kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, *vmobjects: 'VMobject', depth_test: 'bool' = True, shading: 'Tuple[float, float, float]' = (0.2, 0.2, 0.2), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `VPrism(width: 'float' = 3.0, height: 'float' = 2.0, depth: 'float' = 1.0, **kwargs)` ← VCube
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, width: 'float' = 3.0, height: 'float' = 2.0, depth: 'float' = 1.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

- `BLACK` = `'#000000'`
- `BLUE` = `'#58C4DD'`
- `BLUE_D` = `'#29ABCA'`
- `BLUE_E` = `'#1C758A'`
- `GREY_A` = `'#DDDDDD'`
- `IN` = `array([ 0.,  0., -1.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `RIGHT` = `array([1., 0., 0.])`
- `TAU` = `6.283185307179586`
- `TYPE_CHECKING` = `False`
- **`square_to_cube_faces(square: 'T') -> 'list[T]'`**

## mobject/core

### `AnimatedBoundary(vmobject: 'VMobject', colors: 'List[ManimColor]' = ['#29ABCA', '#9CDCEB', '#1C758A', '#736357'], max_stroke_width: 'float' = 3.0, cycle_rate: 'float' = 0.5, back_and_forth: 'bool' = True, draw_rate_func: 'Callable[[float], float]' = <function smooth at 0x7f6ff39332e0>, fade_rate_func: 'Callable[[float], float]' = <function smooth at 0x7f6ff39332e0>, **kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (3) · herdados: 319</summary>

- `__init__(self, vmobject: 'VMobject', colors: 'List[ManimColor]' = ['#29ABCA', '#9CDCEB', '#1C758A', '#736357'], max_stroke_width: 'float' = 3.0, cycle_rate: 'float' = 0.5, back_and_forth: 'bool' = True, draw_rate_func: 'Callable[[float], float]' = <function smooth at 0x7f6ff39332e0>, fade_rate_func: 'Callable[[float], float]' = <function smooth at 0x7f6ff39332e0>, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `full_family_become_partial(self, mob1: 'VMobject', mob2: 'VMobject', a: 'float', b: 'float') -> 'Self'`
- `update_boundary_copies(self, dt: 'float') -> 'Self'`

</details>

### `Axes(x_range: 'RangeSpecifier' = (-8.0, 8.0, 1.0), y_range: 'RangeSpecifier' = (-4.0, 4.0, 1.0), axis_config: 'dict' = {}, x_axis_config: 'dict' = {}, y_axis_config: 'dict' = {}, height: 'float | None' = None, width: 'float | None' = None, unit_size: 'float' = 1.0, **kwargs)` ← VGroup, CoordinateSystem
> Mathematical Object

<details><summary>métodos próprios (7) · herdados: 347</summary>

- `__init__(self, x_range: 'RangeSpecifier' = (-8.0, 8.0, 1.0), y_range: 'RangeSpecifier' = (-4.0, 4.0, 1.0), axis_config: 'dict' = {}, x_axis_config: 'dict' = {}, y_axis_config: 'dict' = {}, height: 'float | None' = None, width: 'float | None' = None, unit_size: 'float' = 1.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_coordinate_labels(self, x_values: 'Iterable[float] | None' = None, y_values: 'Iterable[float] | None' = None, excluding: 'Iterable[float]' = [0], **kwargs) -> 'VGroup'`
- `coords_to_point(self, *coords: 'float | VectN') -> 'Vect3 | Vect3Array'`
- `create_axis(self, range_terms: 'RangeSpecifier', axis_config: 'dict', length: 'float | None') -> 'NumberLine'`
- `get_all_ranges(self) -> 'list[Sequence[float]]'`
- `get_axes(self) -> 'VGroup'`
- `point_to_coords(self, point: 'Vect3 | Vect3Array') -> 'tuple[float | VectN, ...]'`

</details>

### `BackgroundRectangle(mobject: 'Mobject', color: 'ManimColor' = None, stroke_width: 'float' = 0, stroke_opacity: 'float' = 0, fill_opacity: 'float' = 0.75, buff: 'float' = 0, **kwargs)` ← SurroundingRectangle
> Creates a rectangle at the center of the screen.

<details><summary>métodos próprios (4) · herdados: 319</summary>

- `__init__(self, mobject: 'Mobject', color: 'ManimColor' = None, stroke_width: 'float' = 0, stroke_opacity: 'float' = 0, fill_opacity: 'float' = 0.75, buff: 'float' = 0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_fill_color(self) -> 'Color'`
- `pointwise_become_partial(self, mobject: 'Mobject', a: 'float', b: 'float') -> 'Self'` — Set points in such a way as to become only
- `set_style(self, stroke_color: 'ManimColor | None' = None, stroke_width: 'float | None' = None, fill_color: 'ManimColor | None' = None, fill_opacity: 'float | None' = None, family: 'bool' = True, **kwargs) -> 'Self'`

</details>

### `BarChart(values: 'Iterable[float]', height: 'float' = 4, width: 'float' = 6, n_ticks: 'int' = 4, include_x_ticks: 'bool' = False, tick_width: 'float' = 0.2, tick_height: 'float' = 0.15, label_y_axis: 'bool' = True, y_axis_label_height: 'float' = 0.25, max_value: 'float' = 1, bar_colors: 'list[ManimColor]' = ['#58C4DD', '#FFFF00'], bar_fill_opacity: 'float' = 0.8, bar_stroke_width: 'float' = 3, bar_names: 'list[str]' = [], bar_label_scale_val: 'float' = 0.75, **kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (4) · herdados: 319</summary>

- `__init__(self, values: 'Iterable[float]', height: 'float' = 4, width: 'float' = 6, n_ticks: 'int' = 4, include_x_ticks: 'bool' = False, tick_width: 'float' = 0.2, tick_height: 'float' = 0.15, label_y_axis: 'bool' = True, y_axis_label_height: 'float' = 0.25, max_value: 'float' = 1, bar_colors: 'list[ManimColor]' = ['#58C4DD', '#FFFF00'], bar_fill_opacity: 'float' = 0.8, bar_stroke_width: 'float' = 3, bar_names: 'list[str]' = [], bar_label_scale_val: 'float' = 0.75, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_axes(self) -> 'None'`
- `add_bars(self, values: 'Iterable[float]') -> 'None'`
- `change_bar_values(self, values: 'Iterable[float]') -> 'None'`

</details>

### `Button(mobject: 'Mobject', on_click: 'Callable[[Mobject]]', **kwargs)` ← Mobject
> Pass any mobject and register an on_click method

<details><summary>métodos próprios (2) · herdados: 232</summary>

- `__init__(self, mobject: 'Mobject', on_click: 'Callable[[Mobject]]', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `mob_on_mouse_press(self, mob: 'Mobject', event_data) -> 'bool'`

</details>

### `Checkbox(value: 'bool' = True, value_type: 'np.dtype' = dtype('bool'), rect_kwargs: 'dict' = {'width': 0.5, 'height': 0.5, 'fill_opacity': 0.0}, checkmark_kwargs: 'dict' = {'stroke_color': '#83C167', 'stroke_width': 6}, cross_kwargs: 'dict' = {'stroke_color': '#FC6255', 'stroke_width': 6}, box_content_buff: 'float' = 0.1, **kwargs)` ← ControlMobject
> Not meant to be displayed.  Instead the position encodes some

<details><summary>métodos próprios (7) · herdados: 235</summary>

- `__init__(self, value: 'bool' = True, value_type: 'np.dtype' = dtype('bool'), rect_kwargs: 'dict' = {'width': 0.5, 'height': 0.5, 'fill_opacity': 0.0}, checkmark_kwargs: 'dict' = {'stroke_color': '#83C167', 'stroke_width': 6}, cross_kwargs: 'dict' = {'stroke_color': '#FC6255', 'stroke_width': 6}, box_content_buff: 'float' = 0.1, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `assert_value(self, value: 'bool') -> 'None'`
- `get_checkmark(self) -> 'VGroup'`
- `get_cross(self) -> 'VGroup'`
- `on_mouse_press(self, mob: 'Mobject', event_data) -> 'None'`
- `set_value_anim(self, value: 'bool') -> 'None'`
- `toggle_value(self) -> 'None'`

</details>

### `ColorSliders(sliders_kwargs: 'dict' = {}, rect_kwargs: 'dict' = {'width': 2.0, 'height': 0.5, 'stroke_opacity': 1.0}, background_grid_kwargs: 'dict' = {'colors': ['#DDDDDD', '#888888'], 'single_square_len': 0.1}, sliders_buff: 'float' = 0.5, default_rgb_value: 'int' = 255, default_a_value: 'int' = 1, **kwargs)` ← Group
> Mathematical Object

<details><summary>métodos próprios (6) · herdados: 232</summary>

- `__init__(self, sliders_kwargs: 'dict' = {}, rect_kwargs: 'dict' = {'width': 2.0, 'height': 0.5, 'stroke_opacity': 1.0}, background_grid_kwargs: 'dict' = {'colors': ['#DDDDDD', '#888888'], 'single_square_len': 0.1}, sliders_buff: 'float' = 0.5, default_rgb_value: 'int' = 255, default_a_value: 'int' = 1, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_background(self) -> 'VGroup'`
- `get_picked_color(self) -> 'str'`
- `get_picked_opacity(self) -> 'float'`
- `get_value(self) -> 'np.ndarary'`
- `set_value(self, r: 'float', g: 'float', b: 'float', a: 'float')`

</details>

### `ComplexPlane(x_range: 'RangeSpecifier' = (-8.0, 8.0, 1.0), y_range: 'RangeSpecifier' = (-4.0, 4.0, 1.0), background_line_style: 'dict' = {'stroke_color': '#29ABCA', 'stroke_width': 2, 'stroke_opacity': 1}, faded_line_style: 'dict' = {'stroke_width': 1, 'stroke_opacity': 0.25}, faded_line_ratio: 'int' = 4, make_smooth_after_applying_functions: 'bool' = True, **kwargs)` ← NumberPlane
> Mathematical Object

<details><summary>métodos próprios (7) · herdados: 360</summary>

- `add_coordinate_labels(self, numbers: 'list[complex] | None' = None, skip_first: 'bool' = True, font_size: 'int' = 36, **kwargs) -> 'Self'`
- `get_default_coordinate_values(self, skip_first: 'bool' = True) -> 'list[complex]'`
- `get_unit_size(self) -> 'float'`
- `n2p(self, number: 'complex | float | np.array') -> 'Vect3'`
- `number_to_point(self, number: 'complex | float | np.array') -> 'Vect3'`
- `p2n(self, point: 'Vect3') -> 'complex'`
- `point_to_number(self, point: 'Vect3') -> 'complex'`

</details>

### `ControlMobject(value: 'float', *mobjects: 'Mobject', **kwargs)` ← ValueTracker
> Not meant to be displayed.  Instead the position encodes some

<details><summary>métodos próprios (4) · herdados: 234</summary>

- `__init__(self, value: 'float', *mobjects: 'Mobject', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `assert_value(self, value)`
- `set_value(self, value: 'float')`
- `set_value_anim(self, value)`

</details>

### `ControlPanel(*controls: 'ControlMobject', panel_kwargs: 'dict' = {'width': 3.5555555555555554, 'height': 8.25, 'fill_color': '#888888', 'fill_opacity': 1.0, 'stroke_width': 0.0}, opener_kwargs: 'dict' = {'width': 1.7777777777777777, 'height': 0.5, 'fill_color': '#888888', 'fill_opacity': 1.0}, opener_text_kwargs: 'dict' = {'text': 'Control Panel', 'font_size': 20}, **kwargs)` ← Group
> Mathematical Object

<details><summary>métodos próprios (8) · herdados: 232</summary>

- `__init__(self, *controls: 'ControlMobject', panel_kwargs: 'dict' = {'width': 3.5555555555555554, 'height': 8.25, 'fill_color': '#888888', 'fill_opacity': 1.0, 'stroke_width': 0.0}, opener_kwargs: 'dict' = {'width': 1.7777777777777777, 'height': 0.5, 'fill_color': '#888888', 'fill_opacity': 1.0}, opener_text_kwargs: 'dict' = {'text': 'Control Panel', 'font_size': 20}, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_controls(self, *new_controls: 'ControlMobject') -> 'None'`
- `close_panel(self)`
- `move_panel_and_controls_to_panel_opener(self) -> 'None'`
- `open_panel(self)`
- `panel_on_mouse_scroll(self, mob, event_data: 'dict[str, np.ndarray]') -> 'bool'`
- `panel_opener_on_mouse_drag(self, mob, event_data: 'dict[str, np.ndarray]') -> 'bool'`
- `remove_controls(self, *controls_to_remove: 'ControlMobject') -> 'None'`

</details>

### `CoordinateSystem(x_range: 'RangeSpecifier' = (-8.0, 8.0, 1.0), y_range: 'RangeSpecifier' = (-4.0, 4.0, 1.0), num_sampled_graph_points_per_tick: 'int' = 5)` ← ABC
> Abstract class for Axes and NumberPlane

<details><summary>métodos próprios (33) · herdados: 0</summary>

- `__init__(self, x_range: 'RangeSpecifier' = (-8.0, 8.0, 1.0), y_range: 'RangeSpecifier' = (-4.0, 4.0, 1.0), num_sampled_graph_points_per_tick: 'int' = 5)` — Initialize self.  See help(type(self)) for accurate signature.
- `angle_of_tangent(self, x: 'float', graph: 'ParametricCurve', dx: 'float' = 1e-08) -> 'float'`
- `bind_graph_to_func(self, graph: 'VMobject', func: 'Callable[[VectN], VectN]', jagged: 'bool' = False, get_discontinuities: 'Optional[Callable[[], Vect3]]' = None) -> 'VMobject'` — Use for graphing functions which might change over time, or change with
- `c2p(self, *coords: 'float') -> 'Vect3 | Vect3Array'` — Abbreviation for coords_to_point
- `coords_to_point(self, *coords: 'float | VectN') -> 'Vect3 | Vect3Array'`
- `get_all_ranges(self) -> 'list[np.ndarray]'`
- `get_area_under_graph(self, graph, x_range=None, fill_color='#58C4DD', fill_opacity=0.5)`
- `get_axes(self) -> 'VGroup'`
- `get_axis(self, index: 'int') -> 'NumberLine'`
- `get_axis_label(self, label_tex: 'str', axis: 'Vect3', edge: 'Vect3', direction: 'Vect3', buff: 'float' = 0.25, ensure_on_screen: 'bool' = False, **kwargs) -> 'Tex'`
- `get_axis_labels(self, x_label_tex: 'str' = 'x', y_label_tex: 'str' = 'y', **kwargs) -> 'VGroup'`
- `get_graph(self, function: 'Callable[[float], float]', x_range: 'Sequence[float] | None' = None, bind: 'bool' = False, **kwargs) -> 'ParametricCurve'`
- `get_graph_label(self, graph: 'ParametricCurve', label: 'str | Mobject' = 'f(x)', x: 'float | None' = None, direction: 'Vect3' = array([1., 0., 0.]), buff: 'float' = 0.25, color: 'ManimColor | None' = None) -> 'Tex | Mobject'`
- `get_h_line(self, point: 'Vect3', **kwargs)`
- `get_h_line_to_graph(self, x: 'float', graph: 'ParametricCurve', **kwargs)`
- `get_line_from_axis_to_point(self, index: 'int', point: 'Vect3', line_func: 'Type[T]' = <class 'manimlib.mobject.geometry.DashedLine'>, color: 'ManimColor' = '#DDDDDD', stroke_width: 'float' = 2) -> 'T'`
- `get_origin(self) -> 'Vect3'`
- `get_parametric_curve(self, function: 'Callable[[float], Vect3]', **kwargs) -> 'ParametricCurve'`
- `get_riemann_rectangles(self, graph: 'ParametricCurve', x_range: 'Sequence[float]' = None, dx: 'float | None' = None, input_sample_type: 'str' = 'left', stroke_width: 'float' = 1, stroke_color: 'ManimColor' = '#000000', fill_opacity: 'float' = 1, colors: 'Iterable[ManimColor]' = ('#58C4DD', '#83C167'), negative_color: 'ManimColor' = '#FC6255', stroke_background: 'bool' = True, show_signed_area: 'bool' = True) -> 'VGroup'`
- `get_scatterplot(self, x_values: 'Vect3Array', y_values: 'Vect3Array', **dot_config)`
- `get_tangent_line(self, x: 'float', graph: 'ParametricCurve', length: 'float' = 5, line_func: 'Type[T]' = <class 'manimlib.mobject.geometry.Line'>) -> 'T'`
- `get_v_line(self, point: 'Vect3', **kwargs)`
- `get_v_line_to_graph(self, x: 'float', graph: 'ParametricCurve', **kwargs)`
- `get_x_axis(self) -> 'NumberLine'`
- `get_x_axis_label(self, label_tex: 'str', edge: 'Vect3' = array([1., 0., 0.]), direction: 'Vect3' = array([-1., -1.,  0.]), **kwargs) -> 'Tex'`
- `get_y_axis(self) -> 'NumberLine'`
- `get_y_axis_label(self, label_tex: 'str', edge: 'Vect3' = array([0., 1., 0.]), direction: 'Vect3' = array([ 1., -1.,  0.]), **kwargs) -> 'Tex'`
- `get_z_axis(self) -> 'NumberLine'`
- `i2gp(self, x: 'float', graph: 'ParametricCurve') -> 'Vect3 | None'` — Alias for input_to_graph_point
- `input_to_graph_point(self, x: 'float', graph: 'ParametricCurve') -> 'Vect3 | None'`
- `p2c(self, point: 'Vect3') -> 'tuple[float | VectN, ...]'` — Abbreviation for point_to_coords
- `point_to_coords(self, point: 'Vect3 | Vect3Array') -> 'tuple[float | VectN, ...]'`
- `slope_of_tangent(self, x: 'float', graph: 'ParametricCurve', **kwargs) -> 'float'`

</details>

### `Cross(mobject: 'Mobject', stroke_color: 'ManimColor' = '#FC6255', stroke_width: 'float | Sequence[float]' = [0, 6, 0], **kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, mobject: 'Mobject', stroke_color: 'ManimColor' = '#FC6255', stroke_width: 'float | Sequence[float]' = [0, 6, 0], **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `CurvesAsSubmobjects(vmobject: 'VMobject', **kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, vmobject: 'VMobject', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `DashedVMobject(vmobject: 'VMobject', num_dashes: 'int' = 15, positive_space_ratio: 'float' = 0.5, **kwargs)` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, vmobject: 'VMobject', num_dashes: 'int' = 15, positive_space_ratio: 'float' = 0.5, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `DecimalNumber(number: 'float | complex' = 0, color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 0, fill_opacity: 'float' = 1.0, fill_border_width: 'float' = 0.5, num_decimal_places: 'int' = 2, min_total_width: 'Optional[int]' = 0, include_sign: 'bool' = False, group_with_commas: 'bool' = True, digit_buff_per_font_unit: 'float' = 0.001, show_ellipsis: 'bool' = False, unit: 'str | None' = None, include_background_rectangle: 'bool' = False, hide_zero_components_on_complex: 'bool' = True, edge_to_fix: 'Vect3' = array([-1.,  0.,  0.]), font_size: 'float' = 48, text_config: 'dict' = {}, **kwargs)` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (12) · herdados: 318</summary>

- `__init__(self, number: 'float | complex' = 0, color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 0, fill_opacity: 'float' = 1.0, fill_border_width: 'float' = 0.5, num_decimal_places: 'int' = 2, min_total_width: 'Optional[int]' = 0, include_sign: 'bool' = False, group_with_commas: 'bool' = True, digit_buff_per_font_unit: 'float' = 0.001, show_ellipsis: 'bool' = False, unit: 'str | None' = None, include_background_rectangle: 'bool' = False, hide_zero_components_on_complex: 'bool' = True, edge_to_fix: 'Vect3' = array([-1.,  0.,  0.]), font_size: 'float' = 48, text_config: 'dict' = {}, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `char_to_mob(self, char: 'str') -> 'Text'`
- `get_complex_formatter(self, **kwargs) -> 'str'`
- `get_font_size(self) -> 'float'`
- `get_formatter(self, **kwargs) -> 'str'` — Configuration is based first off instance attributes,
- `get_num_string(self, number: 'float | complex') -> 'str'`
- `get_tex(self)`
- `get_value(self) -> 'float | complex'`
- `increment_value(self, delta_t: 'float | complex' = 1) -> 'Self'`
- `interpolate(self, mobject1: 'Mobject', mobject2: 'Mobject', alpha: 'float', path_func: 'Callable[[np.ndarray, np.ndarray, float], np.ndarray]' = <function straight_path at 0x7f6ff3b247c0>) -> 'Self'`
- `set_submobjects_from_number(self, number: 'float | complex') -> 'None'`
- `set_value(self, number: 'float | complex') -> 'Self'`

</details>

### `Difference(subject: 'VMobject', clip: 'VMobject', **kwargs)` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, subject: 'VMobject', clip: 'VMobject', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `DotCloud(points: 'Vect3Array' = array([[0., 0., 0.]]), color: 'ManimColor' = '#888888', opacity: 'float' = 1.0, radius: 'float' = 0.05, glow_factor: 'float' = 0.0, anti_alias_width: 'float' = 2.0, **kwargs)` ← PMobject
> Mathematical Object

<details><summary>métodos próprios (13) · herdados: 235</summary>

- `__init__(self, points: 'Vect3Array' = array([[0., 0., 0.]]), color: 'ManimColor' = '#888888', opacity: 'float' = 1.0, radius: 'float' = 0.05, glow_factor: 'float' = 0.0, anti_alias_width: 'float' = 2.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `compute_bounding_box(self) -> 'Vect3Array'`
- `get_glow_factor(self) -> 'float'`
- `get_radii(self) -> 'np.ndarray'`
- `get_radius(self) -> 'float'`
- `init_uniforms(self) -> 'None'`
- `make_3d(self, reflectiveness: 'float' = 0.5, gloss: 'float' = 0.1, shadow: 'float' = 0.2) -> 'Self'`
- `scale(self, scale_factor: 'float | npt.ArrayLike', scale_radii: 'bool' = True, **kwargs) -> 'Self'` — Default behavior is to scale about the center of the mobject.
- `scale_radii(self, scale_factor: 'float') -> 'Self'`
- `set_glow_factor(self, glow_factor: 'float') -> 'Self'`
- `set_radii(self, radii: 'npt.ArrayLike') -> 'Self'`
- `set_radius(self, radius: 'float') -> 'Self'`
- `to_grid(self, n_rows: 'int', n_cols: 'int', n_layers: 'int' = 1, buff_ratio: 'float | None' = None, h_buff_ratio: 'float' = 1.0, v_buff_ratio: 'float' = 1.0, d_buff_ratio: 'float' = 1.0, height: 'float' = 6) -> 'Self'`

</details>

### `EnableDisableButton(value: 'bool' = True, value_type: 'np.dtype' = dtype('bool'), rect_kwargs: 'dict' = {'width': 0.5, 'height': 0.5, 'fill_opacity': 1.0}, enable_color: 'ManimColor' = '#83C167', disable_color: 'ManimColor' = '#FC6255', **kwargs)` ← ControlMobject
> Not meant to be displayed.  Instead the position encodes some

<details><summary>métodos próprios (5) · herdados: 235</summary>

- `__init__(self, value: 'bool' = True, value_type: 'np.dtype' = dtype('bool'), rect_kwargs: 'dict' = {'width': 0.5, 'height': 0.5, 'fill_opacity': 1.0}, enable_color: 'ManimColor' = '#83C167', disable_color: 'ManimColor' = '#FC6255', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `assert_value(self, value: 'bool') -> 'None'`
- `on_mouse_press(self, mob: 'Mobject', event_data) -> 'bool'`
- `set_value_anim(self, value: 'bool') -> 'None'`
- `toggle_value(self) -> 'None'`

</details>

### `Exclusion(*vmobjects: 'VMobject', **kwargs)` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, *vmobjects: 'VMobject', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `FullScreenFadeRectangle(stroke_width: 'float' = 0.0, fill_color: 'ManimColor' = '#000000', fill_opacity: 'float' = 0.7, **kwargs)` ← FullScreenRectangle
> Creates a rectangle at the center of the screen.

<details><summary>métodos próprios (1) · herdados: 321</summary>

- `__init__(self, stroke_width: 'float' = 0.0, fill_color: 'ManimColor' = '#000000', fill_opacity: 'float' = 0.7, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `FullScreenRectangle(height: 'float' = 8.0, fill_color: 'ManimColor' = '#222222', fill_opacity: 'float' = 1, stroke_width: 'float' = 0, **kwargs)` ← ScreenRectangle
> Creates a rectangle at the center of the screen.

<details><summary>métodos próprios (1) · herdados: 321</summary>

- `__init__(self, height: 'float' = 8.0, fill_color: 'ManimColor' = '#222222', fill_opacity: 'float' = 1, stroke_width: 'float' = 0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `FunctionGraph(function: 'Callable[[float], float]', x_range: 'Tuple[float, float, float]' = (-8, 8, 0.25), color: 'ManimColor' = '#FFFF00', **kwargs)` ← ParametricCurve
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 323</summary>

- `__init__(self, function: 'Callable[[float], float]', x_range: 'Tuple[float, float, float]' = (-8, 8, 0.25), color: 'ManimColor' = '#FFFF00', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `GlowDot(center: 'Vect3' = array([0., 0., 0.]), **kwargs)` ← GlowDots
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 247</summary>

- `__init__(self, center: 'Vect3' = array([0., 0., 0.]), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `GlowDots(points: 'Vect3Array' = array([[0., 0., 0.]]), color: 'ManimColor' = '#FFFF00', radius: 'float' = 0.2, glow_factor: 'float' = 2.0, **kwargs)` ← DotCloud
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 247</summary>

- `__init__(self, points: 'Vect3Array' = array([[0., 0., 0.]]), color: 'ManimColor' = '#FFFF00', radius: 'float' = 0.2, glow_factor: 'float' = 2.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Group(*mobjects: 'SubmobjectType | Iterable[SubmobjectType]', **kwargs)` ← Mobject, Generic
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 232</summary>

- `__init__(self, *mobjects: 'SubmobjectType | Iterable[SubmobjectType]', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ImageMobject(filename: 'str', height: 'float' = 4.0, **kwargs)` ← Mobject
> Mathematical Object

<details><summary>métodos próprios (6) · herdados: 228</summary>

- `__init__(self, filename: 'str', height: 'float' = 4.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `init_data(self) -> 'None'`
- `init_points(self) -> 'None'`
- `point_to_rgb(self, point: 'Vect3') -> 'Vect3'`
- `set_color(self, color, opacity=None, recurse=None)`
- `set_opacity(self, opacity: 'float', recurse: 'bool' = True)`

</details>

### `ImplicitFunction(func: 'Callable[[float, float], float]', x_range: 'Tuple[float, float]' = (-7.111111111111111, 7.111111111111111), y_range: 'Tuple[float, float]' = (-4.0, 4.0), min_depth: 'int' = 5, max_quads: 'int' = 1500, use_smoothing: 'bool' = False, **kwargs)` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, func: 'Callable[[float, float], float]', x_range: 'Tuple[float, float]' = (-7.111111111111111, 7.111111111111111), y_range: 'Tuple[float, float]' = (-4.0, 4.0), min_depth: 'int' = 5, max_quads: 'int' = 1500, use_smoothing: 'bool' = False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Integer(number: 'int' = 0, num_decimal_places: 'int' = 0, **kwargs)` ← DecimalNumber
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 328</summary>

- `__init__(self, number: 'int' = 0, num_decimal_places: 'int' = 0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_value(self) -> 'int'`

</details>

### `Intersection(*vmobjects: 'VMobject', **kwargs)` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, *vmobjects: 'VMobject', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `JuliaFractal(plane: 'CoordinateSystem', parameter: 'complex' = 0j, n_steps: 'int' = 100, **kwargs)` ← MandelbrotFractal
> The Julia set of z -> z^2 + c for one fixed c: which starting points stay bounded, where

<details><summary>métodos próprios (2) · herdados: 238</summary>

- `__init__(self, plane: 'CoordinateSystem', parameter: 'complex' = 0j, n_steps: 'int' = 100, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `set_c(self, c: 'complex') -> 'Self'`

</details>

### `LinearNumberSlider(value: 'float' = 0, value_type: 'type' = <class 'numpy.float64'>, min_value: 'float' = -10.0, max_value: 'float' = 10.0, step: 'float' = 1.0, rounded_rect_kwargs: 'dict' = {'height': 0.075, 'width': 2, 'corner_radius': 0.0375}, circle_kwargs: 'dict' = {'radius': 0.1, 'stroke_color': '#DDDDDD', 'fill_color': '#DDDDDD', 'fill_opacity': 1.0}, **kwargs)` ← ControlMobject
> Not meant to be displayed.  Instead the position encodes some

<details><summary>métodos próprios (5) · herdados: 235</summary>

- `__init__(self, value: 'float' = 0, value_type: 'type' = <class 'numpy.float64'>, min_value: 'float' = -10.0, max_value: 'float' = 10.0, step: 'float' = 1.0, rounded_rect_kwargs: 'dict' = {'height': 0.075, 'width': 2, 'corner_radius': 0.0375}, circle_kwargs: 'dict' = {'radius': 0.1, 'stroke_color': '#DDDDDD', 'fill_color': '#DDDDDD', 'fill_opacity': 1.0}, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `assert_value(self, value: 'float') -> 'None'`
- `get_value_from_point(self, point: 'np.ndarray') -> 'float'`
- `set_value_anim(self, value: 'float') -> 'None'`
- `slider_on_mouse_drag(self, mob, event_data: 'dict[str, np.ndarray]') -> 'bool'`

</details>

### `MandelbrotFractal(plane: 'CoordinateSystem', colors: 'Sequence[ManimColor]' = ['#00065c', '#061e7e', '#0c37a0', '#205abc', '#4287d3', '#D9EDE4', '#F0F9E4', '#BA9F6A', '#573706'], n_steps: 'int' = 300, parameter: 'complex' = 0j, opacity: 'float' = 1.0, mandelbrot: 'bool' = True, **kwargs)` ← PlaneFractal
> The Mandelbrot set: which starting points c leave the iteration z -> z^2 + c bounded,

<details><summary>métodos próprios (4) · herdados: 235</summary>

- `__init__(self, plane: 'CoordinateSystem', colors: 'Sequence[ManimColor]' = ['#00065c', '#061e7e', '#0c37a0', '#205abc', '#4287d3', '#D9EDE4', '#F0F9E4', '#BA9F6A', '#573706'], n_steps: 'int' = 300, parameter: 'complex' = 0j, opacity: 'float' = 1.0, mandelbrot: 'bool' = True, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `set_colors(self, colors: 'Sequence[ManimColor]') -> 'Self'`
- `set_opacity(self, opacity: 'float', recurse: 'bool' = True) -> 'Self'`
- `set_parameter(self, c: 'complex') -> 'Self'` — The c held fixed while the pixel is the orbit's start, so only a Julia set uses it

</details>

### `MetaNewtonFractal(plane: 'CoordinateSystem', fixed_roots: 'Sequence[complex]' = (-1, 1), n_steps: 'int' = 300, black_for_cycles: 'bool' = True, **kwargs)` ← NewtonFractal
> Which cubics Newton's method finds a root of at all: two of the three roots are held

<details><summary>métodos próprios (2) · herdados: 242</summary>

- `__init__(self, plane: 'CoordinateSystem', fixed_roots: 'Sequence[complex]' = (-1, 1), n_steps: 'int' = 300, black_for_cycles: 'bool' = True, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `set_fixed_roots(self, roots: 'Sequence[complex]') -> 'Self'`

</details>

### `Mobject(color: 'ManimColor' = '#FFFFFF', opacity: 'float' = 1.0, shading: 'Tuple[float, float, float]' = (0.0, 0.0, 0.0), texture_paths: 'dict[str, str] | None' = None, is_fixed_in_frame: 'bool' = False, depth_test: 'bool' = False, z_index: 'int' = 0)`
> Mathematical Object

<details><summary>métodos próprios (233) · herdados: 0</summary>

- `__init__(self, color: 'ManimColor' = '#FFFFFF', opacity: 'float' = 1.0, shading: 'Tuple[float, float, float]' = (0.0, 0.0, 0.0), texture_paths: 'dict[str, str] | None' = None, is_fixed_in_frame: 'bool' = False, depth_test: 'bool' = False, z_index: 'int' = 0)` — Initialize self.  See help(type(self)) for accurate signature.
- `add(self, *mobjects: 'Mobject') -> 'Self'`
- `add_background_rectangle(self, color: 'ManimColor | None' = None, opacity: 'float' = 1.0, **kwargs) -> 'Self'`
- `add_background_rectangle_to_family_members_with_points(self, **kwargs) -> 'Self'`
- `add_background_rectangle_to_submobjects(self, **kwargs) -> 'Self'`
- `add_event_listner(self, event_type: 'EventType', event_callback: 'Callable[[Mobject, dict[str]]]')`
- `add_key_press_listner(self, callback)`
- `add_key_release_listner(self, callback)`
- `add_mouse_drag_listner(self, callback)`
- `add_mouse_motion_listner(self, callback)`
- `add_mouse_press_listner(self, callback)`
- `add_mouse_release_listner(self, callback)`
- `add_mouse_scroll_listner(self, callback)`
- `add_n_more_submobjects(self, n: 'int') -> 'Self'`
- `add_to_back(self, *mobjects: 'Mobject') -> 'Self'`
- `add_updater(self, update_func: 'UpdateFunction', call: 'bool' = True) -> 'Self'`
- `align_data(self, mobject: 'Mobject') -> 'Self'`
- `align_data_and_family(self, mobject: 'Mobject') -> 'Self'`
- `align_family(self, mobject: 'Mobject') -> 'Self'`
- `align_on_border(self, direction: 'Vect3', buff: 'float' = 0.5) -> 'Self'` — Direction just needs to be a vector pointing towards side or
- `align_points(self, mobject: 'Mobject') -> 'Self'`
- `align_to(self, mobject_or_point: 'Mobject | Vect3', direction: 'Vect3' = array([0., 0., 0.])) -> 'Self'` — Examples:
- `append_points(self, new_points: 'Vect3Array') -> 'Self'`
- `apply_complex_function(self, function: 'Callable[[complex], complex]', **kwargs) -> 'Self'`
- `apply_depth_test(self, recurse: 'bool' = True) -> 'Self'`
- `apply_function(self, function: 'Callable[[np.ndarray], np.ndarray]', **kwargs) -> 'Self'`
- `apply_function_to_position(self, function: 'Callable[[np.ndarray], np.ndarray]') -> 'Self'`
- `apply_function_to_submobject_positions(self, function: 'Callable[[np.ndarray], np.ndarray]') -> 'Self'`
- `apply_matrix(self, matrix: 'npt.ArrayLike', **kwargs) -> 'Self'`
- `apply_points_function(self, func: 'Callable[[np.ndarray], np.ndarray]', about_point: 'Vect3 | None' = None, about_edge: 'Vect3' = array([0., 0., 0.]), works_on_bounding_box: 'bool' = False) -> 'Self'`
- `are_points_touching(self, points: 'Vect3Array', buff: 'float' = 0) -> 'np.ndarray'`
- `arrange(self, direction: 'Vect3' = array([1., 0., 0.]), center: 'bool' = True, **kwargs) -> 'Self'`
- `arrange_in_grid(self, n_rows: 'int | None' = None, n_cols: 'int | None' = None, buff: 'float | None' = None, h_buff: 'float | None' = None, v_buff: 'float | None' = None, buff_ratio: 'float | None' = None, h_buff_ratio: 'float' = 0.5, v_buff_ratio: 'float' = 0.5, aligned_edge: 'Vect3' = array([0., 0., 0.]), fill_rows_first: 'bool' = True) -> 'Self'`
- `arrange_to_fit_depth(self, depth: 'float', about_edge=array([0., 0., 0.])) -> 'Self'`
- `arrange_to_fit_dim(self, length: 'float', dim: 'int', about_edge=array([0., 0., 0.])) -> 'Self'`
- `arrange_to_fit_height(self, height: 'float', about_edge=array([0., 0., 0.])) -> 'Self'`
- `arrange_to_fit_width(self, width: 'float', about_edge=array([0., 0., 0.])) -> 'Self'`
- `become(self, mobject: 'Mobject', match_updaters=False) -> 'Self'` — Edit all data and submobjects to be idential
- `center(self) -> 'Self'`
- `clear(self) -> 'Self'`
- `clear_event_listners(self, recurse: 'bool' = True)`
- `clear_points(self) -> 'Self'`
- `clear_updaters(self, recurse: 'bool' = True) -> 'Self'`
- `clip_to_box(self, box: 'Mobject', recurse=True) -> 'Self'`
- `compute_bounding_box(self) -> 'Vect3Array'`
- `copy(self, deep: 'bool' = False) -> 'Self'`
- `deactivate_clip_plane(self, recurse=True) -> 'Self'`
- `deactivate_depth_test(self, recurse: 'bool' = True) -> 'Self'`
- `deepcopy(self) -> 'Self'`
- `deserialize(self, data: 'bytes') -> 'Self'`
- `digest_mobject_attrs(self) -> 'Self'` — Ensures all attributes which are mobjects are included
- `fade(self, darkness: 'float' = 0.5, recurse: 'bool' = True) -> 'Self'`
- `family_members_with_points(self) -> 'list[Mobject]'`
- `fix_in_frame(self, recurse: 'bool' = True) -> 'Self'`
- `flip(self, axis: 'Vect3' = array([0., 1., 0.]), **kwargs) -> 'Self'`
- `generate_target(self, use_deepcopy: 'bool' = False) -> 'Self'`
- `get_all_corners(self)`
- `get_all_points(self) -> 'Vect3Array'`
- `get_ancestors(self, extended: 'bool' = False) -> 'list[Mobject]'` — Returns parents, grandparents, etc.
- `get_bottom(self) -> 'Vect3'`
- `get_boundary_point(self, direction: 'Vect3') -> 'Vect3'`
- `get_bounding_box(self) -> 'Vect3Array'`
- `get_bounding_box_point(self, direction: 'Vect3') -> 'Vect3'`
- `get_center(self) -> 'Vect3'`
- `get_center_of_mass(self) -> 'Vect3'`
- `get_color(self) -> 'str'`
- `get_continuous_bounding_box_point(self, direction: 'Vect3') -> 'Vect3'`
- `get_coord(self, dim: 'int', direction: 'Vect3' = array([0., 0., 0.])) -> 'float'` — Meant to generalize get_x, get_y, get_z
- `get_corner(self, direction: 'Vect3') -> 'Vect3'`
- `get_depth(self) -> 'float'`
- `get_edge_center(self, direction: 'Vect3') -> 'Vect3'`
- `get_end(self) -> 'Vect3'`
- `get_event_listners(self)`
- `get_family(self, recurse: 'bool' = True) -> 'list[Mobject]'`
- `get_family_event_listners(self)`
- `get_gloss(self) -> 'float'`
- `get_grid(self, n_rows: 'int', n_cols: 'int', height: 'float | None' = None, width: 'float | None' = None, group_by_rows: 'bool' = False, group_by_cols: 'bool' = False, **kwargs) -> 'Self'` — Returns a new mobject containing multiple copies of this one
- `get_group_class(self)`
- `get_has_event_listner(self)`
- `get_height(self) -> 'float'`
- `get_left(self) -> 'Vect3'`
- `get_nadir(self) -> 'Vect3'`
- `get_num_points(self) -> 'int'`
- `get_opacities(self) -> 'float'`
- `get_opacity(self) -> 'float'`
- `get_pieces(self, n_pieces: 'int') -> 'Group'`
- `get_points(self) -> 'Vect3Array'`
- `get_reflectiveness(self) -> 'float'`
- `get_right(self) -> 'Vect3'`
- `get_shading(self) -> 'np.ndarray'`
- `get_shadow(self) -> 'float'`
- `get_shape(self) -> 'Tuple[float]'`
- `get_start(self) -> 'Vect3'`
- `get_start_and_end(self) -> 'tuple[Vect3, Vect3]'`
- `get_top(self) -> 'Vect3'`
- `get_uniforms(self)`
- `get_updaters(self) -> 'list[UpdateFunction]'`
- `get_width(self) -> 'float'`
- `get_x(self, direction=array([0., 0., 0.])) -> 'float'`
- `get_y(self, direction=array([0., 0., 0.])) -> 'float'`
- `get_z(self, direction=array([0., 0., 0.])) -> 'float'`
- `get_zenith(self) -> 'Vect3'`
- `has_points(self) -> 'bool'`
- `has_same_shape_as(self, mobject: 'Mobject') -> 'bool'`
- `has_time_based_updaters(self) -> 'bool'`
- `has_updaters(self) -> 'bool'`
- `init_colors(self)`
- `init_data(self, length: 'int' = 0)`
- `init_event_listners(self)`
- `init_points(self)`
- `init_uniforms(self)`
- `init_updaters(self)`
- `insert_submobject(self, index: 'int', new_submob: 'Mobject') -> 'Self'`
- `insert_updater(self, update_func: 'UpdateFunction', index=0)`
- `interpolate(self, mobject1: 'Mobject', mobject2: 'Mobject', alpha: 'float', path_func: 'Callable[[np.ndarray, np.ndarray, float], np.ndarray]' = <function straight_path at 0x7f6ff3b247c0>) -> 'Self'`
- `invisible_copy(self) -> 'Self'`
- `is_aligned_with(self, mobject: 'Mobject') -> 'bool'`
- `is_changing(self) -> 'bool'`
- `is_fixed_in_frame(self) -> 'bool'`
- `is_off_screen(self) -> 'bool'`
- `is_point_touching(self, point: 'Vect3', buff: 'float' = 0) -> 'bool'`
- `is_touching(self, mobject: 'Mobject', buff: 'float' = 0.01) -> 'bool'`
- `length_over_dim(self, dim: 'int') -> 'float'`
- `looks_identical(self, mobject: 'Mobject') -> 'bool'`
- `match_color(self, mobject: 'Mobject') -> 'Self'`
- `match_coord(self, mobject_or_point: 'Mobject | Vect3', dim: 'int', direction: 'Vect3' = array([0., 0., 0.])) -> 'Self'`
- `match_depth(self, mobject: 'Mobject', **kwargs) -> 'Self'`
- `match_dim_size(self, mobject: 'Mobject', dim: 'int', **kwargs) -> 'Self'`
- `match_height(self, mobject: 'Mobject', **kwargs) -> 'Self'`
- `match_points(self, mobject: 'Mobject') -> 'Self'`
- `match_style(self, mobject: 'Mobject') -> 'Self'`
- `match_updaters(self, mobject: 'Mobject') -> 'Self'`
- `match_width(self, mobject: 'Mobject', **kwargs) -> 'Self'`
- `match_x(self, mobject_or_point: 'Mobject | Vect3', direction: 'Vect3' = array([0., 0., 0.])) -> 'Self'`
- `match_y(self, mobject_or_point: 'Mobject | Vect3', direction: 'Vect3' = array([0., 0., 0.])) -> 'Self'`
- `match_z(self, mobject_or_point: 'Mobject | Vect3', direction: 'Vect3' = array([0., 0., 0.])) -> 'Self'`
- `move_to(self, point_or_mobject: 'Mobject | Vect3', aligned_edge: 'Vect3' = array([0., 0., 0.]), coor_mask: 'Vect3' = array([1, 1, 1])) -> 'Self'`
- `next_to(self, mobject_or_point: 'Mobject | Vect3', direction: 'Vect3' = array([1., 0., 0.]), buff: 'float' = 0.25, aligned_edge: 'Vect3' = array([0., 0., 0.]), submobject_to_align: 'Mobject | None' = None, index_of_submobject_to_align: 'int | slice | None' = None, coor_mask: 'Vect3' = array([1, 1, 1])) -> 'Self'`
- `note_changed_family(self, only_changed_order=False) -> 'Self'`
- `pfp(self, alpha)` — Abbreviation for point_from_proportion
- `point_from_proportion(self, alpha: 'float') -> 'Vect3'`
- `pointwise_become_partial(self, mobject, a, b) -> 'Self'` — Set points in such a way as to become only
- `prepare_interpolation(self, mobject1: 'Mobject', mobject2: 'Mobject') -> 'Self'` — Tells every submobject's arrays what a blend between the two ends of an animation
- `push_self_into_submobjects(self) -> 'Self'`
- `put_end_on(self, point: 'Vect3') -> 'Self'`
- `put_start_and_end_on(self, start: 'Vect3', end: 'Vect3') -> 'Self'`
- `put_start_on(self, point: 'Vect3') -> 'Self'`
- `refresh_bounding_box(self, recurse_down: 'bool' = False, recurse_up: 'bool' = True) -> 'Self'`
- `refresh_has_updater_status(self) -> 'Self'`
- `remove(self, *to_remove: 'Mobject', reassemble: 'bool' = True, recurse: 'bool' = True) -> 'Self'`
- `remove_event_listner(self, event_type: 'EventType', event_callback: 'Callable[[Mobject, dict[str]]]')`
- `remove_key_press_listner(self, callback)`
- `remove_key_release_listner(self, callback)`
- `remove_mouse_drag_listner(self, callback)`
- `remove_mouse_motion_listner(self, callback)`
- `remove_mouse_press_listner(self, callback)`
- `remove_mouse_release_listner(self, callback)`
- `remove_mouse_scroll_listner(self, callback)`
- `remove_updater(self, update_func: 'UpdateFunction') -> 'Self'`
- `replace(self, mobject: 'Mobject', dim_to_match: 'int' = 0, stretch: 'bool' = False) -> 'Self'`
- `replace_shader_code(self, old: 'str', new: 'str') -> 'Self'`
- `replace_submobject(self, index: 'int', new_submob: 'Mobject') -> 'Self'`
- `replicate(self, n: 'int') -> 'Self'`
- `rescale_to_fit(self, length: 'float', dim: 'int', stretch: 'bool' = False, **kwargs) -> 'Self'`
- `resize_points(self, new_length: 'int', resize_func: 'Callable[[np.ndarray, int], np.ndarray]' = <function resize_array at 0x7f7058a8fec0>) -> 'Self'`
- `restore(self) -> 'Self'`
- `resume_updating(self, recurse: 'bool' = True, call_updater: 'bool' = True) -> 'Self'`
- `reverse_points(self) -> 'Self'`
- `reverse_submobjects(self) -> 'Self'`
- `rotate(self, angle: 'float', axis: 'Vect3' = array([0., 0., 1.]), about_point: 'Vect3 | None' = None, **kwargs) -> 'Self'`
- `rotate_about_origin(self, angle: 'float', axis: 'Vect3' = array([0., 0., 1.])) -> 'Self'`
- `save_state(self, use_deepcopy: 'bool' = False) -> 'Self'`
- `scale(self, scale_factor: 'float | npt.ArrayLike', min_scale_factor: 'float' = 1e-08, about_point: 'Vect3 | None' = None, about_edge: 'Vect3' = array([0., 0., 0.])) -> 'Self'` — Default behavior is to scale about the center of the mobject.
- `serialize(self) -> 'bytes'`
- `set_animating_status(self, is_animating: 'bool', recurse: 'bool' = True) -> 'Self'`
- `set_clip_plane(self, vect: 'Vect3', threshold: 'float', recurse=True) -> 'Self'`
- `set_clip_planes(self, *vect_threshold_pairs: 'Iterable[Tuple[Vect3, float]]', recurse=True) -> 'Self'`
- `set_color(self, color: 'ManimColor | Iterable[ManimColor] | None', opacity: 'float | Iterable[float] | None' = None, recurse: 'bool' = True) -> 'Self'`
- `set_color_by_code(self, wgsl_code: 'str') -> 'Self'` — Takes a snippet of code and inserts it into a context which has the following
- `set_color_by_gradient(self, *colors: 'ManimColor') -> 'Self'`
- `set_color_by_rgb_func(self, func: 'Callable[[Vect3Array], Vect3Array]', opacity: 'float' = 1, recurse: 'bool' = True) -> 'Self'` — Func should accept an (N, 3) array and return an (N, 3) array of RGB values in [0,1]
- `set_color_by_rgba_func(self, func: 'Callable[[Vect3Array], Vect4Array]', recurse: 'bool' = True) -> 'Self'` — Func should accept an (N, 3) array and return an (N, 4) array of RGB values in [0,1]
- `set_color_by_xyz_func(self, wgsl_snippet: 'str', min_value: 'float' = -5.0, max_value: 'float' = 5.0, colormap: 'str' = 'viridis') -> 'Self'` — Pass in a wgsl expression in terms of x, y and z which returns
- `set_coord(self, value: 'float', dim: 'int', direction: 'Vect3' = array([0., 0., 0.])) -> 'Self'`
- `set_data(self, data: 'np.ndarray | StructuredArray') -> 'Self'`
- `set_depth(self, depth: 'float', stretch: 'bool' = False, **kwargs) -> 'Self'`
- `set_gloss(self, gloss: 'float', recurse: 'bool' = True) -> 'Self'`
- `set_height(self, height: 'float', stretch: 'bool' = False, **kwargs) -> 'Self'`
- `set_max_depth(self, max_depth: 'float', **kwargs) -> 'Self'`
- `set_max_height(self, max_height: 'float', **kwargs) -> 'Self'`
- `set_max_width(self, max_width: 'float', **kwargs) -> 'Self'`
- `set_min_depth(self, min_depth: 'float', **kwargs) -> 'Self'`
- `set_min_height(self, min_height: 'float', **kwargs) -> 'Self'`
- `set_min_width(self, min_width: 'float', **kwargs) -> 'Self'`
- `set_opacity(self, opacity: 'float | Iterable[float] | None', recurse: 'bool' = True) -> 'Self'`
- `set_points(self, points: 'Vect3Array | list[Vect3]') -> 'Self'`
- `set_reflectiveness(self, reflectiveness: 'float', recurse: 'bool' = True) -> 'Self'`
- `set_rgba_array(self, rgba_array: 'npt.ArrayLike', name: 'str' = 'rgba', recurse: 'bool' = False) -> 'Self'`
- `set_rgba_array_by_color(self, color: 'ManimColor | Iterable[ManimColor] | None' = None, opacity: 'float | Iterable[float] | None' = None, name: 'str' = 'rgba', recurse: 'bool' = True) -> 'Self'`
- `set_shading(self, reflectiveness: 'float | None' = None, gloss: 'float | None' = None, shadow: 'float | None' = None, recurse: 'bool' = True) -> 'Self'` — Larger reflectiveness makes things brighter when facing the light
- `set_shadow(self, shadow: 'float', recurse: 'bool' = True) -> 'Self'`
- `set_shape(self, width: 'Optional[float]' = None, height: 'Optional[float]' = None, depth: 'Optional[float]' = None, **kwargs) -> 'Self'`
- `set_submobject_colors_by_gradient(self, *colors: 'ManimColor', interp_by_hsl=False) -> 'Self'`
- `set_submobjects(self, submobject_list: 'list[Mobject]') -> 'Self'`
- `set_uniform(self, recurse: 'bool' = True, **new_uniforms) -> 'Self'`
- `set_uniforms(self, uniforms: 'Uniforms') -> 'Self'`
- `set_width(self, width: 'float', stretch: 'bool' = False, **kwargs) -> 'Self'`
- `set_x(self, x: 'float', direction: 'Vect3' = array([0., 0., 0.])) -> 'Self'`
- `set_y(self, y: 'float', direction: 'Vect3' = array([0., 0., 0.])) -> 'Self'`
- `set_z(self, z: 'float', direction: 'Vect3' = array([0., 0., 0.])) -> 'Self'`
- `set_z_index(self, z_index: 'int', recurse=True) -> 'Self'`
- `shift(self, vector: 'Vect3') -> 'Self'`
- `shift_onto_screen(self, **kwargs) -> 'Self'`
- `shuffle(self, recurse: 'bool' = False) -> 'Self'`
- `sort(self, point_to_num_func: 'Callable[[np.ndarray], float]' = <function Mobject.<lambda> at 0x7f6ff3b26a20>, submob_func: 'Callable[[Mobject]] | None' = None) -> 'Self'`
- `space_out_submobjects(self, factor: 'float' = 1.5, **kwargs) -> 'Self'`
- `split(self) -> 'list[Self]'`
- `stash_mobject_pointers(func: 'Callable[..., T]') -> 'Callable[..., T]'`
- `stretch(self, factor: 'float', dim: 'int', **kwargs) -> 'Self'`
- `stretch_about_point(self, factor: 'float', dim: 'int', point: 'Vect3') -> 'Self'`
- `stretch_in_place(self, factor: 'float', dim: 'int') -> 'Self'`
- `stretch_to_fit_depth(self, depth: 'float', **kwargs) -> 'Self'`
- `stretch_to_fit_height(self, height: 'float', **kwargs) -> 'Self'`
- `stretch_to_fit_width(self, width: 'float', **kwargs) -> 'Self'`
- `surround(self, mobject: 'Mobject', dim_to_match: 'int' = 0, stretch: 'bool' = False, buff: 'float' = 0.25) -> 'Self'`
- `suspend_updating(self, recurse: 'bool' = True) -> 'Self'`
- `throw_error_if_no_points(self)`
- `to_corner(self, corner: 'Vect3' = array([-1., -1.,  0.]), buff: 'float' = 0.5) -> 'Self'`
- `to_edge(self, edge: 'Vect3' = array([-1.,  0.,  0.]), buff: 'float' = 0.5) -> 'Self'`
- `turn_off_interpolation_skip(self) -> 'Self'`
- `unfix_from_frame(self, recurse: 'bool' = True) -> 'Self'`
- `update(self, dt: 'float' = 0, recurse: 'bool' = True, frame_rate: 'float | None' = None) -> 'Self'` — Calls all updaters in the family. Passing in a frame_rate accounts for
- `wag(self, direction: 'Vect3' = array([1., 0., 0.]), axis: 'Vect3' = array([ 0., -1.,  0.]), wag_factor: 'float' = 1.0) -> 'Self'`

</details>

### `MotionMobject(mobject: 'Mobject', **kwargs)` ← Mobject
> You could hold and drag this object to any position

<details><summary>métodos próprios (2) · herdados: 232</summary>

- `__init__(self, mobject: 'Mobject', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `mob_on_mouse_drag(self, mob: 'Mobject', event_data: 'dict[str, np.ndarray]') -> 'bool'`

</details>

### `NewtonFractal(plane: 'CoordinateSystem', coefs: 'Sequence[complex]' = (-1.0, 0.0, 0.0, 1.0), roots: 'Sequence[complex] | None' = None, colors: 'Sequence[ManimColor]' = ['#440154', '#3b528b', '#21908c', '#5dc963', '#29abca'], n_steps: 'int' = 30, julia_highlight: 'float' = 0.0, saturation_factor: 'float' = 0.0, opacity: 'float' = 1.0, black_for_cycles: 'bool' = False, is_parameter_space: 'bool' = False, **kwargs)` ← PlaneFractal
> Newton's method run from every pixel of a plane, each colored by which root it converged

<details><summary>métodos próprios (8) · herdados: 235</summary>

- `__init__(self, plane: 'CoordinateSystem', coefs: 'Sequence[complex]' = (-1.0, 0.0, 0.0, 1.0), roots: 'Sequence[complex] | None' = None, colors: 'Sequence[ManimColor]' = ['#440154', '#3b528b', '#21908c', '#5dc963', '#29abca'], n_steps: 'int' = 30, julia_highlight: 'float' = 0.0, saturation_factor: 'float' = 0.0, opacity: 'float' = 1.0, black_for_cycles: 'bool' = False, is_parameter_space: 'bool' = False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `set_coefs(self, coefs: 'Sequence[complex]', reset_roots: 'bool' = True) -> 'Self'`
- `set_colors(self, colors: 'Sequence[ManimColor]') -> 'Self'`
- `set_julia_highlight(self, radius: 'float') -> 'Self'` — How far around each pixel to look for the basin boundary, which above zero shows
- `set_opacities(self, *opacities: 'float') -> 'Self'`
- `set_opacity(self, opacity: 'float', recurse: 'bool' = True) -> 'Self'`
- `set_roots(self, roots: 'Sequence[complex]', reset_coefs: 'bool' = True) -> 'Self'`
- `set_saturation_factor(self, saturation_factor: 'float') -> 'Self'` — How much to brighten what took longer to settle, showing a basin's own structure

</details>

### `NumberLine(x_range: 'RangeSpecifier' = (-8, 8, 1), color: 'ManimColor' = '#BBBBBB', stroke_width: 'float' = 2.0, unit_size: 'float' = 1.0, width: 'Optional[float]' = None, include_ticks: 'bool' = True, tick_size: 'float' = 0.1, longer_tick_multiple: 'float' = 1.5, tick_offset: 'float' = 0.0, big_tick_spacing: 'Optional[float]' = None, big_tick_numbers: 'list[float]' = [], include_numbers: 'bool' = False, line_to_number_direction: 'Vect3' = array([ 0., -1.,  0.]), line_to_number_buff: 'float' = 0.25, include_tip: 'bool' = False, tip_config: 'dict' = {'width': 0.25, 'length': 0.25}, decimal_number_config: 'dict' = {'num_decimal_places': 0, 'font_size': 36}, numbers_to_exclude: 'list | None' = None, **kwargs)` ← Line
> Creates a line joining the points "start" and "end".

<details><summary>métodos próprios (12) · herdados: 347</summary>

- `__init__(self, x_range: 'RangeSpecifier' = (-8, 8, 1), color: 'ManimColor' = '#BBBBBB', stroke_width: 'float' = 2.0, unit_size: 'float' = 1.0, width: 'Optional[float]' = None, include_ticks: 'bool' = True, tick_size: 'float' = 0.1, longer_tick_multiple: 'float' = 1.5, tick_offset: 'float' = 0.0, big_tick_spacing: 'Optional[float]' = None, big_tick_numbers: 'list[float]' = [], include_numbers: 'bool' = False, line_to_number_direction: 'Vect3' = array([ 0., -1.,  0.]), line_to_number_buff: 'float' = 0.25, include_tip: 'bool' = False, tip_config: 'dict' = {'width': 0.25, 'length': 0.25}, decimal_number_config: 'dict' = {'num_decimal_places': 0, 'font_size': 36}, numbers_to_exclude: 'list | None' = None, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_numbers(self, x_values: 'Iterable[float] | None' = None, excluding: 'Iterable[float] | None' = None, font_size: 'int' = 24, **kwargs) -> 'VGroup'`
- `add_ticks(self) -> 'None'`
- `get_number_mobject(self, x: 'float', direction: 'Vect3 | None' = None, buff: 'float | None' = None, unit: 'float' = 1.0, unit_tex: 'str' = '', **number_config) -> 'DecimalNumber'`
- `get_tick(self, x: 'float', size: 'float | None' = None) -> 'Line'`
- `get_tick_marks(self) -> 'VGroup'`
- `get_tick_range(self) -> 'np.ndarray'`
- `get_unit_size(self) -> 'float'`
- `n2p(self, number: 'float | VectN') -> 'Vect3 | Vect3Array'` — Abbreviation for number_to_point
- `number_to_point(self, number: 'float | VectN') -> 'Vect3 | Vect3Array'`
- `p2n(self, point: 'Vect3 | Vect3Array') -> 'float | VectN'` — Abbreviation for point_to_number
- `point_to_number(self, point: 'Vect3 | Vect3Array') -> 'float | VectN'`

</details>

### `NumberPlane(x_range: 'RangeSpecifier' = (-8.0, 8.0, 1.0), y_range: 'RangeSpecifier' = (-4.0, 4.0, 1.0), background_line_style: 'dict' = {'stroke_color': '#29ABCA', 'stroke_width': 2, 'stroke_opacity': 1}, faded_line_style: 'dict' = {'stroke_width': 1, 'stroke_opacity': 0.25}, faded_line_ratio: 'int' = 4, make_smooth_after_applying_functions: 'bool' = True, **kwargs)` ← Axes
> Mathematical Object

<details><summary>métodos próprios (9) · herdados: 352</summary>

- `__init__(self, x_range: 'RangeSpecifier' = (-8.0, 8.0, 1.0), y_range: 'RangeSpecifier' = (-4.0, 4.0, 1.0), background_line_style: 'dict' = {'stroke_color': '#29ABCA', 'stroke_width': 2, 'stroke_opacity': 1}, faded_line_style: 'dict' = {'stroke_width': 1, 'stroke_opacity': 0.25}, faded_line_ratio: 'int' = 4, make_smooth_after_applying_functions: 'bool' = True, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_axes(self) -> 'VGroup'`
- `get_lines(self) -> 'tuple[VGroup, VGroup]'`
- `get_lines_parallel_to_axis(self, axis1: 'NumberLine', axis2: 'NumberLine') -> 'tuple[VGroup, VGroup]'`
- `get_vector(self, coords: 'Iterable[float]', **kwargs) -> 'Arrow'`
- `get_x_unit_size(self) -> 'float'`
- `get_y_unit_size(self) -> 'list'`
- `init_background_lines(self) -> 'None'`
- `prepare_for_nonlinear_transform(self, num_inserted_curves: 'int' = 50) -> 'Self'`

</details>

### `PGroup(*pmobs: 'PMobject', **kwargs)` ← PMobject
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 238</summary>

- `__init__(self, *pmobs: 'PMobject', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `PMobject(color: 'ManimColor' = '#FFFFFF', opacity: 'float' = 1.0, shading: 'Tuple[float, float, float]' = (0.0, 0.0, 0.0), texture_paths: 'dict[str, str] | None' = None, is_fixed_in_frame: 'bool' = False, depth_test: 'bool' = False, z_index: 'int' = 0)` ← Mobject
> Mathematical Object

<details><summary>métodos próprios (10) · herdados: 229</summary>

- `add_point(self, point: 'Vect3', rgba=None, color=None, opacity=None) -> 'Self'`
- `add_points(self, points: 'Vect3Array', rgbas: 'Vect4Array | None' = None, color: 'ManimColor | None' = None, opacity: 'float | None' = None) -> 'Self'` — points must be a Nx3 numpy array, as must rgbas if it is not None
- `filter_out(self, condition: 'Callable[[np.ndarray], bool]') -> 'Self'`
- `ingest_submobjects(self) -> 'Self'`
- `match_colors(self, pmobject: 'PMobject') -> 'Self'`
- `point_from_proportion(self, alpha: 'float') -> 'np.ndarray'`
- `pointwise_become_partial(self, pmobject: 'PMobject', a: 'float', b: 'float') -> 'Self'` — Set points in such a way as to become only
- `set_color_by_gradient(self, *colors: 'ManimColor') -> 'Self'`
- `set_points(self, points: 'Vect3Array')`
- `sort_points(self, function: 'Callable[[Vect3], None]' = <function PMobject.<lambda> at 0x7f6ff1ddd300>) -> 'Self'` — function is any map from R^3 to R

</details>

### `ParametricCurve(t_func: 'Callable[[float], Sequence[float] | Vect3]', t_range: 'Tuple[float, float, float]' = (0, 1, 0.1), epsilon: 'float' = 1e-08, discontinuities: 'Sequence[float]' = [], use_smoothing: 'bool' = True, **kwargs)` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (6) · herdados: 318</summary>

- `__init__(self, t_func: 'Callable[[float], Sequence[float] | Vect3]', t_range: 'Tuple[float, float, float]' = (0, 1, 0.1), epsilon: 'float' = 1e-08, discontinuities: 'Sequence[float]' = [], use_smoothing: 'bool' = True, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_function(self)`
- `get_point_from_function(self, t: 'float') -> 'Vect3'`
- `get_t_func(self)`
- `get_x_range(self)`
- `init_points(self)`

</details>

### `ParametricSurface(uv_func: 'Callable[[float, float], Iterable[float]]', u_range: 'tuple[float, float]' = (0, 1), v_range: 'tuple[float, float]' = (0, 1), **kwargs)` ← Surface
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 246</summary>

- `__init__(self, uv_func: 'Callable[[float, float], Iterable[float]]', u_range: 'tuple[float, float]' = (0, 1), v_range: 'tuple[float, float]' = (0, 1), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `uv_func(self, u, v)`

</details>

### `PlaneFractal(plane: 'CoordinateSystem', **kwargs)` ← Mobject
> A fractal drawn a pixel at a time by its shader, over a rectangle covering a plane.

<details><summary>métodos próprios (7) · herdados: 230</summary>

- `__init__(self, plane: 'CoordinateSystem', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `init_data(self) -> 'None'`
- `match_plane(self, plane: 'CoordinateSystem') -> 'Self'` — Covers the plane, and reads a pixel's place on screen as a place on it
- `set_color(self, color, opacity=None, recurse=True) -> 'Self'` — Nothing: a fractal's colors say what a point converged to or how long it took, and
- `set_n_steps(self, n_steps: 'int') -> 'Self'`
- `set_offset(self, offset: 'Vect3') -> 'Self'`
- `set_scale_factor(self, scale_factor: 'float') -> 'Self'`

</details>

### `Point(location: 'Vect3' = array([0., 0., 0.]), artificial_width: 'float' = 1e-06, artificial_height: 'float' = 1e-06, **kwargs)` ← Mobject
> Mathematical Object

<details><summary>métodos próprios (6) · herdados: 229</summary>

- `__init__(self, location: 'Vect3' = array([0., 0., 0.]), artificial_width: 'float' = 1e-06, artificial_height: 'float' = 1e-06, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_bounding_box_point(self, *args, **kwargs) -> 'Vect3'`
- `get_height(self) -> 'float'`
- `get_location(self) -> 'Vect3'`
- `get_width(self) -> 'float'`
- `set_location(self, new_loc: 'npt.ArrayLike') -> 'Self'`

</details>

### `SampleSpace(width: 'float' = 3, height: 'float' = 3, fill_color: 'ManimColor' = '#444444', fill_opacity: 'float' = 1, stroke_width: 'float' = 0.5, stroke_color: 'ManimColor' = '#BBBBBB', default_label_scale_val: 'float' = 1, **kwargs)` ← Rectangle
> Creates a rectangle at the center of the screen.

<details><summary>métodos próprios (14) · herdados: 321</summary>

- `__init__(self, width: 'float' = 3, height: 'float' = 3, fill_color: 'ManimColor' = '#444444', fill_opacity: 'float' = 1, stroke_width: 'float' = 0.5, stroke_color: 'ManimColor' = '#BBBBBB', default_label_scale_val: 'float' = 1, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_braces_and_labels(self) -> 'None'`
- `add_label(self, label: 'str') -> 'None'`
- `add_title(self, title: 'str' = 'Sample space', buff: 'float' = 0.25) -> 'None'`
- `complete_p_list(self, p_list: 'list[float]') -> 'list[float]'`
- `divide_horizontally(self, *args, **kwargs) -> 'None'`
- `divide_vertically(self, *args, **kwargs) -> 'None'`
- `get_bottom_braces_and_labels(self, labels: 'str', **kwargs) -> 'VGroup'`
- `get_division_along_dimension(self, p_list: 'list[float]', dim: 'int', colors: 'Iterable[ManimColor]', vect: 'np.ndarray') -> 'VGroup'`
- `get_horizontal_division(self, p_list: 'list[float]', colors: 'Iterable[ManimColor]' = ['#699C52', '#1C758A'], vect: 'np.ndarray' = array([ 0., -1.,  0.])) -> 'VGroup'`
- `get_side_braces_and_labels(self, labels: 'str', direction: 'np.ndarray' = array([-1.,  0.,  0.]), **kwargs) -> 'VGroup'`
- `get_subdivision_braces_and_labels(self, parts: 'VGroup', labels: 'str', direction: 'np.ndarray', buff: 'float' = 0.1) -> 'VGroup'`
- `get_top_braces_and_labels(self, labels: 'str', **kwargs) -> 'VGroup'`
- `get_vertical_division(self, p_list: 'list[float]', colors: 'Iterable[ManimColor]' = ['#EC92AB', '#FFFF00'], vect: 'np.ndarray' = array([1., 0., 0.])) -> 'VGroup'`

</details>

### `ScreenRectangle(aspect_ratio: 'float' = 1.7777777777777777, height: 'float' = 4, **kwargs)` ← Rectangle
> Creates a rectangle at the center of the screen.

<details><summary>métodos próprios (1) · herdados: 321</summary>

- `__init__(self, aspect_ratio: 'float' = 1.7777777777777777, height: 'float' = 4, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Slider(value_tracker: 'ValueTracker', x_range: 'Tuple[float, float]' = (-5, 5), var_name: 'Optional[str]' = None, width: 'float' = 3, unit_size: 'float' = 1, arrow_width: 'float' = 0.15, arrow_length: 'float' = 0.15, arrow_color: 'ManimColor' = '#FFFF00', font_size: 'int' = 24, label_buff: 'float' = 0.1, num_decimal_places: 'int' = 2, tick_size: 'float' = 0.05, number_line_config: 'Dict[str, Any]' = {}, arrow_tip_config: 'Dict[str, Any]' = {}, decimal_config: 'Dict[str, Any]' = {}, angle: 'float' = 0, label_direction: 'Optional[np.ndarray]' = None, add_tick_labels: 'bool' = True, tick_label_font_size: 'int' = 16)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, value_tracker: 'ValueTracker', x_range: 'Tuple[float, float]' = (-5, 5), var_name: 'Optional[str]' = None, width: 'float' = 3, unit_size: 'float' = 1, arrow_width: 'float' = 0.15, arrow_length: 'float' = 0.15, arrow_color: 'ManimColor' = '#FFFF00', font_size: 'int' = 24, label_buff: 'float' = 0.1, num_decimal_places: 'int' = 2, tick_size: 'float' = 0.05, number_line_config: 'Dict[str, Any]' = {}, arrow_tip_config: 'Dict[str, Any]' = {}, decimal_config: 'Dict[str, Any]' = {}, angle: 'float' = 0, label_direction: 'Optional[np.ndarray]' = None, add_tick_labels: 'bool' = True, tick_label_font_size: 'int' = 16)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Surface(color: 'ManimColor' = '#888888', shading: 'Tuple[float, float, float]' = (0.3, 0.2, 0.4), depth_test: 'bool' = True, u_range: 'Tuple[float, float]' = (0.0, 1.0), v_range: 'Tuple[float, float]' = (0.0, 1.0), resolution: 'Tuple[int, int]' = (101, 101), preferred_creation_axis: 'int' = 1, sort_to_camera: 'bool' = False, **kwargs)` ← Mobject
> Mathematical Object

<details><summary>métodos próprios (21) · herdados: 227</summary>

- `__init__(self, color: 'ManimColor' = '#888888', shading: 'Tuple[float, float, float]' = (0.3, 0.2, 0.4), depth_test: 'bool' = True, u_range: 'Tuple[float, float]' = (0.0, 1.0), v_range: 'Tuple[float, float]' = (0.0, 1.0), resolution: 'Tuple[int, int]' = (101, 101), preferred_creation_axis: 'int' = 1, sort_to_camera: 'bool' = False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `align_points(self, mobject: 'Mobject') -> 'Self'` — Two surfaces are brought to a common number of points by sampling each over the
- `always_sort_to_camera(self, camera=None) -> 'Self'`
- `color_by_uv_function(self, uv_to_color: 'Callable[[Vect2], Color]')`
- `get_partial_points_array(self, points: 'Vect3Array', a: 'float', b: 'float', resolution: 'Sequence[int]', axis: 'int') -> 'Vect3Array'`
- `get_resolution(self) -> 'Tuple[int, int]'` — How many rows and columns of points the surface samples. Kept among the uniforms,
- `get_triangles(self) -> 'Tuple[np.ndarray, Vect3Array]'` — Which vertex each triangle of the mesh starts at, and where the middle of it sits, for
- `get_unit_normals(self) -> 'Vect3Array'` — Which way the surface faces at each of its points, from the directions it runs
- `get_uv_grid(self) -> 'np.array'` — Returns an (nu, nv, 2) array of all pairs of u, v values, where
- `has_grid(self) -> 'bool'` — Whether the points held really are a grid of the resolution recorded. An imported
- `init_points(self)`
- `init_uniforms(self)`
- `interpolate(self, mobject1: 'Mobject', mobject2: 'Mobject', alpha: 'float', path_func: 'Callable[[np.ndarray, np.ndarray, float], np.ndarray]' = <function straight_path at 0x7f6ff3b247c0>) -> 'Self'`
- `is_opaque(self) -> 'bool'` — Whether nothing behind the surface shows through it, which decides whether its
- `min_opacity(self) -> 'float'` — The least opaque any point of the surface is
- `pointwise_become_partial(self, smobject: "'Surface'", a: 'float', b: 'float', axis: 'int | None' = None) -> 'Self'` — Set points in such a way as to become only
- `resample(self, resolution: 'Tuple[int, int]') -> 'Self'` — Samples the surface over a grid of a different shape, interpolating along each
- `set_resolution(self, resolution: 'Tuple[int, int]') -> 'Self'`
- `set_sort_to_camera(self, sort: 'bool' = True) -> 'Self'` — Asks for the surface's triangles to be drawn furthest from the camera first, whether or
- `uv_func(self, u: 'float', v: 'float') -> 'tuple[float, float, float]'`
- `uv_to_point(self, u, v)`

</details>

### `SurroundingRectangle(mobject: 'Mobject', buff: 'float' = 0.1, color: 'ManimColor' = '#FFFF00', **kwargs)` ← Rectangle
> Creates a rectangle at the center of the screen.

<details><summary>métodos próprios (3) · herdados: 320</summary>

- `__init__(self, mobject: 'Mobject', buff: 'float' = 0.1, color: 'ManimColor' = '#FFFF00', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `set_buff(self, buff) -> 'Self'`
- `surround(self, mobject, buff=None) -> 'Self'`

</details>

### `Textbox(value: 'str' = '', value_type: 'np.dtype' = dtype('O'), box_kwargs: 'dict' = {'width': 2.0, 'height': 1.0, 'fill_color': '#FFFFFF', 'fill_opacity': 1.0}, text_kwargs: 'dict' = {'color': '#58C4DD'}, text_buff: 'float' = 0.25, isInitiallyActive: 'bool' = False, active_color: 'ManimColor' = '#58C4DD', deactive_color: 'ManimColor' = '#FC6255', **kwargs)` ← ControlMobject
> Not meant to be displayed.  Instead the position encodes some

<details><summary>métodos próprios (6) · herdados: 236</summary>

- `__init__(self, value: 'str' = '', value_type: 'np.dtype' = dtype('O'), box_kwargs: 'dict' = {'width': 2.0, 'height': 1.0, 'fill_color': '#FFFFFF', 'fill_opacity': 1.0}, text_kwargs: 'dict' = {'color': '#58C4DD'}, text_buff: 'float' = 0.25, isInitiallyActive: 'bool' = False, active_color: 'ManimColor' = '#58C4DD', deactive_color: 'ManimColor' = '#FC6255', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `active_anim(self, isActive: 'bool') -> 'None'`
- `box_on_mouse_press(self, mob, event_data) -> 'bool'`
- `on_key_press(self, mob: 'Mobject', event_data: 'dict[str, int]') -> 'bool | None'`
- `set_value_anim(self, value: 'str') -> 'None'`
- `update_text(self, value: 'str') -> 'None'`

</details>

### `TexturedGeometry(geometry: 'trimesh.base.Trimesh', texture_file: 'str', **kwargs)` ← TexturedSurface
> An imported mesh, which is a list of triangles rather than a grid of points, so

<details><summary>métodos próprios (2) · herdados: 247</summary>

- `__init__(self, geometry: 'trimesh.base.Trimesh', texture_file: 'str', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `init_points(self)`

</details>

### `TexturedSurface(uv_surface: 'Surface', image_file: 'str', dark_image_file: 'str | None' = None, **kwargs)` ← Surface
> Mathematical Object

<details><summary>métodos próprios (8) · herdados: 241</summary>

- `__init__(self, uv_surface: 'Surface', image_file: 'str', dark_image_file: 'str | None' = None, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `init_points(self)`
- `init_uniforms(self)`
- `min_opacity(self) -> 'float'` — The least opaque any point of the surface is
- `pointwise_become_partial(self, tsmobject: "'TexturedSurface'", a: 'float', b: 'float', axis: 'int | None' = None) -> 'Self'` — Set points in such a way as to become only
- `set_color(self, color: 'ManimColor | Iterable[ManimColor] | None', opacity: 'float | Iterable[float] | None' = None, recurse: 'bool' = True) -> 'Self'`
- `set_image_coords_by_uv_func(self, uv_func) -> 'Self'` — uv_func takes in a pair (u, v), and returns a new pair (u', v') used
- `set_opacity(self, opacity: 'float | Iterable[float]', recurse=True) -> 'Self'`

</details>

### `ThreeDAxes(x_range: 'RangeSpecifier' = (-6.0, 6.0, 1.0), y_range: 'RangeSpecifier' = (-5.0, 5.0, 1.0), z_range: 'RangeSpecifier' = (-4.0, 4.0, 1.0), z_axis_config: 'dict' = {}, z_normal: 'Vect3' = array([ 0., -1.,  0.]), depth: 'float | None' = None, **kwargs)` ← Axes
> Mathematical Object

<details><summary>métodos próprios (5) · herdados: 351</summary>

- `__init__(self, x_range: 'RangeSpecifier' = (-6.0, 6.0, 1.0), y_range: 'RangeSpecifier' = (-5.0, 5.0, 1.0), z_range: 'RangeSpecifier' = (-4.0, 4.0, 1.0), z_axis_config: 'dict' = {}, z_normal: 'Vect3' = array([ 0., -1.,  0.]), depth: 'float | None' = None, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_axis_labels(self, x_tex='x', y_tex='y', z_tex='z', font_size=24, buff=0.2)`
- `get_all_ranges(self) -> 'list[Sequence[float]]'`
- `get_graph(self, func, color='#1C758A', opacity=0.9, u_range=None, v_range=None, **kwargs) -> 'ParametricSurface'`
- `get_parametric_surface(self, func, color='#1C758A', opacity=0.9, **kwargs) -> 'ParametricSurface'`

</details>

### `ThreeDModel(obj_file: 'str', height=3)` ← Group
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 232</summary>

- `__init__(self, obj_file: 'str', height=3)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_textures_from_mtl(self, obj_filepath, suppress_warnings=True)` — Load an OBJ file and extract all texture filenames from its MTL file.

</details>

### `TracedPath(traced_point_func: 'Callable[[], Vect3]', time_traced: 'float' = inf, time_per_anchor: 'float' = 0.06666666666666667, stroke_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float | Iterable[float]' = 2.0, stroke_opacity: 'float' = 1.0, **kwargs)` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 319</summary>

- `__init__(self, traced_point_func: 'Callable[[], Vect3]', time_traced: 'float' = inf, time_per_anchor: 'float' = 0.06666666666666667, stroke_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float | Iterable[float]' = 2.0, stroke_opacity: 'float' = 1.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `update_path(self, dt: 'float') -> 'Self'`

</details>

### `TracingTail(mobject_or_func: 'Mobject | Callable[[], np.ndarray]', time_traced: 'float' = 1.0, stroke_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float | Iterable[float]' = (0, 3), stroke_opacity: 'float | Iterable[float]' = (0, 1), **kwargs)` ← TracedPath
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 320</summary>

- `__init__(self, mobject_or_func: 'Mobject | Callable[[], np.ndarray]', time_traced: 'float' = 1.0, stroke_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float | Iterable[float]' = (0, 3), stroke_opacity: 'float | Iterable[float]' = (0, 1), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `TrueDot(center: 'Vect3' = array([0., 0., 0.]), **kwargs)` ← DotCloud
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 247</summary>

- `__init__(self, center: 'Vect3' = array([0., 0., 0.]), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Underline(mobject: 'Mobject', buff: 'float' = 0.1, stroke_color='#FFFFFF', stroke_width: 'float | Sequence[float]' = [0, 3, 3, 0], stretch_factor=1.2, **kwargs)` ← Line
> Creates a line joining the points "start" and "end".

<details><summary>métodos próprios (1) · herdados: 347</summary>

- `__init__(self, mobject: 'Mobject', buff: 'float' = 0.1, stroke_color='#FFFFFF', stroke_width: 'float | Sequence[float]' = [0, 3, 3, 0], stretch_factor=1.2, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Union(*vmobjects: 'VMobject', **kwargs)` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, *vmobjects: 'VMobject', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `UnitInterval(x_range: 'RangeSpecifier' = (0, 1, 0.1), unit_size: 'float' = 10, big_tick_numbers: 'list[float]' = [0, 1], decimal_number_config: 'dict' = {'num_decimal_places': 1}, **kwargs)` ← NumberLine
> Creates a line joining the points "start" and "end".

<details><summary>métodos próprios (1) · herdados: 358</summary>

- `__init__(self, x_range: 'RangeSpecifier' = (0, 1, 0.1), unit_size: 'float' = 10, big_tick_numbers: 'list[float]' = [0, 1], decimal_number_config: 'dict' = {'num_decimal_places': 1}, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Updater(func: 'UpdateFunction')`
> Light wrapper for a function meant to be called on a mobject every frame.

<details><summary>métodos próprios (3) · herdados: 0</summary>

- `__call__(self, mobject: 'Mobject', dt: 'float' = 0, frame_rate: 'float | None' = None) -> 'None'` — Call self as a function.
- `__init__(self, func: 'UpdateFunction')` — Initialize self.  See help(type(self)) for accurate signature.
- `func_takes_dt(func: 'UpdateFunction') -> 'bool'`

</details>

### `VGroup(*vmobjects: 'SubVmobjectType | Iterable[SubVmobjectType]', **kwargs)` ← Group, VMobject, Generic
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, *vmobjects: 'SubVmobjectType | Iterable[SubVmobjectType]', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `VHighlight(vmobject: 'VMobject', n_layers: 'int' = 5, color_bounds: 'Tuple[ManimColor]' = ('#888888', '#222222'), max_stroke_addition: 'float' = 5.0)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, vmobject: 'VMobject', n_layers: 'int' = 5, color_bounds: 'Tuple[ManimColor]' = ('#888888', '#222222'), max_stroke_addition: 'float' = 5.0)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `VMobject(color: 'ManimColor' = None, fill_color: 'ManimColor' = None, fill_opacity: 'float | Iterable[float] | None' = 0.0, stroke_color: 'ManimColor' = None, stroke_opacity: 'float | Iterable[float] | None' = 1.0, stroke_width: 'float | Iterable[float] | None' = 4.0, stroke_behind: 'bool' = False, background_image_file: 'str | None' = None, long_lines: 'bool' = False, joint_roundness: 'float' = 0.0, flat_stroke: 'bool' = False, stroke_width_in_scene_units: 'bool' = False, use_simple_quadratic_approx: 'bool' = False, anti_alias_width: 'float' = 1.5, fill_border_width: 'float' = 0.0, **kwargs)` ← Mobject
> Mathematical Object

<details><summary>métodos próprios (115) · herdados: 205</summary>

- `__init__(self, color: 'ManimColor' = None, fill_color: 'ManimColor' = None, fill_opacity: 'float | Iterable[float] | None' = 0.0, stroke_color: 'ManimColor' = None, stroke_opacity: 'float | Iterable[float] | None' = 1.0, stroke_width: 'float | Iterable[float] | None' = 4.0, stroke_behind: 'bool' = False, background_image_file: 'str | None' = None, long_lines: 'bool' = False, joint_roundness: 'float' = 0.0, flat_stroke: 'bool' = False, stroke_width_in_scene_units: 'bool' = False, use_simple_quadratic_approx: 'bool' = False, anti_alias_width: 'float' = 1.5, fill_border_width: 'float' = 0.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `add(self, *vmobjects: 'VMobject') -> 'Self'`
- `add_arc_to(self, point: 'Vect3', angle: 'float', n_components: 'int | None' = None, threshold: 'float' = 0.001) -> 'Self'`
- `add_cubic_bezier_curve(self, anchor1: 'Vect3', handle1: 'Vect3', handle2: 'Vect3', anchor2: 'Vect3') -> 'Self'`
- `add_cubic_bezier_curve_to(self, handle1: 'Vect3', handle2: 'Vect3', anchor: 'Vect3') -> 'Self'` — Add cubic bezier curve to the path.
- `add_line_to(self, point: 'Vect3', allow_null_line: 'bool' = True) -> 'Self'`
- `add_points_as_corners(self, points: 'Iterable[Vect3]') -> 'Self'`
- `add_quadratic_bezier_curve_to(self, handle: 'Vect3', anchor: 'Vect3', allow_null_curve=True) -> 'Self'`
- `add_smooth_cubic_curve_to(self, handle: 'Vect3', point: 'Vect3') -> 'Self'`
- `add_smooth_curve_to(self, point: 'Vect3') -> 'Self'`
- `add_subpath(self, points: 'Vect3Array') -> 'Self'`
- `align_points(self, vmobject: 'VMobject') -> 'Self'`
- `append_points(self, points: 'Vect3Array') -> 'Self'`
- `append_vectorized_mobject(self, vmobject: 'VMobject') -> 'Self'`
- `apply_depth_test(self, anti_alias_width: 'float' = 0, recurse: 'bool' = True) -> 'Self'`
- `apply_function(self, function: 'Callable[[Vect3], Vect3]', make_smooth: 'bool' = False, **kwargs) -> 'Self'`
- `apply_matrix(self, *args, **kwargs) -> 'Self'`
- `change_anchor_mode(self, mode: 'str') -> 'Self'`
- `close_path(self, smooth: 'bool' = False) -> 'Self'`
- `consider_points_equal(self, p0: 'Vect3', p1: 'Vect3') -> 'bool'`
- `copy(self, deep: 'bool' = False) -> 'Self'` — A copy is a group of its own. Left pointing at what it was copied from, its fills
- `curve_and_prop_of_partial_point(self, alpha) -> 'Tuple[int, float]'` — If you want a point a proportion alpha along the curve, this
- `deactivate_depth_test(self, anti_alias_width: 'float' = 1.0, recurse: 'bool' = True) -> 'Self'`
- `draw_fills_together(self, draw_together: 'bool' = True) -> 'Self'` — Promises that these mobjects' filled regions do not overlap one another, which lets
- `draw_fills_together_if_disjoint(self) -> 'Self'` — Looks at where the filled members of this family sit, and makes the promise of
- `ensure_positive_orientation(self, recurse=True) -> 'Self'`
- `fade(self, darkness: 'float' = 0.5, recurse: 'bool' = True) -> 'Self'`
- `get_anchors(self) -> 'Vect3Array'`
- `get_anchors_and_handles(self) -> 'list[Vect3]'` — returns anchors1, handles, anchors2,
- `get_anti_alias_width(self)`
- `get_arc_length(self, n_sample_points: 'int | None' = None) -> 'float'`
- `get_area_vector(self) -> 'Vect3'`
- `get_bezier_tuples(self) -> 'Iterable[Vect3Array]'`
- `get_bezier_tuples_from_points(self, points: 'Vect3Array') -> 'Iterable[Vect3Array]'`
- `get_color(self) -> 'str'`
- `get_end_anchors(self) -> 'Vect3'`
- `get_fill_color(self) -> 'str'`
- `get_fill_colors(self) -> 'list[str]'`
- `get_fill_opacity(self) -> 'float'`
- `get_flat_stroke(self) -> 'bool'`
- `get_grid(self, *args, **kwargs) -> 'Self'` — Copies laid out apart from one another, so unless the layout crowds them their
- `get_group_class(self)`
- `get_joint_roundness(self) -> 'float'`
- `get_last_point(self) -> 'Vect3'`
- `get_nth_curve_function(self, n: 'int') -> 'Callable[[float], Vect3]'`
- `get_nth_curve_points(self, n: 'int') -> 'Vect3Array'`
- `get_num_curves(self) -> 'int'`
- `get_opacity(self) -> 'float'`
- `get_points_without_null_curves(self, atol: 'float' = 1e-09) -> 'Vect3Array'`
- `get_reflection_of_last_handle(self) -> 'Vect3'`
- `get_scale_stroke_with_zoom(self) -> 'bool'`
- `get_start_anchors(self) -> 'Vect3Array'`
- `get_stroke_color(self) -> 'str'`
- `get_stroke_colors(self) -> 'list[str]'`
- `get_stroke_opacities(self) -> 'np.ndarray'`
- `get_stroke_opacity(self) -> 'float'`
- `get_stroke_width(self) -> 'float'`
- `get_stroke_width_in_scene_units(self) -> 'bool'`
- `get_stroke_widths(self) -> 'np.ndarray'`
- `get_style(self) -> 'dict[str, Any]'`
- `get_subcurve(self, a: 'float', b: 'float') -> 'Self'`
- `get_subpath_end_indices(self) -> 'np.ndarray'`
- `get_subpath_end_indices_from_points(self, points: 'Vect3Array') -> 'np.ndarray'`
- `get_subpath_range(self, index: 'int' = -1) -> 'Tuple[int, int]'` — Where the subpath holding the point at the given index begins and ends
- `get_subpaths(self) -> 'list[Vect3Array]'`
- `get_subpaths_from_points(self, points: 'Vect3Array') -> 'list[Vect3Array]'`
- `get_unit_normal(self, refresh: 'bool' = False) -> 'Vect3'`
- `has_fill(self) -> 'bool'`
- `has_fill_gradient(self) -> 'bool'`
- `has_new_path_started(self) -> 'bool'`
- `has_stroke(self) -> 'bool'`
- `init_colors(self)`
- `init_uniforms(self)`
- `insert_n_curves(self, n: 'int', recurse: 'bool' = True) -> 'Self'`
- `insert_n_curves_to_point_list(self, n: 'int', points: 'Vect3Array') -> 'Vect3Array'` — The same path traced by n more curves than it was, cut so as to leave the longest of
- `is_closed(self) -> 'bool'`
- `is_smooth(self, angle_tol=0.017453292519943295) -> 'bool'` — Whether the tangent direction carries through each anchor, rather than
- `make_approximately_smooth(self, recurse=True) -> 'Self'`
- `make_jagged(self, recurse=True) -> 'Self'`
- `make_smooth(self, approx=True, recurse=True) -> 'Self'` — Edits the path so as to pass smoothly through all
- `match_style(self, vmobject: 'VMobject', recurse: 'bool' = True) -> 'Self'`
- `point_from_proportion(self, alpha: 'float') -> 'Vect3'`
- `pointwise_become_partial(self, vmobject: 'VMobject', a: 'float', b: 'float') -> 'Self'` — Set points in such a way as to become only
- `quick_point_from_proportion(self, alpha: 'float') -> 'Vect3'`
- `refresh_unit_normal(self) -> 'Self'`
- `replace_shader_code(self, old: 'str', new: 'str', code_target: 'str | None' = None) -> 'Self'` — A snippet naming a field of one of the two shaders, stroke_rgba say, would not compile
- `reverse_points(self, recurse: 'bool' = True) -> 'Self'`
- `rotate(self, angle: 'float', axis: 'Vect3' = array([0., 0., 1.]), about_point: 'Vect3 | None' = None, **kwargs) -> 'Self'`
- `set_anchors_and_handles(self, anchors: 'Vect3Array', handles: 'Vect3Array') -> 'Self'`
- `set_anti_alias_width(self, anti_alias_width: 'float', recurse: 'bool' = True) -> 'Self'`
- `set_backstroke(self, color: 'ManimColor | Iterable[ManimColor]' = '#000000', width: 'float | Iterable[float]' = 3) -> 'Self'`
- `set_color(self, color: 'ManimColor | Iterable[ManimColor] | None', opacity: 'float | Iterable[float] | None' = None, recurse: 'bool' = True) -> 'Self'`
- `set_color_by_code(self, wgsl_code: 'str', code_target: 'str | None' = None) -> 'Self'` — Takes a snippet of code and inserts it into a context which has the following
- `set_color_by_proportion(self, prop_to_color: 'Callable[[float], Color]') -> 'Self'`
- `set_data(self, data: 'np.ndarray') -> 'Self'`
- `set_fill(self, color: 'ManimColor | Iterable[ManimColor]' = None, opacity: 'float | Iterable[float] | None' = None, border_width: 'float | None' = None, gradient_direction: 'Vect3 | None' = None, recurse: 'bool' = True) -> 'Self'` — Two colors, or two opacities, fill with a gradient running between them along
- `set_fill_gradient_points(self, direction: 'Vect3 | None' = None, recurse: 'bool' = True) -> 'Self'` — Puts the gradient's two ends on the extremes of this mobject along the given
- `set_flat_stroke(self, flat_stroke: 'bool' = True, recurse: 'bool' = True) -> 'Self'`
- `set_joint_roundness(self, roundness: 'float', recurse: 'bool' = True) -> 'Self'`
- `set_opacity(self, opacity: 'float | Iterable[float] | None', recurse: 'bool' = True) -> 'Self'`
- `set_points(self, points: 'Vect3Array') -> 'Self'`
- `set_points_as_corners(self, points: 'Iterable[Vect3]') -> 'Self'`
- `set_points_smoothly(self, points: 'Iterable[Vect3]', approx: 'bool' = True) -> 'Self'`
- `set_scale_stroke_with_zoom(self, scale_stroke_with_zoom: 'bool' = True, recurse: 'bool' = True) -> 'Self'`
- `set_stroke(self, color: 'ManimColor | Iterable[ManimColor]' = None, width: 'float | Iterable[float] | None' = None, opacity: 'float | Iterable[float] | None' = None, behind: 'bool | None' = None, flat: 'bool | None' = None, recurse: 'bool' = True) -> 'Self'`
- `set_stroke_width_in_scene_units(self, value: 'bool' = True, recurse: 'bool' = True) -> 'Self'`
- `set_style(self, fill_color: 'ManimColor | Iterable[ManimColor] | None' = None, fill_opacity: 'float | Iterable[float] | None' = None, fill_rgba: 'Vect4 | None' = None, fill_rgba_end: 'Vect4 | None' = None, fill_border_width: 'float | None' = None, stroke_color: 'ManimColor | Iterable[ManimColor] | None' = None, stroke_opacity: 'float | Iterable[float] | None' = None, stroke_rgba: 'Vect4 | None' = None, stroke_width: 'float | Iterable[float] | None' = None, stroke_behind: 'bool | None' = None, flat_stroke: 'Optional[bool]' = None, shading: 'Tuple[float, float, float] | None' = None, recurse: 'bool' = True) -> 'Self'`
- `set_subpath_range(self) -> 'Self'` — Notes against every point how far off the ends of its subpath are. The stroke shader
- `start_new_path(self, point: 'Vect3') -> 'Self'`
- `stretch(self, *args, **kwargs) -> 'Self'`
- `subdivide_curves_by_condition(self, tuple_to_subdivisions: 'Callable', recurse: 'bool' = True) -> 'Self'`
- `subdivide_intersections(self, recurse: 'bool' = True, n_subdivisions: 'int' = 1) -> 'Self'`
- `subdivide_sharp_curves(self, angle_threshold: 'float' = 0.5235987755982988, recurse: 'bool' = True) -> 'Self'`
- `triggers_refresh(func: 'Callable')`
- `use_winding_fill(self, value: 'bool' = True, recurse: 'bool' = True) -> 'Self'`

</details>

### `VectorizedPoint(location: 'np.ndarray' = array([0., 0., 0.]), color: 'ManimColor' = '#000000', fill_opacity: 'float' = 0.0, stroke_width: 'float' = 0.0, **kwargs)` ← Point, VMobject
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 321</summary>

- `__init__(self, location: 'np.ndarray' = array([0., 0., 0.]), color: 'ManimColor' = '#000000', fill_opacity: 'float' = 0.0, stroke_width: 'float' = 0.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

- `BLACK` = `'#000000'`
- `BLACK` = `'#000000'`
- `BLACK` = `'#000000'`
- `BLACK` = `'#000000'`
- `BLACK` = `'#000000'`
- `BLACK` = `'#000000'`
- `BLUE` = `'#58C4DD'`
- `BLUE` = `'#58C4DD'`
- `BLUE` = `'#58C4DD'`
- `BLUE_B` = `'#9CDCEB'`
- `BLUE_D` = `'#29ABCA'`
- `BLUE_D` = `'#29ABCA'`
- `BLUE_E` = `'#1C758A'`
- `BLUE_E` = `'#1C758A'`
- `BLUE_E` = `'#1C758A'`
- `COMMON_UNIFORMS` = `(('is_fixed_in_frame', 1), ('shading', 3), ('clip_plane0', 4), ('clip_plane1', 4), ('clip_plane2', 4), ('clip_plane3'...`
- `COMMON_UNIFORMS` = `(('is_fixed_in_frame', 1), ('shading', 3), ('clip_plane0', 4), ('clip_plane1', 4), ('clip_plane2', 4), ('clip_plane3'...`
- `COMMON_UNIFORMS` = `(('is_fixed_in_frame', 1), ('shading', 3), ('clip_plane0', 4), ('clip_plane1', 4), ('clip_plane2', 4), ('clip_plane3'...`
- `COMMON_UNIFORMS` = `(('is_fixed_in_frame', 1), ('shading', 3), ('clip_plane0', 4), ('clip_plane1', 4), ('clip_plane2', 4), ('clip_plane3'...`
- `COMMON_UNIFORMS` = `(('is_fixed_in_frame', 1), ('shading', 3), ('clip_plane0', 4), ('clip_plane1', 4), ('clip_plane2', 4), ('clip_plane3'...`
- `DEFAULT_BUFF_RATIO` = `0.5`
- `DEFAULT_DOT_RADIUS` = `0.05`
- `DEFAULT_GLOW_DOT_RADIUS` = `0.2`
- `DEFAULT_GRID_HEIGHT` = `6`
- `DEFAULT_LIGHT_COLOR` = `'#BBBBBB'`
- `DEFAULT_MOBJECT_COLOR` = `'#FFFFFF'`
- `DEFAULT_MOBJECT_COLOR` = `'#FFFFFF'`
- `DEFAULT_MOBJECT_COLOR` = `'#FFFFFF'`
- `DEFAULT_MOBJECT_COLOR` = `'#FFFFFF'`
- `DEFAULT_MOBJECT_COLOR` = `'#FFFFFF'`
- `DEFAULT_MOBJECT_COLOR` = `'#FFFFFF'`
- `DEFAULT_MOBJECT_TO_EDGE_BUFF` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFF` = `0.25`
- `DEFAULT_STROKE_WIDTH` = `4.0`
- `DEFAULT_VMOBJECT_FILL_COLOR` = `'#888888'`
- `DEFAULT_VMOBJECT_STROKE_COLOR` = `'#DDDDDD'`
- `DEFAULT_X_RANGE` = `(-8.0, 8.0, 1.0)`
- `DEFAULT_Y_RANGE` = `(-4.0, 4.0, 1.0)`
- `DEG` = `0.017453292519943295`
- `DEG` = `0.017453292519943295`
- `DEG` = `0.017453292519943295`
- `DEG` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPSILON` = `1e-08`
- `EPSILON` = `0.0001`
- `FRAME_HEIGHT` = `8.0`
- `FRAME_HEIGHT` = `8.0`
- `FRAME_WIDTH` = `14.222222222222221`
- `FRAME_X_RADIUS` = `7.111111111111111`
- `FRAME_X_RADIUS` = `7.111111111111111`
- `FRAME_X_RADIUS` = `7.111111111111111`
- `FRAME_Y_RADIUS` = `4.0`
- `FRAME_Y_RADIUS` = `4.0`
- `FRAME_Y_RADIUS` = `4.0`
- `GRADIENT_POINT_KEYS` = `['gradient_start', 'gradient_end']`
- `GREEN` = `'#83C167'`
- `GREEN` = `'#83C167'`
- `GREEN_E` = `'#699C52'`
- `GREY` = `'#888888'`
- `GREY_A` = `'#DDDDDD'`
- `GREY_A` = `'#DDDDDD'`
- `GREY_A` = `'#DDDDDD'`
- `GREY_B` = `'#BBBBBB'`
- `GREY_BROWN` = `'#736357'`
- `GREY_C` = `'#888888'`
- `GREY_C` = `'#888888'`
- `GREY_C` = `'#888888'`
- `GREY_D` = `'#444444'`
- `GREY_E` = `'#222222'`
- `GREY_E` = `'#222222'`
- `IN` = `array([ 0.,  0., -1.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `MANDELBROT_COLORS` = `['#00065c', '#061e7e', '#0c37a0', '#205abc', '#4287d3', '#D9EDE4', '#F0F9E4', '#BA9F6A', '#573706']`
- `MAROON_B` = `'#EC92AB'`
- `MAX_DEGREE` = `5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `NEWTON_ROOT_COLORS` = `['#440154', '#3b528b', '#21908c', '#5dc963', '#29abca']`
- `NULL_POINTS` = `array([[0., 0., 0.]])`
- `N_MANDELBROT_COLORS` = `9`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `RED` = `'#FC6255'`
- `RED` = `'#FC6255'`
- `RED` = `'#FC6255'`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `WHITE` = `'#FFFFFF'`
- `YELLOW` = `'#FFFF00'`
- `YELLOW` = `'#FFFF00'`
- `YELLOW` = `'#FFFF00'`
- `YELLOW` = `'#FFFF00'`
- `YELLOW` = `'#FFFF00'`
- **`always(method, *args, **kwargs)`**
- **`always_redraw(func: 'Callable[..., Mobject]', *args, **kwargs) -> 'Mobject'`**
- **`always_rotate(mobject: 'Mobject', rate: 'float' = 0.3490658503988659, **kwargs) -> 'Mobject'`**
- **`always_shift(mobject: 'Mobject', direction: 'np.ndarray' = array([1., 0., 0.]), rate: 'float' = 0.1) -> 'Mobject'`**
- **`as_color_rows(colors: 'Sequence[ManimColor]', length: 'int', opacity: 'float' = 1.0)`** — Colors as the rows of such an array, the last of them repeated to fill it
- **`as_complex_pairs(values: 'Iterable[complex]', length: 'int') -> 'np.ndarray'`** — Complex numbers as the rows of an array a uniform block has room for, which holds four
- **`assert_is_mobject_method(method)`**
- **`coefficients_to_roots(coefs: 'Iterable[complex]') -> 'np.ndarray'`** — The roots of a polynomial given lowest power first
- **`cycle_animation(animation: 'Animation', **kwargs) -> 'Mobject'`**
- **`f_always(method, *arg_generators, **kwargs)`** — More functional version of always, where instead
- **`full_range_specifier(range_args)`**
- **`norms_along_axis(vectors: 'Vect3Array') -> 'np.ndarray'`**
- **`override_animate(method)`**
- **`roots_to_coefficients(roots: 'Iterable[complex]') -> 'np.ndarray'`** — The polynomial with these roots and a leading coefficient of one, lowest power first
- **`turn_animation_into_updater(animation: 'Animation', cycle: 'bool' = False, **kwargs) -> 'Mobject'`** — Add an updater to the animation's mobject which applies

## mobject/geometry

### `AnnularSector(angle: 'float' = 1.5707963267948966, start_angle: 'float' = 0.0, inner_radius: 'float' = 1.0, outer_radius: 'float' = 2.0, arc_center: 'Vect3' = array([0., 0., 0.]), fill_color: 'ManimColor' = '#BBBBBB', fill_opacity: 'float' = 1.0, stroke_width: 'float' = 0.0, **kwargs)` ← VMobject
> Creates an annular sector.

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, angle: 'float' = 1.5707963267948966, start_angle: 'float' = 0.0, inner_radius: 'float' = 1.0, outer_radius: 'float' = 2.0, arc_center: 'Vect3' = array([0., 0., 0.]), fill_color: 'ManimColor' = '#BBBBBB', fill_opacity: 'float' = 1.0, stroke_width: 'float' = 0.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Annulus(inner_radius: 'float' = 1.0, outer_radius: 'float' = 2.0, fill_opacity: 'float' = 1.0, stroke_width: 'float' = 0.0, fill_color: 'ManimColor' = '#BBBBBB', center: 'Vect3' = array([0., 0., 0.]), **kwargs)` ← VMobject
> Creates an annulus.

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, inner_radius: 'float' = 1.0, outer_radius: 'float' = 2.0, fill_opacity: 'float' = 1.0, stroke_width: 'float' = 0.0, fill_color: 'ManimColor' = '#BBBBBB', center: 'Vect3' = array([0., 0., 0.]), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Arc(start_angle: 'float' = 0, angle: 'float' = 1.5707963267948966, radius: 'float' = 1.0, n_components: 'Optional[int]' = None, arc_center: 'Vect3' = array([0., 0., 0.]), **kwargs)` ← TipableVMobject
> Creates an arc.

<details><summary>métodos próprios (5) · herdados: 334</summary>

- `__init__(self, start_angle: 'float' = 0, angle: 'float' = 1.5707963267948966, radius: 'float' = 1.0, n_components: 'Optional[int]' = None, arc_center: 'Vect3' = array([0., 0., 0.]), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_arc_center(self) -> 'Vect3'` — Looks at the normals to the first two
- `get_start_angle(self) -> 'float'`
- `get_stop_angle(self) -> 'float'`
- `move_arc_center_to(self, point: 'Vect3') -> 'Self'`

</details>

### `ArcBetweenPoints(start: 'Vect3', end: 'Vect3', angle: 'float' = 1.5707963267948966, **kwargs)` ← Arc
> Creates an arc passing through the specified points with "angle" as the

<details><summary>métodos próprios (1) · herdados: 338</summary>

- `__init__(self, start: 'Vect3', end: 'Vect3', angle: 'float' = 1.5707963267948966, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Arrow(start: 'Vect3 | Mobject' = array([-1.,  0.,  0.]), end: 'Vect3 | Mobject' = array([-1.,  0.,  0.]), buff: 'float' = 0.25, path_arc: 'float' = 0, fill_color: 'ManimColor' = '#BBBBBB', fill_opacity: 'float' = 1.0, stroke_width: 'float' = 0.0, thickness: 'float' = 3.0, tip_width_ratio: 'float' = 5, tip_angle: 'float' = 1.0471975511965976, max_tip_length_to_length_ratio: 'float' = 0.5, max_width_to_length_ratio: 'float' = 0.1, **kwargs)` ← Line
> Creates an arrow.

<details><summary>métodos próprios (9) · herdados: 341</summary>

- `__init__(self, start: 'Vect3 | Mobject' = array([-1.,  0.,  0.]), end: 'Vect3 | Mobject' = array([-1.,  0.,  0.]), buff: 'float' = 0.25, path_arc: 'float' = 0, fill_color: 'ManimColor' = '#BBBBBB', fill_opacity: 'float' = 1.0, stroke_width: 'float' = 0.0, thickness: 'float' = 3.0, tip_width_ratio: 'float' = 5, tip_angle: 'float' = 1.0471975511965976, max_tip_length_to_length_ratio: 'float' = 0.5, max_width_to_length_ratio: 'float' = 0.1, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_end(self) -> 'Vect3'`
- `get_key_dimensions(self, length)`
- `get_start(self) -> 'Vect3'`
- `get_start_and_end(self)`
- `put_start_and_end_on(self, start: 'Vect3', end: 'Vect3') -> 'Self'`
- `scale(self, *args, **kwargs) -> 'Self'` — Default behavior is to scale about the center of the mobject.
- `set_points_by_ends(self, start: 'Vect3', end: 'Vect3', buff: 'float' = 0, path_arc: 'float' = 0) -> 'Self'`
- `set_thickness(self, thickness: 'float') -> 'Self'`

</details>

### `ArrowTip(angle: 'float' = 0, width: 'float' = 0.35, length: 'float' = 0.35, fill_opacity: 'float' = 1.0, fill_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 0.0, tip_style: 'int' = 0, **kwargs)` ← Triangle
> Creates a triangle of edge length 1 at the center of the screen.

<details><summary>métodos próprios (6) · herdados: 321</summary>

- `__init__(self, angle: 'float' = 0, width: 'float' = 0.35, length: 'float' = 0.35, fill_opacity: 'float' = 1.0, fill_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 0.0, tip_style: 'int' = 0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_angle(self) -> 'float'`
- `get_base(self) -> 'Vect3'`
- `get_length(self) -> 'float'`
- `get_tip_point(self) -> 'Vect3'`
- `get_vector(self) -> 'Vect3'`

</details>

### `Circle(start_angle: 'float' = 0, stroke_color: 'ManimColor' = '#FC6255', **kwargs)` ← Arc
> Creates a circle.

<details><summary>métodos próprios (4) · herdados: 337</summary>

- `__init__(self, start_angle: 'float' = 0, stroke_color: 'ManimColor' = '#FC6255', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_radius(self) -> 'float'`
- `point_at_angle(self, angle: 'float') -> 'Vect3'`
- `surround(self, mobject: 'Mobject', dim_to_match: 'int' = 0, stretch: 'bool' = False, buff: 'float' = 0.25) -> 'Self'`

</details>

### `CubicBezier(a0: 'Vect3', h0: 'Vect3', h1: 'Vect3', a1: 'Vect3', **kwargs)` ← VMobject
> Creates a cubic Bézier curve.

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, a0: 'Vect3', h0: 'Vect3', h1: 'Vect3', a1: 'Vect3', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `CurvedArrow(start_point: 'Vect3', end_point: 'Vect3', **kwargs)` ← ArcBetweenPoints
> Creates a curved arrow passing through the specified points with "angle" as the

<details><summary>métodos próprios (1) · herdados: 338</summary>

- `__init__(self, start_point: 'Vect3', end_point: 'Vect3', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `CurvedDoubleArrow(start_point: 'Vect3', end_point: 'Vect3', **kwargs)` ← CurvedArrow
> Creates a curved double arrow passing through the specified points with "angle" as the

<details><summary>métodos próprios (1) · herdados: 338</summary>

- `__init__(self, start_point: 'Vect3', end_point: 'Vect3', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `DashedLine(start: 'Vect3' = array([-1.,  0.,  0.]), end: 'Vect3' = array([1., 0., 0.]), dash_length: 'float' = 0.05, positive_space_ratio: 'float' = 0.5, **kwargs)` ← Line
> Creates a dashed line joining the points "start" and "end".

<details><summary>métodos próprios (7) · herdados: 342</summary>

- `__init__(self, start: 'Vect3' = array([-1.,  0.,  0.]), end: 'Vect3' = array([1., 0., 0.]), dash_length: 'float' = 0.05, positive_space_ratio: 'float' = 0.5, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `calculate_num_dashes(self, dash_length: 'float', positive_space_ratio: 'float') -> 'int'`
- `get_end(self) -> 'Vect3'`
- `get_first_handle(self) -> 'Vect3'`
- `get_last_handle(self) -> 'Vect3'`
- `get_start(self) -> 'Vect3'`
- `get_start_and_end(self) -> 'Tuple[Vect3, Vect3]'`

</details>

### `Dot(point: 'Vect3' = array([0., 0., 0.]), radius: 'float' = 0.08, stroke_color: 'ManimColor' = '#000000', stroke_width: 'float' = 0.0, fill_opacity: 'float' = 1.0, fill_color: 'ManimColor' = '#FFFFFF', **kwargs)` ← Circle
> Creates a dot. Dot is a filled white circle with no bounary and DEFAULT_DOT_RADIUS.

<details><summary>métodos próprios (1) · herdados: 340</summary>

- `__init__(self, point: 'Vect3' = array([0., 0., 0.]), radius: 'float' = 0.08, stroke_color: 'ManimColor' = '#000000', stroke_width: 'float' = 0.0, fill_opacity: 'float' = 1.0, fill_color: 'ManimColor' = '#FFFFFF', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Elbow(width: 'float' = 0.2, angle: 'float' = 0, **kwargs)` ← VMobject
> Creates an elbow. Elbow is an L-shaped shaped object.

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, width: 'float' = 0.2, angle: 'float' = 0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Ellipse(width: 'float' = 2.0, height: 'float' = 1.0, **kwargs)` ← Circle
> Creates an ellipse.

<details><summary>métodos próprios (1) · herdados: 340</summary>

- `__init__(self, width: 'float' = 2.0, height: 'float' = 1.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Line(start: 'Vect3 | Mobject' = array([-1.,  0.,  0.]), end: 'Vect3 | Mobject' = array([1., 0., 0.]), buff: 'float' = 0.0, path_arc: 'float' = 0.0, **kwargs)` ← TipableVMobject
> Creates a line joining the points "start" and "end".

<details><summary>métodos próprios (16) · herdados: 332</summary>

- `__init__(self, start: 'Vect3 | Mobject' = array([-1.,  0.,  0.]), end: 'Vect3 | Mobject' = array([1., 0., 0.]), buff: 'float' = 0.0, path_arc: 'float' = 0.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_angle(self) -> 'float'`
- `get_arc_length(self) -> 'float'`
- `get_projection(self, point: 'Vect3') -> 'Vect3'` — Return projection of a point onto the line
- `get_slope(self) -> 'float'`
- `get_unit_vector(self) -> 'Vect3'`
- `get_vector(self) -> 'Vect3'`
- `pointify(self, mob_or_point: 'Mobject | Vect3', direction: 'Vect3 | None' = None) -> 'Vect3'` — Take an argument passed into Line (or subclass) and turn
- `put_start_and_end_on(self, start: 'Vect3', end: 'Vect3') -> 'Self'`
- `reset_points_around_ends(self) -> 'Self'`
- `set_angle(self, angle: 'float', about_point: 'Optional[Vect3]' = None) -> 'Self'`
- `set_length(self, length: 'float', **kwargs)`
- `set_path_arc(self, path_arc: 'float') -> 'Self'`
- `set_perpendicular_to_camera(self, camera_frame)`
- `set_points_by_ends(self, start: 'Vect3', end: 'Vect3', buff: 'float' = 0, path_arc: 'float' = 0) -> 'Self'`
- `set_start_and_end_attrs(self, start: 'Vect3 | Mobject', end: 'Vect3 | Mobject')`

</details>

### `Polygon(*vertices: 'Vect3', **kwargs)` ← VMobject
> Creates a polygon by joining the specified vertices.

<details><summary>métodos próprios (3) · herdados: 319</summary>

- `__init__(self, *vertices: 'Vect3', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_vertices(self) -> 'Vect3Array'`
- `round_corners(self, radius: 'Optional[float]' = None) -> 'Self'`

</details>

### `Polyline(*vertices: 'Vect3', **kwargs)` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, *vertices: 'Vect3', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Rectangle(width: 'float' = 4.0, height: 'float' = 2.0, **kwargs)` ← Polygon
> Creates a rectangle at the center of the screen.

<details><summary>métodos próprios (2) · herdados: 320</summary>

- `__init__(self, width: 'float' = 4.0, height: 'float' = 2.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `surround(self, mobject, buff=0.1) -> 'Self'`

</details>

### `RegularPolygon(n: 'int' = 6, radius: 'float' = 1.0, start_angle: 'float | None' = None, **kwargs)` ← Polygon
> Creates a regular polygon of edge length 1 at the center of the screen.

<details><summary>métodos próprios (1) · herdados: 321</summary>

- `__init__(self, n: 'int' = 6, radius: 'float' = 1.0, start_angle: 'float | None' = None, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `RoundedRectangle(width: 'float' = 4.0, height: 'float' = 2.0, corner_radius: 'float' = 0.5, **kwargs)` ← Rectangle
> Creates a rectangle with round edges at the center of the screen.

<details><summary>métodos próprios (1) · herdados: 321</summary>

- `__init__(self, width: 'float' = 4.0, height: 'float' = 2.0, corner_radius: 'float' = 0.5, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Sector(angle: 'float' = 1.5707963267948966, radius: 'float' = 1.0, **kwargs)` ← AnnularSector
> Creates a sector.

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, angle: 'float' = 1.5707963267948966, radius: 'float' = 1.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `SmallDot(point: 'Vect3' = array([0., 0., 0.]), radius: 'float' = 0.04, **kwargs)` ← Dot
> Creates a small dot. Small dot is a filled white circle with no bounary and DEFAULT_SMALL_DOT_RADIUS.

<details><summary>métodos próprios (1) · herdados: 340</summary>

- `__init__(self, point: 'Vect3' = array([0., 0., 0.]), radius: 'float' = 0.04, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Square(side_length: 'float' = 2.0, **kwargs)` ← Rectangle
> Creates a square at the center of the screen.

<details><summary>métodos próprios (1) · herdados: 321</summary>

- `__init__(self, side_length: 'float' = 2.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `StrokeArrow(start: 'Vect3 | Mobject', end: 'Vect3 | Mobject', stroke_color: 'ManimColor' = '#BBBBBB', stroke_width: 'float' = 5, buff: 'float' = 0.25, tip_width_ratio: 'float' = 5, tip_len_to_width: 'float' = 0.0075, max_tip_length_to_length_ratio: 'float' = 0.3, max_width_to_length_ratio: 'float' = 8.0, **kwargs)` ← Line
> Creates a line joining the points "start" and "end".

<details><summary>métodos próprios (6) · herdados: 345</summary>

- `__init__(self, start: 'Vect3 | Mobject', end: 'Vect3 | Mobject', stroke_color: 'ManimColor' = '#BBBBBB', stroke_width: 'float' = 5, buff: 'float' = 0.25, tip_width_ratio: 'float' = 5, tip_len_to_width: 'float' = 0.0075, max_tip_length_to_length_ratio: 'float' = 0.3, max_width_to_length_ratio: 'float' = 8.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `create_tip_with_stroke_width(self) -> 'Self'`
- `insert_tip_anchor(self) -> 'Self'`
- `reset_tip(self) -> 'Self'`
- `set_points_by_ends(self, start: 'Vect3', end: 'Vect3', buff: 'float' = 0, path_arc: 'float' = 0) -> 'Self'`
- `set_stroke(self, color: 'ManimColor | Iterable[ManimColor] | None' = None, width: 'float | Iterable[float] | None' = None, *args, **kwargs) -> 'Self'`

</details>

### `TangentLine(vmob: 'VMobject', alpha: 'float', length: 'float' = 2, d_alpha: 'float' = 1e-06, **kwargs)` ← Line
> Creates a tangent line to the specified vectorized math object.

<details><summary>métodos próprios (1) · herdados: 347</summary>

- `__init__(self, vmob: 'VMobject', alpha: 'float', length: 'float' = 2, d_alpha: 'float' = 1e-06, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `TipableVMobject(color: 'ManimColor' = None, fill_color: 'ManimColor' = None, fill_opacity: 'float | Iterable[float] | None' = 0.0, stroke_color: 'ManimColor' = None, stroke_opacity: 'float | Iterable[float] | None' = 1.0, stroke_width: 'float | Iterable[float] | None' = 4.0, stroke_behind: 'bool' = False, background_image_file: 'str | None' = None, long_lines: 'bool' = False, joint_roundness: 'float' = 0.0, flat_stroke: 'bool' = False, stroke_width_in_scene_units: 'bool' = False, use_simple_quadratic_approx: 'bool' = False, anti_alias_width: 'float' = 1.5, fill_border_width: 'float' = 0.0, **kwargs)` ← VMobject
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (17) · herdados: 318</summary>

- `add_tip(self, at_start: 'bool' = False, **kwargs) -> 'Self'` — Adds a tip to the TipableVMobject instance, recognising
- `asign_tip_attr(self, tip: 'ArrowTip', at_start: 'bool') -> 'Self'`
- `create_tip(self, at_start: 'bool' = False, **kwargs) -> 'ArrowTip'` — Stylises the tip, positions it spacially, and returns
- `get_default_tip_length(self) -> 'float'`
- `get_end(self) -> 'Vect3'`
- `get_first_handle(self) -> 'Vect3'`
- `get_last_handle(self) -> 'Vect3'`
- `get_length(self) -> 'float'`
- `get_start(self) -> 'Vect3'`
- `get_tip(self) -> 'ArrowTip'` — Returns the TipableVMobject instance's (first) tip,
- `get_tips(self) -> 'VGroup'` — Returns a VGroup (collection of VMobjects) containing
- `get_unpositioned_tip(self, **kwargs) -> 'ArrowTip'` — Returns a tip that has been stylistically configured,
- `has_start_tip(self) -> 'bool'`
- `has_tip(self) -> 'bool'`
- `pop_tips(self) -> 'VGroup'`
- `position_tip(self, tip: 'ArrowTip', at_start: 'bool' = False) -> 'ArrowTip'`
- `reset_endpoints_based_on_tip(self, tip: 'ArrowTip', at_start: 'bool') -> 'Self'`

</details>

### `Triangle(**kwargs)` ← RegularPolygon
> Creates a triangle of edge length 1 at the center of the screen.

<details><summary>métodos próprios (1) · herdados: 321</summary>

- `__init__(self, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Vector(direction: 'Vect3' = array([1., 0., 0.]), buff: 'float' = 0.0, **kwargs)` ← Arrow
> Creates a vector. Vector is an arrow with start point as ORIGIN

<details><summary>métodos próprios (1) · herdados: 349</summary>

- `__init__(self, direction: 'Vect3' = array([1., 0., 0.]), buff: 'float' = 0.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

- `BLACK` = `'#000000'`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_WIDTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_LIGHT_COLOR` = `'#BBBBBB'`
- `DEFAULT_MOBJECT_COLOR` = `'#FFFFFF'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEG` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `MED_SMALL_BUFF` = `0.25`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `RED` = `'#FC6255'`
- `RIGHT` = `array([1., 0., 0.])`
- `SMALL_BUFF` = `0.1`
- `TAU` = `6.283185307179586`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`

## mobject/matrix

### `DecimalMatrix(matrix: 'FloatMatrixType', num_decimal_places: 'int' = 2, decimal_config: 'dict' = {}, **config)` ← Matrix
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 333</summary>

- `__init__(self, matrix: 'FloatMatrixType', num_decimal_places: 'int' = 2, decimal_config: 'dict' = {}, **config)` — Matrix can either include numbers, tex_strings,
- `element_to_mobject(self, element, **decimal_config) -> 'DecimalNumber'`

</details>

### `IntegerMatrix(matrix: 'FloatMatrixType', num_decimal_places: 'int' = 0, decimal_config: 'dict' = {}, **config)` ← DecimalMatrix
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 334</summary>

- `__init__(self, matrix: 'FloatMatrixType', num_decimal_places: 'int' = 0, decimal_config: 'dict' = {}, **config)` — Matrix can either include numbers, tex_strings,

</details>

### `Matrix(matrix: 'GenericMatrixType', v_buff: 'float' = 0.5, h_buff: 'float' = 0.5, bracket_h_buff: 'float' = 0.2, bracket_v_buff: 'float' = 0.25, height: 'float | None' = None, element_config: 'dict' = {}, element_alignment_corner: 'Vect3' = array([ 0., -1.,  0.]), ellipses_row: 'Optional[int]' = None, ellipses_col: 'Optional[int]' = None)` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (17) · herdados: 318</summary>

- `__init__(self, matrix: 'GenericMatrixType', v_buff: 'float' = 0.5, h_buff: 'float' = 0.5, bracket_h_buff: 'float' = 0.2, bracket_v_buff: 'float' = 0.25, height: 'float | None' = None, element_config: 'dict' = {}, element_alignment_corner: 'Vect3' = array([ 0., -1.,  0.]), ellipses_row: 'Optional[int]' = None, ellipses_col: 'Optional[int]' = None)` — Matrix can either include numbers, tex_strings,
- `add_background_to_entries(self) -> 'Self'`
- `copy(self, deep: 'bool' = False)` — A copy is a group of its own. Left pointing at what it was copied from, its fills
- `create_brackets(self, rows, v_buff: 'float', h_buff: 'float') -> 'VGroup'`
- `create_mobject_matrix(self, matrix: 'GenericMatrixType', v_buff: 'float', h_buff: 'float', aligned_corner: 'Vect3', **element_config) -> 'VMobjectMatrixType'` — Creates and organizes the matrix of mobjects
- `element_to_mobject(self, element, **config) -> 'VMobject'`
- `get_brackets(self) -> 'VGroup'`
- `get_column(self, index: 'int')`
- `get_columns(self) -> 'VGroup'`
- `get_ellipses(self) -> 'VGroup'`
- `get_entries(self) -> 'VGroup'`
- `get_mob_matrix(self) -> 'VMobjectMatrixType'`
- `get_row(self, index: 'int')`
- `get_rows(self) -> 'VGroup'`
- `set_column_colors(self, *colors: 'ManimColor') -> 'Self'`
- `swap_entries_for_ellipses(self, row_index: 'Optional[int]' = None, col_index: 'Optional[int]' = None, height_ratio: 'float' = 0.65, width_ratio: 'float' = 0.4)`
- `swap_entry_for_dots(self, entry, dots)`

</details>

### `MobjectMatrix(group: 'VGroup', n_rows: 'int | None' = None, n_cols: 'int | None' = None, height: 'float' = 4.0, element_alignment_corner=array([0., 0., 0.]), **config)` ← Matrix
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 333</summary>

- `__init__(self, group: 'VGroup', n_rows: 'int | None' = None, n_cols: 'int | None' = None, height: 'float' = 4.0, element_alignment_corner=array([0., 0., 0.]), **config)` — Matrix can either include numbers, tex_strings,
- `element_to_mobject(self, element: 'VMobject', **config) -> 'VMobject'`

</details>

### `TexMatrix(matrix: 'StringMatrixType', tex_config: 'dict' = {}, **config)` ← Matrix
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 334</summary>

- `__init__(self, matrix: 'StringMatrixType', tex_config: 'dict' = {}, **config)` — Matrix can either include numbers, tex_strings,

</details>

- `DEG` = `0.017453292519943295`
- `DOWN` = `array([ 0., -1.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `TYPE_CHECKING` = `False`

## mobject/svg

### `Brace(mobject: 'Mobject', direction: 'Vect3' = array([ 0., -1.,  0.]), buff: 'float' = 0.2, tex_string: 'str' = '\\underbrace{\\qquad}', **kwargs)` ← Tex
> An abstract base class for `Tex` and `MarkupText`

<details><summary>métodos próprios (7) · herdados: 372</summary>

- `__init__(self, mobject: 'Mobject', direction: 'Vect3' = array([ 0., -1.,  0.]), buff: 'float' = 0.2, tex_string: 'str' = '\\underbrace{\\qquad}', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_direction(self) -> 'np.ndarray'`
- `get_tex(self, *tex: 'str', **kwargs) -> 'Tex'`
- `get_text(self, text: 'str', **kwargs) -> 'Text'`
- `get_tip(self) -> 'np.ndarray'`
- `put_at_tip(self, mob: 'Mobject', use_next_to: 'bool' = True, **kwargs)`
- `set_initial_width(self, width: 'float')`

</details>

### `BraceLabel(obj: 'VMobject | list[VMobject]', text: 'str | Iterable[str]', brace_direction: 'np.ndarray' = array([ 0., -1.,  0.]), label_scale: 'float' = 1.0, label_buff: 'float' = 0.25, **kwargs) -> 'None'` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (6) · herdados: 318</summary>

- `__init__(self, obj: 'VMobject | list[VMobject]', text: 'str | Iterable[str]', brace_direction: 'np.ndarray' = array([ 0., -1.,  0.]), label_scale: 'float' = 1.0, label_buff: 'float' = 0.25, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `change_brace_label(self, obj: 'VMobject | list[VMobject]', *text: 'str')`
- `change_label(self, *text: 'str', **kwargs)`
- `copy(self)` — A copy is a group of its own. Left pointing at what it was copied from, its fills
- `creation_anim(self, label_anim: 'Animation' = <class 'manimlib.animation.fading.FadeIn'>, brace_anim: 'Animation' = <class 'manimlib.animation.growing.GrowFromCenter'>) -> 'AnimationGroup'`
- `shift_brace(self, obj: 'VMobject | list[VMobject]', **kwargs)`

</details>

### `BraceText(obj: 'VMobject | list[VMobject]', text: 'str | Iterable[str]', brace_direction: 'np.ndarray' = array([ 0., -1.,  0.]), label_scale: 'float' = 1.0, label_buff: 'float' = 0.25, **kwargs) -> 'None'` ← BraceLabel
> Mathematical Object

### `Bubble(content: 'str | VMobject | None' = None, buff: 'float' = 1.0, filler_shape: 'Tuple[float, float]' = (3.0, 2.0), pin_point: 'Vect3 | None' = None, direction: 'Vect3' = array([-1.,  0.,  0.]), add_content: 'bool' = True, fill_color: 'ManimColor' = '#000000', fill_opacity: 'float' = 0.8, stroke_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 3.0, **kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (12) · herdados: 317</summary>

- `__init__(self, content: 'str | VMobject | None' = None, buff: 'float' = 1.0, filler_shape: 'Tuple[float, float]' = (3.0, 2.0), pin_point: 'Vect3 | None' = None, direction: 'Vect3' = array([-1.,  0.,  0.]), add_content: 'bool' = True, fill_color: 'ManimColor' = '#000000', fill_opacity: 'float' = 0.8, stroke_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 3.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_content(self, mobject)`
- `clear(self)`
- `flip(self, axis=array([0., 1., 0.]), only_body=True, **kwargs)`
- `get_body(self, content: 'VMobject', direction: 'Vect3', buff: 'float') -> 'VMobject'`
- `get_bubble_center(self)`
- `get_tip(self)`
- `move_tip_to(self, point)`
- `pin_to(self, mobject, auto_flip=False)`
- `position_mobject_inside(self, mobject, buff=0.5)`
- `resize_to_content(self, buff=1.0)`
- `write(self, text)`

</details>

### `BulletedList(*items: 'str', buff: 'float' = 0.5, aligned_edge: 'Vect3' = array([-1.,  0.,  0.]), numbered: 'bool' = False, **kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 319</summary>

- `__init__(self, *items: 'str', buff: 'float' = 0.5, aligned_edge: 'Vect3' = array([-1.,  0.,  0.]), numbered: 'bool' = False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `fade_all_but(self, index: 'int', opacity: 'float' = 0.25, scale_factor=0.7) -> 'None'`

</details>

### `Checkmark(**kwargs)` ← TexTextFromPresetString
> An abstract base class for `Tex` and `MarkupText`

### `Clock(stroke_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 3.0, hour_hand_height: 'float' = 0.3, minute_hand_height: 'float' = 0.6, tick_length: 'float' = 0.1, **kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, stroke_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 3.0, hour_hand_height: 'float' = 0.3, minute_hand_height: 'float' = 0.6, tick_length: 'float' = 0.1, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ClockPassesTime(clock: 'Clock', run_time: 'float' = 5.0, hours_passed: 'float' = 12.0, rate_func: 'Callable[[float], float]' = <function linear at 0x7f6ff3932de0>, **kwargs)` ← AnimationGroup

<details><summary>métodos próprios (1) · herdados: 26</summary>

- `__init__(self, clock: 'Clock', run_time: 'float' = 5.0, hours_passed: 'float' = 12.0, rate_func: 'Callable[[float], float]' = <function linear at 0x7f6ff3932de0>, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Code(code: 'str', font: 'str' = 'Consolas', font_size: 'int' = 24, lsh: 'float' = 1.0, fill_color: 'ManimColor' = None, stroke_color: 'ManimColor' = None, language: 'str' = 'python', code_style: 'str' = 'monokai', **kwargs)` ← MarkupText
> An abstract base class for `Tex` and `MarkupText`

<details><summary>métodos próprios (1) · herdados: 373</summary>

- `__init__(self, code: 'str', font: 'str' = 'Consolas', font_size: 'int' = 24, lsh: 'float' = 1.0, fill_color: 'ManimColor' = None, stroke_color: 'ManimColor' = None, language: 'str' = 'python', code_style: 'str' = 'monokai', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Dartboard(**kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `DieFace(value: 'int', side_length: 'float' = 1.0, corner_radius: 'float' = 0.15, stroke_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 2.0, fill_color: 'ManimColor' = '#222222', dot_radius: 'float' = 0.08, dot_color: 'ManimColor' = '#FFFFFF', dot_coalesce_factor: 'float' = 0.5)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, value: 'int', side_length: 'float' = 1.0, corner_radius: 'float' = 0.15, stroke_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 2.0, fill_color: 'ManimColor' = '#222222', dot_radius: 'float' = 0.08, dot_color: 'ManimColor' = '#FFFFFF', dot_coalesce_factor: 'float' = 0.5)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `DoubleSpeechBubble(content: 'str | VMobject | None' = None, buff: 'float' = 1.0, filler_shape: 'Tuple[float, float]' = (3.0, 2.0), pin_point: 'Vect3 | None' = None, direction: 'Vect3' = array([-1.,  0.,  0.]), add_content: 'bool' = True, fill_color: 'ManimColor' = '#000000', fill_opacity: 'float' = 0.8, stroke_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 3.0, **kwargs)` ← Bubble
> Mathematical Object

### `Exmark(**kwargs)` ← TexTextFromPresetString
> An abstract base class for `Tex` and `MarkupText`

### `Laptop(width: 'float' = 3, body_dimensions: 'Tuple[float, float, float]' = (4.0, 3.0, 0.05), screen_thickness: 'float' = 0.01, keyboard_width_to_body_width: 'float' = 0.9, keyboard_height_to_body_height: 'float' = 0.5, screen_width_to_screen_plate_width: 'float' = 0.9, key_color_kwargs: 'dict' = {'stroke_width': 0, 'fill_color': '#000000', 'fill_opacity': 1}, fill_opacity: 'float' = 1.0, stroke_width: 'float' = 0.0, body_color: 'ManimColor' = '#BBBBBB', shaded_body_color: 'ManimColor' = '#888888', open_angle: 'float' = 0.7853981633974483, **kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, width: 'float' = 3, body_dimensions: 'Tuple[float, float, float]' = (4.0, 3.0, 0.05), screen_thickness: 'float' = 0.01, keyboard_width_to_body_width: 'float' = 0.9, keyboard_height_to_body_height: 'float' = 0.5, screen_width_to_screen_plate_width: 'float' = 0.9, key_color_kwargs: 'dict' = {'stroke_width': 0, 'fill_color': '#000000', 'fill_opacity': 1}, fill_opacity: 'float' = 1.0, stroke_width: 'float' = 0.0, body_color: 'ManimColor' = '#BBBBBB', shaded_body_color: 'ManimColor' = '#888888', open_angle: 'float' = 0.7853981633974483, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Lightbulb(height: 'float' = 1.0, color: 'ManimColor' = '#FFFF00', stroke_width: 'float' = 3.0, fill_opacity: 'float' = 0.0, **kwargs)` ← SVGMobject
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 335</summary>

- `__init__(self, height: 'float' = 1.0, color: 'ManimColor' = '#FFFF00', stroke_width: 'float' = 3.0, fill_opacity: 'float' = 0.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `LineBrace(line: 'Line', direction=array([0., 1., 0.]), **kwargs)` ← Brace
> An abstract base class for `Tex` and `MarkupText`

<details><summary>métodos próprios (1) · herdados: 378</summary>

- `__init__(self, line: 'Line', direction=array([0., 1., 0.]), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `MarkupText(text: 'str', font_size: 'int' = 48, height: 'float | None' = None, justify: 'bool' = False, indent: 'float' = 0, alignment: 'str' = '', line_width: 'float | None' = None, font: 'str' = '', slant: 'str' = 'NORMAL', weight: 'str' = 'NORMAL', gradient: 'Iterable[ManimColor] | None' = None, line_spacing_height: 'float | None' = None, text2color: 'dict' = {}, text2font: 'dict' = {}, text2gradient: 'dict' = {}, text2slant: 'dict' = {}, text2weight: 'dict' = {}, lsh: 'float | None' = None, t2c: 'dict' = {}, t2f: 'dict' = {}, t2g: 'dict' = {}, t2s: 'dict' = {}, t2w: 'dict' = {}, global_config: 'dict' = {}, local_configs: 'dict' = {}, disable_ligatures: 'bool' = True, isolate: 'Selector' = re.compile('\\w+'), **kwargs)` ← StringMobject
> An abstract base class for `Tex` and `MarkupText`

<details><summary>métodos próprios (17) · herdados: 357</summary>

- `__init__(self, text: 'str', font_size: 'int' = 48, height: 'float | None' = None, justify: 'bool' = False, indent: 'float' = 0, alignment: 'str' = '', line_width: 'float | None' = None, font: 'str' = '', slant: 'str' = 'NORMAL', weight: 'str' = 'NORMAL', gradient: 'Iterable[ManimColor] | None' = None, line_spacing_height: 'float | None' = None, text2color: 'dict' = {}, text2font: 'dict' = {}, text2gradient: 'dict' = {}, text2slant: 'dict' = {}, text2weight: 'dict' = {}, lsh: 'float | None' = None, t2c: 'dict' = {}, t2f: 'dict' = {}, t2g: 'dict' = {}, t2s: 'dict' = {}, t2w: 'dict' = {}, global_config: 'dict' = {}, local_configs: 'dict' = {}, disable_ligatures: 'bool' = True, isolate: 'Selector' = re.compile('\\w+'), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `escape_markup_char(substr: 'str') -> 'str'`
- `get_attr_dict_from_command_pair(open_command: 're.Match', close_command: 're.Match') -> 'dict[str, str] | None'`
- `get_command_flag(match_obj: 're.Match') -> 'int'`
- `get_command_matches(string: 'str') -> 'list[re.Match]'`
- `get_command_string(attr_dict: 'dict[str, str]', is_end: 'bool', label_hex: 'str | None') -> 'str'`
- `get_configured_items(self) -> 'list[tuple[Span, dict[str, str]]]'`
- `get_content_prefix_and_suffix(self, is_labelled: 'bool') -> 'tuple[str, str]'`
- `get_part_by_text(self, selector: 'Selector', **kwargs) -> 'VGroup'`
- `get_parts_by_text(self, selector: 'Selector') -> 'VGroup'`
- `get_svg_string_by_content(self, content: 'str') -> 'str'`
- `get_text(self) -> 'str'`
- `replace_for_content(match_obj: 're.Match') -> 'str'`
- `replace_for_matching(match_obj: 're.Match') -> 'str'`
- `set_color_by_text(self, selector: 'Selector', color: 'ManimColor')`
- `set_color_by_text_to_color_map(self, color_map: 'dict[Selector, ManimColor]')`
- `unescape_markup_char(substr: 'str') -> 'str'`

</details>

### `OldSpeechBubble(content: 'str | VMobject | None' = None, buff: 'float' = 1.0, filler_shape: 'Tuple[float, float]' = (3.0, 2.0), pin_point: 'Vect3 | None' = None, direction: 'Vect3' = array([-1.,  0.,  0.]), add_content: 'bool' = True, fill_color: 'ManimColor' = '#000000', fill_opacity: 'float' = 0.8, stroke_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 3.0, **kwargs)` ← Bubble
> Mathematical Object

### `OldTex(*tex_strings: 'str', arg_separator: 'str' = '', isolate: 'List[str]' = [], tex_to_color_map: 'Dict[str, ManimColor]' = {}, **kwargs)` ← SingleStringTex
> Mathematical Object

<details><summary>métodos próprios (12) · herdados: 342</summary>

- `__init__(self, *tex_strings: 'str', arg_separator: 'str' = '', isolate: 'List[str]' = [], tex_to_color_map: 'Dict[str, ManimColor]' = {}, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `break_up_by_substrings(self, tex_strings: 'Iterable[str]')` — Reorganize existing submojects one layer
- `break_up_tex_strings(self, tex_strings: 'Iterable[str]', substrings_to_isolate: 'List[str]' = []) -> 'Iterable[str]'`
- `get_part_by_tex(self, tex: 'str', **kwargs) -> 'SingleStringTex | None'`
- `get_parts_by_tex(self, tex: 'str', substring: 'bool' = True, case_sensitive: 'bool' = True) -> 'VGroup'`
- `index_of_part(self, part: 'SingleStringTex', start: 'int' = 0) -> 'int'`
- `index_of_part_by_tex(self, tex: 'str', start: 'int' = 0, **kwargs) -> 'int'`
- `set_bstroke(self, color: 'ManimColor' = '#000000', width: 'float' = 4)`
- `set_color_by_tex(self, tex: 'str', color: 'ManimColor', **kwargs)`
- `set_color_by_tex_to_color_map(self, tex_to_color_map: 'dict[str, ManimColor]', **kwargs)`
- `slice_by_tex(self, start_tex: 'str | None' = None, stop_tex: 'str | None' = None, **kwargs) -> 'VGroup'`
- `sort_alphabetically(self) -> 'None'`

</details>

### `OldTexText(*tex_strings: 'str', math_mode: 'bool' = False, arg_separator: 'str' = '', **kwargs)` ← OldTex
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 353</summary>

- `__init__(self, *tex_strings: 'str', math_mode: 'bool' = False, arg_separator: 'str' = '', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OldThoughtBubble(content: 'str | VMobject | None' = None, buff: 'float' = 1.0, filler_shape: 'Tuple[float, float]' = (3.0, 2.0), pin_point: 'Vect3 | None' = None, direction: 'Vect3' = array([-1.,  0.,  0.]), add_content: 'bool' = True, fill_color: 'ManimColor' = '#000000', fill_opacity: 'float' = 0.8, stroke_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 3.0, **kwargs)` ← Bubble
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 328</summary>

- `get_body(self, content: 'VMobject', direction: 'Vect3', buff: 'float') -> 'VMobject'`
- `make_green_screen(self)`

</details>

### `Piano(n_white_keys=52, black_pattern=[0, 2, 3, 5, 6], white_keys_per_octave=7, white_key_dims=(0.15, 1.0), black_key_dims=(0.1, 0.66), key_buff=0.02, white_key_color='#FFFFFF', black_key_color='#222222', total_width=13, **kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (4) · herdados: 319</summary>

- `__init__(self, n_white_keys=52, black_pattern=[0, 2, 3, 5, 6], white_keys_per_octave=7, white_key_dims=(0.15, 1.0), black_key_dims=(0.1, 0.66), key_buff=0.02, white_key_color='#FFFFFF', black_key_color='#222222', total_width=13, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_black_keys(self)`
- `add_white_keys(self)`
- `sort_keys(self)`

</details>

### `Piano3D(shading: 'Tuple[float, float, float]' = (1.0, 0.2, 0.2), stroke_width: 'float' = 0.25, stroke_color: 'ManimColor' = '#000000', key_depth: 'float' = 0.1, black_key_shift: 'float' = 0.05, piano_2d_config: 'dict' = {'white_key_color': '#DDDDDD', 'key_buff': 0.001}, **kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, shading: 'Tuple[float, float, float]' = (1.0, 0.2, 0.2), stroke_width: 'float' = 0.25, stroke_color: 'ManimColor' = '#000000', key_depth: 'float' = 0.1, black_key_shift: 'float' = 0.05, piano_2d_config: 'dict' = {'white_key_color': '#DDDDDD', 'key_buff': 0.001}, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `SVGMobject(file_name: 'str' = '', svg_string: 'str' = '', should_center: 'bool' = True, height: 'float | None' = None, width: 'float | None' = None, color: 'ManimColor' = None, fill_color: 'ManimColor' = None, fill_opacity: 'float | None' = None, stroke_width: 'float | None' = None, stroke_color: 'ManimColor' = None, stroke_opacity: 'float | None' = None, svg_default: 'dict' = {'color': None, 'opacity': None, 'fill_color': None, 'fill_opacity': None, 'stroke_width': None, 'stroke_color': None, 'stroke_opacity': None}, path_string_config: 'dict' = {}, **kwargs)` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (17) · herdados: 319</summary>

- `__init__(self, file_name: 'str' = '', svg_string: 'str' = '', should_center: 'bool' = True, height: 'float | None' = None, width: 'float | None' = None, color: 'ManimColor' = None, fill_color: 'ManimColor' = None, fill_opacity: 'float | None' = None, stroke_width: 'float | None' = None, stroke_color: 'ManimColor' = None, stroke_opacity: 'float | None' = None, svg_default: 'dict' = {'color': None, 'opacity': None, 'fill_color': None, 'fill_opacity': None, 'stroke_width': None, 'stroke_color': None, 'stroke_opacity': None}, path_string_config: 'dict' = {}, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `apply_style_to_mobject(mob: 'VMobject', shape: 'se.GraphicObject') -> 'VMobject'`
- `ellipse_to_mobject(self, ellipse: 'se.Circle | se.Ellipse') -> 'Circle'`
- `file_name_to_svg_string(self, file_name: 'str') -> 'str'`
- `generate_config_style_dict(self) -> 'dict[str, str]'`
- `handle_transform(mob: 'VMobject', matrix: 'se.Matrix') -> 'VMobject'`
- `init_svg_mobject(self) -> 'None'`
- `line_to_mobject(self, line: 'se.SimpleLine') -> 'Line'`
- `mobjects_from_svg(self, svg: 'se.SVG') -> 'list[VMobject]'`
- `mobjects_from_svg_string(self, svg_string: 'str') -> 'list[VMobject]'`
- `modify_xml_tree(self, element_tree: 'ET.ElementTree') -> 'ET.ElementTree'`
- `path_to_mobject(self, path: 'se.Path', svg: 'se.SVG') -> 'VMobjectFromSVGPath'`
- `polygon_to_mobject(self, polygon: 'se.Polygon') -> 'Polygon'`
- `polyline_to_mobject(self, polyline: 'se.Polyline') -> 'Polyline'`
- `rect_to_mobject(self, rect: 'se.Rect') -> 'Rectangle'`
- `scale_stroke_widths(self, factor: 'float') -> 'None'`
- `text_to_mobject(self, text: 'se.Text')`

</details>

### `SingleStringTex(tex_string: 'str', height: 'float | None' = None, fill_color: 'ManimColor' = '#FFFFFF', fill_opacity: 'float' = 1.0, stroke_width: 'float' = 0, svg_default: 'dict' = {'fill_color': '#FFFFFF'}, path_string_config: 'dict' = {}, font_size: 'int' = 48, alignment: 'str' = '\\centering', math_mode: 'bool' = True, organize_left_to_right: 'bool' = False, template: 'str' = '', additional_preamble: 'str' = '', **kwargs)` ← SVGMobject
> Mathematical Object

<details><summary>métodos próprios (8) · herdados: 335</summary>

- `__init__(self, tex_string: 'str', height: 'float | None' = None, fill_color: 'ManimColor' = '#FFFFFF', fill_opacity: 'float' = 1.0, stroke_width: 'float' = 0, svg_default: 'dict' = {'fill_color': '#FFFFFF'}, path_string_config: 'dict' = {}, font_size: 'int' = 48, alignment: 'str' = '\\centering', math_mode: 'bool' = True, organize_left_to_right: 'bool' = False, template: 'str' = '', additional_preamble: 'str' = '', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `balance_braces(self, tex: 'str') -> 'str'` — Makes Tex resiliant to unmatched braces
- `get_modified_expression(self, tex_string: 'str') -> 'str'`
- `get_svg_string_by_content(self, content: 'str') -> 'str'`
- `get_tex(self) -> 'str'`
- `get_tex_file_body(self, tex_string: 'str') -> 'str'`
- `modify_special_strings(self, tex: 'str') -> 'str'`
- `organize_submobjects_left_to_right(self)`

</details>

### `SpeechBubble(content: 'str | VMobject | None' = None, buff: 'float' = 0.25, filler_shape: 'Tuple[float, float]' = (2.0, 1.0), stem_height_to_bubble_height: 'float' = 0.5, stem_top_x_props: 'Tuple[float, float]' = (0.2, 0.3), **kwargs)` ← Bubble
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 327</summary>

- `__init__(self, content: 'str | VMobject | None' = None, buff: 'float' = 0.25, filler_shape: 'Tuple[float, float]' = (2.0, 1.0), stem_height_to_bubble_height: 'float' = 0.5, stem_top_x_props: 'Tuple[float, float]' = (0.2, 0.3), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_body(self, content: 'VMobject', direction: 'Vect3', buff: 'float') -> 'VMobject'`

</details>

### `Speedometer(arc_angle: 'float' = 4.1887902047863905, num_ticks: 'int' = 8, tick_length: 'float' = 0.2, needle_width: 'float' = 0.1, needle_height: 'float' = 0.8, needle_color: 'ManimColor' = '#FFFF00', **kwargs)` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (6) · herdados: 318</summary>

- `__init__(self, arc_angle: 'float' = 4.1887902047863905, num_ticks: 'int' = 8, tick_length: 'float' = 0.2, needle_width: 'float' = 0.1, needle_height: 'float' = 0.8, needle_color: 'ManimColor' = '#FFFF00', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_center(self)`
- `get_needle_angle(self)`
- `get_needle_tip(self)`
- `move_needle_to_velocity(self, velocity)`
- `rotate_needle(self, angle)`

</details>

### `StringMobject(string: 'str', fill_color: 'ManimColor' = '#FFFFFF', fill_border_width: 'float' = 0.5, stroke_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 0, base_color: 'ManimColor' = '#FFFFFF', isolate: 'Selector' = (), protect: 'Selector' = (), use_labelled_svg: 'bool' = False, **kwargs)` ← SVGMobject, ABC
> An abstract base class for `Tex` and `MarkupText`

<details><summary>métodos próprios (33) · herdados: 334</summary>

- `__init__(self, string: 'str', fill_color: 'ManimColor' = '#FFFFFF', fill_border_width: 'float' = 0.5, stroke_color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 0, base_color: 'ManimColor' = '#FFFFFF', isolate: 'Selector' = (), protect: 'Selector' = (), use_labelled_svg: 'bool' = False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `assign_labels_by_color(self, mobjects: 'list[VMobject]') -> 'None'` — Assuming each mobject in the list `mobjects` has a fill color
- `build_groups(self) -> 'VGroup'`
- `build_parts_from_indices_lists(self, indices_lists: 'list[list[int]]') -> 'VGroup'`
- `find_spans_by_selector(self, selector: 'Selector') -> 'list[Span]'`
- `get_attr_dict_from_command_pair(open_command: 're.Match', close_command: 're.Match') -> 'dict[str, str] | None'`
- `get_command_flag(match_obj: 're.Match') -> 'int'`
- `get_command_matches(string: 'str') -> 'list[re.Match]'`
- `get_command_string(attr_dict: 'dict[str, str]', is_end: 'bool', label_hex: 'str | None') -> 'str'`
- `get_configured_items(self) -> 'list[tuple[Span, dict[str, str]]]'`
- `get_content(self, is_labelled: 'bool') -> 'str'`
- `get_content_prefix_and_suffix(self, is_labelled: 'bool') -> 'tuple[str, str]'`
- `get_group_part_items(self) -> 'list[tuple[str, list[int]]]'`
- `get_specified_part_items(self) -> 'list[tuple[str, list[int]]]'`
- `get_specified_substrings(self) -> 'list[str]'`
- `get_string(self) -> 'str'`
- `get_submob_indices_list_by_span(self, arbitrary_span: 'Span') -> 'list[int]'`
- `get_submob_indices_lists_by_selector(self, selector: 'Selector') -> 'list[list[int]]'`
- `get_svg_string(self, is_labelled: 'bool' = False) -> 'str'`
- `get_svg_string_by_content(self, content: 'str') -> 'str'`
- `get_symbol_substrings(self)`
- `mobjects_from_svg_string(self, svg_string: 'str') -> 'list[VMobject]'`
- `parse(self) -> 'None'`
- `rearrange_submobjects_by_positions(self, labelled_submobs: 'list[VMobject]', unlabelled_submobs: 'list[VMobject]') -> 'None'` — Rearrange `labeleled_submobjects` so that each submobject
- `replace_for_content(match_obj: 're.Match') -> 'str'`
- `replace_for_matching(match_obj: 're.Match') -> 'str'`
- `select_part(self, selector: 'Selector', index: 'int' = 0) -> 'VMobject'`
- `select_parts(self, selector: 'Selector') -> 'VGroup'`
- `select_unisolated_substring(self, pattern: 'str | re.Pattern') -> 'VGroup'`
- `set_parts_color(self, selector: 'Selector', color: 'ManimColor')`
- `set_parts_color_by_dict(self, color_map: 'dict[Selector, ManimColor]')`
- `span_contains(span_0: 'Span', span_1: 'Span') -> 'bool'`
- `substr_to_path_count(self, substr: 'str') -> 'int'`

</details>

### `Tex(*tex_strings: 'str', font_size: 'int' = 48, alignment: 'str' = '\\centering', template: 'str' = '', additional_preamble: 'str' = '', tex_to_color_map: 'dict' = {}, t2c: 'dict' = {}, isolate: 'Selector' = [], use_labelled_svg: 'bool' = True, **kwargs)` ← StringMobject
> An abstract base class for `Tex` and `MarkupText`

<details><summary>métodos próprios (19) · herdados: 355</summary>

- `__init__(self, *tex_strings: 'str', font_size: 'int' = 48, alignment: 'str' = '\\centering', template: 'str' = '', additional_preamble: 'str' = '', tex_to_color_map: 'dict' = {}, t2c: 'dict' = {}, isolate: 'Selector' = [], use_labelled_svg: 'bool' = True, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_attr_dict_from_command_pair(open_command: 're.Match', close_command: 're.Match') -> 'dict[str, str] | None'`
- `get_color_command(rgb_hex: 'str') -> 'str'`
- `get_command_flag(match_obj: 're.Match') -> 'int'`
- `get_command_matches(string: 'str') -> 'list[re.Match]'`
- `get_command_string(attr_dict: 'dict[str, str]', is_end: 'bool', label_hex: 'str | None') -> 'str'`
- `get_configured_items(self) -> 'list[tuple[Span, dict[str, str]]]'`
- `get_content_prefix_and_suffix(self, is_labelled: 'bool') -> 'tuple[str, str]'`
- `get_part_by_tex(self, selector: 'Selector', index: 'int' = 0) -> 'VMobject'`
- `get_parts_by_tex(self, selector: 'Selector') -> 'VGroup'`
- `get_svg_string_by_content(self, content: 'str') -> 'str'`
- `get_symbol_substrings(self)`
- `get_tex(self) -> 'str'`
- `make_number_changeable(self, value: 'float | int | str', index: 'int' = 0, replace_all: 'bool' = False, **config) -> 'VMobject'`
- `replace_for_content(match_obj: 're.Match') -> 'str'`
- `replace_for_matching(match_obj: 're.Match') -> 'str'`
- `set_color_by_tex(self, selector: 'Selector', color: 'ManimColor')`
- `set_color_by_tex_to_color_map(self, color_map: 'dict[Selector, ManimColor]')`
- `substr_to_path_count(self, substr: 'str') -> 'int'`

</details>

### `TexText(*tex_strings: 'str', font_size: 'int' = 48, alignment: 'str' = '\\centering', template: 'str' = '', additional_preamble: 'str' = '', tex_to_color_map: 'dict' = {}, t2c: 'dict' = {}, isolate: 'Selector' = [], use_labelled_svg: 'bool' = True, **kwargs)` ← Tex
> An abstract base class for `Tex` and `MarkupText`

### `TexTextFromPresetString(**kwargs)` ← TexText
> An abstract base class for `Tex` and `MarkupText`

<details><summary>métodos próprios (1) · herdados: 373</summary>

- `__init__(self, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Text(text: 'str', isolate: 'Selector' = (re.compile('\\w+'), re.compile('\\S+')), use_labelled_svg: 'bool' = True, path_string_config: 'dict' = {'use_simple_quadratic_approx': True}, **kwargs)` ← MarkupText
> An abstract base class for `Tex` and `MarkupText`

<details><summary>métodos próprios (5) · herdados: 369</summary>

- `__init__(self, text: 'str', isolate: 'Selector' = (re.compile('\\w+'), re.compile('\\S+')), use_labelled_svg: 'bool' = True, path_string_config: 'dict' = {'use_simple_quadratic_approx': True}, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_command_flag(match_obj: 're.Match') -> 'int'`
- `get_command_matches(string: 'str') -> 'list[re.Match]'`
- `replace_for_content(match_obj: 're.Match') -> 'str'`
- `replace_for_matching(match_obj: 're.Match') -> 'str'`

</details>

### `ThoughtBubble(content: 'str | VMobject | None' = None, buff: 'float' = 0.1, filler_shape: 'Tuple[float, float]' = (2.0, 1.0), bulge_radius: 'float' = 0.35, bulge_overlap: 'float' = 0.25, noise_factor: 'float' = 0.1, circle_radii: 'list[float]' = [0.1, 0.15, 0.2], **kwargs)` ← Bubble
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 327</summary>

- `__init__(self, content: 'str | VMobject | None' = None, buff: 'float' = 0.1, filler_shape: 'Tuple[float, float]' = (2.0, 1.0), bulge_radius: 'float' = 0.35, bulge_overlap: 'float' = 0.25, noise_factor: 'float' = 0.1, circle_radii: 'list[float]' = [0.1, 0.15, 0.2], **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_body(self, content: 'VMobject', direction: 'Vect3', buff: 'float') -> 'VMobject'`

</details>

### `Title(*text_parts: 'str', font_size: 'int' = 72, include_underline: 'bool' = True, underline_width: 'float' = 12.222222222222221, match_underline_width_to_text: 'bool' = False, underline_buff: 'float' = 0.1, underline_style: 'dict' = {'stroke_width': 2, 'stroke_color': '#888888'}, **kwargs)` ← TexText
> An abstract base class for `Tex` and `MarkupText`

<details><summary>métodos próprios (1) · herdados: 373</summary>

- `__init__(self, *text_parts: 'str', font_size: 'int' = 72, include_underline: 'bool' = True, underline_width: 'float' = 12.222222222222221, match_underline_width_to_text: 'bool' = False, underline_buff: 'float' = 0.1, underline_style: 'dict' = {'stroke_width': 2, 'stroke_color': '#888888'}, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `VMobjectFromSVGPath(path_obj: 'se.Path', **kwargs)` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (4) · herdados: 318</summary>

- `__init__(self, path_obj: 'se.Path', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `handle_arc(self, arc: 'se.Arc') -> 'None'`
- `handle_commands(self) -> 'None'`
- `init_points(self) -> 'None'`

</details>

### `VectorizedEarth(height: 'float' = 2.0, **kwargs)` ← SVGMobject
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 335</summary>

- `__init__(self, height: 'float' = 2.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `VideoIcon(width: 'float' = 1.2, color='#C7E9F1', **kwargs)` ← SVGMobject
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 335</summary>

- `__init__(self, width: 'float' = 1.2, color='#C7E9F1', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `VideoSeries(num_videos: 'int' = 11, gradient_colors: 'Sequence[ManimColor]' = ['#9CDCEB', '#29ABCA'], width: 'float' = 13.722222222222221, **kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (1) · herdados: 319</summary>

- `__init__(self, num_videos: 'int' = 11, gradient_colors: 'Sequence[ManimColor]' = ['#9CDCEB', '#29ABCA'], width: 'float' = 13.722222222222221, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

- `BLACK` = `'#000000'`
- `BLACK` = `'#000000'`
- `BLUE_A` = `'#C7E9F1'`
- `BLUE_B` = `'#9CDCEB'`
- `BLUE_C` = `'#58C4DD'`
- `BLUE_D` = `'#29ABCA'`
- `DEFAULT_CANVAS_HEIGHT` = `16384`
- `DEFAULT_CANVAS_WIDTH` = `16384`
- `DEFAULT_LINE_SPACING_SCALE` = `0.6`
- `DEFAULT_MOBJECT_COLOR` = `'#FFFFFF'`
- `DEFAULT_MOBJECT_COLOR` = `'#FFFFFF'`
- `DEFAULT_MOBJECT_COLOR` = `'#FFFFFF'`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFF` = `0.25`
- `DEFAULT_PIXEL_WIDTH` = `1920`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `FRAME_WIDTH` = `14.222222222222221`
- `FRAME_WIDTH` = `14.222222222222221`
- `FRAME_WIDTH` = `14.222222222222221`
- `GREEN` = `'#83C167'`
- `GREEN_E` = `'#699C52'`
- `GREEN_SCREEN` = `'#00FF00'`
- `GREY` = `'#888888'`
- `GREY_A` = `'#DDDDDD'`
- `GREY_B` = `'#BBBBBB'`
- `GREY_C` = `'#888888'`
- `GREY_E` = `'#222222'`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `PATH_TO_POINTS` = `{}`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `RED` = `'#FC6255'`
- `RED_E` = `'#CF5044'`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `STROKE_WIDTHS_PER_UNIT` = `100.0`
- `SVG_HASH_TO_MOB_MAP` = `{}`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `WHITE` = `'#FFFFFF'`
- `YELLOW` = `'#FFFF00'`
- **`get_svg_content_height(svg_string: 'str') -> 'float'`**
- **`register_font(font_file: 'str | Path')`** — Temporarily add a font file to Pango's search path.

## mobject/value_tracker

### `ComplexValueTracker(value: 'float | complex | np.ndarray' = 0, **kwargs)` ← ValueTracker
> Not meant to be displayed.  Instead the position encodes some

### `ExponentialValueTracker(value: 'float | complex | np.ndarray' = 0, **kwargs)` ← ValueTracker
> Operates just like ValueTracker, except it encodes the value as the

<details><summary>métodos próprios (2) · herdados: 234</summary>

- `get_value(self) -> 'float | complex'`
- `set_value(self, value: 'float | complex')`

</details>

### `ValueTracker(value: 'float | complex | np.ndarray' = 0, **kwargs)` ← Mobject
> Not meant to be displayed.  Instead the position encodes some

<details><summary>métodos próprios (6) · herdados: 230</summary>

- `__init__(self, value: 'float | complex | np.ndarray' = 0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `become(self, mobject: 'ValueTracker', match_updaters: 'bool' = False) -> 'Self'` — Edit all data and submobjects to be idential
- `get_value(self) -> 'float | complex | np.ndarray'`
- `increment_value(self, d_value: 'float | complex') -> 'None'`
- `interpolate(self, mobject1: 'ValueTracker', mobject2: 'ValueTracker', alpha: 'float', path_func: 'Callable[[np.ndarray, np.ndarray, float], np.ndarray]' = <function straight_path at 0x7f6ff3b247c0>) -> 'Self'`
- `set_value(self, value: 'float | complex | np.ndarray') -> 'Self'`

</details>

- `TYPE_CHECKING` = `False`

## mobject/vector_field

### `AnimatedStreamLines(stream_lines: 'StreamLines', lag_range: 'float' = 4, rate_multiple: 'float' = 1.0, line_anim_config: 'dict' = {'rate_func': <function linear at 0x7f6ff3932de0>, 'time_width': 1.0}, **kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 318</summary>

- `__init__(self, stream_lines: 'StreamLines', lag_range: 'float' = 4, rate_multiple: 'float' = 1.0, line_anim_config: 'dict' = {'rate_func': <function linear at 0x7f6ff3932de0>, 'time_width': 1.0}, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `update(self, dt: 'float' = 0) -> 'None'` — Calls all updaters in the family. Passing in a frame_rate accounts for

</details>

### `StreamLines(func: 'Callable[[VectArray], VectArray]', coordinate_system: 'CoordinateSystem', density: 'float' = 1.0, n_repeats: 'int' = 1, noise_factor: 'float | None' = None, solution_time: 'float' = 3, dt: 'float' = 0.05, arc_len: 'float' = 3, max_time_steps: 'int' = 200, n_samples_per_line: 'int' = 10, cutoff_norm: 'float' = 15, stroke_width: 'float' = 1.0, stroke_color: 'ManimColor' = '#FFFFFF', stroke_opacity: 'float' = 1, color_by_magnitude: 'bool' = True, magnitude_range: 'Tuple[float, float]' = (0, 2.0), taper_stroke_width: 'bool' = False, color_map: 'str' = '3b1b_colormap', **kwargs)` ← VGroup
> Mathematical Object

<details><summary>métodos próprios (5) · herdados: 319</summary>

- `__init__(self, func: 'Callable[[VectArray], VectArray]', coordinate_system: 'CoordinateSystem', density: 'float' = 1.0, n_repeats: 'int' = 1, noise_factor: 'float | None' = None, solution_time: 'float' = 3, dt: 'float' = 0.05, arc_len: 'float' = 3, max_time_steps: 'int' = 200, n_samples_per_line: 'int' = 10, cutoff_norm: 'float' = 15, stroke_width: 'float' = 1.0, stroke_color: 'ManimColor' = '#FFFFFF', stroke_opacity: 'float' = 1, color_by_magnitude: 'bool' = True, magnitude_range: 'Tuple[float, float]' = (0, 2.0), taper_stroke_width: 'bool' = False, color_map: 'str' = '3b1b_colormap', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `draw_lines(self) -> 'None'`
- `get_sample_coords(self)`
- `init_style(self) -> 'None'`
- `point_func(self, points: 'Vect3Array') -> 'Vect3'`

</details>

### `TimeVaryingVectorField(time_func: 'Callable[[VectArray, float], VectArray]', coordinate_system: 'CoordinateSystem', **kwargs)` ← VectorField
> Mathematical Object

<details><summary>métodos próprios (2) · herdados: 325</summary>

- `__init__(self, time_func: 'Callable[[VectArray, float], VectArray]', coordinate_system: 'CoordinateSystem', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `increment_time(self, dt)`

</details>

### `VectorField(func: 'Callable[[VectArray], VectArray]', coordinate_system: 'CoordinateSystem', sample_coords: 'Optional[VectArray]' = None, density: 'float' = 2.0, magnitude_range: 'Optional[Tuple[float, float]]' = None, color: 'Optional[ManimColor]' = None, color_map_name: 'Optional[str]' = '3b1b_colormap', color_map: 'Optional[Callable[[Sequence[float]], Vect4Array]]' = None, stroke_opacity: 'float' = 1.0, stroke_width: 'float' = 3, tip_width_ratio: 'float' = 4, tip_len_to_width: 'float' = 0.01, max_vect_len: 'float | None' = None, max_vect_len_to_step_size: 'float' = 0.8, flat_stroke: 'bool' = False, norm_to_opacity_func=None, **kwargs)` ← VMobject
> Mathematical Object

<details><summary>métodos próprios (9) · herdados: 317</summary>

- `__init__(self, func: 'Callable[[VectArray], VectArray]', coordinate_system: 'CoordinateSystem', sample_coords: 'Optional[VectArray]' = None, density: 'float' = 2.0, magnitude_range: 'Optional[Tuple[float, float]]' = None, color: 'Optional[ManimColor]' = None, color_map_name: 'Optional[str]' = '3b1b_colormap', color_map: 'Optional[Callable[[Sequence[float]], Vect4Array]]' = None, stroke_opacity: 'float' = 1.0, stroke_width: 'float' = 3, tip_width_ratio: 'float' = 4, tip_len_to_width: 'float' = 0.01, max_vect_len: 'float | None' = None, max_vect_len_to_step_size: 'float' = 0.8, flat_stroke: 'bool' = False, norm_to_opacity_func=None, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_sample_points(self, center: 'np.ndarray', width: 'float', height: 'float', depth: 'float', x_density: 'float', y_density: 'float', z_density: 'float') -> 'np.ndarray'`
- `init_base_stroke_width_array(self, n_sample_points)`
- `init_points(self)`
- `set_sample_coords(self, sample_coords: 'VectArray')`
- `set_stroke(self, color=None, width=None, opacity=None, behind=None, flat=None, recurse=True)`
- `set_stroke_width(self, width: 'float')`
- `update_sample_points(self)`
- `update_vectors(self)`

</details>

- `DEFAULT_MOBJECT_COLOR` = `'#FFFFFF'`
- `FRAME_HEIGHT` = `8.0`
- `FRAME_WIDTH` = `14.222222222222221`
- `TYPE_CHECKING` = `False`
- **`get_rgb_gradient_function(min_value: 'T', max_value: 'T', color_map: 'str') -> 'Callable[[float], Vect3]'`**
- **`get_sample_coords(coordinate_system: 'CoordinateSystem', density: 'float' = 1.0) -> 'it.product[tuple[Vect3, ...]]'`**
- **`get_vectorized_rgb_gradient_function(min_value: 'T', max_value: 'T', color_map: 'str') -> 'Callable[[VectN], Vect3Array]'`**
- **`move_along_vector_field(mobject: 'Mobject', func: 'Callable[[Vect3], Vect3]') -> 'Mobject'`**
- **`move_points_along_vector_field(mobject: 'Mobject', func: 'Callable[[float, float], Iterable[float]]', coordinate_system: 'CoordinateSystem') -> 'Mobject'`**
- **`move_submobjects_along_vector_field(mobject: 'Mobject', func: 'Callable[[Vect3], Vect3]') -> 'Mobject'`**
- **`ode_solution_points(function, state0, time, dt=0.01)`**
- **`vectorize(pointwise_function: 'Callable[[Tuple], Tuple]')`**

## other

### `BlankScene(window: 'Optional[Window]' = None, camera_config: 'dict' = {}, file_writer_config: 'dict' = {}, skip_animations: 'bool' = False, always_update_mobjects: 'bool' = False, start_at_animation_number: 'int | None' = None, end_at_animation_number: 'int | None' = None, show_animation_progress: 'bool' = False, leave_progress_bars: 'bool' = False, preview_while_skipping: 'bool' = True, presenter_mode: 'bool' = False, default_wait_time: 'float' = 1.0, invert_zoom_scroll: 'bool' = False)` ← InteractiveScene
> To select mobjects on screen, hold ctrl and move the mouse to highlight a region,

<details><summary>métodos próprios (1) · herdados: 113</summary>

- `construct(self)`

</details>

### `EventDispatcher()`

<details><summary>métodos próprios (9) · herdados: 0</summary>

- `__call__(self, event_type: 'EventType', **event_data)`
- `__init__(self)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_listner(self, event_listner: 'EventListener')`
- `dispatch(self, event_type: 'EventType', **event_data)`
- `get_listners_count(self) -> 'int'`
- `get_mouse_drag_point(self) -> 'np.ndarray'`
- `get_mouse_point(self) -> 'np.ndarray'`
- `is_key_pressed(self, symbol: 'int') -> 'bool'`
- `remove_listner(self, event_listner: 'EventListener')`

</details>

### `EventListener(mobject: 'Mobject', event_type: 'EventType', event_callback: 'Callable[[Mobject, dict[str]]]')`

<details><summary>métodos próprios (1) · herdados: 0</summary>

- `__init__(self, mobject: 'Mobject', event_type: 'EventType', event_callback: 'Callable[[Mobject, dict[str]]]')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `EventType(*values)` ← Enum
> Create a collection of name/value pairs.

### `Keys()`

### `Mods()`
> Which modifiers were held while an event happened, as the bits of one number

### `ModuleLoader()`
> Utility class to load a module from a file and handle its imports.

<details><summary>métodos próprios (1) · herdados: 1</summary>

- `get_module(file_name: 'str | None', is_during_reload=False) -> 'Module | None'` — Imports a module from a file and returns it.

</details>

### `Window(scene: 'Optional[Scene]' = None, position_string: 'str' = 'UR', monitor_index: 'int' = 1, full_screen: 'bool' = False, size: 'Optional[tuple[int, int]]' = None, position: 'Optional[tuple[int, int]]' = None)`
> Where a scene is previewed: somewhere to show a finished frame, and where mouse and key

<details><summary>métodos próprios (29) · herdados: 0</summary>

- `__init__(self, scene: 'Optional[Scene]' = None, position_string: 'str' = 'UR', monitor_index: 'int' = 1, full_screen: 'bool' = False, size: 'Optional[tuple[int, int]]' = None, position: 'Optional[tuple[int, int]]' = None)` — Initialize self.  See help(type(self)) for accurate signature.
- `configure(self) -> 'None'` — Points the surface at the device whose frames it will be showing.
- `destroy(self) -> 'None'`
- `draw(self) -> 'None'`
- `event_point(self, event: 'dict') -> 'np.ndarray'`
- `event_position(self, event: 'dict') -> 'np.ndarray'` — Where in the window something happened, measuring y upwards from the bottom the way
- `focus(self) -> 'None'`
- `get_default_size(self, monitor, full_screen: 'bool') -> 'tuple[int, int]'`
- `get_monitor(self, index: 'int')`
- `get_monitor_area(self, monitor) -> 'tuple[int, int, int, int]'` — Where the monitor's usable area is and how big it is, in screen coordinates
- `get_position(self, monitor, position_string: 'str') -> 'tuple[int, int]'` — Which corner of the monitor to open in, named by a pair of characters as in UR for
- `get_size(self) -> 'tuple[int, int]'` — How many pixels there are to draw, which is not the size in screen coordinates
- `has_undrawn_event(self) -> 'bool'`
- `init_for_scene(self, scene: 'Scene') -> 'None'` — Resets the state and updates the scene associated to this window.
- `init_present_resources(self) -> 'None'` — What a finished frame is read through on its way to the surface, made once
- `is_key_pressed(self, key: 'int') -> 'bool'`
- `note_event(self) -> 'None'`
- `on_close(self, event: 'dict') -> 'None'`
- `on_key_down(self, event: 'dict') -> 'None'`
- `on_key_up(self, event: 'dict') -> 'None'`
- `on_pointer_down(self, event: 'dict') -> 'None'`
- `on_pointer_move(self, event: 'dict') -> 'None'`
- `on_pointer_up(self, event: 'dict') -> 'None'`
- `on_resize(self, event: 'dict') -> 'None'`
- `on_wheel(self, event: 'dict') -> 'None'`
- `pixel_coords_to_space_coords(self, px: 'float', py: 'float', relative: 'bool' = False) -> 'np.ndarray'` — Where in the scene a place in the window is, both measuring y upwards from the
- `poll_events(self) -> 'None'` — Hands whatever the window has to say to the handlers below, and notices if it has been
- `present(self, target_view) -> 'None'` — Draws the finished frame onto what the surface gave us, stretched to fill it, see
- `show(self, frame_view) -> 'None'` — Puts a finished frame on screen. The canvas presents whatever its draw function drew,

</details>

- `ARRAY_ELEMENT_SIZE` = `4`
- `ARROW_SYMBOLS` = `[57344, 57346, 57345, 57347]`
- `ASPECT_RATIO` = `1.7777777777777777`
- `ASPECT_RATIO` = `1.7777777777777777`
- `BLACK` = `'#000000'`
- `BLOCK_MEMBER_TYPES` = `{1: 'f32', 2: 'vec2f', 3: 'vec3f', 4: 'vec4f', 16: 'mat4x4f'}`
- `BLUE` = `'#58C4DD'`
- `BLUE_A` = `'#C7E9F1'`
- `BLUE_B` = `'#9CDCEB'`
- `BLUE_C` = `'#58C4DD'`
- `BLUE_D` = `'#29ABCA'`
- `BLUE_E` = `'#1C758A'`
- `BOLD` = `'BOLD'`
- `BOTTOM` = `array([ 0., -4.,  0.])`
- `CACHE_SIZE` = `1000000000.0`
- `CLOSED_THRESHOLD` = `0.001`
- `COLORMAP_3B1B` = `['#1C758A', '#83C167', '#FFFF00', '#FC6255']`
- `COLOR_FORMAT` = `'rgba8unorm'`
- `COLOR_KEY` = `'c'`
- `COMMON_UNIFORMS` = `(('is_fixed_in_frame', 1), ('shading', 3), ('clip_plane0', 4), ('clip_plane1', 4), ('clip_plane2', 4), ('clip_plane3'...`
- `CURSOR_KEY` = `'k'`
- `DARK_BROWN` = `'#8B4513'`
- `DEFAULT_ANIMATION_LAG_RATIO` = `0`
- `DEFAULT_ANIMATION_RUN_TIME` = `1.0`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_WIDTH` = `0.35`
- `DEFAULT_BUFF_RATIO` = `0.5`
- `DEFAULT_CANVAS_HEIGHT` = `16384`
- `DEFAULT_CANVAS_WIDTH` = `16384`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.05`
- `DEFAULT_GLOW_DOT_RADIUS` = `0.2`
- `DEFAULT_GRID_HEIGHT` = `6`
- `DEFAULT_LAGGED_START_LAG_RATIO` = `0.05`
- `DEFAULT_LIGHT_COLOR` = `'#BBBBBB'`
- `DEFAULT_LINE_SPACING_SCALE` = `0.6`
- `DEFAULT_MOBJECT_COLOR` = `'#FFFFFF'`
- `DEFAULT_MOBJECT_TO_EDGE_BUFF` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFF` = `0.25`
- `DEFAULT_PIXEL_HEIGHT` = `1080`
- `DEFAULT_PIXEL_WIDTH` = `1920`
- `DEFAULT_RESOLUTION` = `(1920, 1080)`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4.0`
- `DEFAULT_VMOBJECT_FILL_COLOR` = `'#888888'`
- `DEFAULT_VMOBJECT_STROKE_COLOR` = `'#DDDDDD'`
- `DEFAULT_X_RANGE` = `(-8.0, 8.0, 1.0)`
- `DEFAULT_Y_RANGE` = `(-4.0, 4.0, 1.0)`
- `DEG` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DEPTH_STENCIL_FORMAT` = `'depth24plus-stencil8'`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPSILON` = `0.0001`
- `FORMAT` = `'%(message)s'`
- `FRAME_HEIGHT` = `8.0`
- `FRAME_SHAPE` = `(14.222222222222221, 8.0)`
- `FRAME_SHAPE` = `(14.222222222222221, 8.0)`
- `FRAME_WIDTH` = `14.222222222222221`
- `FRAME_X_RADIUS` = `7.111111111111111`
- `FRAME_Y_RADIUS` = `4.0`
- `GOLD` = `'#F0AC5F'`
- `GOLD_A` = `'#F7C797'`
- `GOLD_B` = `'#F9B775'`
- `GOLD_C` = `'#F0AC5F'`
- `GOLD_D` = `'#E1A158'`
- `GOLD_E` = `'#C78D46'`
- `GRAB_KEY` = `'g'`
- `GRAB_KEYS` = `['g', 'h', 'v', 'z']`
- `GRADIENT_POINT_KEYS` = `['gradient_start', 'gradient_end']`
- `GREEN` = `'#83C167'`
- `GREEN_A` = `'#C9E2AE'`
- `GREEN_B` = `'#A6CF8C'`
- `GREEN_C` = `'#83C167'`
- `GREEN_D` = `'#77B05D'`
- `GREEN_E` = `'#699C52'`
- `GREEN_SCREEN` = `'#00FF00'`
- `GREY` = `'#888888'`
- `GREY_A` = `'#DDDDDD'`
- `GREY_B` = `'#BBBBBB'`
- `GREY_BROWN` = `'#736357'`
- `GREY_C` = `'#888888'`
- `GREY_D` = `'#444444'`
- `GREY_E` = `'#222222'`
- `IN` = `array([ 0.,  0., -1.])`
- `INFORMATION_KEY` = `'i'`
- `ITALIC` = `'ITALIC'`
- `KEY_NAMES` = `{'Backspace': 8, 'Tab': 9, 'Enter': 13, 'Escape': 27, 'Delete': 127, 'ArrowLeft': 57344, 'ArrowRight': 57345, 'ArrowU...`
- `KEY_NAMES` = `{'Backspace': 8, 'Tab': 9, 'Enter': 13, 'Escape': 27, 'Delete': 127, 'ArrowLeft': 57344, 'ArrowRight': 57345, 'ArrowU...`
- `LARGE_BUFF` = `1.0`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT_SIDE` = `array([-7.11111111,  0.        ,  0.        ])`
- `LIGHT_BROWN` = `'#CD853F'`
- `LIGHT_PINK` = `'#DC75CD'`
- `MANDELBROT_COLORS` = `['#00065c', '#061e7e', '#0c37a0', '#205abc', '#4287d3', '#D9EDE4', '#F0F9E4', '#BA9F6A', '#573706']`
- `MANIM_COLORS` = `['#1C758A', '#29ABCA', '#58C4DD', '#9CDCEB', '#C7E9F1', '#49A88F', '#55C1A7', '#5CD0B3', '#76DDC0', '#ACEAD7', '#699C...`
- `MAROON` = `'#C55F73'`
- `MAROON_A` = `'#ECABC1'`
- `MAROON_B` = `'#EC92AB'`
- `MAROON_C` = `'#C55F73'`
- `MAROON_D` = `'#A24D61'`
- `MAROON_E` = `'#94424F'`
- `MAX_DEGREE` = `5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `MOD_NAMES` = `{'Shift': 1, 'Control': 2, 'Alt': 4, 'Meta': 8}`
- `MOD_NAMES` = `{'Shift': 1, 'Control': 2, 'Alt': 4, 'Meta': 8}`
- `NEWTON_ROOT_COLORS` = `['#440154', '#3b528b', '#21908c', '#5dc963', '#29abca']`
- `NORMAL` = `'NORMAL'`
- `NULL_POINTS` = `array([[0., 0., 0.]])`
- `N_MANDELBROT_COLORS` = `9`
- `OBLIQUE` = `'OBLIQUE'`
- `ORANGE` = `'#FF862F'`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `PATH_TO_POINTS` = `{}`
- `PI` = `3.141592653589793`
- `PINK` = `'#D147BD'`
- `POSITION_STEPS` = `{'L': 0.0, 'U': 0.0, 'O': 0.5, 'R': 1.0, 'D': 1.0}`
- `POSITION_STEPS` = `{'L': 0.0, 'U': 0.0, 'O': 0.5, 'R': 1.0, 'D': 1.0}`
- `PRESENT_SHADER` = `'present.wgsl'`
- `PRESENT_SHADER` = `'present.wgsl'`
- `PURE_BLUE` = `'#0000FF'`
- `PURE_GREEN` = `'#00FF00'`
- `PURE_RED` = `'#FF0000'`
- `PURPLE` = `'#9A72AC'`
- `PURPLE_A` = `'#CAA3E8'`
- `PURPLE_B` = `'#B189C6'`
- `PURPLE_C` = `'#9A72AC'`
- `PURPLE_D` = `'#715582'`
- `PURPLE_E` = `'#644172'`
- `RADIANS` = `1`
- `RED` = `'#FC6255'`
- `RED_A` = `'#F7A1A3'`
- `RED_B` = `'#FF8080'`
- `RED_C` = `'#FC6255'`
- `RED_D` = `'#E65A4C'`
- `RED_E` = `'#CF5044'`
- `RESIZE_KEY` = `'t'`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT_SIDE` = `array([7.11111111, 0.        , 0.        ])`
- `SELECT_KEY` = `'s'`
- `SMALL_BUFF` = `0.1`
- `STRAIGHT_PATH_THRESHOLD` = `0.01`
- `STROKE_WIDTHS_PER_UNIT` = `100.0`
- `SVG_HASH_TO_MOB_MAP` = `{}`
- `TAU` = `6.283185307179586`
- `TEAL` = `'#5CD0B3'`
- `TEAL_A` = `'#ACEAD7'`
- `TEAL_B` = `'#76DDC0'`
- `TEAL_C` = `'#5CD0B3'`
- `TEAL_D` = `'#55C1A7'`
- `TEAL_E` = `'#49A88F'`
- `TEX_TO_SYMBOL_COUNT` = `{'\\!': 0, '\\,': 0, '\\-': 0, '\\/': 0, '\\:': 0, '\\;': 0, '\\>': 0, '\\aa': 0, '\\AA': 0, '\\ae': 0, '\\AE': 0, '\...`
- `TOP` = `array([0., 4., 0.])`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `UNSELECT_KEY` = `'u'`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `WHEEL_NOTCH` = `100.0`
- `WHEEL_NOTCH` = `100.0`
- `WHITE` = `'#FFFFFF'`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_GRAB_KEY` = `'h'`
- `YELLOW` = `'#FFFF00'`
- `YELLOW_A` = `'#FFF1B6'`
- `YELLOW_B` = `'#FFEA94'`
- `YELLOW_C` = `'#FFFF00'`
- `YELLOW_D` = `'#F4D345'`
- `YELLOW_E` = `'#E8C11C'`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_GRAB_KEY` = `'v'`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_GRAB_KEY` = `'z'`
- **`compute_total_frames(scene_class, scene_config)`** — When a scene is being written to file, a copy of the scene is run with
- **`get_animations_numbers(args: 'Namespace') -> 'tuple[int | None, int | None]'`**
- **`get_file_ext(args: 'Namespace') -> 'str'`**
- **`get_indent(code_lines: 'list[str]', line_number: 'int') -> 'str'`** — Find the indent associated with a given line of python code,
- **`get_manim_dir()`**
- **`get_module(run_config: 'Dict') -> 'Module'`**
- **`get_output_directory(args: 'Namespace', config: 'Dict') -> 'str'`**
- **`get_resolution_from_args(args: 'Optional[Namespace]', resolution_options: 'dict') -> 'Optional[tuple[int, int]]'`**
- **`get_scene_classes(module: 'Optional[Module]')`**
- **`get_scenes_to_render(all_scene_classes: 'list', scene_config: 'Dict', run_config: 'Dict')`**
- **`initialize_manim_config() -> 'Dict'`** — Return default configuration for various classes in manim, such as
- **`insert_embed_line_to_module(module: 'Module', run_config: 'Dict') -> 'None'`** — This is hacky, but convenient. When user includes the argument "-e", it will try
- **`is_child_scene(obj, module)`**
- **`load_yaml(file_path: 'str')`**
- **`main()`** — Main entry point for ManimGL.
- **`main(scene_config: 'Dict', run_config: 'Dict')`**
- **`note_missing_scenes(arg_names, module_names)`**
- **`parse_cli()`**
- **`prompt_user_for_choice(scene_classes)`**
- **`run_scenes()`** — Runs the scenes in a loop and detects when a scene reload is requested.
- **`scene_from_class(scene_class, scene_config: 'Dict', run_config: 'Dict')`**
- **`to_key(name: 'str') -> 'Optional[int]'`** — manim's name for a key, or None for one it has no name for, which is every key nothing
- **`to_mods(names: 'Sequence[str]') -> 'int'`**
- **`update_camera_config(config: 'Dict', args: 'Namespace')`**
- **`update_directory_config(config: 'Dict')`**
- **`update_embed_config(config: 'Dict', args: 'Namespace')`**
- **`update_file_writer_config(config: 'Dict', args: 'Namespace')`**
- **`update_run_config(config: 'Dict', args: 'Namespace')`**
- **`update_scene_config(config: 'Dict', args: 'Namespace')`**
- **`update_window_config(config: 'Dict', args: 'Namespace')`**

## renderer

### `Bundling(allowed: 'bool' = True)`
> When a frame's draws are worth gathering into a render bundle, and for how long the one

<details><summary>métodos próprios (3) · herdados: 0</summary>

- `__init__(self, allowed: 'bool' = True)` — Initialize self.  See help(type(self)) for accurate signature.
- `invalidate(self) -> 'None'`
- `take(self, make: 'Callable[[], Any]') -> 'Any'` — The bundle to replay this frame, or none where the draws have to be made afresh. Makes

</details>

### `Drawing(material: 'Material', mobject: 'Mobject')`
> One mobject's place in a frame: where its values went in the shared buffers, everything

<details><summary>métodos próprios (11) · herdados: 0</summary>

- `__init__(self, material: 'Material', mobject: 'Mobject')` — Initialize self.  See help(type(self)) for accurate signature.
- `can_follow(self, previous: 'Drawing') -> 'bool'` — Whether one draw could cover this mobject along with the one before it, which means
- `draw(self, render_pass: 'RenderPass') -> 'None'` — Every pass this mobject takes. What they read is bound once here, all of them reading
- `draw_pass(self, render_pass: 'RenderPass', module: 'str', state: 'PipelineState', vertices: 'int', indices: 'Any' = None) -> 'None'`
- `draw_passes(self, render_pass: 'RenderPass') -> 'None'` — Every pass this kind of mobject takes, which for most kinds is the one
- `draws(mobject: 'Mobject') -> 'bool'` — Whether this mobject has anything to be drawn by, which a group has not
- `key(mobject: 'Mobject') -> 'tuple'` — What two mobjects have to agree about to share one material
- `module_specs(mobject: 'Mobject') -> 'list[ModuleSpec]'` — Which modules this kind of drawing needs compiled, and what to name them by
- `resource_bind_group(self) -> 'Any'` — What this mobject's records and images are read through. Without images of its own it
- `write_records(self) -> 'None'` — A mobject's records into a stretch of the shared buffer, or, where it draws a run of
- `write_uniforms(self) -> 'bool'` — A mobject's uniforms into the buffer they share, along with everything its draw needs

</details>

### `Gpu()`
> The device everything is made from, and every cache built on it: the modules shaders are

<details><summary>métodos próprios (14) · herdados: 0</summary>

- `__init__(self)` — Initialize self.  See help(type(self)) for accurate signature.
- `begin_writes(self) -> 'None'` — Gives back every stretch of every buffer, a frame's stretches being a frame's own
- `bind_layouts(self, texture_count: 'int') -> 'tuple[Any, Any]'` — What a shader may bind: the frame's values, the mobject's values, and its records along
- `bundle(self, draw: 'Callable[[RenderPass], None]') -> 'Any'` — The draws a callable makes, gathered into a bundle to be replayed with one call rather
- `data_buffer(self, record_size: 'int') -> 'SharedBuffer'` — Where the records of a mobject whose records are this size are gathered
- `end_writes(self) -> 'None'`
- `module(self, code: 'str') -> 'Any'` — One module holds both stages of a shader, sharing a struct rather than a varying
- `pipeline(self, layout: 'Any', module: 'Any', state: 'PipelineState') -> 'Any'` — The pipeline for one pass over one kind of mobject, kept here so that every mobject of
- `render_pass(self, attachments: 'dict') -> 'Iterator[RenderPass]'` — The one render pass a frame is drawn in. Opening a pass loads its attachments into fast
- `sampler(self) -> 'Any'` — The one sampler every image is read through
- `send_frame_uniforms(self) -> 'None'` — The frame's uniforms, if they have been written to since they were last sent
- `shared_buffer(self, key: 'tuple', layout: 'Any', usage: 'int', limit: 'str', first_capacity: 'int') -> 'SharedBuffer'`
- `texture(self, path: 'str') -> 'Any'` — An image on the gpu, for whatever samples it. Uploaded once per path.
- `uniform_buffer(self, block_size: 'int') -> 'SharedBuffer'` — Where the uniforms of a mobject whose block is this size are gathered

</details>

### `Material(gpu: 'Gpu', mobject: 'Mobject', specs: 'Sequence[ModuleSpec]')`
> Everything one kind of mobject is drawn with, and nothing about any particular one: the

<details><summary>métodos próprios (4) · herdados: 0</summary>

- `__init__(self, gpu: 'Gpu', mobject: 'Mobject', specs: 'Sequence[ModuleSpec]')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_code(self, mobject: 'Mobject', filename: 'str', replacements: 'dict[str, str]') -> 'str'` — A shader's source, told where the fields of one of these mobjects' records sit and what
- `make_resource_bind_group(self) -> 'Any'` — A group through which one mobject reads its records and its own images. Only a mobject
- `pipeline(self, module: 'str', state: 'PipelineState') -> 'Any'` — The pipeline for one pass, naming the module by what the drawing asked for it as

</details>

### `PipelineState(depth_test: 'bool | None' = None, depth_write: 'bool' = True, color_write: 'bool' = True, stencil_compare: 'str' = 'always', stencil_ops: 'tuple[tuple[str, str, str], tuple[str, str, str]]' = (('keep', 'keep', 'keep'), ('keep', 'keep', 'keep'))) -> None`
> The fixed function half of a pipeline: everything about how a draw behaves beyond which

<details><summary>métodos próprios (3) · herdados: 0</summary>

- `__init__(self, depth_test: 'bool | None' = None, depth_write: 'bool' = True, color_write: 'bool' = True, stencil_compare: 'str' = 'always', stencil_ops: 'tuple[tuple[str, str, str], tuple[str, str, str]]' = (('keep', 'keep', 'keep'), ('keep', 'keep', 'keep'))) -> None` — Initialize self.  See help(type(self)) for accurate signature.
- `depth_stencil_descriptor(self) -> 'dict'` — This state as a pipeline descriptor wants it
- `resolved(self, depth_test: 'bool') -> 'PipelineState'` — This state with the mobject's own choice of depth test settled into it, or as it

</details>

### `RenderPass(encoder: 'Any', frame_bind_group: 'Any')`
> Where draw commands go. A live pass and a bundle being recorded take the same commands, so

<details><summary>métodos próprios (5) · herdados: 0</summary>

- `__init__(self, encoder: 'Any', frame_bind_group: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `bind(self, group: 'int', bind_group: 'Any', offsets: 'tuple' = ()) -> 'None'`
- `draw(self, pipeline: 'Any', vertices: 'int', indices: 'Any' = None) -> 'None'` — One pass over a mobject's records, taking them in the order a buffer of indices gives
- `forget(self) -> 'None'` — Whatever was told to the pass is forgotten, and the one thing every draw reads said
- `replay(self, bundle: 'Any') -> 'None'`

</details>

### `Renderer(gpu: 'Gpu', bundle: 'bool' = True, together: 'bool' = True)`
> What a frame draws, in the order it draws it: a drawing for each mobject holding points,

<details><summary>métodos próprios (7) · herdados: 0</summary>

- `__init__(self, gpu: 'Gpu', bundle: 'bool' = True, together: 'bool' = True)` — Initialize self.  See help(type(self)) for accurate signature.
- `compare_uniforms(self, drawings: 'list[Drawing]') -> 'None'` — Tells every mobject whether the one drawn before it holds the same uniforms, which is
- `draw(self, mobjects: 'Iterable[Mobject]', attachments: 'dict') -> 'None'`
- `group(self, drawings: 'list[Drawing]') -> 'tuple'` — Gathers consecutive mobjects which one draw can cover: the same material, nothing about
- `make_draws(self, render_pass: 'RenderPass') -> 'None'`
- `material_for(self, mobject: 'Mobject', drawing_class: 'type') -> 'Material'` — What draws this mobject, shared with every mobject its key agrees with, see
- `resolve(self, mobjects: 'Iterable[Mobject]') -> 'list[Drawing]'` — A drawing for every member of every family which has anything to draw, in drawing

</details>

### `SharedBuffer(gpu: 'Gpu', layout: 'Any', usage: 'int', alignment: 'int', first_capacity: 'int')`
> One buffer holding what many mobjects read, a stretch of it each, sent in one write.

<details><summary>métodos próprios (8) · herdados: 0</summary>

- `__init__(self, gpu: 'Gpu', layout: 'Any', usage: 'int', alignment: 'int', first_capacity: 'int')` — Initialize self.  See help(type(self)) for accurate signature.
- `claim(self, nbytes: 'int') -> 'int'` — Where the next stretch goes, as the offset its draw is to be given. There has to be a
- `grow_to(self, needed: 'int') -> 'bool'` — Room for that many bytes, and whether that meant a new buffer
- `make_bindings(self) -> 'None'` — A group afresh, which whatever binds through this one has to hear about
- `matching_claims(self) -> 'list[bool]'` — For every stretch claimed since the last reset, whether it holds the same bytes as the
- `put(self, offset: 'int', source: 'np.ndarray', record_size: 'int' = 0, repeats: 'int' = 0) -> 'None'` — Bytes into the buffer, followed by the last record_size of them written again that many
- `reset(self) -> 'None'`
- `upload(self) -> 'None'` — Whatever was written into since the last send, in one write

</details>

### `SurfaceDrawing(material: 'Material', mobject: 'Mobject')` ← Drawing
> An opaque surface is drawn in one pass and left to the depth test, which decides what

<details><summary>métodos próprios (5) · herdados: 8</summary>

- `__init__(self, material: 'Material', mobject: 'Mobject')` — Initialize self.  See help(type(self)) for accurate signature.
- `draw_passes(self, render_pass: 'RenderPass') -> 'None'` — Every pass this kind of mobject takes, which for most kinds is the one
- `order_triangles_by_depth(self) -> 'bool'` — Lists the vertices of every triangle of the mesh, three to each, those furthest from
- `write_order_buffer(self, indices: 'np.ndarray') -> 'None'`
- `write_uniforms(self) -> 'bool'` — A mobject's uniforms into the buffer they share, along with everything its draw needs

</details>

### `Uniforms(dtype: 'np.dtype')` ← StructuredArray
> A mobject's uniforms: one value each for the whole of it, laid out to match the block its

<details><summary>métodos próprios (2) · herdados: 11</summary>

- `__init__(self, dtype: 'np.dtype')` — Initialize self.  See help(type(self)) for accurate signature.
- `apply(self, key: 'str', func: 'Callable[[np.ndarray], np.ndarray]') -> 'None'` — Passes one uniform through a function written for many rows of values, e.g. one

</details>

### `VDrawing(material: 'Material', mobject: 'Mobject')` ← Drawing
> A vectorized mobject is drawn by two shaders: a fill over the region its path encloses,

<details><summary>métodos próprios (12) · herdados: 4</summary>

- `__init__(self, material: 'Material', mobject: 'Mobject')` — Initialize self.  See help(type(self)) for accurate signature.
- `can_follow(self, previous: 'Drawing') -> 'bool'` — A fill counts its winding across the whole of a draw, so two filled mobjects may share
- `draw_fill(self, render_pass: 'RenderPass') -> 'None'` — Fill is drawn with a "stencil then cover" approach.
- `draw_fill_border(self, render_pass: 'RenderPass') -> 'None'` — Traces the boundary with a stroke in the fill color, which is what anti-aliases the
- `draw_passes(self, render_pass: 'RenderPass') -> 'None'` — Every pass this kind of mobject takes, which for most kinds is the one
- `draw_stroke(self, render_pass: 'RenderPass') -> 'None'`
- `draws(mobject: 'Mobject') -> 'bool'` — Always, the two shaders being named here rather than by the mobject
- `get_num_curves(self) -> 'int'`
- `key(mobject: 'Mobject') -> 'tuple'` — What two mobjects have to agree about to share one material
- `module_specs(mobject: 'Mobject') -> 'list[ModuleSpec]'` — Three modules from two sources: the border around a fill is the stroke shader with one
- `stroke_vertices(self, extra_curves: 'int' = 0) -> 'int'`
- `write_uniforms(self) -> 'bool'` — A mobject's uniforms into the buffer they share, along with everything its draw needs

</details>

- `ARRAY_ELEMENT_SIZE` = `4`
- `BLEND` = `{'color': {'src_factor': 'src-alpha', 'dst_factor': 'one-minus-src-alpha', 'operation': 'add'}, 'alpha': {'src_factor...`
- `BLOCK_MEMBER_TYPES` = `{1: 'f32', 2: 'vec2f', 3: 'vec3f', 4: 'vec4f', 16: 'mat4x4f'}`
- `COLOR_FORMAT` = `'rgba8unorm'`
- `COLOR_FORMAT` = `'rgba8unorm'`
- `COMMON_UNIFORMS` = `(('is_fixed_in_frame', 1), ('shading', 3), ('clip_plane0', 4), ('clip_plane1', 4), ('clip_plane2', 4), ('clip_plane3'...`
- `DATA_BINDING` = `0`
- `DATA_BINDING` = `0`
- `DATA_BINDING` = `0`
- `DEFAULT` = `PipelineState(depth_test=None, depth_write=True, color_write=True, stencil_compare='always', stencil_ops=(('keep', 'k...`
- `DEFAULT` = `PipelineState(depth_test=None, depth_write=True, color_write=True, stencil_compare='always', stencil_ops=(('keep', 'k...`
- `DEPTH_STENCIL_FORMAT` = `'depth24plus-stencil8'`
- `DEPTH_STENCIL_FORMAT` = `'depth24plus-stencil8'`
- `FILL_BORDER` = `PipelineState(depth_test=None, depth_write=True, color_write=True, stencil_compare='equal', stencil_ops=(('keep', 'ke...`
- `FIRST_TEXTURE_BINDING` = `2`
- `FIRST_TEXTURE_BINDING` = `2`
- `FIRST_TEXTURE_BINDING` = `2`
- `FRAMES_BEFORE_BUNDLING` = `2`
- `FRAME_DTYPE` = `dtype([('view', '<f4', (16,)), ('frame_rescale_factors', '<f4', (3,)), ('frame_scale', '<f4'), ('camera_position', '<...`
- `FRAME_GROUP` = `0`
- `FRAME_GROUP` = `0`
- `FRAME_UNIFORMS` = `(('view', 16), ('frame_rescale_factors', 3), ('frame_scale', 1), ('camera_position', 3), ('pixel_size', 1), ('light_p...`
- `KEEP` = `('keep', 'keep', 'keep')`
- `KEEP` = `('keep', 'keep', 'keep')`
- `MOBJECT_GROUP` = `1`
- `MOBJECT_GROUP` = `1`
- `RECORDS` = `4096`
- `RESOURCE_GROUP` = `2`
- `RESOURCE_GROUP` = `2`
- `SAMPLER_BINDING` = `1`
- `SAMPLER_BINDING` = `1`
- `SAMPLER_BINDING` = `1`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `UNIFORM_BLOCKS` = `256`
- `WINDING_COUNT` = `PipelineState(depth_test=False, depth_write=False, color_write=False, stencil_compare='always', stencil_ops=(('keep',...`
- `WINDING_COVER` = `PipelineState(depth_test=None, depth_write=True, color_write=True, stencil_compare='not-equal', stencil_ops=(('keep',...`
- **`build_pipeline(device: 'Any', layout: 'Any', module: 'Any', state: 'PipelineState', samples: 'int') -> 'Any'`** — One pipeline. No shader is handed vertex attributes, hence the empty list of vertex
- **`data_layout_code(dtype: 'np.dtype') -> 'str'`** — Where each field of a record sits, in floats, for a shader to index by. No shader is handed
- **`get_colormap_code(rgb_list: 'Sequence[float]') -> 'str'`** — A list of colors as a shader array literal, for a snippet coloring by a value
- **`get_shader_code(filename: 'str', data_dtype: 'np.dtype', uniform_dtype: 'np.dtype', texture_names: 'tuple[str, ...]' = ()) -> 'str | None'`** — Reads a shader from file, filling in what its source depends on about the mobject it will
- **`texture_binding_code(texture_names: 'tuple[str, ...]') -> 'str'`** — How a shader declares the images its kind of mobject named, and the sampler they share,
- **`uniform_block_code(dtype: 'np.dtype') -> 'str'`** — A dtype written as the members of a shader struct, which is where a shader gets them,
- **`uniform_block_dtype(*members: 'tuple[str, int] | tuple[str, int, int]') -> 'np.dtype'`** — Lays out members, each given as a name and how many floats it holds, exactly as std140

## scene

### `CheckpointManager()`

<details><summary>métodos próprios (5) · herdados: 0</summary>

- `__init__(self)` — Initialize self.  See help(type(self)) for accurate signature.
- `checkpoint_paste(self, shell, scene)` — Used during interactive development to run (or re-run)
- `clear_checkpoints(self)`
- `get_leading_comment(code_string: 'str') -> 'str'`
- `handle_checkpoint_key(self, scene, key: 'str')`

</details>

### `EndScene()` ← Exception
> Common base class for all non-exit exceptions.

### `InteractiveScene(window: 'Optional[Window]' = None, camera_config: 'dict' = {}, file_writer_config: 'dict' = {}, skip_animations: 'bool' = False, always_update_mobjects: 'bool' = False, start_at_animation_number: 'int | None' = None, end_at_animation_number: 'int | None' = None, show_animation_progress: 'bool' = False, leave_progress_bars: 'bool' = False, preview_while_skipping: 'bool' = True, presenter_mode: 'bool' = False, default_wait_time: 'float' = 1.0, invert_zoom_scroll: 'bool' = False)` ← Scene
> To select mobjects on screen, hold ctrl and move the mouse to highlight a region,

<details><summary>métodos próprios (47) · herdados: 67</summary>

- `add(self, *mobjects: 'Mobject')` — Mobjects will be displayed, from background to
- `add_to_selection(self, *mobjects: 'Mobject')`
- `choose_color(self, point: 'Vect3')`
- `clear_selection(self)`
- `copy_cursor_position(self)`
- `copy_frame_positioning(self)`
- `copy_selection(self)`
- `delete_selection(self)`
- `disable_interaction(self, *mobjects: 'Mobject')`
- `display_information(self, show=True)`
- `enable_interaction(self, *mobjects: 'Mobject')`
- `enable_selection(self)`
- `gather_new_selection(self)`
- `get_color_palette(self)`
- `get_corner_dots(self, mobject: 'Mobject') -> 'Mobject'`
- `get_crosshair(self)`
- `get_highlight(self, mobject: 'Mobject') -> 'Mobject'`
- `get_information_label(self)`
- `get_selection_highlight(self)`
- `get_selection_rectangle(self)`
- `get_selection_search_set(self) -> 'list[Mobject]'`
- `get_state(self)`
- `group_selection(self)`
- `handle_grabbing(self, point: 'Vect3')`
- `handle_resizing(self, point: 'Vect3')`
- `handle_sweeping_selection(self, point: 'Vect3')`
- `nudge_selection(self, vect: 'np.ndarray', large: 'bool' = False)`
- `on_key_press(self, symbol: 'int', modifiers: 'int') -> 'None'`
- `on_key_release(self, symbol: 'int', modifiers: 'int') -> 'None'`
- `on_mouse_drag(self, point: 'Vect3', d_point: 'Vect3', buttons: 'int', modifiers: 'int') -> 'None'`
- `on_mouse_motion(self, point: 'Vect3', d_point: 'Vect3') -> 'None'`
- `on_mouse_release(self, point: 'Vect3', button: 'int', mods: 'int') -> 'None'`
- `paste_selection(self)`
- `prepare_grab(self)`
- `prepare_resizing(self, about_corner=False)`
- `refresh_selection_scope(self)`
- `regenerate_selection_search_set(self)`
- `remove(self, *mobjects: 'Mobject')` — Removes anything in mobjects from scenes mobject list, but in the event that one
- `remove_all_except(self, *mobjects_to_keep: 'Mobject')`
- `restore_state(self, scene_state: 'SceneState')`
- `setup(self)` — This is meant to be implement by any scenes which
- `toggle_color_palette(self)`
- `toggle_from_selection(self, *mobjects: 'Mobject')`
- `toggle_selection_mode(self)`
- `ungroup_selection(self)`
- `update_selection_highlight(self, highlight: 'Mobject')`
- `update_selection_rectangle(self, rect: 'Rectangle')`

</details>

### `InteractiveSceneEmbed(scene: 'Scene')`

<details><summary>métodos próprios (11) · herdados: 0</summary>

- `__init__(self, scene: 'Scene')` — Initialize self.  See help(type(self)) for accurate signature.
- `auto_reload(self)` — Enables reload the shell's module before all calls
- `checkpoint_paste(self, skip: 'bool' = False, record: 'bool' = False, progress_bar: 'bool' = True)`
- `enable_gui(self)` — Enables gui interactions during the embed
- `ensure_flash_on_error(self)` — Flash border, and potentially play sound, on exceptions
- `ensure_frame_update_post_cell(self)` — Ensure the scene updates its frame after each ipython cell
- `get_ipython_shell_for_embedded_scene(self) -> 'InteractiveShellEmbed'` — Create embedded IPython terminal configured to have access to
- `get_shortcuts(self)` — A few custom shortcuts useful to have in the interactive shell namespace
- `launch(self)`
- `reload_scene(self, embed_line: 'int | None' = None) -> 'None'` — Reloads the scene just like the `manimgl` command would do with the
- `validate_syntax(self, file_path: 'str') -> 'bool'` — Validates the syntax of a Python file without executing it.

</details>

### `Scene(window: 'Optional[Window]' = None, camera_config: 'dict' = {}, file_writer_config: 'dict' = {}, skip_animations: 'bool' = False, always_update_mobjects: 'bool' = False, start_at_animation_number: 'int | None' = None, end_at_animation_number: 'int | None' = None, show_animation_progress: 'bool' = False, leave_progress_bars: 'bool' = False, preview_while_skipping: 'bool' = True, presenter_mode: 'bool' = False, default_wait_time: 'float' = 1.0, invert_zoom_scroll: 'bool' = False)`

<details><summary>métodos próprios (78) · herdados: 0</summary>

- `__init__(self, window: 'Optional[Window]' = None, camera_config: 'dict' = {}, file_writer_config: 'dict' = {}, skip_animations: 'bool' = False, always_update_mobjects: 'bool' = False, start_at_animation_number: 'int | None' = None, end_at_animation_number: 'int | None' = None, show_animation_progress: 'bool' = False, leave_progress_bars: 'bool' = False, preview_while_skipping: 'bool' = True, presenter_mode: 'bool' = False, default_wait_time: 'float' = 1.0, invert_zoom_scroll: 'bool' = False)` — Initialize self.  See help(type(self)) for accurate signature.
- `add(self, *new_mobjects: 'Mobject')` — Mobjects will be displayed, from background to
- `add_mobjects_among(self, values: 'Iterable')` — This is meant mostly for quick prototyping,
- `add_sound(self, sound_file: 'str', time_offset: 'float' = 0, gain: 'float | None' = None, gain_to_background: 'float | None' = None)`
- `affects_mobject_list(func: 'Callable[..., T]') -> 'Callable[..., T]'`
- `begin_animations(self, animations: 'Iterable[Animation]') -> 'None'`
- `bring_to_back(self, *mobjects: 'Mobject')`
- `bring_to_front(self, *mobjects: 'Mobject')`
- `clear(self)`
- `construct(self) -> 'None'`
- `draw_frame(self, dt: 'float' = 0, force_draw: 'bool' = False) -> 'None'`
- `embed(self, close_scene_on_exit: 'bool' = True, show_animation_progress: 'bool' = False) -> 'None'`
- `emit_frame(self) -> 'None'`
- `finish_animations(self, animations: 'Iterable[Animation]') -> 'None'`
- `focus(self) -> 'None'` — Puts focus on the ManimGL window.
- `force_skipping(self)`
- `get_animation_time_progression(self, animations: 'Iterable[Animation]') -> 'list[float] | np.ndarray | ProgressDisplay'`
- `get_group(self, *mobjects)`
- `get_image(self) -> 'Image'`
- `get_mobject_copies(self) -> 'list[Mobject]'`
- `get_mobject_family_members(self) -> 'list[Mobject]'`
- `get_mobjects(self) -> 'list[Mobject]'`
- `get_run_time(self, animations: 'Iterable[Animation]') -> 'float'`
- `get_state(self) -> 'SceneState'`
- `get_time(self) -> 'float'`
- `get_time_progression(self, run_time: 'float', n_iterations: 'int | None' = None, desc: 'str' = '', override_skip_animations: 'bool' = False) -> 'list[float] | np.ndarray | ProgressDisplay'`
- `get_top_level_mobjects(self) -> 'list[Mobject]'`
- `get_wait_time_progression(self, duration: 'float', stop_condition: 'Callable[[], bool] | None' = None) -> 'list[float] | np.ndarray | ProgressDisplay'`
- `get_window(self) -> 'Window | None'`
- `hold_loop(self)`
- `i2g(self, *id_values)`
- `i2m(self, id_value)`
- `id_to_mobject(self, id_value)`
- `ids_to_group(self, *id_values)`
- `increment_time(self, dt: 'float') -> 'None'`
- `interact(self) -> 'None'` — If there is a window, enter a loop which updates the frame, each of those
- `is_window_closing(self)`
- `on_close(self) -> 'None'`
- `on_hide(self) -> 'None'`
- `on_key_press(self, symbol: 'int', modifiers: 'int') -> 'None'`
- `on_key_release(self, symbol: 'int', modifiers: 'int') -> 'None'`
- `on_mouse_drag(self, point: 'Vect3', d_point: 'Vect3', buttons: 'int', modifiers: 'int') -> 'None'`
- `on_mouse_motion(self, point: 'Vect3', d_point: 'Vect3') -> 'None'`
- `on_mouse_press(self, point: 'Vect3', button: 'int', mods: 'int') -> 'None'`
- `on_mouse_release(self, point: 'Vect3', button: 'int', mods: 'int') -> 'None'`
- `on_mouse_scroll(self, point: 'Vect3', offset: 'Vect3', x_pixel_offset: 'float', y_pixel_offset: 'float') -> 'None'`
- `on_resize(self, width: 'int', height: 'int') -> 'None'`
- `on_show(self) -> 'None'`
- `play(self, *proto_animations: 'Animation | _AnimationBuilder', run_time: 'float | None' = None, rate_func: 'Callable[[float], float] | None' = None, lag_ratio: 'float | None' = None) -> 'None'`
- `point_to_mobject(self, point: 'np.ndarray', search_set: 'Iterable[Mobject] | None' = None, buff: 'float' = 0) -> 'Mobject | None'` — E.g. if clicking on the scene, this returns the top layer mobject
- `post_play(self)`
- `pre_play(self)`
- `progress_through_animations(self, animations: 'Iterable[Animation]') -> 'None'`
- `redo(self)`
- `remove(self, *mobjects_to_remove: 'Mobject')` — Removes anything in mobjects from scenes mobject list, but in the event that one
- `remove_all_except(self, *mobjects_to_keep: 'Mobject')`
- `replace(self, mobject: 'Mobject', *replacements: 'Mobject')`
- `restore_state(self, scene_state: 'SceneState')`
- `revert_to_original_skipping_status(self)`
- `run(self) -> 'None'`
- `save_state(self) -> 'None'`
- `set_background_color(self, background_color, background_opacity=1) -> 'None'`
- `set_floor_plane(self, plane: 'str' = 'xy')`
- `setup(self) -> 'None'` — This is meant to be implement by any scenes which
- `should_update_mobjects(self) -> 'bool'`
- `show(self) -> 'None'`
- `stop_skipping(self) -> 'None'`
- `tear_down(self) -> 'None'`
- `temp_config_change(self, skip=False, record=False, progress_bar=False)`
- `temp_progress_bar(self)`
- `temp_record(self)`
- `temp_skip(self)`
- `undo(self)`
- `update_frame(self, dt: 'float' = 0, force_draw: 'bool' = False) -> 'None'`
- `update_mobjects(self, dt: 'float') -> 'None'`
- `update_skipping_status(self) -> 'None'`
- `wait(self, duration: 'Optional[float]' = None, stop_condition: 'Callable[[], bool]' = None, note: 'str' = None, ignore_presenter_mode: 'bool' = False)`
- `wait_until(self, stop_condition: 'Callable[[], bool]', max_time: 'float' = 60)`

</details>

### `SceneFileWriter(scene: 'Scene', write_to_movie: 'bool' = False, subdivide_output: 'bool' = False, png_mode: 'str' = 'RGBA', save_last_frame: 'bool' = False, movie_file_extension: 'str' = '.mp4', output_directory: 'str' = '.', file_name: 'str | None' = None, open_file_upon_completion: 'bool' = False, show_file_location_upon_completion: 'bool' = False, quiet: 'bool' = False, total_frames: 'int' = 0, progress_description_len: 'int' = 40, ffmpeg_bin: 'str' = 'ffmpeg', video_codec: 'str' = 'libx264', pixel_format: 'str' = 'yuv420p', crf: 'int | None' = None, saturation: 'float' = 1.0, gamma: 'float' = 1.0)`

<details><summary>métodos próprios (32) · herdados: 0</summary>

- `__init__(self, scene: 'Scene', write_to_movie: 'bool' = False, subdivide_output: 'bool' = False, png_mode: 'str' = 'RGBA', save_last_frame: 'bool' = False, movie_file_extension: 'str' = '.mp4', output_directory: 'str' = '.', file_name: 'str | None' = None, open_file_upon_completion: 'bool' = False, show_file_location_upon_completion: 'bool' = False, quiet: 'bool' = False, total_frames: 'int' = 0, progress_description_len: 'int' = 40, ffmpeg_bin: 'str' = 'ffmpeg', video_codec: 'str' = 'libx264', pixel_format: 'str' = 'yuv420p', crf: 'int | None' = None, saturation: 'float' = 1.0, gamma: 'float' = 1.0)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_audio_segment(self, new_segment: 'AudioSegment', time: 'float | None' = None, gain_to_background: 'float | None' = None) -> 'None'`
- `add_sound(self, sound_file: 'str', time: 'float | None' = None, gain: 'float | None' = None, gain_to_background: 'float | None' = None) -> 'None'`
- `add_sound_to_video(self) -> 'None'`
- `begin(self) -> 'None'`
- `begin_animation(self) -> 'None'`
- `begin_insert(self)`
- `close_movie_pipe(self) -> 'None'`
- `create_audio_segment(self) -> 'None'`
- `end_animation(self) -> 'None'`
- `end_insert(self)`
- `finish(self) -> 'None'`
- `get_image_file_path(self) -> 'str'`
- `get_insert_file_path(self, index: 'int') -> 'Path'`
- `get_movie_file_path(self) -> 'str'`
- `get_next_partial_movie_path(self) -> 'str'`
- `get_output_file_name(self) -> 'str'`
- `get_output_file_rootname(self) -> 'Path'`
- `has_progress_display(self)`
- `init_audio(self) -> 'None'`
- `init_image_file_path(self) -> 'Path'`
- `init_movie_file_path(self) -> 'Path'`
- `init_output_directories(self) -> 'None'`
- `init_partial_movie_directory(self)`
- `open_file(self) -> 'None'`
- `open_movie_pipe(self, file_path: 'str') -> 'None'`
- `print_file_ready_message(self, file_path: 'str') -> 'None'`
- `save_final_image(self, image: 'Image') -> 'None'`
- `set_progress_display_description(self, file: 'str' = '', sub_desc: 'str' = '') -> 'None'`
- `should_open_file(self) -> 'bool'`
- `use_fast_encoding(self)`
- `write_frame(self) -> 'None'`

</details>

### `SceneState(scene: 'Scene', ignore: 'list[Mobject] | None' = None)`

<details><summary>métodos próprios (4) · herdados: 0</summary>

- `__init__(self, scene: 'Scene', ignore: 'list[Mobject] | None' = None)` — Initialize self.  See help(type(self)) for accurate signature.
- `mobjects_match(self, state: 'SceneState')`
- `n_changes(self, state: 'SceneState')`
- `restore_scene(self, scene: 'Scene')`

</details>

### `ThreeDScene(window: 'Optional[Window]' = None, camera_config: 'dict' = {}, file_writer_config: 'dict' = {}, skip_animations: 'bool' = False, always_update_mobjects: 'bool' = False, start_at_animation_number: 'int | None' = None, end_at_animation_number: 'int | None' = None, show_animation_progress: 'bool' = False, leave_progress_bars: 'bool' = False, preview_while_skipping: 'bool' = True, presenter_mode: 'bool' = False, default_wait_time: 'float' = 1.0, invert_zoom_scroll: 'bool' = False)` ← Scene

<details><summary>métodos próprios (1) · herdados: 77</summary>

- `add(self, *mobjects: 'Mobject', set_depth_test: 'bool' = True, perp_stroke: 'bool' = True)` — Mobjects will be displayed, from background to

</details>

- `ARROW_SYMBOLS` = `[57344, 57346, 57345, 57347]`
- `COLOR_KEY` = `'c'`
- `CURSOR_KEY` = `'k'`
- `DEG` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `FRAME_HEIGHT` = `8.0`
- `FRAME_WIDTH` = `14.222222222222221`
- `GRAB_KEY` = `'g'`
- `GRAB_KEYS` = `['g', 'h', 'v', 'z']`
- `GREY_A` = `'#DDDDDD'`
- `GREY_C` = `'#888888'`
- `INFORMATION_KEY` = `'i'`
- `LEFT` = `array([-1.,  0.,  0.])`
- `MANIM_COLORS` = `['#1C758A', '#29ABCA', '#58C4DD', '#9CDCEB', '#C7E9F1', '#49A88F', '#55C1A7', '#5CD0B3', '#76DDC0', '#ACEAD7', '#699C...`
- `ORIGIN` = `array([0., 0., 0.])`
- `PI` = `3.141592653589793`
- `RED` = `'#FC6255'`
- `RESIZE_KEY` = `'t'`
- `RIGHT` = `array([1., 0., 0.])`
- `SELECT_KEY` = `'s'`
- `SMALL_BUFF` = `0.1`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `UNSELECT_KEY` = `'u'`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `WHITE` = `'#FFFFFF'`
- `X_GRAB_KEY` = `'h'`
- `Y_GRAB_KEY` = `'v'`
- `Z_GRAB_KEY` = `'z'`

## typing

- `TYPE_CHECKING` = `False`

## utils/bezier

- `CLOSED_THRESHOLD` = `0.001`
- `TYPE_CHECKING` = `False`
- **`approx_smooth_quadratic_bezier_handles(points: 'FloatArray') -> 'FloatArray'`** — Figuring out which bezier curves most smoothly connect a sequence of points.
- **`bezier(points: 'Sequence[float | FloatArray] | VectNArray') -> 'Callable[[float], float | FloatArray]'`**
- **`diag_to_matrix(l_and_u: 'tuple[int, int]', diag: 'np.ndarray') -> 'np.ndarray'`** — Converts array whose rows represent diagonal
- **`get_quadratic_approximation_of_cubic(a0: 'FloatArray', h0: 'FloatArray', h1: 'FloatArray', a1: 'FloatArray') -> 'FloatArray'`**
- **`get_smooth_cubic_bezier_handle_points(points: 'Sequence[VectN] | VectNArray') -> 'tuple[FloatArray, FloatArray]'`**
- **`get_smooth_quadratic_bezier_path_through(points: 'Sequence[VectN]') -> 'np.ndarray'`**
- **`integer_interpolate(start: 'int', end: 'int', alpha: 'float') -> 'tuple[int, float]'`** — alpha is a float between 0 and 1.  This returns
- **`interpolate(start: 'Scalable', end: 'Scalable', alpha: 'float | VectN') -> 'Scalable'`**
- **`inverse_interpolate(start: 'Scalable', end: 'Scalable', value: 'Scalable') -> 'np.ndarray'`**
- **`is_closed(points: 'FloatArray') -> 'bool'`**
- **`match_interpolate(new_start: 'Scalable', new_end: 'Scalable', old_start: 'Scalable', old_end: 'Scalable', old_value: 'Scalable') -> 'Scalable'`**
- **`mid(start: 'Scalable', end: 'Scalable') -> 'Scalable'`**
- **`outer_interpolate(start: 'Scalable', end: 'Scalable', alpha: 'Scalable') -> 'np.ndarray'`**
- **`partial_bezier_points(points: 'Sequence[Scalable]', a: 'float', b: 'float') -> 'list[Scalable]'`** — Given an list of points which define
- **`partial_quadratic_bezier_points(points: 'Sequence[VectN] | VectNArray', a: 'float', b: 'float') -> 'list[VectN]'`**
- **`quadratic_bezier_points_for_arc(angle: 'float', n_components: 'int' = 8)`**
- **`set_array_by_interpolation(arr: 'np.ndarray', arr1: 'np.ndarray', arr2: 'np.ndarray', alpha: 'float', interp_func: 'Callable[[np.ndarray, np.ndarray, float], np.ndarray]' = <function interpolate at 0x7f6ff5270400>) -> 'np.ndarray'`**
- **`smooth_quadratic_path(anchors: 'Vect3Array') -> 'Vect3Array'`** — Returns a path defining a smooth quadratic bezier spline

## utils/color

- `COLORMAP_3B1B` = `['#1C758A', '#83C167', '#FFFF00', '#FC6255']`
- `TYPE_CHECKING` = `False`
- `WHITE` = `'#FFFFFF'`
- **`average_color(*colors: 'ManimColor') -> 'Color'`**
- **`color_gradient(reference_colors: 'Iterable[ManimColor]', length_of_output: 'int', interp_by_hsl: 'bool' = False) -> 'list[Color]'`**
- **`color_to_hex(color: 'ManimColor') -> 'str'`**
- **`color_to_int_rgb(color: 'ManimColor') -> 'np.ndarray[int, np.dtype[np.uint8]]'`**
- **`color_to_int_rgba(color: 'ManimColor', opacity: 'float' = 1.0) -> 'np.ndarray[int, np.dtype[np.uint8]]'`**
- **`color_to_rgb(color: 'ManimColor') -> 'Vect3'`**
- **`color_to_rgba(color: 'ManimColor', alpha: 'float' = 1.0) -> 'Vect4'`**
- **`get_color_map(map_name: 'str') -> 'Callable[[Sequence[float]], Vect4Array]'`**
- **`get_colormap_from_colors(colors: 'Iterable[ManimColor]') -> 'Callable[[Sequence[float]], Vect4Array]'`** — Returns a funciton which takes in values between 0 and 1, and returns
- **`get_colormap_list(map_name: 'str' = 'viridis', n_colors: 'int' = 9) -> 'Vect3Array'`** — Options for map_name:
- **`hex_to_int(rgb_hex: 'str') -> 'int'`**
- **`hex_to_rgb(hex_code: 'str') -> 'Vect3'`**
- **`int_to_hex(rgb_int: 'int') -> 'str'`**
- **`interpolate_color(color1: 'ManimColor', color2: 'ManimColor', alpha: 'float', interp_by_hsl: 'bool' = False) -> 'Color'`**
- **`interpolate_color_by_hsl(color1: 'ManimColor', color2: 'ManimColor', alpha: 'float') -> 'Color'`**
- **`invert_color(color: 'ManimColor') -> 'Color'`**
- **`random_bright_color(hue_range: 'tuple[float, float]' = (0.0, 1.0), saturation_range: 'tuple[float, float]' = (0.5, 0.8), luminance_range: 'tuple[float, float]' = (0.5, 1.0)) -> 'Color'`**
- **`random_color() -> 'Color'`**
- **`rgb_to_color(rgb: 'Vect3 | Sequence[float]') -> 'Color'`**
- **`rgb_to_hex(rgb: 'Vect3 | Sequence[float]') -> 'str'`**
- **`rgba_to_color(rgba: 'Vect4') -> 'Color'`**

## utils/other

### `StructuredArray(dtype: 'np.dtype', length: 'int' = 0)`
> A structured numpy array laid out to match what a shader reads, and read from python as a

<details><summary>métodos próprios (12) · herdados: 0</summary>

- `__init__(self, dtype: 'np.dtype', length: 'int' = 0)` — Initialize self.  See help(type(self)) for accurate signature.
- `being_written(self) -> 'Iterator[np.ndarray]'` — The rows, for writing into. Writes made through the view this hands back cannot be
- `copy(self) -> 'Self'`
- `interpolate(self, array1: 'StructuredArray', array2: 'StructuredArray', alpha: 'float', keys_to_alt_func: 'dict[str, Callable] | None' = None) -> 'None'` — Takes on the blend of two others, every field at once.
- `keys(self) -> 'Sequence[str]'`
- `match(self, other: 'StructuredArray') -> 'None'` — Takes on another's values, field by field where the two are laid out
- `note_change(self) -> 'None'` — Says that the array was written to through a view onto it, which it cannot count
- `prepare_interpolation(self, array1: 'StructuredArray', array2: 'StructuredArray') -> 'None'` — Settles what a blend between these two comes to for as long as the pair stands:
- `resize(self, length: 'int', resize_func: 'Callable[[np.ndarray, int], np.ndarray]' = <function resize_array at 0x7f7058a8fec0>) -> 'None'` — Emptying the array keeps hold of its first row, and growing from empty starts
- `set_array(self, array: 'np.ndarray') -> 'None'` — The array, along with the two ways of seeing the whole of it at once: every field as one
- `turn_off_interpolation_skip(self) -> 'None'`
- `update(self, values: 'Mapping | None' = None, **kwargs) -> 'None'` — Fields the array has no room for are passed over, since one mobject's values

</details>

- `BLACK` = `'#000000'`
- `CACHE_SIZE` = `1000000000.0`
- `FRAME_HEIGHT` = `8.0`
- `FRAME_WIDTH` = `14.222222222222221`
- `OUT` = `array([0., 0., 1.])`
- `STRAIGHT_PATH_THRESHOLD` = `0.01`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- **`adjacent_n_tuples(objects: 'Sequence[T]', n: 'int') -> 'zip[tuple[T, ...]]'`**
- **`adjacent_pairs(objects: 'Sequence[T]') -> 'zip[tuple[T, T]]'`**
- **`arr_clip(arr: 'np.ndarray', min_a: 'float', max_a: 'float') -> 'np.ndarray'`**
- **`array_is_constant(arr: 'np.ndarray') -> 'bool'`**
- **`arrays_match(arr1: 'np.ndarray', arr2: 'np.ndarray') -> 'bool'`**
- **`batch_by_comparison(items: 'Iterable[T]', comparison: 'Callable[[T, T], bool]') -> 'List[List[T]]'`** — Runs of consecutive items, each item joining the one before it wherever the comparison
- **`batch_by_property(items: 'Iterable[T]', property_func: 'Callable[[T], S]') -> 'list[tuple[T, S]]'`** — Takes in a list, and returns a list of tuples, (batch, prop)
- **`binary_search(function: 'Callable[[float], float]', target: 'float', lower_bound: 'float', upper_bound: 'float', tolerance: 'float' = 0.0001) -> 'float | None'`**
- **`cache_on_disk(func: 'Callable[..., T]') -> 'Callable[..., T]'`**
- **`cartesian_product(*arrays: 'np.ndarray')`** — Copied from https://stackoverflow.com/a/11146645
- **`clear_cache()`**
- **`clip(a: 'float', min_a: 'float', max_a: 'float') -> 'float'`**
- **`clockwise_path() -> 'Callable[[Vect3Array, Vect3Array, float], Vect3Array]'`**
- **`counterclockwise_path() -> 'Callable[[Vect3Array, Vect3Array, float], Vect3Array]'`**
- **`extract_mobject_family_members(mobject_list: 'Iterable[Mobject]', exclude_pointless: 'bool' = False) -> 'list[Mobject]'`**
- **`fdiv(a: 'Scalable', b: 'Scalable', zero_over_zero_value: 'Scalable | None' = None) -> 'Scalable'`** — Less heavyweight name for np.true_divide, enabling
- **`find_file(file_name: 'str', directories: 'Iterable[str] | None' = None, extensions: 'Iterable[str] | None' = None) -> 'Path'`**
- **`gen_choose(n: 'int', r: 'int') -> 'int'`**
- **`get_cache_dir() -> 'str'`**
- **`get_directories() -> 'dict[str, str]'`**
- **`get_downloads_dir() -> 'str'`**
- **`get_full_raster_image_path(image_file_name: 'str') -> 'str'`**
- **`get_full_sound_file_path(sound_file_name: 'str') -> 'str'`**
- **`get_full_three_d_model_path(model_file_name: 'str') -> 'str'`**
- **`get_full_vector_image_path(image_file_name: 'str') -> 'str'`**
- **`get_num_args(function: 'Callable') -> 'int'`**
- **`get_output_dir() -> 'str'`**
- **`get_parameters(function: 'Callable') -> 'Iterable[str]'`**
- **`get_raster_image_dir() -> 'str'`**
- **`get_shader_dir() -> 'str'`**
- **`get_sound_dir() -> 'str'`**
- **`get_temp_dir() -> 'str'`**
- **`get_three_d_model_dir() -> 'str'`**
- **`get_vector_image_dir() -> 'str'`**
- **`guarantee_existence(path: 'str | Path') -> 'Path'`**
- **`hash_obj(obj: 'object') -> 'int'`**
- **`hash_string(string: 'str', n_bytes=16) -> 'str'`**
- **`index_labels(mobject: 'Mobject', label_height: 'float' = 0.15) -> 'VGroup'`**
- **`index_within_group(counts: 'np.ndarray') -> 'np.ndarray'`** — Where each member of a run of groups sits within its own group, given how many members
- **`invert_image(image: 'Iterable') -> 'Image.Image'`**
- **`keep_larger(start: 'np.ndarray', end: 'np.ndarray', alpha: 'float') -> 'np.ndarray'`** — Takes in both rather than blending between them, for a field which counts something and
- **`list_difference_update(l1: 'Iterable[T]', l2: 'Iterable[T]') -> 'list[T]'`**
- **`list_update(l1: 'Iterable[T]', l2: 'Iterable[T]') -> 'list[T]'`** — Used instead of list(set(l1).update(l2)) to maintain order,
- **`listify(obj: 'object') -> 'list'`**
- **`make_even(iterable_1: 'Sequence[T]', iterable_2: 'Sequence[S]') -> 'tuple[Sequence[T], Sequence[S]]'`**
- **`merge_dicts_recursively(*dicts)`** — Creates a dict whose keyset is the union of all the
- **`path_along_arc(arc_angle: 'float | Tuple[float, float] | np.ndarray', axis: 'Vect3' = array([0., 0., 1.])) -> 'Callable[[Vect3Array, Vect3Array, float], Vect3Array]'`** — arc_angle can be a single angle, or a pair of angles, in which case
- **`play_sound(sound_file)`** — Play a sound file using the system's audio player
- **`print_family(mobject: 'Mobject', n_tabs: 'int' = 0) -> 'None'`** — For debugging purposes
- **`recursive_mobject_remove(mobjects: 'List[Mobject]', to_remove: 'Set[Mobject]') -> 'Tuple[List[Mobject], bool]'`** — Takes in a list of mobjects, together with a set of mobjects to remove.
- **`remove_list_redundancies(lst: 'Sequence[T]') -> 'list[T]'`** — Remove duplicate elements while preserving order.
- **`resize_array(nparray: 'np.ndarray', length: 'int') -> 'np.ndarray'`**
- **`resize_preserving_order(nparray: 'np.ndarray', length: 'int') -> 'np.ndarray'`**
- **`resize_with_interpolation(nparray: 'np.ndarray', length: 'int') -> 'np.ndarray'`**
- **`shuffled(iterable: 'Iterable') -> 'list'`**
- **`sigmoid(x: 'float | FloatArray')`**
- **`straight_path(start_points: 'np.ndarray', end_points: 'np.ndarray', alpha: 'float') -> 'np.ndarray'`** — Same function as interpolate, but renamed to reflect
- **`vmobject_to_svg(vmobject, filename: 'str | None' = None, pixel_width: 'int' = 1920, pixel_height: 'int' = 1080) -> 'str'`** — Convert a VMobject (and its family) to an SVG string.

## utils/rate_functions

- `TYPE_CHECKING` = `False`
- **`double_smooth(t: 'float') -> 'float'`**
- **`exponential_decay(t: 'float', half_life: 'float' = 0.1) -> 'float'`**
- **`linear(t: 'float') -> 'float'`**
- **`lingering(t: 'float') -> 'float'`**
- **`not_quite_there(func: 'Callable[[float], float]' = <function smooth at 0x7f6ff39332e0>, proportion: 'float' = 0.7) -> 'Callable[[float], float]'`**
- **`overshoot(t: 'float', pull_factor: 'float' = 1.5) -> 'float'`**
- **`running_start(t: 'float', pull_factor: 'float' = -0.5) -> 'float'`**
- **`rush_from(t: 'float') -> 'float'`**
- **`rush_into(t: 'float') -> 'float'`**
- **`slow_into(t: 'float') -> 'float'`**
- **`smooth(t: 'float') -> 'float'`**
- **`squish_rate_func(func: 'Callable[[float], float]', a: 'float' = 0.4, b: 'float' = 0.6) -> 'Callable[[float], float]'`**
- **`there_and_back(t: 'float') -> 'float'`**
- **`there_and_back_with_pause(t: 'float', pause_ratio: 'float' = 0.3333333333333333) -> 'float'`**
- **`wiggle(t: 'float', wiggles: 'float' = 2) -> 'float'`**

## utils/space_ops

- `DOWN` = `array([ 0., -1.,  0.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `RIGHT` = `array([1., 0., 0.])`
- `TAU` = `6.283185307179586`
- `TYPE_CHECKING` = `False`
- `UP` = `array([0., 1., 0.])`
- **`R3_to_complex(point: 'Vect3') -> 'complex'`**
- **`angle_axis_from_quaternion(quat: 'Vect4') -> 'Tuple[float, Vect3]'`**
- **`angle_between_vectors(v1: 'VectN', v2: 'VectN') -> 'float'`** — Returns the angle between two 3D vectors.
- **`angle_of_vector(vector: 'Vect2 | Vect3') -> 'float'`** — Returns polar coordinate theta when vector is project on xy plane
- **`boxes_are_disjoint(mins: 'Vect3Array', maxs: 'Vect3Array') -> 'bool'`** — Whether no two of the boxes with these lower and upper corners share any of their
- **`center_of_mass(points: 'Sequence[Vect3]') -> 'Vect3'`**
- **`compass_directions(n: 'int' = 4, start_vect: 'Vect3' = array([1., 0., 0.])) -> 'Vect3'`**
- **`complex_func_to_R3_func(complex_func: 'Callable[[complex], complex]') -> 'Callable[[Vect3], Vect3]'`**
- **`complex_to_R3(complex_num: 'complex') -> 'Vect3'`**
- **`cross(v1: 'Vect3 | List[float]', v2: 'Vect3 | List[float]', out: 'np.ndarray | None' = None) -> 'Vect3 | Vect3Array'`**
- **`cross2d(a: 'Vect2 | Vect2Array', b: 'Vect2 | Vect2Array') -> 'Vect2 | Vect2Array'`**
- **`find_intersection(p0: 'Vect3 | Vect3Array', v0: 'Vect3 | Vect3Array', p1: 'Vect3 | Vect3Array', v1: 'Vect3 | Vect3Array', threshold: 'float' = 1e-05) -> 'Vect3'`** — Return the intersection of a line passing through p0 in direction v0
- **`get_closest_point_on_line(a: 'VectN', b: 'VectN', p: 'VectN') -> 'VectN'`** — It returns point x such that
- **`get_dist(vect1: 'VectN', vect2: 'VectN')`**
- **`get_norm(vect: 'VectN | List[float]') -> 'float'`**
- **`get_unit_normal(v1: 'Vect3', v2: 'Vect3', tol: 'float' = 1e-06) -> 'Vect3'`**
- **`get_winding_number(points: 'Sequence[Vect2 | Vect3]') -> 'float'`**
- **`line_intersection(line1: 'Tuple[Vect3, Vect3]', line2: 'Tuple[Vect3, Vect3]') -> 'Vect3'`** — return intersection point of two lines,
- **`line_intersects_path(start: 'Vect2 | Vect3', end: 'Vect2 | Vect3', path: 'Vect2Array | Vect3Array') -> 'bool'`** — Tests whether the line (start, end) intersects
- **`midpoint(point1: 'VectN', point2: 'VectN') -> 'VectN'`**
- **`normalize(vect: 'VectN | List[float]', fall_back: 'VectN | List[float] | None' = None) -> 'VectN'`**
- **`normalize_along_axis(array: 'np.ndarray', axis: 'int') -> 'np.ndarray'`**
- **`poly_line_length(points)`** — Return the sum of the lengths between adjacent points
- **`project_along_vector(point: 'Vect3', vector: 'Vect3') -> 'Vect3'`**
- **`quaternion_conjugate(quaternion: 'Vect4') -> 'Vect4'`**
- **`quaternion_from_angle_axis(angle: 'float', axis: 'Vect3') -> 'Vect4'`**
- **`quaternion_mult(*quats: 'Vect4') -> 'Vect4'`** — Inputs are treated as quaternions, where the real part is the
- **`rotate_vector(vector: 'Vect3', angle: 'float', axis: 'Vect3' = array([0., 0., 1.])) -> 'Vect3'`**
- **`rotate_vector_2d(vector: 'Vect2', angle: 'float') -> 'Vect2'`**
- **`rotation_about_z(angle: 'float') -> 'Matrix3x3'`**
- **`rotation_between_vectors(v1: 'Vect3', v2: 'Vect3') -> 'Matrix3x3'`**
- **`rotation_matrix(angle: 'float', axis: 'Vect3') -> 'Matrix3x3'`** — Rotation in R^3 about a specified axis of rotation.
- **`rotation_matrix_from_quaternion(quat: 'Vect4') -> 'Matrix3x3'`**
- **`rotation_matrix_transpose(angle: 'float', axis: 'Vect3') -> 'Matrix3x3'`**
- **`rotation_matrix_transpose_from_quaternion(quat: 'Vect4') -> 'Matrix3x3'`**
- **`thick_diagonal(dim: 'int', thickness: 'int' = 2) -> 'np.ndarray'`**
- **`z_to_vector(vector: 'Vect3') -> 'Matrix3x3'`**

## utils/tex

### `LatexError()` ← Exception
> Common base class for all non-exit exceptions.

- `TEX_TO_SYMBOL_COUNT` = `{'\\!': 0, '\\,': 0, '\\-': 0, '\\/': 0, '\\:': 0, '\\;': 0, '\\>': 0, '\\aa': 0, '\\AA': 0, '\\ae': 0, '\\AE': 0, '\...`
- `TEX_TO_SYMBOL_COUNT` = `{'\\!': 0, '\\,': 0, '\\-': 0, '\\/': 0, '\\:': 0, '\\;': 0, '\\>': 0, '\\aa': 0, '\\AA': 0, '\\ae': 0, '\\AE': 0, '\...`
- **`full_tex_to_svg(full_tex: 'str', compiler: 'str' = 'latex', message: 'str' = '')`**
- **`get_full_tex(content: 'str', preamble: 'str' = '')`**
- **`get_tex_template_config(template_name: 'str') -> 'dict[str, str]'`**
- **`remove_tex_environments(tex: 'str') -> 'str'`**

