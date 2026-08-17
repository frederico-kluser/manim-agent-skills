# API de `manim` v0.21.0

5523 símbolos públicos · 50945 métodos indexados · Python 3.12.3

Gerado por `mx api-dump` a partir do pacote instalado. Regenere após atualizar o Manim.

## Categorias

- [`animation/changing`](#animationchanging) — 7 símbolos
- [`animation/composition`](#animationcomposition) — 6 símbolos
- [`animation/core`](#animationcore) — 8 símbolos
- [`animation/creation`](#animationcreation) — 17 símbolos
- [`animation/fading`](#animationfading) — 3 símbolos
- [`animation/growing`](#animationgrowing) — 7 símbolos
- [`animation/indication`](#animationindication) — 72 símbolos
- [`animation/movement`](#animationmovement) — 6 símbolos
- [`animation/numbers`](#animationnumbers) — 2 símbolos
- [`animation/rotation`](#animationrotation) — 6 símbolos
- [`animation/specialized`](#animationspecialized) — 62 símbolos
- [`animation/speed`](#animationspeed) — 2 símbolos
- [`animation/transform`](#animationtransform) — 30 símbolos
- [`animation/updaters`](#animationupdaters) — 16 símbolos
- [`camera`](#camera) — 138 símbolos
- [`config`](#config) — 14 símbolos
- [`constants`](#constants) — 65 símbolos
- [`mobject/3d`](#mobject3d) — 96 símbolos
- [`mobject/core`](#mobjectcore) — 281 símbolos
- [`mobject/geometry`](#mobjectgeometry) — 384 símbolos
- [`mobject/graph`](#mobjectgraph) — 6 símbolos
- [`mobject/graphing`](#mobjectgraphing) — 216 símbolos
- [`mobject/logo`](#mobjectlogo) — 2 símbolos
- [`mobject/matrix`](#mobjectmatrix) — 68 símbolos
- [`mobject/opengl`](#mobjectopengl) — 546 símbolos
- [`mobject/svg`](#mobjectsvg) — 72 símbolos
- [`mobject/table`](#mobjecttable) — 7 símbolos
- [`mobject/text`](#mobjecttext) — 272 símbolos
- [`mobject/value_tracker`](#mobjectvalue_tracker) — 3 símbolos
- [`mobject/vector_field`](#mobjectvector_field) — 12 símbolos
- [`other`](#other) — 189 símbolos
- [`plugins`](#plugins) — 2 símbolos
- [`renderer`](#renderer) — 89 símbolos
- [`scene`](#scene) — 213 símbolos
- [`typing`](#typing) — 1 símbolos
- [`utils/bezier`](#utilsbezier) — 22 símbolos
- [`utils/color`](#utilscolor) — 2335 símbolos
- [`utils/other`](#utilsother) — 137 símbolos
- [`utils/rate_functions`](#utilsrate_functions) — 50 símbolos
- [`utils/space_ops`](#utilsspace_ops) — 43 símbolos
- [`utils/tex`](#utilstex) — 16 símbolos

## animation/changing

### `AnimatedBoundary(vmobject: 'VMobject', colors: 'Sequence[ParsableManimColor]' = [ManimColor('#29ABCA'), ManimColor('#9CDCEB'), ManimColor('#236B8E'), ManimColor('#736357')], max_stroke_width: 'float' = 3, cycle_rate: 'float' = 0.5, back_and_forth: 'bool' = True, draw_rate_func: 'RateFunction' = <function smooth at 0x713b879e5e40>, fade_rate_func: 'RateFunction' = <function smooth at 0x713b879e5e40>, **kwargs: 'Any')` ← VGroup
> Boundary of a :class:`.VMobject` with animated color change.

<details><summary>métodos próprios (3) · herdados: 242</summary>

- `__init__(self, vmobject: 'VMobject', colors: 'Sequence[ParsableManimColor]' = [ManimColor('#29ABCA'), ManimColor('#9CDCEB'), ManimColor('#236B8E'), ManimColor('#736357')], max_stroke_width: 'float' = 3, cycle_rate: 'float' = 0.5, back_and_forth: 'bool' = True, draw_rate_func: 'RateFunction' = <function smooth at 0x713b879e5e40>, fade_rate_func: 'RateFunction' = <function smooth at 0x713b879e5e40>, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `full_family_become_partial(self, mob1: 'VMobject', mob2: 'VMobject', a: 'float', b: 'float') -> 'Self'`
- `update_boundary_copies(self, dt: 'float') -> 'None'`

</details>

### `TracedPath(traced_point_func: 'Callable', stroke_width: 'float' = 2, stroke_color: 'ParsableManimColor | None' = ManimColor('#FFFFFF'), dissipating_time: 'float | None' = None, **kwargs: 'Any') -> 'None'` ← VMobject
> Traces the path of a point returned by a function call.

<details><summary>métodos próprios (2) · herdados: 242</summary>

- `__init__(self, traced_point_func: 'Callable', stroke_width: 'float' = 2, stroke_color: 'ParsableManimColor | None' = ManimColor('#FFFFFF'), dissipating_time: 'float | None' = None, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `update_path(self, mob: 'Mobject', dt: 'float') -> 'None'`

</details>

- `BLUE_B` = `ManimColor('#9CDCEB')`
- `BLUE_D` = `ManimColor('#29ABCA')`
- `BLUE_E` = `ManimColor('#236B8E')`
- `GREY_BROWN` = `ManimColor('#736357')`
- `WHITE` = `ManimColor('#FFFFFF')`

## animation/composition

### `AnimationGroup(*animations: 'Animation | Iterable[Animation]', group: 'Group | VGroup | OpenGLGroup | OpenGLVGroup | None' = None, run_time: 'float | None' = None, rate_func: 'Callable[[float], float]' = <function linear at 0x713b879e5d00>, lag_ratio: 'float' = 0, **kwargs: 'Any')` ← Animation
> Plays a group or series of :class:`~.Animation`.

<details><summary>métodos próprios (9) · herdados: 15</summary>

- `__init__(self, *animations: 'Animation | Iterable[Animation]', group: 'Group | VGroup | OpenGLGroup | OpenGLVGroup | None' = None, run_time: 'float | None' = None, rate_func: 'Callable[[float], float]' = <function linear at 0x713b879e5d00>, lag_ratio: 'float' = 0, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'` — Begin the animation.
- `build_animations_with_timings(self) -> 'None'` — Creates a list of triplets of the form (anim, start_time, end_time).
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'` — Clean up the :class:`~.Scene` after finishing the animation.
- `finish(self) -> 'None'` — Finish the animation.
- `get_all_mobjects(self) -> 'Sequence[Mobject | OpenGLMobject]'` — Get all mobjects involved in the animation.
- `init_run_time(self, run_time: 'float | None') -> 'float'` — Calculates the run time of the animation, if different from ``run_time``.
- `interpolate(self, alpha: 'float') -> 'None'` — Set the animation progress.
- `update_mobjects(self, dt: 'float') -> 'None'` — Updates things like starting_mobject, and (for

</details>

### `LaggedStart(*animations: 'Animation', lag_ratio: 'float' = 0.05, **kwargs: 'Any')` ← AnimationGroup
> Adjusts the timing of a series of :class:`~.Animation` according to ``lag_ratio``.

<details><summary>métodos próprios (1) · herdados: 23</summary>

- `__init__(self, *animations: 'Animation', lag_ratio: 'float' = 0.05, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `LaggedStartMap(animation_class: 'type[Animation]', mobject: 'Mobject', arg_creator: 'Callable[[Mobject], Iterable[Any]] | None' = None, run_time: 'float' = 2, lag_ratio: 'float' = 0.05, **kwargs: 'Any')` ← LaggedStart
> Plays a series of :class:`~.Animation` while mapping a function to submobjects.

<details><summary>métodos próprios (1) · herdados: 23</summary>

- `__init__(self, animation_class: 'type[Animation]', mobject: 'Mobject', arg_creator: 'Callable[[Mobject], Iterable[Any]] | None' = None, run_time: 'float' = 2, lag_ratio: 'float' = 0.05, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Succession(*animations: 'Animation', lag_ratio: 'float' = 1, **kwargs: 'Any')` ← AnimationGroup
> Plays a series of animations in succession.

<details><summary>métodos próprios (7) · herdados: 19</summary>

- `__init__(self, *animations: 'Animation', lag_ratio: 'float' = 1, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'` — Begin the animation.
- `finish(self) -> 'None'` — Finish the animation.
- `interpolate(self, alpha: 'float') -> 'None'` — Set the animation progress.
- `next_animation(self) -> 'None'` — Proceeds to the next animation.
- `update_active_animation(self, index: 'int') -> 'None'`
- `update_mobjects(self, dt: 'float') -> 'None'` — Updates things like starting_mobject, and (for

</details>

- `DEFAULT_LAGGED_START_LAG_RATIO` = `0.05`
- `TYPE_CHECKING` = `False`

## animation/core

### `Add(*mobjects: 'Mobject', run_time: 'float' = 0.0, **kwargs: 'Any') -> 'None'` ← Animation
> Add Mobjects to a scene, without animating them in any other way. This

<details><summary>métodos próprios (6) · herdados: 16</summary>

- `__init__(self, *mobjects: 'Mobject', run_time: 'float' = 0.0, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'` — Begin the animation.
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'` — Clean up the :class:`~.Scene` after finishing the animation.
- `finish(self) -> 'None'` — Finish the animation.
- `interpolate(self, alpha: 'float') -> 'None'` — Set the animation progress.
- `update_mobjects(self, dt: 'float') -> 'None'` — Updates things like starting_mobject, and (for

</details>

### `Animation(mobject=None, *args, use_override=True, **kwargs) -> 'Self'`
> An animation.

<details><summary>métodos próprios (22) · herdados: 0</summary>

- `__init__(self, mobject: 'Mobject | OpenGLMobject | None', lag_ratio: 'float' = 0.0, run_time: 'float' = 1.0, rate_func: 'Callable[[float], float]' = <function smooth at 0x713b879e5e40>, reverse_rate_function: 'bool' = False, name: 'str' = None, remover: 'bool' = False, suspend_mobject_updating: 'bool' = True, introducer: 'bool' = False, *, _on_finish: 'Callable[[Scene], None]' = <function Animation.<lambda> at 0x713b879ed620>, use_override: 'bool' = True) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'` — Begin the animation.
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'` — Clean up the :class:`~.Scene` after finishing the animation.
- `copy(self) -> 'Animation'` — Create a copy of the animation.
- `create_starting_mobject(self) -> 'Mobject | OpenGLMobject'`
- `finish(self) -> 'None'` — Finish the animation.
- `get_all_families_zipped(self) -> 'Iterable[tuple]'`
- `get_all_mobjects(self) -> 'Sequence[Mobject | OpenGLMobject]'` — Get all mobjects involved in the animation.
- `get_all_mobjects_to_update(self) -> 'list[Mobject]'` — Get all mobjects to be updated during the animation.
- `get_rate_func(self) -> 'Callable[[float], float]'` — Get the rate function of the animation.
- `get_run_time(self) -> 'float'` — Get the run time of the animation.
- `get_sub_alpha(self, alpha: 'float', index: 'int', num_submobjects: 'int') -> 'float'` — Get the animation progress of any submobjects subanimation.
- `interpolate(self, alpha: 'float') -> 'None'` — Set the animation progress.
- `interpolate_mobject(self, alpha: 'float') -> 'None'` — Interpolates the mobject of the :class:`Animation` based on alpha value.
- `interpolate_submobject(self, submobject: 'Mobject', starting_submobject: 'Mobject', alpha: 'float') -> 'Animation'`
- `is_introducer(self) -> 'bool'` — Test if the animation is an introducer.
- `is_remover(self) -> 'bool'` — Test if the animation is a remover.
- `set_default(**kwargs) -> 'None'` — Sets the default values of keyword arguments.
- `set_name(self, name: 'str') -> 'Animation'` — Set the name of the animation.
- `set_rate_func(self, rate_func: 'Callable[[float], float]') -> 'Animation'` — Set the rate function of the animation.
- `set_run_time(self, run_time: 'float') -> 'Animation'` — Set the run time of the animation.
- `update_mobjects(self, dt: 'float') -> 'None'` — Updates things like starting_mobject, and (for

</details>

### `Wait(run_time: 'float' = 1, stop_condition: 'Callable[[], bool] | None' = None, frozen_frame: 'bool | None' = None, rate_func: 'Callable[[float], float]' = <function linear at 0x713b879e5d00>, **kwargs)` ← Animation
> A "no operation" animation.

<details><summary>métodos próprios (6) · herdados: 16</summary>

- `__init__(self, run_time: 'float' = 1, stop_condition: 'Callable[[], bool] | None' = None, frozen_frame: 'bool | None' = None, rate_func: 'Callable[[float], float]' = <function linear at 0x713b879e5d00>, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'` — Begin the animation.
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'` — Clean up the :class:`~.Scene` after finishing the animation.
- `finish(self) -> 'None'` — Finish the animation.
- `interpolate(self, alpha: 'float') -> 'None'` — Set the animation progress.
- `update_mobjects(self, dt: 'float') -> 'None'` — Updates things like starting_mobject, and (for

</details>

- `DEFAULT_ANIMATION_LAG_RATIO` = `0.0`
- `DEFAULT_ANIMATION_RUN_TIME` = `1.0`
- `TYPE_CHECKING` = `False`
- **`override_animation(animation_class: 'type[Animation]') -> 'Callable[[Callable], Callable]'`** — Decorator used to mark methods as overrides for specific :class:`~.Animation` types.
- **`prepare_animation(anim: 'Animation | mobject._AnimationBuilder | opengl_mobject._AnimationBuilder') -> 'Animation'`** — Returns either an unchanged animation, or the animation built

## animation/creation

### `AddTextLetterByLetter(text: 'Text', suspend_mobject_updating: 'bool' = False, int_func: 'Callable[[np.ndarray], np.ndarray]' = <ufunc 'ceil'>, rate_func: 'Callable[[float], float]' = <function linear at 0x713b879e5d00>, time_per_char: 'float' = 0.1, run_time: 'float | None' = None, reverse_rate_function=False, introducer=True, **kwargs) -> 'None'` ← ShowIncreasingSubsets
> Show a :class:`~.Text` letter by letter on the scene.

<details><summary>métodos próprios (1) · herdados: 22</summary>

- `__init__(self, text: 'Text', suspend_mobject_updating: 'bool' = False, int_func: 'Callable[[np.ndarray], np.ndarray]' = <ufunc 'ceil'>, rate_func: 'Callable[[float], float]' = <function linear at 0x713b879e5d00>, time_per_char: 'float' = 0.1, run_time: 'float | None' = None, reverse_rate_function=False, introducer=True, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `AddTextWordByWord(text_mobject: 'Text', run_time: 'float' = None, time_per_char: 'float' = 0.06, **kwargs) -> 'None'` ← Succession
> Show a :class:`~.Text` word by word on the scene. Note: currently broken.

<details><summary>métodos próprios (1) · herdados: 25</summary>

- `__init__(self, text_mobject: 'Text', run_time: 'float' = None, time_per_char: 'float' = 0.06, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Create(mobject: 'VMobject | OpenGLVMobject | OpenGLSurface', lag_ratio: 'float' = 1.0, introducer: 'bool' = True, **kwargs) -> 'None'` ← ShowPartial
> Incrementally show a VMobject.

<details><summary>métodos próprios (1) · herdados: 21</summary>

- `__init__(self, mobject: 'VMobject | OpenGLVMobject | OpenGLSurface', lag_ratio: 'float' = 1.0, introducer: 'bool' = True, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `DrawBorderThenFill(vmobject: 'VMobject | OpenGLVMobject', run_time: 'float' = 2, rate_func: 'Callable[[float], float]' = <function double_smooth at 0x713b879e6700>, stroke_width: 'float' = 2, stroke_color: 'str' = None, introducer: 'bool' = True, **kwargs) -> 'None'` ← Animation
> Draw the border first and then show the fill.

<details><summary>métodos próprios (6) · herdados: 18</summary>

- `__init__(self, vmobject: 'VMobject | OpenGLVMobject', run_time: 'float' = 2, rate_func: 'Callable[[float], float]' = <function double_smooth at 0x713b879e6700>, stroke_width: 'float' = 2, stroke_color: 'str' = None, introducer: 'bool' = True, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'` — Begin the animation.
- `get_all_mobjects(self) -> 'Sequence[Mobject]'` — Get all mobjects involved in the animation.
- `get_outline(self) -> 'Mobject'`
- `get_stroke_color(self, vmobject: 'VMobject | OpenGLVMobject') -> 'ManimColor'`
- `interpolate_submobject(self, submobject: 'Mobject', starting_submobject: 'Mobject', outline, alpha: 'float') -> 'None'`

</details>

### `RemoveTextLetterByLetter(text: 'Text', suspend_mobject_updating: 'bool' = False, int_func: 'Callable[[np.ndarray], np.ndarray]' = <ufunc 'ceil'>, rate_func: 'Callable[[float], float]' = <function linear at 0x713b879e5d00>, time_per_char: 'float' = 0.1, run_time: 'float | None' = None, reverse_rate_function=True, introducer=False, remover=True, **kwargs) -> 'None'` ← AddTextLetterByLetter
> Remove a :class:`~.Text` letter by letter from the scene.

<details><summary>métodos próprios (1) · herdados: 22</summary>

- `__init__(self, text: 'Text', suspend_mobject_updating: 'bool' = False, int_func: 'Callable[[np.ndarray], np.ndarray]' = <ufunc 'ceil'>, rate_func: 'Callable[[float], float]' = <function linear at 0x713b879e5d00>, time_per_char: 'float' = 0.1, run_time: 'float | None' = None, reverse_rate_function=True, introducer=False, remover=True, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ShowIncreasingSubsets(group: 'Mobject', suspend_mobject_updating: 'bool' = False, int_func: 'Callable[[np.ndarray], np.ndarray]' = <ufunc 'floor'>, reverse_rate_function=False, **kwargs) -> 'None'` ← Animation
> Show one submobject at a time, leaving all previous ones displayed on screen.

<details><summary>métodos próprios (3) · herdados: 20</summary>

- `__init__(self, group: 'Mobject', suspend_mobject_updating: 'bool' = False, int_func: 'Callable[[np.ndarray], np.ndarray]' = <ufunc 'floor'>, reverse_rate_function=False, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_mobject(self, alpha: 'float') -> 'None'` — Interpolates the mobject of the :class:`Animation` based on alpha value.
- `update_submobject_list(self, index: 'int') -> 'None'`

</details>

### `ShowPartial(mobject: 'VMobject | OpenGLVMobject | OpenGLSurface | None', **kwargs)` ← Animation
> Abstract class for Animations that show the VMobject partially.

<details><summary>métodos próprios (2) · herdados: 20</summary>

- `__init__(self, mobject: 'VMobject | OpenGLVMobject | OpenGLSurface | None', **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_submobject(self, submobject: 'Mobject', starting_submobject: 'Mobject', alpha: 'float') -> 'None'`

</details>

### `ShowSubmobjectsOneByOne(group: 'Iterable[Mobject]', int_func: 'Callable[[np.ndarray], np.ndarray]' = <ufunc 'ceil'>, **kwargs) -> 'None'` ← ShowIncreasingSubsets
> Show one submobject at a time, removing all previously displayed ones from screen.

<details><summary>métodos próprios (2) · herdados: 21</summary>

- `__init__(self, group: 'Iterable[Mobject]', int_func: 'Callable[[np.ndarray], np.ndarray]' = <ufunc 'ceil'>, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `update_submobject_list(self, index: 'int') -> 'None'`

</details>

### `SpiralIn(shapes: 'Mobject', scale_factor: 'float' = 8, fade_in_fraction=0.3, **kwargs) -> 'None'` ← Animation
> Create the Mobject with sub-Mobjects flying in on spiral trajectories.

<details><summary>métodos próprios (2) · herdados: 20</summary>

- `__init__(self, shapes: 'Mobject', scale_factor: 'float' = 8, fade_in_fraction=0.3, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_mobject(self, alpha: 'float') -> 'None'` — Interpolates the mobject of the :class:`Animation` based on alpha value.

</details>

### `TypeWithCursor(text: 'Text', cursor: 'Mobject', buff: 'float' = 0.1, keep_cursor_y: 'bool' = True, leave_cursor_on: 'bool' = True, time_per_char: 'float' = 0.1, reverse_rate_function=False, introducer=True, **kwargs) -> 'None'` ← AddTextLetterByLetter
> Similar to :class:`~.AddTextLetterByLetter` , but with an additional cursor mobject at the end.

<details><summary>métodos próprios (5) · herdados: 18</summary>

- `__init__(self, text: 'Text', cursor: 'Mobject', buff: 'float' = 0.1, keep_cursor_y: 'bool' = True, leave_cursor_on: 'bool' = True, time_per_char: 'float' = 0.1, reverse_rate_function=False, introducer=True, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'` — Begin the animation.
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'` — Clean up the :class:`~.Scene` after finishing the animation.
- `finish(self) -> 'None'` — Finish the animation.
- `update_submobject_list(self, index: 'int') -> 'None'`

</details>

### `Uncreate(mobject: 'VMobject | OpenGLVMobject', reverse_rate_function: 'bool' = True, remover: 'bool' = True, **kwargs) -> 'None'` ← Create
> Like :class:`Create` but in reverse.

<details><summary>métodos próprios (1) · herdados: 21</summary>

- `__init__(self, mobject: 'VMobject | OpenGLVMobject', reverse_rate_function: 'bool' = True, remover: 'bool' = True, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `UntypeWithCursor(text: 'Text', cursor: 'VMobject | None' = None, time_per_char: 'float' = 0.1, reverse_rate_function=True, introducer=False, remover=True, **kwargs) -> 'None'` ← TypeWithCursor
> Similar to :class:`~.RemoveTextLetterByLetter` , but with an additional cursor mobject at the end.

<details><summary>métodos próprios (1) · herdados: 22</summary>

- `__init__(self, text: 'Text', cursor: 'VMobject | None' = None, time_per_char: 'float' = 0.1, reverse_rate_function=True, introducer=False, remover=True, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Unwrite(vmobject: 'VMobject', rate_func: 'Callable[[float], float]' = <function linear at 0x713b879e5d00>, reverse: 'bool' = True, **kwargs) -> 'None'` ← Write
> Simulate erasing by hand a :class:`~.Text` or a :class:`~.VMobject`.

<details><summary>métodos próprios (1) · herdados: 24</summary>

- `__init__(self, vmobject: 'VMobject', rate_func: 'Callable[[float], float]' = <function linear at 0x713b879e5d00>, reverse: 'bool' = True, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Write(vmobject: 'VMobject | OpenGLVMobject', rate_func: 'Callable[[float], float]' = <function linear at 0x713b879e5d00>, reverse: 'bool' = False, **kwargs) -> 'None'` ← DrawBorderThenFill
> Simulate hand-writing a :class:`~.Text` or hand-drawing a :class:`~.VMobject`.

<details><summary>métodos próprios (4) · herdados: 21</summary>

- `__init__(self, vmobject: 'VMobject | OpenGLVMobject', rate_func: 'Callable[[float], float]' = <function linear at 0x713b879e5d00>, reverse: 'bool' = False, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'` — Begin the animation.
- `finish(self) -> 'None'` — Finish the animation.
- `reverse_submobjects(self) -> 'None'`

</details>

- `RIGHT` = `array([1., 0., 0.])`
- `TAU` = `6.283185307179586`
- `TYPE_CHECKING` = `False`

## animation/fading

### `FadeIn(*mobjects: 'Mobject', **kwargs: 'Any') -> 'None'` ← _Fade
> Fade in :class:`~.Mobject` s.

<details><summary>métodos próprios (3) · herdados: 20</summary>

- `__init__(self, *mobjects: 'Mobject', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `create_starting_mobject(self) -> 'Mobject'`
- `create_target(self) -> 'Mobject'`

</details>

### `FadeOut(*mobjects: 'Mobject', **kwargs: 'Any') -> 'None'` ← _Fade
> Fade out :class:`~.Mobject` s.

<details><summary>métodos próprios (3) · herdados: 20</summary>

- `__init__(self, *mobjects: 'Mobject', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'` — Clean up the :class:`~.Scene` after finishing the animation.
- `create_target(self) -> 'Mobject'`

</details>

- `ORIGIN` = `array([0., 0., 0.])`

## animation/growing

### `GrowArrow(arrow: 'Arrow', point_color: 'ParsableManimColor | None' = None, **kwargs: 'Any')` ← GrowFromPoint
> Introduce an :class:`~.Arrow` by growing it from its start toward its tip.

<details><summary>métodos próprios (2) · herdados: 21</summary>

- `__init__(self, arrow: 'Arrow', point_color: 'ParsableManimColor | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `create_starting_mobject(self) -> 'Mobject | OpenGLMobject'`

</details>

### `GrowFromCenter(mobject: 'Mobject', point_color: 'ParsableManimColor | None' = None, **kwargs: 'Any')` ← GrowFromPoint
> Introduce an :class:`~.Mobject` by growing it from its center.

<details><summary>métodos próprios (1) · herdados: 22</summary>

- `__init__(self, mobject: 'Mobject', point_color: 'ParsableManimColor | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `GrowFromEdge(mobject: 'Mobject', edge: 'Vector3DLike', point_color: 'ParsableManimColor | None' = None, **kwargs: 'Any')` ← GrowFromPoint
> Introduce an :class:`~.Mobject` by growing it from one of its bounding box edges.

<details><summary>métodos próprios (1) · herdados: 22</summary>

- `__init__(self, mobject: 'Mobject', edge: 'Vector3DLike', point_color: 'ParsableManimColor | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `GrowFromPoint(mobject: 'Mobject', point: 'Point3DLike', point_color: 'ParsableManimColor | None' = None, **kwargs: 'Any')` ← Transform
> Introduce an :class:`~.Mobject` by growing it from a point.

<details><summary>métodos próprios (3) · herdados: 20</summary>

- `__init__(self, mobject: 'Mobject', point: 'Point3DLike', point_color: 'ParsableManimColor | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `create_starting_mobject(self) -> 'Mobject | OpenGLMobject'`
- `create_target(self) -> 'Mobject | OpenGLMobject'`

</details>

### `SpinInFromNothing(mobject: 'Mobject', angle: 'float' = 1.5707963267948966, point_color: 'ParsableManimColor | None' = None, **kwargs: 'Any')` ← GrowFromCenter
> Introduce an :class:`~.Mobject` spinning and growing it from its center.

<details><summary>métodos próprios (1) · herdados: 22</summary>

- `__init__(self, mobject: 'Mobject', angle: 'float' = 1.5707963267948966, point_color: 'ParsableManimColor | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

- `PI` = `3.141592653589793`
- `TYPE_CHECKING` = `False`

## animation/indication

### `ApplyWave(mobject: 'Mobject', direction: 'Vector3DLike' = array([0., 1., 0.]), amplitude: 'float' = 0.2, wave_func: 'RateFunction' = <function smooth at 0x713b879e5e40>, time_width: 'float' = 1, ripples: 'int' = 1, run_time: 'float' = 2, **kwargs: 'Any')` ← Homotopy
> Send a wave through the Mobject distorting it temporarily.

<details><summary>métodos próprios (1) · herdados: 22</summary>

- `__init__(self, mobject: 'Mobject', direction: 'Vector3DLike' = array([0., 1., 0.]), amplitude: 'float' = 0.2, wave_func: 'RateFunction' = <function smooth at 0x713b879e5e40>, time_width: 'float' = 1, ripples: 'int' = 1, run_time: 'float' = 2, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Blink(mobject: 'Mobject', time_on: 'float' = 0.5, time_off: 'float' = 0.5, blinks: 'int' = 1, hide_at_end: 'bool' = False, **kwargs: 'Any')` ← Succession
> Blink the mobject.

<details><summary>métodos próprios (1) · herdados: 25</summary>

- `__init__(self, mobject: 'Mobject', time_on: 'float' = 0.5, time_off: 'float' = 0.5, blinks: 'int' = 1, hide_at_end: 'bool' = False, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Circumscribe(mobject: 'Mobject', shape: 'type[Rectangle] | type[Circle]' = <class 'manim.mobject.geometry.polygram.Rectangle'>, fade_in: 'bool' = False, fade_out: 'bool' = False, time_width: 'float' = 0.3, buff: 'float' = 0.1, color: 'ParsableManimColor' = ManimColor('#FFFF00'), run_time: 'float' = 1, stroke_width: 'float' = 4, **kwargs: 'Any')` ← Succession
> Draw a temporary line surrounding the mobject.

<details><summary>métodos próprios (1) · herdados: 25</summary>

- `__init__(self, mobject: 'Mobject', shape: 'type[Rectangle] | type[Circle]' = <class 'manim.mobject.geometry.polygram.Rectangle'>, fade_in: 'bool' = False, fade_out: 'bool' = False, time_width: 'float' = 0.3, buff: 'float' = 0.1, color: 'ParsableManimColor' = ManimColor('#FFFF00'), run_time: 'float' = 1, stroke_width: 'float' = 4, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Flash(point: 'Point3DLike | Mobject', line_length: 'float' = 0.2, num_lines: 'int' = 12, flash_radius: 'float' = 0.1, line_stroke_width: 'int' = 3, color: 'ParsableManimColor' = ManimColor('#FFFF00'), time_width: 'float' = 1, run_time: 'float' = 1.0, **kwargs: 'Any')` ← AnimationGroup
> Send out lines in all directions.

<details><summary>métodos próprios (3) · herdados: 23</summary>

- `__init__(self, point: 'Point3DLike | Mobject', line_length: 'float' = 0.2, num_lines: 'int' = 12, flash_radius: 'float' = 0.1, line_stroke_width: 'int' = 3, color: 'ParsableManimColor' = ManimColor('#FFFF00'), time_width: 'float' = 1, run_time: 'float' = 1.0, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `create_line_anims(self) -> 'Iterable[ShowPassingFlash]'`
- `create_lines(self) -> 'VGroup'`

</details>

### `FocusOn(focus_point: 'Point3DLike | Mobject', opacity: 'float' = 0.2, color: 'ParsableManimColor' = ManimColor('#888888'), run_time: 'float' = 2, **kwargs: 'Any')` ← Transform
> Shrink a spotlight to a position.

<details><summary>métodos próprios (2) · herdados: 21</summary>

- `__init__(self, focus_point: 'Point3DLike | Mobject', opacity: 'float' = 0.2, color: 'ParsableManimColor' = ManimColor('#888888'), run_time: 'float' = 2, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `create_target(self) -> 'Dot'`

</details>

### `Indicate(mobject: 'Mobject', scale_factor: 'float' = 1.2, color: 'ParsableManimColor' = ManimColor('#FFFF00'), rate_func: 'RateFunction' = <function there_and_back at 0x713b879e6840>, **kwargs: 'Any')` ← Transform
> Indicate a Mobject by temporarily resizing and recoloring it.

<details><summary>métodos próprios (2) · herdados: 21</summary>

- `__init__(self, mobject: 'Mobject', scale_factor: 'float' = 1.2, color: 'ParsableManimColor' = ManimColor('#FFFF00'), rate_func: 'RateFunction' = <function there_and_back at 0x713b879e6840>, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `create_target(self) -> 'Mobject | OpenGLMobject'`

</details>

### `ShowPassingFlash(mobject: 'VMobject', time_width: 'float' = 0.1, **kwargs: 'Any') -> 'None'` ← ShowPartial
> Show only a sliver of the VMobject each frame.

<details><summary>métodos próprios (2) · herdados: 20</summary>

- `__init__(self, mobject: 'VMobject', time_width: 'float' = 0.1, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'` — Clean up the :class:`~.Scene` after finishing the animation.

</details>

### `ShowPassingFlashWithThinningStrokeWidth(vmobject: 'VMobject', n_segments: 'int' = 10, time_width: 'float' = 0.1, remover: 'bool' = True, **kwargs: 'Any')` ← AnimationGroup
> Plays a group or series of :class:`~.Animation`.

<details><summary>métodos próprios (1) · herdados: 23</summary>

- `__init__(self, vmobject: 'VMobject', n_segments: 'int' = 10, time_width: 'float' = 0.1, remover: 'bool' = True, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Wiggle(mobject: 'Mobject', scale_value: 'float' = 1.1, rotation_angle: 'float' = 0.06283185307179587, n_wiggles: 'int' = 6, scale_about_point: 'Point3DLike | None' = None, rotate_about_point: 'Point3DLike | None' = None, run_time: 'float' = 2, **kwargs: 'Any')` ← Animation
> Wiggle a Mobject.

<details><summary>métodos próprios (4) · herdados: 20</summary>

- `__init__(self, mobject: 'Mobject', scale_value: 'float' = 1.1, rotation_angle: 'float' = 0.06283185307179587, n_wiggles: 'int' = 6, scale_about_point: 'Point3DLike | None' = None, rotate_about_point: 'Point3DLike | None' = None, run_time: 'float' = 2, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_rotate_about_point(self) -> 'Point3D'`
- `get_scale_about_point(self) -> 'Point3D'`
- `interpolate_submobject(self, submobject: 'Mobject', starting_submobject: 'Mobject', alpha: 'float') -> 'Self'`

</details>

- `BOLD` = `'BOLD'`
- `BOOK` = `'BOOK'`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CTRL_VALUE` = `65507`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `GREY` = `ManimColor('#888888')`
- `HEAVY` = `'HEAVY'`
- `IN` = `array([ 0.,  0., -1.])`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LIGHT` = `'LIGHT'`
- `MEDIUM` = `'MEDIUM'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OBLIQUE` = `'OBLIQUE'`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `PURE_YELLOW` = `ManimColor('#FFFF00')`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RIGHT` = `array([1., 0., 0.])`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SHIFT_VALUE` = `65505`
- `SMALL_BUFF` = `0.1`
- `START_X` = `30`
- `START_Y` = `20`
- `TAU` = `6.283185307179586`
- `THIN` = `'THIN'`
- `UL` = `array([-1.,  1.,  0.])`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Z_AXIS` = `array([0., 0., 1.])`

## animation/movement

### `ComplexHomotopy(complex_homotopy: 'Callable[[complex, float], float]', mobject: 'Mobject', **kwargs: 'Any')` ← Homotopy
> A Homotopy.

<details><summary>métodos próprios (1) · herdados: 22</summary>

- `__init__(self, complex_homotopy: 'Callable[[complex, float], float]', mobject: 'Mobject', **kwargs: 'Any')` — Complex Homotopy a function Cx[0, 1] to C

</details>

### `Homotopy(homotopy: 'Callable[[float, float, float, float], tuple[float, float, float]]', mobject: 'Mobject', run_time: 'float' = 3, apply_function_kwargs: 'dict[str, Any] | None' = None, **kwargs: 'Any')` ← Animation
> A Homotopy.

<details><summary>métodos próprios (3) · herdados: 20</summary>

- `__init__(self, homotopy: 'Callable[[float, float, float, float], tuple[float, float, float]]', mobject: 'Mobject', run_time: 'float' = 3, apply_function_kwargs: 'dict[str, Any] | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `function_at_time_t(self, t: 'float') -> 'MappingFunction'`
- `interpolate_submobject(self, submobject: 'Mobject', starting_submobject: 'Mobject', alpha: 'float') -> 'Self'`

</details>

### `MoveAlongPath(mobject: 'Mobject', path: 'VMobject', suspend_mobject_updating: 'bool' = False, **kwargs: 'Any')` ← Animation
> Make one mobject move along the path of another mobject.

<details><summary>métodos próprios (2) · herdados: 20</summary>

- `__init__(self, mobject: 'Mobject', path: 'VMobject', suspend_mobject_updating: 'bool' = False, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_mobject(self, alpha: 'float') -> 'None'` — Interpolates the mobject of the :class:`Animation` based on alpha value.

</details>

### `PhaseFlow(function: 'Callable[[np.ndarray], np.ndarray]', mobject: 'Mobject', virtual_time: 'float' = 1, suspend_mobject_updating: 'bool' = False, rate_func: 'RateFunction' = <function linear at 0x713b879e5d00>, **kwargs: 'Any')` ← Animation
> An animation.

<details><summary>métodos próprios (2) · herdados: 20</summary>

- `__init__(self, function: 'Callable[[np.ndarray], np.ndarray]', mobject: 'Mobject', virtual_time: 'float' = 1, suspend_mobject_updating: 'bool' = False, rate_func: 'RateFunction' = <function linear at 0x713b879e5d00>, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_mobject(self, alpha: 'float') -> 'None'` — Interpolates the mobject of the :class:`Animation` based on alpha value.

</details>

### `SmoothedVectorizedHomotopy(homotopy: 'Callable[[float, float, float, float], tuple[float, float, float]]', mobject: 'Mobject', run_time: 'float' = 3, apply_function_kwargs: 'dict[str, Any] | None' = None, **kwargs: 'Any')` ← Homotopy
> A Homotopy.

<details><summary>métodos próprios (1) · herdados: 22</summary>

- `interpolate_submobject(self, submobject: 'Mobject', starting_submobject: 'Mobject', alpha: 'float') -> 'Self'`

</details>

- `TYPE_CHECKING` = `False`

## animation/numbers

### `ChangeDecimalToValue(decimal_mob: 'DecimalNumber', target_number: 'int', **kwargs: 'Any') -> 'None'` ← ChangingDecimal
> Animate a :class:`~.DecimalNumber` to a target value using linear interpolation.

<details><summary>métodos próprios (1) · herdados: 22</summary>

- `__init__(self, decimal_mob: 'DecimalNumber', target_number: 'int', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ChangingDecimal(decimal_mob: 'DecimalNumber', number_update_func: 'Callable[[float], float]', suspend_mobject_updating: 'bool' = False, **kwargs: 'Any') -> 'None'` ← Animation
> Animate a :class:`~.DecimalNumber` to values specified by a user-supplied function.

<details><summary>métodos próprios (3) · herdados: 20</summary>

- `__init__(self, decimal_mob: 'DecimalNumber', number_update_func: 'Callable[[float], float]', suspend_mobject_updating: 'bool' = False, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `check_validity_of_input(self, decimal_mob: 'DecimalNumber') -> 'None'`
- `interpolate_mobject(self, alpha: 'float') -> 'None'` — Interpolates the mobject of the :class:`Animation` based on alpha value.

</details>


## animation/rotation

### `Rotate(mobject: 'Mobject', angle: 'float' = 3.141592653589793, axis: 'Vector3DLike' = array([0., 0., 1.]), about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = None, **kwargs: 'Any') -> 'None'` ← Transform
> Animation that rotates a Mobject.

<details><summary>métodos próprios (2) · herdados: 21</summary>

- `__init__(self, mobject: 'Mobject', angle: 'float' = 3.141592653589793, axis: 'Vector3DLike' = array([0., 0., 1.]), about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = None, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `create_target(self) -> 'Mobject | OpenGLMobject'`

</details>

### `Rotating(mobject: 'Mobject', angle: 'float' = 6.283185307179586, axis: 'Vector3DLike' = array([0., 0., 1.]), about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = None, run_time: 'float' = 5, rate_func: 'Callable[[float], float]' = <function linear at 0x713b879e5d00>, **kwargs: 'Any') -> 'None'` ← Animation
> Animation that rotates a Mobject.

<details><summary>métodos próprios (2) · herdados: 20</summary>

- `__init__(self, mobject: 'Mobject', angle: 'float' = 6.283185307179586, axis: 'Vector3DLike' = array([0., 0., 1.]), about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = None, run_time: 'float' = 5, rate_func: 'Callable[[float], float]' = <function linear at 0x713b879e5d00>, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_mobject(self, alpha: 'float') -> 'None'` — Interpolates the mobject of the :class:`Animation` based on alpha value.

</details>

- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `TAU` = `6.283185307179586`
- `TYPE_CHECKING` = `False`

## animation/specialized

### `Broadcast(mobject: 'Mobject', focal_point: 'Sequence[float]' = array([0., 0., 0.]), n_mobs: 'int' = 5, initial_opacity: 'float' = 1, final_opacity: 'float' = 0, initial_width: 'float' = 0.0, remover: 'bool' = True, lag_ratio: 'float' = 0.2, run_time: 'float' = 3, **kwargs: 'Any')` ← LaggedStart
> Broadcast a mobject starting from an ``initial_width``, up to the actual size of the mobject.

<details><summary>métodos próprios (1) · herdados: 23</summary>

- `__init__(self, mobject: 'Mobject', focal_point: 'Sequence[float]' = array([0., 0., 0.]), n_mobs: 'int' = 5, initial_opacity: 'float' = 1, final_opacity: 'float' = 0, initial_width: 'float' = 0.0, remover: 'bool' = True, lag_ratio: 'float' = 0.2, run_time: 'float' = 3, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

- `BOLD` = `'BOLD'`
- `BOOK` = `'BOOK'`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CTRL_VALUE` = `65507`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `HEAVY` = `'HEAVY'`
- `IN` = `array([ 0.,  0., -1.])`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LIGHT` = `'LIGHT'`
- `MEDIUM` = `'MEDIUM'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OBLIQUE` = `'OBLIQUE'`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RIGHT` = `array([1., 0., 0.])`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SHIFT_VALUE` = `65505`
- `SMALL_BUFF` = `0.1`
- `START_X` = `30`
- `START_Y` = `20`
- `TAU` = `6.283185307179586`
- `THIN` = `'THIN'`
- `UL` = `array([-1.,  1.,  0.])`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Z_AXIS` = `array([0., 0., 1.])`

## animation/speed

### `ChangeSpeed(anim: 'Animation | _AnimationBuilder', speedinfo: 'dict[float, float]', rate_func: 'Callable[[float], float] | None' = None, affects_speed_updaters: 'bool' = True, **kwargs) -> 'None'` ← Animation
> Modifies the speed of passed animation.

<details><summary>métodos próprios (9) · herdados: 16</summary>

- `__init__(self, anim: 'Animation | _AnimationBuilder', speedinfo: 'dict[float, float]', rate_func: 'Callable[[float], float] | None' = None, affects_speed_updaters: 'bool' = True, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `add_updater(mobject: 'Mobject', update_function: 'Updater', index: 'int | None' = None, call_updater: 'bool' = False)` — This static method can be used to apply speed change to updaters.
- `begin(self) -> 'None'` — Begin the animation.
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'` — Clean up the :class:`~.Scene` after finishing the animation.
- `finish(self) -> 'None'` — Finish the animation.
- `get_scaled_total_time(self) -> 'float'` — The time taken by the animation under the assumption that the ``run_time`` is 1.
- `interpolate(self, alpha: 'float') -> 'None'` — Set the animation progress.
- `setup(self, anim)`
- `update_mobjects(self, dt: 'float') -> 'None'` — Updates things like starting_mobject, and (for

</details>

- `TYPE_CHECKING` = `False`

## animation/transform

### `ApplyComplexFunction(function: 'types.MethodType', mobject: 'Mobject', **kwargs) -> 'None'` ← ApplyMethod
> Animates a mobject by applying a method.

<details><summary>métodos próprios (1) · herdados: 23</summary>

- `__init__(self, function: 'types.MethodType', mobject: 'Mobject', **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ApplyFunction(function: 'types.MethodType', mobject: 'Mobject', **kwargs) -> 'None'` ← Transform
> A Transform transforms a Mobject into a target Mobject.

<details><summary>métodos próprios (2) · herdados: 21</summary>

- `__init__(self, function: 'types.MethodType', mobject: 'Mobject', **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `create_target(self) -> 'Any'`

</details>

### `ApplyMatrix(matrix: 'np.ndarray', mobject: 'Mobject', about_point: 'np.ndarray' = array([0., 0., 0.]), **kwargs) -> 'None'` ← ApplyPointwiseFunction
> Applies a matrix transform to an mobject.

<details><summary>métodos próprios (2) · herdados: 23</summary>

- `__init__(self, matrix: 'np.ndarray', mobject: 'Mobject', about_point: 'np.ndarray' = array([0., 0., 0.]), **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `initialize_matrix(self, matrix: 'np.ndarray') -> 'np.ndarray'`

</details>

### `ApplyMethod(method: 'Callable', *args, **kwargs) -> 'None'` ← Transform
> Animates a mobject by applying a method.

<details><summary>métodos próprios (3) · herdados: 21</summary>

- `__init__(self, method: 'Callable', *args, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `check_validity_of_input(self, method: 'Callable') -> 'None'`
- `create_target(self) -> 'Mobject'`

</details>

### `ApplyPointwiseFunction(function: 'types.MethodType', mobject: 'Mobject', run_time: 'float' = 3.0, **kwargs) -> 'None'` ← ApplyMethod
> Animation that applies a pointwise function to a mobject.

<details><summary>métodos próprios (1) · herdados: 23</summary>

- `__init__(self, function: 'types.MethodType', mobject: 'Mobject', run_time: 'float' = 3.0, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ApplyPointwiseFunctionToCenter(function: 'types.MethodType', mobject: 'Mobject', **kwargs) -> 'None'` ← ApplyPointwiseFunction
> Animation that applies a pointwise function to a mobject.

<details><summary>métodos próprios (2) · herdados: 22</summary>

- `__init__(self, function: 'types.MethodType', mobject: 'Mobject', **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'` — Begin the animation.

</details>

### `ClockwiseTransform(mobject: 'Mobject', target_mobject: 'Mobject', path_arc: 'float' = -3.141592653589793, **kwargs) -> 'None'` ← Transform
> Transforms the points of a mobject along a clockwise oriented arc.

<details><summary>métodos próprios (1) · herdados: 22</summary>

- `__init__(self, mobject: 'Mobject', target_mobject: 'Mobject', path_arc: 'float' = -3.141592653589793, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `CounterclockwiseTransform(mobject: 'Mobject', target_mobject: 'Mobject', path_arc: 'float' = 3.141592653589793, **kwargs) -> 'None'` ← Transform
> Transforms the points of a mobject along a counterclockwise oriented arc.

<details><summary>métodos próprios (1) · herdados: 22</summary>

- `__init__(self, mobject: 'Mobject', target_mobject: 'Mobject', path_arc: 'float' = 3.141592653589793, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `CyclicReplace(*mobjects: 'Mobject', path_arc: 'float' = 1.5707963267948966, **kwargs) -> 'None'` ← Transform
> An animation moving mobjects cyclically.

<details><summary>métodos próprios (2) · herdados: 21</summary>

- `__init__(self, *mobjects: 'Mobject', path_arc: 'float' = 1.5707963267948966, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `create_target(self) -> 'Group | VGroup'`

</details>

### `FadeToColor(mobject: 'Mobject', color: 'str', **kwargs) -> 'None'` ← ApplyMethod
> Animation that changes color of a mobject.

<details><summary>métodos próprios (1) · herdados: 23</summary>

- `__init__(self, mobject: 'Mobject', color: 'str', **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `FadeTransform(mobject: 'Mobject', target_mobject: 'Mobject', stretch: 'bool' = True, dim_to_match: 'int' = 1, **kwargs: 'Any')` ← Transform
> Fades one mobject into another.

<details><summary>métodos próprios (6) · herdados: 18</summary>

- `__init__(self, mobject: 'Mobject', target_mobject: 'Mobject', stretch: 'bool' = True, dim_to_match: 'int' = 1, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self)` — Initial setup for the animation.
- `clean_up_from_scene(self, scene)` — Clean up the :class:`~.Scene` after finishing the animation.
- `get_all_families_zipped(self)`
- `get_all_mobjects(self) -> 'Sequence[Mobject]'` — Get all mobjects involved in the animation.
- `ghost_to(self, source, target)` — Replaces the source by the target and sets the opacity to 0.

</details>

### `FadeTransformPieces(mobject: 'Mobject', target_mobject: 'Mobject', stretch: 'bool' = True, dim_to_match: 'int' = 1, **kwargs: 'Any')` ← FadeTransform
> Fades submobjects of one mobject into submobjects of another one.

<details><summary>métodos próprios (2) · herdados: 22</summary>

- `begin(self)` — Initial setup for the animation.
- `ghost_to(self, source, target)` — Replaces the source submobjects by the target submobjects and sets

</details>

### `MoveToTarget(mobject: 'Mobject', **kwargs) -> 'None'` ← Transform
> Transforms a mobject to the mobject stored in its ``target`` attribute.

<details><summary>métodos próprios (2) · herdados: 22</summary>

- `__init__(self, mobject: 'Mobject', **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `check_validity_of_input(self, mobject: 'Mobject') -> 'None'`

</details>

### `ReplacementTransform(mobject: 'Mobject', target_mobject: 'Mobject', **kwargs) -> 'None'` ← Transform
> Replaces and morphs a mobject into a target mobject.

<details><summary>métodos próprios (1) · herdados: 22</summary>

- `__init__(self, mobject: 'Mobject', target_mobject: 'Mobject', **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Restore(mobject: 'Mobject', **kwargs) -> 'None'` ← ApplyMethod
> Transforms a mobject to its last saved state.

<details><summary>métodos próprios (1) · herdados: 23</summary>

- `__init__(self, mobject: 'Mobject', **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ScaleInPlace(mobject: 'Mobject', scale_factor: 'float', **kwargs) -> 'None'` ← ApplyMethod
> Animation that scales a mobject by a certain factor.

<details><summary>métodos próprios (1) · herdados: 23</summary>

- `__init__(self, mobject: 'Mobject', scale_factor: 'float', **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ShrinkToCenter(mobject: 'Mobject', **kwargs) -> 'None'` ← ScaleInPlace
> Animation that makes a mobject shrink to center.

<details><summary>métodos próprios (1) · herdados: 23</summary>

- `__init__(self, mobject: 'Mobject', **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Swap(*mobjects: 'Mobject', path_arc: 'float' = 1.5707963267948966, **kwargs) -> 'None'` ← CyclicReplace
> Another name for :class:`~.CyclicReplace`, which is more understandable for two entries.

### `Transform(mobject: 'Mobject | None', target_mobject: 'Mobject | None' = None, path_func: 'Callable | None' = None, path_arc: 'float' = 0, path_arc_axis: 'np.ndarray' = array([0., 0., 1.]), path_arc_centers: 'Point3DLike | Point3DLike_Array | None' = None, replace_mobject_with_target_in_scene: 'bool' = False, **kwargs) -> 'None'` ← Animation
> A Transform transforms a Mobject into a target Mobject.

<details><summary>métodos próprios (7) · herdados: 16</summary>

- `__init__(self, mobject: 'Mobject | None', target_mobject: 'Mobject | None' = None, path_func: 'Callable | None' = None, path_arc: 'float' = 0, path_arc_axis: 'np.ndarray' = array([0., 0., 1.]), path_arc_centers: 'Point3DLike | Point3DLike_Array | None' = None, replace_mobject_with_target_in_scene: 'bool' = False, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `begin(self) -> 'None'` — Begin the animation.
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'` — Clean up the :class:`~.Scene` after finishing the animation.
- `create_target(self) -> 'Mobject | OpenGLMobject'`
- `get_all_families_zipped(self) -> 'Iterable[tuple]'`
- `get_all_mobjects(self) -> 'Sequence[Mobject]'` — Get all mobjects involved in the animation.
- `interpolate_submobject(self, submobject: 'Mobject', starting_submobject: 'Mobject', target_copy: 'Mobject', alpha: 'float') -> 'Transform'`

</details>

### `TransformAnimations(start_anim: 'Animation', end_anim: 'Animation', rate_func: 'Callable' = <function squish_rate_func.<locals>.result at 0x713b849a1300>, **kwargs) -> 'None'` ← Transform
> A Transform transforms a Mobject into a target Mobject.

<details><summary>métodos próprios (2) · herdados: 21</summary>

- `__init__(self, start_anim: 'Animation', end_anim: 'Animation', rate_func: 'Callable' = <function squish_rate_func.<locals>.result at 0x713b849a1300>, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate(self, alpha: 'float') -> 'None'` — Set the animation progress.

</details>

### `TransformFromCopy(mobject: 'Mobject', target_mobject: 'Mobject', **kwargs) -> 'None'` ← Transform
> Preserves a copy of the original VMobject and transforms only it's copy to the target VMobject

<details><summary>métodos próprios (2) · herdados: 21</summary>

- `__init__(self, mobject: 'Mobject', target_mobject: 'Mobject', **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate(self, alpha: 'float') -> 'None'` — Set the animation progress.

</details>

### `TransformMatchingAbstractBase(mobject: 'Mobject', target_mobject: 'Mobject', transform_mismatches: 'bool' = False, fade_transform_mismatches: 'bool' = False, key_map: 'dict | None' = None, **kwargs: 'Any')` ← AnimationGroup
> Abstract base class for transformations that keep track of matching parts.

<details><summary>métodos próprios (5) · herdados: 22</summary>

- `__init__(self, mobject: 'Mobject', target_mobject: 'Mobject', transform_mismatches: 'bool' = False, fade_transform_mismatches: 'bool' = False, key_map: 'dict | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `clean_up_from_scene(self, scene: 'Scene') -> 'None'` — Clean up the :class:`~.Scene` after finishing the animation.
- `get_mobject_key(mobject: 'Mobject') -> 'int | str'`
- `get_mobject_parts(mobject: 'Mobject') -> 'list[Mobject]'`
- `get_shape_map(self, mobject: 'Mobject') -> 'dict'`

</details>

### `TransformMatchingShapes(mobject: 'Mobject', target_mobject: 'Mobject', transform_mismatches: 'bool' = False, fade_transform_mismatches: 'bool' = False, key_map: 'dict | None' = None, **kwargs: 'Any')` ← TransformMatchingAbstractBase
> An animation trying to transform groups by matching the shape

<details><summary>métodos próprios (3) · herdados: 24</summary>

- `__init__(self, mobject: 'Mobject', target_mobject: 'Mobject', transform_mismatches: 'bool' = False, fade_transform_mismatches: 'bool' = False, key_map: 'dict | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_mobject_key(mobject: 'Mobject') -> 'int'`
- `get_mobject_parts(mobject: 'Mobject') -> 'list[Mobject]'`

</details>

### `TransformMatchingTex(mobject: 'Mobject', target_mobject: 'Mobject', transform_mismatches: 'bool' = False, fade_transform_mismatches: 'bool' = False, key_map: 'dict | None' = None, **kwargs: 'Any')` ← TransformMatchingAbstractBase
> A transformation trying to transform rendered LaTeX strings.

<details><summary>métodos próprios (3) · herdados: 24</summary>

- `__init__(self, mobject: 'Mobject', target_mobject: 'Mobject', transform_mismatches: 'bool' = False, fade_transform_mismatches: 'bool' = False, key_map: 'dict | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_mobject_key(mobject: 'Mobject') -> 'str'`
- `get_mobject_parts(mobject: 'Mobject') -> 'list[Mobject]'`

</details>

- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEGREES` = `0.017453292519943295`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`

## animation/updaters

### `MaintainPositionRelativeTo(mobject: 'Mobject', tracked_mobject: 'Mobject', **kwargs: 'Any') -> 'None'` ← Animation
> An animation.

<details><summary>métodos próprios (2) · herdados: 20</summary>

- `__init__(self, mobject: 'Mobject', tracked_mobject: 'Mobject', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_mobject(self, alpha: 'float') -> 'None'` — Interpolates the mobject of the :class:`Animation` based on alpha value.

</details>

### `UpdateFromAlphaFunc(mobject: 'Mobject', update_function: 'Callable[[Mobject], Any]', suspend_mobject_updating: 'bool' = False, **kwargs: 'Any') -> 'None'` ← UpdateFromFunc
> update_function of the form func(mobject), presumably

<details><summary>métodos próprios (1) · herdados: 21</summary>

- `interpolate_mobject(self, alpha: 'float') -> 'None'` — Interpolates the mobject of the :class:`Animation` based on alpha value.

</details>

### `UpdateFromFunc(mobject: 'Mobject', update_function: 'Callable[[Mobject], Any]', suspend_mobject_updating: 'bool' = False, **kwargs: 'Any') -> 'None'` ← Animation
> update_function of the form func(mobject), presumably

<details><summary>métodos próprios (2) · herdados: 20</summary>

- `__init__(self, mobject: 'Mobject', update_function: 'Callable[[Mobject], Any]', suspend_mobject_updating: 'bool' = False, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `interpolate_mobject(self, alpha: 'float') -> 'None'` — Interpolates the mobject of the :class:`Animation` based on alpha value.

</details>

- `DEGREES` = `0.017453292519943295`
- `M` = `~M`
- `RIGHT` = `array([1., 0., 0.])`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- **`always(method: 'Callable', *args, **kwargs) -> 'Mobject'`**
- **`always_redraw(func: 'Callable[[], M]') -> 'M'`** — Redraw the mobject constructed by a function every frame.
- **`always_rotate(mobject: 'M', rate: 'float' = 0.3490658503988659, **kwargs) -> 'M'`** — A mobject which is continuously rotated at a certain rate.
- **`always_shift(mobject: 'M', direction: 'np.ndarray[np.float64]' = array([1., 0., 0.]), rate: 'float' = 0.1) -> 'M'`** — A mobject which is continuously shifted along some direction
- **`assert_is_mobject_method(method: 'Callable') -> 'None'`**
- **`cycle_animation(animation: 'Animation', **kwargs) -> 'Mobject'`**
- **`f_always(method: 'Callable[[M], None]', *arg_generators, **kwargs) -> 'M'`** — More functional version of always, where instead
- **`turn_animation_into_updater(animation: 'Animation', cycle: 'bool' = False, delay: 'float' = 0, **kwargs) -> 'Mobject'`** — Add an updater to the animation's mobject which applies

## camera

### `BackgroundColoredVMobjectDisplayer(camera: 'Camera')`
> Auxiliary class that handles displaying vectorized mobjects with

<details><summary>métodos próprios (6) · herdados: 0</summary>

- `__init__(self, camera: 'Camera')` — Initialize self.  See help(type(self)) for accurate signature.
- `display(self, *cvmobjects: 'VMobject') -> 'PixelArray | None'` — Displays the colored VMobjects.
- `get_background_array(self, image: 'Image.Image | pathlib.Path | str') -> 'PixelArray'` — Gets the background array that has the passed file_name.
- `reset_pixel_array(self) -> 'None'`
- `resize_background_array(self, background_array: 'PixelArray', new_width: 'float', new_height: 'float', mode: 'str' = 'RGBA') -> 'PixelArray'` — Resizes the pixel array representing the background.
- `resize_background_array_to_match(self, background_array: 'PixelArray', pixel_array: 'PixelArray') -> 'PixelArray'` — Resizes the background array to match the passed pixel array.

</details>

### `Camera(background_image: 'str | None' = None, frame_center: 'Point3D' = array([0., 0., 0.]), image_mode: 'str' = 'RGBA', n_channels: 'int' = 4, pixel_array_dtype: 'str' = 'uint8', cairo_line_width_multiple: 'float' = 0.01, use_z_index: 'bool' = True, background: 'PixelArray | None' = None, pixel_height: 'int | None' = None, pixel_width: 'int | None' = None, frame_height: 'float | None' = None, frame_width: 'float | None' = None, frame_rate: 'float | None' = None, background_color: 'ParsableManimColor | None' = None, background_opacity: 'float | None' = None, **kwargs: 'Any') -> 'None'`
> Base camera class.

<details><summary>métodos próprios (46) · herdados: 0</summary>

- `__init__(self, background_image: 'str | None' = None, frame_center: 'Point3D' = array([0., 0., 0.]), image_mode: 'str' = 'RGBA', n_channels: 'int' = 4, pixel_array_dtype: 'str' = 'uint8', cairo_line_width_multiple: 'float' = 0.01, use_z_index: 'bool' = True, background: 'PixelArray | None' = None, pixel_height: 'int | None' = None, pixel_width: 'int | None' = None, frame_height: 'float | None' = None, frame_width: 'float | None' = None, frame_rate: 'float | None' = None, background_color: 'ParsableManimColor | None' = None, background_opacity: 'float | None' = None, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `adjust_out_of_range_points(self, points: 'np.ndarray') -> 'np.ndarray'` — If any of the points in the passed array are out of
- `adjusted_thickness(self, thickness: 'float') -> 'float'` — Computes the adjusted stroke width for a zoomed camera.
- `apply_fill(self, ctx: 'cairo.Context', vmobject: 'VMobject') -> 'Self'` — Fills the cairo context
- `apply_stroke(self, ctx: 'cairo.Context', vmobject: 'VMobject', background: 'bool' = False) -> 'Self'` — Applies a stroke to the VMobject in the cairo context.
- `cache_cairo_context(self, pixel_array: 'PixelArray', ctx: 'cairo.Context') -> 'None'` — Caches the passed Pixel array into a Cairo Context
- `capture_mobject(self, mobject: 'Mobject', **kwargs: 'Any') -> 'None'` — Capture mobjects by storing it in :attr:`pixel_array`.
- `capture_mobjects(self, mobjects: 'Iterable[Mobject]', **kwargs: 'Any') -> 'None'` — Capture mobjects by printing them on :attr:`pixel_array`.
- `convert_pixel_array(self, pixel_array: 'PixelArray | list | tuple') -> 'PixelArray'` — Converts a pixel array with float values to proper RGB values.
- `display_image_mobject(self, image_mobject: 'AbstractImageMobject', pixel_array: 'np.ndarray') -> 'None'` — Display an :class:`~.ImageMobject` by changing the ``pixel_array`` suitably.
- `display_multiple_background_colored_vmobjects(self, cvmobjects: 'Iterable[VMobject]', pixel_array: 'PixelArray') -> 'Self'` — Displays multiple vmobjects that have the same color as the background.
- `display_multiple_image_mobjects(self, image_mobjects: 'Iterable[AbstractImageMobject]', pixel_array: 'PixelArray') -> 'None'` — Displays multiple image mobjects by modifying the passed pixel_array.
- `display_multiple_non_background_colored_vmobjects(self, vmobjects: 'Iterable[VMobject]', pixel_array: 'PixelArray') -> 'None'` — Displays multiple VMobjects in the cairo context, as long as they don't have
- `display_multiple_point_cloud_mobjects(self, pmobjects: 'Iterable[PMobject]', pixel_array: 'PixelArray') -> 'None'` — Displays multiple PMobjects by modifying the passed pixel array.
- `display_multiple_vectorized_mobjects(self, vmobjects: 'list[VMobject]', pixel_array: 'PixelArray') -> 'None'` — Displays multiple VMobjects in the pixel_array
- `display_point_cloud(self, pmobject: 'PMobject', points: 'Point3D_Array', rgbas: 'FloatRGBA_Array', thickness: 'float', pixel_array: 'PixelArray') -> 'None'` — Displays a PMobject by modifying the pixel array suitably.
- `display_vectorized(self, vmobject: 'VMobject', ctx: 'cairo.Context') -> 'Self'` — Displays a VMobject in the cairo context
- `get_background_colored_vmobject_displayer(self) -> 'BackgroundColoredVMobjectDisplayer'` — Returns the background_colored_vmobject_displayer
- `get_cached_cairo_context(self, pixel_array: 'PixelArray') -> 'cairo.Context | None'` — Returns the cached cairo context of the passed
- `get_cairo_context(self, pixel_array: 'PixelArray') -> 'cairo.Context'` — Returns the cairo context for a pixel array after
- `get_coords_of_all_pixels(self) -> 'PixelArray'` — Returns the cartesian coordinates of each pixel.
- `get_fill_rgbas(self, vmobject: 'VMobject') -> 'FloatRGBA_Array'` — Returns the RGBA array of the fill of the passed VMobject
- `get_image(self, pixel_array: 'PixelArray | list | tuple | None' = None) -> 'Image.Image'` — Returns an image from the passed
- `get_mobjects_to_display(self, mobjects: 'Iterable[Mobject]', include_submobjects: 'bool' = True, excluded_mobjects: 'list | None' = None) -> 'list[Mobject]'` — Used to get the list of mobjects to display
- `get_stroke_rgbas(self, vmobject: 'VMobject', background: 'bool' = False) -> 'FloatRGBA_Array'` — Gets the RGBA array for the stroke of the passed
- `get_thickening_nudges(self, thickness: 'float') -> 'PixelArray'` — Determine a list of vectors used to nudge
- `init_background(self) -> 'None'` — Initialize the background.
- `is_in_frame(self, mobject: 'Mobject') -> 'bool'` — Checks whether the passed mobject is in
- `make_background_from_func(self, coords_to_colors_func: 'Callable[[np.ndarray], np.ndarray]') -> 'PixelArray'` — Makes a pixel array for the background by using coords_to_colors_func to determine each pixel's color. Each input
- `on_screen_pixels(self, pixel_coords: 'np.ndarray') -> 'PixelArray'` — Returns array of pixels that are on the screen from a given
- `overlay_PIL_image(self, pixel_array: 'np.ndarray', image: 'Image') -> 'None'` — Overlays a PIL image on the passed pixel array.
- `overlay_rgba_array(self, pixel_array: 'np.ndarray', new_array: 'np.ndarray') -> 'None'` — Overlays an RGBA array on top of the given Pixel array.
- `points_to_pixel_coords(self, mobject: 'Mobject', points: 'Point3D_Array') -> 'npt.NDArray[ManimInt]'`
- `points_to_subpixel_coords(self, mobject: 'Mobject', points: 'Point3D_Array') -> 'npt.NDArray[ManimFloat]'`
- `reset(self) -> 'Self'` — Resets the camera's pixel array
- `reset_pixel_shape(self, new_height: 'float', new_width: 'float') -> 'None'` — This method resets the height and width
- `resize_frame_shape(self, fixed_dimension: 'int' = 0) -> 'None'` — Changes frame_shape to match the aspect ratio
- `set_background(self, pixel_array: 'PixelArray | list | tuple', convert_from_floats: 'bool' = False) -> 'None'` — Sets the background to the passed pixel_array after converting
- `set_background_from_func(self, coords_to_colors_func: 'Callable[[np.ndarray], np.ndarray]') -> 'None'` — Sets the background to a pixel array using coords_to_colors_func to determine each pixel's color. Each input
- `set_cairo_context_color(self, ctx: 'cairo.Context', rgbas: 'FloatRGBALike_Array', vmobject: 'VMobject') -> 'Self'` — Sets the color of the cairo context
- `set_cairo_context_path(self, ctx: 'cairo.Context', vmobject: 'VMobject') -> 'Self'` — Sets a path for the cairo context with the vmobject passed
- `set_frame_to_background(self, background: 'PixelArray') -> 'None'`
- `set_pixel_array(self, pixel_array: 'PixelArray | list | tuple', convert_from_floats: 'bool' = False) -> 'None'` — Sets the pixel array of the camera to the passed pixel array.
- `thickened_coordinates(self, pixel_coords: 'np.ndarray', thickness: 'float') -> 'PixelArray'` — Returns thickened coordinates for a passed array of pixel coords and
- `transform_points_pre_display(self, mobject: 'Mobject', points: 'Point3D_Array') -> 'Point3D_Array'`
- `type_or_raise(self, mobject: 'Mobject') -> 'type[VMobject] | type[PMobject] | type[AbstractImageMobject] | type[Mobject]'` — Return the type of mobject, if it is a type that can be rendered.

</details>

### `MappingCamera(mapping_func=<function MappingCamera.<lambda> at 0x713b83cd09a0>, min_num_curves=50, allow_object_intrusion=False, **kwargs)` ← Camera
> Parameters

<details><summary>métodos próprios (3) · herdados: 43</summary>

- `__init__(self, mapping_func=<function MappingCamera.<lambda> at 0x713b83cd09a0>, min_num_curves=50, allow_object_intrusion=False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `capture_mobjects(self, mobjects, **kwargs)` — Capture mobjects for rendering after applying the spatial mapping.
- `points_to_pixel_coords(self, mobject, points)`

</details>

### `MovingCamera(frame: 'Mobject | None' = None, fixed_dimension: 'int' = 0, default_frame_stroke_color: 'ManimColor' = ManimColor('#FFFFFF'), default_frame_stroke_width: 'int' = 0, **kwargs: 'Any')` ← Camera
> A camera that follows and matches the size and position of its 'frame', a Rectangle (or similar Mobject).

<details><summary>métodos próprios (6) · herdados: 42</summary>

- `__init__(self, frame: 'Mobject | None' = None, fixed_dimension: 'int' = 0, default_frame_stroke_color: 'ManimColor' = ManimColor('#FFFFFF'), default_frame_stroke_width: 'int' = 0, **kwargs: 'Any')` — Frame is a Mobject, (should almost certainly be a rectangle)
- `auto_zoom(self, mobjects: 'Iterable[Mobject]', margin: 'float' = 0, only_mobjects_in_frame: 'bool' = False, animate: 'bool' = True) -> '_AnimationBuilder | Mobject'` — Zooms on to a given array of mobjects (or a singular mobject)
- `cache_cairo_context(self, pixel_array: 'PixelArray', ctx: 'Context') -> 'None'` — Since the frame can be moving around, the cairo
- `capture_mobjects(self, mobjects: 'Iterable[Mobject]', **kwargs: 'Any') -> 'None'` — Capture mobjects by printing them on :attr:`pixel_array`.
- `get_cached_cairo_context(self, pixel_array: 'PixelArray') -> 'None'` — Since the frame can be moving around, the cairo
- `get_mobjects_indicating_movement(self) -> 'list[Mobject]'` — Returns all mobjects whose movement implies that the camera

</details>

### `MultiCamera(image_mobjects_from_cameras: 'Iterable[ImageMobjectFromCamera] | None' = None, allow_cameras_to_capture_their_own_display: 'bool' = False, **kwargs: 'Any') -> 'None'` ← MovingCamera
> Camera Object that allows for multiple perspectives.

<details><summary>métodos próprios (6) · herdados: 44</summary>

- `__init__(self, image_mobjects_from_cameras: 'Iterable[ImageMobjectFromCamera] | None' = None, allow_cameras_to_capture_their_own_display: 'bool' = False, **kwargs: 'Any') -> 'None'` — Initialises the MultiCamera
- `add_image_mobject_from_camera(self, image_mobject_from_camera: 'ImageMobjectFromCamera') -> 'None'` — Adds an ImageMobject that's been obtained from the camera
- `capture_mobjects(self, mobjects: 'Iterable[Mobject]', **kwargs: 'Any') -> 'None'` — Capture mobjects by printing them on :attr:`pixel_array`.
- `get_mobjects_indicating_movement(self) -> 'list[Mobject]'` — Returns all mobjects whose movement implies that the camera
- `reset(self) -> 'Self'` — Resets the MultiCamera.
- `update_sub_cameras(self) -> 'None'` — Reshape sub_camera pixel_arrays

</details>

### `OldMultiCamera(*cameras_with_start_positions, **kwargs)` ← Camera
> Parameters

<details><summary>métodos próprios (5) · herdados: 41</summary>

- `__init__(self, *cameras_with_start_positions, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `capture_mobjects(self, mobjects, **kwargs)` — Capture mobjects by printing them on :attr:`pixel_array`.
- `init_background(self)` — Initialize the background.
- `set_background(self, pixel_array, **kwargs)` — Sets the background to the passed pixel_array after converting
- `set_pixel_array(self, pixel_array, **kwargs)` — Sets the pixel array of the camera to the passed pixel array.

</details>

### `SplitScreenCamera(left_camera, right_camera, **kwargs)` ← OldMultiCamera
> Initializes a split screen camera setup with two side-by-side cameras.

<details><summary>métodos próprios (1) · herdados: 45</summary>

- `__init__(self, left_camera, right_camera, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ThreeDCamera(focal_distance: 'float' = 20.0, shading_factor: 'float' = 0.2, default_distance: 'float' = 5.0, light_source_start_point: 'Point3DLike' = array([-7., -9., 10.]), should_apply_shading: 'bool' = True, exponential_projection: 'bool' = False, phi: 'float' = 0, theta: 'float' = -1.5707963267948966, gamma: 'float' = 0, zoom: 'float' = 1, **kwargs: 'Any')` ← Camera
> Base camera class.

<details><summary>métodos próprios (27) · herdados: 40</summary>

- `__init__(self, focal_distance: 'float' = 20.0, shading_factor: 'float' = 0.2, default_distance: 'float' = 5.0, light_source_start_point: 'Point3DLike' = array([-7., -9., 10.]), should_apply_shading: 'bool' = True, exponential_projection: 'bool' = False, phi: 'float' = 0, theta: 'float' = -1.5707963267948966, gamma: 'float' = 0, zoom: 'float' = 1, **kwargs: 'Any')` — Initializes the ThreeDCamera
- `add_fixed_in_frame_mobjects(self, *mobjects: 'Mobject') -> 'None'` — This method allows the mobject to have a fixed position,
- `add_fixed_orientation_mobjects(self, *mobjects: 'Mobject', use_static_center_func: 'bool' = False, center_func: 'Callable[[], Point3D] | None' = None) -> 'None'` — This method allows the mobject to have a fixed orientation,
- `capture_mobjects(self, mobjects: 'Iterable[Mobject]', **kwargs: 'Any') -> 'None'` — Capture mobjects by printing them on :attr:`pixel_array`.
- `generate_rotation_matrix(self) -> 'MatrixMN'` — Generates a rotation matrix based off the current position of the camera.
- `get_fill_rgbas(self, vmobject: 'VMobject') -> 'FloatRGBA_Array'` — Returns the RGBA array of the fill of the passed VMobject
- `get_focal_distance(self) -> 'float'` — Returns focal_distance of the Camera.
- `get_gamma(self) -> 'float'` — Returns the rotation of the camera about the vector from the ORIGIN to the Camera.
- `get_mobjects_to_display(self, *args: 'Any', **kwargs: 'Any') -> 'list[Mobject]'` — Used to get the list of mobjects to display
- `get_phi(self) -> 'float'` — Returns the Polar angle (the angle off Z_AXIS) phi.
- `get_rotation_matrix(self) -> 'MatrixMN'` — Returns the matrix corresponding to the current position of the camera.
- `get_stroke_rgbas(self, vmobject: 'VMobject', background: 'bool' = False) -> 'FloatRGBA_Array'` — Gets the RGBA array for the stroke of the passed
- `get_theta(self) -> 'float'` — Returns the Azimuthal i.e the angle that spins the camera around the Z_AXIS.
- `get_value_trackers(self) -> 'list[ValueTracker]'` — A list of :class:`ValueTrackers <.ValueTracker>` of phi, theta, focal_distance,
- `get_zoom(self) -> 'float'` — Returns the zoom amount of the camera.
- `modified_rgbas(self, vmobject: 'VMobject', rgbas: 'FloatRGBA_Array') -> 'FloatRGBA_Array'`
- `project_point(self, point: 'Point3D') -> 'Point3D'` — Applies the current rotation_matrix as a projection
- `project_points(self, points: 'Point3D_Array') -> 'Point3D_Array'` — Applies the current rotation_matrix as a projection
- `remove_fixed_in_frame_mobjects(self, *mobjects: 'Mobject') -> 'None'` — If a mobject was fixed in frame by passing it through
- `remove_fixed_orientation_mobjects(self, *mobjects: 'Mobject') -> 'None'` — If a mobject was fixed in its orientation by passing it through
- `reset_rotation_matrix(self) -> 'None'` — Sets the value of self.rotation_matrix to
- `set_focal_distance(self, value: 'float') -> 'None'` — Sets the focal_distance of the Camera.
- `set_gamma(self, value: 'float') -> 'None'` — Sets the angle of rotation of the camera about the vector from the ORIGIN to the Camera.
- `set_phi(self, value: 'float') -> 'None'` — Sets the polar angle i.e the angle between Z_AXIS and Camera through ORIGIN in radians.
- `set_theta(self, value: 'float') -> 'None'` — Sets the azimuthal angle i.e the angle that spins the camera around Z_AXIS in radians.
- `set_zoom(self, value: 'float') -> 'None'` — Sets the zoom amount of the camera.
- `transform_points_pre_display(self, mobject: 'Mobject', points: 'Point3D_Array') -> 'Point3D_Array'`

</details>

- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `CAP_STYLE_MAP` = `{<CapStyleType.AUTO: 0>: None, <CapStyleType.ROUND: 1>: cairo.LineCap.ROUND, <CapStyleType.BUTT: 2>: cairo.LineCap.BU...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `LINE_JOIN_MAP` = `{<LineJointType.AUTO: 0>: None, <LineJointType.ROUND: 1>: cairo.LineJoin.ROUND, <LineJointType.BEVEL: 2>: cairo.LineJ...`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `START_X` = `30`
- `START_X` = `30`
- `START_Y` = `20`
- `START_Y` = `20`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `WHITE` = `ManimColor('#FFFFFF')`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`

## config

### `JSONFormatter(fmt=None, datefmt=None, style='%', validate=True, *, defaults=None)` ← Formatter
> A formatter that outputs logs in a custom JSON format.

<details><summary>métodos próprios (1) · herdados: 7</summary>

- `format(self, record: 'logging.LogRecord') -> 'str'` — Format the record in a custom JSON format.

</details>

### `ManimConfig() -> 'None'` ← MutableMapping
> Dict-like class storing all config options.

<details><summary>métodos próprios (8) · herdados: 8</summary>

- `__init__(self) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `copy(self) -> 'Self'` — Deepcopy the contents of this ManimConfig.
- `digest_args(self, args: 'argparse.Namespace') -> 'Self'` — Process the config options present in CLI arguments.
- `digest_file(self, filename: 'StrPath') -> 'Self'` — Process the config options present in a ``.cfg`` file.
- `digest_parser(self, parser: 'configparser.ConfigParser') -> 'Self'` — Process the config options present in a :class:`ConfigParser` object.
- `get_dir(self, key: 'str', **kwargs: 'Any') -> 'Path'` — Resolve a config option that stores a directory.
- `resolve_movie_file_extension(self, is_transparent: 'bool') -> 'None'`
- `update(self, obj: 'ManimConfig | dict[str, Any]') -> 'None'` — Digest the options found in another :class:`ManimConfig` or in a dict.

</details>

### `ManimFrame(c: 'ManimConfig') -> 'None'` ← Mapping
> A Mapping is a generic container for associating key/value

<details><summary>métodos próprios (1) · herdados: 4</summary>

- `__init__(self, c: 'ManimConfig') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

- `HIGHLIGHTED_KEYWORDS` = `['Played', 'animations', 'scene', 'Reading', 'Writing', 'script', 'arguments', 'Invalid', 'Aborting', 'module', 'File...`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `WRONG_COLOR_CONFIG_MSG` = `"\n[logging.level.error]Your colour configuration couldn't be parsed.\nLoading the default color configuration.[/logg...`
- **`config_file_paths() -> 'list[Path]'`** — The paths where ``.cfg`` files will be searched for.
- **`make_config_parser(custom_file: 'StrPath | None' = None) -> 'configparser.ConfigParser'`** — Make a :class:`ConfigParser` object and load any ``.cfg`` files.
- **`make_logger(parser: 'configparser.SectionProxy', verbosity: 'str') -> 'tuple[logging.Logger, Console, Console]'`** — Make the manim logger and console.
- **`parse_cli_ctx(parser: 'configparser.SectionProxy') -> 'dict[str, Any]'`**
- **`parse_theme(parser: 'configparser.SectionProxy') -> 'Theme | None'`** — Configure the rich style of logger and console output.
- **`set_file_logger(scene_name: 'str', module_name: 'str', log_dir: 'Path') -> 'None'`** — Add a file handler to manim logger.
- **`tempconfig(temp: 'ManimConfig | dict[str, Any]') -> 'Generator[None, None, None]'`** — Temporarily modifies the global ``config`` object using a context manager.

## constants

### `CapStyleType(*values)` ← Enum
> Collection of available cap styles.

### `LineJointType(*values)` ← Enum
> Collection of available line joint types.

### `QualityDict()` ← dict
> dict() -> new empty dictionary

### `RendererType(*values)` ← Enum
> An enumeration of all renderer types that can be assigned to

- `BOLD` = `'BOLD'`
- `BOOK` = `'BOOK'`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CTRL_VALUE` = `65507`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `HEAVY` = `'HEAVY'`
- `IN` = `array([ 0.,  0., -1.])`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LIGHT` = `'LIGHT'`
- `MEDIUM` = `'MEDIUM'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OBLIQUE` = `'OBLIQUE'`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RIGHT` = `array([1., 0., 0.])`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SHIFT_VALUE` = `65505`
- `SMALL_BUFF` = `0.1`
- `START_X` = `30`
- `START_Y` = `20`
- `TAU` = `6.283185307179586`
- `THIN` = `'THIN'`
- `UL` = `array([-1.,  1.,  0.])`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Z_AXIS` = `array([0., 0., 1.])`

## mobject/3d

### `Arrow3D(start: 'Point3DLike' = array([-1.,  0.,  0.]), end: 'Point3DLike' = array([1., 0., 0.]), thickness: 'float' = 0.02, height: 'float' = 0.3, base_radius: 'float' = 0.08, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), resolution: 'int | tuple[int, int]' = 24, **kwargs: 'Any') -> 'None'` ← Line3D
> An arrow made out of a cylindrical line and a conical tip.

<details><summary>métodos próprios (2) · herdados: 250</summary>

- `__init__(self, start: 'Point3DLike' = array([-1.,  0.,  0.]), end: 'Point3DLike' = array([1., 0., 0.]), thickness: 'float' = 0.02, height: 'float' = 0.3, base_radius: 'float' = 0.08, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), resolution: 'int | tuple[int, int]' = 24, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `get_end(self) -> 'np.ndarray'` — Returns the ending point of the :class:`Line3D`.

</details>

### `Cone(base_radius: 'float' = 1, height: 'float' = 1, direction: 'Vector3DLike' = array([0., 0., 1.]), show_base: 'bool' = False, v_range: 'tuple[float, float]' = (0, 6.283185307179586), u_min: 'float' = 0, checkerboard_colors: 'Iterable[ParsableManimColor] | Literal[False]' = False, **kwargs: 'Any') -> 'None'` ← Surface
> A circular cone.

<details><summary>métodos próprios (6) · herdados: 241</summary>

- `__init__(self, base_radius: 'float' = 1, height: 'float' = 1, direction: 'Vector3DLike' = array([0., 0., 1.]), show_base: 'bool' = False, v_range: 'tuple[float, float]' = (0, 6.283185307179586), u_min: 'float' = 0, checkerboard_colors: 'Iterable[ParsableManimColor] | Literal[False]' = False, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `func(self, u: 'float', v: 'float') -> 'Point3D'` — Converts from spherical coordinates to cartesian.
- `get_direction(self) -> 'Vector3D'` — Returns the current direction of the apex of the :class:`Cone`.
- `get_end(self) -> 'Point3D'` — Returns the point, where the stroke that surrounds the :class:`~.Mobject` ends.
- `get_start(self) -> 'Point3D'` — Returns the point, where the stroke that surrounds the :class:`~.Mobject` starts.
- `set_direction(self, direction: 'Vector3DLike') -> 'Self'` — Changes the direction of the apex of the :class:`Cone`.

</details>

### `ConvexHull3D(*points: 'Point3D', tolerance: 'float' = 1e-05, **kwargs: 'Any')` ← Polyhedron
> A convex hull for a set of points

<details><summary>métodos próprios (1) · herdados: 246</summary>

- `__init__(self, *points: 'Point3D', tolerance: 'float' = 1e-05, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Cube(side_length: 'float' = 2, fill_opacity: 'float' = 0.75, fill_color: 'ParsableManimColor' = ManimColor('#58C4DD'), stroke_width: 'float' = 0, **kwargs: 'Any') -> 'None'` ← VGroup
> A three-dimensional cube.

<details><summary>métodos próprios (3) · herdados: 241</summary>

- `__init__(self, side_length: 'float' = 2, fill_opacity: 'float' = 0.75, fill_color: 'ParsableManimColor' = ManimColor('#58C4DD'), stroke_width: 'float' = 0, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `generate_points(self) -> 'Self'` — Creates the sides of the :class:`Cube`.
- `init_points(self) -> 'Self'`

</details>

### `Cylinder(radius: 'float' = 1, height: 'float' = 2, direction: 'Vector3DLike' = array([0., 0., 1.]), v_range: 'tuple[float, float]' = (0, 6.283185307179586), show_ends: 'bool' = True, resolution: 'int | tuple[int, int]' = (24, 24), **kwargs: 'Any') -> 'None'` ← Surface
> A cylinder, defined by its height, radius and direction,

<details><summary>métodos próprios (5) · herdados: 243</summary>

- `__init__(self, radius: 'float' = 1, height: 'float' = 2, direction: 'Vector3DLike' = array([0., 0., 1.]), v_range: 'tuple[float, float]' = (0, 6.283185307179586), show_ends: 'bool' = True, resolution: 'int | tuple[int, int]' = (24, 24), **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `add_bases(self) -> 'Self'` — Adds the end caps of the cylinder.
- `func(self, u: 'float', v: 'float') -> 'np.ndarray'` — Converts from cylindrical coordinates to cartesian.
- `get_direction(self) -> 'np.ndarray'` — Returns the direction of the central axis of the :class:`Cylinder`.
- `set_direction(self, direction: 'Vector3DLike') -> 'Self'` — Sets the direction of the central axis of the :class:`Cylinder`.

</details>

### `Dodecahedron(edge_length: 'float' = 1, **kwargs: 'Any')` ← Polyhedron
> A dodecahedron, one of the five platonic solids. It has 12 faces, 30 edges and 20 vertices.

<details><summary>métodos próprios (1) · herdados: 246</summary>

- `__init__(self, edge_length: 'float' = 1, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Dot3D(point: 'Point3D' = array([0., 0., 0.]), radius: 'float' = 0.08, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), resolution: 'int | tuple[int, int] | None' = (8, 8), **kwargs: 'Any') -> 'None'` ← Sphere
> A spherical dot.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, point: 'Point3D' = array([0., 0., 0.]), radius: 'float' = 0.08, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), resolution: 'int | tuple[int, int] | None' = (8, 8), **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Icosahedron(edge_length: 'float' = 1, **kwargs: 'Any')` ← Polyhedron
> An icosahedron, one of the five platonic solids. It has 20 faces, 30 edges and 12 vertices.

<details><summary>métodos próprios (1) · herdados: 246</summary>

- `__init__(self, edge_length: 'float' = 1, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Line3D(start: 'Point3DLike' = array([-1.,  0.,  0.]), end: 'Point3DLike' = array([1., 0., 0.]), thickness: 'float' = 0.02, color: 'ParsableManimColor | None' = None, resolution: 'int | tuple[int, int]' = 24, **kwargs: 'Any')` ← Cylinder
> A cylindrical line, for use in ThreeDScene.

<details><summary>métodos próprios (7) · herdados: 245</summary>

- `__init__(self, start: 'Point3DLike' = array([-1.,  0.,  0.]), end: 'Point3DLike' = array([1., 0., 0.]), thickness: 'float' = 0.02, color: 'ParsableManimColor | None' = None, resolution: 'int | tuple[int, int]' = 24, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_end(self) -> 'Point3D'` — Returns the ending point of the :class:`Line3D`.
- `get_start(self) -> 'Point3D'` — Returns the starting point of the :class:`Line3D`.
- `parallel_to(line: 'Line3D', point: 'Point3DLike' = array([0., 0., 0.]), length: 'float' = 5, **kwargs: 'Any') -> 'Line3D'` — Returns a line parallel to another line going through
- `perpendicular_to(line: 'Line3D', point: 'Point3DLike' = array([0., 0., 0.]), length: 'float' = 5, **kwargs: 'Any') -> 'Line3D'` — Returns a line perpendicular to another line going through
- `pointify(self, mob_or_point: 'Mobject | Point3DLike', direction: 'Vector3DLike | None' = None) -> 'Point3D'` — Gets a point representing the center of the :class:`Mobjects <.Mobject>`.
- `set_start_and_end_attrs(self, start: 'Point3DLike', end: 'Point3DLike', **kwargs: 'Any') -> 'Self'` — Sets the start and end points of the line.

</details>

### `Octahedron(edge_length: 'float' = 1, **kwargs: 'Any')` ← Polyhedron
> An octahedron, one of the five platonic solids. It has 8 faces, 12 edges and 6 vertices.

<details><summary>métodos próprios (1) · herdados: 246</summary>

- `__init__(self, edge_length: 'float' = 1, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Polyhedron(vertex_coords: 'Point3DLike_Array', faces_list: 'list[list[int]]', faces_config: 'dict[str, str | int | float | bool]' = {}, graph_config: 'dict[str, Any]' = {})` ← VGroup
> An abstract polyhedra class.

<details><summary>métodos próprios (5) · herdados: 242</summary>

- `__init__(self, vertex_coords: 'Point3DLike_Array', faces_list: 'list[list[int]]', faces_config: 'dict[str, str | int | float | bool]' = {}, graph_config: 'dict[str, Any]' = {})` — Initialize self.  See help(type(self)) for accurate signature.
- `create_faces(self, face_coords: 'Point3DLike_Array') -> 'VGroup'` — Creates VGroup of faces from a list of face coordinates.
- `extract_face_coords(self) -> 'Point3DLike_Array'` — Extracts the coordinates of the vertices in the graph.
- `get_edges(self, faces_list: 'list[list[int]]') -> 'list[tuple[int, int]]'` — Creates list of cyclic pairwise tuples.
- `update_faces(self, m: 'Mobject') -> 'Self'`

</details>

### `Prism(dimensions: 'Vector3DLike' = [3, 2, 1], **kwargs: 'Any') -> 'None'` ← Cube
> A right rectangular prism (or rectangular cuboid).

<details><summary>métodos próprios (2) · herdados: 242</summary>

- `__init__(self, dimensions: 'Vector3DLike' = [3, 2, 1], **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `generate_points(self) -> 'Self'` — Creates the sides of the :class:`Prism`.

</details>

### `Sphere(center: 'Point3DLike' = array([0., 0., 0.]), radius: 'float' = 1, resolution: 'int | Sequence[int] | None' = None, u_range: 'tuple[float, float]' = (0, 6.283185307179586), v_range: 'tuple[float, float]' = (0, 3.141592653589793), **kwargs: 'Any') -> 'None'` ← Surface
> A three-dimensional sphere.

<details><summary>métodos próprios (2) · herdados: 244</summary>

- `__init__(self, center: 'Point3DLike' = array([0., 0., 0.]), radius: 'float' = 1, resolution: 'int | Sequence[int] | None' = None, u_range: 'tuple[float, float]' = (0, 6.283185307179586), v_range: 'tuple[float, float]' = (0, 3.141592653589793), **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `func(self, u: 'float', v: 'float') -> 'Point3D'` — The z values defining the :class:`Sphere` being plotted.

</details>

### `Surface(func: 'Callable[[float, float], np.ndarray]', u_range: 'tuple[float, float]' = (0, 1), v_range: 'tuple[float, float]' = (0, 1), resolution: 'int | Sequence[int]' = 32, surface_piece_config: 'dict' = {}, fill_color: 'ParsableManimColor' = ManimColor('#29ABCA'), fill_opacity: 'float' = 1.0, checkerboard_colors: 'Iterable[ParsableManimColor] | Literal[False]' = [ManimColor('#29ABCA'), ManimColor('#236B8E')], stroke_color: 'ParsableManimColor' = ManimColor('#BBBBBB'), stroke_width: 'float' = 0.5, should_make_jagged: 'bool' = False, pre_function_handle_to_anchor_scale_factor: 'float' = 1e-05, **kwargs: 'Any') -> 'None'` ← VGroup
> Creates a Parametric Surface using a checkerboard pattern.

<details><summary>métodos próprios (4) · herdados: 242</summary>

- `__init__(self, func: 'Callable[[float, float], np.ndarray]', u_range: 'tuple[float, float]' = (0, 1), v_range: 'tuple[float, float]' = (0, 1), resolution: 'int | Sequence[int]' = 32, surface_piece_config: 'dict' = {}, fill_color: 'ParsableManimColor' = ManimColor('#29ABCA'), fill_opacity: 'float' = 1.0, checkerboard_colors: 'Iterable[ParsableManimColor] | Literal[False]' = [ManimColor('#29ABCA'), ManimColor('#236B8E')], stroke_color: 'ParsableManimColor' = ManimColor('#BBBBBB'), stroke_width: 'float' = 0.5, should_make_jagged: 'bool' = False, pre_function_handle_to_anchor_scale_factor: 'float' = 1e-05, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `func(self, u: 'float', v: 'float') -> 'np.ndarray'`
- `set_fill_by_checkerboard(self, *colors: 'ParsableManimColor', opacity: 'float | None' = None) -> 'Self'` — Sets the fill_color of each face of :class:`Surface` in
- `set_fill_by_value(self, axes: 'ThreeDAxes', colorscale: 'Iterable[ParsableManimColor] | Iterable[tuple[ParsableManimColor, float]] | None' = None, axis: 'int' = 2, **kwargs: 'Any') -> 'Self'` — Sets the color of each mobject of a parametric surface to a color

</details>

### `Tetrahedron(edge_length: 'float' = 1, **kwargs: 'Any')` ← Polyhedron
> A tetrahedron, one of the five platonic solids. It has 4 faces, 6 edges, and 4 vertices.

<details><summary>métodos próprios (1) · herdados: 246</summary>

- `__init__(self, edge_length: 'float' = 1, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ThreeDVMobject(shade_in_3d: 'bool' = True, **kwargs: 'Any')` ← VMobject
> A vectorized mobject.

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, shade_in_3d: 'bool' = True, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Torus(major_radius: 'float' = 3, minor_radius: 'float' = 1, u_range: 'tuple[float, float]' = (0, 6.283185307179586), v_range: 'tuple[float, float]' = (0, 6.283185307179586), resolution: 'int | tuple[int, int] | None' = None, **kwargs: 'Any') -> 'None'` ← Surface
> A torus.

<details><summary>métodos próprios (2) · herdados: 244</summary>

- `__init__(self, major_radius: 'float' = 3, minor_radius: 'float' = 1, u_range: 'tuple[float, float]' = (0, 6.283185307179586), v_range: 'tuple[float, float]' = (0, 6.283185307179586), resolution: 'int | tuple[int, int] | None' = None, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `func(self, u: 'float', v: 'float') -> 'Point3D'` — The z values defining the :class:`Torus` being plotted.

</details>

- `BLUE` = `ManimColor('#58C4DD')`
- `BLUE_D` = `ManimColor('#29ABCA')`
- `BLUE_E` = `ManimColor('#236B8E')`
- `BOLD` = `'BOLD'`
- `BOOK` = `'BOOK'`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CTRL_VALUE` = `65507`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `HEAVY` = `'HEAVY'`
- `IN` = `array([ 0.,  0., -1.])`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LIGHT` = `'LIGHT'`
- `LIGHT_GREY` = `ManimColor('#BBBBBB')`
- `MEDIUM` = `'MEDIUM'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OBLIQUE` = `'OBLIQUE'`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RIGHT` = `array([1., 0., 0.])`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SHIFT_VALUE` = `65505`
- `SMALL_BUFF` = `0.1`
- `START_X` = `30`
- `START_Y` = `20`
- `TAU` = `6.283185307179586`
- `THIN` = `'THIN'`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `WHITE` = `ManimColor('#FFFFFF')`
- `X_AXIS` = `array([1., 0., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- **`get_3d_vmob_end_corner(vmob: 'VMobject') -> 'Point3D'`**
- **`get_3d_vmob_end_corner_index(vmob: 'VMobject') -> 'int'`**
- **`get_3d_vmob_end_corner_unit_normal(vmob: 'VMobject') -> 'Vector3D'`**
- **`get_3d_vmob_gradient_start_and_end_points(vmob: 'VMobject') -> 'tuple[Point3D, Point3D]'`**
- **`get_3d_vmob_start_corner(vmob: 'VMobject') -> 'Point3D'`**
- **`get_3d_vmob_start_corner_index(vmob: 'VMobject') -> 'Literal[0]'`**
- **`get_3d_vmob_start_corner_unit_normal(vmob: 'VMobject') -> 'Vector3D'`**
- **`get_3d_vmob_unit_normal(vmob: 'VMobject', point_index: 'int') -> 'Vector3D'`**

## mobject/core

### `AbstractImageMobject(scale_to_resolution: 'int', pixel_array_dtype: 'str' = 'uint8', resampling_algorithm: 'Resampling' = <Resampling.BICUBIC: 3>, **kwargs: 'Any') -> 'None'` ← Mobject
> Automatically filters out black pixels

<details><summary>métodos próprios (5) · herdados: 154</summary>

- `__init__(self, scale_to_resolution: 'int', pixel_array_dtype: 'str' = 'uint8', resampling_algorithm: 'Resampling' = <Resampling.BICUBIC: 3>, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `get_pixel_array(self) -> 'PixelArray'`
- `reset_points(self) -> 'Self'` — Sets :attr:`points` to be the four image corners.
- `set_color(self, color: 'ParsableManimColor' = ManimColor('#F7D96F'), alpha: 'Any' = None, family: 'bool' = True) -> 'Self'` — Condition is function which takes in one arguments, (x, y, z).
- `set_resampling_algorithm(self, resampling_algorithm: 'int') -> 'Self'` — Sets the interpolation method for upscaling the image. By default the image is

</details>

### `CurvesAsSubmobjects(vmobject: 'VMobject', **kwargs) -> 'None'` ← VGroup
> Convert a curve's elements to submobjects.

<details><summary>métodos próprios (2) · herdados: 241</summary>

- `__init__(self, vmobject: 'VMobject', **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `point_from_proportion(self, alpha: 'float') -> 'Point3D'` — Gets the point at a proportion along the path of the :class:`CurvesAsSubmobjects`.

</details>

### `DashedVMobject(vmobject: 'VMobject', num_dashes: 'int' = 15, dashed_ratio: 'float' = 0.5, dash_offset: 'float' = 0, color: 'ManimColor' = ManimColor('#FFFFFF'), equal_lengths: 'bool' = True, **kwargs) -> 'None'` ← VMobject
> A :class:`VMobject` composed of dashes instead of lines.

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, vmobject: 'VMobject', num_dashes: 'int' = 15, dashed_ratio: 'float' = 0.5, dash_offset: 'float' = 0, color: 'ManimColor' = ManimColor('#FFFFFF'), equal_lengths: 'bool' = True, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `FullScreenRectangle(**kwargs: 'Any') -> 'None'` ← ScreenRectangle
> A quadrilateral with two sets of parallel sides.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Group(*mobjects: 'Any', **kwargs: 'Any') -> 'None'` ← Mobject
> Groups together multiple :class:`Mobjects <.Mobject>`.

<details><summary>métodos próprios (1) · herdados: 156</summary>

- `__init__(self, *mobjects: 'Any', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ImageMobject(filename_or_array: 'StrPath | npt.NDArray', scale_to_resolution: 'int' = 1080, invert: 'bool' = False, image_mode: 'str' = 'RGBA', **kwargs: 'Any') -> 'None'` ← AbstractImageMobject
> Displays an Image from a numpy array or a file.

<details><summary>métodos próprios (7) · herdados: 154</summary>

- `__init__(self, filename_or_array: 'StrPath | npt.NDArray', scale_to_resolution: 'int' = 1080, invert: 'bool' = False, image_mode: 'str' = 'RGBA', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `fade(self, darkness: 'float' = 0.5, family: 'bool' = True) -> 'Self'` — Sets the image's opacity using a 1 - alpha relationship.
- `get_pixel_array(self) -> 'PixelArray'` — A simple getter method.
- `get_style(self) -> 'dict[str, Any]'`
- `interpolate_color(self, mobject1: 'Mobject', mobject2: 'Mobject', alpha: 'float') -> 'Self'` — Interpolates the array of pixel color values from one ImageMobject
- `set_color(self, color: 'ParsableManimColor' = ManimColor('#F7D96F'), alpha: 'Any' = None, family: 'bool' = True) -> 'Self'` — Condition is function which takes in one arguments, (x, y, z).
- `set_opacity(self, alpha: 'float') -> 'Self'` — Sets the image's opacity.

</details>

### `ImageMobjectFromCamera(camera: 'MovingCamera', default_display_frame_config: 'dict[str, Any] | None' = None, **kwargs: 'Any') -> 'None'` ← AbstractImageMobject
> Automatically filters out black pixels

<details><summary>métodos próprios (4) · herdados: 156</summary>

- `__init__(self, camera: 'MovingCamera', default_display_frame_config: 'dict[str, Any] | None' = None, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `add_display_frame(self, **kwargs: 'Any') -> 'Self'`
- `get_pixel_array(self) -> 'PixelArray'`
- `interpolate_color(self, mobject1: 'Mobject', mobject2: 'Mobject', alpha: 'float') -> 'Self'`

</details>

### `Mobject(color: 'ParsableManimColor | list[ParsableManimColor]' = ManimColor('#FFFFFF'), name: 'str | None' = None, dim: 'int' = 3, target: 'Mobject | None' = None, z_index: 'float' = 0)`
> Mathematical Object: base class for objects that can be displayed on screen.

<details><summary>métodos próprios (157) · herdados: 0</summary>

- `__init__(self, color: 'ParsableManimColor | list[ParsableManimColor]' = ManimColor('#FFFFFF'), name: 'str | None' = None, dim: 'int' = 3, target: 'Mobject | None' = None, z_index: 'float' = 0)` — Initialize self.  See help(type(self)) for accurate signature.
- `add(self, *mobjects: 'Mobject') -> 'Self'` — Add mobjects as submobjects.
- `add_animation_override(animation_class: 'type[Animation]', override_func: 'FunctionOverride') -> 'None'` — Add an animation override.
- `add_background_rectangle(self, color: 'ParsableManimColor | None' = None, opacity: 'float' = 0.75, **kwargs: 'Any') -> 'Self'` — Add a BackgroundRectangle as submobject.
- `add_background_rectangle_to_family_members_with_points(self, **kwargs: 'Any') -> 'Self'`
- `add_background_rectangle_to_submobjects(self, **kwargs: 'Any') -> 'Self'`
- `add_n_more_submobjects(self, n: 'int') -> 'Self | None'`
- `add_to_back(self, *mobjects: 'Mobject') -> 'Self'` — Add all passed mobjects to the back of the submobjects.
- `add_updater(self, update_function: '_Updater', index: 'int | None' = None, call_updater: 'bool' = False) -> 'Self'` — Add an update function to this mobject.
- `align_data(self, mobject: 'Mobject', skip_point_alignment: 'bool' = False) -> 'Self'` — Aligns the family structure and data of this mobject with another mobject.
- `align_on_border(self, direction: 'Vector3DLike', buff: 'float' = 0.5) -> 'Self'` — Direction just needs to be a vector pointing towards side or
- `align_points(self, mobject: 'Mobject') -> 'Self'`
- `align_points_with_larger(self, larger_mobject: 'Mobject') -> 'Self'`
- `align_submobjects(self, mobject: 'Mobject') -> 'Self'`
- `align_to(self, mobject_or_point: 'Mobject | Point3DLike', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Aligns mobject to another :class:`~.Mobject` in a certain direction.
- `animation_override_for(animation_class: 'type[Animation]') -> 'FunctionOverride | None'` — Returns the function defining a specific animation override for this class.
- `apply_complex_function(self, function: 'Callable[[complex], complex]', *, about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = None) -> 'Self'` — Applies a complex function to a :class:`Mobject`.
- `apply_function(self, function: 'MappingFunction', *, about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = None) -> 'Self'`
- `apply_function_to_position(self, function: 'MappingFunction') -> 'Self'`
- `apply_function_to_submobject_positions(self, function: 'MappingFunction') -> 'Self'`
- `apply_matrix(self, matrix: 'MatrixMN', *, about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = None) -> 'Self'`
- `apply_over_attr_arrays(self, func: 'MultiMappingFunction') -> 'Self'`
- `apply_points_function_about_point(self, func: 'MultiMappingFunction', about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = None) -> 'Self'`
- `apply_to_family(self, func: 'Callable[[Mobject], None]') -> 'Self'` — Apply a function to ``self`` and every submobject with points recursively.
- `arrange(self, direction: 'Vector3DLike' = array([1., 0., 0.]), buff: 'float' = 0.25, center: 'bool' = True, **kwargs: 'Any') -> 'Self'` — Sorts :class:`~.Mobject` next to each other on screen.
- `arrange_in_grid(self, rows: 'int | None' = None, cols: 'int | None' = None, buff: 'float | tuple[float, float]' = 0.25, cell_alignment: 'Vector3DLike' = array([0., 0., 0.]), row_alignments: 'str | None' = None, col_alignments: 'str | None' = None, row_heights: 'Iterable[float | None] | None' = None, col_widths: 'Iterable[float | None] | None' = None, flow_order: 'str' = 'rd', **kwargs: 'Any') -> 'Self'` — Arrange submobjects in a grid.
- `arrange_submobjects(self, *args: 'Any', **kwargs: 'Any') -> 'Self'` — Arrange the position of :attr:`submobjects` with a small buffer.
- `become(self, mobject: 'Mobject', match_height: 'bool' = False, match_width: 'bool' = False, match_depth: 'bool' = False, match_center: 'bool' = False, stretch: 'bool' = False) -> 'Self'` — Edit points, colors and submobjects to be identical
- `center(self) -> 'Self'` — Moves the center of the mobject to the center of the scene.
- `clear_updaters(self, recursive: 'bool' = True) -> 'Self'` — Remove every updater.
- `copy(self) -> 'Self'` — Create and return an identical copy of the :class:`Mobject` including all
- `fade(self, darkness: 'float' = 0.5, family: 'bool' = True) -> 'Self'`
- `fade_to(self, color: 'ParsableManimColor', alpha: 'float', family: 'bool' = True) -> 'Self'`
- `family_members_with_points(self) -> 'list[Mobject]'` — Filters the list of family members (generated by :meth:`.get_family`) to include only mobjects with points.
- `flip(self, axis: 'Vector3DLike' = array([0., 1., 0.]), *, about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = None) -> 'Self'` — Flips/Mirrors an mobject about its center.
- `generate_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `generate_target(self, use_deepcopy: 'bool' = False) -> 'Self'`
- `get_all_points(self) -> 'Point3D_Array'` — Return all points from this mobject and all submobjects.
- `get_array_attrs(self) -> 'list[str]'`
- `get_bottom(self) -> 'Point3D'` — Get bottom Point3Ds of a box bounding the :class:`~.Mobject`
- `get_boundary_point(self, direction: 'Vector3DLike') -> 'Point3D'`
- `get_center(self) -> 'Point3D'` — Get center Point3Ds
- `get_center_of_mass(self) -> 'Point3D'`
- `get_color(self) -> 'ManimColor'` — Returns the color of the :class:`~.Mobject`
- `get_coord(self, dim: 'int', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'float'` — Meant to generalize ``get_x``, ``get_y`` and ``get_z``
- `get_corner(self, direction: 'Vector3DLike') -> 'Point3D'` — Get corner Point3Ds for certain direction.
- `get_critical_point(self, direction: 'Vector3DLike') -> 'Point3D'` — Picture a box bounding the :class:`~.Mobject`.  Such a box has
- `get_edge_center(self, direction: 'Vector3DLike') -> 'Point3D'` — Get edge Point3Ds for certain direction.
- `get_end(self) -> 'Point3D'` — Returns the point, where the stroke that surrounds the :class:`~.Mobject` ends.
- `get_extremum_along_dim(self, points: 'Point3DLike_Array | None' = None, dim: 'int' = 0, key: 'int' = 0) -> 'float'`
- `get_family(self, recurse: 'bool' = True) -> 'list[Mobject]'` — Lists all mobjects in the hierarchy (family) of the given mobject,
- `get_family_updaters(self) -> 'list[_Updater]'`
- `get_group_class(self) -> 'type[Group]'`
- `get_image(self, camera: 'Camera | None' = None) -> 'Image.Image'`
- `get_left(self) -> 'Point3D'` — Get left Point3Ds of a box bounding the :class:`~.Mobject`
- `get_merged_array(self, array_attr: 'str') -> 'np.ndarray'` — Return all of a given attribute from this mobject and all submobjects.
- `get_midpoint(self) -> 'Point3D'` — Get Point3Ds of the middle of the path that forms the  :class:`~.Mobject`.
- `get_mobject_type_class() -> 'type[Mobject]'` — Return the base class of this mobject type.
- `get_nadir(self) -> 'Point3D'` — Get nadir (opposite the zenith) Point3Ds of a box bounding a 3D :class:`~.Mobject`.
- `get_num_points(self) -> 'int'`
- `get_pieces(self, n_pieces: 'float') -> 'Group'`
- `get_point_mobject(self, center: 'Point3DLike | None' = None) -> 'Point'` — The simplest :class:`~.Mobject` to be transformed to or from self.
- `get_points_defining_boundary(self) -> 'Point3D_Array'`
- `get_right(self) -> 'Point3D'` — Get right Point3Ds of a box bounding the :class:`~.Mobject`
- `get_start(self) -> 'Point3D'` — Returns the point, where the stroke that surrounds the :class:`~.Mobject` starts.
- `get_start_and_end(self) -> 'tuple[Point3D, Point3D]'` — Returns starting and ending point of a stroke as a ``tuple``.
- `get_time_based_updaters(self) -> 'list[_TimeBasedUpdater]'` — Return all updaters using the ``dt`` parameter.
- `get_top(self) -> 'Point3D'` — Get top Point3Ds of a box bounding the :class:`~.Mobject`
- `get_updaters(self) -> 'list[_Updater]'` — Return all updaters.
- `get_x(self, direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'float'` — Returns x Point3D of the center of the :class:`~.Mobject` as ``float``
- `get_y(self, direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'float'` — Returns y Point3D of the center of the :class:`~.Mobject` as ``float``
- `get_z(self, direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'float'` — Returns z Point3D of the center of the :class:`~.Mobject` as ``float``
- `get_z_index_reference_point(self) -> 'Point3D'`
- `get_zenith(self) -> 'Point3D'` — Get zenith Point3Ds of a box bounding a 3D :class:`~.Mobject`.
- `has_no_points(self) -> 'bool'` — Check if :class:`~.Mobject` *does not* contains points.
- `has_points(self) -> 'bool'` — Check if :class:`~.Mobject` contains points.
- `has_time_based_updater(self) -> 'bool'` — Test if ``self`` has a time based updater.
- `init_colors(self, propagate_colors: 'bool' = True) -> 'Self'` — Initializes the colors.
- `insert(self, index: 'int', mobject: 'Mobject') -> 'Self'` — Inserts a mobject at a specific position into self.submobjects
- `interpolate(self, mobject1: 'Mobject', mobject2: 'Mobject', alpha: 'float', path_func: 'PathFuncType' = <function interpolate at 0x713b87942020>) -> 'Self'` — Turns this :class:`~.Mobject` into an interpolation between ``mobject1``
- `interpolate_color(self, mobject1: 'Mobject', mobject2: 'Mobject', alpha: 'float') -> 'Self'`
- `invert(self, recursive: 'bool' = False) -> 'Self'` — Inverts the list of :attr:`submobjects`.
- `is_off_screen(self) -> 'bool'`
- `length_over_dim(self, dim: 'int') -> 'float'` — Measure the length of an :class:`~.Mobject` in a certain direction.
- `match_color(self, mobject: 'Mobject') -> 'Self'` — Match the color with the color of another :class:`~.Mobject`.
- `match_coord(self, mobject: 'Mobject', dim: 'int', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Match the Point3Ds with the Point3Ds of another :class:`~.Mobject`.
- `match_depth(self, mobject: 'Mobject', **kwargs: 'Any') -> 'Self'` — Match the depth with the depth of another :class:`~.Mobject`.
- `match_dim_size(self, mobject: 'Mobject', dim: 'int', **kwargs: 'Any') -> 'Self'` — Match the specified dimension with the dimension of another :class:`~.Mobject`.
- `match_height(self, mobject: 'Mobject', **kwargs: 'Any') -> 'Self'` — Match the height with the height of another :class:`~.Mobject`.
- `match_points(self, mobject: 'Mobject', copy_submobjects: 'bool' = True) -> 'Self'` — Edit points, positions, and submobjects to be identical
- `match_updaters(self, mobject: 'Mobject') -> 'Self'` — Match the updaters of the given mobject.
- `match_width(self, mobject: 'Mobject', **kwargs: 'Any') -> 'Self'` — Match the width with the width of another :class:`~.Mobject`.
- `match_x(self, mobject: 'Mobject', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Match x coord. to the x coord. of another :class:`~.Mobject`.
- `match_y(self, mobject: 'Mobject', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Match y coord. to the x coord. of another :class:`~.Mobject`.
- `match_z(self, mobject: 'Mobject', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Match z coord. to the x coord. of another :class:`~.Mobject`.
- `move_to(self, point_or_mobject: 'Point3DLike | Mobject', aligned_edge: 'Vector3DLike' = array([0., 0., 0.]), coor_mask: 'Vector3DLike' = array([1, 1, 1])) -> 'Self'` — Move center of the :class:`~.Mobject` to certain Point3D.
- `next_to(self, mobject_or_point: 'Mobject | Point3DLike', direction: 'Vector3DLike' = array([1., 0., 0.]), buff: 'float' = 0.25, aligned_edge: 'Vector3DLike' = array([0., 0., 0.]), submobject_to_align: 'Mobject | None' = None, index_of_submobject_to_align: 'int | None' = None, coor_mask: 'Vector3DLike' = array([1, 1, 1])) -> 'Self'` — Move this :class:`~.Mobject` next to another's :class:`~.Mobject` or Point3D.
- `nonempty_submobjects(self) -> 'Sequence[Mobject]'`
- `null_point_align(self, mobject: 'Mobject') -> 'Self'` — If a :class:`~.Mobject` with points is being aligned to
- `point_from_proportion(self, alpha: 'float') -> 'Point3D'`
- `pose_at_angle(self, **kwargs: 'Any') -> 'Self'`
- `proportion_from_point(self, point: 'Point3DLike') -> 'float'`
- `push_self_into_submobjects(self) -> 'Self'`
- `put_start_and_end_on(self, start: 'Point3DLike', end: 'Point3DLike') -> 'Self'`
- `reduce_across_dimension(self, reduce_func: 'Callable[[Iterable[float]], float]', dim: 'int') -> 'float | None'` — Find the min or max value from a dimension across all points in this Mobject and its
- `remove(self, *mobjects: 'Mobject') -> 'Self'` — Remove :attr:`submobjects`.
- `remove_updater(self, update_function: '_Updater') -> 'Self'` — Remove an updater.
- `repeat(self, count: 'int') -> 'Self'` — This can make transition animations nicer
- `repeat_submobject(self, submob: 'Mobject') -> 'Mobject'`
- `replace(self, mobject: 'Mobject', dim_to_match: 'int' = 0, stretch: 'bool' = False) -> 'Self'`
- `rescale_to_fit(self, length: 'float', dim: 'int', stretch: 'bool' = False, **kwargs: 'Any') -> 'Self'`
- `reset_points(self) -> 'Self'` — Sets :attr:`points` to be an empty array.
- `restore(self) -> 'Self'` — Restores the state that was previously saved with :meth:`~.Mobject.save_state`.
- `resume_updating(self, recursive: 'bool' = True) -> 'Self'` — Enable updating from updaters and animations.
- `reverse_points(self) -> 'Self'`
- `rotate(self, angle: 'float', axis: 'Vector3DLike' = array([0., 0., 1.]), *, about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = None, **kwargs: 'Any') -> 'Self'` — Rotates the :class:`~.Mobject` around a specified axis and point.
- `rotate_about_origin(self, angle: 'float', axis: 'Vector3DLike' = array([0., 0., 1.])) -> 'Self'` — Rotates the :class:`~.Mobject` about the ORIGIN, which is at [0,0,0].
- `save_image(self, name: 'str | None' = None) -> 'None'` — Saves an image of only this :class:`Mobject` at its position to a png
- `save_state(self) -> 'Self'` — Save the current state (position, color & size). Can be restored with :meth:`~.Mobject.restore`.
- `scale(self, scale_factor: 'float', *, about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = None) -> 'Self'` — Scale the size by a factor.
- `scale_to_fit_depth(self, depth: 'float', **kwargs: 'Any') -> 'Self'` — Scales the :class:`~.Mobject` to fit a depth while keeping width/height proportional.
- `scale_to_fit_height(self, height: 'float', **kwargs: 'Any') -> 'Self'` — Scales the :class:`~.Mobject` to fit a height while keeping width/depth proportional.
- `scale_to_fit_width(self, width: 'float', **kwargs: 'Any') -> 'Self'` — Scales the :class:`~.Mobject` to fit a width while keeping height/depth proportional.
- `set(self, **kwargs: 'Any') -> 'Self'` — Sets attributes.
- `set_color(self, color: 'ParsableManimColor' = ManimColor('#FFFF00'), alpha: 'Any' = None, family: 'bool' = True) -> 'Self'` — Condition is function which takes in one arguments, (x, y, z).
- `set_color_by_gradient(self, *colors: 'ParsableManimColor') -> 'Self'` — Parameters
- `set_colors_by_radial_gradient(self, center: 'Point3DLike | None' = None, radius: 'float' = 1, inner_color: 'ParsableManimColor' = ManimColor('#FFFFFF'), outer_color: 'ParsableManimColor' = ManimColor('#000000')) -> 'Self'`
- `set_coord(self, value: 'float', dim: 'int', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'`
- `set_default(**kwargs: 'Any') -> 'None'` — Sets the default values of keyword arguments.
- `set_submobject_colors_by_gradient(self, *colors: 'ParsableManimColor') -> 'Self'`
- `set_submobject_colors_by_radial_gradient(self, center: 'Point3DLike | None' = None, radius: 'float' = 1, inner_color: 'ParsableManimColor' = ManimColor('#FFFFFF'), outer_color: 'ParsableManimColor' = ManimColor('#000000')) -> 'Self'`
- `set_x(self, x: 'float', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Set x value of the center of the :class:`~.Mobject` (``int`` or ``float``)
- `set_y(self, y: 'float', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Set y value of the center of the :class:`~.Mobject` (``int`` or ``float``)
- `set_z(self, z: 'float', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Set z value of the center of the :class:`~.Mobject` (``int`` or ``float``)
- `set_z_index(self, z_index_value: 'float', family: 'bool' = True) -> 'Self'` — Sets the :class:`~.Mobject`'s :attr:`z_index` to the value specified in `z_index_value`.
- `set_z_index_by_z_Point3D(self) -> 'Self'` — Sets the :class:`~.Mobject`'s z Point3D to the value of :attr:`z_index`.
- `shift(self, *vectors: 'Vector3DLike') -> 'Self'` — Shift by the given vectors.
- `shift_onto_screen(self, **kwargs: 'Any') -> 'Self'`
- `show(self, camera: 'Camera | None' = None) -> 'None'`
- `shuffle(self, recursive: 'bool' = False) -> 'Self'` — Shuffles the list of :attr:`submobjects`.
- `shuffle_submobjects(self, *args: 'Any', **kwargs: 'Any') -> 'Self'` — Shuffles the order of :attr:`submobjects`
- `sort(self, point_to_num_func: 'Callable[[Point3DLike], float]' = <function Mobject.<lambda> at 0x713b879e4680>, submob_func: 'Callable[[Mobject], Any] | None' = None) -> 'Self'` — Sorts the list of :attr:`submobjects` by a function defined by ``submob_func``.
- `sort_submobjects(self, *args: 'Any', **kwargs: 'Any') -> 'Self'` — Sort the :attr:`submobjects`
- `space_out_submobjects(self, factor: 'float' = 1.5, **kwargs: 'Any') -> 'Self'`
- `split(self) -> 'list[Mobject]'`
- `stretch(self, factor: 'float', dim: 'int', *, about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = None) -> 'Self'`
- `stretch_about_point(self, factor: 'float', dim: 'int', point: 'Point3DLike') -> 'Self'`
- `stretch_to_fit_depth(self, depth: 'float', **kwargs: 'Any') -> 'Self'` — Stretches the :class:`~.Mobject` to fit a depth, not keeping width/height proportional.
- `stretch_to_fit_height(self, height: 'float', **kwargs: 'Any') -> 'Self'` — Stretches the :class:`~.Mobject` to fit a height, not keeping width/depth proportional.
- `stretch_to_fit_width(self, width: 'float', **kwargs: 'Any') -> 'Self'` — Stretches the :class:`~.Mobject` to fit a width, not keeping height/depth proportional.
- `surround(self, mobject: 'Mobject', dim_to_match: 'int' = 0, stretch: 'bool' = False, buff: 'float' = 0.25) -> 'Self'`
- `suspend_updating(self, recursive: 'bool' = True) -> 'Self'` — Disable updating from updaters and animations.
- `throw_error_if_no_points(self) -> 'None'`
- `to_corner(self, corner: 'Vector3DLike' = array([-1., -1.,  0.]), buff: 'float' = 0.5) -> 'Self'` — Moves this :class:`~.Mobject` to the given corner of the screen.
- `to_edge(self, edge: 'Vector3DLike' = array([-1.,  0.,  0.]), buff: 'float' = 0.5) -> 'Self'` — Moves this :class:`~.Mobject` to the given edge of the screen,
- `to_original_color(self) -> 'Self'`
- `update(self, dt: 'float' = 0, recursive: 'bool' = True) -> 'Self'` — Apply all updaters.

</details>

### `Mobject1D(density: 'int' = 10, **kwargs: 'Any') -> 'None'` ← PMobject
> A disc made of a cloud of Dots

<details><summary>métodos próprios (2) · herdados: 166</summary>

- `__init__(self, density: 'int' = 10, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `add_line(self, start: 'npt.NDArray', end: 'npt.NDArray', color: 'ParsableManimColor | None' = None) -> 'Self'`

</details>

### `Mobject2D(density: 'int' = 25, **kwargs: 'Any') -> 'None'` ← PMobject
> A disc made of a cloud of Dots

<details><summary>métodos próprios (1) · herdados: 166</summary>

- `__init__(self, density: 'int' = 25, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `PGroup(*pmobs: 'Any', **kwargs: 'Any') -> 'None'` ← PMobject
> A group for several point mobjects.

<details><summary>métodos próprios (2) · herdados: 165</summary>

- `__init__(self, *pmobs: 'Any', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `fade_to(self, color: 'ParsableManimColor', alpha: 'float', family: 'bool' = True) -> 'Self'`

</details>

### `PMobject(stroke_width: 'int' = 4, **kwargs: 'Any') -> 'None'` ← Mobject
> A disc made of a cloud of Dots

<details><summary>métodos próprios (23) · herdados: 144</summary>

- `__init__(self, stroke_width: 'int' = 4, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `add_points(self, points: 'Point3DLike_Array', rgbas: 'FloatRGBALike_Array | None' = None, color: 'ParsableManimColor | None' = None, alpha: 'float' = 1.0) -> 'Self'` — Add points.
- `align_points_with_larger(self, larger_mobject: 'Mobject') -> 'Self'`
- `fade_to(self, color: 'ParsableManimColor', alpha: 'float', family: 'bool' = True) -> 'Self'`
- `filter_out(self, condition: 'npt.NDArray') -> 'Self'`
- `get_all_rgbas(self) -> 'npt.NDArray'`
- `get_array_attrs(self) -> 'list[str]'`
- `get_color(self) -> 'ManimColor'` — Returns the color of the :class:`~.Mobject`
- `get_mobject_type_class() -> 'type[PMobject]'` — Return the base class of this mobject type.
- `get_point_mobject(self, center: 'Point3DLike | None' = None) -> 'Point'` — The simplest :class:`~.Mobject` to be transformed to or from self.
- `get_stroke_width(self) -> 'int'`
- `ingest_submobjects(self) -> 'Self'`
- `interpolate_color(self, mobject1: 'Mobject', mobject2: 'Mobject', alpha: 'float') -> 'Self'`
- `match_colors(self, mobject: 'Mobject') -> 'Self'`
- `point_from_proportion(self, alpha: 'float') -> 'Any'`
- `pointwise_become_partial(self, mobject: 'Mobject', a: 'float', b: 'float') -> 'Self'`
- `reset_points(self) -> 'Self'` — Sets :attr:`points` to be an empty array.
- `set_color(self, color: 'ParsableManimColor' = ManimColor('#FFFF00'), family: 'bool' = True) -> 'Self'` — Condition is function which takes in one arguments, (x, y, z).
- `set_color_by_gradient(self, *colors: 'ParsableManimColor') -> 'Self'` — Parameters
- `set_colors_by_radial_gradient(self, center: 'Point3DLike | None' = None, radius: 'float' = 1, inner_color: 'ParsableManimColor' = ManimColor('#FFFFFF'), outer_color: 'ParsableManimColor' = ManimColor('#000000')) -> 'Self'`
- `set_stroke_width(self, width: 'int', family: 'bool' = True) -> 'Self'`
- `sort_points(self, function: 'Callable[[npt.NDArray[ManimFloat]], float]' = <function PMobject.<lambda> at 0x713b859be520>) -> 'Self'` — Function is any map from R^3 to R
- `thin_out(self, factor: 'int' = 5) -> 'Self'` — Removes all but every nth point for n = factor

</details>

### `Point(location: 'Point3DLike' = array([0., 0., 0.]), color: 'ManimColor' = ManimColor('#000000'), **kwargs: 'Any') -> 'None'` ← PMobject
> A mobject representing a point.

<details><summary>métodos próprios (3) · herdados: 165</summary>

- `__init__(self, location: 'Point3DLike' = array([0., 0., 0.]), color: 'ManimColor' = ManimColor('#000000'), **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `generate_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `init_points(self) -> 'Self'`

</details>

### `PointCloudDot(center: 'Point3DLike' = array([0., 0., 0.]), radius: 'float' = 2.0, stroke_width: 'int' = 2, density: 'int' = 10, color: 'ManimColor' = ManimColor('#FFFF00'), **kwargs: 'Any') -> 'None'` ← Mobject1D
> A disc made of a cloud of dots.

<details><summary>métodos próprios (3) · herdados: 166</summary>

- `__init__(self, center: 'Point3DLike' = array([0., 0., 0.]), radius: 'float' = 2.0, stroke_width: 'int' = 2, density: 'int' = 10, color: 'ManimColor' = ManimColor('#FFFF00'), **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `generate_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `init_points(self) -> 'Self'`

</details>

### `ScreenRectangle(aspect_ratio: 'float' = 1.7777777777777777, height: 'float' = 4, **kwargs: 'Any') -> 'None'` ← Rectangle
> A quadrilateral with two sets of parallel sides.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, aspect_ratio: 'float' = 1.7777777777777777, height: 'float' = 4, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `VDict(mapping_or_iterable: 'Mapping[Hashable, VMobject] | Iterable[tuple[Hashable, VMobject]]' = {}, show_keys: 'bool' = False, **kwargs) -> 'None'` ← VMobject
> A VGroup-like class, also offering submobject access by

<details><summary>métodos próprios (5) · herdados: 240</summary>

- `__init__(self, mapping_or_iterable: 'Mapping[Hashable, VMobject] | Iterable[tuple[Hashable, VMobject]]' = {}, show_keys: 'bool' = False, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `add(self, mapping_or_iterable: 'Mapping[Hashable, VMobject] | Iterable[tuple[Hashable, VMobject]]') -> 'Self'` — Adds the key-value pairs to the :class:`VDict` object.
- `add_key_value_pair(self, key: 'Hashable', value: 'VMobject') -> 'Self'` — A utility function used by :meth:`add` to add the key-value pair
- `get_all_submobjects(self) -> 'list[list]'` — To get all the submobjects associated with a particular :class:`VDict` object
- `remove(self, key: 'Hashable') -> 'Self'` — Removes the mobject from the :class:`VDict` object having the key `key`

</details>

### `VGroup(*vmobjects: 'VMobject | Iterable[VMobject]', **kwargs: 'Any') -> 'None'` ← VMobject
> A group of vectorized mobjects.

<details><summary>métodos próprios (2) · herdados: 241</summary>

- `__init__(self, *vmobjects: 'VMobject | Iterable[VMobject]', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `add(self, *vmobjects: 'VMobject | Iterable[VMobject]') -> 'Self'` — Checks if all passed elements are an instance, or iterables of VMobject and then adds them to submobjects

</details>

### `VMobject(fill_color: 'ParsableManimColor | None' = None, fill_opacity: 'float' = 0.0, stroke_color: 'ParsableManimColor | None' = None, stroke_opacity: 'float' = 1.0, stroke_width: 'float' = 4, background_stroke_color: 'ParsableManimColor | None' = ManimColor('#000000'), background_stroke_opacity: 'float' = 1.0, background_stroke_width: 'float' = 0, sheen_factor: 'float' = 0.0, joint_type: 'LineJointType | None' = None, sheen_direction: 'Vector3DLike' = array([-1.,  1.,  0.]), close_new_points: 'bool' = False, pre_function_handle_to_anchor_scale_factor: 'float' = 0.01, make_smooth_after_applying_functions: 'bool' = False, background_image: 'Image | str | None' = None, shade_in_3d: 'bool' = False, tolerance_for_point_equality: 'float' = 1e-06, n_points_per_cubic_curve: 'int' = 4, cap_style: 'CapStyleType' = <CapStyleType.AUTO: 0>, **kwargs: 'Any')` ← Mobject
> A vectorized mobject.

<details><summary>métodos próprios (104) · herdados: 139</summary>

- `__init__(self, fill_color: 'ParsableManimColor | None' = None, fill_opacity: 'float' = 0.0, stroke_color: 'ParsableManimColor | None' = None, stroke_opacity: 'float' = 1.0, stroke_width: 'float' = 4, background_stroke_color: 'ParsableManimColor | None' = ManimColor('#000000'), background_stroke_opacity: 'float' = 1.0, background_stroke_width: 'float' = 0, sheen_factor: 'float' = 0.0, joint_type: 'LineJointType | None' = None, sheen_direction: 'Vector3DLike' = array([-1.,  1.,  0.]), close_new_points: 'bool' = False, pre_function_handle_to_anchor_scale_factor: 'float' = 0.01, make_smooth_after_applying_functions: 'bool' = False, background_image: 'Image | str | None' = None, shade_in_3d: 'bool' = False, tolerance_for_point_equality: 'float' = 1e-06, n_points_per_cubic_curve: 'int' = 4, cap_style: 'CapStyleType' = <CapStyleType.AUTO: 0>, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `add_cubic_bezier_curve(self, anchor1: 'Point3DLike', handle1: 'Point3DLike', handle2: 'Point3DLike', anchor2: 'Point3DLike') -> 'Self'`
- `add_cubic_bezier_curve_to(self, handle1: 'Point3DLike', handle2: 'Point3DLike', anchor: 'Point3DLike') -> 'Self'` — Add cubic bezier curve to the path.
- `add_cubic_bezier_curves(self, curves) -> 'Self'`
- `add_line_to(self, point: 'Point3DLike') -> 'Self'` — Add a straight line from the last point of VMobject to the given point.
- `add_points_as_corners(self, points: 'Point3DLike_Array') -> 'Self'` — Append multiple straight lines at the end of
- `add_quadratic_bezier_curve_to(self, handle: 'Point3DLike', anchor: 'Point3DLike') -> 'Self'` — Add Quadratic bezier curve to the path.
- `add_smooth_curve_to(self, *points: 'Point3DLike') -> 'Self'` — Creates a smooth curve from given points and add it to the VMobject. If two points are passed in, the first is interpreted
- `add_subpath(self, points: 'CubicBezierPathLike') -> 'Self'`
- `align_points(self, vmobject: 'VMobject') -> 'Self'` — Adds points to self and vmobject so that they both have the same number of subpaths, with
- `align_rgbas(self, vmobject: 'VMobject') -> 'Self'`
- `append_points(self, new_points: 'Point3DLike_Array') -> 'Self'` — Append the given ``new_points`` to the end of
- `append_vectorized_mobject(self, vectorized_mobject: 'VMobject') -> 'Self'`
- `apply_function(self, function: 'MappingFunction', *, about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = None) -> 'Self'`
- `change_anchor_mode(self, mode: "Literal['jagged', 'smooth']") -> 'Self'` — Changes the anchor mode of the bezier curves. This will modify the handles.
- `clear_points(self) -> 'Self'`
- `close_path(self) -> 'Self'`
- `color_using_background_image(self, background_image: 'Image | str') -> 'Self'`
- `consider_points_equals(self, p0: 'Point3DLike', p1: 'Point3DLike') -> 'bool'`
- `consider_points_equals_2d(self, p0: 'Point2DLike', p1: 'Point2DLike') -> 'bool'` — Determine if two points are close enough to be considered equal.
- `fade(self, darkness: 'float' = 0.5, family: 'bool' = True) -> 'Self'`
- `force_direction(self, target_direction: "Literal['CW', 'CCW']") -> 'Self'` — Makes sure that points are either directed clockwise or
- `gen_cubic_bezier_tuples_from_points(self, points: 'CubicBezierPathLike') -> 'tuple[CubicBezierPointsLike, ...]'` — Returns the bezier tuples from an array of points.
- `gen_subpaths_from_points_2d(self, points: 'CubicBezierPath') -> 'Iterable[CubicSpline]'`
- `generate_rgbas_array(self, color: 'ParsableManimColor | Iterable[ManimColor] | None', opacity: 'float | Iterable[float]') -> 'FloatRGBA'` — First arg can be either a color, or a tuple/list of colors.
- `get_anchors(self) -> 'list[Point3D]'` — Returns the anchors of the curves forming the VMobject.
- `get_anchors_and_handles(self) -> 'list[Point3D_Array]'` — Returns anchors1, handles1, handles2, anchors2,
- `get_arc_length(self, sample_points_per_curve: 'int | None' = None) -> 'float'` — Return the approximated length of the whole curve.
- `get_background_image(self) -> 'Image | str'`
- `get_color(self) -> 'ManimColor'` — Returns the color of the :class:`~.Mobject`
- `get_cubic_bezier_tuples(self) -> 'CubicBezierPoints_Array'`
- `get_cubic_bezier_tuples_from_points(self, points: 'CubicBezierPathLike') -> 'CubicBezierPoints_Array'`
- `get_curve_functions(self) -> 'Iterable[Callable[[float], Point3D]]'` — Gets the functions for the curves of the mobject.
- `get_curve_functions_with_lengths(self, **kwargs) -> 'Iterable[tuple[Callable[[float], Point3D], float]]'` — Gets the functions and lengths of the curves for the mobject.
- `get_direction(self) -> "Literal['CW', 'CCW']"` — Uses :func:`~.space_ops.shoelace_direction` to calculate the direction.
- `get_end_anchors(self) -> 'Point3D_Array'` — Return the end anchors of the bezier curves.
- `get_fill_color(self) -> 'ManimColor'` — If there are multiple colors (for gradient)
- `get_fill_colors(self) -> 'list[ManimColor | None]'`
- `get_fill_opacities(self) -> 'npt.NDArray[ManimFloat]'`
- `get_fill_opacity(self) -> 'ManimFloat'` — If there are multiple opacities, this returns the
- `get_fill_rgbas(self) -> 'FloatRGBA_Array'`
- `get_gradient_start_and_end_points(self) -> 'tuple[Point3D, Point3D]'`
- `get_group_class(self) -> 'type[VGroup]'`
- `get_last_point(self) -> 'Point3D'`
- `get_mobject_type_class() -> 'type[VMobject]'` — Return the base class of this mobject type.
- `get_nth_curve_function(self, n: 'int') -> 'Callable[[float], Point3D]'` — Returns the expression of the nth curve.
- `get_nth_curve_function_with_length(self, n: 'int', sample_points: 'int | None' = None) -> 'tuple[Callable[[float], Point3D], float]'` — Returns the expression of the nth curve along with its (approximate) length.
- `get_nth_curve_length(self, n: 'int', sample_points: 'int | None' = None) -> 'float'` — Returns the (approximate) length of the nth curve.
- `get_nth_curve_length_pieces(self, n: 'int', sample_points: 'int | None' = None) -> 'npt.NDArray[ManimFloat]'` — Returns the array of short line lengths used for length approximation.
- `get_nth_curve_points(self, n: 'int') -> 'CubicBezierPoints'` — Returns the points defining the nth curve of the vmobject.
- `get_num_curves(self) -> 'int'` — Returns the number of curves of the vmobject.
- `get_point_mobject(self, center: 'Point3DLike | None' = None) -> 'VectorizedPoint'` — The simplest :class:`~.Mobject` to be transformed to or from self.
- `get_points_defining_boundary(self) -> 'Point3D_Array'`
- `get_sheen_direction(self) -> 'Vector3D'`
- `get_sheen_factor(self) -> 'float'`
- `get_start_anchors(self) -> 'Point3D_Array'` — Returns the start anchors of the bezier curves.
- `get_stroke_color(self, background: 'bool' = False) -> 'ManimColor | None'`
- `get_stroke_colors(self, background: 'bool' = False) -> 'list[ManimColor | None]'`
- `get_stroke_opacities(self, background: 'bool' = False) -> 'npt.NDArray[ManimFloat]'`
- `get_stroke_opacity(self, background: 'bool' = False) -> 'ManimFloat'`
- `get_stroke_rgbas(self, background: 'bool' = False) -> 'FloatRGBA_Array'`
- `get_stroke_width(self, background: 'bool' = False) -> 'float'`
- `get_style(self, simple: 'bool' = False) -> 'dict'`
- `get_subcurve(self, a: 'float', b: 'float') -> 'Self'` — Returns the subcurve of the VMobject between the interval [a, b].
- `get_subpath_split_indices_from_points(self, points: 'CubicBezierPathLike', n_dims: 'int' = 3) -> 'npt.NDArray[np.int_]'` — Return the point indices delimiting each subpath in ``points``.
- `get_subpaths(self) -> 'list[CubicSpline]'` — Returns subpaths formed by the curves of the VMobject.
- `get_subpaths_from_points(self, points: 'CubicBezierPath') -> 'list[CubicSpline]'`
- `has_new_path_started(self) -> 'bool'`
- `init_colors(self, propagate_colors: 'bool' = True) -> 'Self'` — Initializes the colors.
- `insert_n_curves(self, n: 'int') -> 'Self'` — Inserts n curves to the bezier curves of the vmobject.
- `insert_n_curves_to_point_list(self, n: 'int', points: 'BezierPathLike') -> 'BezierPath'` — Given an array of k points defining a bezier curves (anchors and handles), returns points defining exactly k + n bezier curves.
- `interpolate_color(self, mobject1: 'VMobject', mobject2: 'VMobject', alpha: 'float') -> 'Self'`
- `is_closed(self) -> 'bool'`
- `make_jagged(self) -> 'Self'`
- `make_smooth(self) -> 'Self'`
- `match_background_image(self, vmobject: 'VMobject') -> 'Self'`
- `match_style(self, vmobject: 'VMobject', family: 'bool' = True) -> 'Self'`
- `nonempty_submobjects(self) -> 'Sequence[VMobject]'`
- `point_from_proportion(self, alpha: 'float') -> 'Point3D'` — Gets the point at a proportion along the path of the :class:`VMobject`.
- `pointwise_become_partial(self, vmobject: 'VMobject', a: 'float', b: 'float') -> 'Self'` — Given a 2nd :class:`.VMobject` ``vmobject``, a lower bound ``a`` and
- `proportion_from_point(self, point: 'Point3DLike') -> 'float'` — Returns the proportion along the path of the :class:`VMobject`
- `resize_points(self, new_length: 'int', resize_func: 'Callable[[Point3D_Array, int], Point3D_Array]' = <function resize_array at 0x713b8b242e80>) -> 'Self'` — Resize the array of anchor points and handles to have
- `reverse_direction(self) -> 'Self'` — Reverts the point direction by inverting the point order.
- `rotate(self, angle: 'float', axis: 'Vector3DLike' = array([0., 0., 1.]), *, about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = None) -> 'Self'` — Rotates the :class:`~.Mobject` around a specified axis and point.
- `rotate_sheen_direction(self, angle: 'float', axis: 'Vector3DLike' = array([0., 0., 1.]), family: 'bool' = True) -> 'Self'` — Rotates the direction of the applied sheen.
- `scale(self, scale_factor: 'float', scale_stroke: 'bool' = False, *, about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = None) -> 'Self'` — Scale the size by a factor.
- `scale_handle_to_anchor_distances(self, factor: 'float') -> 'Self'` — If the distance between a given handle point H and its associated
- `set_anchors_and_handles(self, anchors1: 'Point3DLike_Array', handles1: 'Point3DLike_Array', handles2: 'Point3DLike_Array', anchors2: 'Point3DLike_Array') -> 'Self'` — Given two sets of anchors and handles, process them to set them as anchors
- `set_background_stroke(self, **kwargs) -> 'Self'`
- `set_cap_style(self, cap_style: 'CapStyleType') -> 'Self'` — Sets the cap style of the :class:`VMobject`.
- `set_color(self, color: 'ParsableManimColor', family: 'bool' = True) -> 'Self'` — Condition is function which takes in one arguments, (x, y, z).
- `set_fill(self, color: 'ParsableManimColor | None' = None, opacity: 'float | None' = None, family: 'bool' = True) -> 'Self'` — Set the fill color and fill opacity of a :class:`VMobject`.
- `set_opacity(self, opacity: 'float', family: 'bool' = True) -> 'Self'`
- `set_points(self, points: 'Point3DLike_Array') -> 'Self'`
- `set_points_as_corners(self, points: 'Point3DLike_Array') -> 'Self'` — Given an array of points, set them as corners of the
- `set_points_smoothly(self, points: 'Point3DLike_Array') -> 'Self'`
- `set_shade_in_3d(self, value: 'bool' = True, z_index_as_group: 'bool' = False) -> 'Self'`
- `set_sheen(self, factor: 'float', direction: 'Vector3DLike | None' = None, family: 'bool' = True) -> 'Self'` — Applies a color gradient from a direction.
- `set_sheen_direction(self, direction: 'Vector3DLike', family: 'bool' = True) -> 'Self'` — Sets the direction of the applied sheen.
- `set_stroke(self, color: 'ParsableManimColor' = None, width: 'float | None' = None, opacity: 'float | None' = None, background=False, family: 'bool' = True) -> 'Self'`
- `set_style(self, fill_color: 'ParsableManimColor | None' = None, fill_opacity: 'float | None' = None, stroke_color: 'ParsableManimColor | None' = None, stroke_width: 'float | None' = None, stroke_opacity: 'float | None' = None, background_stroke_color: 'ParsableManimColor | None' = None, background_stroke_width: 'float | None' = None, background_stroke_opacity: 'float | None' = None, sheen_factor: 'float | None' = None, sheen_direction: 'Vector3DLike | None' = None, background_image: 'Image | str | None' = None, family: 'bool' = True) -> 'Self'`
- `split(self) -> 'list[VMobject]'`
- `start_new_path(self, point: 'Point3DLike') -> 'Self'` — Append a ``point`` to the :attr:`VMobject.points`, which will be the
- `update_rgbas_array(self, array_name: 'str', color: 'ParsableManimColor | Iterable[ManimColor] | None' = None, opacity: 'float | None' = None) -> 'Self'`

</details>

### `VectorizedPoint(location: 'Point3DLike' = array([0., 0., 0.]), color: 'ManimColor' = ManimColor('#000000'), fill_opacity: 'float' = 0, stroke_width: 'float' = 0, artificial_width: 'float' = 0.01, artificial_height: 'float' = 0.01, **kwargs) -> 'None'` ← VMobject
> A vectorized mobject.

<details><summary>métodos próprios (3) · herdados: 242</summary>

- `__init__(self, location: 'Point3DLike' = array([0., 0., 0.]), color: 'ManimColor' = ManimColor('#000000'), fill_opacity: 'float' = 0, stroke_width: 'float' = 0, artificial_width: 'float' = 0.01, artificial_height: 'float' = 0.01, **kwargs) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `get_location(self) -> 'Point3D'`
- `set_location(self, new_loc: 'Point3D') -> 'Self'`

</details>

- `BLACK` = `ManimColor('#000000')`
- `BLACK` = `ManimColor('#000000')`
- `BLACK` = `ManimColor('#000000')`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PURE_YELLOW` = `ManimColor('#FFFF00')`
- `PURE_YELLOW` = `ManimColor('#FFFF00')`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `START_X` = `30`
- `START_X` = `30`
- `START_X` = `30`
- `START_X` = `30`
- `START_Y` = `20`
- `START_Y` = `20`
- `START_Y` = `20`
- `START_Y` = `20`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `YELLOW_C` = `ManimColor('#F7D96F')`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- **`get_mobject_class() -> 'type'`** — Gets the base mobject class, depending on the currently active renderer.
- **`get_point_mobject_class() -> 'type'`** — Gets the point cloud mobject class, depending on the currently
- **`get_vectorized_mobject_class() -> 'type'`** — Gets the vectorized mobject class, depending on the currently
- **`override_animate(method: 'types.MethodType') -> 'Callable[[types.MethodType], types.MethodType]'`** — Decorator for overriding method animations.

## mobject/geometry

### `Angle(line1: 'Line', line2: 'Line', radius: 'float | None' = None, quadrant: 'AngleQuadrant' = (1, 1), other_angle: 'bool' = False, dot: 'bool' = False, dot_radius: 'float | None' = None, dot_distance: 'float' = 0.55, dot_color: 'ParsableManimColor' = ManimColor('#FFFFFF'), elbow: 'bool' = False, **kwargs: 'Any') -> 'None'` ← VMobject
> A circular arc or elbow-type mobject representing an angle of two lines.

<details><summary>métodos próprios (4) · herdados: 242</summary>

- `__init__(self, line1: 'Line', line2: 'Line', radius: 'float | None' = None, quadrant: 'AngleQuadrant' = (1, 1), other_angle: 'bool' = False, dot: 'bool' = False, dot_radius: 'float | None' = None, dot_distance: 'float' = 0.55, dot_color: 'ParsableManimColor' = ManimColor('#FFFFFF'), elbow: 'bool' = False, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `from_three_points(A: 'Point3DLike', B: 'Point3DLike', C: 'Point3DLike', **kwargs: 'Any') -> 'Angle'` — The angle between the lines AB and BC.
- `get_lines(self) -> 'VGroup'` — Get the lines forming an angle of the :class:`Angle` class.
- `get_value(self, degrees: 'bool' = False) -> 'float'` — Get the value of an angle of the :class:`Angle` class.

</details>

### `AnnotationDot(radius: 'float' = 0.10400000000000001, stroke_width: 'float' = 5, stroke_color: 'ParsableManimColor' = ManimColor('#FFFFFF'), fill_color: 'ParsableManimColor' = ManimColor('#58C4DD'), **kwargs: 'Any') -> 'None'` ← Dot
> A dot with bigger radius and bold stroke to annotate scenes.

<details><summary>métodos próprios (1) · herdados: 263</summary>

- `__init__(self, radius: 'float' = 0.10400000000000001, stroke_width: 'float' = 5, stroke_color: 'ParsableManimColor' = ManimColor('#FFFFFF'), fill_color: 'ParsableManimColor' = ManimColor('#58C4DD'), **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `AnnularSector(inner_radius: 'float' = 1, outer_radius: 'float' = 2, angle: 'float' = 1.5707963267948966, start_angle: 'float' = 0, fill_opacity: 'float' = 1, stroke_width: 'float' = 0, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), **kwargs: 'Any') -> 'None'` ← Arc
> A sector of an annulus.

<details><summary>métodos próprios (3) · herdados: 259</summary>

- `__init__(self, inner_radius: 'float' = 1, outer_radius: 'float' = 2, angle: 'float' = 1.5707963267948966, start_angle: 'float' = 0, fill_opacity: 'float' = 1, stroke_width: 'float' = 0, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `generate_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `init_points(self) -> 'Self'`

</details>

### `Annulus(inner_radius: 'float' = 1, outer_radius: 'float' = 2, fill_opacity: 'float' = 1, stroke_width: 'float' = 0, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), mark_paths_closed: 'bool' = False, **kwargs: 'Any') -> 'None'` ← Circle
> Region between two concentric :class:`Circles <.Circle>`.

<details><summary>métodos próprios (3) · herdados: 261</summary>

- `__init__(self, inner_radius: 'float' = 1, outer_radius: 'float' = 2, fill_opacity: 'float' = 1, stroke_width: 'float' = 0, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), mark_paths_closed: 'bool' = False, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `generate_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `init_points(self) -> 'Self'`

</details>

### `Arc(radius: 'float | None' = 1.0, start_angle: 'float' = 0, angle: 'float' = 1.5707963267948966, num_components: 'int' = 9, arc_center: 'Point3DLike' = array([0., 0., 0.]), **kwargs: 'Any')` ← TipableVMobject
> A circular arc.

<details><summary>métodos próprios (6) · herdados: 256</summary>

- `__init__(self, radius: 'float | None' = 1.0, start_angle: 'float' = 0, angle: 'float' = 1.5707963267948966, num_components: 'int' = 9, arc_center: 'Point3DLike' = array([0., 0., 0.]), **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `generate_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `get_arc_center(self, warning: 'bool' = True) -> 'Point3D'` — Looks at the normals to the first two
- `init_points(self) -> 'Self'`
- `move_arc_center_to(self, point: 'Point3DLike') -> 'Self'`
- `stop_angle(self) -> 'float'`

</details>

### `ArcBetweenPoints(start: 'Point3DLike', end: 'Point3DLike', angle: 'float' = 1.5707963267948966, radius: 'float | None' = None, **kwargs: 'Any') -> 'None'` ← Arc
> Inherits from Arc and additionally takes 2 points between which the arc is spanned.

<details><summary>métodos próprios (1) · herdados: 261</summary>

- `__init__(self, start: 'Point3DLike', end: 'Point3DLike', angle: 'float' = 1.5707963267948966, radius: 'float | None' = None, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ArcPolygon(*vertices: 'Point3DLike', angle: 'float' = 0.7853981633974483, radius: 'float | None' = None, arc_config: 'list[dict] | None' = None, **kwargs: 'Any') -> 'None'` ← VMobject
> A generalized polygon allowing for points to be connected with arcs.

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, *vertices: 'Point3DLike', angle: 'float' = 0.7853981633974483, radius: 'float | None' = None, arc_config: 'list[dict] | None' = None, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ArcPolygonFromArcs(*arcs: 'Arc | ArcBetweenPoints', **kwargs: 'Any') -> 'None'` ← VMobject
> A generalized polygon allowing for points to be connected with arcs.

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, *arcs: 'Arc | ArcBetweenPoints', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Arrow(*args: 'Any', stroke_width: 'float' = 6, buff: 'float' = 0.25, max_tip_length_to_length_ratio: 'float' = 0.25, max_stroke_width_to_length_ratio: 'float' = 5, **kwargs: 'Any') -> 'None'` ← Line
> An arrow.

<details><summary>métodos próprios (5) · herdados: 265</summary>

- `__init__(self, *args: 'Any', stroke_width: 'float' = 6, buff: 'float' = 0.25, max_tip_length_to_length_ratio: 'float' = 0.25, max_stroke_width_to_length_ratio: 'float' = 5, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `get_default_tip_length(self) -> 'float'` — Returns the default tip_length of the arrow.
- `get_normal_vector(self) -> 'Vector3D'` — Returns the normal of a vector.
- `reset_normal_vector(self) -> 'Self'` — Resets the normal of a vector
- `scale(self, factor: 'float', scale_tips: 'bool' = False, **kwargs: 'Any') -> 'Self'` — Scale an arrow, but keep stroke width and arrow tip size fixed.

</details>

### `ArrowCircleFilledTip(fill_opacity: 'float' = 1, stroke_width: 'float' = 0, **kwargs: 'Any') -> 'None'` ← ArrowCircleTip
> Circular arrow tip with filled tip.

<details><summary>métodos próprios (1) · herdados: 263</summary>

- `__init__(self, fill_opacity: 'float' = 1, stroke_width: 'float' = 0, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ArrowCircleTip(fill_opacity: 'float' = 0, stroke_width: 'float' = 3, length: 'float' = 0.35, start_angle: 'float' = 3.141592653589793, **kwargs: 'Any') -> 'None'` ← ArrowTip, Circle
> Circular arrow tip.

<details><summary>métodos próprios (1) · herdados: 263</summary>

- `__init__(self, fill_opacity: 'float' = 0, stroke_width: 'float' = 3, length: 'float' = 0.35, start_angle: 'float' = 3.141592653589793, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ArrowSquareFilledTip(fill_opacity: 'float' = 1, stroke_width: 'float' = 0, **kwargs: 'Any') -> 'None'` ← ArrowSquareTip
> Square arrow tip with filled tip.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, fill_opacity: 'float' = 1, stroke_width: 'float' = 0, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ArrowSquareTip(fill_opacity: 'float' = 0, stroke_width: 'float' = 3, length: 'float' = 0.35, start_angle: 'float' = 3.141592653589793, **kwargs: 'Any') -> 'None'` ← ArrowTip, Square
> Square arrow tip.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, fill_opacity: 'float' = 0, stroke_width: 'float' = 3, length: 'float' = 0.35, start_angle: 'float' = 3.141592653589793, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ArrowTip(*args: 'Any', **kwargs: 'Any') -> 'None'` ← VMobject
> Base class for arrow tips.

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, *args: 'Any', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ArrowTriangleFilledTip(fill_opacity: 'float' = 1, stroke_width: 'float' = 0, **kwargs: 'Any') -> 'None'` ← ArrowTriangleTip
> Triangular arrow tip with filled tip.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, fill_opacity: 'float' = 1, stroke_width: 'float' = 0, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ArrowTriangleTip(fill_opacity: 'float' = 0, stroke_width: 'float' = 3, length: 'float' = 0.35, width: 'float' = 0.35, start_angle: 'float' = 3.141592653589793, **kwargs: 'Any') -> 'None'` ← ArrowTip, Triangle
> Triangular arrow tip.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, fill_opacity: 'float' = 0, stroke_width: 'float' = 3, length: 'float' = 0.35, width: 'float' = 0.35, start_angle: 'float' = 3.141592653589793, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `BackgroundRectangle(*mobjects: 'Mobject', color: 'ParsableManimColor | None' = None, stroke_width: 'float' = 0, stroke_opacity: 'float' = 0, fill_opacity: 'float' = 0.75, buff: 'float | tuple[float, float]' = 0, **kwargs: 'Any') -> 'None'` ← SurroundingRectangle
> A background rectangle. Its default color is the background color

<details><summary>métodos próprios (3) · herdados: 243</summary>

- `__init__(self, *mobjects: 'Mobject', color: 'ParsableManimColor | None' = None, stroke_width: 'float' = 0, stroke_opacity: 'float' = 0, fill_opacity: 'float' = 0.75, buff: 'float | tuple[float, float]' = 0, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `pointwise_become_partial(self, mobject: 'Mobject', a: 'Any', b: 'float') -> 'Self'` — Given a 2nd :class:`.VMobject` ``vmobject``, a lower bound ``a`` and
- `set_style(self, fill_opacity: 'float', **kwargs: 'Any') -> 'Self'`

</details>

### `Circle(radius: 'float | None' = None, color: 'ParsableManimColor' = ManimColor('#FC6255'), **kwargs: 'Any') -> 'None'` ← Arc
> A circle.

<details><summary>métodos próprios (4) · herdados: 260</summary>

- `__init__(self, radius: 'float | None' = None, color: 'ParsableManimColor' = ManimColor('#FC6255'), **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `from_three_points(p1: 'Point3DLike', p2: 'Point3DLike', p3: 'Point3DLike', **kwargs: 'Any') -> 'Circle'` — Returns a circle passing through the specified
- `point_at_angle(self, angle: 'float') -> 'Point3D'` — Returns the position of a point on the circle.
- `surround(self, mobject: 'Mobject', dim_to_match: 'int' = 0, stretch: 'bool' = False, buffer_factor: 'float' = 1.2) -> 'Self'` — Modifies a circle so that it surrounds a given mobject.

</details>

### `ConvexHull(*points: 'Point3DLike', tolerance: 'float' = 1e-05, **kwargs: 'Any') -> 'None'` ← Polygram
> Constructs a convex hull for a set of points in no particular order.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, *points: 'Point3DLike', tolerance: 'float' = 1e-05, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Cross(mobject: 'Mobject | None' = None, stroke_color: 'ParsableManimColor' = ManimColor('#FC6255'), stroke_width: 'float' = 6.0, scale_factor: 'float' = 1.0, **kwargs: 'Any') -> 'None'` ← VGroup
> Creates a cross.

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, mobject: 'Mobject | None' = None, stroke_color: 'ParsableManimColor' = ManimColor('#FC6255'), stroke_width: 'float' = 6.0, scale_factor: 'float' = 1.0, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `CubicBezier(start_anchor: 'Point3DLike', start_handle: 'Point3DLike', end_handle: 'Point3DLike', end_anchor: 'Point3DLike', **kwargs: 'Any') -> 'None'` ← VMobject
> A cubic Bézier curve.

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, start_anchor: 'Point3DLike', start_handle: 'Point3DLike', end_handle: 'Point3DLike', end_anchor: 'Point3DLike', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `CurvedArrow(start_point: 'Point3DLike', end_point: 'Point3DLike', **kwargs: 'Any') -> 'None'` ← ArcBetweenPoints
> Inherits from Arc and additionally takes 2 points between which the arc is spanned.

<details><summary>métodos próprios (1) · herdados: 261</summary>

- `__init__(self, start_point: 'Point3DLike', end_point: 'Point3DLike', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `CurvedDoubleArrow(start_point: 'Point3DLike', end_point: 'Point3DLike', **kwargs: 'Any') -> 'None'` ← CurvedArrow
> Inherits from Arc and additionally takes 2 points between which the arc is spanned.

<details><summary>métodos próprios (1) · herdados: 261</summary>

- `__init__(self, start_point: 'Point3DLike', end_point: 'Point3DLike', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Cutout(main_shape: 'VMobject', *mobjects: 'VMobject', **kwargs: 'Any') -> 'None'` ← VMobject
> A shape with smaller cutouts.

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, main_shape: 'VMobject', *mobjects: 'VMobject', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `DashedLine(*args: 'Any', dash_length: 'float' = 0.05, dashed_ratio: 'float' = 0.5, **kwargs: 'Any') -> 'None'` ← Line
> A dashed :class:`Line`.

<details><summary>métodos próprios (5) · herdados: 263</summary>

- `__init__(self, *args: 'Any', dash_length: 'float' = 0.05, dashed_ratio: 'float' = 0.5, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `get_end(self) -> 'Point3D'` — Returns the end point of the line.
- `get_first_handle(self) -> 'Point3D'` — Returns the point of the first handle.
- `get_last_handle(self) -> 'Point3D'` — Returns the point of the last handle.
- `get_start(self) -> 'Point3D'` — Returns the start point of the line.

</details>

### `Difference(subject: 'VMobject', clip: 'VMobject', **kwargs: 'Any') -> 'None'` ← _BooleanOps
> Subtracts one :class:`~.VMobject` from another one.

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, subject: 'VMobject', clip: 'VMobject', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Dot(point: 'Point3DLike' = array([0., 0., 0.]), radius: 'float' = 0.08, stroke_width: 'float' = 0, fill_opacity: 'float' = 1.0, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), **kwargs: 'Any') -> 'None'` ← Circle
> A circle with a very small radius.

<details><summary>métodos próprios (1) · herdados: 263</summary>

- `__init__(self, point: 'Point3DLike' = array([0., 0., 0.]), radius: 'float' = 0.08, stroke_width: 'float' = 0, fill_opacity: 'float' = 1.0, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `DoubleArrow(*args: 'Any', **kwargs: 'Any') -> 'None'` ← Arrow
> An arrow with tips on both ends.

<details><summary>métodos próprios (1) · herdados: 269</summary>

- `__init__(self, *args: 'Any', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Elbow(width: 'float' = 0.2, angle: 'float' = 0, **kwargs: 'Any') -> 'None'` ← VMobject
> Two lines that create a right angle about each other: L-shape.

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, width: 'float' = 0.2, angle: 'float' = 0, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Ellipse(width: 'float' = 2, height: 'float' = 1, **kwargs: 'Any') -> 'None'` ← Circle
> A circular shape; oval, circle.

<details><summary>métodos próprios (1) · herdados: 263</summary>

- `__init__(self, width: 'float' = 2, height: 'float' = 1, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Exclusion(subject: 'VMobject', clip: 'VMobject', **kwargs: 'Any') -> 'None'` ← _BooleanOps
> Find the XOR between two :class:`~.VMobject`.

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, subject: 'VMobject', clip: 'VMobject', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Intersection(*vmobjects: 'VMobject', **kwargs: 'Any') -> 'None'` ← _BooleanOps
> Find the intersection of two :class:`~.VMobject` s.

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, *vmobjects: 'VMobject', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Label(label: 'str | ManimTextLabel', label_config: 'dict[str, Any] | None' = None, box_config: 'dict[str, Any] | None' = None, frame_config: 'dict[str, Any] | None' = None, **kwargs: 'Any') -> 'None'` ← VGroup
> A Label consisting of text surrounded by a frame.

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, label: 'str | ManimTextLabel', label_config: 'dict[str, Any] | None' = None, box_config: 'dict[str, Any] | None' = None, frame_config: 'dict[str, Any] | None' = None, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `LabeledArrow(*args: 'Any', **kwargs: 'Any') -> 'None'` ← LabeledLine, Arrow
> Constructs an arrow containing a label box somewhere along its length.

<details><summary>métodos próprios (1) · herdados: 269</summary>

- `__init__(self, *args: 'Any', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `LabeledDot(label: 'str | SingleStringMathTex | Text | Tex', radius: 'float | None' = None, buff: 'float' = 0.1, **kwargs: 'Any') -> 'None'` ← Dot
> A :class:`Dot` containing a label in its center.

<details><summary>métodos próprios (1) · herdados: 263</summary>

- `__init__(self, label: 'str | SingleStringMathTex | Text | Tex', radius: 'float | None' = None, buff: 'float' = 0.1, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `LabeledLine(label: 'str | ManimTextLabel', label_position: 'float' = 0.5, label_config: 'dict[str, Any] | None' = None, box_config: 'dict[str, Any] | None' = None, frame_config: 'dict[str, Any] | None' = None, *args: 'Any', **kwargs: 'Any') -> 'None'` ← Line
> Constructs a line containing a label box somewhere along its length.

<details><summary>métodos próprios (1) · herdados: 267</summary>

- `__init__(self, label: 'str | ManimTextLabel', label_position: 'float' = 0.5, label_config: 'dict[str, Any] | None' = None, box_config: 'dict[str, Any] | None' = None, frame_config: 'dict[str, Any] | None' = None, *args: 'Any', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `LabeledPolygram(*vertex_groups: 'Point3DLike_Array', label: 'str | ManimTextLabel', precision: 'float' = 0.01, label_config: 'dict[str, Any] | None' = None, box_config: 'dict[str, Any] | None' = None, frame_config: 'dict[str, Any] | None' = None, **kwargs: 'Any') -> 'None'` ← Polygram
> Constructs a polygram containing a label box at its pole of inaccessibility.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, *vertex_groups: 'Point3DLike_Array', label: 'str | ManimTextLabel', precision: 'float' = 0.01, label_config: 'dict[str, Any] | None' = None, box_config: 'dict[str, Any] | None' = None, frame_config: 'dict[str, Any] | None' = None, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Line(start: 'Point3DLike | Mobject' = array([-1.,  0.,  0.]), end: 'Point3DLike | Mobject' = array([1., 0., 0.]), buff: 'float' = 0, path_arc: 'float' = 0, **kwargs: 'Any') -> 'None'` ← TipableVMobject
> A straight or curved line segment between two points or mobjects.

<details><summary>métodos próprios (13) · herdados: 255</summary>

- `__init__(self, start: 'Point3DLike | Mobject' = array([-1.,  0.,  0.]), end: 'Point3DLike | Mobject' = array([1., 0., 0.]), buff: 'float' = 0, path_arc: 'float' = 0, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `generate_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `get_angle(self) -> 'float'`
- `get_projection(self, point: 'Point3DLike') -> 'Point3D'` — Returns the projection of a point onto a line.
- `get_slope(self) -> 'float'`
- `get_unit_vector(self) -> 'Vector3D'`
- `get_vector(self) -> 'Vector3D'`
- `init_points(self) -> 'Self'`
- `put_start_and_end_on(self, start: 'Point3DLike', end: 'Point3DLike') -> 'Self'` — Sets starts and end coordinates of a line.
- `set_angle(self, angle: 'float', about_point: 'Point3DLike | None' = None) -> 'Self'`
- `set_length(self, length: 'float') -> 'Self'`
- `set_path_arc(self, new_value: 'float') -> 'Self'`
- `set_points_by_ends(self, start: 'Point3DLike | Mobject', end: 'Point3DLike | Mobject', buff: 'float' = 0, path_arc: 'float' = 0) -> 'Self'` — Sets the points of the line based on its start and end points.

</details>

### `Polygon(*vertices: 'Point3DLike', **kwargs: 'Any') -> 'None'` ← Polygram
> A shape consisting of one closed loop of vertices.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, *vertices: 'Point3DLike', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Polygram(*vertex_groups: 'Point3DLike_Array', color: 'ParsableManimColor' = ManimColor('#58C4DD'), **kwargs: 'Any')` ← VMobject
> A generalized :class:`Polygon`, allowing for disconnected sets of edges.

<details><summary>métodos próprios (4) · herdados: 242</summary>

- `__init__(self, *vertex_groups: 'Point3DLike_Array', color: 'ParsableManimColor' = ManimColor('#58C4DD'), **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_vertex_groups(self) -> 'list[Point3D_Array]'` — Gets the vertex groups of the :class:`Polygram`.
- `get_vertices(self) -> 'Point3D_Array'` — Gets the vertices of the :class:`Polygram`.
- `round_corners(self, radius: 'float | list[float]' = 0.5, evenly_distribute_anchors: 'bool' = False, components_per_rounded_corner: 'int' = 2) -> 'Self'` — Rounds off the corners of the :class:`Polygram`.

</details>

### `Rectangle(color: 'ParsableManimColor' = ManimColor('#FFFFFF'), height: 'float' = 2.0, width: 'float' = 4.0, grid_xstep: 'float | None' = None, grid_ystep: 'float | None' = None, mark_paths_closed: 'bool' = True, close_new_points: 'bool' = True, **kwargs: 'Any')` ← Polygon
> A quadrilateral with two sets of parallel sides.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), height: 'float' = 2.0, width: 'float' = 4.0, grid_xstep: 'float | None' = None, grid_ystep: 'float | None' = None, mark_paths_closed: 'bool' = True, close_new_points: 'bool' = True, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `RegularPolygon(n: 'int' = 6, **kwargs: 'Any') -> 'None'` ← RegularPolygram
> An n-sided regular :class:`Polygon`.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, n: 'int' = 6, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `RegularPolygram(num_vertices: 'int', *, density: 'int' = 2, radius: 'float' = 1, start_angle: 'float | None' = None, **kwargs: 'Any') -> 'None'` ← Polygram
> A :class:`Polygram` with regularly spaced vertices.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, num_vertices: 'int', *, density: 'int' = 2, radius: 'float' = 1, start_angle: 'float | None' = None, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `RightAngle(line1: 'Line', line2: 'Line', length: 'float | None' = None, **kwargs: 'Any') -> 'None'` ← Angle
> An elbow-type mobject representing a right angle between two lines.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, line1: 'Line', line2: 'Line', length: 'float | None' = None, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `RoundedRectangle(corner_radius: 'float | list[float]' = 0.5, **kwargs: 'Any')` ← Rectangle
> A rectangle with rounded corners.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, corner_radius: 'float | list[float]' = 0.5, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Sector(radius: 'float' = 1, **kwargs: 'Any') -> 'None'` ← AnnularSector
> A sector of a circle.

<details><summary>métodos próprios (1) · herdados: 261</summary>

- `__init__(self, radius: 'float' = 1, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Square(side_length: 'float' = 2.0, **kwargs: 'Any') -> 'None'` ← Rectangle
> A rectangle with equal side lengths.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, side_length: 'float' = 2.0, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Star(n: 'int' = 5, *, outer_radius: 'float' = 1, inner_radius: 'float | None' = None, density: 'int' = 2, start_angle: 'float | None' = 1.5707963267948966, **kwargs: 'Any') -> 'None'` ← Polygon
> A regular polygram without the intersecting lines.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, n: 'int' = 5, *, outer_radius: 'float' = 1, inner_radius: 'float | None' = None, density: 'int' = 2, start_angle: 'float | None' = 1.5707963267948966, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `StealthTip(fill_opacity: 'float' = 1, stroke_width: 'float' = 3, length: 'float' = 0.175, start_angle: 'float' = 3.141592653589793, **kwargs: 'Any')` ← ArrowTip
> 'Stealth' fighter / kite arrow shape.

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, fill_opacity: 'float' = 1, stroke_width: 'float' = 3, length: 'float' = 0.175, start_angle: 'float' = 3.141592653589793, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `SurroundingRectangle(*mobjects: 'Mobject', color: 'ParsableManimColor' = ManimColor('#FFFF00'), buff: 'float | tuple[float, float]' = 0.1, corner_radius: 'float' = 0.0, **kwargs: 'Any') -> 'None'` ← RoundedRectangle
> A rectangle surrounding a :class:`~.Mobject`

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, *mobjects: 'Mobject', color: 'ParsableManimColor' = ManimColor('#FFFF00'), buff: 'float | tuple[float, float]' = 0.1, corner_radius: 'float' = 0.0, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `TangentLine(vmob: 'VMobject', alpha: 'float', length: 'float' = 1, d_alpha: 'float' = 1e-06, **kwargs: 'Any') -> 'None'` ← Line
> Constructs a line tangent to a :class:`~.VMobject` at a specific point.

<details><summary>métodos próprios (1) · herdados: 267</summary>

- `__init__(self, vmob: 'VMobject', alpha: 'float', length: 'float' = 1, d_alpha: 'float' = 1e-06, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `TangentialArc(line1: 'Line', line2: 'Line', radius: 'float', corner: 'Any' = (1, 1), **kwargs: 'Any')` ← ArcBetweenPoints
> Construct an arc that is tangent to two intersecting lines.

<details><summary>métodos próprios (1) · herdados: 261</summary>

- `__init__(self, line1: 'Line', line2: 'Line', radius: 'float', corner: 'Any' = (1, 1), **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `TipableVMobject(tip_length: 'float' = 0.35, normal_vector: 'Vector3DLike' = array([0., 0., 1.]), tip_style: 'dict | None' = None, **kwargs: 'Any') -> 'None'` ← VMobject
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (18) · herdados: 240</summary>

- `__init__(self, tip_length: 'float' = 0.35, normal_vector: 'Vector3DLike' = array([0., 0., 1.]), tip_style: 'dict | None' = None, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `add_tip(self, tip: 'tips.ArrowTip | None' = None, tip_shape: 'type[tips.ArrowTip] | None' = None, tip_length: 'float | None' = None, tip_width: 'float | None' = None, at_start: 'bool' = False) -> 'Self'` — Adds a tip to the TipableVMobject instance, recognising
- `assign_tip_attr(self, tip: 'tips.ArrowTip', at_start: 'bool') -> 'Self'`
- `create_tip(self, tip_shape: 'type[tips.ArrowTip] | None' = None, tip_length: 'float | None' = None, tip_width: 'float | None' = None, at_start: 'bool' = False) -> 'tips.ArrowTip'` — Stylises the tip, positions it spatially, and returns
- `get_default_tip_length(self) -> 'float'`
- `get_end(self) -> 'Point3D'` — Returns the point, where the stroke that surrounds the :class:`~.Mobject` ends.
- `get_first_handle(self) -> 'Point3D'`
- `get_last_handle(self) -> 'Point3D'`
- `get_length(self) -> 'float'`
- `get_start(self) -> 'Point3D'` — Returns the point, where the stroke that surrounds the :class:`~.Mobject` starts.
- `get_tip(self) -> 'VMobject'` — Returns the TipableVMobject instance's (first) tip,
- `get_tips(self) -> 'VGroup'` — Returns a VGroup (collection of VMobjects) containing
- `get_unpositioned_tip(self, tip_shape: 'type[tips.ArrowTip] | None' = None, tip_length: 'float | None' = None, tip_width: 'float | None' = None) -> 'tips.ArrowTip | tips.ArrowTriangleFilledTip'` — Returns a tip that has been stylistically configured,
- `has_start_tip(self) -> 'bool'`
- `has_tip(self) -> 'bool'`
- `pop_tips(self) -> 'VGroup'`
- `position_tip(self, tip: 'tips.ArrowTip', at_start: 'bool' = False) -> 'tips.ArrowTip'`
- `reset_endpoints_based_on_tip(self, tip: 'tips.ArrowTip', at_start: 'bool') -> 'Self'`

</details>

### `Triangle(**kwargs: 'Any') -> 'None'` ← RegularPolygon
> An equilateral triangle.

<details><summary>métodos próprios (1) · herdados: 245</summary>

- `__init__(self, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Underline(mobject: 'Mobject', buff: 'float' = 0.1, **kwargs: 'Any') -> 'None'` ← Line
> Creates an underline.

<details><summary>métodos próprios (1) · herdados: 267</summary>

- `__init__(self, mobject: 'Mobject', buff: 'float' = 0.1, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Union(*vmobjects: 'VMobject', **kwargs: 'Any') -> 'None'` ← _BooleanOps
> Union of two or more :class:`~.VMobject` s. This returns the common region of

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, *vmobjects: 'VMobject', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Vector(direction: 'Vector2DLike | Vector3DLike' = array([1., 0., 0.]), buff: 'float' = 0, **kwargs: 'Any') -> 'None'` ← Arrow
> A vector specialized for use in graphs.

<details><summary>métodos próprios (2) · herdados: 269</summary>

- `__init__(self, direction: 'Vector2DLike | Vector3DLike' = array([1., 0., 0.]), buff: 'float' = 0, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `coordinate_label(self, integer_labels: 'bool' = True, n_dim: 'int' = 2, color: 'ParsableManimColor | None' = None, **kwargs: 'Any') -> 'Matrix'` — Creates a label based on the coordinates of the vector.

</details>

- `BLACK` = `ManimColor('#000000')`
- `BLACK` = `ManimColor('#000000')`
- `BLUE` = `ManimColor('#58C4DD')`
- `BLUE` = `ManimColor('#58C4DD')`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
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
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PURE_YELLOW` = `ManimColor('#FFFF00')`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `RED` = `ManimColor('#FC6255')`
- `RED` = `ManimColor('#FC6255')`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `START_X` = `30`
- `START_X` = `30`
- `START_X` = `30`
- `START_X` = `30`
- `START_X` = `30`
- `START_Y` = `20`
- `START_Y` = `20`
- `START_Y` = `20`
- `START_Y` = `20`
- `START_Y` = `20`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
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
- `UL` = `array([-1.,  1.,  0.])`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`

## mobject/graph

### `DiGraph(vertices: 'Sequence[Hashable]', edges: 'Sequence[tuple[Hashable, Hashable]]', labels: 'bool | dict' = False, label_fill_color: 'str' = ManimColor('#000000'), layout: 'LayoutName | dict[Hashable, Point3DLike] | LayoutFunction' = 'spring', layout_scale: 'float | tuple[float, float, float]' = 2, layout_config: 'dict | None' = None, vertex_type: 'type[Mobject]' = <class 'manim.mobject.geometry.arc.Dot'>, vertex_config: 'dict | None' = None, vertex_mobjects: 'dict | None' = None, edge_type: 'type[Mobject]' = <class 'manim.mobject.geometry.line.Line'>, partitions: 'Sequence[Sequence[Hashable]] | None' = None, root_vertex: 'Hashable | None' = None, edge_config: 'dict | None' = None) -> 'None'` ← GenericGraph
> A directed graph.

<details><summary>métodos próprios (1) · herdados: 249</summary>

- `update_edges(self, graph) -> 'Self'` — Updates the edges to stick at their corresponding vertices.

</details>

### `GenericGraph(vertices: 'Sequence[Hashable]', edges: 'Sequence[tuple[Hashable, Hashable]]', labels: 'bool | dict' = False, label_fill_color: 'str' = ManimColor('#000000'), layout: 'LayoutName | dict[Hashable, Point3DLike] | LayoutFunction' = 'spring', layout_scale: 'float | tuple[float, float, float]' = 2, layout_config: 'dict | None' = None, vertex_type: 'type[Mobject]' = <class 'manim.mobject.geometry.arc.Dot'>, vertex_config: 'dict | None' = None, vertex_mobjects: 'dict | None' = None, edge_type: 'type[Mobject]' = <class 'manim.mobject.geometry.line.Line'>, partitions: 'Sequence[Sequence[Hashable]] | None' = None, root_vertex: 'Hashable | None' = None, edge_config: 'dict | None' = None) -> 'None'` ← VMobject
> Abstract base class for graphs (that is, a collection of vertices

<details><summary>métodos próprios (7) · herdados: 242</summary>

- `__init__(self, vertices: 'Sequence[Hashable]', edges: 'Sequence[tuple[Hashable, Hashable]]', labels: 'bool | dict' = False, label_fill_color: 'str' = ManimColor('#000000'), layout: 'LayoutName | dict[Hashable, Point3DLike] | LayoutFunction' = 'spring', layout_scale: 'float | tuple[float, float, float]' = 2, layout_config: 'dict | None' = None, vertex_type: 'type[Mobject]' = <class 'manim.mobject.geometry.arc.Dot'>, vertex_config: 'dict | None' = None, vertex_mobjects: 'dict | None' = None, edge_type: 'type[Mobject]' = <class 'manim.mobject.geometry.line.Line'>, partitions: 'Sequence[Sequence[Hashable]] | None' = None, root_vertex: 'Hashable | None' = None, edge_config: 'dict | None' = None) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `add_edges(self, *edges: 'tuple[Hashable, Hashable]', edge_type: 'type[Mobject]' = <class 'manim.mobject.geometry.line.Line'>, edge_config: 'dict | None' = None, **kwargs)` — Add new edges to the graph.
- `add_vertices(self: 'Graph', *vertices: 'Hashable', positions: 'dict | None' = None, labels: 'bool' = False, label_fill_color: 'str' = ManimColor('#000000'), vertex_type: 'type[Mobject]' = <class 'manim.mobject.geometry.arc.Dot'>, vertex_config: 'dict | None' = None, vertex_mobjects: 'dict | None' = None)` — Add a list of vertices to the graph.
- `change_layout(self, layout: 'LayoutName | dict[Hashable, Point3DLike] | LayoutFunction' = 'spring', layout_scale: 'float | tuple[float, float, float]' = 2, layout_config: 'dict[str, Any] | None' = None, partitions: 'list[list[Hashable]] | None' = None, root_vertex: 'Hashable | None' = None) -> 'Graph'` — Change the layout of this graph.
- `from_networkx(nxgraph: 'nx.classes.graph.Graph | nx.classes.digraph.DiGraph', **kwargs)` — Build a :class:`~.Graph` or :class:`~.DiGraph` from a
- `remove_edges(self, *edges: 'tuple[Hashable]') -> 'VGroup'` — Remove several edges from the graph.
- `remove_vertices(self, *vertices)` — Remove several vertices from the graph.

</details>

### `Graph(vertices: 'Sequence[Hashable]', edges: 'Sequence[tuple[Hashable, Hashable]]', labels: 'bool | dict' = False, label_fill_color: 'str' = ManimColor('#000000'), layout: 'LayoutName | dict[Hashable, Point3DLike] | LayoutFunction' = 'spring', layout_scale: 'float | tuple[float, float, float]' = 2, layout_config: 'dict | None' = None, vertex_type: 'type[Mobject]' = <class 'manim.mobject.geometry.arc.Dot'>, vertex_config: 'dict | None' = None, vertex_mobjects: 'dict | None' = None, edge_type: 'type[Mobject]' = <class 'manim.mobject.geometry.line.Line'>, partitions: 'Sequence[Sequence[Hashable]] | None' = None, root_vertex: 'Hashable | None' = None, edge_config: 'dict | None' = None) -> 'None'` ← GenericGraph
> An undirected graph (vertices connected with edges).

<details><summary>métodos próprios (1) · herdados: 249</summary>

- `update_edges(self, graph) -> 'Self'`

</details>

### `LayoutFunction(*args, **kwargs)` ← Protocol
> A protocol for automatic layout functions that compute a layout for a graph to be used in :meth:`~.Graph.change_layout`.

<details><summary>métodos próprios (2) · herdados: 0</summary>

- `__call__(self, graph: 'NxGraph', scale: 'float | tuple[float, float, float]' = 2, *args: 'Any', **kwargs: 'Any') -> 'dict[Hashable, Point3D]'` — Given a graph and a scale, return a dictionary of coordinates.
- `__init__(self, *args, **kwargs)`

</details>

- `BLACK` = `ManimColor('#000000')`
- `TYPE_CHECKING` = `False`

## mobject/graphing

### `Axes(x_range: 'Sequence[float] | None' = None, y_range: 'Sequence[float] | None' = None, x_length: 'float | None' = 12, y_length: 'float | None' = 6, axis_config: 'dict | None' = None, x_axis_config: 'dict | None' = None, y_axis_config: 'dict | None' = None, tips: 'bool' = True, **kwargs: 'Any')` ← VGroup, CoordinateSystem
> Creates a set of axes.

<details><summary>métodos próprios (6) · herdados: 281</summary>

- `__init__(self, x_range: 'Sequence[float] | None' = None, y_range: 'Sequence[float] | None' = None, x_length: 'float | None' = 12, y_length: 'float | None' = 6, axis_config: 'dict | None' = None, x_axis_config: 'dict | None' = None, y_axis_config: 'dict | None' = None, tips: 'bool' = True, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `coords_to_point(self, *coords: 'float | Sequence[float] | Sequence[Sequence[float]] | np.ndarray') -> 'np.ndarray'` — Accepts coordinates from the axes and returns a point with respect to the scene.
- `get_axes(self) -> 'VGroup'` — Gets the axes.
- `get_axis_labels(self, x_label: 'float | str | Mobject' = 'x', y_label: 'float | str | Mobject' = 'y') -> 'VGroup'` — Defines labels for the x-axis and y-axis of the graph.
- `plot_line_graph(self, x_values: 'Iterable[float]', y_values: 'Iterable[float]', z_values: 'Iterable[float] | None' = None, line_color: 'ParsableManimColor' = ManimColor('#FFFF00'), add_vertex_dots: 'bool' = True, vertex_dot_radius: 'float' = 0.08, vertex_dot_style: 'dict[str, Any] | None' = None, **kwargs: 'Any') -> 'VDict'` — Draws a line graph.
- `point_to_coords(self, point: 'Sequence[float]') -> 'np.ndarray'` — Accepts a point from the scene and returns its coordinates with respect to the axes.

</details>

### `BarChart(values: 'MutableSequence[float]', bar_names: 'Sequence[str] | None' = None, y_range: 'Sequence[float] | None' = None, x_length: 'float | None' = None, y_length: 'float | None' = None, bar_colors: 'Iterable[str]' = ['#003f5c', '#58508d', '#bc5090', '#ff6361', '#ffa600'], bar_width: 'float' = 0.6, bar_fill_opacity: 'float' = 0.7, bar_stroke_width: 'float' = 3, **kwargs: 'Any')` ← Axes
> Creates a bar chart. Inherits from :class:`~.Axes`, so it shares its methods

<details><summary>métodos próprios (3) · herdados: 286</summary>

- `__init__(self, values: 'MutableSequence[float]', bar_names: 'Sequence[str] | None' = None, y_range: 'Sequence[float] | None' = None, x_length: 'float | None' = None, y_length: 'float | None' = None, bar_colors: 'Iterable[str]' = ['#003f5c', '#58508d', '#bc5090', '#ff6361', '#ffa600'], bar_width: 'float' = 0.6, bar_fill_opacity: 'float' = 0.7, bar_stroke_width: 'float' = 3, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `change_bar_values(self, values: 'Iterable[float]', update_colors: 'bool' = True) -> 'Self'` — Updates the height of the bars of the chart.
- `get_bar_labels(self, color: 'ParsableManimColor | None' = None, font_size: 'float' = 24, buff: 'float' = 0.25, label_constructor: 'type[MathTex]' = <class 'manim.mobject.text.tex_mobject.Tex'>) -> 'VGroup'` — Annotates each bar with its corresponding value. Use ``self.bar_labels`` to access the

</details>

### `ComplexPlane(**kwargs: 'Any')` ← NumberPlane
> A :class:`~.NumberPlane` specialized for use with complex numbers.

<details><summary>métodos próprios (7) · herdados: 287</summary>

- `__init__(self, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `add_coordinates(self, *numbers: 'Iterable[float | complex]', **kwargs: 'Any') -> 'Self'` — Adds the labels produced from :meth:`~.NumberPlane.get_coordinate_labels` to the plane.
- `get_coordinate_labels(self, *numbers: 'Iterable[float | complex]', **kwargs: 'Any') -> 'VGroup'` — Generates the :class:`~.DecimalNumber` mobjects for the coordinates of the plane.
- `n2p(self, number: 'float | complex') -> 'np.ndarray'` — Abbreviation for :meth:`number_to_point`.
- `number_to_point(self, number: 'float | complex') -> 'np.ndarray'` — Accepts a float/complex number and returns the equivalent point on the plane.
- `p2n(self, point: 'Point3DLike') -> 'complex'` — Abbreviation for :meth:`point_to_number`.
- `point_to_number(self, point: 'Point3DLike') -> 'complex'` — Accepts a point and returns a complex number equivalent to that point on the plane.

</details>

### `CoordinateSystem(x_range: 'Sequence[float] | None' = None, y_range: 'Sequence[float] | None' = None, x_length: 'float | None' = None, y_length: 'float | None' = None, dimension: 'int' = 2)`
> Abstract base class for Axes and NumberPlane.

<details><summary>métodos próprios (44) · herdados: 0</summary>

- `__init__(self, x_range: 'Sequence[float] | None' = None, y_range: 'Sequence[float] | None' = None, x_length: 'float | None' = None, y_length: 'float | None' = None, dimension: 'int' = 2)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_coordinates(self, *axes_numbers: 'Iterable[float] | None | dict[float, str | float | Mobject]', **kwargs: 'Any') -> 'Self'` — Adds labels to the axes. Use ``Axes.coordinate_labels`` to
- `angle_of_tangent(self, x: 'float', graph: 'ParametricFunction', dx: 'float' = 1e-08) -> 'float'` — Returns the angle to the x-axis of the tangent
- `c2p(self, *coords: 'float | Sequence[float] | Sequence[Sequence[float]] | np.ndarray') -> 'np.ndarray'` — Abbreviation for :meth:`coords_to_point`
- `coords_to_point(self, *coords: 'ManimFloat') -> 'Point3D'`
- `get_T_label(self, x_val: 'float', graph: 'ParametricFunction', label: 'float | str | Mobject | None' = None, label_color: 'ParsableManimColor | None' = None, triangle_size: 'float' = 0.25, triangle_color: 'ParsableManimColor | None' = ManimColor('#FFFFFF'), line_func: 'type[Line]' = <class 'manim.mobject.geometry.line.Line'>, line_color: 'ParsableManimColor' = ManimColor('#FFFF00')) -> 'VGroup'` — Creates a labelled triangle marker with a vertical line from the x-axis
- `get_area(self, graph: 'ParametricFunction', x_range: 'tuple[float, float] | None' = None, color: 'ParsableManimColor | Iterable[ParsableManimColor]' = (ManimColor('#58C4DD'), ManimColor('#83C167')), opacity: 'float' = 0.3, bounded_graph: 'ParametricFunction | None' = None, **kwargs: 'Any') -> 'Polygon'` — Returns a :class:`~.Polygon` representing the area under the graph passed.
- `get_axes(self) -> 'VGroup'`
- `get_axis(self, index: 'int') -> 'NumberLine'`
- `get_axis_labels(self) -> 'VGroup'`
- `get_graph_label(self, graph: 'ParametricFunction', label: 'float | str | VMobject' = 'f(x)', x_val: 'float | None' = None, direction: 'Sequence[float]' = array([1., 0., 0.]), buff: 'float' = 0.25, color: 'ParsableManimColor | None' = None, dot: 'bool' = False, dot_config: 'dict[str, Any] | None' = None) -> 'Mobject'` — Creates a properly positioned label for the passed graph, with an optional dot.
- `get_horizontal_line(self, point: 'Point3DLike', **kwargs: 'Any') -> 'Line'` — A horizontal line from the y-axis to a given point in the scene.
- `get_line_from_axis_to_point(self, index, point, line_func=<class 'manim.mobject.geometry.line.DashedLine'>, line_config=None, color=None, stroke_width=2)` — Returns a straight line from a given axis to a point in the scene.
- `get_lines_to_point(self, point: 'Point3DLike', **kwargs: 'Any') -> 'VGroup'` — Generate both horizontal and vertical lines from the axis to a point.
- `get_origin(self) -> 'Point3D'` — Gets the origin of :class:`~.Axes`.
- `get_riemann_rectangles(self, graph: 'ParametricFunction', x_range: 'Sequence[float] | None' = None, dx: 'float' = 0.1, input_sample_type: 'str' = 'left', stroke_width: 'float' = 1, stroke_color: 'ParsableManimColor' = ManimColor('#000000'), fill_opacity: 'float' = 1, color: 'Iterable[ParsableManimColor] | ParsableManimColor' = (ManimColor('#58C4DD'), ManimColor('#83C167')), show_signed_area: 'bool' = True, bounded_graph: 'ParametricFunction | None' = None, blend: 'bool' = False, width_scale_factor: 'float' = 1.001) -> 'VGroup'` — Generates a :class:`~.VGroup` of the Riemann Rectangles for a given curve.
- `get_secant_slope_group(self, x: 'float', graph: 'ParametricFunction', dx: 'float | None' = None, dx_line_color: 'ParsableManimColor' = ManimColor('#FFFF00'), dy_line_color: 'ParsableManimColor | None' = None, dx_label: 'float | str | None' = None, dy_label: 'float | str | None' = None, include_secant_line: 'bool' = True, secant_line_color: 'ParsableManimColor' = ManimColor('#83C167'), secant_line_length: 'float' = 10) -> 'VGroup'` — Creates two lines representing `dx` and `df`, the labels for `dx` and `df`, and
- `get_vertical_line(self, point: 'Point3DLike', **kwargs: 'Any') -> 'Line'` — A vertical line from the x-axis to a given point in the scene.
- `get_vertical_lines_to_graph(self, graph: 'ParametricFunction', x_range: 'Sequence[float] | None' = None, num_lines: 'int' = 20, **kwargs: 'Any') -> 'VGroup'` — Obtains multiple lines from the x-axis to the curve.
- `get_x_axis(self) -> 'NumberLine'`
- `get_x_axis_label(self, label: 'float | str | VMobject', edge: 'Vector3D' = array([1., 1., 0.]), direction: 'Vector3D' = array([1., 1., 0.]), buff: 'float' = 0.1, **kwargs: 'Any') -> 'Mobject'` — Generate an x-axis label.
- `get_x_unit_size(self) -> 'float'`
- `get_y_axis(self) -> 'NumberLine'`
- `get_y_axis_label(self, label: 'float | str | VMobject', edge: 'Vector3D' = array([1., 1., 0.]), direction: 'Vector3D' = array([1. , 0.5, 0. ]), buff: 'float' = 0.1, **kwargs: 'Any') -> 'Mobject'` — Generate a y-axis label.
- `get_y_unit_size(self) -> 'float'`
- `get_z_axis(self) -> 'NumberLine'`
- `i2gc(self, x: 'float', graph: 'ParametricFunction') -> 'tuple[float, float]'` — Alias for :meth:`input_to_graph_coords`.
- `i2gp(self, x: 'float', graph: 'ParametricFunction') -> 'np.ndarray'` — Alias for :meth:`input_to_graph_point`.
- `input_to_graph_coords(self, x: 'float', graph: 'ParametricFunction') -> 'tuple[float, float]'` — Returns a tuple of the axis relative coordinates of the point
- `input_to_graph_point(self, x: 'float', graph: 'ParametricFunction | VMobject') -> 'Point3D'` — Returns the coordinates of the point on a ``graph`` corresponding to an ``x`` value.
- `p2c(self, point: 'Point3DLike') -> 'list[ManimFloat]'` — Abbreviation for :meth:`point_to_coords`
- `plot(self, function: 'Callable[[float], float]', x_range: 'Sequence[float] | None' = None, use_vectorized: 'bool' = False, colorscale: 'Iterable[ParsableManimColor] | Iterable[ParsableManimColor, float] | None' = None, colorscale_axis: 'int' = 1, **kwargs: 'Any') -> 'ParametricFunction'` — Generates a curve based on a function.
- `plot_antiderivative_graph(self, graph: 'ParametricFunction', y_intercept: 'float' = 0, samples: 'int' = 50, use_vectorized: 'bool' = False, **kwargs: 'Any') -> 'ParametricFunction'` — Plots an antiderivative graph.
- `plot_derivative_graph(self, graph: 'ParametricFunction', color: 'ParsableManimColor' = ManimColor('#83C167'), **kwargs: 'Any') -> 'ParametricFunction'` — Returns the curve of the derivative of the passed graph.
- `plot_implicit_curve(self, func: 'Callable[[float, float], float]', min_depth: 'int' = 5, max_quads: 'int' = 1500, **kwargs: 'Any') -> 'ImplicitFunction'` — Creates the curves of an implicit function.
- `plot_parametric_curve(self, function: 'Callable[[float], np.ndarray]', use_vectorized: 'bool' = False, **kwargs: 'Any') -> 'ParametricFunction'` — A parametric curve.
- `plot_polar_graph(self, r_func: 'Callable[[float], float]', theta_range: 'Sequence[float] | None' = None, **kwargs: 'Any') -> 'ParametricFunction'` — A polar graph.
- `plot_surface(self, function: 'Callable[[float], float]', u_range: 'Sequence[float] | None' = None, v_range: 'Sequence[float] | None' = None, colorscale: 'Sequence[ParsableManimColor] | Sequence[tuple[ParsableManimColor, float]] | None' = None, colorscale_axis: 'int' = 2, **kwargs: 'Any') -> 'Surface | OpenGLSurface'` — Generates a surface based on a function.
- `point_to_coords(self, point: 'Point3DLike') -> 'list[ManimFloat]'`
- `point_to_polar(self, point: 'Point2DLike') -> 'Point2D'` — Gets polar coordinates from a point.
- `polar_to_point(self, radius: 'float', azimuth: 'float') -> 'Point2D'` — Gets a point from polar coordinates.
- `pr2pt(self, radius: 'float', azimuth: 'float') -> 'np.ndarray'` — Abbreviation for :meth:`polar_to_point`
- `pt2pr(self, point: 'np.ndarray') -> 'Point2D'` — Abbreviation for :meth:`point_to_polar`
- `slope_of_tangent(self, x: 'float', graph: 'ParametricFunction', **kwargs: 'Any') -> 'float'` — Returns the slope of the tangent to the plotted curve

</details>

### `FunctionGraph(function: 'Callable[[float], Any]', x_range: 'tuple[float, float] | tuple[float, float, float] | None' = None, color: 'ParsableManimColor' = ManimColor('#FFFF00'), **kwargs: 'Any') -> 'None'` ← ParametricFunction
> A :class:`ParametricFunction` that spans the length of the scene by default.

<details><summary>métodos próprios (3) · herdados: 243</summary>

- `__init__(self, function: 'Callable[[float], Any]', x_range: 'tuple[float, float] | tuple[float, float, float] | None' = None, color: 'ParsableManimColor' = ManimColor('#FFFF00'), **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `get_function(self) -> 'Callable[[float], Any]'`
- `get_point_from_function(self, x: 'float') -> 'Point3D'`

</details>

### `ImplicitFunction(func: 'Callable[[float, float], float]', x_range: 'Sequence[float] | None' = None, y_range: 'Sequence[float] | None' = None, min_depth: 'int' = 5, max_quads: 'int' = 1500, use_smoothing: 'bool' = True, **kwargs: 'Any')` ← VMobject
> A vectorized mobject.

<details><summary>métodos próprios (3) · herdados: 241</summary>

- `__init__(self, func: 'Callable[[float, float], float]', x_range: 'Sequence[float] | None' = None, y_range: 'Sequence[float] | None' = None, min_depth: 'int' = 5, max_quads: 'int' = 1500, use_smoothing: 'bool' = True, **kwargs: 'Any')` — An implicit function.
- `generate_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `init_points(self) -> 'Self'`

</details>

### `LinearBase(scale_factor: 'float' = 1.0)` ← _ScaleBase
> Scale baseclass for graphing/functions.

<details><summary>métodos próprios (3) · herdados: 1</summary>

- `__init__(self, scale_factor: 'float' = 1.0)` — The default scaling class.
- `function(self, value: 'float') -> 'float'` — Multiplies the value by the scale factor.
- `inverse_function(self, value: 'float') -> 'float'` — Inverse of function. Divides the value by the scale factor.

</details>

### `LogBase(base: 'float' = 10, custom_labels: 'bool' = True)` ← _ScaleBase
> Scale baseclass for graphing/functions.

<details><summary>métodos próprios (4) · herdados: 0</summary>

- `__init__(self, base: 'float' = 10, custom_labels: 'bool' = True)` — Scale for logarithmic graphs/functions.
- `function(self, value: 'float') -> 'float'` — Scales the value to fit it to a logarithmic scale.``self.function(5)==10**5``
- `get_custom_labels(self, val_range: 'Iterable[float]', unit_decimal_places: 'int' = 0, **base_config: 'Any') -> 'list[Integer]'` — Produces custom :class:`~.Integer` labels in the form of ``10^2``.
- `inverse_function(self, value: 'float') -> 'float'` — Inverse of ``function``. The value must be greater than 0

</details>

### `NumberLine(x_range: 'Sequence[float] | None' = None, length: 'float | None' = None, unit_size: 'float' = 1, include_ticks: 'bool' = True, tick_size: 'float' = 0.1, numbers_with_elongated_ticks: 'Iterable[float] | None' = None, longer_tick_multiple: 'int' = 2, exclude_origin_tick: 'bool' = False, rotation: 'float' = 0, stroke_width: 'float' = 2.0, include_tip: 'bool' = False, tip_width: 'float' = 0.35, tip_height: 'float' = 0.35, tip_shape: 'type[ArrowTip] | None' = None, include_numbers: 'bool' = False, font_size: 'float' = 36, label_direction: 'Point3DLike' = array([ 0., -1.,  0.]), label_constructor: 'type[ManimTextLabel]' = <class 'manim.mobject.text.tex_mobject.MathTex'>, scaling: '_ScaleBase' = <manim.mobject.graphing.scale.LinearBase object at 0x713b83560ec0>, line_to_number_buff: 'float' = 0.25, decimal_number_config: 'dict | None' = None, numbers_to_exclude: 'Iterable[float] | None' = None, numbers_to_include: 'Iterable[float] | None' = None, **kwargs: 'Any')` ← Line
> Creates a number line with tick marks.

<details><summary>métodos próprios (18) · herdados: 266</summary>

- `__init__(self, x_range: 'Sequence[float] | None' = None, length: 'float | None' = None, unit_size: 'float' = 1, include_ticks: 'bool' = True, tick_size: 'float' = 0.1, numbers_with_elongated_ticks: 'Iterable[float] | None' = None, longer_tick_multiple: 'int' = 2, exclude_origin_tick: 'bool' = False, rotation: 'float' = 0, stroke_width: 'float' = 2.0, include_tip: 'bool' = False, tip_width: 'float' = 0.35, tip_height: 'float' = 0.35, tip_shape: 'type[ArrowTip] | None' = None, include_numbers: 'bool' = False, font_size: 'float' = 36, label_direction: 'Point3DLike' = array([ 0., -1.,  0.]), label_constructor: 'type[ManimTextLabel]' = <class 'manim.mobject.text.tex_mobject.MathTex'>, scaling: '_ScaleBase' = <manim.mobject.graphing.scale.LinearBase object at 0x713b83560ec0>, line_to_number_buff: 'float' = 0.25, decimal_number_config: 'dict | None' = None, numbers_to_exclude: 'Iterable[float] | None' = None, numbers_to_include: 'Iterable[float] | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `add_labels(self, dict_values: 'dict[float, str | float | VMobject]', direction: 'Point3DLike | None' = None, buff: 'float | None' = None, font_size: 'float | None' = None, label_constructor: 'type[ManimTextLabel] | None' = None) -> 'Self'` — Adds specifically positioned labels to the :class:`~.NumberLine` using a ``dict``.
- `add_numbers(self, x_values: 'Iterable[float] | None' = None, excluding: 'Iterable[float] | None' = None, font_size: 'float | None' = None, label_constructor: 'type[SingleStringMathTex] | None' = None, **kwargs: 'Any') -> 'Self'` — Adds :class:`~.DecimalNumber` mobjects representing their position
- `add_ticks(self) -> 'Self'` — Adds ticks to the number line. Ticks can be accessed after creation
- `get_labels(self) -> 'VGroup'`
- `get_number_mobject(self, x: 'float', direction: 'Vector3D | None' = None, buff: 'float | None' = None, font_size: 'float | None' = None, label_constructor: 'type[SingleStringMathTex] | None' = None, **number_config: 'dict[str, Any]') -> 'VMobject'` — Generates a positioned :class:`~.DecimalNumber` mobject
- `get_number_mobjects(self, *numbers: 'float', **kwargs: 'Any') -> 'VGroup'`
- `get_tick(self, x: 'float', size: 'float | None' = None) -> 'Line'` — Generates a tick and positions it along the number line.
- `get_tick_marks(self) -> 'VGroup'`
- `get_tick_range(self) -> 'np.ndarray'` — Generates the range of values on which labels are plotted based on the
- `get_unit_size(self) -> 'float'`
- `get_unit_vector(self) -> 'Vector3D'`
- `n2p(self, number: 'float | np.ndarray') -> 'Point3D'` — Abbreviation for :meth:`~.NumberLine.number_to_point`.
- `number_to_point(self, number: 'float | np.ndarray') -> 'np.ndarray'` — Accepts a value along the number line and returns a point with
- `p2n(self, point: 'Point3DLike') -> 'float'` — Abbreviation for :meth:`~.NumberLine.point_to_number`.
- `point_to_number(self, point: 'Sequence[float]') -> 'float'` — Accepts a point with respect to the scene and returns
- `rotate_about_number(self, number: 'float', angle: 'float', axis: 'Vector3D' = array([0., 0., 1.]), **kwargs: 'Any') -> 'Self'`
- `rotate_about_zero(self, angle: 'float', axis: 'Vector3D' = array([0., 0., 1.]), **kwargs: 'Any') -> 'Self'`

</details>

### `NumberPlane(x_range: 'Sequence[float] | None' = (-7.111111111111111, 7.111111111111111, 1), y_range: 'Sequence[float] | None' = (-4.0, 4.0, 1), x_length: 'float | None' = None, y_length: 'float | None' = None, background_line_style: 'dict[str, Any] | None' = None, faded_line_style: 'dict[str, Any] | None' = None, faded_line_ratio: 'int' = 1, make_smooth_after_applying_functions: 'bool' = True, **kwargs: 'dict[str, Any]')` ← Axes
> Creates a cartesian plane with background lines.

<details><summary>métodos próprios (3) · herdados: 286</summary>

- `__init__(self, x_range: 'Sequence[float] | None' = (-7.111111111111111, 7.111111111111111, 1), y_range: 'Sequence[float] | None' = (-4.0, 4.0, 1), x_length: 'float | None' = None, y_length: 'float | None' = None, background_line_style: 'dict[str, Any] | None' = None, faded_line_style: 'dict[str, Any] | None' = None, faded_line_ratio: 'int' = 1, make_smooth_after_applying_functions: 'bool' = True, **kwargs: 'dict[str, Any]')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_vector(self, coords: 'Sequence[ManimFloat]', **kwargs: 'Any') -> 'Arrow'`
- `prepare_for_nonlinear_transform(self, num_inserted_curves: 'int' = 50) -> 'Self'`

</details>

### `ParametricFunction(function: 'Callable[[float], Point3DLike]', t_range: 'tuple[float, float] | tuple[float, float, float]' = (0, 1), scaling: '_ScaleBase' = <manim.mobject.graphing.scale.LinearBase object at 0x713b8308a240>, dt: 'float' = 1e-08, discontinuities: 'Iterable[float] | None' = None, use_smoothing: 'bool' = True, use_vectorized: 'bool' = False, **kwargs: 'Any')` ← VMobject
> A parametric curve.

<details><summary>métodos próprios (5) · herdados: 241</summary>

- `__init__(self, function: 'Callable[[float], Point3DLike]', t_range: 'tuple[float, float] | tuple[float, float, float]' = (0, 1), scaling: '_ScaleBase' = <manim.mobject.graphing.scale.LinearBase object at 0x713b8308a240>, dt: 'float' = 1e-08, discontinuities: 'Iterable[float] | None' = None, use_smoothing: 'bool' = True, use_vectorized: 'bool' = False, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `generate_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `get_function(self) -> 'Callable[[float], Point3D]'`
- `get_point_from_function(self, t: 'float') -> 'Point3D'`
- `init_points(self) -> 'Self'`

</details>

### `PolarPlane(radius_max: 'float' = 4.0, size: 'float | None' = None, radius_step: 'float' = 1, azimuth_step: 'float | None' = None, azimuth_units: 'str' = 'PI radians', azimuth_compact_fraction: 'bool' = True, azimuth_offset: 'float' = 0, azimuth_direction: 'str' = 'CCW', azimuth_label_buff: 'float' = 0.1, azimuth_label_font_size: 'float' = 24, radius_config: 'dict[str, Any] | None' = None, background_line_style: 'dict[str, Any] | None' = None, faded_line_style: 'dict[str, Any] | None' = None, faded_line_ratio: 'int' = 1, make_smooth_after_applying_functions: 'bool' = True, **kwargs: 'Any')` ← Axes
> Creates a polar plane with background lines.

<details><summary>métodos próprios (7) · herdados: 284</summary>

- `__init__(self, radius_max: 'float' = 4.0, size: 'float | None' = None, radius_step: 'float' = 1, azimuth_step: 'float | None' = None, azimuth_units: 'str' = 'PI radians', azimuth_compact_fraction: 'bool' = True, azimuth_offset: 'float' = 0, azimuth_direction: 'str' = 'CCW', azimuth_label_buff: 'float' = 0.1, azimuth_label_font_size: 'float' = 24, radius_config: 'dict[str, Any] | None' = None, background_line_style: 'dict[str, Any] | None' = None, faded_line_style: 'dict[str, Any] | None' = None, faded_line_ratio: 'int' = 1, make_smooth_after_applying_functions: 'bool' = True, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `add_coordinates(self, r_values: 'Iterable[float] | None' = None, a_values: 'Iterable[float] | None' = None) -> 'Self'` — Adds the coordinates.
- `get_axes(self) -> 'VGroup'` — Gets the axes.
- `get_coordinate_labels(self, r_values: 'Iterable[float] | None' = None, a_values: 'Iterable[float] | None' = None, **kwargs: 'Any') -> 'VDict'` — Gets labels for the coordinates
- `get_radian_label(self, number: 'float', font_size: 'float' = 24, **kwargs: 'Any') -> 'MathTex'`
- `get_vector(self, coords: 'Sequence[ManimFloat]', **kwargs: 'Any') -> 'Arrow'`
- `prepare_for_nonlinear_transform(self, num_inserted_curves: 'int' = 50) -> 'Self'`

</details>

### `SampleSpace(height: 'float' = 3, width: 'float' = 3, fill_color: 'ParsableManimColor' = ManimColor('#444444'), fill_opacity: 'float' = 1, stroke_width: 'float' = 0.5, stroke_color: 'ParsableManimColor' = ManimColor('#BBBBBB'), default_label_scale_val: 'float' = 1)` ← Rectangle
> A mobject representing a twodimensional rectangular

<details><summary>métodos próprios (14) · herdados: 245</summary>

- `__init__(self, height: 'float' = 3, width: 'float' = 3, fill_color: 'ParsableManimColor' = ManimColor('#444444'), fill_opacity: 'float' = 1, stroke_width: 'float' = 0.5, stroke_color: 'ParsableManimColor' = ManimColor('#BBBBBB'), default_label_scale_val: 'float' = 1)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_braces_and_labels(self) -> 'Self'`
- `add_label(self, label: 'str') -> 'Self'`
- `add_title(self, title: 'str' = 'Sample space', buff: 'float' = 0.25) -> 'Self'`
- `complete_p_list(self, p_list: 'float | Iterable[float]') -> 'list[float]'`
- `divide_horizontally(self, *args: 'Any', **kwargs: 'Any') -> 'Self'`
- `divide_vertically(self, *args: 'Any', **kwargs: 'Any') -> 'Self'`
- `get_bottom_braces_and_labels(self, labels: 'list[str | VMobject | OpenGLVMobject]', **kwargs: 'Any') -> 'VGroup'`
- `get_division_along_dimension(self, p_list: 'float | Iterable[float]', dim: 'int', colors: 'Sequence[ParsableManimColor]', vect: 'Vector3D') -> 'VGroup'`
- `get_horizontal_division(self, p_list: 'float | Iterable[float]', colors: 'Sequence[ParsableManimColor]' = [ManimColor('#699C52'), ManimColor('#236B8E')], vect: 'Vector3D' = array([ 0., -1.,  0.])) -> 'VGroup'`
- `get_side_braces_and_labels(self, labels: 'list[str | VMobject | OpenGLVMobject]', direction: 'Vector3D' = array([-1.,  0.,  0.]), **kwargs: 'Any') -> 'VGroup'`
- `get_subdivision_braces_and_labels(self, parts: 'VGroup', labels: 'list[str | VMobject | OpenGLVMobject]', direction: 'Vector3D', buff: 'float' = 0.1, min_num_quads: 'int' = 1) -> 'VGroup'`
- `get_top_braces_and_labels(self, labels: 'list[str | VMobject | OpenGLVMobject]', **kwargs: 'Any') -> 'VGroup'`
- `get_vertical_division(self, p_list: 'float | Iterable[float]', colors: 'Sequence[ParsableManimColor]' = [ManimColor('#EC92AB'), ManimColor('#F7D96F')], vect: 'Vector3D' = array([1., 0., 0.])) -> 'VGroup'`

</details>

### `ThreeDAxes(x_range: 'Sequence[float] | None' = (-6, 6, 1), y_range: 'Sequence[float] | None' = (-5, 5, 1), z_range: 'Sequence[float] | None' = (-4, 4, 1), x_length: 'float | None' = 10.5, y_length: 'float | None' = 10.5, z_length: 'float | None' = 6.5, z_axis_config: 'dict[str, Any] | None' = None, z_normal: 'Vector3DLike' = array([ 0., -1.,  0.]), num_axis_pieces: 'int' = 20, light_source: 'Point3DLike' = array([-7., -9., 10.]), depth: 'Any' = None, gloss: 'float' = 0.5, **kwargs: 'dict[str, Any]')` ← Axes
> A 3-dimensional set of axes.

<details><summary>métodos próprios (4) · herdados: 284</summary>

- `__init__(self, x_range: 'Sequence[float] | None' = (-6, 6, 1), y_range: 'Sequence[float] | None' = (-5, 5, 1), z_range: 'Sequence[float] | None' = (-4, 4, 1), x_length: 'float | None' = 10.5, y_length: 'float | None' = 10.5, z_length: 'float | None' = 6.5, z_axis_config: 'dict[str, Any] | None' = None, z_normal: 'Vector3DLike' = array([ 0., -1.,  0.]), num_axis_pieces: 'int' = 20, light_source: 'Point3DLike' = array([-7., -9., 10.]), depth: 'Any' = None, gloss: 'float' = 0.5, **kwargs: 'dict[str, Any]')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_axis_labels(self, x_label: 'float | str | VMobject' = 'x', y_label: 'float | str | VMobject' = 'y', z_label: 'float | str | VMobject' = 'z') -> 'VGroup'` — Defines labels for the x_axis and y_axis of the graph.
- `get_y_axis_label(self, label: 'float | str | VMobject', edge: 'Vector3DLike' = array([1., 1., 0.]), direction: 'Vector3DLike' = array([1., 1., 0.]), buff: 'float' = 0.1, rotation: 'float' = 1.5707963267948966, rotation_axis: 'Vector3DLike' = array([0., 0., 1.]), **kwargs: 'dict[str, Any]') -> 'Mobject'` — Generate a y-axis label.
- `get_z_axis_label(self, label: 'float | str | VMobject', edge: 'Vector3DLike' = array([0., 0., 1.]), direction: 'Vector3DLike' = array([1., 0., 0.]), buff: 'float' = 0.1, rotation: 'float' = 1.5707963267948966, rotation_axis: 'Vector3DLike' = array([1., 0., 0.]), **kwargs: 'Any') -> 'Mobject'` — Generate a z-axis label.

</details>

### `UnitInterval(unit_size: 'float' = 10, numbers_with_elongated_ticks: 'list[float] | None' = None, decimal_number_config: 'dict[str, Any] | None' = None, **kwargs: 'Any')` ← NumberLine
> Creates a number line with tick marks.

<details><summary>métodos próprios (1) · herdados: 283</summary>

- `__init__(self, unit_size: 'float' = 10, numbers_with_elongated_ticks: 'list[float] | None' = None, decimal_number_config: 'dict[str, Any] | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

- `BLACK` = `ManimColor('#000000')`
- `BLUE` = `ManimColor('#58C4DD')`
- `BLUE_D` = `ManimColor('#29ABCA')`
- `BLUE_E` = `ManimColor('#236B8E')`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `DARK_GREY` = `ManimColor('#444444')`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPSILON` = `0.0001`
- `GREEN` = `ManimColor('#83C167')`
- `GREEN_E` = `ManimColor('#699C52')`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `LIGHT_GREY` = `ManimColor('#BBBBBB')`
- `MAROON_B` = `ManimColor('#EC92AB')`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PURE_YELLOW` = `ManimColor('#FFFF00')`
- `PURE_YELLOW` = `ManimColor('#FFFF00')`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `START_X` = `30`
- `START_X` = `30`
- `START_X` = `30`
- `START_Y` = `20`
- `START_Y` = `20`
- `START_Y` = `20`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `WHITE` = `ManimColor('#FFFFFF')`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `YELLOW` = `ManimColor('#F7D96F')`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`

## mobject/logo

### `ManimBanner(dark_theme: 'bool' = True)` ← VGroup
> Convenience class representing Manim's banner.

<details><summary>métodos próprios (4) · herdados: 241</summary>

- `__init__(self, dark_theme: 'bool' = True)` — Initialize self.  See help(type(self)) for accurate signature.
- `create(self, run_time: 'float' = 2) -> 'AnimationGroup'` — The creation animation for Manim's logo.
- `expand(self, run_time: 'float' = 1.5, direction: 'str' = 'center') -> 'Succession'` — An animation that expands Manim's logo into its banner.
- `scale(self, scale_factor: 'float', **kwargs: 'Any') -> 'Self'` — Scale the banner by the specified scale factor.

</details>

- `MANIM_SVG_PATHS` = `[Path(Move(end=Point(4.64259,-2.092154)), Line(start=Point(4.64259,-2.092154), end=Point(2.739726,-6.625156)), CubicB...`

## mobject/matrix

### `DecimalMatrix(matrix: 'Iterable[Iterable[Any]]', element_to_mobject: 'type[VMobject] | Callable[..., VMobject]' = <class 'manim.mobject.text.numbers.DecimalNumber'>, element_to_mobject_config: 'dict[str, Any]' = {'num_decimal_places': 1}, **kwargs: 'Any')` ← Matrix
> A mobject that displays a matrix with decimal entries on the screen.

<details><summary>métodos próprios (1) · herdados: 250</summary>

- `__init__(self, matrix: 'Iterable[Iterable[Any]]', element_to_mobject: 'type[VMobject] | Callable[..., VMobject]' = <class 'manim.mobject.text.numbers.DecimalNumber'>, element_to_mobject_config: 'dict[str, Any]' = {'num_decimal_places': 1}, **kwargs: 'Any')` — Will round/truncate the decimal places as per the provided config.

</details>

### `IntegerMatrix(matrix: 'Iterable[Iterable[Any]]', element_to_mobject: 'type[VMobject] | Callable[..., VMobject]' = <class 'manim.mobject.text.numbers.Integer'>, **kwargs: 'Any')` ← Matrix
> A mobject that displays a matrix with integer entries on the screen.

<details><summary>métodos próprios (1) · herdados: 250</summary>

- `__init__(self, matrix: 'Iterable[Iterable[Any]]', element_to_mobject: 'type[VMobject] | Callable[..., VMobject]' = <class 'manim.mobject.text.numbers.Integer'>, **kwargs: 'Any')` — Will round if there are decimal entries in the matrix.

</details>

### `Matrix(matrix: 'Iterable[Iterable[Any] | Vector2DLike]', v_buff: 'float' = 0.8, h_buff: 'float' = 1.3, bracket_h_buff: 'float' = 0.25, bracket_v_buff: 'float' = 0.25, add_background_rectangles_to_entries: 'bool' = False, include_background_rectangle: 'bool' = False, element_to_mobject: 'type[VMobject] | Callable[..., VMobject]' = <class 'manim.mobject.text.tex_mobject.MathTex'>, element_to_mobject_config: 'dict[str, Any]' = {}, element_alignment_corner: 'Vector3DLike' = array([ 1., -1.,  0.]), left_bracket: 'str' = '[', right_bracket: 'str' = ']', stretch_brackets: 'bool' = True, bracket_config: 'dict' = {}, **kwargs: 'Any')` ← VMobject
> A mobject that displays a matrix on the screen.

<details><summary>métodos próprios (9) · herdados: 242</summary>

- `__init__(self, matrix: 'Iterable[Iterable[Any] | Vector2DLike]', v_buff: 'float' = 0.8, h_buff: 'float' = 1.3, bracket_h_buff: 'float' = 0.25, bracket_v_buff: 'float' = 0.25, add_background_rectangles_to_entries: 'bool' = False, include_background_rectangle: 'bool' = False, element_to_mobject: 'type[VMobject] | Callable[..., VMobject]' = <class 'manim.mobject.text.tex_mobject.MathTex'>, element_to_mobject_config: 'dict[str, Any]' = {}, element_alignment_corner: 'Vector3DLike' = array([ 1., -1.,  0.]), left_bracket: 'str' = '[', right_bracket: 'str' = ']', stretch_brackets: 'bool' = True, bracket_config: 'dict' = {}, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `add_background_to_entries(self) -> 'Self'` — Add a black background rectangle to the matrix,
- `get_brackets(self) -> 'VGroup'` — Return the bracket mobjects.
- `get_columns(self) -> 'VGroup'` — Return columns of the matrix as VGroups.
- `get_entries(self) -> 'VGroup'` — Return the individual entries of the matrix.
- `get_mob_matrix(self) -> 'list[list[VMobject]]'` — Return the underlying mob matrix mobjects.
- `get_rows(self) -> 'VGroup'` — Return rows of the matrix as VGroups.
- `set_column_colors(self, *colors: 'str') -> 'Self'` — Set individual colors for each columns of the matrix.
- `set_row_colors(self, *colors: 'str') -> 'Self'` — Set individual colors for each row of the matrix.

</details>

### `MobjectMatrix(matrix: 'Iterable[Iterable[Any]]', element_to_mobject: 'type[VMobject] | Callable[..., VMobject]' = <function MobjectMatrix.<lambda> at 0x713b830db6a0>, **kwargs: 'Any')` ← Matrix
> A mobject that displays a matrix of mobject entries on the screen.

<details><summary>métodos próprios (1) · herdados: 250</summary>

- `__init__(self, matrix: 'Iterable[Iterable[Any]]', element_to_mobject: 'type[VMobject] | Callable[..., VMobject]' = <function MobjectMatrix.<lambda> at 0x713b830db6a0>, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

- `BOLD` = `'BOLD'`
- `BOOK` = `'BOOK'`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CTRL_VALUE` = `65507`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `HEAVY` = `'HEAVY'`
- `IN` = `array([ 0.,  0., -1.])`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LIGHT` = `'LIGHT'`
- `MEDIUM` = `'MEDIUM'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OBLIQUE` = `'OBLIQUE'`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RIGHT` = `array([1., 0., 0.])`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SHIFT_VALUE` = `65505`
- `SMALL_BUFF` = `0.1`
- `START_X` = `30`
- `START_Y` = `20`
- `TAU` = `6.283185307179586`
- `THIN` = `'THIN'`
- `UL` = `array([-1.,  1.,  0.])`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- **`get_det_text(matrix: 'Matrix', determinant: 'int | str | None' = None, background_rect: 'bool' = False, initial_scale_factor: 'float' = 2) -> 'VGroup'`** — Helper function to create determinant.
- **`matrix_to_mobject(matrix: 'np.ndarray') -> 'MathTex'`**
- **`matrix_to_tex_string(matrix: 'np.ndarray') -> 'str'`**

## mobject/opengl

### `ConvertToOpenGL(name: 'str', bases: 'tuple[type, ...]', namespace: 'dict[str, Any]') -> 'type'` ← ABCMeta
> Metaclass for swapping (V)Mobject with its OpenGL counterpart at runtime

<details><summary>métodos próprios (1) · herdados: 3</summary>

- `__init__(cls, name: 'str', bases: 'tuple[type, ...]', namespace: 'dict[str, Any]')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `DotCloud(color: 'ParsableManimColor' = ManimColor('#FFFF00'), stroke_width: 'float' = 2.0, radius: 'float' = 2.0, density: 'float' = 10, **kwargs: 'Any')` ← OpenGLPMobject
> Mathematical Object: base class for objects that can be displayed on screen.

<details><summary>métodos próprios (3) · herdados: 194</summary>

- `__init__(self, color: 'ParsableManimColor' = ManimColor('#FFFF00'), stroke_width: 'float' = 2.0, radius: 'float' = 2.0, density: 'float' = 10, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `init_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `make_3d(self, gloss: 'float' = 0.5, shadow: 'float' = 0.2) -> 'Self'`

</details>

### `OpenGLAnnularSector(inner_radius: 'float' = 1, outer_radius: 'float' = 2, angle: 'float' = 1.5707963267948966, start_angle: 'float' = 0, fill_opacity: 'float' = 1, stroke_width: 'float' = 0, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), **kwargs: 'Any')` ← OpenGLArc
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (2) · herdados: 289</summary>

- `__init__(self, inner_radius: 'float' = 1, outer_radius: 'float' = 2, angle: 'float' = 1.5707963267948966, start_angle: 'float' = 0, fill_opacity: 'float' = 1, stroke_width: 'float' = 0, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `init_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.

</details>

### `OpenGLAnnulus(inner_radius: 'float' = 1, outer_radius: 'float' = 2, fill_opacity: 'float' = 1, stroke_width: 'float' = 0, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), mark_paths_closed: 'bool' = False, **kwargs: 'Any')` ← OpenGLCircle
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (2) · herdados: 290</summary>

- `__init__(self, inner_radius: 'float' = 1, outer_radius: 'float' = 2, fill_opacity: 'float' = 1, stroke_width: 'float' = 0, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), mark_paths_closed: 'bool' = False, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `init_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.

</details>

### `OpenGLArc(start_angle: 'float' = 0, angle: 'float' = 1.5707963267948966, radius: 'float' = 1.0, n_components: 'int' = 8, arc_center: 'Point3DLike' = array([0., 0., 0.]), **kwargs: 'Any')` ← OpenGLTipableVMobject
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (7) · herdados: 284</summary>

- `__init__(self, start_angle: 'float' = 0, angle: 'float' = 1.5707963267948966, radius: 'float' = 1.0, n_components: 'int' = 8, arc_center: 'Point3DLike' = array([0., 0., 0.]), **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `create_quadratic_bezier_points(angle: 'float', start_angle: 'float' = 0, n_components: 'int' = 8) -> 'QuadraticSpline'`
- `get_arc_center(self) -> 'Point3D'` — Looks at the normals to the first two
- `get_start_angle(self) -> 'float'`
- `get_stop_angle(self) -> 'float'`
- `init_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `move_arc_center_to(self, point: 'Point3DLike') -> 'Self'`

</details>

### `OpenGLArcBetweenPoints(start: 'Point3DLike', end: 'Point3DLike', angle: 'float' = 1.5707963267948966, **kwargs: 'Any')` ← OpenGLArc
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (1) · herdados: 290</summary>

- `__init__(self, start: 'Point3DLike', end: 'Point3DLike', angle: 'float' = 1.5707963267948966, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLArrow(start: 'Point3DLike' = array([-1.,  0.,  0.]), end: 'Point3DLike' = array([1., 0., 0.]), path_arc: 'float' = 0, fill_color: 'ParsableManimColor' = ManimColor('#DDDDDD'), fill_opacity: 'float' = 1, stroke_width: 'float' = 0, buff: 'float' = 0.25, thickness: 'float' = 0.05, tip_width_ratio: 'float' = 5, tip_angle: 'float' = 1.0471975511965976, max_tip_length_to_length_ratio: 'float' = 0.5, max_width_to_length_ratio: 'float' = 0.1, **kwargs: 'Any')` ← OpenGLLine
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (9) · herdados: 291</summary>

- `__init__(self, start: 'Point3DLike' = array([-1.,  0.,  0.]), end: 'Point3DLike' = array([1., 0., 0.]), path_arc: 'float' = 0, fill_color: 'ParsableManimColor' = ManimColor('#DDDDDD'), fill_opacity: 'float' = 1, stroke_width: 'float' = 0, buff: 'float' = 0.25, thickness: 'float' = 0.05, tip_width_ratio: 'float' = 5, tip_angle: 'float' = 1.0471975511965976, max_tip_length_to_length_ratio: 'float' = 0.5, max_width_to_length_ratio: 'float' = 0.1, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_end(self) -> 'Point3D'` — Returns the point, where the stroke that surrounds the :class:`~.OpenGLMobject` ends.
- `get_start(self) -> 'Point3D'` — Returns the point, where the stroke that surrounds the :class:`~.OpenGLMobject` starts.
- `put_start_and_end_on(self, start: 'Point3DLike', end: 'Point3DLike') -> 'Self'`
- `reset_points_around_ends(self) -> 'Self'`
- `scale(self, *args: 'Any', **kwargs: 'Any') -> 'Self'` — Scale the size by a factor.
- `set_path_arc(self, path_arc: 'float') -> 'Self'`
- `set_points_by_ends(self, start: 'Point3DLike', end: 'Point3DLike', buff: 'float' = 0, path_arc: 'float' = 0) -> 'Self'`
- `set_thickness(self, thickness: 'float') -> 'Self'`

</details>

### `OpenGLArrowTip(fill_opacity: 'float' = 1, fill_color: 'ParsableManimColor' = ManimColor('#FFFFFF'), stroke_width: 'float' = 0, width: 'float' = 0.35, length: 'float' = 0.35, angle: 'float' = 0, **kwargs: 'Any')` ← OpenGLTriangle
> A vectorized mobject.

<details><summary>métodos próprios (6) · herdados: 272</summary>

- `__init__(self, fill_opacity: 'float' = 1, fill_color: 'ParsableManimColor' = ManimColor('#FFFFFF'), stroke_width: 'float' = 0, width: 'float' = 0.35, length: 'float' = 0.35, angle: 'float' = 0, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_angle(self) -> 'float'`
- `get_base(self) -> 'Point3D'`
- `get_length(self) -> 'float'`
- `get_tip_point(self) -> 'Point3D'`
- `get_vector(self) -> 'Vector3D'`

</details>

### `OpenGLCircle(color: 'ParsableManimColor' = ManimColor('#FC6255'), **kwargs: 'Any')` ← OpenGLArc
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (3) · herdados: 289</summary>

- `__init__(self, color: 'ParsableManimColor' = ManimColor('#FC6255'), **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `point_at_angle(self, angle: 'float') -> 'Point3D'`
- `surround(self, mobject: 'OpenGLMobject', dim_to_match: 'int' = 0, stretch: 'bool' = False, buff: 'float' = 0.25) -> 'Self'`

</details>

### `OpenGLCubicBezier(a0: 'Point3DLike', h0: 'Point3DLike', h1: 'Point3DLike', a1: 'Point3DLike', **kwargs: 'Any')` ← OpenGLVMobject
> A vectorized mobject.

<details><summary>métodos próprios (1) · herdados: 270</summary>

- `__init__(self, a0: 'Point3DLike', h0: 'Point3DLike', h1: 'Point3DLike', a1: 'Point3DLike', **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLCurvedArrow(start_point: 'Point3DLike', end_point: 'Point3DLike', **kwargs: 'Any')` ← OpenGLArcBetweenPoints
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (1) · herdados: 290</summary>

- `__init__(self, start_point: 'Point3DLike', end_point: 'Point3DLike', **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLCurvedDoubleArrow(start_point: 'Point3DLike', end_point: 'Point3DLike', **kwargs: 'Any')` ← OpenGLCurvedArrow
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (1) · herdados: 290</summary>

- `__init__(self, start_point: 'Point3DLike', end_point: 'Point3DLike', **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLCurvesAsSubmobjects(vmobject, **kwargs)` ← OpenGLVGroup
> Convert a curve's elements to submobjects.

<details><summary>métodos próprios (1) · herdados: 270</summary>

- `__init__(self, vmobject, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLDashedLine(*args: 'Any', dash_length: 'float' = 0.05, dashed_ratio: 'float' = 0.5, **kwargs: 'Any')` ← OpenGLLine
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (6) · herdados: 293</summary>

- `__init__(self, *args: 'Any', dash_length: 'float' = 0.05, dashed_ratio: 'float' = 0.5, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `calculate_num_dashes(self, dashed_ratio: 'float') -> 'int'`
- `get_end(self) -> 'Point3D'` — Returns the point, where the stroke that surrounds the :class:`~.OpenGLMobject` ends.
- `get_first_handle(self) -> 'Point3D'`
- `get_last_handle(self) -> 'Point3D'`
- `get_start(self) -> 'Point3D'` — Returns the point, where the stroke that surrounds the :class:`~.OpenGLMobject` starts.

</details>

### `OpenGLDashedVMobject(vmobject: 'OpenGLVMobject', num_dashes: 'int' = 15, dashed_ratio: 'float' = 0.5, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), **kwargs)` ← OpenGLVMobject
> A :class:`OpenGLVMobject` composed of dashes instead of lines.

<details><summary>métodos próprios (1) · herdados: 270</summary>

- `__init__(self, vmobject: 'OpenGLVMobject', num_dashes: 'int' = 15, dashed_ratio: 'float' = 0.5, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLDot(point: 'Point3DLike' = array([0., 0., 0.]), radius: 'float' = 0.08, stroke_width: 'float' = 0, fill_opacity: 'float' = 1.0, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), **kwargs: 'Any')` ← OpenGLCircle
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (1) · herdados: 291</summary>

- `__init__(self, point: 'Point3DLike' = array([0., 0., 0.]), radius: 'float' = 0.08, stroke_width: 'float' = 0, fill_opacity: 'float' = 1.0, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLDoubleArrow(*args: 'Any', **kwargs: 'Any')` ← OpenGLArrow
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (1) · herdados: 299</summary>

- `__init__(self, *args: 'Any', **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLElbow(width: 'float' = 0.2, angle: 'float' = 0, **kwargs: 'Any')` ← OpenGLVMobject
> A vectorized mobject.

<details><summary>métodos próprios (1) · herdados: 270</summary>

- `__init__(self, width: 'float' = 0.2, angle: 'float' = 0, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLEllipse(width: 'float' = 2, height: 'float' = 1, **kwargs: 'Any')` ← OpenGLCircle
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (1) · herdados: 291</summary>

- `__init__(self, width: 'float' = 2, height: 'float' = 1, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLGroup(*mobjects: 'OpenGLMobject', **kwargs: 'Any') -> 'None'` ← OpenGLMobject
> Mathematical Object: base class for objects that can be displayed on screen.

<details><summary>métodos próprios (1) · herdados: 186</summary>

- `__init__(self, *mobjects: 'OpenGLMobject', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLImageMobject(filename_or_array: 'str | Path | npt.NDArray', width: 'float | None' = None, height: 'float | None' = None, image_mode: 'str' = 'RGBA', resampling_algorithm: 'Resampling' = <Resampling.BICUBIC: 3>, opacity: 'float' = 1, gloss: 'float' = 0, shadow: 'float' = 0, **kwargs: 'Any')` ← OpenGLTexturedSurface
> Creates a Surface.

<details><summary>métodos próprios (2) · herdados: 194</summary>

- `__init__(self, filename_or_array: 'str | Path | npt.NDArray', width: 'float | None' = None, height: 'float | None' = None, image_mode: 'str' = 'RGBA', resampling_algorithm: 'Resampling' = <Resampling.BICUBIC: 3>, opacity: 'float' = 1, gloss: 'float' = 0, shadow: 'float' = 0, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_image_from_file(self, image_file: 'str | Path | np.ndarray', image_mode: 'str') -> 'Image.Image'`

</details>

### `OpenGLLine(start: 'Point3DLike' = array([-1.,  0.,  0.]), end: 'Point3DLike' = array([1., 0., 0.]), buff: 'float' = 0, path_arc: 'float' = 0, **kwargs: 'Any')` ← OpenGLTipableVMobject
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (15) · herdados: 283</summary>

- `__init__(self, start: 'Point3DLike' = array([-1.,  0.,  0.]), end: 'Point3DLike' = array([1., 0., 0.]), buff: 'float' = 0, path_arc: 'float' = 0, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `account_for_buff(self, buff: 'float') -> 'Self'`
- `get_angle(self) -> 'float'`
- `get_projection(self, point: 'Point3DLike') -> 'Point3D'` — Return projection of a point onto the line
- `get_slope(self) -> 'float'`
- `get_unit_vector(self) -> 'Vector3D'`
- `get_vector(self) -> 'Vector3D'`
- `init_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `pointify(self, mob_or_point: 'Mobject | Point3DLike', direction: 'Vector3DLike' = None) -> 'Point3D'` — Take an argument passed into Line (or subclass) and turn
- `put_start_and_end_on(self, start: 'Point3DLike', end: 'Point3DLike') -> 'Self'`
- `set_angle(self, angle: 'float', about_point: 'Point3DLike | None' = None) -> 'Self'`
- `set_length(self, length: 'float') -> 'Self'`
- `set_path_arc(self, new_value: 'float') -> 'Self'`
- `set_points_by_ends(self, start: 'Point3DLike', end: 'Point3DLike', buff: 'float' = 0, path_arc: 'float' = 0) -> 'Self'`
- `set_start_and_end_attrs(self, start: 'Mobject | Point3DLike', end: 'Mobject | Point3DLike') -> 'Self'`

</details>

### `OpenGLMobject(color: 'ParsableManimColor | Sequence[ParsableManimColor]' = ManimColor('#FFFFFF'), opacity: 'float' = 1, dim: 'int' = 3, gloss: 'float' = 0.0, shadow: 'float' = 0.0, render_primitive: 'int' = 4, texture_paths: 'dict[str, str] | None' = None, depth_test: 'bool' = False, is_fixed_in_frame: 'bool' = False, is_fixed_orientation: 'bool' = False, listen_to_events: 'bool' = False, model_matrix: 'MatrixMN | None' = None, should_render: 'bool' = True, name: 'str | None' = None, **kwargs: 'Any')`
> Mathematical Object: base class for objects that can be displayed on screen.

<details><summary>métodos próprios (187) · herdados: 0</summary>

- `__init__(self, color: 'ParsableManimColor | Sequence[ParsableManimColor]' = ManimColor('#FFFFFF'), opacity: 'float' = 1, dim: 'int' = 3, gloss: 'float' = 0.0, shadow: 'float' = 0.0, render_primitive: 'int' = 4, texture_paths: 'dict[str, str] | None' = None, depth_test: 'bool' = False, is_fixed_in_frame: 'bool' = False, is_fixed_orientation: 'bool' = False, listen_to_events: 'bool' = False, model_matrix: 'MatrixMN | None' = None, should_render: 'bool' = True, name: 'str | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `add(self, *mobjects: 'OpenGLMobject', update_parent: 'bool' = False) -> 'Self'` — Add mobjects as submobjects.
- `add_background_rectangle(self, color: 'ParsableManimColor | None' = None, opacity: 'float' = 0.75, **kwargs: 'Any') -> 'Self'` — Add a BackgroundRectangle as submobject.
- `add_background_rectangle_to_family_members_with_points(self, **kwargs: 'Any') -> 'Self'`
- `add_background_rectangle_to_submobjects(self, **kwargs: 'Any') -> 'Self'`
- `add_n_more_submobjects(self, n: 'int') -> 'Self'`
- `add_to_back(self, *mobjects: 'OpenGLMobject') -> 'Self'` — Add all passed mobjects to the back of the submobjects.
- `add_updater(self, update_function: '_Updater', index: 'int | None' = None, call_updater: 'bool' = False) -> 'Self'`
- `align_data(self, mobject: 'OpenGLMobject') -> 'Self'`
- `align_data_and_family(self, mobject: 'OpenGLMobject') -> 'Self'`
- `align_family(self, mobject: 'OpenGLMobject') -> 'Self'`
- `align_on_border(self, direction: 'Vector3DLike', buff: 'float' = 0.5) -> 'Self'` — Direction just needs to be a vector pointing towards side or
- `align_points(self, mobject: 'OpenGLMobject') -> 'Self'`
- `align_to(self, mobject_or_point: 'OpenGLMobject | Point3DLike', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Examples:
- `append_points(self, new_points: 'Point3DLike_Array') -> 'Self'`
- `apply_complex_function(self, function: 'Callable[[complex], complex]', **kwargs: 'Any') -> 'Self'` — Applies a complex function to a :class:`OpenGLMobject`.
- `apply_depth_test(self) -> 'Self'`
- `apply_function(self, function: 'MappingFunction', **kwargs: 'Any') -> 'Self'`
- `apply_function_to_position(self, function: 'MappingFunction') -> 'Self'`
- `apply_function_to_submobject_positions(self, function: 'MappingFunction') -> 'Self'`
- `apply_matrix(self, matrix: 'MatrixMN', **kwargs: 'Any') -> 'Self'`
- `apply_over_attr_arrays(self, func: 'Callable[[npt.NDArray[_T_np]], npt.NDArray[_T_np]]') -> 'Self'`
- `apply_points_function(self, func: 'MultiMappingFunction', about_point: 'Point3DLike | None' = None, about_edge: 'Vector3DLike | None' = array([0., 0., 0.]), works_on_bounding_box: 'bool' = False) -> 'Self'`
- `arrange(self, direction: 'Vector3DLike' = array([1., 0., 0.]), center: 'bool' = True, **kwargs: 'Any') -> 'Self'` — Sorts :class:`~.OpenGLMobject` next to each other on screen.
- `arrange_in_grid(self, rows: 'int | None' = None, cols: 'int | None' = None, buff: 'float | tuple[float, float]' = 0.25, cell_alignment: 'Vector3DLike' = array([0., 0., 0.]), row_alignments: 'str | None' = None, col_alignments: 'str | None' = None, row_heights: 'Sequence[float | None] | None' = None, col_widths: 'Sequence[float | None] | None' = None, flow_order: 'str' = 'rd', **kwargs: 'Any') -> 'Self'` — Arrange submobjects in a grid.
- `assemble_family(self) -> 'Self'`
- `become(self, mobject: 'OpenGLMobject', match_height: 'bool' = False, match_width: 'bool' = False, match_depth: 'bool' = False, match_center: 'bool' = False, stretch: 'bool' = False) -> 'Self'` — Edit all data and submobjects to be identical
- `center(self) -> 'Self'` — Moves the mobject to the center of the Scene.
- `check_data_alignment(self, array: '_ShaderData', data_key: 'str') -> 'Self'`
- `clear_points(self) -> 'Self'`
- `clear_updaters(self, recurse: 'bool' = True) -> 'Self'`
- `compute_bounding_box(self) -> 'Point3D_Array'`
- `copy(self, shallow: 'bool' = False) -> 'Self'` — Create and return an identical copy of the :class:`OpenGLMobject` including all
- `deactivate_depth_test(self) -> 'Self'`
- `deepcopy(self) -> 'Self'`
- `duplicate(self, n: 'int') -> 'OpenGLGroup'` — Returns an :class:`~.OpenGLGroup` containing ``n`` copies of the mobject.
- `fade(self, darkness: 'float' = 0.5, recurse: 'bool' = True) -> 'Self'`
- `family_members_with_points(self) -> 'Sequence[OpenGLMobject]'`
- `fix_in_frame(self) -> 'Self'`
- `fix_orientation(self) -> 'Self'`
- `flip(self, axis: 'Vector3DLike' = array([0., 1., 0.]), **kwargs: 'Any') -> 'Self'` — Flips/Mirrors an mobject about its center.
- `generate_target(self, use_deepcopy: 'bool' = False) -> 'Self'`
- `get_all_points(self) -> 'Point3D_Array'`
- `get_array_attrs(self) -> 'Iterable[str]'`
- `get_bottom(self) -> 'Point3D'` — Get bottom coordinates of a box bounding the :class:`~.OpenGLMobject`
- `get_boundary_point(self, direction: 'Vector3DLike') -> 'Point3D'`
- `get_bounding_box(self) -> 'Point3D_Array'`
- `get_bounding_box_point(self, direction: 'Vector3DLike') -> 'Point3D'`
- `get_center(self) -> 'Point3D'` — Get center coordinates.
- `get_center_of_mass(self) -> 'Point3D'`
- `get_color(self) -> 'str'`
- `get_continuous_bounding_box_point(self, direction: 'Vector3DLike') -> 'Point3D'`
- `get_coord(self, dim: 'int', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'ManimFloat'` — Meant to generalize ``get_x``, ``get_y`` and ``get_z``
- `get_corner(self, direction: 'Vector3DLike') -> 'Point3D'` — Get corner coordinates for certain direction.
- `get_depth(self) -> 'float'` — Returns the depth of the mobject.
- `get_edge_center(self, direction: 'Vector3DLike') -> 'Point3D'` — Get edge coordinates for certain direction.
- `get_end(self) -> 'Point3D'` — Returns the point, where the stroke that surrounds the :class:`~.OpenGLMobject` ends.
- `get_family(self, recurse: 'bool' = True) -> 'Sequence[OpenGLMobject]'`
- `get_family_updaters(self) -> 'Sequence[_Updater]'`
- `get_gloss(self) -> 'float'`
- `get_grid(self, n_rows: 'int', n_cols: 'int', height: 'float | None' = None, **kwargs: 'Any') -> 'OpenGLGroup'` — Returns a new mobject containing multiple copies of this one
- `get_group_class(self) -> 'type[OpenGLGroup]'`
- `get_height(self) -> 'float'` — Returns the height of the mobject.
- `get_left(self) -> 'Point3D'` — Get left coordinates of a box bounding the :class:`~.OpenGLMobject`
- `get_midpoint(self) -> 'Point3D'` — Get coordinates of the middle of the path that forms the  :class:`~.OpenGLMobject`.
- `get_mobject_type_class() -> 'type[OpenGLMobject]'` — Return the base class of this mobject type.
- `get_nadir(self) -> 'Point3D'` — Get nadir (opposite the zenith) coordinates of a box bounding a 3D :class:`~.OpenGLMobject`.
- `get_num_points(self) -> 'int'`
- `get_opacity(self) -> 'float'`
- `get_pieces(self, n_pieces: 'int') -> 'OpenGLMobject'`
- `get_resized_shader_data_array(self, length: 'float') -> '_ShaderData'`
- `get_right(self) -> 'Point3D'` — Get right coordinates of a box bounding the :class:`~.OpenGLMobject`
- `get_shader_data(self) -> '_ShaderData'`
- `get_shader_uniforms(self) -> 'dict[str, Any]'`
- `get_shader_vert_indices(self) -> 'Sequence[int] | None'`
- `get_shader_wrapper(self) -> "'ShaderWrapper'"`
- `get_shader_wrapper_list(self) -> "Sequence['ShaderWrapper']"`
- `get_shadow(self) -> 'float'`
- `get_start(self) -> 'Point3D'` — Returns the point, where the stroke that surrounds the :class:`~.OpenGLMobject` starts.
- `get_start_and_end(self) -> 'tuple[Point3D, Point3D]'` — Returns starting and ending point of a stroke as a ``tuple``.
- `get_time_based_updaters(self) -> 'Sequence[_TimeBasedUpdater]'`
- `get_top(self) -> 'Point3D'` — Get top coordinates of a box bounding the :class:`~.OpenGLMobject`
- `get_updaters(self) -> 'Sequence[_Updater]'`
- `get_width(self) -> 'float'` — Returns the width of the mobject.
- `get_x(self, direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'ManimFloat'` — Returns x coordinate of the center of the :class:`~.OpenGLMobject` as ``float``
- `get_y(self, direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'ManimFloat'` — Returns y coordinate of the center of the :class:`~.OpenGLMobject` as ``float``
- `get_z(self, direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'ManimFloat'` — Returns z coordinate of the center of the :class:`~.OpenGLMobject` as ``float``
- `get_z_index_reference_point(self) -> 'Point3D'`
- `get_zenith(self) -> 'Point3D'` — Get zenith coordinates of a box bounding a 3D :class:`~.OpenGLMobject`.
- `has_points(self) -> 'bool'`
- `has_time_based_updater(self) -> 'bool'`
- `hierarchical_model_matrix(self) -> 'MatrixMN'`
- `init_colors(self) -> 'Self'` — Initializes the colors.
- `init_data(self) -> 'Self'` — Initializes the ``points``, ``bounding_box`` and ``rgbas`` attributes and groups them into self.data.
- `init_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `init_updaters(self) -> 'Self'`
- `insert(self, index: 'int', mobject: 'OpenGLMobject', update_parent: 'bool' = False) -> 'Self'` — Inserts a mobject at a specific position into self.submobjects
- `interpolate(self, mobject1: 'OpenGLMobject', mobject2: 'OpenGLMobject', alpha: 'float', path_func: 'PathFuncType' = <function interpolate at 0x713b87942020>) -> 'Self'` — Turns this :class:`~.OpenGLMobject` into an interpolation between ``mobject1``
- `invert(self, recursive: 'bool' = False) -> 'Self'` — Inverts the list of :attr:`submobjects`.
- `is_off_screen(self) -> 'bool'`
- `is_point_touching(self, point: 'Point3DLike', buff: 'float' = 0.25) -> 'bool'`
- `length_over_dim(self, dim: 'int') -> 'float'`
- `lock_data(self, keys: 'Iterable[str]') -> 'Self'` — To speed up some animations, particularly transformations,
- `lock_matching_data(self, mobject1: 'OpenGLMobject', mobject2: 'OpenGLMobject') -> 'Self'`
- `match_color(self, mobject: 'OpenGLMobject') -> 'Self'` — Match the color with the color of another :class:`~.OpenGLMobject`.
- `match_coord(self, mobject: 'OpenGLMobject', dim: 'int', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Match the coordinates with the coordinates of another :class:`~.OpenGLMobject`.
- `match_depth(self, mobject: 'OpenGLMobject', **kwargs: 'Any') -> 'Self'` — Match the depth with the depth of another :class:`~.OpenGLMobject`.
- `match_dim_size(self, mobject: 'OpenGLMobject', dim: 'int', **kwargs: 'Any') -> 'Self'` — Match the specified dimension with the dimension of another :class:`~.OpenGLMobject`.
- `match_height(self, mobject: 'OpenGLMobject', **kwargs: 'Any') -> 'Self'` — Match the height with the height of another :class:`~.OpenGLMobject`.
- `match_points(self, mobject: 'OpenGLMobject') -> 'Self'` — Edit points, positions, and submobjects to be identical
- `match_updaters(self, mobject: 'OpenGLMobject') -> 'Self'`
- `match_width(self, mobject: 'OpenGLMobject', **kwargs: 'Any') -> 'Self'` — Match the width with the width of another :class:`~.OpenGLMobject`.
- `match_x(self, mobject: 'OpenGLMobject', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Match x coord. to the x coord. of another :class:`~.OpenGLMobject`.
- `match_y(self, mobject: 'OpenGLMobject', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Match y coord. to the x coord. of another :class:`~.OpenGLMobject`.
- `match_z(self, mobject: 'OpenGLMobject', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Match z coord. to the x coord. of another :class:`~.OpenGLMobject`.
- `move_to(self, point_or_mobject: 'Point3DLike | OpenGLMobject', aligned_edge: 'Vector3DLike' = array([0., 0., 0.]), coor_mask: 'Vector3DLike' = array([1, 1, 1])) -> 'Self'` — Move center of the :class:`~.OpenGLMobject` to certain coordinate.
- `next_to(self, mobject_or_point: 'OpenGLMobject | Point3DLike', direction: 'Vector3DLike' = array([1., 0., 0.]), buff: 'float' = 0.25, aligned_edge: 'Vector3DLike' = array([0., 0., 0.]), submobject_to_align: 'OpenGLMobject | None' = None, index_of_submobject_to_align: 'int | None' = None, coor_mask: 'Vector3DLike' = array([1, 1, 1])) -> 'Self'` — Move this :class:`~.OpenGLMobject` next to another's :class:`~.OpenGLMobject` or coordinate.
- `pfp(self, alpha: 'float') -> 'Point3D'` — Abbreviation for point_from_proportion
- `point_from_proportion(self, alpha: 'float') -> 'Point3D'`
- `pointwise_become_partial(self, mobject: 'OpenGLMobject', a: 'float', b: 'float') -> 'Self'` — Set points in such a way as to become only
- `push_self_into_submobjects(self) -> 'Self'`
- `put_start_and_end_on(self, start: 'Point3DLike', end: 'Point3DLike') -> 'Self'`
- `read_data_to_shader(self, shader_data: '_ShaderData', shader_data_key: 'str', data_key: 'str') -> 'Self'`
- `refresh_bounding_box(self, recurse_down: 'bool' = False, recurse_up: 'bool' = True) -> 'Self'`
- `refresh_has_updater_status(self) -> 'Self'`
- `refresh_shader_data(self) -> 'Self'`
- `refresh_shader_wrapper_id(self) -> 'Self'`
- `remove(self, *mobjects: 'OpenGLMobject', update_parent: 'bool' = False) -> 'Self'` — Remove :attr:`submobjects`.
- `remove_updater(self, update_function: '_Updater') -> 'Self'`
- `replace(self, mobject: 'OpenGLMobject', dim_to_match: 'int' = 0, stretch: 'bool' = False) -> 'Self'`
- `replace_shader_code(self, old_code: 'str', new_code: 'str') -> 'Self'`
- `replace_submobject(self, index: 'int', new_submob: 'OpenGLMobject') -> 'Self'`
- `rescale_to_fit(self, length: 'float', dim: 'int', stretch: 'bool' = False, **kwargs: 'Any') -> 'Self'`
- `resize_points(self, new_length: 'int', resize_func: 'Callable[[Point3D_Array, int], Point3D_Array]' = <function resize_array at 0x713b8b242e80>) -> 'Self'`
- `restore(self) -> 'Self'` — Restores the state that was previously saved with :meth:`~.OpenGLMobject.save_state`.
- `resume_updating(self, recurse: 'bool' = True, call_updater: 'bool' = True) -> 'Self'`
- `reverse_points(self) -> 'Self'`
- `rotate(self, angle: 'float', axis: 'Vector3DLike' = array([0., 0., 1.]), about_point: 'Point3DLike | None' = None, **kwargs: 'Any') -> 'Self'` — Rotates the :class:`~.OpenGLMobject` about a certain point.
- `rotate_about_origin(self, angle: 'float', axis: 'Vector3DLike' = array([0., 0., 1.])) -> 'Self'`
- `save_state(self, use_deepcopy: 'bool' = False) -> 'Self'` — Save the current state (position, color & size). Can be restored with :meth:`~.OpenGLMobject.restore`.
- `scale(self, scale_factor: 'float', about_point: 'Point3DLike | None' = None, about_edge: 'Point3DLike | None' = array([0., 0., 0.]), **_kwargs: 'object') -> 'Self'` — Scale the size by a factor.
- `scale_to_fit_depth(self, depth: 'float', stretch: 'bool' = False, **kwargs: 'Any') -> 'Self'` — Scales the :class:`~.OpenGLMobject` to fit a depth while keeping width/height proportional.
- `scale_to_fit_height(self, height: 'float', stretch: 'bool' = False, **kwargs: 'Any') -> 'Self'` — Scales the :class:`~.OpenGLMobject` to fit a height while keeping width/depth proportional.
- `scale_to_fit_width(self, width: 'float', stretch: 'bool' = False, **kwargs: 'Any') -> 'Self'` — Scales the :class:`~.OpenGLMobject` to fit a width while keeping height/depth proportional.
- `set(self, **kwargs: 'object') -> 'Self'` — Sets attributes.
- `set_color(self, color: 'ParsableManimColor | Sequence[ParsableManimColor] | None', opacity: 'float | Iterable[float] | None' = None, recurse: 'bool' = True) -> 'Self'`
- `set_color_by_code(self, glsl_code: 'str') -> 'Self'` — Takes a snippet of code and inserts it into a
- `set_color_by_gradient(self, *colors: 'ParsableManimColor') -> 'Self'`
- `set_color_by_xyz_func(self, glsl_snippet: 'str', min_value: 'float' = -5.0, max_value: 'float' = 5.0, colormap: 'str' = 'viridis') -> 'Self'` — Pass in a glsl expression in terms of x, y and z which returns
- `set_coord(self, value: 'float', dim: 'int', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'`
- `set_data(self, data: 'dict[str, Any]') -> 'Self'`
- `set_default(**kwargs: 'Any') -> 'None'` — Sets the default values of keyword arguments.
- `set_depth(self, depth: 'float', stretch: 'bool' = False, **kwargs: 'Any') -> 'Self'` — Scales the :class:`~.OpenGLMobject` to fit a depth while keeping width/height proportional.
- `set_gloss(self, gloss: 'float', recurse: 'bool' = True) -> 'Self'`
- `set_height(self, height: 'float', stretch: 'bool' = False, **kwargs: 'Any') -> 'Self'` — Scales the :class:`~.OpenGLMobject` to fit a height while keeping width/depth proportional.
- `set_opacity(self, opacity: 'float | Iterable[float] | None', recurse: 'bool' = True) -> 'Self'`
- `set_points(self, points: 'Point3DLike_Array') -> 'Self'`
- `set_rgba_array(self, color: 'ParsableManimColor | Iterable[ParsableManimColor] | None' = None, opacity: 'float | Iterable[float] | None' = None, name: 'str' = 'rgbas', recurse: 'bool' = True) -> 'Self'`
- `set_rgba_array_direct(self, rgbas: 'FloatRGBA_Array', name: 'str' = 'rgbas', recurse: 'bool' = True) -> 'Self'` — Directly set rgba data from `rgbas` and optionally do the same recursively
- `set_shadow(self, shadow: 'float', recurse: 'bool' = True) -> 'Self'`
- `set_submobject_colors_by_gradient(self, *colors: 'ParsableManimColor') -> 'Self'`
- `set_uniforms(self, uniforms: 'dict[str, Any]') -> 'Self'`
- `set_width(self, width: 'float', stretch: 'bool' = False, **kwargs: 'Any') -> 'Self'` — Scales the :class:`~.OpenGLMobject` to fit a width while keeping height/depth proportional.
- `set_x(self, x: 'float', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Set x value of the center of the :class:`~.OpenGLMobject` (``int`` or ``float``)
- `set_y(self, y: 'float', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Set y value of the center of the :class:`~.OpenGLMobject` (``int`` or ``float``)
- `set_z(self, z: 'float', direction: 'Vector3DLike' = array([0., 0., 0.])) -> 'Self'` — Set z value of the center of the :class:`~.OpenGLMobject` (``int`` or ``float``)
- `shift(self, vector: 'Vector3DLike') -> 'Self'`
- `shift_onto_screen(self, **kwargs: 'Any') -> 'Self'`
- `shuffle(self, recurse: 'bool' = False) -> 'Self'` — Shuffles the order of :attr:`submobjects`
- `sort(self, point_to_num_func: 'Callable[[Point3DLike], float]' = <function OpenGLMobject.<lambda> at 0x713b879622a0>, submob_func: 'Callable[[OpenGLMobject], Any] | None' = None) -> 'Self'` — Sorts the list of :attr:`submobjects` by a function defined by ``submob_func``.
- `space_out_submobjects(self, factor: 'float' = 1.5, **kwargs: 'Any') -> 'Self'`
- `split(self) -> 'Sequence[OpenGLMobject]'`
- `stretch(self, factor: 'float', dim: 'int', **kwargs: 'Any') -> 'Self'`
- `stretch_about_point(self, factor: 'float', dim: 'int', point: 'Point3DLike') -> 'Self'`
- `stretch_to_fit_depth(self, depth: 'float', **kwargs: 'Any') -> 'Self'` — Stretches the :class:`~.OpenGLMobject` to fit a depth, not keeping width/height proportional.
- `stretch_to_fit_height(self, height: 'float', **kwargs: 'Any') -> 'Self'` — Stretches the :class:`~.OpenGLMobject` to fit a height, not keeping width/height proportional.
- `stretch_to_fit_width(self, width: 'float', **kwargs: 'Any') -> 'Self'` — Stretches the :class:`~.OpenGLMobject` to fit a width, not keeping height/depth proportional.
- `surround(self, mobject: 'OpenGLMobject', dim_to_match: 'int' = 0, stretch: 'bool' = False, buff: 'float' = 0.25) -> 'Self'`
- `suspend_updating(self, recurse: 'bool' = True) -> 'Self'`
- `throw_error_if_no_points(self) -> 'None'`
- `to_corner(self, corner: 'Vector3DLike' = array([-1., -1.,  0.]), buff: 'float' = 0.5) -> 'Self'`
- `to_edge(self, edge: 'Vector3DLike' = array([-1.,  0.,  0.]), buff: 'float' = 0.5) -> 'Self'`
- `unfix_from_frame(self) -> 'Self'`
- `unfix_orientation(self) -> 'Self'`
- `unlock_data(self) -> 'Self'`
- `update(self, dt: 'float' = 0, recurse: 'bool' = True) -> 'Self'`
- `wag(self, direction: 'Vector3DLike' = array([1., 0., 0.]), axis: 'Vector3DLike' = array([ 0., -1.,  0.]), wag_factor: 'float' = 1.0) -> 'Self'`

</details>

### `OpenGLPGroup(*pmobs, **kwargs)` ← OpenGLPMobject
> Mathematical Object: base class for objects that can be displayed on screen.

<details><summary>métodos próprios (2) · herdados: 194</summary>

- `__init__(self, *pmobs, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `fade_to(self, color, alpha, family=True) -> 'Self'`

</details>

### `OpenGLPMPoint(location=array([0., 0., 0.]), stroke_width=4.0, **kwargs)` ← OpenGLPMobject
> Mathematical Object: base class for objects that can be displayed on screen.

<details><summary>métodos próprios (2) · herdados: 194</summary>

- `__init__(self, location=array([0., 0., 0.]), stroke_width=4.0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `init_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.

</details>

### `OpenGLPMobject(stroke_width: 'float' = 2.0, color: 'ParsableManimColor' = ManimColor('#FFFF00'), render_primitive: 'int' = 0, **kwargs)` ← OpenGLMobject
> Mathematical Object: base class for objects that can be displayed on screen.

<details><summary>métodos próprios (16) · herdados: 180</summary>

- `__init__(self, stroke_width: 'float' = 2.0, color: 'ParsableManimColor' = ManimColor('#FFFF00'), render_primitive: 'int' = 0, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_points(self, points: 'Point3DLike_Array', rgbas: 'FloatRGBALike_Array | None' = None, color: 'ParsableManimColor | None' = None, opacity: 'float | None' = None) -> 'Self'` — Add points.
- `fade_to(self, color, alpha, family=True) -> 'Self'`
- `filter_out(self, condition) -> 'Self'`
- `get_array_attrs(self)`
- `get_mobject_type_class()` — Return the base class of this mobject type.
- `get_shader_data(self)`
- `ingest_submobjects(self) -> 'Self'`
- `match_colors(self, pmobject) -> 'Self'`
- `point_from_proportion(self, alpha)`
- `pointwise_become_partial(self, pmobject, a, b) -> 'Self'` — Set points in such a way as to become only
- `reset_points(self) -> 'Self'`
- `set_color_by_gradient(self, *colors) -> 'Self'`
- `set_colors_by_radial_gradient(self, center=None, radius=1, inner_color=ManimColor('#FFFFFF'), outer_color=ManimColor('#000000')) -> 'Self'`
- `sort_points(self, function=<function OpenGLPMobject.<lambda> at 0x713b8796dee0>) -> 'Self'` — function is any map from R^3 to R
- `thin_out(self, factor=5) -> 'Self'` — Removes all but every nth point for n = factor

</details>

### `OpenGLPoint(location: 'Point3DLike' = array([0., 0., 0.]), artificial_width: 'float' = 1e-06, artificial_height: 'float' = 1e-06, **kwargs: 'Any') -> 'None'` ← OpenGLMobject
> Mathematical Object: base class for objects that can be displayed on screen.

<details><summary>métodos próprios (6) · herdados: 183</summary>

- `__init__(self, location: 'Point3DLike' = array([0., 0., 0.]), artificial_width: 'float' = 1e-06, artificial_height: 'float' = 1e-06, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `get_bounding_box_point(self, *args: 'object', **kwargs: 'Any') -> 'Point3D'`
- `get_height(self) -> 'float'` — Returns the height of the mobject.
- `get_location(self) -> 'Point3D'`
- `get_width(self) -> 'float'` — Returns the width of the mobject.
- `set_location(self, new_loc: 'Point3DLike') -> 'Self'`

</details>

### `OpenGLPolygon(*vertices: 'Point3DLike', **kwargs: 'Any')` ← OpenGLVMobject
> A vectorized mobject.

<details><summary>métodos próprios (4) · herdados: 269</summary>

- `__init__(self, *vertices: 'Point3DLike', **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_vertices(self) -> 'Point3D_Array'`
- `init_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `round_corners(self, radius: 'float' = 0.5) -> 'Self'`

</details>

### `OpenGLRectangle(color: 'ParsableManimColor' = ManimColor('#FFFFFF'), width: 'float' = 4.0, height: 'float' = 2.0, **kwargs: 'Any')` ← OpenGLPolygon
> A vectorized mobject.

<details><summary>métodos próprios (1) · herdados: 272</summary>

- `__init__(self, color: 'ParsableManimColor' = ManimColor('#FFFFFF'), width: 'float' = 4.0, height: 'float' = 2.0, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLRegularPolygon(n: 'int' = 6, start_angle: 'float | None' = None, **kwargs: 'Any')` ← OpenGLPolygon
> A vectorized mobject.

<details><summary>métodos próprios (1) · herdados: 272</summary>

- `__init__(self, n: 'int' = 6, start_angle: 'float | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLRoundedRectangle(corner_radius: 'float' = 0.5, **kwargs: 'Any')` ← OpenGLRectangle
> A vectorized mobject.

<details><summary>métodos próprios (1) · herdados: 272</summary>

- `__init__(self, corner_radius: 'float' = 0.5, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLSector(outer_radius: 'float' = 1, inner_radius: 'float' = 0, **kwargs: 'Any')` ← OpenGLAnnularSector
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (1) · herdados: 290</summary>

- `__init__(self, outer_radius: 'float' = 1, inner_radius: 'float' = 0, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLSquare(side_length: 'float' = 2.0, **kwargs: 'Any')` ← OpenGLRectangle
> A vectorized mobject.

<details><summary>métodos próprios (1) · herdados: 272</summary>

- `__init__(self, side_length: 'float' = 2.0, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLSurface(uv_func=None, u_range=None, v_range=None, resolution=None, axes=None, color=ManimColor('#888888'), colorscale=None, colorscale_axis=2, opacity=1.0, gloss=0.3, shadow=0.4, prefered_creation_axis=1, epsilon=1e-05, render_primitive=4, depth_test=True, shader_folder=None, **kwargs: 'Any')` ← OpenGLMobject
> Creates a Surface.

<details><summary>métodos próprios (13) · herdados: 182</summary>

- `__init__(self, uv_func=None, u_range=None, v_range=None, resolution=None, axes=None, color=ManimColor('#888888'), colorscale=None, colorscale_axis=2, opacity=1.0, gloss=0.3, shadow=0.4, prefered_creation_axis=1, epsilon=1e-05, render_primitive=4, depth_test=True, shader_folder=None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `compute_triangle_indices(self) -> 'Self'`
- `fill_in_shader_color_info(self, shader_data)` — Fills in the shader color data when the surface
- `get_partial_points_array(self, points, a, b, resolution, axis)`
- `get_shader_data(self)` — Called by parent Mobject to calculate and return
- `get_shader_vert_indices(self)`
- `get_surface_points_and_nudged_points(self) -> 'tuple[Point3D_Array, Point3D_Array, Point3D_Array]'`
- `get_triangle_indices(self)`
- `get_unit_normals(self) -> 'Vector3D_Array'`
- `init_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `pointwise_become_partial(self, smobject, a, b, axis=None) -> 'Self'` — Set points in such a way as to become only
- `sort_faces_back_to_front(self, vect=array([0., 0., 1.])) -> 'Self'`
- `uv_func(self, u, v)`

</details>

### `OpenGLSurfaceGroup(*parametric_surfaces, resolution=None, **kwargs)` ← OpenGLSurface
> Creates a Surface.

<details><summary>métodos próprios (2) · herdados: 193</summary>

- `__init__(self, *parametric_surfaces, resolution=None, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `init_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.

</details>

### `OpenGLSurfaceMesh(uv_surface: 'OpenGLSurface', resolution: 'tuple[int, int] | None' = None, stroke_width: 'float' = 1, normal_nudge: 'float' = 0.01, depth_test: 'bool' = True, flat_stroke: 'bool' = False, **kwargs: 'Any')` ← OpenGLVGroup
> A group of vectorized mobjects.

<details><summary>métodos próprios (2) · herdados: 269</summary>

- `__init__(self, uv_surface: 'OpenGLSurface', resolution: 'tuple[int, int] | None' = None, stroke_width: 'float' = 1, normal_nudge: 'float' = 0.01, depth_test: 'bool' = True, flat_stroke: 'bool' = False, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `init_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.

</details>

### `OpenGLTangentLine(vmob: 'OpenGLVMobject', alpha: 'float', length: 'float' = 1, d_alpha: 'float' = 1e-06, **kwargs: 'Any')` ← OpenGLLine
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (1) · herdados: 297</summary>

- `__init__(self, vmob: 'OpenGLVMobject', alpha: 'float', length: 'float' = 1, d_alpha: 'float' = 1e-06, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLTexturedSurface(uv_surface: 'OpenGLSurface', image_file: 'str | Path | npt.NDArray', dark_image_file: 'str | Path' = None, image_mode: 'str | Iterable[str]' = 'RGBA', shader_folder: 'str | Path' = None, **kwargs)` ← OpenGLSurface
> Creates a Surface.

<details><summary>métodos próprios (8) · herdados: 188</summary>

- `__init__(self, uv_surface: 'OpenGLSurface', image_file: 'str | Path | npt.NDArray', dark_image_file: 'str | Path' = None, image_mode: 'str | Iterable[str]' = 'RGBA', shader_folder: 'str | Path' = None, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `fill_in_shader_color_info(self, shader_data)` — Fills in the shader color data when the surface
- `get_image_from_file(self, image_file: 'str | Path', image_mode: 'str') -> 'Image.Image'`
- `init_colors(self) -> 'Self'` — Initializes the colors.
- `init_data(self) -> 'Self'` — Initializes the ``points``, ``bounding_box`` and ``rgbas`` attributes and groups them into self.data.
- `init_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `pointwise_become_partial(self, tsmobject, a, b, axis=1) -> 'Self'` — Set points in such a way as to become only
- `set_opacity(self, opacity, recurse=True) -> 'Self'`

</details>

### `OpenGLTipableVMobject(tip_length: 'float' = 0.35, normal_vector: 'Vector3DLike' = array([0., 0., 1.]), tip_config: 'dict[str, Any]' = {}, **kwargs: 'Any')` ← OpenGLVMobject
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (18) · herdados: 268</summary>

- `__init__(self, tip_length: 'float' = 0.35, normal_vector: 'Vector3DLike' = array([0., 0., 1.]), tip_config: 'dict[str, Any]' = {}, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `add_tip(self, at_start: 'bool' = False, **kwargs: 'Any') -> 'Self'` — Adds a tip to the TipableVMobject instance, recognising
- `assign_tip_attr(self, tip: 'OpenGLArrowTip', at_start: 'bool') -> 'Self'`
- `create_tip(self, at_start: 'bool' = False, **kwargs: 'Any') -> 'OpenGLArrowTip'` — Stylises the tip, positions it spacially, and returns
- `get_default_tip_length(self) -> 'float'`
- `get_end(self) -> 'Point3D'` — Returns the point, where the stroke that surrounds the :class:`~.OpenGLMobject` ends.
- `get_first_handle(self) -> 'Point3D'`
- `get_last_handle(self) -> 'Point3D'`
- `get_length(self) -> 'float'`
- `get_start(self) -> 'Point3D'` — Returns the point, where the stroke that surrounds the :class:`~.OpenGLMobject` starts.
- `get_tip(self) -> 'OpenGLArrowTip'` — Returns the TipableVMobject instance's (first) tip,
- `get_tips(self) -> 'OpenGLVGroup'` — Returns a VGroup (collection of VMobjects) containing
- `get_unpositioned_tip(self, **kwargs: 'Any') -> 'OpenGLArrowTip'` — Returns a tip that has been stylistically configured,
- `has_start_tip(self) -> 'bool'`
- `has_tip(self) -> 'bool'`
- `pop_tips(self) -> 'OpenGLVGroup'`
- `position_tip(self, tip: 'OpenGLArrowTip', at_start: 'bool' = False) -> 'OpenGLArrowTip'`
- `reset_endpoints_based_on_tip(self, tip: 'OpenGLArrowTip', at_start: 'bool') -> 'Self'`

</details>

### `OpenGLTriangle(**kwargs: 'Any')` ← OpenGLRegularPolygon
> A vectorized mobject.

<details><summary>métodos próprios (1) · herdados: 272</summary>

- `__init__(self, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLVGroup(*vmobjects: 'OpenGLVMobject', **kwargs: 'Any')` ← OpenGLVMobject
> A group of vectorized mobjects.

<details><summary>métodos próprios (2) · herdados: 269</summary>

- `__init__(self, *vmobjects: 'OpenGLVMobject', **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `add(self, *vmobjects: 'OpenGLVMobject') -> 'Self'` — Checks if all passed elements are an instance of OpenGLVMobject and then add them to submobjects

</details>

### `OpenGLVMobject(fill_color: 'ParsableManimColor | None' = None, fill_opacity: 'float' = 0.0, stroke_color: 'ParsableManimColor | None' = None, stroke_opacity: 'float' = 1.0, stroke_width: 'float' = 4, draw_stroke_behind_fill: 'bool' = False, pre_function_handle_to_anchor_scale_factor: 'float' = 0.01, make_smooth_after_applying_functions: 'float' = False, background_image_file: 'str | None' = None, tolerance_for_point_equality: 'float' = 1e-08, n_points_per_curve: 'int' = 3, long_lines: 'bool' = False, should_subdivide_sharp_curves: 'bool' = False, should_remove_null_curves: 'bool' = False, joint_type: 'LineJointType | None' = None, flat_stroke: 'bool' = True, render_primitive=4, triangulation_locked: 'bool' = False, **kwargs)` ← OpenGLMobject
> A vectorized mobject.

<details><summary>métodos próprios (106) · herdados: 165</summary>

- `__init__(self, fill_color: 'ParsableManimColor | None' = None, fill_opacity: 'float' = 0.0, stroke_color: 'ParsableManimColor | None' = None, stroke_opacity: 'float' = 1.0, stroke_width: 'float' = 4, draw_stroke_behind_fill: 'bool' = False, pre_function_handle_to_anchor_scale_factor: 'float' = 0.01, make_smooth_after_applying_functions: 'float' = False, background_image_file: 'str | None' = None, tolerance_for_point_equality: 'float' = 1e-08, n_points_per_curve: 'int' = 3, long_lines: 'bool' = False, should_subdivide_sharp_curves: 'bool' = False, should_remove_null_curves: 'bool' = False, joint_type: 'LineJointType | None' = None, flat_stroke: 'bool' = True, render_primitive=4, triangulation_locked: 'bool' = False, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_cubic_bezier_curve(self, anchor1: 'Point3DLike', handle1: 'Point3DLike', handle2: 'Point3DLike', anchor2: 'Point3DLike') -> 'Self'`
- `add_cubic_bezier_curve_to(self, handle1, handle2, anchor) -> 'Self'` — Add cubic bezier curve to the path.
- `add_line_to(self, point: 'Sequence[float]') -> 'Self'` — Add a straight line from the last point of OpenGLVMobject to the given point.
- `add_points_as_corners(self, points) -> 'Self'`
- `add_quadratic_bezier_curve_to(self, handle, anchor) -> 'Self'`
- `add_smooth_cubic_curve_to(self, handle, point) -> 'Self'`
- `add_smooth_curve_to(self, point) -> 'Self'`
- `add_subpath(self, points) -> 'Self'`
- `align_points(self, vmobject) -> 'Self'`
- `append_vectorized_mobject(self, vectorized_mobject) -> 'Self'`
- `apply_function(self, function, make_smooth=False, **kwargs) -> 'Self'`
- `apply_points_function(self, *args, **kwargs) -> 'Self'`
- `change_anchor_mode(self, mode) -> 'Self'` — Changes the anchor mode of the bezier curves. This will modify the handles.
- `close_path(self) -> 'Self'`
- `consider_points_equals(self, p0, p1)`
- `fade(self, darkness=0.5, recurse=True) -> 'Self'`
- `flip(self, *args, **kwargs) -> 'Self'` — Flips/Mirrors an mobject about its center.
- `force_direction(self, target_direction: 'str') -> 'Self'` — Makes sure that points are either directed clockwise or
- `get_anchors(self) -> 'Iterable[np.ndarray]'` — Returns the anchors of the curves forming the OpenGLVMobject.
- `get_anchors_and_handles(self) -> 'Iterable[np.ndarray]'` — Returns anchors1, handles, anchors2,
- `get_arc_length(self, sample_points_per_curve: 'int | None' = None) -> 'float'` — Return the approximated length of the whole curve.
- `get_area_vector(self)`
- `get_bezier_tuples(self)`
- `get_bezier_tuples_from_points(self, points)`
- `get_color(self)`
- `get_colors(self)`
- `get_curve_functions(self) -> 'Iterable[Callable[[float], np.ndarray]]'` — Gets the functions for the curves of the mobject.
- `get_curve_functions_with_lengths(self, **kwargs) -> 'Iterable[tuple[Callable[[float], np.ndarray], float]]'` — Gets the functions and lengths of the curves for the mobject.
- `get_direction(self)` — Uses :func:`~.space_ops.shoelace_direction` to calculate the direction.
- `get_end_anchors(self) -> 'np.ndarray'` — Return the starting anchors of the bezier curves.
- `get_fill_color(self)` — If there are multiple colors (for gradient)
- `get_fill_colors(self)`
- `get_fill_opacities(self)`
- `get_fill_opacity(self)` — If there are multiple opacities, this returns the
- `get_fill_shader_data(self)`
- `get_fill_shader_vert_indices(self)`
- `get_fill_shader_wrapper(self)`
- `get_fill_uniforms(self)`
- `get_flat_stroke(self)`
- `get_group_class(self)`
- `get_last_point(self)`
- `get_mobject_type_class()` — Return the base class of this mobject type.
- `get_nth_curve_function(self, n: 'int') -> 'Callable[[float], np.ndarray]'` — Returns the expression of the nth curve.
- `get_nth_curve_function_with_length(self, n: 'int', sample_points: 'int | None' = None) -> 'tuple[Callable[[float], np.ndarray], float]'` — Returns the expression of the nth curve along with its (approximate) length.
- `get_nth_curve_length(self, n: 'int', sample_points: 'int | None' = None) -> 'float'` — Returns the (approximate) length of the nth curve.
- `get_nth_curve_length_pieces(self, n: 'int', sample_points: 'int | None' = None) -> 'np.ndarray'` — Returns the array of short line lengths used for length approximation.
- `get_nth_curve_points(self, n: 'int') -> 'np.ndarray'` — Returns the points defining the nth curve of the vmobject.
- `get_num_curves(self) -> 'int'` — Returns the number of curves of the vmobject.
- `get_opacity(self)`
- `get_points_without_null_curves(self, atol=1e-09)`
- `get_reflection_of_last_handle(self)`
- `get_shader_wrapper_list(self)`
- `get_start_anchors(self) -> 'np.ndarray'` — Returns the start anchors of the bezier curves.
- `get_stroke_color(self)`
- `get_stroke_colors(self)`
- `get_stroke_opacities(self)`
- `get_stroke_opacity(self)`
- `get_stroke_shader_data(self)`
- `get_stroke_shader_wrapper(self)`
- `get_stroke_uniforms(self)`
- `get_stroke_width(self)`
- `get_stroke_widths(self)`
- `get_style(self)`
- `get_subcurve(self, a: 'float', b: 'float') -> 'OpenGLVMobject'` — Returns the subcurve of the OpenGLVMobject between the interval [a, b].
- `get_subpaths(self)` — Returns subpaths formed by the curves of the OpenGLVMobject.
- `get_subpaths_from_points(self, points)`
- `get_triangulation(self, normal_vector=None)`
- `get_unit_normal(self, recompute=False)`
- `has_fill(self)`
- `has_new_path_started(self)`
- `has_stroke(self)`
- `init_colors(self) -> 'Self'` — Initializes the colors.
- `init_data(self) -> 'Self'` — Initializes the ``points``, ``bounding_box`` and ``rgbas`` attributes and groups them into self.data.
- `init_shader_data(self) -> 'Self'`
- `insert_n_curves(self, n: 'int', recurse=True) -> 'Self'` — Inserts n curves to the bezier curves of the vmobject.
- `insert_n_curves_to_point_list(self, n: 'int', points: 'np.ndarray') -> 'np.ndarray'` — Given an array of k points defining a bezier curves
- `interpolate(self, mobject1, mobject2, alpha, *args, **kwargs) -> 'Self'` — Turns this :class:`~.OpenGLMobject` into an interpolation between ``mobject1``
- `is_closed(self)`
- `make_approximately_smooth(self) -> 'Self'` — Unlike make_smooth, this will not change the number of
- `make_jagged(self) -> 'Self'`
- `make_smooth(self) -> 'Self'` — This will double the number of points in the mobject,
- `match_style(self, vmobject, recurse=True) -> 'Self'`
- `point_from_proportion(self, alpha: 'float') -> 'Point3D'` — Gets the point at a proportion along the path of the :class:`OpenGLVMobject`.
- `pointwise_become_partial(self, vmobject: 'OpenGLVMobject', a: 'float', b: 'float', remap: 'bool' = True) -> 'Self'` — Given two bounds a and b, transforms the points of the self vmobject into the points of the vmobject
- `proportion_from_point(self, point: 'Point3DLike') -> 'float'` — Returns the proportion along the path of the :class:`OpenGLVMobject`
- `refresh_shader_data(self) -> 'Self'`
- `refresh_shader_wrapper_id(self) -> 'Self'`
- `refresh_triangulation(self) -> 'Self'`
- `refresh_unit_normal(self) -> 'Self'`
- `reverse_direction(self) -> 'Self'` — Reverts the point direction by inverting the point order.
- `set_anchors_and_handles(self, anchors1, handles, anchors2) -> 'Self'`
- `set_color(self, color, opacity=None, recurse=True) -> 'Self'`
- `set_data(self, data) -> 'Self'`
- `set_fill(self, color: 'ParsableManimColor | None' = None, opacity: 'float | None' = None, recurse: 'bool' = True) -> 'Self'` — Set the fill color and fill opacity of a :class:`OpenGLVMobject`.
- `set_flat_stroke(self, flat_stroke=True, recurse=True) -> 'Self'`
- `set_opacity(self, opacity, recurse=True) -> 'Self'`
- `set_points(self, points) -> 'Self'`
- `set_points_as_corners(self, points: 'Point3DLike_Array') -> 'Self'` — Given an array of points, set them as corner of the vmobject.
- `set_points_smoothly(self, points: 'Point3DLike_Array', true_smooth: 'bool' = False) -> 'Self'`
- `set_stroke(self, color=None, width=None, opacity=None, background=None, recurse=True) -> 'Self'`
- `set_style(self, fill_color=None, fill_opacity=None, fill_rgba=None, stroke_color=None, stroke_opacity=None, stroke_rgba=None, stroke_width=None, gloss=None, shadow=None, recurse=True) -> 'Self'`
- `start_new_path(self, point) -> 'Self'`
- `subdivide_sharp_curves(self, angle_threshold=0.5235987755982988, recurse=True) -> 'Self'`
- `update_fill_shader_wrapper(self) -> 'Self'`
- `update_stroke_shader_wrapper(self) -> 'Self'`

</details>

### `OpenGLVector(direction: 'Vector2DLike | Vector3DLike' = array([1., 0., 0.]), buff: 'float' = 0, **kwargs: 'Any')` ← OpenGLArrow
> Meant for shared functionality between Arc and Line.

<details><summary>métodos próprios (1) · herdados: 299</summary>

- `__init__(self, direction: 'Vector2DLike | Vector3DLike' = array([1., 0., 0.]), buff: 'float' = 0, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `OpenGLVectorizedPoint(location=array([0., 0., 0.]), color=ManimColor('#000000'), fill_opacity=0, stroke_width=0, artificial_width=0.01, artificial_height=0.01, **kwargs)` ← OpenGLPoint, OpenGLVMobject
> A vectorized mobject.

<details><summary>métodos próprios (1) · herdados: 272</summary>

- `__init__(self, location=array([0., 0., 0.]), color=ManimColor('#000000'), fill_opacity=0, stroke_width=0, artificial_width=0.01, artificial_height=0.01, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `TrueDot(center: 'Point3DLike' = array([0., 0., 0.]), stroke_width: 'float' = 2.0, **kwargs: 'Any')` ← DotCloud
> Mathematical Object: base class for objects that can be displayed on screen.

<details><summary>métodos próprios (1) · herdados: 196</summary>

- `__init__(self, center: 'Point3DLike' = array([0., 0., 0.]), stroke_width: 'float' = 2.0, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

- `BLACK` = `ManimColor('#000000')`
- `BLACK` = `ManimColor('#000000')`
- `BLACK` = `ManimColor('#000000')`
- `BLACK` = `ManimColor('#000000')`
- `BLUE` = `ManimColor('#58C4DD')`
- `BLUE` = `ManimColor('#58C4DD')`
- `BLUE_A` = `ManimColor('#C7E9F1')`
- `BLUE_A` = `ManimColor('#C7E9F1')`
- `BLUE_B` = `ManimColor('#9CDCEB')`
- `BLUE_B` = `ManimColor('#9CDCEB')`
- `BLUE_C` = `ManimColor('#58C4DD')`
- `BLUE_C` = `ManimColor('#58C4DD')`
- `BLUE_D` = `ManimColor('#29ABCA')`
- `BLUE_D` = `ManimColor('#29ABCA')`
- `BLUE_E` = `ManimColor('#236B8E')`
- `BLUE_E` = `ManimColor('#236B8E')`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `DARKER_GRAY` = `ManimColor('#222222')`
- `DARKER_GRAY` = `ManimColor('#222222')`
- `DARKER_GREY` = `ManimColor('#222222')`
- `DARKER_GREY` = `ManimColor('#222222')`
- `DARK_BLUE` = `ManimColor('#236B8E')`
- `DARK_BLUE` = `ManimColor('#236B8E')`
- `DARK_BROWN` = `ManimColor('#8B4513')`
- `DARK_BROWN` = `ManimColor('#8B4513')`
- `DARK_GRAY` = `ManimColor('#444444')`
- `DARK_GRAY` = `ManimColor('#444444')`
- `DARK_GREY` = `ManimColor('#444444')`
- `DARK_GREY` = `ManimColor('#444444')`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_WIDTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `GOLD` = `ManimColor('#F0AC5F')`
- `GOLD` = `ManimColor('#F0AC5F')`
- `GOLD_A` = `ManimColor('#F7C797')`
- `GOLD_A` = `ManimColor('#F7C797')`
- `GOLD_B` = `ManimColor('#F9B775')`
- `GOLD_B` = `ManimColor('#F9B775')`
- `GOLD_C` = `ManimColor('#F0AC5F')`
- `GOLD_C` = `ManimColor('#F0AC5F')`
- `GOLD_D` = `ManimColor('#E1A158')`
- `GOLD_D` = `ManimColor('#E1A158')`
- `GOLD_E` = `ManimColor('#C78D46')`
- `GOLD_E` = `ManimColor('#C78D46')`
- `GRAY` = `ManimColor('#888888')`
- `GRAY` = `ManimColor('#888888')`
- `GRAY_A` = `ManimColor('#DDDDDD')`
- `GRAY_A` = `ManimColor('#DDDDDD')`
- `GRAY_B` = `ManimColor('#BBBBBB')`
- `GRAY_B` = `ManimColor('#BBBBBB')`
- `GRAY_BROWN` = `ManimColor('#736357')`
- `GRAY_BROWN` = `ManimColor('#736357')`
- `GRAY_C` = `ManimColor('#888888')`
- `GRAY_C` = `ManimColor('#888888')`
- `GRAY_D` = `ManimColor('#444444')`
- `GRAY_D` = `ManimColor('#444444')`
- `GRAY_E` = `ManimColor('#222222')`
- `GRAY_E` = `ManimColor('#222222')`
- `GREEN` = `ManimColor('#83C167')`
- `GREEN` = `ManimColor('#83C167')`
- `GREEN_A` = `ManimColor('#C9E2AE')`
- `GREEN_A` = `ManimColor('#C9E2AE')`
- `GREEN_B` = `ManimColor('#A6CF8C')`
- `GREEN_B` = `ManimColor('#A6CF8C')`
- `GREEN_C` = `ManimColor('#83C167')`
- `GREEN_C` = `ManimColor('#83C167')`
- `GREEN_D` = `ManimColor('#77B05D')`
- `GREEN_D` = `ManimColor('#77B05D')`
- `GREEN_E` = `ManimColor('#699C52')`
- `GREEN_E` = `ManimColor('#699C52')`
- `GREY` = `ManimColor('#888888')`
- `GREY` = `ManimColor('#888888')`
- `GREY_A` = `ManimColor('#DDDDDD')`
- `GREY_A` = `ManimColor('#DDDDDD')`
- `GREY_B` = `ManimColor('#BBBBBB')`
- `GREY_B` = `ManimColor('#BBBBBB')`
- `GREY_BROWN` = `ManimColor('#736357')`
- `GREY_BROWN` = `ManimColor('#736357')`
- `GREY_C` = `ManimColor('#888888')`
- `GREY_C` = `ManimColor('#888888')`
- `GREY_D` = `ManimColor('#444444')`
- `GREY_D` = `ManimColor('#444444')`
- `GREY_E` = `ManimColor('#222222')`
- `GREY_E` = `ManimColor('#222222')`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `LIGHTER_GRAY` = `ManimColor('#DDDDDD')`
- `LIGHTER_GRAY` = `ManimColor('#DDDDDD')`
- `LIGHTER_GREY` = `ManimColor('#DDDDDD')`
- `LIGHTER_GREY` = `ManimColor('#DDDDDD')`
- `LIGHT_BROWN` = `ManimColor('#CD853F')`
- `LIGHT_BROWN` = `ManimColor('#CD853F')`
- `LIGHT_GRAY` = `ManimColor('#BBBBBB')`
- `LIGHT_GRAY` = `ManimColor('#BBBBBB')`
- `LIGHT_GREY` = `ManimColor('#BBBBBB')`
- `LIGHT_GREY` = `ManimColor('#BBBBBB')`
- `LIGHT_PINK` = `ManimColor('#DC75CD')`
- `LIGHT_PINK` = `ManimColor('#DC75CD')`
- `LOGO_BLACK` = `ManimColor('#343434')`
- `LOGO_BLACK` = `ManimColor('#343434')`
- `LOGO_BLUE` = `ManimColor('#525893')`
- `LOGO_BLUE` = `ManimColor('#525893')`
- `LOGO_GREEN` = `ManimColor('#87C2A5')`
- `LOGO_GREEN` = `ManimColor('#87C2A5')`
- `LOGO_RED` = `ManimColor('#E07A5F')`
- `LOGO_RED` = `ManimColor('#E07A5F')`
- `LOGO_WHITE` = `ManimColor('#ECE7E2')`
- `LOGO_WHITE` = `ManimColor('#ECE7E2')`
- `MAROON` = `ManimColor('#C55F73')`
- `MAROON` = `ManimColor('#C55F73')`
- `MAROON_A` = `ManimColor('#ECABC1')`
- `MAROON_A` = `ManimColor('#ECABC1')`
- `MAROON_B` = `ManimColor('#EC92AB')`
- `MAROON_B` = `ManimColor('#EC92AB')`
- `MAROON_C` = `ManimColor('#C55F73')`
- `MAROON_C` = `ManimColor('#C55F73')`
- `MAROON_D` = `ManimColor('#A24D61')`
- `MAROON_D` = `ManimColor('#A24D61')`
- `MAROON_E` = `ManimColor('#94424F')`
- `MAROON_E` = `ManimColor('#94424F')`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `ORANGE` = `ManimColor('#FF862F')`
- `ORANGE` = `ManimColor('#FF862F')`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PINK` = `ManimColor('#D147BD')`
- `PINK` = `ManimColor('#D147BD')`
- `PURE_BLUE` = `ManimColor('#0000FF')`
- `PURE_BLUE` = `ManimColor('#0000FF')`
- `PURE_CYAN` = `ManimColor('#00FFFF')`
- `PURE_CYAN` = `ManimColor('#00FFFF')`
- `PURE_GREEN` = `ManimColor('#00FF00')`
- `PURE_GREEN` = `ManimColor('#00FF00')`
- `PURE_MAGENTA` = `ManimColor('#FF00FF')`
- `PURE_MAGENTA` = `ManimColor('#FF00FF')`
- `PURE_RED` = `ManimColor('#FF0000')`
- `PURE_RED` = `ManimColor('#FF0000')`
- `PURE_YELLOW` = `ManimColor('#FFFF00')`
- `PURE_YELLOW` = `ManimColor('#FFFF00')`
- `PURE_YELLOW` = `ManimColor('#FFFF00')`
- `PURE_YELLOW` = `ManimColor('#FFFF00')`
- `PURPLE` = `ManimColor('#9A72AC')`
- `PURPLE` = `ManimColor('#9A72AC')`
- `PURPLE_A` = `ManimColor('#CAA3E8')`
- `PURPLE_A` = `ManimColor('#CAA3E8')`
- `PURPLE_B` = `ManimColor('#B189C6')`
- `PURPLE_B` = `ManimColor('#B189C6')`
- `PURPLE_C` = `ManimColor('#9A72AC')`
- `PURPLE_C` = `ManimColor('#9A72AC')`
- `PURPLE_D` = `ManimColor('#715582')`
- `PURPLE_D` = `ManimColor('#715582')`
- `PURPLE_E` = `ManimColor('#644172')`
- `PURPLE_E` = `ManimColor('#644172')`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `RED` = `ManimColor('#FC6255')`
- `RED` = `ManimColor('#FC6255')`
- `RED_A` = `ManimColor('#F7A1A3')`
- `RED_A` = `ManimColor('#F7A1A3')`
- `RED_B` = `ManimColor('#FF8080')`
- `RED_B` = `ManimColor('#FF8080')`
- `RED_C` = `ManimColor('#FC6255')`
- `RED_C` = `ManimColor('#FC6255')`
- `RED_D` = `ManimColor('#E65A4C')`
- `RED_D` = `ManimColor('#E65A4C')`
- `RED_E` = `ManimColor('#CF5044')`
- `RED_E` = `ManimColor('#CF5044')`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `START_X` = `30`
- `START_X` = `30`
- `START_X` = `30`
- `START_X` = `30`
- `START_X` = `30`
- `START_Y` = `20`
- `START_Y` = `20`
- `START_Y` = `20`
- `START_Y` = `20`
- `START_Y` = `20`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TEAL` = `ManimColor('#5CD0B3')`
- `TEAL` = `ManimColor('#5CD0B3')`
- `TEAL_A` = `ManimColor('#ACEAD7')`
- `TEAL_A` = `ManimColor('#ACEAD7')`
- `TEAL_B` = `ManimColor('#76DDC0')`
- `TEAL_B` = `ManimColor('#76DDC0')`
- `TEAL_C` = `ManimColor('#5CD0B3')`
- `TEAL_C` = `ManimColor('#5CD0B3')`
- `TEAL_D` = `ManimColor('#55C1A7')`
- `TEAL_D` = `ManimColor('#55C1A7')`
- `TEAL_E` = `ManimColor('#49A88F')`
- `TEAL_E` = `ManimColor('#49A88F')`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `YELLOW` = `ManimColor('#F7D96F')`
- `YELLOW` = `ManimColor('#F7D96F')`
- `YELLOW_A` = `ManimColor('#FFF1B6')`
- `YELLOW_A` = `ManimColor('#FFF1B6')`
- `YELLOW_B` = `ManimColor('#FFEA94')`
- `YELLOW_B` = `ManimColor('#FFEA94')`
- `YELLOW_C` = `ManimColor('#F7D96F')`
- `YELLOW_C` = `ManimColor('#F7D96F')`
- `YELLOW_D` = `ManimColor('#F4D345')`
- `YELLOW_D` = `ManimColor('#F4D345')`
- `YELLOW_E` = `ManimColor('#E8C11C')`
- `YELLOW_E` = `ManimColor('#E8C11C')`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- **`affects_shader_info_id(func: 'Callable[[OpenGLMobject], OpenGLMobject]') -> 'Callable[[OpenGLMobject], OpenGLMobject]'`**
- **`override_animate(method: 'types.FunctionType') -> '_OverrideAnimateDecorator'`** — Decorator for overriding method animations.
- **`triggers_refreshed_triangulation(func)`**

## mobject/svg

### `ArcBrace(arc: 'Arc | None' = None, direction: 'Vector3DLike' = array([1., 0., 0.]), **kwargs: 'Any')` ← Brace
> Creates a :class:`~Brace` that wraps around an :class:`~.Arc`.

<details><summary>métodos próprios (1) · herdados: 248</summary>

- `__init__(self, arc: 'Arc | None' = None, direction: 'Vector3DLike' = array([1., 0., 0.]), **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Brace(mobject: 'Mobject', direction: 'Vector3DLike' = array([ 0., -1.,  0.]), buff: 'float' = 0.2, sharpness: 'float' = 2, stroke_width: 'float' = 0, fill_opacity: 'float' = 1.0, background_stroke_width: 'float' = 0, background_stroke_color: 'ParsableManimColor' = ManimColor('#000000'), **kwargs: 'Any')` ← VMobjectFromSVGPath
> Takes a mobject and draws a brace adjacent to it.

<details><summary>métodos próprios (6) · herdados: 243</summary>

- `__init__(self, mobject: 'Mobject', direction: 'Vector3DLike' = array([ 0., -1.,  0.]), buff: 'float' = 0.2, sharpness: 'float' = 2, stroke_width: 'float' = 0, fill_opacity: 'float' = 1.0, background_stroke_width: 'float' = 0, background_stroke_color: 'ParsableManimColor' = ManimColor('#000000'), **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_direction(self) -> 'Vector3D'` — Returns the direction from the center to the brace tip.
- `get_tex(self, *tex: 'str', **kwargs: 'Any') -> 'MathTex'` — Places the tex at the brace tip.
- `get_text(self, *text: 'str', **kwargs: 'Any') -> 'Tex'` — Places the text at the brace tip.
- `get_tip(self) -> 'Point3D'` — Returns the point at the brace tip.
- `put_at_tip(self, mob: 'Mobject', use_next_to: 'bool' = True, **kwargs: 'Any') -> 'Self'` — Puts the given mobject at the brace tip.

</details>

### `BraceBetweenPoints(point_1: 'Point3DLike', point_2: 'Point3DLike', direction: 'Vector3DLike' = array([0., 0., 0.]), **kwargs: 'Any')` ← Brace
> Similar to Brace, but instead of taking a mobject it uses 2

<details><summary>métodos próprios (1) · herdados: 248</summary>

- `__init__(self, point_1: 'Point3DLike', point_2: 'Point3DLike', direction: 'Vector3DLike' = array([0., 0., 0.]), **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `BraceLabel(obj: 'Mobject', text: 'str', brace_direction: 'Vector3DLike' = array([ 0., -1.,  0.]), label_constructor: 'type[SingleStringMathTex | Text]' = <class 'manim.mobject.text.tex_mobject.MathTex'>, font_size: 'float' = 48, buff: 'float' = 0.2, brace_config: 'dict[str, Any] | None' = None, **kwargs: 'Any')` ← VMobject
> Create a brace with a label attached.

<details><summary>métodos próprios (5) · herdados: 242</summary>

- `__init__(self, obj: 'Mobject', text: 'str', brace_direction: 'Vector3DLike' = array([ 0., -1.,  0.]), label_constructor: 'type[SingleStringMathTex | Text]' = <class 'manim.mobject.text.tex_mobject.MathTex'>, font_size: 'float' = 48, buff: 'float' = 0.2, brace_config: 'dict[str, Any] | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `change_brace_label(self, obj: 'Mobject', *text: 'str', **kwargs: 'Any') -> 'Self'`
- `change_label(self, *text: 'str', **kwargs: 'Any') -> 'Self'`
- `creation_anim(self, label_anim: 'type[Animation]' = <class 'manim.animation.fading.FadeIn'>, brace_anim: 'type[Animation]' = <class 'manim.animation.growing.GrowFromCenter'>) -> 'AnimationGroup'`
- `shift_brace(self, obj: 'Mobject', **kwargs: 'Any') -> 'Self'`

</details>

### `BraceText(obj: 'Mobject', text: 'str', label_constructor: 'type[SingleStringMathTex | Text]' = <class 'manim.mobject.text.text_mobject.Text'>, **kwargs: 'Any')` ← BraceLabel
> Create a brace with a text label attached.

<details><summary>métodos próprios (1) · herdados: 246</summary>

- `__init__(self, obj: 'Mobject', text: 'str', label_constructor: 'type[SingleStringMathTex | Text]' = <class 'manim.mobject.text.text_mobject.Text'>, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `SVGMobject(file_name: 'str | os.PathLike | None' = None, should_center: 'bool' = True, height: 'float | None' = 2, width: 'float | None' = None, color: 'ParsableManimColor | None' = None, opacity: 'float | None' = None, fill_color: 'ParsableManimColor | None' = None, fill_opacity: 'float | None' = None, stroke_color: 'ParsableManimColor | None' = None, stroke_opacity: 'float | None' = None, stroke_width: 'float | None' = None, svg_default: 'dict | None' = None, path_string_config: 'dict | None' = None, use_svg_cache: 'bool' = True, **kwargs: 'Any')` ← VMobject
> A vectorized mobject created from importing an SVG file.

<details><summary>métodos próprios (18) · herdados: 242</summary>

- `__init__(self, file_name: 'str | os.PathLike | None' = None, should_center: 'bool' = True, height: 'float | None' = 2, width: 'float | None' = None, color: 'ParsableManimColor | None' = None, opacity: 'float | None' = None, fill_color: 'ParsableManimColor | None' = None, fill_opacity: 'float | None' = None, stroke_color: 'ParsableManimColor | None' = None, stroke_opacity: 'float | None' = None, stroke_width: 'float | None' = None, svg_default: 'dict | None' = None, path_string_config: 'dict | None' = None, use_svg_cache: 'bool' = True, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `apply_style_to_mobject(mob: 'VMobject', shape: 'se.GraphicObject') -> 'VMobject'` — Apply SVG style information to the converted mobject.
- `ellipse_to_mobject(ellipse: 'se.Ellipse | se.Circle') -> 'Circle'` — Convert an ellipse or circle element to a vectorized mobject.
- `generate_config_style_dict(self) -> 'dict[str, str]'` — Generate a dictionary holding the default style information.
- `generate_mobject(self) -> 'Self'` — Parse the SVG and translate its elements to submobjects.
- `get_file_path(self) -> 'Path'` — Search for an existing file based on the specified file name.
- `get_mob_from_shape_element(self, shape: 'se.SVGElement') -> 'VMobject | None'`
- `get_mobjects_from(self, svg: 'se.SVG') -> 'tuple[list[VMobject], dict[str, VGroup]]'` — Convert the elements of the SVG to a list of mobjects.
- `handle_transform(mob: 'VMobject', matrix: 'se.Matrix') -> 'VMobject'` — Apply SVG transformations to the converted mobject.
- `init_svg_mobject(self, use_svg_cache: 'bool') -> 'Self'` — Checks whether the SVG has already been imported and
- `line_to_mobject(line: 'se.Line') -> 'Line'` — Convert a line element to a vectorized mobject.
- `modify_xml_tree(self, element_tree: 'ET.ElementTree') -> 'ET.ElementTree'` — Modifies the SVG element tree to include default
- `move_into_position(self) -> 'Self'` — Scale and move the generated mobject into position.
- `path_to_mobject(self, path: 'se.Path') -> 'VMobjectFromSVGPath'` — Convert a path element to a vectorized mobject.
- `polygon_to_mobject(polygon: 'se.Polygon') -> 'Polygon'` — Convert a polygon element to a vectorized mobject.
- `polyline_to_mobject(self, polyline: 'se.Polyline') -> 'VMobject'` — Convert a polyline element to a vectorized mobject.
- `rect_to_mobject(rect: 'se.Rect') -> 'Rectangle'` — Convert a rectangle element to a vectorized mobject.
- `text_to_mobject(text: 'se.Text') -> 'VMobject'` — Convert a text element to a vectorized mobject.

</details>

### `VMobjectFromSVGPath(path_obj: 'se.Path', long_lines: 'bool' = False, should_subdivide_sharp_curves: 'bool' = False, should_remove_null_curves: 'bool' = False, **kwargs: 'Any')` ← VMobject
> A vectorized mobject representing an SVG path.

<details><summary>métodos próprios (4) · herdados: 241</summary>

- `__init__(self, path_obj: 'se.Path', long_lines: 'bool' = False, should_subdivide_sharp_curves: 'bool' = False, should_remove_null_curves: 'bool' = False, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `generate_points(self) -> 'Self'` — Initializes :attr:`points` and therefore the shape.
- `handle_commands(self) -> 'Self'`
- `init_points(self) -> 'Self'`

</details>

- `BLACK` = `ManimColor('#000000')`
- `BOLD` = `'BOLD'`
- `BOOK` = `'BOOK'`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CTRL_VALUE` = `65507`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `HEAVY` = `'HEAVY'`
- `IN` = `array([ 0.,  0., -1.])`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LIGHT` = `'LIGHT'`
- `MEDIUM` = `'MEDIUM'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OBLIQUE` = `'OBLIQUE'`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SHIFT_VALUE` = `65505`
- `SMALL_BUFF` = `0.1`
- `START_X` = `30`
- `START_Y` = `20`
- `SVG_HASH_TO_MOB_MAP` = `{}`
- `TAU` = `6.283185307179586`
- `THIN` = `'THIN'`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Z_AXIS` = `array([0., 0., 1.])`

## mobject/table

### `DecimalTable(table: 'Iterable[Iterable[float | str]]', element_to_mobject: 'Callable[[float | str], VMobject] | type[VMobject]' = <class 'manim.mobject.text.numbers.DecimalNumber'>, element_to_mobject_config: 'dict' = {'num_decimal_places': 1}, **kwargs: 'Any')` ← Table
> A specialized :class:`~.Table` mobject for use with :class:`~.DecimalNumber` to display decimal entries.

<details><summary>métodos próprios (1) · herdados: 258</summary>

- `__init__(self, table: 'Iterable[Iterable[float | str]]', element_to_mobject: 'Callable[[float | str], VMobject] | type[VMobject]' = <class 'manim.mobject.text.numbers.DecimalNumber'>, element_to_mobject_config: 'dict' = {'num_decimal_places': 1}, **kwargs: 'Any')` — Special case of :class:`~.Table` with ``element_to_mobject`` set to :class:`~.DecimalNumber`.

</details>

### `IntegerTable(table: 'Iterable[Iterable[float | str]]', element_to_mobject: 'Callable[[float | str], VMobject] | type[VMobject]' = <class 'manim.mobject.text.numbers.Integer'>, **kwargs: 'Any')` ← Table
> A specialized :class:`~.Table` mobject for use with :class:`~.Integer`.

<details><summary>métodos próprios (1) · herdados: 258</summary>

- `__init__(self, table: 'Iterable[Iterable[float | str]]', element_to_mobject: 'Callable[[float | str], VMobject] | type[VMobject]' = <class 'manim.mobject.text.numbers.Integer'>, **kwargs: 'Any')` — Special case of :class:`~.Table` with `element_to_mobject` set to :class:`~.Integer`.

</details>

### `MathTable(table: 'Iterable[Iterable[float | str]]', element_to_mobject: 'Callable[[float | str], VMobject] | type[VMobject]' = <class 'manim.mobject.text.tex_mobject.MathTex'>, **kwargs: 'Any')` ← Table
> A specialized :class:`~.Table` mobject for use with LaTeX.

<details><summary>métodos próprios (1) · herdados: 258</summary>

- `__init__(self, table: 'Iterable[Iterable[float | str]]', element_to_mobject: 'Callable[[float | str], VMobject] | type[VMobject]' = <class 'manim.mobject.text.tex_mobject.MathTex'>, **kwargs: 'Any')` — Special case of :class:`~.Table` with `element_to_mobject` set to :class:`~.MathTex`.

</details>

### `MobjectTable(table: 'Iterable[Iterable[VMobject]]', element_to_mobject: 'Callable[[VMobject], VMobject] | type[VMobject]' = <function MobjectTable.<lambda> at 0x713b83114b80>, **kwargs: 'Any')` ← Table
> A specialized :class:`~.Table` mobject for use with :class:`~.Mobject`.

<details><summary>métodos próprios (1) · herdados: 258</summary>

- `__init__(self, table: 'Iterable[Iterable[VMobject]]', element_to_mobject: 'Callable[[VMobject], VMobject] | type[VMobject]' = <function MobjectTable.<lambda> at 0x713b83114b80>, **kwargs: 'Any')` — Special case of :class:`~.Table` with ``element_to_mobject`` set to an identity function.

</details>

### `Table(table: 'Iterable[Iterable[float | str | VMobject]]', row_labels: 'Iterable[VMobject] | None' = None, col_labels: 'Iterable[VMobject] | None' = None, top_left_entry: 'VMobject | None' = None, v_buff: 'float' = 0.8, h_buff: 'float' = 1.3, include_outer_lines: 'bool' = False, include_inner_lines: 'bool' = True, add_background_rectangles_to_entries: 'bool' = False, entries_background_color: 'ParsableManimColor' = ManimColor('#000000'), include_background_rectangle: 'bool' = False, background_rectangle_color: 'ParsableManimColor' = ManimColor('#000000'), element_to_mobject: 'Callable[[float | str], VMobject] | Callable[[VMobject], VMobject] | Callable[[float | str | VMobject], VMobject] | type[VMobject]' = <class 'manim.mobject.text.text_mobject.Paragraph'>, element_to_mobject_config: 'dict' = {}, arrange_in_grid_config: 'dict' = {}, line_config: 'dict' = {}, **kwargs: 'Any')` ← VGroup
> A mobject that displays a table on the screen.

<details><summary>métodos próprios (18) · herdados: 241</summary>

- `__init__(self, table: 'Iterable[Iterable[float | str | VMobject]]', row_labels: 'Iterable[VMobject] | None' = None, col_labels: 'Iterable[VMobject] | None' = None, top_left_entry: 'VMobject | None' = None, v_buff: 'float' = 0.8, h_buff: 'float' = 1.3, include_outer_lines: 'bool' = False, include_inner_lines: 'bool' = True, add_background_rectangles_to_entries: 'bool' = False, entries_background_color: 'ParsableManimColor' = ManimColor('#000000'), include_background_rectangle: 'bool' = False, background_rectangle_color: 'ParsableManimColor' = ManimColor('#000000'), element_to_mobject: 'Callable[[float | str], VMobject] | Callable[[VMobject], VMobject] | Callable[[float | str | VMobject], VMobject] | type[VMobject]' = <class 'manim.mobject.text.text_mobject.Paragraph'>, element_to_mobject_config: 'dict' = {}, arrange_in_grid_config: 'dict' = {}, line_config: 'dict' = {}, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `add_background_to_entries(self, color: 'ParsableManimColor' = ManimColor('#000000')) -> 'Self'` — Adds a black :class:`~.BackgroundRectangle` to each entry of the table.
- `add_highlighted_cell(self, pos: 'Sequence[int]' = (1, 1), color: 'ParsableManimColor' = ManimColor('#FFFF00'), **kwargs: 'Any') -> 'Self'` — Highlights one cell at a specific position on the table by adding a :class:`~.BackgroundRectangle`.
- `create(self, lag_ratio: 'float' = 1, line_animation: 'Callable[[VMobject | VGroup], Animation]' = <class 'manim.animation.creation.Create'>, label_animation: 'Callable[[VMobject | VGroup], Animation]' = <class 'manim.animation.creation.Write'>, element_animation: 'Callable[[VMobject | VGroup], Animation]' = <class 'manim.animation.creation.Create'>, entry_animation: 'Callable[[VMobject | VGroup], Animation]' = <class 'manim.animation.fading.FadeIn'>, **kwargs: 'Any') -> 'AnimationGroup'` — Customized create-type function for tables.
- `get_cell(self, pos: 'Sequence[int]' = (1, 1), **kwargs: 'Any') -> 'Polygon'` — Returns one specific cell as a rectangular :class:`~.Polygon` without the entry.
- `get_col_labels(self) -> 'VGroup'` — Return the column labels of the table.
- `get_columns(self) -> 'VGroup'` — Return columns of the table as a :class:`~.VGroup` of :class:`~.VGroup`.
- `get_entries(self, pos: 'Sequence[int] | None' = None) -> 'VMobject | VGroup'` — Return the individual entries of the table (including labels) or one specific entry
- `get_entries_without_labels(self, pos: 'Sequence[int] | None' = None) -> 'VMobject | VGroup'` — Return the individual entries of the table (without labels) or one specific entry
- `get_highlighted_cell(self, pos: 'Sequence[int]' = (1, 1), color: 'ParsableManimColor' = ManimColor('#FFFF00'), **kwargs: 'Any') -> 'BackgroundRectangle'` — Returns a :class:`~.BackgroundRectangle` of the cell at the given position.
- `get_horizontal_lines(self) -> 'VGroup'` — Return the horizontal lines of the table.
- `get_labels(self) -> 'VGroup'` — Returns the labels of the table.
- `get_row_labels(self) -> 'VGroup'` — Return the row labels of the table.
- `get_rows(self) -> 'VGroup'` — Return the rows of the table as a :class:`~.VGroup` of :class:`~.VGroup`.
- `get_vertical_lines(self) -> 'VGroup'` — Return the vertical lines of the table.
- `scale(self, scale_factor: 'float', scale_stroke: 'bool' = False, **kwargs: 'Any') -> 'Self'` — Scale the size by a factor.
- `set_column_colors(self, *colors: 'Iterable[ParsableManimColor]') -> 'Self'` — Set individual colors for each column of the table.
- `set_row_colors(self, *colors: 'Iterable[ParsableManimColor]') -> 'Self'` — Set individual colors for each row of the table.

</details>

- `BLACK` = `ManimColor('#000000')`
- `PURE_YELLOW` = `ManimColor('#FFFF00')`

## mobject/text

### `BulletedList(*items: 'str', buff: 'float' = 0.5, dot_scale_factor: 'float' = 2, tex_environment: 'str | None' = None, dot_buff: 'float' = 0.1, **kwargs: 'Any')` ← Tex
> A bulleted list.

<details><summary>métodos próprios (2) · herdados: 266</summary>

- `__init__(self, *items: 'str', buff: 'float' = 0.5, dot_scale_factor: 'float' = 2, tex_environment: 'str | None' = None, dot_buff: 'float' = 0.1, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `fade_all_but(self, index_or_string: 'int | str', opacity: 'float' = 0.5) -> 'Self'`

</details>

### `Code(code_file: 'StrPath | None' = None, code_string: 'str | None' = None, language: 'str | None' = None, formatter_style: 'str | type[Style]' = 'vim', tab_width: 'int' = 4, add_line_numbers: 'bool' = True, line_numbers_from: 'int' = 1, background: "Literal['rectangle', 'window']" = 'rectangle', background_config: 'dict[str, Any] | None' = None, paragraph_config: 'dict[str, Any] | None' = None)` ← VMobject
> A highlighted source code listing.

<details><summary>métodos próprios (3) · herdados: 242</summary>

- `__init__(self, code_file: 'StrPath | None' = None, code_string: 'str | None' = None, language: 'str | None' = None, formatter_style: 'str | type[Style]' = 'vim', tab_width: 'int' = 4, add_line_numbers: 'bool' = True, line_numbers_from: 'int' = 1, background: "Literal['rectangle', 'window']" = 'rectangle', background_config: 'dict[str, Any] | None' = None, paragraph_config: 'dict[str, Any] | None' = None)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_pygments_style(name: 'str') -> 'type[Style]'` — Return the Pygments style registered under ``name``.
- `get_styles_list() -> 'list[str]'` — Get the list of all available formatter styles.

</details>

### `DecimalNumber(number: 'float' = 0, num_decimal_places: 'int' = 2, mob_class: 'type[SingleStringMathTex]' = <class 'manim.mobject.text.tex_mobject.MathTex'>, include_sign: 'bool' = False, group_with_commas: 'bool' = True, digit_buff_per_font_unit: 'float' = 0.001, show_ellipsis: 'bool' = False, unit: 'str | None' = None, unit_buff_per_font_unit: 'float' = 0, include_background_rectangle: 'bool' = False, edge_to_fix: 'Vector3DLike' = array([-1.,  0.,  0.]), font_size: 'float' = 48, stroke_width: 'float' = 0, fill_opacity: 'float' = 1.0, **kwargs: 'Any')` ← VMobject
> An mobject representing a decimal number.

<details><summary>métodos próprios (4) · herdados: 242</summary>

- `__init__(self, number: 'float' = 0, num_decimal_places: 'int' = 2, mob_class: 'type[SingleStringMathTex]' = <class 'manim.mobject.text.tex_mobject.MathTex'>, include_sign: 'bool' = False, group_with_commas: 'bool' = True, digit_buff_per_font_unit: 'float' = 0.001, show_ellipsis: 'bool' = False, unit: 'str | None' = None, unit_buff_per_font_unit: 'float' = 0, include_background_rectangle: 'bool' = False, edge_to_fix: 'Vector3DLike' = array([-1.,  0.,  0.]), font_size: 'float' = 48, stroke_width: 'float' = 0, fill_opacity: 'float' = 1.0, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_value(self) -> 'float'`
- `increment_value(self, delta_t: 'float' = 1) -> 'Self'`
- `set_value(self, number: 'float') -> 'Self'` — Set the value of the :class:`~.DecimalNumber` to a new number.

</details>

### `Integer(number: 'float' = 0, num_decimal_places: 'int' = 0, **kwargs: 'Any') -> 'None'` ← DecimalNumber
> A class for displaying Integers.

<details><summary>métodos próprios (2) · herdados: 244</summary>

- `__init__(self, number: 'float' = 0, num_decimal_places: 'int' = 0, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `get_value(self) -> 'int'`

</details>

### `MarkupText(text: 'str', fill_opacity: 'float' = 1, stroke_width: 'float' = 0, color: 'ParsableManimColor | None' = None, font_size: 'float' = 48, line_spacing: 'float' = -1, font: 'str' = '', slant: 'str' = 'NORMAL', weight: 'str' = 'NORMAL', justify: 'bool' = False, gradient: 'Iterable[ParsableManimColor] | None' = None, tab_width: 'int' = 4, height: 'int | None' = None, width: 'int | None' = None, should_center: 'bool' = True, disable_ligatures: 'bool' = False, warn_missing_font: 'bool' = True, **kwargs: 'Any')` ← SVGMobject
> Display (non-LaTeX) text rendered using `Pango <https://pango.org/>`_.

<details><summary>métodos próprios (2) · herdados: 259</summary>

- `__init__(self, text: 'str', fill_opacity: 'float' = 1, stroke_width: 'float' = 0, color: 'ParsableManimColor | None' = None, font_size: 'float' = 48, line_spacing: 'float' = -1, font: 'str' = '', slant: 'str' = 'NORMAL', weight: 'str' = 'NORMAL', justify: 'bool' = False, gradient: 'Iterable[ParsableManimColor] | None' = None, tab_width: 'int' = 4, height: 'int | None' = None, width: 'int | None' = None, should_center: 'bool' = True, disable_ligatures: 'bool' = False, warn_missing_font: 'bool' = True, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `font_list() -> 'list[str]'`

</details>

### `MathTex(*tex_strings: 'str', arg_separator: 'str' = ' ', substrings_to_isolate: 'Iterable[str] | None' = None, tex_to_color_map: 'dict[str, ParsableManimColor] | None' = None, tex_environment: 'str | None' = 'align*', **kwargs: 'Any')` ← SingleStringMathTex
> A string compiled with LaTeX in math mode.

<details><summary>métodos próprios (7) · herdados: 260</summary>

- `__init__(self, *tex_strings: 'str', arg_separator: 'str' = ' ', substrings_to_isolate: 'Iterable[str] | None' = None, tex_to_color_map: 'dict[str, ParsableManimColor] | None' = None, tex_environment: 'str | None' = 'align*', **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_part_by_tex(self, tex: 'str', **kwargs: 'Any') -> 'VGroup | None'`
- `index_of_part(self, part: 'VMobject') -> 'int'`
- `set_color_by_tex(self, tex: 'str', color: 'ParsableManimColor', **kwargs: 'Any') -> 'Self'`
- `set_color_by_tex_to_color_map(self, texs_to_color_map: 'dict[str, ParsableManimColor]', **kwargs: 'Any') -> 'Self'`
- `set_opacity_by_tex(self, tex: 'str', opacity: 'float' = 0.5, remaining_opacity: 'float | None' = None, **kwargs: 'Any') -> 'Self'` — Sets the opacity of the tex specified. If 'remaining_opacity' is specified,
- `sort_alphabetically(self) -> 'Self'`

</details>

### `MathTexPart(fill_color: 'ParsableManimColor | None' = None, fill_opacity: 'float' = 0.0, stroke_color: 'ParsableManimColor | None' = None, stroke_opacity: 'float' = 1.0, stroke_width: 'float' = 4, background_stroke_color: 'ParsableManimColor | None' = ManimColor('#000000'), background_stroke_opacity: 'float' = 1.0, background_stroke_width: 'float' = 0, sheen_factor: 'float' = 0.0, joint_type: 'LineJointType | None' = None, sheen_direction: 'Vector3DLike' = array([-1.,  1.,  0.]), close_new_points: 'bool' = False, pre_function_handle_to_anchor_scale_factor: 'float' = 0.01, make_smooth_after_applying_functions: 'bool' = False, background_image: 'Image | str | None' = None, shade_in_3d: 'bool' = False, tolerance_for_point_equality: 'float' = 1e-06, n_points_per_cubic_curve: 'int' = 4, cap_style: 'CapStyleType' = <CapStyleType.AUTO: 0>, **kwargs: 'Any')` ← VMobject
> A vectorized mobject.

### `MathTypst(math_expression: 'str', **kwargs: 'Any')` ← Typst
> Convenience wrapper: wraps the input in Typst math delimiters.

<details><summary>métodos próprios (1) · herdados: 261</summary>

- `__init__(self, math_expression: 'str', **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Paragraph(*text: 'str', line_spacing: 'float' = -1, alignment: 'str | None' = None, **kwargs: 'Any')` ← VGroup
> Display a paragraph of text.

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, *text: 'str', line_spacing: 'float' = -1, alignment: 'str | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `SingleStringMathTex(tex_string: 'str', stroke_width: 'float' = 0, should_center: 'bool' = True, height: 'float | None' = None, organize_left_to_right: 'bool' = False, tex_environment: 'str | None' = 'align*', tex_template: 'TexTemplate | None' = None, font_size: 'float' = 48, color: 'ParsableManimColor | None' = None, **kwargs: 'Any')` ← SVGMobject
> Elementary building block for rendering text with LaTeX.

<details><summary>métodos próprios (3) · herdados: 258</summary>

- `__init__(self, tex_string: 'str', stroke_width: 'float' = 0, should_center: 'bool' = True, height: 'float | None' = None, organize_left_to_right: 'bool' = False, tex_environment: 'str | None' = 'align*', tex_template: 'TexTemplate | None' = None, font_size: 'float' = 48, color: 'ParsableManimColor | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_tex_string(self) -> 'str'`
- `init_colors(self, propagate_colors: 'bool' = True) -> 'Self'` — Initializes the colors.

</details>

### `Tex(*tex_strings: 'str', arg_separator: 'str' = '', tex_environment: 'str | None' = 'center', **kwargs: 'Any')` ← MathTex
> A string compiled with LaTeX in normal mode.

<details><summary>métodos próprios (1) · herdados: 266</summary>

- `__init__(self, *tex_strings: 'str', arg_separator: 'str' = '', tex_environment: 'str | None' = 'center', **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Text(text: 'str', fill_opacity: 'float' = 1.0, stroke_width: 'float' = 0, color: 'ParsableManimColor | None' = None, font_size: 'float' = 48, line_spacing: 'float' = -1, font: 'str' = '', slant: 'str' = 'NORMAL', weight: 'str' = 'NORMAL', t2c: 'dict[str, str] | None' = None, t2f: 'dict[str, str] | None' = None, t2g: 'dict[str, Iterable[ParsableManimColor]] | None' = None, t2s: 'dict[str, str] | None' = None, t2w: 'dict[str, str] | None' = None, gradient: 'Iterable[ParsableManimColor] | None' = None, tab_width: 'int' = 4, warn_missing_font: 'bool' = True, height: 'float | None' = None, width: 'float | None' = None, should_center: 'bool' = True, disable_ligatures: 'bool' = False, use_svg_cache: 'bool' = False, **kwargs: 'Any')` ← SVGMobject
> Display (non-LaTeX) text rendered using `Pango <https://pango.org/>`_.

<details><summary>métodos próprios (3) · herdados: 258</summary>

- `__init__(self, text: 'str', fill_opacity: 'float' = 1.0, stroke_width: 'float' = 0, color: 'ParsableManimColor | None' = None, font_size: 'float' = 48, line_spacing: 'float' = -1, font: 'str' = '', slant: 'str' = 'NORMAL', weight: 'str' = 'NORMAL', t2c: 'dict[str, str] | None' = None, t2f: 'dict[str, str] | None' = None, t2g: 'dict[str, Iterable[ParsableManimColor]] | None' = None, t2s: 'dict[str, str] | None' = None, t2w: 'dict[str, str] | None' = None, gradient: 'Iterable[ParsableManimColor] | None' = None, tab_width: 'int' = 4, warn_missing_font: 'bool' = True, height: 'float | None' = None, width: 'float | None' = None, should_center: 'bool' = True, disable_ligatures: 'bool' = False, use_svg_cache: 'bool' = False, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `font_list() -> 'list[str]'`
- `init_colors(self, propagate_colors: 'bool' = True) -> 'Self'` — Initializes the colors.

</details>

### `Title(*text_parts: 'str', include_underline: 'bool' = True, match_underline_width_to_text: 'bool' = False, underline_buff: 'float' = 0.25, **kwargs: 'Any')` ← Tex
> A mobject representing an underlined title.

<details><summary>métodos próprios (1) · herdados: 266</summary>

- `__init__(self, *text_parts: 'str', include_underline: 'bool' = True, match_underline_width_to_text: 'bool' = False, underline_buff: 'float' = 0.25, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Typst(typst_code: 'str', *, font_size: 'float' = 48, typst_preamble: 'str' = '', color: 'ParsableManimColor | None' = None, stroke_width: 'float | None' = None, font_paths: 'list[str | Path] | None' = None, track_baselines: 'bool' = False, should_center: 'bool' = True, height: 'float | None' = None, **kwargs: 'Any')` ← SVGMobject
> A mobject rendered from a Typst markup string.

<details><summary>métodos próprios (7) · herdados: 255</summary>

- `__init__(self, typst_code: 'str', *, font_size: 'float' = 48, typst_preamble: 'str' = '', color: 'ParsableManimColor | None' = None, stroke_width: 'float | None' = None, font_paths: 'list[str | Path] | None' = None, track_baselines: 'bool' = False, should_center: 'bool' = True, height: 'float | None' = None, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `get_baseline_frame(self, submobject: 'VMobject') -> 'tuple[np.ndarray, np.ndarray, np.ndarray]'` — Return the current Typst baseline frame for a tracked submobject.
- `get_mob_from_shape_element(self, shape: 'se.SVGElement') -> 'VMobject | None'` — Attach Typst-specific metadata to imported shape mobjects.
- `init_colors(self, propagate_colors: 'bool' = True) -> 'Self'` — Recolor black submobjects to ``self.color``.
- `modify_xml_tree(self, element_tree: 'ET.ElementTree') -> 'ET.ElementTree'` — Convert ``data-typst-label`` attributes to ``id`` before parsing.
- `scale(self, scale_factor: 'float', scale_stroke: 'bool' = False, *, about_point: 'np.ndarray | None' = None, about_edge: 'np.ndarray | None' = None) -> 'Self'` — Scale the size by a factor.
- `select(self, key: 'str | int') -> 'VGroup'` — Select a labeled sub-expression.

</details>

### `Variable(var: 'float', label: 'str | Tex | MathTex | Text | SingleStringMathTex', var_type: 'type[DecimalNumber | Integer]' = <class 'manim.mobject.text.numbers.DecimalNumber'>, num_decimal_places: 'int' = 2, **kwargs: 'Any')` ← VMobject
> A class for displaying text that shows "label = value" with

<details><summary>métodos próprios (1) · herdados: 242</summary>

- `__init__(self, var: 'float', label: 'str | Tex | MathTex | Text | SingleStringMathTex', var_type: 'type[DecimalNumber | Integer]' = <class 'manim.mobject.text.numbers.DecimalNumber'>, num_decimal_places: 'int' = 2, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

- `BLACK` = `ManimColor('#000000')`
- `BLACK` = `ManimColor('#000000')`
- `BLACK` = `ManimColor('#000000')`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_LINE_SPACING_SCALE` = `0.3`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `MATHTEX_SUBSTRING` = `'substring'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `START_X` = `30`
- `START_X` = `30`
- `START_X` = `30`
- `START_X` = `30`
- `START_Y` = `20`
- `START_Y` = `20`
- `START_Y` = `20`
- `START_Y` = `20`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TEXT2SVG_ADJUSTMENT_FACTOR` = `4.8`
- `TEXT_MOB_SCALE_FACTOR` = `0.05`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `WHITE` = `ManimColor('#FFFFFF')`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- **`register_font(font_file: 'str | Path') -> 'Iterator[None]'`** — Temporarily add a font file to Pango's search path.
- **`remove_invisible_chars(mobject: 'VMobject') -> 'VMobject'`** — Function to remove unwanted invisible characters from some mobjects.

## mobject/value_tracker

### `ComplexValueTracker(value: 'float' = 0, **kwargs: 'Any') -> 'None'` ← ValueTracker
> Tracks a complex-valued parameter.

<details><summary>métodos próprios (2) · herdados: 158</summary>

- `get_value(self) -> 'complex'` — Get the current value of this ComplexValueTracker as a complex number.
- `set_value(self, value: 'complex | float') -> 'Self'` — Sets a new complex value to the ComplexValueTracker.

</details>

### `ValueTracker(value: 'float' = 0, **kwargs: 'Any') -> 'None'` ← Mobject
> A mobject that can be used for tracking (real-valued) parameters.

<details><summary>métodos próprios (5) · herdados: 155</summary>

- `__init__(self, value: 'float' = 0, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `get_value(self) -> 'float'` — Get the current value of this ValueTracker.
- `increment_value(self, d_value: 'float') -> 'Self'` — Increments (adds) a scalar value to the ValueTracker.
- `interpolate(self, mobject1: 'Mobject', mobject2: 'Mobject', alpha: 'float', path_func: 'PathFuncType' = <function interpolate at 0x713b87942020>) -> 'Self'` — Turns ``self`` into an interpolation between ``mobject1`` and ``mobject2``.
- `set_value(self, value: 'float') -> 'Self'` — Sets a new scalar value to the ValueTracker.

</details>

- `TYPE_CHECKING` = `False`

## mobject/vector_field

### `ArrowVectorField(func: 'Callable[[np.ndarray], np.ndarray]', color: 'ParsableManimColor | None' = None, color_scheme: 'Callable[[np.ndarray], float] | None' = None, min_color_scheme_value: 'float' = 0, max_color_scheme_value: 'float' = 2, colors: 'Sequence[ParsableManimColor]' = [ManimColor('#236B8E'), ManimColor('#83C167'), ManimColor('#F7D96F'), ManimColor('#FC6255')], x_range: 'Sequence[float]' = None, y_range: 'Sequence[float]' = None, z_range: 'Sequence[float]' = None, three_dimensions: 'bool' = False, length_func: 'Callable[[float], float]' = <function ArrowVectorField.<lambda> at 0x713b82e43ba0>, opacity: 'float' = 1.0, vector_config: 'dict | None' = None, **kwargs)` ← VectorField
> A :class:`VectorField` represented by a set of change vectors.

<details><summary>métodos próprios (2) · herdados: 252</summary>

- `__init__(self, func: 'Callable[[np.ndarray], np.ndarray]', color: 'ParsableManimColor | None' = None, color_scheme: 'Callable[[np.ndarray], float] | None' = None, min_color_scheme_value: 'float' = 0, max_color_scheme_value: 'float' = 2, colors: 'Sequence[ParsableManimColor]' = [ManimColor('#236B8E'), ManimColor('#83C167'), ManimColor('#F7D96F'), ManimColor('#FC6255')], x_range: 'Sequence[float]' = None, y_range: 'Sequence[float]' = None, z_range: 'Sequence[float]' = None, three_dimensions: 'bool' = False, length_func: 'Callable[[float], float]' = <function ArrowVectorField.<lambda> at 0x713b82e43ba0>, opacity: 'float' = 1.0, vector_config: 'dict | None' = None, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_vector(self, point: 'np.ndarray')` — Creates a vector in the vector field.

</details>

### `StreamLines(func: 'Callable[[np.ndarray], np.ndarray]', color: 'ParsableManimColor | None' = None, color_scheme: 'Callable[[np.ndarray], float] | None' = None, min_color_scheme_value: 'float' = 0, max_color_scheme_value: 'float' = 2, colors: 'Sequence[ParsableManimColor]' = [ManimColor('#236B8E'), ManimColor('#83C167'), ManimColor('#F7D96F'), ManimColor('#FC6255')], x_range: 'Sequence[float]' = None, y_range: 'Sequence[float]' = None, z_range: 'Sequence[float]' = None, three_dimensions: 'bool' = False, noise_factor: 'float | None' = None, n_repeats=1, dt=0.05, virtual_time=3, max_anchors_per_line=100, padding=3, stroke_width=1, opacity=1, **kwargs)` ← VectorField
> StreamLines represent the flow of a :class:`VectorField` using the trace of moving agents.

<details><summary>métodos próprios (4) · herdados: 252</summary>

- `__init__(self, func: 'Callable[[np.ndarray], np.ndarray]', color: 'ParsableManimColor | None' = None, color_scheme: 'Callable[[np.ndarray], float] | None' = None, min_color_scheme_value: 'float' = 0, max_color_scheme_value: 'float' = 2, colors: 'Sequence[ParsableManimColor]' = [ManimColor('#236B8E'), ManimColor('#83C167'), ManimColor('#F7D96F'), ManimColor('#FC6255')], x_range: 'Sequence[float]' = None, y_range: 'Sequence[float]' = None, z_range: 'Sequence[float]' = None, three_dimensions: 'bool' = False, noise_factor: 'float | None' = None, n_repeats=1, dt=0.05, virtual_time=3, max_anchors_per_line=100, padding=3, stroke_width=1, opacity=1, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `create(self, lag_ratio: 'float | None' = None, run_time: 'Callable[[float], float] | None' = None, **kwargs) -> 'AnimationGroup'` — The creation animation of the stream lines.
- `end_animation(self) -> 'AnimationGroup'` — End the stream line animation smoothly.
- `start_animation(self, warm_up: 'bool' = True, flow_speed: 'float' = 1, time_width: 'float' = 0.3, rate_func: 'Callable[[float], float]' = <function linear at 0x713b879e5d00>, line_animation_class: 'type[ShowPassingFlash]' = <class 'manim.animation.indication.ShowPassingFlash'>, **kwargs) -> 'Self'` — Animates the stream lines using an updater.

</details>

### `VectorField(func: 'Callable[[Point3D], Vector3D]', color: 'ParsableManimColor | None' = None, color_scheme: 'Callable[[Vector3D], float] | None' = None, min_color_scheme_value: 'float' = 0, max_color_scheme_value: 'float' = 2, colors: 'Sequence[ParsableManimColor]' = [ManimColor('#236B8E'), ManimColor('#83C167'), ManimColor('#F7D96F'), ManimColor('#FC6255')], **kwargs)` ← VGroup
> A vector field.

<details><summary>métodos próprios (11) · herdados: 242</summary>

- `__init__(self, func: 'Callable[[Point3D], Vector3D]', color: 'ParsableManimColor | None' = None, color_scheme: 'Callable[[Vector3D], float] | None' = None, min_color_scheme_value: 'float' = 0, max_color_scheme_value: 'float' = 2, colors: 'Sequence[ParsableManimColor]' = [ManimColor('#236B8E'), ManimColor('#83C167'), ManimColor('#F7D96F'), ManimColor('#FC6255')], **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `fit_to_coordinate_system(self, coordinate_system: 'CoordinateSystem') -> 'Self'` — Scale the vector field to fit a coordinate system.
- `get_colored_background_image(self, sampling_rate: 'int' = 5) -> 'Image.Image'` — Generate an image that displays the vector field.
- `get_nudge_updater(self, speed: 'float' = 1, pointwise: 'bool' = False) -> 'Callable[[Mobject, float], Mobject]'` — Get an update function to move a :class:`~.Mobject` along the vector field.
- `get_vectorized_rgba_gradient_function(self, start: 'float', end: 'float', colors: 'Iterable[ParsableManimColor]') -> 'Callable[[Sequence[float], float], FloatRGBA_Array]'` — Generates a gradient of rgbas as a numpy array
- `nudge(self, mob: 'Mobject', dt: 'float' = 1, substeps: 'int' = 1, pointwise: 'bool' = False) -> 'Self'` — Nudge a :class:`~.Mobject` along the vector field.
- `nudge_submobjects(self, dt: 'float' = 1, substeps: 'int' = 1, pointwise: 'bool' = False) -> 'Self'` — Apply a nudge along the vector field to all submobjects.
- `scale_func(func: 'Callable[[np.ndarray], np.ndarray]', scalar: 'float') -> 'Callable[[np.ndarray], np.ndarray]'` — Scale a vector field function.
- `shift_func(func: 'Callable[[np.ndarray], np.ndarray]', shift_vector: 'np.ndarray') -> 'Callable[[np.ndarray], np.ndarray]'` — Shift a vector field function.
- `start_submobject_movement(self, speed: 'float' = 1, pointwise: 'bool' = False) -> 'Self'` — Start continuously moving all submobjects along the vector field.
- `stop_submobject_movement(self) -> 'Self'` — Stops the continuous movement started using :meth:`start_submobject_movement`.

</details>

- `BLUE_E` = `ManimColor('#236B8E')`
- `DEFAULT_SCALAR_FIELD_COLORS` = `[ManimColor('#236B8E'), ManimColor('#83C167'), ManimColor('#F7D96F'), ManimColor('#FC6255')]`
- `GREEN` = `ManimColor('#83C167')`
- `OUT` = `array([0., 0., 1.])`
- `RED` = `ManimColor('#FC6255')`
- `RIGHT` = `array([1., 0., 0.])`
- `TYPE_CHECKING` = `False`
- `UP` = `array([0., 1., 0.])`
- `YELLOW` = `ManimColor('#F7D96F')`

## other

### `ClickArgs(args: 'dict[str, Any]') -> 'None'` ← Namespace
> Simple object for storing attributes.

<details><summary>métodos próprios (1) · herdados: 0</summary>

- `__init__(self, args: 'dict[str, Any]') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `DefaultGroup(*args: 'Any', **kwargs: 'Any')` ← Group
> Invokes a subcommand marked with ``default=True`` if any subcommand is not

<details><summary>métodos próprios (6) · herdados: 48</summary>

- `__init__(self, *args: 'Any', **kwargs: 'Any')` — :param align_sections:
- `command(self, *args: 'Any', **kwargs: 'Any') -> 'Callable[[Callable[..., object]], Command]'` — Return a decorator which converts any function into the default
- `get_command(self, ctx: 'Context', cmd_name: 'str') -> 'Command | None'` — Get a command function by its name, by forwarding the arguments to
- `parse_args(self, ctx: 'Context', args: 'list[str]') -> 'list[str]'` — Parses the list of ``args`` by forwarding it to
- `resolve_command(self, ctx: 'Context', args: 'list[str]') -> 'tuple[str | None, Command | None, list[str]]'` — Given a list of ``args`` given by a CLI, find a command which
- `set_default_command(self, command: 'Command') -> 'None'` — Sets a command function as the default command.

</details>

### `HealthCheckFunction(*args, **kwargs)` ← Protocol
> Base class for protocol classes.

<details><summary>métodos próprios (2) · herdados: 0</summary>

- `__call__(self) -> 'bool'` — Call self as a function.
- `__init__(self, *args, **kwargs)`

</details>

### `MarkupUtils()`

<details><summary>métodos próprios (2) · herdados: 1</summary>

- `text2svg(text: 'str', font: 'str | None', slant: 'str', weight: 'str', size: 'float', _, disable_liga: 'bool', file_name: 'str', START_X: 'int', START_Y: 'int', width: 'int', height: 'int', *, justify: 'bool | None' = None, indent: 'float | int | None' = None, line_spacing: 'float | None' = None, alignment: 'Alignment | None' = None, pango_width: 'int | None' = None) -> 'str'` — Render an SVG file from a :class:`manim.mobject.svg.text_mobject.MarkupText` object.
- `validate(markup: 'str') -> 'str'` — Validates whether markup is a valid Markup

</details>

### `MethodWithArgs(method: 'MethodType', args: 'Iterable[Any]', kwargs: 'dict[str, Any]') -> None`
> Object containing a :attr:`method` which is intended to be called later

<details><summary>métodos próprios (1) · herdados: 0</summary>

- `__init__(self, method: 'MethodType', args: 'Iterable[Any]', kwargs: 'dict[str, Any]') -> None` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `PangoUtils()`

<details><summary>métodos próprios (3) · herdados: 1</summary>

- `remove_last_M(file_name: str) -> None` — Remove element from the SVG file in order to allow comparison.
- `str2style(string: str) -> manimpango.enums.Style` — Internally used function. Converts text to Pango Understandable Styles.
- `str2weight(string: str) -> manimpango.enums.Weight` — Internally used function. Convert text to Pango Understandable Weight

</details>

### `TextSetting(start: 'int', end: 'int', font: 'str', slant: 'str', weight: 'str', line_num=-1, color: 'str' = None)`
> Formatting for slices of a :class:`manim.mobject.svg.text_mobject.Text` object.

<details><summary>métodos próprios (1) · herdados: 0</summary>

- `__init__(self, start: 'int', end: 'int', font: 'str', slant: 'str', weight: 'str', line_num=-1, color: 'str' = None)`

</details>

- `BLACK` = `ManimColor('#000000')`
- `BLUE` = `ManimColor('#58C4DD')`
- `BLUE_A` = `ManimColor('#C7E9F1')`
- `BLUE_B` = `ManimColor('#9CDCEB')`
- `BLUE_C` = `ManimColor('#58C4DD')`
- `BLUE_D` = `ManimColor('#29ABCA')`
- `BLUE_E` = `ManimColor('#236B8E')`
- `BOLD` = `'BOLD'`
- `BOOK` = `'BOOK'`
- `CFG_DEFAULTS` = `{'frame_rate': 30, 'background_color': 'BLACK', 'background_opacity': 1, 'scene_names': 'Default', 'resolution': (108...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CTRL_VALUE` = `65507`
- `DARKER_GRAY` = `ManimColor('#222222')`
- `DARKER_GREY` = `ManimColor('#222222')`
- `DARK_BLUE` = `ManimColor('#236B8E')`
- `DARK_BROWN` = `ManimColor('#8B4513')`
- `DARK_GRAY` = `ManimColor('#444444')`
- `DARK_GREY` = `ManimColor('#444444')`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `GOLD` = `ManimColor('#F0AC5F')`
- `GOLD_A` = `ManimColor('#F7C797')`
- `GOLD_B` = `ManimColor('#F9B775')`
- `GOLD_C` = `ManimColor('#F0AC5F')`
- `GOLD_D` = `ManimColor('#E1A158')`
- `GOLD_E` = `ManimColor('#C78D46')`
- `GRAY` = `ManimColor('#888888')`
- `GRAY_A` = `ManimColor('#DDDDDD')`
- `GRAY_B` = `ManimColor('#BBBBBB')`
- `GRAY_BROWN` = `ManimColor('#736357')`
- `GRAY_C` = `ManimColor('#888888')`
- `GRAY_D` = `ManimColor('#444444')`
- `GRAY_E` = `ManimColor('#222222')`
- `GREEN` = `ManimColor('#83C167')`
- `GREEN_A` = `ManimColor('#C9E2AE')`
- `GREEN_B` = `ManimColor('#A6CF8C')`
- `GREEN_C` = `ManimColor('#83C167')`
- `GREEN_D` = `ManimColor('#77B05D')`
- `GREEN_E` = `ManimColor('#699C52')`
- `GREY` = `ManimColor('#888888')`
- `GREY_A` = `ManimColor('#DDDDDD')`
- `GREY_B` = `ManimColor('#BBBBBB')`
- `GREY_BROWN` = `ManimColor('#736357')`
- `GREY_C` = `ManimColor('#888888')`
- `GREY_D` = `ManimColor('#444444')`
- `GREY_E` = `ManimColor('#222222')`
- `HEALTH_CHECKS` = `[<function is_manim_on_path at 0x713b82ee19e0>, <function is_manim_executable_associated_to_this_library at 0x713b82e...`
- `HEALTH_CHECKS` = `[<function is_manim_on_path at 0x713b82ee19e0>, <function is_manim_executable_associated_to_this_library at 0x713b82e...`
- `HEAVY` = `'HEAVY'`
- `IN` = `array([ 0.,  0., -1.])`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LIGHT` = `'LIGHT'`
- `LIGHTER_GRAY` = `ManimColor('#DDDDDD')`
- `LIGHTER_GREY` = `ManimColor('#DDDDDD')`
- `LIGHT_BROWN` = `ManimColor('#CD853F')`
- `LIGHT_GRAY` = `ManimColor('#BBBBBB')`
- `LIGHT_GREY` = `ManimColor('#BBBBBB')`
- `LIGHT_PINK` = `ManimColor('#DC75CD')`
- `LOGO_BLACK` = `ManimColor('#343434')`
- `LOGO_BLUE` = `ManimColor('#525893')`
- `LOGO_GREEN` = `ManimColor('#87C2A5')`
- `LOGO_RED` = `ManimColor('#E07A5F')`
- `LOGO_WHITE` = `ManimColor('#ECE7E2')`
- `MAROON` = `ManimColor('#C55F73')`
- `MAROON_A` = `ManimColor('#ECABC1')`
- `MAROON_B` = `ManimColor('#EC92AB')`
- `MAROON_C` = `ManimColor('#C55F73')`
- `MAROON_D` = `ManimColor('#A24D61')`
- `MAROON_E` = `ManimColor('#94424F')`
- `MEDIUM` = `'MEDIUM'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OBLIQUE` = `'OBLIQUE'`
- `ORANGE` = `ManimColor('#FF862F')`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `PINK` = `ManimColor('#D147BD')`
- `PURE_BLUE` = `ManimColor('#0000FF')`
- `PURE_CYAN` = `ManimColor('#00FFFF')`
- `PURE_GREEN` = `ManimColor('#00FF00')`
- `PURE_MAGENTA` = `ManimColor('#FF00FF')`
- `PURE_RED` = `ManimColor('#FF0000')`
- `PURE_YELLOW` = `ManimColor('#FFFF00')`
- `PURPLE` = `ManimColor('#9A72AC')`
- `PURPLE_A` = `ManimColor('#CAA3E8')`
- `PURPLE_B` = `ManimColor('#B189C6')`
- `PURPLE_C` = `ManimColor('#9A72AC')`
- `PURPLE_D` = `ManimColor('#715582')`
- `PURPLE_E` = `ManimColor('#644172')`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `RED` = `ManimColor('#FC6255')`
- `RED_A` = `ManimColor('#F7A1A3')`
- `RED_B` = `ManimColor('#FF8080')`
- `RED_C` = `ManimColor('#FC6255')`
- `RED_D` = `ManimColor('#E65A4C')`
- `RED_E` = `ManimColor('#CF5044')`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RICH_COLOUR_INSTRUCTIONS` = `'\n[red]The default colour is used by the input statement.\nIf left empty, the default colour will be used.[/red]\n[m...`
- `RICH_NON_STYLE_ENTRIES` = `['log.width', 'log.height', 'log.timestamps']`
- `RIGHT` = `array([1., 0., 0.])`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SHIFT_VALUE` = `65505`
- `SMALL_BUFF` = `0.1`
- `START_X` = `30`
- `START_Y` = `20`
- `TAU` = `6.283185307179586`
- `TEAL` = `ManimColor('#5CD0B3')`
- `TEAL_A` = `ManimColor('#ACEAD7')`
- `TEAL_B` = `ManimColor('#76DDC0')`
- `TEAL_C` = `ManimColor('#5CD0B3')`
- `TEAL_D` = `ManimColor('#55C1A7')`
- `TEAL_E` = `ManimColor('#49A88F')`
- `THIN` = `'THIN'`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `WHITE` = `ManimColor('#FFFFFF')`
- `X_AXIS` = `array([1., 0., 0.])`
- `YELLOW` = `ManimColor('#F7D96F')`
- `YELLOW_A` = `ManimColor('#FFF1B6')`
- `YELLOW_B` = `ManimColor('#FFEA94')`
- `YELLOW_C` = `ManimColor('#F7D96F')`
- `YELLOW_D` = `ManimColor('#F4D345')`
- `YELLOW_E` = `ManimColor('#E8C11C')`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- **`healthcheck(description: 'str', recommendation: 'str', skip_on_failed: 'list[HealthCheckFunction | str] | None' = None, post_fail_fix_hook: 'Callable[..., object] | None' = None) -> 'Callable[[Callable[[], bool]], HealthCheckFunction]'`** — Decorator used for declaring health checks.
- **`is_dvisvgm_available() -> 'bool'`** — Check whether ``dvisvgm`` is in ``PATH`` and can be executed.
- **`is_latex_available() -> 'bool'`** — Check whether ``latex`` is in ``PATH`` and can be executed.
- **`is_manim_executable_associated_to_this_library() -> 'bool'`** — Check whether the ``manim`` executable in ``PATH`` is associated to this
- **`is_manim_on_path() -> 'bool'`** — Check whether ``manim`` is in ``PATH``.
- **`is_valid_style(style: 'str') -> 'bool'`** — Checks whether the entered color style is valid, according to ``rich``.
- **`print_version_and_exit(ctx: 'click.Context', param: 'click.Option', value: 'str | None') -> 'None'`** — Same as :func:`show_splash`, but also exit when giving a value by
- **`replace_keys(default: 'dict[str, Any]') -> 'dict[str, Any]'`** — Replace ``_`` with ``.`` and vice versa in a dictionary's keys for
- **`select_resolution() -> 'tuple[int, int]'`** — Prompts input of type click.Choice from user. Presents options from QUALITIES constant.
- **`show_splash(ctx: 'click.Context', param: 'click.Option', value: 'str | None') -> 'None'`** — When giving a value by console, show an initial message with the Manim
- **`update_cfg(cfg_dict: 'dict[str, Any]', project_cfg_path: 'Path') -> 'None'`** — Update the ``manim.cfg`` file after reading it from the specified
- **`validate_gui_location(ctx: 'Context', param: 'Option', value: 'str | None') -> 'tuple[int, int] | None'`** — If the ``value`` string is given, extract from it the GUI location,
- **`validate_resolution(ctx: 'Context', param: 'Option', value: 'str | None') -> 'tuple[int, int] | None'`** — If the ``value`` string is given, extract from it the resolution, which
- **`validate_scene_range(ctx: 'Context', param: 'Option', value: 'str | None') -> 'tuple[int] | tuple[int, int] | None'`** — If the ``value`` string is given, extract from it the scene range, which
- **`value_from_string(value: 'str') -> 'str | int | bool'`** — Extract the literal of proper datatype from a ``value`` string.

## plugins

- **`get_plugins() -> 'dict[str, Any]'`**
- **`list_plugins() -> 'None'`**

## renderer

### `CairoRenderer(file_writer_class: 'type[SceneFileWriter]' = <class 'manim.scene.scene_file_writer.SceneFileWriter'>, camera_class: 'type[Camera] | None' = None, skip_animations: 'bool' = False, **kwargs: 'Any')`
> A renderer using Cairo.

<details><summary>métodos próprios (12) · herdados: 0</summary>

- `__init__(self, file_writer_class: 'type[SceneFileWriter]' = <class 'manim.scene.scene_file_writer.SceneFileWriter'>, camera_class: 'type[Camera] | None' = None, skip_animations: 'bool' = False, **kwargs: 'Any')` — Initialize self.  See help(type(self)) for accurate signature.
- `add_frame(self, frame: 'PixelArray', num_frames: 'int' = 1) -> 'None'` — Adds a frame to the video_file_stream
- `freeze_current_frame(self, duration: 'float') -> 'None'` — Adds a static frame to the movie for a given duration. The static frame is the current frame.
- `get_frame(self) -> 'PixelArray'` — Gets the current frame as NumPy array.
- `init_scene(self, scene: 'Scene') -> 'None'`
- `play(self, scene: 'Scene', *args: 'Animation | Mobject | _AnimationBuilder', **kwargs: 'Any') -> 'None'`
- `render(self, scene: 'Scene', time: 'float', moving_mobjects: 'Iterable[Mobject] | None' = None) -> 'None'`
- `save_static_frame_data(self, scene: 'Scene', static_mobjects: 'Iterable[Mobject]') -> 'PixelArray | None'` — Compute and save the static frame, that will be reused at each frame
- `scene_finished(self, scene: 'Scene') -> 'None'`
- `show_frame(self, scene: 'Scene') -> 'None'` — Opens the current frame in the Default Image Viewer
- `update_frame(self, scene: 'Scene', mobjects: 'Iterable[Mobject] | None' = None, include_submobjects: 'bool' = True, ignore_skipping: 'bool' = True, **kwargs: 'Any') -> 'None'` — Update the frame.
- `update_skipping_status(self) -> 'None'` — This method is used internally to check if the current

</details>

### `FullScreenQuad(context: 'moderngl.Context', fragment_shader_source: 'str | None' = None, fragment_shader_name: 'str | None' = None)` ← Mesh

<details><summary>métodos próprios (2) · herdados: 25</summary>

- `__init__(self, context: 'moderngl.Context', fragment_shader_source: 'str | None' = None, fragment_shader_name: 'str | None' = None)` — Initialize self.  See help(type(self)) for accurate signature.
- `render(self) -> 'None'`

</details>

### `Mesh(shader: 'Shader | None' = None, attributes: 'npt.NDArray | None' = None, geometry: 'Mesh | None' = None, material: 'Shader | None' = None, indices: 'npt.NDArray | None' = None, use_depth_test: 'bool' = True, primitive: 'int' = 4)` ← Object3D

<details><summary>métodos próprios (4) · herdados: 23</summary>

- `__init__(self, shader: 'Shader | None' = None, attributes: 'npt.NDArray | None' = None, geometry: 'Mesh | None' = None, material: 'Shader | None' = None, indices: 'npt.NDArray | None' = None, use_depth_test: 'bool' = True, primitive: 'int' = 4)` — Initialize self.  See help(type(self)) for accurate signature.
- `render(self) -> 'None'`
- `set_uniforms(self, renderer: 'OpenGLRenderer') -> 'None'`
- `single_copy(self) -> 'Mesh'`

</details>

### `Object3D(*children: 'Object3D')`

<details><summary>métodos próprios (25) · herdados: 0</summary>

- `__init__(self, *children: 'Object3D')` — Initialize self.  See help(type(self)) for accurate signature.
- `add(self, *children: 'Object3D') -> 'None'`
- `add_updater(self, update_function: 'MeshUpdater', index: 'int | None' = None, call_updater: 'bool' = True) -> 'Self'`
- `align_data_and_family(self, _: 'Any') -> 'None'`
- `clear_updaters(self) -> 'Self'`
- `copy(self) -> 'Object3D'`
- `get_family(self) -> 'Iterator[Object3D]'`
- `get_meshes(self) -> 'Iterator[Mesh]'`
- `get_position(self) -> 'Point3D'`
- `get_time_based_updaters(self) -> 'list[MeshTimeBasedUpdater]'`
- `get_updaters(self) -> 'list[MeshUpdater]'`
- `has_time_based_updater(self) -> 'bool'`
- `hierarchical_model_matrix(self) -> 'MatrixMN'`
- `hierarchical_normal_matrix(self) -> 'MatrixMN'`
- `init_updaters(self) -> 'None'`
- `interpolate(self, start: 'Object3D', end: 'Object3D', alpha: 'float', _: 'Any') -> 'None'`
- `match_updaters(self, mesh: 'Object3D') -> 'Self'`
- `refresh_has_updater_status(self) -> 'Self'`
- `remove(self, *children: 'Object3D', current_children_only: 'bool' = True) -> 'None'`
- `remove_updater(self, update_function: 'MeshUpdater') -> 'Self'`
- `resume_updating(self, call_updater: 'bool' = True) -> 'Self'`
- `set_position(self, position: 'Point3D') -> 'Self'`
- `single_copy(self) -> 'Object3D'`
- `suspend_updating(self) -> 'Self'`
- `update(self, dt: 'float' = 0) -> 'Self'`

</details>

### `OpenGLCamera(frame_shape: 'tuple[float, float] | None' = None, center_point: 'Point3DLike | None' = None, euler_angles: 'Point3DLike | None' = None, focal_distance: 'float' = 2.0, light_source_position: 'Point3DLike | None' = None, orthographic: 'bool' = False, minimum_polar_angle: 'float' = -1.5707963267948966, maximum_polar_angle: 'float' = 1.5707963267948966, model_matrix: 'MatrixMN | None' = None, **kwargs: 'Any') -> 'None'` ← OpenGLMobject
> An OpenGL-based camera for 3D scene rendering.

<details><summary>métodos próprios (22) · herdados: 180</summary>

- `__init__(self, frame_shape: 'tuple[float, float] | None' = None, center_point: 'Point3DLike | None' = None, euler_angles: 'Point3DLike | None' = None, focal_distance: 'float' = 2.0, light_source_position: 'Point3DLike | None' = None, orthographic: 'bool' = False, minimum_polar_angle: 'float' = -1.5707963267948966, maximum_polar_angle: 'float' = 1.5707963267948966, model_matrix: 'MatrixMN | None' = None, **kwargs: 'Any') -> 'None'` — Initializes an OpenGLCamera instance.
- `formatted_view_matrix()` — The formatted view matrix for shader input.
- `get_center(self) -> 'Point3D'` — Retrieve the center point of the camera in 3D space.
- `get_focal_distance(self) -> 'float'` — Retrieve the focal distance of the camera.
- `get_height(self) -> 'float'` — Retrieve the height of the camera frame.
- `get_position(self) -> 'Point3D'` — Retrieve the camera's position in 3D space.
- `get_shape(self) -> 'tuple[float, float]'` — Retrieve the width and height of the camera frame.
- `get_width(self) -> 'float'` — Retrieve the width of the camera frame.
- `increment_gamma(self, dgamma: 'float') -> 'Self'` — Increment the camera's gamma Euler angle by a given amount (in radians).
- `increment_phi(self, dphi: 'float') -> 'Self'` — Increment the camera's phi Euler angle by a given amount (in radians).
- `increment_theta(self, dtheta: 'float') -> 'Self'` — Increment the camera's theta Euler angle by a given amount (in radians).
- `init_points(self) -> 'Self'` — Initialize the camera's points based on frame shape and center point.
- `interpolate(self, mobject1: 'OpenGLMobject', mobject2: 'OpenGLMobject', alpha: 'float', path_func: 'PathFuncType' = <function interpolate at 0x713b87942020>) -> 'Self'` — Turns this :class:`~.OpenGLMobject` into an interpolation between ``mobject1``
- `refresh_rotation_matrix(self) -> 'Self'` — Refresh the camera's inverse rotation matrix based on its Euler angles.
- `rotate(self, angle: 'float', axis: 'Vector3DLike' = array([0., 0., 1.]), about_point: 'Point3DLike | None' = None, **kwargs: 'Any') -> 'Self'` — Rotate the camera by a given angle around a specified axis.
- `set_euler_angles(self, theta: 'float | None' = None, phi: 'float | None' = None, gamma: 'float | None' = None) -> 'Self'` — Set the camera's Euler angles [1]_ (theta, phi, gamma).
- `set_gamma(self, gamma: 'float') -> 'Self'` — Set the camera's gamma Euler angle (in radians).
- `set_phi(self, phi: 'float') -> 'Self'` — Set the camera's phi Euler angle (in radians).
- `set_position(self, position: 'Point3D') -> 'Self'` — Set the camera's position in 3D space.
- `set_theta(self, theta: 'float') -> 'Self'` — Set the camera's theta Euler angle (in radians).
- `to_default_state(self) -> 'Self'` — Reset the camera to its default state
- `unformatted_view_matrix()`

</details>

### `OpenGLRenderer(file_writer_class: 'type[SceneFileWriter]' = <class 'manim.scene.scene_file_writer.SceneFileWriter'>, skip_animations: 'bool' = False) -> 'None'`
> An OpenGL-based renderer.

<details><summary>métodos próprios (20) · herdados: 0</summary>

- `__init__(self, file_writer_class: 'type[SceneFileWriter]' = <class 'manim.scene.scene_file_writer.SceneFileWriter'>, skip_animations: 'bool' = False) -> 'None'` — Initializes the OpenGLRenderer.
- `clear_screen(self) -> 'None'` — Clears the current frame buffer and updates the display window
- `get_frame(self) -> 'RGBAPixelArray'` — Get the current frame buffer as a Numpy array of RGBA pixel values.
- `get_frame_buffer_object(self, context: 'moderngl.Context', samples: 'int' = 0) -> 'Framebuffer'` — Creates and returns a framebuffer object configured with color
- `get_image(self) -> 'Image.Image'` — Get the current OpenGL frame buffer as a PIL Image.
- `get_pixel_shape(self) -> 'tuple[int, int] | None'` — Retrieve the pixel dimensions of the current frame buffer object (2D).
- `get_raw_frame_buffer_object_data(self, dtype: 'str' = 'f1') -> 'bytes'` — Get the raw data from the current frame buffer object as bytes.
- `get_texture_id(self, path: 'str') -> 'int'` — Retrieves the OpenGL texture ID associated with the given image file path.
- `init_scene(self, scene: 'Scene') -> 'None'` — Initializes the OpenGL rendering context and related resources
- `pixel_coords_to_space_coords(self, px: 'float', py: 'float', relative: 'bool' = False, top_left: 'bool' = False) -> 'Point3D'` — Converts pixel coordinates to space (scene) coordinates.
- `play(self: 'OpenGLRenderer', scene: 'Scene', *args: 'Any', **kwargs: 'Any') -> 'None'`
- `refresh_perspective_uniforms(self, camera: 'OpenGLCamera') -> 'None'` — Update the perspective-related uniform variables used in the
- `render(self, scene: 'Scene', frame_offset: 'float', moving_mobjects: 'list[Mobject]') -> 'None'` — Renders a single frame of the given scene using OpenGL.
- `render_mobject(self, mobject: 'OpenGLMobject | OpenGLVMobject') -> 'None'` — Render an OpenGL mobject (either OpenGLMobject or OpenGLVMobject)
- `save_static_frame_data(self, scene: 'Scene', static_mobjects: 'Iterable[Mobject]') -> 'None'`
- `scene_finished(self, scene: 'Scene') -> 'None'` — Handle the finalization process after a scene has finished rendering.
- `should_create_window(self) -> 'bool'` — Determine whether a window should be created for rendering
- `should_save_last_frame(self) -> 'bool'` — Determine whether the last frame of the scene should be saved,
- `update_frame(self, scene: 'Scene') -> 'None'` — Update and render the current frame for the given scene.
- `update_skipping_status(self) -> 'None'` — Check and update the skipping status for the current animation

</details>

### `Shader(context: 'moderngl.Context', name: 'str | None' = None, source: 'dict[str, Any] | None' = None)`

<details><summary>métodos próprios (2) · herdados: 0</summary>

- `__init__(self, context: 'moderngl.Context', name: 'str | None' = None, source: 'dict[str, Any] | None' = None)` — Initialize self.  See help(type(self)) for accurate signature.
- `set_uniform(self, name: 'str', value: 'Any') -> 'None'`

</details>

### `ShaderWrapper(vert_data: '_ShaderData' = None, vert_indices: 'Sequence[int] | None' = None, shader_folder: 'Path | str | None' = None, uniforms: 'dict[str, float | tuple[float, ...]] | None' = None, texture_paths: 'Mapping[str, Path | str] | None' = None, depth_test: 'bool' = False, render_primitive: 'int | str' = 5)`

<details><summary>métodos próprios (12) · herdados: 0</summary>

- `__init__(self, vert_data: '_ShaderData' = None, vert_indices: 'Sequence[int] | None' = None, shader_folder: 'Path | str | None' = None, uniforms: 'dict[str, float | tuple[float, ...]] | None' = None, texture_paths: 'Mapping[str, Path | str] | None' = None, depth_test: 'bool' = False, render_primitive: 'int | str' = 5)` — Initialize self.  See help(type(self)) for accurate signature.
- `combine_with(self, *shader_wrappers: "'ShaderWrapper'") -> 'Self'`
- `copy(self)`
- `create_id(self)`
- `create_program_id(self)`
- `get_id(self) -> 'str'`
- `get_program_code(self)`
- `get_program_id(self) -> 'int'`
- `init_program_code(self)`
- `is_valid(self) -> 'bool'`
- `refresh_id(self) -> 'None'`
- `replace_code(self, old: 'str', new: 'str') -> 'None'`

</details>

### `Window(renderer: 'OpenGLRenderer', window_size: 'str | tuple[int, ...]' = 'default', **kwargs: 'Any') -> 'None'` ← Window
> Window based on Pyglet 1.4.x

<details><summary>métodos próprios (18) · herdados: 12</summary>

- `__init__(self, renderer: 'OpenGLRenderer', window_size: 'str | tuple[int, ...]' = 'default', **kwargs: 'Any') -> 'None'` — Initialize a window instance.
- `close(self) -> None` — Close the pyglet window directly
- `destroy(self) -> None` — Destroy the pyglet window
- `find_initial_position(self, size: 'tuple[int, int]', monitor: 'Monitor') -> 'tuple[int, int]'`
- `on_close(self) -> None` — Pyglet specific window close callback
- `on_file_drop(self, x: int, y: int, paths: list[typing.Union[str, pathlib.Path]]) -> None` — Called when files dropped onto the window
- `on_hide(self) -> None` — Called when window is minimized
- `on_key_press(self, symbol: 'int', modifiers: 'int') -> 'bool'` — Pyglet specific key press callback.
- `on_key_release(self, symbol: 'int', modifiers: 'int') -> 'None'` — Pyglet specific key release callback.
- `on_mouse_drag(self, x: 'int', y: 'int', dx: 'int', dy: 'int', buttons: 'int', modifiers: 'int') -> 'None'` — Pyglet specific mouse drag event.
- `on_mouse_motion(self, x: 'int', y: 'int', dx: 'int', dy: 'int') -> 'None'` — Pyglet specific mouse motion callback.
- `on_mouse_press(self, x: 'int', y: 'int', button: 'int', modifiers: 'int') -> 'None'` — Handle mouse press events and forward to standard methods
- `on_mouse_release(self, x: int, y: int, button: int, mods: int) -> None` — Handle mouse release events and forward to standard methods
- `on_mouse_scroll(self, x: 'int', y: 'int', x_offset: 'float', y_offset: 'float') -> 'None'` — Handle mouse wheel.
- `on_resize(self, width: int, height: int) -> None` — Pyglet specific callback for window resize events forwarding to standard methods
- `on_show(self) -> None` — Called when window first appear or restored from hidden state
- `on_text(self, text: str) -> None` — Pyglet specific text input callback
- `swap_buffers(self) -> None` — Swap buffers, increment frame counter and pull events

</details>

- `BOLD` = `'BOLD'`
- `BOOK` = `'BOOK'`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CTRL_VALUE` = `65507`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `HEAVY` = `'HEAVY'`
- `IN` = `array([ 0.,  0., -1.])`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LIGHT` = `'LIGHT'`
- `MEDIUM` = `'MEDIUM'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OBLIQUE` = `'OBLIQUE'`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RIGHT` = `array([1., 0., 0.])`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SHADER_FOLDER` = `PosixPath('<site-packages>/manim/renderer/shaders')`
- `SHIFT_VALUE` = `65505`
- `SMALL_BUFF` = `0.1`
- `START_X` = `30`
- `START_Y` = `20`
- `TAU` = `6.283185307179586`
- `THIN` = `'THIN'`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- **`build_matrix_lists(mob: 'OpenGLVMobject') -> 'defaultdict[tuple[float, ...], list[OpenGLVMobject]]'`**
- **`filter_attributes(unfiltered_attributes: 'npt.NDArray', attributes: 'Sequence[str]') -> 'npt.NDArray'`**
- **`find_file(file_name: 'Path', directories: 'list[Path]') -> 'Path'`**
- **`get_colormap_code(rgb_list: 'FloatRGBLike_Array') -> 'str'`**
- **`get_shader_code_from_file(file_path: 'Path') -> 'str'`**
- **`get_shader_code_from_file(filename: 'Path') -> 'str | None'`**
- **`get_shader_dir()`**
- **`render_mobject_fills_with_matrix(renderer: 'OpenGLRenderer', model_matrix: 'MatrixMN', mobjects: 'Iterable[OpenGLVMobject]') -> 'None'`**
- **`render_mobject_strokes_with_matrix(renderer: 'OpenGLRenderer', model_matrix: 'MatrixMN', mobjects: 'Sequence[OpenGLVMobject]') -> 'None'`**
- **`render_opengl_vectorized_mobject_fill(renderer: 'OpenGLRenderer', mobject: 'OpenGLVMobject') -> 'None'`**
- **`render_opengl_vectorized_mobject_stroke(renderer: 'OpenGLRenderer', mobject: 'OpenGLVMobject') -> 'None'`**
- **`triangulate_mobject(mob: 'OpenGLVMobject') -> 'np.ndarray'`**

## scene

### `DefaultSectionType(*values)` ← StrEnum
> The type of a section can be used for third party applications.

### `LinearTransformationScene(include_background_plane: 'bool' = True, include_foreground_plane: 'bool' = True, background_plane_kwargs: 'dict[str, Any] | None' = None, foreground_plane_kwargs: 'dict[str, Any] | None' = None, show_coordinates: 'bool' = False, show_basis_vectors: 'bool' = True, basis_vector_stroke_width: 'float' = 6, i_hat_color: 'ParsableManimColor' = ManimColor('#83C167'), j_hat_color: 'ParsableManimColor' = ManimColor('#FC6255'), leave_ghost_vectors: 'bool' = False, **kwargs: 'Any') -> 'None'` ← VectorScene
> This scene contains special methods that make it

<details><summary>métodos próprios (27) · herdados: 68</summary>

- `__init__(self, include_background_plane: 'bool' = True, include_foreground_plane: 'bool' = True, background_plane_kwargs: 'dict[str, Any] | None' = None, foreground_plane_kwargs: 'dict[str, Any] | None' = None, show_coordinates: 'bool' = False, show_basis_vectors: 'bool' = True, basis_vector_stroke_width: 'float' = 6, i_hat_color: 'ParsableManimColor' = ManimColor('#83C167'), j_hat_color: 'ParsableManimColor' = ManimColor('#FC6255'), leave_ghost_vectors: 'bool' = False, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `add_background_mobject(self, *mobjects: 'Mobject') -> 'None'` — Adds the mobjects to the special list
- `add_foreground_mobject(self, *mobjects: 'Mobject') -> 'None'` — Adds the mobjects to the special list
- `add_moving_mobject(self, mobject: 'Mobject', target_mobject: 'Mobject | None' = None) -> 'None'` — Adds the mobject to the special list
- `add_special_mobjects(self, mob_list: 'list[Mobject]', *mobs_to_add: 'Mobject') -> 'None'` — Adds mobjects to a separate list that can be tracked,
- `add_title(self, title: 'str | MathTex | Tex', scale_factor: 'float' = 1.5, animate: 'bool' = False) -> 'Self'` — Adds a title, after scaling it, adding a background rectangle,
- `add_transformable_label(self, vector: 'Vector', label: 'MathTex | str', transformation_name: 'str | MathTex' = 'L', new_label: 'str | MathTex | None' = None, **kwargs: 'Any') -> 'MathTex'` — Method for creating, and animating the addition of
- `add_transformable_mobject(self, *mobjects: 'Mobject') -> 'None'` — Adds the mobjects to the special list
- `add_unit_square(self, animate: 'bool' = False, **kwargs: 'Any') -> 'Self'` — Adds a unit square to the scene via
- `add_vector(self, vector: 'Arrow | list | tuple | np.ndarray', color: 'ParsableManimColor' = ManimColor('#FFFF00'), animate: 'bool' = False, **kwargs: 'Any') -> 'Arrow'` — Adds a vector to the scene, and puts it in the special
- `apply_function(self, function: 'MappingFunction', added_anims: 'list[Animation]' = [], **kwargs: 'Any') -> 'None'` — Applies the given function to each of the mobjects in
- `apply_inverse(self, matrix: 'np.ndarray | list | tuple', **kwargs: 'Any') -> 'None'` — This method applies the linear transformation
- `apply_inverse_transpose(self, t_matrix: 'np.ndarray | list | tuple', **kwargs: 'Any') -> 'None'` — Applies the inverse of the transformation represented
- `apply_matrix(self, matrix: 'np.ndarray | list | tuple', **kwargs: 'Any') -> 'None'` — Applies the transformation represented by the
- `apply_nonlinear_transformation(self, function: 'Callable[[np.ndarray], np.ndarray]', **kwargs: 'Any') -> 'None'` — Applies the non-linear transformation represented
- `apply_transposed_matrix(self, transposed_matrix: 'np.ndarray | list | tuple', **kwargs: 'Any') -> 'None'` — Applies the transformation represented by the
- `get_ghost_vectors(self) -> 'VGroup'` — Returns all ghost vectors ever added to ``self``. Each element is a ``VGroup`` of
- `get_matrix_transformation(self, matrix: 'np.ndarray | list | tuple') -> 'Callable[[Point3D], Point3D]'` — Returns a function corresponding to the linear
- `get_moving_mobject_movement(self, func: 'MappingFunction') -> 'Transform'` — This method returns an animation that moves a mobject
- `get_piece_movement(self, pieces: 'Iterable[Mobject]') -> 'Transform'` — This method returns an animation that moves an arbitrary
- `get_transformable_label_movement(self) -> 'Transform'` — This method returns an animation that moves all labels
- `get_transposed_matrix_transformation(self, transposed_matrix: 'np.ndarray | list | tuple') -> 'Callable[[Point3D], Point3D]'` — Returns a function corresponding to the linear
- `get_unit_square(self, color: 'ParsableManimColor | Iterable[ParsableManimColor]' = ManimColor('#FFFF00'), opacity: 'float' = 0.3, stroke_width: 'float' = 3) -> 'Rectangle'` — Returns a unit square for the current NumberPlane.
- `get_vector_movement(self, func: 'MappingFunction') -> 'Transform'` — This method returns an animation that moves a mobject
- `setup(self) -> 'None'` — This is meant to be implemented by any scenes which
- `update_default_configs(default_configs: 'Iterable[dict[str, Any]]', passed_configs: 'Iterable[dict[str, Any] | None]') -> 'None'`
- `write_vector_coordinates(self, vector: 'Vector', **kwargs: 'Any') -> 'Matrix'` — Returns a column matrix indicating the vector coordinates,

</details>

### `MovingCameraScene(camera_class: 'type[Camera]' = <class 'manim.camera.moving_camera.MovingCamera'>, **kwargs: 'Any') -> 'None'` ← Scene
> This is a Scene, with special configurations and properties that

<details><summary>métodos próprios (2) · herdados: 56</summary>

- `__init__(self, camera_class: 'type[Camera]' = <class 'manim.camera.moving_camera.MovingCamera'>, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `get_moving_mobjects(self, *animations: 'Animation') -> 'list[Mobject]'` — This method returns a list of all of the Mobjects in the Scene that

</details>

### `RerunSceneHandler(queue: 'Queue[SceneInteractAction]') -> 'None'` ← FileSystemEventHandler
> A class to handle rerunning a Scene after the input file is modified.

<details><summary>métodos próprios (2) · herdados: 8</summary>

- `__init__(self, queue: 'Queue[SceneInteractAction]') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `on_modified(self, event: 'DirModifiedEvent | FileModifiedEvent') -> 'None'` — Called when a file or directory is modified.

</details>

### `Scene(renderer: 'CairoRenderer | OpenGLRenderer | None' = None, camera_class: 'type[Camera]' = <class 'manim.camera.camera.Camera'>, always_update_mobjects: 'bool' = False, random_seed: 'int | None' = None, skip_animations: 'bool' = False) -> 'None'`
> A Scene is the canvas of your animation.

<details><summary>métodos próprios (58) · herdados: 0</summary>

- `__init__(self, renderer: 'CairoRenderer | OpenGLRenderer | None' = None, camera_class: 'type[Camera]' = <class 'manim.camera.camera.Camera'>, always_update_mobjects: 'bool' = False, random_seed: 'int | None' = None, skip_animations: 'bool' = False) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `add(self, *mobjects: 'Mobject | OpenGLMobject') -> 'Self'` — Mobjects will be displayed, from background to
- `add_foreground_mobject(self, mobject: 'Mobject') -> 'Scene'` — Adds a single mobject to the foreground, and internally to the list
- `add_foreground_mobjects(self, *mobjects: 'Mobject') -> 'Scene'` — Adds mobjects to the foreground, and internally to the list
- `add_mobjects_from_animations(self, animations: 'list[Animation]') -> 'None'`
- `add_sound(self, sound_file: 'str', time_offset: 'float' = 0, gain: 'float | None' = None, **kwargs: 'Any') -> 'None'` — This method is used to add a sound to the animation.
- `add_subcaption(self, content: 'str', duration: 'float' = 1, offset: 'float' = 0) -> 'None'` — Adds an entry in the corresponding subcaption file
- `add_updater(self, func: 'Callable[[float], None]') -> 'None'` — Add an update function to the scene.
- `begin_animations(self) -> 'None'` — Start the animations of the scene.
- `bring_to_back(self, *mobjects: 'Mobject') -> 'Scene'` — Removes the mobject from the scene and
- `bring_to_front(self, *mobjects: 'Mobject') -> 'Scene'` — Adds the passed mobjects to the scene again,
- `check_interactive_embed_is_valid(self) -> 'bool'`
- `clear(self) -> 'Self'` — Removes all mobjects present in self.mobjects
- `compile_animation_data(self, *animations: 'Animation | Mobject | _AnimationBuilder', **play_kwargs: 'Any') -> 'Self | None'` — Given a list of animations, compile the corresponding
- `compile_animations(self, *args: 'Animation | Mobject | _AnimationBuilder', **kwargs: 'Any') -> 'list[Animation]'` — Creates _MethodAnimations from any _AnimationBuilders and updates animation
- `construct(self) -> 'None'` — Add content to the Scene.
- `embed(self) -> 'None'`
- `get_attrs(self, *keys: 'str') -> 'list[Any]'` — Gets attributes of a scene given the attribute's identifier/name.
- `get_mobject_family_members(self) -> 'list[Mobject]'` — Returns list of family-members of all mobjects in scene.
- `get_moving_and_static_mobjects(self, animations: 'Iterable[Animation]') -> 'tuple[list[Mobject], list[Mobject]]'`
- `get_moving_mobjects(self, *animations: 'Animation') -> 'list[Mobject]'` — Gets all moving mobjects in the passed animation(s).
- `get_restructured_mobject_list(self, mobjects: 'Iterable[Mobject]', to_remove: 'Iterable[Mobject]') -> 'list[Mobject]'` — Given a list of mobjects and a list of mobjects to be removed, this
- `get_run_time(self, animations: 'list[Animation]') -> 'float'` — Gets the total run time for a list of animations.
- `get_time_progression(self, run_time: 'float', description: 'str', n_iterations: 'int | None' = None, override_skip_animations: 'bool' = False) -> 'tqdm[float]'` — You will hardly use this when making your own animations.
- `get_top_level_mobjects(self) -> 'list[Mobject]'` — Returns all mobjects which are not submobjects.
- `interact(self, shell: 'Any', keyboard_thread: 'threading.Thread') -> 'None'`
- `interactive_embed(self) -> 'None'` — Like embed(), but allows for screen interaction.
- `is_current_animation_frozen_frame(self) -> 'bool'` — Returns whether the current animation produces a static frame (generally a Wait).
- `mouse_drag_orbit_controls(self, point: 'Point3D', d_point: 'Point3D', buttons: 'int', modifiers: 'int') -> 'None'`
- `mouse_scroll_orbit_controls(self, point: 'Point3D', offset: 'Point3D') -> 'None'`
- `next_section(self, name: 'str' = 'unnamed', section_type: 'str' = <DefaultSectionType.NORMAL: 'default.normal'>, skip_animations: 'bool' = False) -> 'None'` — Create separation here; the last section gets finished and a new one gets created.
- `on_key_press(self, symbol: 'int', modifiers: 'int') -> 'None'`
- `on_key_release(self, symbol: 'int', modifiers: 'int') -> 'None'`
- `on_mouse_drag(self, point: 'Point3D', d_point: 'Point3D', buttons: 'int', modifiers: 'int') -> 'None'`
- `on_mouse_motion(self, point: 'Point3D', d_point: 'Point3D') -> 'None'`
- `on_mouse_press(self, point: 'Point3D', button: 'str', modifiers: 'int') -> 'None'`
- `on_mouse_scroll(self, point: 'Point3D', offset: 'Point3D') -> 'None'`
- `pause(self, duration: 'float' = 1.0) -> 'None'` — Pauses the scene (i.e., displays a frozen frame).
- `play(self, *args: 'Animation | Mobject | _AnimationBuilder', subcaption: 'str | None' = None, subcaption_duration: 'float | None' = None, subcaption_offset: 'float' = 0, **kwargs: 'Any') -> 'None'` — Plays an animation in this scene.
- `play_internal(self, skip_rendering: 'bool' = False) -> 'None'` — This method is used to prep the animations for rendering,
- `remove(self, *mobjects: 'Mobject') -> 'Self'` — Removes mobjects in the passed list of mobjects
- `remove_foreground_mobject(self, mobject: 'Mobject') -> 'Scene'` — Removes a single mobject from the foreground, and internally from the list
- `remove_foreground_mobjects(self, *to_remove: 'Mobject') -> 'Scene'` — Removes mobjects from the foreground, and internally from the list
- `remove_updater(self, func: 'Callable[[float], None]') -> 'None'` — Remove an update function from the scene.
- `render(self, preview: 'bool' = False) -> 'bool'` — Renders this Scene.
- `replace(self, old_mobject: 'Mobject', new_mobject: 'Mobject') -> 'None'` — Replace one mobject in the scene with another, preserving draw order.
- `restructure_mobjects(self, to_remove: 'Sequence[Mobject]', mobject_list_name: 'str' = 'mobjects', extract_families: 'bool' = True) -> 'Scene'` — tl:wr
- `set_key_function(self, char: 'str', func: 'Callable[[], Any]') -> 'None'`
- `setup(self) -> 'None'` — This is meant to be implemented by any scenes which
- `should_update_mobjects(self) -> 'bool'` — Returns True if the mobjects of this scene should be updated.
- `tear_down(self) -> 'None'` — This is meant to be implemented by any scenes which
- `update_meshes(self, dt: 'float') -> 'None'`
- `update_mobjects(self, dt: 'float') -> 'None'` — Begins updating all mobjects in the Scene.
- `update_self(self, dt: 'float') -> 'None'` — Run all scene updater functions.
- `update_to_time(self, t: 'float') -> 'None'`
- `validate_run_time(run_time: 'float', method: 'Callable[[Any], Any]', parameter_name: 'str' = 'run_time') -> 'float'`
- `wait(self, duration: 'float' = 1.0, stop_condition: 'Callable[[], bool] | None' = None, frozen_frame: 'bool | None' = None) -> 'None'` — Plays a "no operation" animation.
- `wait_until(self, stop_condition: 'Callable[[], bool]', max_time: 'float' = 60) -> 'None'` — Wait until a condition is satisfied, up to a given maximum duration.

</details>

### `SceneFileWriter(renderer: 'CairoRenderer | OpenGLRenderer', scene_name: 'str', **kwargs: 'Any') -> 'None'`
> SceneFileWriter is the object that actually writes the animations

<details><summary>métodos próprios (28) · herdados: 0</summary>

- `__init__(self, renderer: 'CairoRenderer | OpenGLRenderer', scene_name: 'str', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `abort_encode_jobs(self, reraise_encoder_failures: 'bool' = False) -> 'None'` — Tear down encode jobs after an aborted or rerun render.
- `add_audio_segment(self, new_segment: 'AudioSegment', time: 'float | None' = None, gain_to_background: 'float | None' = None) -> 'None'` — This method adds an audio segment from an AudioSegment type object
- `add_partial_movie_file(self, hash_animation: 'str | None') -> 'None'` — Adds a new partial movie file path to ``scene.partial_movie_files``
- `add_sound(self, sound_file: 'StrPath', time: 'float | None' = None, gain: 'float | None' = None, **kwargs: 'Any') -> 'None'` — This method adds an audio segment from a sound file.
- `begin_animation(self, allow_write: 'bool' = False, file_path: 'StrPath | None' = None) -> 'None'` — Used internally by manim to stream the animation to FFMPEG for
- `clean_cache(self) -> 'None'` — Will clean the cache by removing the oldest partial_movie_files.
- `close_partial_movie_stream(self) -> 'None'` — Close the currently opened video container.
- `combine_files(self, input_files: 'list[str]', output_file: 'Path', create_gif: 'bool' = False, includes_sound: 'bool' = False) -> 'None'`
- `combine_to_movie(self) -> 'None'` — Used internally by Manim to combine the separate
- `combine_to_section_videos(self) -> 'None'` — Concatenate partial movie files for each section.
- `create_audio_segment(self) -> 'None'` — Creates an empty, silent, Audio Segment.
- `end_animation(self, allow_write: 'bool' = False) -> 'None'` — Internally used by Manim to stop streaming to FFMPEG gracefully.
- `finish(self) -> 'None'` — Finishes writing to the FFMPEG buffer or writing images to output directory.
- `finish_last_section(self) -> 'None'` — Delete current section if it is empty.
- `flush_cache_directory(self) -> 'None'` — Delete all the cached partial movie files
- `get_resolution_directory(self) -> 'str'` — Get the name of the resolution directory directly containing
- `init_audio(self) -> 'None'` — Preps the writer for adding audio to the movie.
- `init_output_directories(self, scene_name: 'str') -> 'None'` — Initialise output directories.
- `is_already_cached(self, hash_invocation: 'str') -> 'bool'` — Will check if a file named with `hash_invocation` exists.
- `join_all_encode_jobs(self) -> 'None'` — Join every in-flight encode job, re-raising the first failure.
- `next_section(self, name: 'str', type_: 'str', skip_animations: 'bool') -> 'None'` — Create segmentation cut here.
- `open_partial_movie_stream(self, file_path: 'StrPath | None' = None) -> 'None'` — Open a container holding a video stream.
- `output_image(self, image: 'Image.Image', target_dir: 'StrPath', ext: 'str', zero_pad: 'int') -> 'None'`
- `print_file_ready_message(self, file_path: 'StrPath') -> 'None'` — Prints the "File Ready" message to STDOUT.
- `save_image(self, image: 'Image.Image') -> 'None'` — This method saves the image passed to it in the default image directory.
- `write_frame(self, frame_or_renderer: 'PixelArray | OpenGLRenderer', num_frames: 'int' = 1) -> 'None'` — Used internally by Manim to write a frame to the FFMPEG input buffer.
- `write_subcaption_file(self) -> 'None'` — Writes the subcaption file.

</details>

### `SceneInteractContinue(sender: 'str') -> None`
> Object which, when encountered in :meth:`.Scene.interact`, triggers

<details><summary>métodos próprios (1) · herdados: 0</summary>

- `__init__(self, sender: 'str') -> None` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `SceneInteractRerun(sender: 'str', **kwargs: 'Any') -> 'None'`
> Object which, when encountered in :meth:`.Scene.interact`, triggers

<details><summary>métodos próprios (1) · herdados: 0</summary>

- `__init__(self, sender: 'str', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Section(type_: 'str', video: 'str | None', name: 'str', skip_animations: 'bool') -> 'None'`
> A :class:`.Scene` can be segmented into multiple Sections.

<details><summary>métodos próprios (4) · herdados: 0</summary>

- `__init__(self, type_: 'str', video: 'str | None', name: 'str', skip_animations: 'bool') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `get_clean_partial_movie_files(self) -> 'list[str]'` — Return all partial movie files that are not ``None``.
- `get_dict(self, sections_dir: 'Path') -> 'dict[str, Any]'` — Get dictionary representation with metadata of output video.
- `is_empty(self) -> 'bool'` — Check whether this section is empty.

</details>

### `SpecialThreeDScene(cut_axes_at_radius=True, camera_config={'should_apply_shading': True, 'exponential_projection': True}, three_d_axes_config={'num_axis_pieces': 1, 'axis_config': {'unit_size': 2, 'tick_frequency': 1, 'numbers_with_elongated_ticks': [0, 1, 2], 'stroke_width': 2}}, sphere_config={'radius': 2, 'resolution': (24, 48)}, default_angled_camera_position={'phi': 1.2217304763960306, 'theta': -1.9198621771937625}, low_quality_config={'camera_config': {'should_apply_shading': False}, 'three_d_axes_config': {'num_axis_pieces': 1}, 'sphere_config': {'resolution': (12, 24)}}, **kwargs)` ← ThreeDScene
> An extension of :class:`ThreeDScene` with more settings.

<details><summary>métodos próprios (5) · herdados: 68</summary>

- `__init__(self, cut_axes_at_radius=True, camera_config={'should_apply_shading': True, 'exponential_projection': True}, three_d_axes_config={'num_axis_pieces': 1, 'axis_config': {'unit_size': 2, 'tick_frequency': 1, 'numbers_with_elongated_ticks': [0, 1, 2], 'stroke_width': 2}}, sphere_config={'radius': 2, 'resolution': (24, 48)}, default_angled_camera_position={'phi': 1.2217304763960306, 'theta': -1.9198621771937625}, low_quality_config={'camera_config': {'should_apply_shading': False}, 'three_d_axes_config': {'num_axis_pieces': 1}, 'sphere_config': {'resolution': (12, 24)}}, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `get_axes(self)` — Return a set of 3D axes.
- `get_default_camera_position(self)` — Returns the default_angled_camera position.
- `get_sphere(self, **kwargs)` — Returns a sphere with the passed keyword arguments as properties.
- `set_camera_to_default_position(self)` — Sets the camera to its default position.

</details>

### `ThreeDScene(camera_class=<class 'manim.camera.three_d_camera.ThreeDCamera'>, ambient_camera_rotation=None, default_angled_camera_orientation_kwargs=None, **kwargs)` ← Scene
> This is a Scene, with special configurations and properties that

<details><summary>métodos próprios (13) · herdados: 56</summary>

- `__init__(self, camera_class=<class 'manim.camera.three_d_camera.ThreeDCamera'>, ambient_camera_rotation=None, default_angled_camera_orientation_kwargs=None, **kwargs)` — Initialize self.  See help(type(self)) for accurate signature.
- `add_fixed_in_frame_mobjects(self, *mobjects: 'Mobject')` — This method is used to prevent the rotation and movement
- `add_fixed_orientation_mobjects(self, *mobjects: 'Mobject', **kwargs)` — This method is used to prevent the rotation and tilting
- `begin_3dillusion_camera_rotation(self, rate: 'float' = 1, origin_phi: 'float | None' = None, origin_theta: 'float | None' = None)` — This method creates a 3D camera rotation illusion around
- `begin_ambient_camera_rotation(self, rate: 'float' = 0.02, about: 'str' = 'theta')` — This method begins an ambient rotation of the camera about the Z_AXIS,
- `get_moving_mobjects(self, *animations: 'Animation')` — This method returns a list of all of the Mobjects in the Scene that
- `move_camera(self, phi: 'float | None' = None, theta: 'float | None' = None, gamma: 'float | None' = None, zoom: 'float | None' = None, focal_distance: 'float | None' = None, frame_center: 'Mobject | Sequence[float] | None' = None, added_anims: 'Iterable[Animation]' = [], **kwargs)` — This method animates the movement of the camera
- `remove_fixed_in_frame_mobjects(self, *mobjects: 'Mobject')` — This method undoes what add_fixed_in_frame_mobjects does.
- `remove_fixed_orientation_mobjects(self, *mobjects: 'Mobject')` — This method "unfixes" the orientation of the mobjects
- `set_camera_orientation(self, phi: 'float | None' = None, theta: 'float | None' = None, gamma: 'float | None' = None, zoom: 'float | None' = None, focal_distance: 'float | None' = None, frame_center: 'Mobject | Sequence[float] | None' = None, **kwargs)` — This method sets the orientation of the camera in the scene.
- `set_to_default_angled_camera_orientation(self, **kwargs)` — This method sets the default_angled_camera_orientation to the
- `stop_3dillusion_camera_rotation(self)` — This method stops all illusion camera rotations.
- `stop_ambient_camera_rotation(self, about='theta')` — This method stops all ambient camera rotation.

</details>

### `VectorScene(basis_vector_stroke_width: 'float' = 6.0, **kwargs: 'Any') -> 'None'` ← Scene
> A Scene is the canvas of your animation.

<details><summary>métodos próprios (16) · herdados: 57</summary>

- `__init__(self, basis_vector_stroke_width: 'float' = 6.0, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `add_axes(self, animate: 'bool' = False, color: 'ParsableManimColor | Iterable[ParsableManimColor]' = ManimColor('#FFFFFF')) -> 'Axes'` — Adds a pair of Axes to the Scene.
- `add_plane(self, animate: 'bool' = False, **kwargs: 'Any') -> 'NumberPlane'` — Adds a NumberPlane object to the background.
- `add_vector(self, vector: 'Arrow | Vector3DLike', color: 'ParsableManimColor | Iterable[ParsableManimColor]' = ManimColor('#FFFF00'), animate: 'bool' = True, **kwargs: 'Any') -> 'Arrow'` — Returns the Vector after adding it to the Plane.
- `coords_to_vector(self, vector: 'Vector2DLike', coords_start: 'Point3DLike' = array([2., 2., 0.]), clean_up: 'bool' = True) -> 'None'` — This method writes the vector as a column matrix (henceforth called the label),
- `get_basis_vector_labels(self, **kwargs: 'Any') -> 'VGroup'` — Returns naming labels for the basis vectors.
- `get_basis_vectors(self, i_hat_color: 'ParsableManimColor | Iterable[ParsableManimColor]' = ManimColor('#83C167'), j_hat_color: 'ParsableManimColor | Iterable[ParsableManimColor]' = ManimColor('#FC6255')) -> 'VGroup'` — Returns a VGroup of the Basis Vectors (1,0) and (0,1)
- `get_vector(self, numerical_vector: 'Vector3DLike', **kwargs: 'Any') -> 'Arrow'` — Returns an arrow on the Plane given an input numerical vector.
- `get_vector_label(self, vector: 'Vector', label: 'ManimTextLabel | str', at_tip: 'bool' = False, direction: 'str' = 'left', rotate: 'bool' = False, color: 'ParsableManimColor | None' = None, label_scale_factor: 'float' = 0.8) -> 'ManimTextLabel'` — Returns naming labels for the passed vector.
- `label_vector(self, vector: 'Vector', label: 'ManimTextLabel | str', animate: 'bool' = True, **kwargs: 'Any') -> 'ManimTextLabel'` — Shortcut method for creating, and animating the addition of
- `lock_in_faded_grid(self, dimness: 'float' = 0.7, axes_dimness: 'float' = 0.5) -> 'None'` — This method freezes the NumberPlane and Axes that were already
- `position_x_coordinate(self, x_coord: 'MathTex', x_line: 'Line', vector: 'Vector3DLike') -> 'MathTex'`
- `position_y_coordinate(self, y_coord: 'MathTex', y_line: 'Line', vector: 'Vector3DLike') -> 'MathTex'`
- `show_ghost_movement(self, vector: 'Arrow | Vector2DLike | Vector3DLike') -> 'None'` — This method plays an animation that partially shows the entire plane moving
- `vector_to_coords(self, vector: 'Vector3DLike', integer_labels: 'bool' = True, clean_up: 'bool' = True) -> 'tuple[Matrix, Line, Line]'` — This method displays vector as a Vector() based vector, and then shows
- `write_vector_coordinates(self, vector: 'Vector', **kwargs: 'Any') -> 'Matrix'` — Returns a column matrix indicating the vector coordinates,

</details>

### `ZoomedScene(camera_class: 'type[Camera]' = <class 'manim.camera.multi_camera.MultiCamera'>, zoomed_display_height: 'float' = 3, zoomed_display_width: 'float' = 3, zoomed_display_center: 'Point3DLike | None' = None, zoomed_display_corner: 'Vector3D' = array([1., 1., 0.]), zoomed_display_corner_buff: 'float' = 0.5, zoomed_camera_config: 'dict[str, Any]' = {'default_frame_stroke_width': 2, 'background_opacity': 1}, zoomed_camera_image_mobject_config: 'dict[str, Any]' = {}, zoomed_camera_frame_starting_position: 'Point3DLike' = array([0., 0., 0.]), zoom_factor: 'float' = 0.15, image_frame_stroke_width: 'float' = 3, zoom_activated: 'bool' = False, **kwargs: 'Any') -> 'None'` ← MovingCameraScene
> This is a Scene with special configurations made for when

<details><summary>métodos próprios (6) · herdados: 56</summary>

- `__init__(self, camera_class: 'type[Camera]' = <class 'manim.camera.multi_camera.MultiCamera'>, zoomed_display_height: 'float' = 3, zoomed_display_width: 'float' = 3, zoomed_display_center: 'Point3DLike | None' = None, zoomed_display_corner: 'Vector3D' = array([1., 1., 0.]), zoomed_display_corner_buff: 'float' = 0.5, zoomed_camera_config: 'dict[str, Any]' = {'default_frame_stroke_width': 2, 'background_opacity': 1}, zoomed_camera_image_mobject_config: 'dict[str, Any]' = {}, zoomed_camera_frame_starting_position: 'Point3DLike' = array([0., 0., 0.]), zoom_factor: 'float' = 0.15, image_frame_stroke_width: 'float' = 3, zoom_activated: 'bool' = False, **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `activate_zooming(self, animate: 'bool' = False) -> 'None'` — This method is used to activate the zooming for the zoomed_camera.
- `get_zoom_factor(self) -> 'float'` — Returns the Zoom factor of the Zoomed camera.
- `get_zoom_in_animation(self, run_time: 'float' = 2, **kwargs: 'Any') -> 'ApplyMethod'` — Returns the animation of camera zooming in.
- `get_zoomed_display_pop_out_animation(self, **kwargs: 'Any') -> 'ApplyMethod'` — This is the animation of the popping out of the mini-display that
- `setup(self) -> 'None'` — This method is used internally by Manim to

</details>

- `BLACK` = `ManimColor('#000000')`
- `BLUE_D` = `ManimColor('#29ABCA')`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOLD` = `'BOLD'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `BOOK` = `'BOOK'`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CONTEXT_SETTINGS` = `{'align_option_groups': True, 'align_sections': True, 'show_constraints': True}`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `CTRL_VALUE` = `65507`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_ARROW_TIP_LENGTH` = `0.35`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DASH_LENGTH` = `0.05`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_DOT_RADIUS` = `0.08`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_FONT_SIZE` = `48`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_EDGE_BUFFER` = `0.5`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER` = `0.25`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINTWISE_FUNCTION_RUN_TIME` = `3.0`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_1D` = `10`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_POINT_DENSITY_2D` = `25`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_QUALITY` = `'high_quality'`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_SMALL_DOT_RADIUS` = `0.04`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_STROKE_WIDTH` = `4`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEFAULT_WAIT_TIME` = `1.0`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DEGREES` = `0.017453292519943295`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DL` = `array([-1., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DOWN` = `array([ 0., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `DR` = `array([ 1., -1.,  0.])`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `EPILOG` = `'Made with <3 by Manim Community developers.'`
- `GREEN_C` = `ManimColor('#83C167')`
- `GREY` = `ManimColor('#888888')`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `HEAVY` = `'HEAVY'`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `IN` = `array([ 0.,  0., -1.])`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `ITALIC` = `'ITALIC'`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LARGE_BUFF` = `1`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LEFT` = `array([-1.,  0.,  0.])`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `LIGHT` = `'LIGHT'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MEDIUM` = `'MEDIUM'`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_LARGE_BUFF` = `0.5`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `MED_SMALL_BUFF` = `0.25`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NORMAL` = `'NORMAL'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `OBLIQUE` = `'OBLIQUE'`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `ORIGIN` = `array([0., 0., 0.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PI` = `3.141592653589793`
- `PURE_YELLOW` = `ManimColor('#FFFF00')`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `QUALITIES` = `{'fourk_quality': {'flag': 'k', 'pixel_height': 2160, 'pixel_width': 3840, 'frame_rate': 60}, 'production_quality': {...`
- `RED_C` = `ManimColor('#FC6255')`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RESAMPLING_ALGORITHMS` = `{'nearest': <Resampling.NEAREST: 0>, 'none': <Resampling.NEAREST: 0>, 'bilinear': <Resampling.BILINEAR: 2>, 'linear':...`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `RIGHT` = `array([1., 0., 0.])`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCALE_FACTOR_PER_FONT_POINT` = `0.0010416666666666667`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMIBOLD` = `'SEMIBOLD'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SEMILIGHT` = `'SEMILIGHT'`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SHIFT_VALUE` = `65505`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `SMALL_BUFF` = `0.1`
- `START_X` = `30`
- `START_X` = `30`
- `START_X` = `30`
- `START_Y` = `20`
- `START_Y` = `20`
- `START_Y` = `20`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `TAU` = `6.283185307179586`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `THIN` = `'THIN'`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `TYPE_CHECKING` = `False`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `UL` = `array([-1.,  1.,  0.])`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRABOLD` = `'ULTRABOLD'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRAHEAVY` = `'ULTRAHEAVY'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `ULTRALIGHT` = `'ULTRALIGHT'`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UP` = `array([0., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `UR` = `array([1., 1., 0.])`
- `WHITE` = `ManimColor('#FFFFFF')`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_AXIS` = `array([1., 0., 0.])`
- `X_COLOR` = `ManimColor('#83C167')`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_AXIS` = `array([0., 1., 0.])`
- `Y_COLOR` = `ManimColor('#FC6255')`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_AXIS` = `array([0., 0., 1.])`
- `Z_COLOR` = `ManimColor('#29ABCA')`
- **`convert_audio(input_path: 'Path', output_path: 'Path | _TemporaryFileWrapper[bytes]', codec_name: 'str') -> 'None'`**
- **`to_av_frame_rate(fps: 'float') -> 'Fraction'`**

## typing

- `TYPE_CHECKING` = `False`

## utils/bezier

- `CP_CLOSED_MEMO` = `array([0.33333333])`
- `CP_OPEN_MEMO` = `array([0.5])`
- `SUBDIVISION_MATRICES` = `[{}, {}, {}, {}]`
- `TYPE_CHECKING` = `False`
- `UP_CLOSED_MEMO` = `array([0.33333333])`
- **`bezier(points: 'Point3D_Array | Sequence[Point3D_Array]') -> 'Callable[[float | ColVector], Point3D_Array]'`** — Classic implementation of a Bézier curve.
- **`bezier_remap(bezier_tuples: 'BezierPointsLike_Array', new_number_of_curves: 'int') -> 'BezierPoints_Array'`** — Subdivides each curve in ``bezier_tuples`` into as many parts as necessary, until the final number of
- **`get_quadratic_approximation_of_cubic(a0: 'Point3D | Point3D_Array', h0: 'Point3D | Point3D_Array', h1: 'Point3D | Point3D_Array', a1: 'Point3D | Point3D_Array') -> 'QuadraticSpline | QuadraticBezierPath'`** — If ``a0``, ``h0``, ``h1`` and ``a1`` are the control points of a cubic
- **`get_smooth_closed_cubic_bezier_handle_points(anchors: 'Point3DLike_Array') -> 'tuple[Point3D_Array, Point3D_Array]'`** — Special case of :func:`get_smooth_cubic_bezier_handle_points`,
- **`get_smooth_cubic_bezier_handle_points(anchors: 'Point3DLike_Array') -> 'tuple[Point3D_Array, Point3D_Array]'`** — Given an array of anchors for a cubic spline (array of connected cubic
- **`get_smooth_open_cubic_bezier_handle_points(anchors: 'Point3DLike_Array') -> 'tuple[Point3D_Array, Point3D_Array]'`** — Special case of :func:`get_smooth_cubic_bezier_handle_points`,
- **`integer_interpolate(start: 'float', end: 'float', alpha: 'float') -> 'tuple[int, float]'`** — This is a variant of interpolate that returns an integer and the residual
- **`interpolate(start: 'float | Point3D', end: 'float | Point3D', alpha: 'float | ColVector') -> 'float | ColVector | Point3D | Point3D_Array'`** — Linearly interpolates between two values ``start`` and ``end``.
- **`inverse_interpolate(start: 'float | Point3D', end: 'float | Point3D', value: 'float | Point3D') -> 'float | Point3D'`** — Perform inverse interpolation to determine the alpha
- **`is_closed(points: 'Point3D_Array') -> 'bool'`** — Returns ``True`` if the spline given by ``points`` is closed, by
- **`match_interpolate(new_start: 'float', new_end: 'float', old_start: 'float', old_end: 'float', old_value: 'float | Point3D') -> 'float | Point3D'`** — Interpolate a value from an old range to a new range.
- **`mid(start: 'float | Point3D', end: 'float | Point3D') -> 'float | Point3D'`** — Returns the midpoint between two values.
- **`partial_bezier_points(points: 'BezierPointsLike', a: 'float', b: 'float') -> 'BezierPoints'`** — Given an array of ``points`` which define a Bézier curve, and two numbers :math:`a, b`
- **`point_lies_on_bezier(point: 'Point3DLike', control_points: 'BezierPointsLike', round_to: 'float' = 1e-06) -> 'bool'`** — Checks if a given point lies on the bezier curves with the given control points.
- **`proportions_along_bezier_curve_for_point(point: 'Point3DLike', control_points: 'BezierPointsLike', round_to: 'float' = 1e-06) -> 'MatrixMN'`** — Obtains the proportion along the bezier curve corresponding to a given point
- **`split_bezier(points: 'BezierPointsLike', t: 'float') -> 'Spline'`** — Split a Bézier curve at argument ``t`` into two curves.
- **`subdivide_bezier(points: 'BezierPointsLike', n_divisions: 'int') -> 'Spline'`** — Subdivide a Bézier curve into :math:`n` subcurves which have the same shape.

## utils/color

### `HSV(hsv: 'FloatHSVLike | FloatHSVALike', alpha: 'float' = 1.0) -> 'None'` ← ManimColor
> HSV Color Space

<details><summary>métodos próprios (1) · herdados: 24</summary>

- `__init__(self, hsv: 'FloatHSVLike | FloatHSVALike', alpha: 'float' = 1.0) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `ManimColor(value: 'ParsableManimColor | None', alpha: 'float' = 1.0) -> 'None'`
> Internal representation of a color.

<details><summary>métodos próprios (25) · herdados: 0</summary>

- `__init__(self, value: 'ParsableManimColor | None', alpha: 'float' = 1.0) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `contrasting(self, threshold: 'float' = 0.5, light: 'Self | None' = None, dark: 'Self | None' = None) -> 'Self'` — Return one of two colors, light or dark (by default white or black),
- `darker(self, blend: 'float' = 0.2) -> 'Self'` — Return a new color that is darker than the current color, i.e.
- `from_hex(hex_str: 'str', alpha: 'float' = 1.0) -> 'Self'` — Create a :class:`ManimColor` from a hex string.
- `from_hsl(hsl: 'FloatHSLLike', alpha: 'float' = 1.0) -> 'Self'` — Create a :class:`ManimColor` from an HSL array.
- `from_hsv(hsv: 'FloatHSVLike', alpha: 'float' = 1.0) -> 'Self'` — Create a :class:`ManimColor` from an HSV array.
- `from_rgb(rgb: 'FloatRGBLike | IntRGBLike', alpha: 'float' = 1.0) -> 'Self'` — Create a ManimColor from an RGB array. Automagically decides which type it
- `from_rgba(rgba: 'FloatRGBALike | IntRGBALike') -> 'Self'` — Create a ManimColor from an RGBA Array. Automagically decides which type it
- `gradient(colors: 'list[ManimColor]', length: 'int') -> 'ManimColor | list[ManimColor]'` — This method is currently not implemented. Refer to :func:`color_gradient` for
- `interpolate(self, other: 'Self', alpha: 'float') -> 'Self'` — Interpolate between the current and the given :class:`ManimColor`, and return
- `into(self, class_type: 'type[ManimColorT]') -> 'ManimColorT'` — Convert the current color into a different colorspace given by ``class_type``,
- `invert(self, with_alpha: 'bool' = False) -> 'Self'` — Return a new, linearly inverted version of this :class:`ManimColor` (no
- `lighter(self, blend: 'float' = 0.2) -> 'Self'` — Return a new color that is lighter than the current color, i.e.
- `opacity(self, opacity: 'float') -> 'Self'` — Create a new :class:`ManimColor` with the given opacity and the same color
- `parse(color: 'ParsableManimColor | Sequence[ParsableManimColor] | None', alpha: 'float' = 1.0) -> 'Self | list[Self]'` — Parse one color as a :class:`ManimColor` or a sequence of colors as a list of
- `to_hex(self, with_alpha: 'bool' = False) -> 'str'` — Convert the :class:`ManimColor` to a hexadecimal representation of the color.
- `to_hsl(self) -> 'FloatHSL'` — Convert the :class:`ManimColor` to an HSL array.
- `to_hsv(self) -> 'FloatHSV'` — Convert the :class:`ManimColor` to an HSV array.
- `to_int_rgb(self) -> 'IntRGB'` — Convert the current :class:`ManimColor` into an RGB array of integers.
- `to_int_rgba(self) -> 'IntRGBA'` — Convert the current ManimColor into an RGBA array of integers.
- `to_int_rgba_with_alpha(self, alpha: 'float') -> 'IntRGBA'` — Convert the current :class:`ManimColor` into an RGBA array of integers. This
- `to_integer(self) -> 'int'` — Convert the current :class:`ManimColor` into an integer.
- `to_rgb(self) -> 'FloatRGB'` — Convert the current :class:`ManimColor` into an RGB array of floats.
- `to_rgba(self) -> 'FloatRGBA'` — Convert the current :class:`ManimColor` into an RGBA array of floats.
- `to_rgba_with_alpha(self, alpha: 'float') -> 'FloatRGBA'` — Convert the current :class:`ManimColor` into an RGBA array of floats. This is

</details>

### `RGBA(value: 'ParsableManimColor | None', alpha: 'float' = 1.0) -> 'None'`
> Internal representation of a color.

<details><summary>métodos próprios (25) · herdados: 0</summary>

- `__init__(self, value: 'ParsableManimColor | None', alpha: 'float' = 1.0) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `contrasting(self, threshold: 'float' = 0.5, light: 'Self | None' = None, dark: 'Self | None' = None) -> 'Self'` — Return one of two colors, light or dark (by default white or black),
- `darker(self, blend: 'float' = 0.2) -> 'Self'` — Return a new color that is darker than the current color, i.e.
- `from_hex(hex_str: 'str', alpha: 'float' = 1.0) -> 'Self'` — Create a :class:`ManimColor` from a hex string.
- `from_hsl(hsl: 'FloatHSLLike', alpha: 'float' = 1.0) -> 'Self'` — Create a :class:`ManimColor` from an HSL array.
- `from_hsv(hsv: 'FloatHSVLike', alpha: 'float' = 1.0) -> 'Self'` — Create a :class:`ManimColor` from an HSV array.
- `from_rgb(rgb: 'FloatRGBLike | IntRGBLike', alpha: 'float' = 1.0) -> 'Self'` — Create a ManimColor from an RGB array. Automagically decides which type it
- `from_rgba(rgba: 'FloatRGBALike | IntRGBALike') -> 'Self'` — Create a ManimColor from an RGBA Array. Automagically decides which type it
- `gradient(colors: 'list[ManimColor]', length: 'int') -> 'ManimColor | list[ManimColor]'` — This method is currently not implemented. Refer to :func:`color_gradient` for
- `interpolate(self, other: 'Self', alpha: 'float') -> 'Self'` — Interpolate between the current and the given :class:`ManimColor`, and return
- `into(self, class_type: 'type[ManimColorT]') -> 'ManimColorT'` — Convert the current color into a different colorspace given by ``class_type``,
- `invert(self, with_alpha: 'bool' = False) -> 'Self'` — Return a new, linearly inverted version of this :class:`ManimColor` (no
- `lighter(self, blend: 'float' = 0.2) -> 'Self'` — Return a new color that is lighter than the current color, i.e.
- `opacity(self, opacity: 'float') -> 'Self'` — Create a new :class:`ManimColor` with the given opacity and the same color
- `parse(color: 'ParsableManimColor | Sequence[ParsableManimColor] | None', alpha: 'float' = 1.0) -> 'Self | list[Self]'` — Parse one color as a :class:`ManimColor` or a sequence of colors as a list of
- `to_hex(self, with_alpha: 'bool' = False) -> 'str'` — Convert the :class:`ManimColor` to a hexadecimal representation of the color.
- `to_hsl(self) -> 'FloatHSL'` — Convert the :class:`ManimColor` to an HSL array.
- `to_hsv(self) -> 'FloatHSV'` — Convert the :class:`ManimColor` to an HSV array.
- `to_int_rgb(self) -> 'IntRGB'` — Convert the current :class:`ManimColor` into an RGB array of integers.
- `to_int_rgba(self) -> 'IntRGBA'` — Convert the current ManimColor into an RGBA array of integers.
- `to_int_rgba_with_alpha(self, alpha: 'float') -> 'IntRGBA'` — Convert the current :class:`ManimColor` into an RGBA array of integers. This
- `to_integer(self) -> 'int'` — Convert the current :class:`ManimColor` into an integer.
- `to_rgb(self) -> 'FloatRGB'` — Convert the current :class:`ManimColor` into an RGB array of floats.
- `to_rgba(self) -> 'FloatRGBA'` — Convert the current :class:`ManimColor` into an RGBA array of floats.
- `to_rgba_with_alpha(self, alpha: 'float') -> 'FloatRGBA'` — Convert the current :class:`ManimColor` into an RGBA array of floats. This is

</details>

### `RandomColorGenerator(seed: 'int | None' = None, sample_colors: 'list[ManimColor] | None' = None) -> 'None'`
> A generator for producing random colors from a given list of Manim colors,

<details><summary>métodos próprios (2) · herdados: 0</summary>

- `__init__(self, seed: 'int | None' = None, sample_colors: 'list[ManimColor] | None' = None) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `next(self) -> 'ManimColor'` — Returns the next color from the configured color list.

</details>

- `ACIDGREEN` = `ManimColor('#8FFE09')`
- `ADOBE` = `ManimColor('#BD6C48')`
- `AIRCRAFT_BLUE` = `ManimColor('#173679')`
- `AIRCRAFT_GREY` = `ManimColor('#88918D')`
- `AIRCRAFT_GREY_GREEN` = `ManimColor('#7E8F6E')`
- `ALGAE` = `ManimColor('#54AC68')`
- `ALGAEGREEN` = `ManimColor('#21C36F')`
- `ALICEBLUE` = `ManimColor('#EFF7FF')`
- `ALICEBLUE` = `ManimColor('#F0F8FF')`
- `ALMOSTBLACK` = `ManimColor('#070D0D')`
- `AMBER` = `ManimColor('#FEB308')`
- `AMETHYST` = `ManimColor('#9B5FC0')`
- `ANTIQUEWHITE` = `ManimColor('#F9EAD7')`
- `ANTIQUEWHITE` = `ManimColor('#FAEBD7')`
- `ANTIQUEWHITE1` = `ManimColor('#FFEFDB')`
- `ANTIQUEWHITE2` = `ManimColor('#EEDFCC')`
- `ANTIQUEWHITE3` = `ManimColor('#CDC0B0')`
- `ANTIQUEWHITE4` = `ManimColor('#8B8378')`
- `APPLE` = `ManimColor('#6ECB3C')`
- `APPLEGREEN` = `ManimColor('#76CD26')`
- `APRICOT` = `ManimColor('#FB9C06')`
- `APRICOT` = `ManimColor('#FBB982')`
- `APRICOT` = `ManimColor('#FFB16D')`
- `AQUA` = `ManimColor('#00FFFF')`
- `AQUA` = `ManimColor('#13EAC9')`
- `AQUABLUE` = `ManimColor('#02D8E9')`
- `AQUAGREEN` = `ManimColor('#12E193')`
- `AQUAMARINE` = `ManimColor('#00B5BE')`
- `AQUAMARINE` = `ManimColor('#7EFFD3')`
- `AQUAMARINE` = `ManimColor('#2EE8BB')`
- `AQUAMARINE1` = `ManimColor('#7FFFD4')`
- `AQUAMARINE2` = `ManimColor('#76EEC6')`
- `AQUAMARINE4` = `ManimColor('#458B74')`
- `ARCTIC_BLUE` = `ManimColor('#78ADC2')`
- `ARMYGREEN` = `ManimColor('#4B5D16')`
- `ASPARAGUS` = `ManimColor('#77AB56')`
- `AUBERGINE` = `ManimColor('#3D0734')`
- `AUBURN` = `ManimColor('#9A3001')`
- `AVOCADO` = `ManimColor('#90B134')`
- `AVOCADOGREEN` = `ManimColor('#87A922')`
- `AZO_ORANGE` = `ManimColor('#F24816')`
- `AZUL` = `ManimColor('#1D5DEC')`
- `AZURE` = `ManimColor('#EFFFFF')`
- `AZURE` = `ManimColor('#069AF3')`
- `AZURE1` = `ManimColor('#F0FFFF')`
- `AZURE2` = `ManimColor('#E0EEEE')`
- `AZURE3` = `ManimColor('#C1CDCD')`
- `AZURE4` = `ManimColor('#838B8B')`
- `AZURE_BLUE` = `ManimColor('#264D7E')`
- `B11_RICH_BLUE` = `ManimColor('#2B3770')`
- `B12_ROYAL_BLUE` = `ManimColor('#2C3563')`
- `B13_NAVY_BLUE` = `ManimColor('#28304D')`
- `B14_SAPHHIRE` = `ManimColor('#28426B')`
- `B15_MID_BLUE` = `ManimColor('#144B6F')`
- `B21_ULTRAMARINE` = `ManimColor('#2C5098')`
- `B22_HOMEBUSH_BLUE` = `ManimColor('#215097')`
- `B23_BRIGHT_BLUE` = `ManimColor('#174F90')`
- `B24_HARBOUR_BLUE` = `ManimColor('#1C6293')`
- `B25_AQUA` = `ManimColor('#5097AC')`
- `B32_POWDER_BLUE` = `ManimColor('#B7C8DB')`
- `B33_MIST_BLUE` = `ManimColor('#E0E6E2')`
- `B34_PARADISE_BLUE` = `ManimColor('#3499BA')`
- `B35_PALE_BLUE` = `ManimColor('#CDE4E2')`
- `B41_BLUEBELL` = `ManimColor('#5B94D1')`
- `B42_PURPLE_BLUE` = `ManimColor('#5E7899')`
- `B43_GREY_BLUE` = `ManimColor('#627C8D')`
- `B44_LIGHT_GREY_BLUE` = `ManimColor('#C0C0C1')`
- `B45_SKY_BLUE` = `ManimColor('#7DB7C7')`
- `B51_PERIWINKLE` = `ManimColor('#3871AC')`
- `B53_DARK_GREY_BLUE` = `ManimColor('#4F6572')`
- `B55_STORM_BLUE` = `ManimColor('#3F7C94')`
- `B61_CORAL_SEA` = `ManimColor('#2B3873')`
- `B62_MIDNIGHT_BLUE` = `ManimColor('#292A34')`
- `B64_CHARCOAL` = `ManimColor('#363E45')`
- `BABYBLUE` = `ManimColor('#A2CFFE')`
- `BABYGREEN` = `ManimColor('#8CFF9E')`
- `BABYPINK` = `ManimColor('#FFB7CE')`
- `BABYPOO` = `ManimColor('#AB9004')`
- `BABYPOOP` = `ManimColor('#937C00')`
- `BABYPOOPGREEN` = `ManimColor('#8F9805')`
- `BABYPUKEGREEN` = `ManimColor('#B6C406')`
- `BABYPURPLE` = `ManimColor('#CA9BF7')`
- `BABYSHITBROWN` = `ManimColor('#AD900D')`
- `BABYSHITGREEN` = `ManimColor('#889717')`
- `BANANA` = `ManimColor('#FFFF7E')`
- `BANANAYELLOW` = `ManimColor('#FAFE4B')`
- `BARBIEPINK` = `ManimColor('#FE46A5')`
- `BARFGREEN` = `ManimColor('#94AC02')`
- `BARNEY` = `ManimColor('#AC1DB8')`
- `BARNEYPURPLE` = `ManimColor('#A00498')`
- `BATTLESHIPGREY` = `ManimColor('#6B7C85')`
- `BEECH_BROWN` = `ManimColor('#573320')`
- `BEIGE` = `ManimColor('#E4CF93')`
- `BEIGE` = `ManimColor('#F4F4DC')`
- `BEIGE` = `ManimColor('#F5F5DC')`
- `BEIGE` = `ManimColor('#E6DAA6')`
- `BERRY` = `ManimColor('#990F4B')`
- `BILE` = `ManimColor('#B5C306')`
- `BISCUIT` = `ManimColor('#FEEBA8')`
- `BISQUE` = `ManimColor('#FFE3C4')`
- `BISQUE1` = `ManimColor('#FFE4C4')`
- `BISQUE2` = `ManimColor('#EED5B7')`
- `BISQUE3` = `ManimColor('#CDB79E')`
- `BISQUE4` = `ManimColor('#8B7D6B')`
- `BITTERSWEET` = `ManimColor('#C04F17')`
- `BLACK` = `ManimColor('#000000')`
- `BLACK` = `ManimColor('#221E1F')`
- `BLACK` = `ManimColor('#000000')`
- `BLACK` = `ManimColor('#000000')`
- `BLACK` = `ManimColor('#000000')`
- `BLACK` = `ManimColor('#000000')`
- `BLANCHEDALMOND` = `ManimColor('#FFEACD')`
- `BLANCHEDALMOND` = `ManimColor('#FFEBCD')`
- `BLAND` = `ManimColor('#AFA88B')`
- `BLOOD` = `ManimColor('#770001')`
- `BLOODORANGE` = `ManimColor('#FE4B03')`
- `BLOODRED` = `ManimColor('#980002')`
- `BLUE` = `ManimColor('#58C4DD')`
- `BLUE` = `ManimColor('#2D2F92')`
- `BLUE` = `ManimColor('#0000FF')`
- `BLUE` = `ManimColor('#0343DF')`
- `BLUE` = `ManimColor('#58C4DD')`
- `BLUE1` = `ManimColor('#0000FF')`
- `BLUE2` = `ManimColor('#0000EE')`
- `BLUE4` = `ManimColor('#00008B')`
- `BLUEBERRY` = `ManimColor('#464196')`
- `BLUEBLUE` = `ManimColor('#2242C7')`
- `BLUEGREEN` = `ManimColor('#00B3B8')`
- `BLUEGREEN` = `ManimColor('#0F9B8E')`
- `BLUEGREY` = `ManimColor('#85A3B2')`
- `BLUEPURPLE` = `ManimColor('#5A06EF')`
- `BLUEVIOLET` = `ManimColor('#473992')`
- `BLUEVIOLET` = `ManimColor('#892BE2')`
- `BLUEVIOLET` = `ManimColor('#8A2BE2')`
- `BLUEVIOLET` = `ManimColor('#5D06E9')`
- `BLUEWITHAHINTOFPURPLE` = `ManimColor('#533CC6')`
- `BLUEYGREEN` = `ManimColor('#2BB179')`
- `BLUEYGREY` = `ManimColor('#89A0B0')`
- `BLUEYPURPLE` = `ManimColor('#6241C7')`
- `BLUE_A` = `ManimColor('#C7E9F1')`
- `BLUE_A` = `ManimColor('#C7E9F1')`
- `BLUE_B` = `ManimColor('#9CDCEB')`
- `BLUE_B` = `ManimColor('#9CDCEB')`
- `BLUE_C` = `ManimColor('#58C4DD')`
- `BLUE_C` = `ManimColor('#58C4DD')`
- `BLUE_D` = `ManimColor('#29ABCA')`
- `BLUE_D` = `ManimColor('#29ABCA')`
- `BLUE_E` = `ManimColor('#236B8E')`
- `BLUE_E` = `ManimColor('#236B8E')`
- `BLUISH` = `ManimColor('#2976BB')`
- `BLUISHGREEN` = `ManimColor('#10A674')`
- `BLUISHGREY` = `ManimColor('#748B97')`
- `BLUISHPURPLE` = `ManimColor('#703BE7')`
- `BLURPLE` = `ManimColor('#5539CC')`
- `BLUSH` = `ManimColor('#F29E8E')`
- `BLUSHPINK` = `ManimColor('#FE828C')`
- `BOLD_GREEN` = `ManimColor('#44945E')`
- `BOLD_RED` = `ManimColor('#DD3524')`
- `BOLD_YELLOW` = `ManimColor('#FDE706')`
- `BOOGER` = `ManimColor('#9BB53C')`
- `BOOGERGREEN` = `ManimColor('#96B403')`
- `BORDEAUX` = `ManimColor('#7B002C')`
- `BORINGGREEN` = `ManimColor('#63B365')`
- `BOTTLEGREEN` = `ManimColor('#044A05')`
- `BRICK` = `ManimColor('#A03623')`
- `BRICKORANGE` = `ManimColor('#C14A09')`
- `BRICKRED` = `ManimColor('#B6321C')`
- `BRICKRED` = `ManimColor('#8F1402')`
- `BRIGHTAQUA` = `ManimColor('#0BF9EA')`
- `BRIGHTBLUE` = `ManimColor('#0165FC')`
- `BRIGHTCYAN` = `ManimColor('#41FDFE')`
- `BRIGHTGREEN` = `ManimColor('#01FF07')`
- `BRIGHTLAVENDER` = `ManimColor('#C760FF')`
- `BRIGHTLIGHTBLUE` = `ManimColor('#26F7FD')`
- `BRIGHTLIGHTGREEN` = `ManimColor('#2DFE54')`
- `BRIGHTLILAC` = `ManimColor('#C95EFB')`
- `BRIGHTLIME` = `ManimColor('#87FD05')`
- `BRIGHTLIMEGREEN` = `ManimColor('#65FE08')`
- `BRIGHTMAGENTA` = `ManimColor('#FF08E8')`
- `BRIGHTOLIVE` = `ManimColor('#9CBB04')`
- `BRIGHTORANGE` = `ManimColor('#FF5B00')`
- `BRIGHTPINK` = `ManimColor('#FE01B1')`
- `BRIGHTPURPLE` = `ManimColor('#BE03FD')`
- `BRIGHTRED` = `ManimColor('#FF000D')`
- `BRIGHTSEAGREEN` = `ManimColor('#05FFA6')`
- `BRIGHTSKYBLUE` = `ManimColor('#02CCFE')`
- `BRIGHTTEAL` = `ManimColor('#01F9C6')`
- `BRIGHTTURQUOISE` = `ManimColor('#0FFEF9')`
- `BRIGHTVIOLET` = `ManimColor('#AD0AFD')`
- `BRIGHTYELLOW` = `ManimColor('#FFFD01')`
- `BRIGHTYELLOWGREEN` = `ManimColor('#9DFF00')`
- `BRILLIANT_GREEN` = `ManimColor('#507D3A')`
- `BRITISHRACINGGREEN` = `ManimColor('#05480D')`
- `BRONZE` = `ManimColor('#A87900')`
- `BROWN` = `ManimColor('#792500')`
- `BROWN` = `ManimColor('#A52A2A')`
- `BROWN` = `ManimColor('#A52A2A')`
- `BROWN` = `ManimColor('#653700')`
- `BROWN1` = `ManimColor('#FF4040')`
- `BROWN2` = `ManimColor('#EE3B3B')`
- `BROWN3` = `ManimColor('#CD3333')`
- `BROWN4` = `ManimColor('#8B2323')`
- `BROWNGREEN` = `ManimColor('#706C11')`
- `BROWNGREY` = `ManimColor('#8D8468')`
- `BROWNISH` = `ManimColor('#9C6D57')`
- `BROWNISHGREEN` = `ManimColor('#6A6E09')`
- `BROWNISHGREY` = `ManimColor('#86775F')`
- `BROWNISHORANGE` = `ManimColor('#CB7723')`
- `BROWNISHPINK` = `ManimColor('#C27E79')`
- `BROWNISHPURPLE` = `ManimColor('#76424E')`
- `BROWNISHRED` = `ManimColor('#9E3623')`
- `BROWNISHYELLOW` = `ManimColor('#C9B003')`
- `BROWNORANGE` = `ManimColor('#B96902')`
- `BROWNRED` = `ManimColor('#922B05')`
- `BROWNYELLOW` = `ManimColor('#B29705')`
- `BROWNYGREEN` = `ManimColor('#6F6C0A')`
- `BROWNYORANGE` = `ManimColor('#CA6B02')`
- `BRUISE` = `ManimColor('#7E4071')`
- `BS381_101` = `ManimColor('#94BFAC')`
- `BS381_102` = `ManimColor('#5B9291')`
- `BS381_103` = `ManimColor('#3B6879')`
- `BS381_104` = `ManimColor('#264D7E')`
- `BS381_105` = `ManimColor('#1F3057')`
- `BS381_106` = `ManimColor('#2A283D')`
- `BS381_107` = `ManimColor('#3A73A9')`
- `BS381_108` = `ManimColor('#173679')`
- `BS381_109` = `ManimColor('#1C5680')`
- `BS381_110` = `ManimColor('#2C3E75')`
- `BS381_111` = `ManimColor('#8CC5BB')`
- `BS381_112` = `ManimColor('#78ADC2')`
- `BS381_113` = `ManimColor('#3F687D')`
- `BS381_114` = `ManimColor('#1F4B61')`
- `BS381_115` = `ManimColor('#5F88C1')`
- `BS381_166` = `ManimColor('#2458AF')`
- `BS381_169` = `ManimColor('#135B75')`
- `BS381_172` = `ManimColor('#A7C6EB')`
- `BS381_174` = `ManimColor('#64A0AA')`
- `BS381_175` = `ManimColor('#4F81C5')`
- `BS381_210` = `ManimColor('#BBC9A5')`
- `BS381_216` = `ManimColor('#BCD890')`
- `BS381_217` = `ManimColor('#96BF65')`
- `BS381_218` = `ManimColor('#698B47')`
- `BS381_219` = `ManimColor('#757639')`
- `BS381_220` = `ManimColor('#4B5729')`
- `BS381_221` = `ManimColor('#507D3A')`
- `BS381_222` = `ManimColor('#6A7031')`
- `BS381_223` = `ManimColor('#49523A')`
- `BS381_224` = `ManimColor('#3E4630')`
- `BS381_225` = `ManimColor('#406A28')`
- `BS381_226` = `ManimColor('#33533B')`
- `BS381_227` = `ManimColor('#254432')`
- `BS381_228` = `ManimColor('#428B64')`
- `BS381_241` = `ManimColor('#4F5241')`
- `BS381_262` = `ManimColor('#44945E')`
- `BS381_267` = `ManimColor('#476A4C')`
- `BS381_275` = `ManimColor('#8FC693')`
- `BS381_276` = `ManimColor('#2E4C1E')`
- `BS381_277` = `ManimColor('#364A20')`
- `BS381_278` = `ManimColor('#87965A')`
- `BS381_279` = `ManimColor('#3B3629')`
- `BS381_280` = `ManimColor('#68AB77')`
- `BS381_282` = `ManimColor('#506B52')`
- `BS381_283` = `ManimColor('#7E8F6E')`
- `BS381_284` = `ManimColor('#6B6F5A')`
- `BS381_285` = `ManimColor('#5F5C4B')`
- `BS381_298` = `ManimColor('#4F5138')`
- `BS381_309` = `ManimColor('#FEEC04')`
- `BS381_310` = `ManimColor('#FEF963')`
- `BS381_315` = `ManimColor('#FEF96A')`
- `BS381_320` = `ManimColor('#9E7339')`
- `BS381_337` = `ManimColor('#4C4A3C')`
- `BS381_350` = `ManimColor('#7B6B4F')`
- `BS381_352` = `ManimColor('#FCED96')`
- `BS381_353` = `ManimColor('#FDF07A')`
- `BS381_354` = `ManimColor('#E9BB43')`
- `BS381_355` = `ManimColor('#FDD906')`
- `BS381_356` = `ManimColor('#FCC808')`
- `BS381_358` = `ManimColor('#F6C870')`
- `BS381_359` = `ManimColor('#DBAC50')`
- `BS381_361` = `ManimColor('#D4B97D')`
- `BS381_362` = `ManimColor('#AC7C42')`
- `BS381_363` = `ManimColor('#FDE706')`
- `BS381_364` = `ManimColor('#CEC093')`
- `BS381_365` = `ManimColor('#F4F0BD')`
- `BS381_366` = `ManimColor('#F5E7A1')`
- `BS381_367` = `ManimColor('#FEF6BF')`
- `BS381_368` = `ManimColor('#DD7B00')`
- `BS381_369` = `ManimColor('#FEEBA8')`
- `BS381_380` = `ManimColor('#BBA38A')`
- `BS381_384` = `ManimColor('#EEDFA5')`
- `BS381_385` = `ManimColor('#E8C88F')`
- `BS381_386` = `ManimColor('#E6C18D')`
- `BS381_387` = `ManimColor('#CFB48A')`
- `BS381_388` = `ManimColor('#E4CF93')`
- `BS381_389` = `ManimColor('#B2A788')`
- `BS381_397` = `ManimColor('#F3D163')`
- `BS381_411` = `ManimColor('#74542F')`
- `BS381_412` = `ManimColor('#5C422E')`
- `BS381_413` = `ManimColor('#402D21')`
- `BS381_414` = `ManimColor('#A86C29')`
- `BS381_415` = `ManimColor('#61361E')`
- `BS381_420` = `ManimColor('#A89177')`
- `BS381_435` = `ManimColor('#845B4D')`
- `BS381_436` = `ManimColor('#564B47')`
- `BS381_439` = `ManimColor('#753B1E')`
- `BS381_443` = `ManimColor('#C98A71')`
- `BS381_444` = `ManimColor('#A65341')`
- `BS381_445` = `ManimColor('#83422B')`
- `BS381_446` = `ManimColor('#774430')`
- `BS381_447` = `ManimColor('#F3B28B')`
- `BS381_448` = `ManimColor('#67403A')`
- `BS381_449` = `ManimColor('#693B3F')`
- `BS381_452` = `ManimColor('#613339')`
- `BS381_453` = `ManimColor('#FBDED6')`
- `BS381_454` = `ManimColor('#E8A1A2')`
- `BS381_460` = `ManimColor('#BD8F56')`
- `BS381_473` = `ManimColor('#793932')`
- `BS381_489` = `ManimColor('#8D5B41')`
- `BS381_490` = `ManimColor('#573320')`
- `BS381_499` = `ManimColor('#59493E')`
- `BS381_536` = `ManimColor('#BB3016')`
- `BS381_537` = `ManimColor('#DD3420')`
- `BS381_538` = `ManimColor('#C41C22')`
- `BS381_539` = `ManimColor('#D21E2B')`
- `BS381_540` = `ManimColor('#8B1A32')`
- `BS381_541` = `ManimColor('#471B21')`
- `BS381_542` = `ManimColor('#982D57')`
- `BS381_557` = `ManimColor('#EF841E')`
- `BS381_564` = `ManimColor('#DD3524')`
- `BS381_568` = `ManimColor('#FB9C06')`
- `BS381_570` = `ManimColor('#A83C19')`
- `BS381_591` = `ManimColor('#D04E09')`
- `BS381_592` = `ManimColor('#E45523')`
- `BS381_593` = `ManimColor('#F24816')`
- `BS381_626` = `ManimColor('#A0A9AA')`
- `BS381_627` = `ManimColor('#BEC0B8')`
- `BS381_628` = `ManimColor('#9D9D7E')`
- `BS381_629` = `ManimColor('#7A838B')`
- `BS381_630` = `ManimColor('#A5AD98')`
- `BS381_631` = `ManimColor('#9AAA9F')`
- `BS381_632` = `ManimColor('#6B7477')`
- `BS381_633` = `ManimColor('#424C53')`
- `BS381_634` = `ManimColor('#6F7264')`
- `BS381_635` = `ManimColor('#525B55')`
- `BS381_636` = `ManimColor('#5F7682')`
- `BS381_637` = `ManimColor('#8E9B9C')`
- `BS381_638` = `ManimColor('#6C7377')`
- `BS381_639` = `ManimColor('#667563')`
- `BS381_640` = `ManimColor('#566164')`
- `BS381_642` = `ManimColor('#282B2F')`
- `BS381_671` = `ManimColor('#4E5355')`
- `BS381_676` = `ManimColor('#A9B7B9')`
- `BS381_677` = `ManimColor('#676F76')`
- `BS381_692` = `ManimColor('#7B93A3')`
- `BS381_693` = `ManimColor('#88918D')`
- `BS381_694` = `ManimColor('#909A92')`
- `BS381_697` = `ManimColor('#B6D3CC')`
- `BS381_796` = `ManimColor('#6E4A75')`
- `BS381_797` = `ManimColor('#C9A8CE')`
- `BUBBLEGUM` = `ManimColor('#FF6CB5')`
- `BUBBLEGUMPINK` = `ManimColor('#FF69AF')`
- `BUFF` = `ManimColor('#FEF69E')`
- `BURGUNDY` = `ManimColor('#610023')`
- `BURLYWOOD` = `ManimColor('#DDB787')`
- `BURLYWOOD` = `ManimColor('#DEB887')`
- `BURLYWOOD1` = `ManimColor('#FFD39B')`
- `BURLYWOOD2` = `ManimColor('#EEC591')`
- `BURLYWOOD3` = `ManimColor('#CDAA7D')`
- `BURLYWOOD4` = `ManimColor('#8B7355')`
- `BURNTORANGE` = `ManimColor('#F7921D')`
- `BURNTORANGE` = `ManimColor('#C04E01')`
- `BURNTRED` = `ManimColor('#9F2305')`
- `BURNTSIENA` = `ManimColor('#B75203')`
- `BURNTSIENNA` = `ManimColor('#B04E0F')`
- `BURNTUMBER` = `ManimColor('#A0450E')`
- `BURNTYELLOW` = `ManimColor('#D5AB09')`
- `BURPLE` = `ManimColor('#6832E3')`
- `BUTTER` = `ManimColor('#FFFF81')`
- `BUTTERSCOTCH` = `ManimColor('#FDB147')`
- `BUTTERYELLOW` = `ManimColor('#FFFD74')`
- `CADETBLUE` = `ManimColor('#74729A')`
- `CADETBLUE` = `ManimColor('#5E9EA0')`
- `CADETBLUE` = `ManimColor('#5F9EA0')`
- `CADETBLUE` = `ManimColor('#4E7496')`
- `CADETBLUE1` = `ManimColor('#98F5FF')`
- `CADETBLUE2` = `ManimColor('#8EE5EE')`
- `CADETBLUE3` = `ManimColor('#7AC5CD')`
- `CADETBLUE4` = `ManimColor('#53868B')`
- `CAMEL` = `ManimColor('#C69F59')`
- `CAMO` = `ManimColor('#7F8F4E')`
- `CAMOGREEN` = `ManimColor('#526525')`
- `CAMOUFLAGEGREEN` = `ManimColor('#4B6113')`
- `CAMOUFLAGE_BEIGE` = `ManimColor('#B2A788')`
- `CAMOUFLAGE_DESERT_SAND` = `ManimColor('#BBA38A')`
- `CAMOUFLAGE_GREY` = `ManimColor('#A0A9AA')`
- `CAMOUFLAGE_RED` = `ManimColor('#845B4D')`
- `CANARY` = `ManimColor('#FDFF63')`
- `CANARYYELLOW` = `ManimColor('#FFFE40')`
- `CANARY_YELLOW` = `ManimColor('#FEEC04')`
- `CANDYPINK` = `ManimColor('#FF63E9')`
- `CARAMEL` = `ManimColor('#AF6F09')`
- `CARMINE` = `ManimColor('#9D0216')`
- `CARNATION` = `ManimColor('#FD798F')`
- `CARNATIONPINK` = `ManimColor('#F282B4')`
- `CARNATIONPINK` = `ManimColor('#FF7FA7')`
- `CAROLINABLUE` = `ManimColor('#8AB8FE')`
- `CELADON` = `ManimColor('#BEFDB7')`
- `CELERY` = `ManimColor('#C1FD95')`
- `CEMENT` = `ManimColor('#A5A391')`
- `CERISE` = `ManimColor('#DE0C62')`
- `CERULEAN` = `ManimColor('#00A2E3')`
- `CERULEAN` = `ManimColor('#0485D1')`
- `CERULEANBLUE` = `ManimColor('#056EEE')`
- `CHAMPAGNE` = `ManimColor('#E6C18D')`
- `CHARCOAL` = `ManimColor('#343837')`
- `CHARCOALGREY` = `ManimColor('#3C4142')`
- `CHARTREUSE` = `ManimColor('#7EFF00')`
- `CHARTREUSE` = `ManimColor('#C1F80A')`
- `CHARTREUSE1` = `ManimColor('#7FFF00')`
- `CHARTREUSE2` = `ManimColor('#76EE00')`
- `CHARTREUSE3` = `ManimColor('#66CD00')`
- `CHARTREUSE4` = `ManimColor('#458B00')`
- `CHERRY` = `ManimColor('#C41C22')`
- `CHERRY` = `ManimColor('#CF0234')`
- `CHERRYRED` = `ManimColor('#F7022A')`
- `CHESTNUT` = `ManimColor('#742802')`
- `CHOCOLATE` = `ManimColor('#D2681D')`
- `CHOCOLATE` = `ManimColor('#D2691E')`
- `CHOCOLATE` = `ManimColor('#3D1C02')`
- `CHOCOLATE1` = `ManimColor('#FF7F24')`
- `CHOCOLATE2` = `ManimColor('#EE7621')`
- `CHOCOLATE3` = `ManimColor('#CD661D')`
- `CHOCOLATEBROWN` = `ManimColor('#411900')`
- `CINNAMON` = `ManimColor('#AC4F06')`
- `CLARET` = `ManimColor('#680018')`
- `CLAY` = `ManimColor('#B66A50')`
- `CLAYBROWN` = `ManimColor('#B2713D')`
- `CLEARBLUE` = `ManimColor('#247AFD')`
- `COBALT` = `ManimColor('#1E488F')`
- `COBALTBLUE` = `ManimColor('#030AA7')`
- `COBALT_BLUE` = `ManimColor('#5F88C1')`
- `COCOA` = `ManimColor('#875F42')`
- `COFFEE` = `ManimColor('#A6814C')`
- `COOLBLUE` = `ManimColor('#4984B8')`
- `COOLGREEN` = `ManimColor('#33B864')`
- `COOLGREY` = `ManimColor('#95A3A6')`
- `COPPER` = `ManimColor('#B66325')`
- `CORAL` = `ManimColor('#FF7E4F')`
- `CORAL` = `ManimColor('#FF7F50')`
- `CORAL` = `ManimColor('#FC5A50')`
- `CORAL1` = `ManimColor('#FF7256')`
- `CORAL2` = `ManimColor('#EE6A50')`
- `CORAL3` = `ManimColor('#CD5B45')`
- `CORAL4` = `ManimColor('#8B3E2F')`
- `CORALPINK` = `ManimColor('#FF6163')`
- `CORNFLOWER` = `ManimColor('#6A79F7')`
- `CORNFLOWERBLUE` = `ManimColor('#41B0E4')`
- `CORNFLOWERBLUE` = `ManimColor('#6395ED')`
- `CORNFLOWERBLUE` = `ManimColor('#6495ED')`
- `CORNFLOWERBLUE` = `ManimColor('#5170D7')`
- `CORNSILK` = `ManimColor('#FFF7DC')`
- `CORNSILK1` = `ManimColor('#FFF8DC')`
- `CORNSILK2` = `ManimColor('#EEE8CD')`
- `CORNSILK3` = `ManimColor('#CDC8B1')`
- `CORNSILK4` = `ManimColor('#8B8878')`
- `CRANBERRY` = `ManimColor('#9E003A')`
- `CREAM` = `ManimColor('#FFFFC2')`
- `CREME` = `ManimColor('#FFFFB6')`
- `CRIMSON` = `ManimColor('#8B1A32')`
- `CRIMSON` = `ManimColor('#DC143B')`
- `CRIMSON` = `ManimColor('#8C000F')`
- `CURRANT_RED` = `ManimColor('#D21E2B')`
- `CUSTARD` = `ManimColor('#FFFD78')`
- `CYAN` = `ManimColor('#00AEEF')`
- `CYAN` = `ManimColor('#00FFFF')`
- `CYAN` = `ManimColor('#00FFFF')`
- `CYAN1` = `ManimColor('#00FFFF')`
- `CYAN2` = `ManimColor('#00EEEE')`
- `CYAN3` = `ManimColor('#00CDCD')`
- `CYAN4` = `ManimColor('#008B8B')`
- `CYPRESS_GREEN` = `ManimColor('#364A20')`
- `DANDELION` = `ManimColor('#FDBC42')`
- `DANDELION` = `ManimColor('#FEDF08')`
- `DARK` = `ManimColor('#1B2431')`
- `DARKAQUA` = `ManimColor('#05696B')`
- `DARKAQUAMARINE` = `ManimColor('#017371')`
- `DARKBEIGE` = `ManimColor('#AC9362')`
- `DARKBLUE` = `ManimColor('#00008A')`
- `DARKBLUE` = `ManimColor('#030764')`
- `DARKBLUEGREEN` = `ManimColor('#005249')`
- `DARKBLUEGREY` = `ManimColor('#1F3B4D')`
- `DARKBROWN` = `ManimColor('#341C02')`
- `DARKCORAL` = `ManimColor('#CF524E')`
- `DARKCREAM` = `ManimColor('#FFF39A')`
- `DARKCYAN` = `ManimColor('#008A8A')`
- `DARKCYAN` = `ManimColor('#0A888A')`
- `DARKER_GRAY` = `ManimColor('#222222')`
- `DARKER_GRAY` = `ManimColor('#222222')`
- `DARKER_GREY` = `ManimColor('#222222')`
- `DARKER_GREY` = `ManimColor('#222222')`
- `DARKFORESTGREEN` = `ManimColor('#002D04')`
- `DARKFUCHSIA` = `ManimColor('#9D0759')`
- `DARKGOLD` = `ManimColor('#B59410')`
- `DARKGOLDENROD` = `ManimColor('#B7850B')`
- `DARKGOLDENROD` = `ManimColor('#B8860B')`
- `DARKGOLDENROD1` = `ManimColor('#FFB90F')`
- `DARKGOLDENROD2` = `ManimColor('#EEAD0E')`
- `DARKGOLDENROD3` = `ManimColor('#CD950C')`
- `DARKGOLDENROD4` = `ManimColor('#8B6508')`
- `DARKGRASSGREEN` = `ManimColor('#388004')`
- `DARKGRAY` = `ManimColor('#A9A9A9')`
- `DARKGREEN` = `ManimColor('#006300')`
- `DARKGREEN` = `ManimColor('#006400')`
- `DARKGREEN` = `ManimColor('#054907')`
- `DARKGREENBLUE` = `ManimColor('#1F6357')`
- `DARKGREY` = `ManimColor('#A9A9A9')`
- `DARKGREY` = `ManimColor('#363737')`
- `DARKGREYBLUE` = `ManimColor('#29465B')`
- `DARKHOTPINK` = `ManimColor('#D90166')`
- `DARKINDIGO` = `ManimColor('#1F0954')`
- `DARKISHBLUE` = `ManimColor('#014182')`
- `DARKISHGREEN` = `ManimColor('#287C37')`
- `DARKISHPINK` = `ManimColor('#DA467D')`
- `DARKISHPURPLE` = `ManimColor('#751973')`
- `DARKISHRED` = `ManimColor('#A90308')`
- `DARKKHAKI` = `ManimColor('#BCB66B')`
- `DARKKHAKI` = `ManimColor('#BDB76B')`
- `DARKKHAKI` = `ManimColor('#9B8F55')`
- `DARKLAVENDER` = `ManimColor('#856798')`
- `DARKLILAC` = `ManimColor('#9C6DA5')`
- `DARKLIME` = `ManimColor('#84B701')`
- `DARKLIMEGREEN` = `ManimColor('#7EBD01')`
- `DARKMAGENTA` = `ManimColor('#8A008A')`
- `DARKMAGENTA` = `ManimColor('#960056')`
- `DARKMAROON` = `ManimColor('#3C0008')`
- `DARKMAUVE` = `ManimColor('#874C62')`
- `DARKMINT` = `ManimColor('#48C072')`
- `DARKMINTGREEN` = `ManimColor('#20C073')`
- `DARKMUSTARD` = `ManimColor('#A88905')`
- `DARKNAVY` = `ManimColor('#000435')`
- `DARKNAVYBLUE` = `ManimColor('#00022E')`
- `DARKOLIVE` = `ManimColor('#373E02')`
- `DARKOLIVEGREEN` = `ManimColor('#546B2F')`
- `DARKOLIVEGREEN` = `ManimColor('#556B2F')`
- `DARKOLIVEGREEN` = `ManimColor('#3C4D03')`
- `DARKOLIVEGREEN1` = `ManimColor('#CAFF70')`
- `DARKOLIVEGREEN2` = `ManimColor('#BCEE68')`
- `DARKOLIVEGREEN3` = `ManimColor('#A2CD5A')`
- `DARKOLIVEGREEN4` = `ManimColor('#6E8B3D')`
- `DARKORANGE` = `ManimColor('#FF8C00')`
- `DARKORANGE` = `ManimColor('#FF8C00')`
- `DARKORANGE` = `ManimColor('#C65102')`
- `DARKORANGE1` = `ManimColor('#FF7F00')`
- `DARKORANGE2` = `ManimColor('#EE7600')`
- `DARKORANGE3` = `ManimColor('#CD6600')`
- `DARKORANGE4` = `ManimColor('#8B4500')`
- `DARKORCHID` = `ManimColor('#A4538A')`
- `DARKORCHID` = `ManimColor('#9931CC')`
- `DARKORCHID` = `ManimColor('#9932CC')`
- `DARKORCHID1` = `ManimColor('#BF3EFF')`
- `DARKORCHID2` = `ManimColor('#B23AEE')`
- `DARKORCHID3` = `ManimColor('#9A32CD')`
- `DARKORCHID4` = `ManimColor('#68228B')`
- `DARKPASTELGREEN` = `ManimColor('#56AE57')`
- `DARKPEACH` = `ManimColor('#DE7E5D')`
- `DARKPERIWINKLE` = `ManimColor('#665FD1')`
- `DARKPINK` = `ManimColor('#CB416B')`
- `DARKPLUM` = `ManimColor('#3F012C')`
- `DARKPURPLE` = `ManimColor('#35063E')`
- `DARKRED` = `ManimColor('#8A0000')`
- `DARKRED` = `ManimColor('#840000')`
- `DARKROSE` = `ManimColor('#B5485D')`
- `DARKROYALBLUE` = `ManimColor('#02066F')`
- `DARKSAGE` = `ManimColor('#598556')`
- `DARKSALMON` = `ManimColor('#E8967A')`
- `DARKSALMON` = `ManimColor('#E9967A')`
- `DARKSALMON` = `ManimColor('#C85A53')`
- `DARKSAND` = `ManimColor('#A88F59')`
- `DARKSEAFOAM` = `ManimColor('#1FB57A')`
- `DARKSEAFOAMGREEN` = `ManimColor('#3EAF76')`
- `DARKSEAGREEN` = `ManimColor('#8EBB8E')`
- `DARKSEAGREEN` = `ManimColor('#8FBC8F')`
- `DARKSEAGREEN` = `ManimColor('#11875D')`
- `DARKSEAGREEN1` = `ManimColor('#C1FFC1')`
- `DARKSEAGREEN2` = `ManimColor('#B4EEB4')`
- `DARKSEAGREEN3` = `ManimColor('#9BCD9B')`
- `DARKSEAGREEN4` = `ManimColor('#698B69')`
- `DARKSKYBLUE` = `ManimColor('#448EE4')`
- `DARKSLATEBLUE` = `ManimColor('#483D8A')`
- `DARKSLATEBLUE` = `ManimColor('#483D8B')`
- `DARKSLATEBLUE` = `ManimColor('#214761')`
- `DARKSLATEGRAY` = `ManimColor('#2F4F4F')`
- `DARKSLATEGRAY` = `ManimColor('#2F4F4F')`
- `DARKSLATEGRAY1` = `ManimColor('#97FFFF')`
- `DARKSLATEGRAY2` = `ManimColor('#8DEEEE')`
- `DARKSLATEGRAY3` = `ManimColor('#79CDCD')`
- `DARKSLATEGRAY4` = `ManimColor('#528B8B')`
- `DARKSLATEGREY` = `ManimColor('#2F4F4F')`
- `DARKTAN` = `ManimColor('#AF884A')`
- `DARKTAUPE` = `ManimColor('#7F684E')`
- `DARKTEAL` = `ManimColor('#014D4E')`
- `DARKTURQUOISE` = `ManimColor('#00CED1')`
- `DARKTURQUOISE` = `ManimColor('#00CED1')`
- `DARKTURQUOISE` = `ManimColor('#045C5A')`
- `DARKVIOLET` = `ManimColor('#9300D3')`
- `DARKVIOLET` = `ManimColor('#9400D3')`
- `DARKVIOLET` = `ManimColor('#34013F')`
- `DARKYELLOW` = `ManimColor('#D5B60A')`
- `DARKYELLOWGREEN` = `ManimColor('#728F02')`
- `DARK_ADMIRALTY_GREY` = `ManimColor('#6B7477')`
- `DARK_BLUE` = `ManimColor('#236B8E')`
- `DARK_BLUE` = `ManimColor('#236B8E')`
- `DARK_BROWN` = `ManimColor('#8B4513')`
- `DARK_BROWN` = `ManimColor('#5C422E')`
- `DARK_BROWN` = `ManimColor('#8B4513')`
- `DARK_CAMOUFLAGE_BROWN` = `ManimColor('#564B47')`
- `DARK_CAMOUFLAGE_DESERT_SAND` = `ManimColor('#A89177')`
- `DARK_CAMOUFLAGE_GREY` = `ManimColor('#7A838B')`
- `DARK_CRIMSON` = `ManimColor('#613339')`
- `DARK_EARTH` = `ManimColor('#7B6B4F')`
- `DARK_GRAY` = `ManimColor('#444444')`
- `DARK_GRAY` = `ManimColor('#444444')`
- `DARK_GREEN` = `ManimColor('#4F5241')`
- `DARK_GREY` = `ManimColor('#444444')`
- `DARK_GREY` = `ManimColor('#444444')`
- `DARK_SEA_GREY` = `ManimColor('#6C7377')`
- `DARK_VIOLET` = `ManimColor('#6E4A75')`
- `DARK_WEATHERWORK_GREY` = `ManimColor('#676F76')`
- `DEEPAQUA` = `ManimColor('#08787F')`
- `DEEPBLUE` = `ManimColor('#040273')`
- `DEEPBROWN` = `ManimColor('#410200')`
- `DEEPGREEN` = `ManimColor('#02590F')`
- `DEEPLAVENDER` = `ManimColor('#8D5EB7')`
- `DEEPLILAC` = `ManimColor('#966EBD')`
- `DEEPMAGENTA` = `ManimColor('#A0025C')`
- `DEEPORANGE` = `ManimColor('#DC4D01')`
- `DEEPPINK` = `ManimColor('#FF1492')`
- `DEEPPINK` = `ManimColor('#CB0162')`
- `DEEPPINK1` = `ManimColor('#FF1493')`
- `DEEPPINK2` = `ManimColor('#EE1289')`
- `DEEPPINK3` = `ManimColor('#CD1076')`
- `DEEPPINK4` = `ManimColor('#8B0A50')`
- `DEEPPURPLE` = `ManimColor('#36013F')`
- `DEEPRED` = `ManimColor('#9A0200')`
- `DEEPROSE` = `ManimColor('#C74767')`
- `DEEPSEABLUE` = `ManimColor('#015482')`
- `DEEPSKYBLUE` = `ManimColor('#00BFFF')`
- `DEEPSKYBLUE` = `ManimColor('#0D75F8')`
- `DEEPSKYBLUE1` = `ManimColor('#00BFFF')`
- `DEEPSKYBLUE2` = `ManimColor('#00B2EE')`
- `DEEPSKYBLUE3` = `ManimColor('#009ACD')`
- `DEEPSKYBLUE4` = `ManimColor('#00688B')`
- `DEEPTEAL` = `ManimColor('#00555A')`
- `DEEPTURQUOISE` = `ManimColor('#017374')`
- `DEEPVIOLET` = `ManimColor('#490648')`
- `DEEP_BRONZE_GREEN` = `ManimColor('#3E4630')`
- `DEEP_BRUNSWICK_GREEN` = `ManimColor('#254432')`
- `DEEP_BUFF` = `ManimColor('#BD8F56')`
- `DEEP_CHROME_GREEN` = `ManimColor('#476A4C')`
- `DEEP_CREAM` = `ManimColor('#FDF07A')`
- `DEEP_INDIAN_RED` = `ManimColor('#67403A')`
- `DEEP_ORANGE` = `ManimColor('#D04E09')`
- `DEEP_SAXE_BLUE` = `ManimColor('#3F687D')`
- `DENIM` = `ManimColor('#3B638C')`
- `DENIMBLUE` = `ManimColor('#3B5B92')`
- `DESERT` = `ManimColor('#CCAD60')`
- `DIARRHEA` = `ManimColor('#9F8303')`
- `DIMGRAY` = `ManimColor('#686868')`
- `DIMGRAY` = `ManimColor('#696969')`
- `DIMGREY` = `ManimColor('#686868')`
- `DIRT` = `ManimColor('#8A6E45')`
- `DIRTBROWN` = `ManimColor('#836539')`
- `DIRTYBLUE` = `ManimColor('#3F829D')`
- `DIRTYGREEN` = `ManimColor('#667E2C')`
- `DIRTYORANGE` = `ManimColor('#C87606')`
- `DIRTYPINK` = `ManimColor('#CA7B80')`
- `DIRTYPURPLE` = `ManimColor('#734A65')`
- `DIRTYYELLOW` = `ManimColor('#CDC50A')`
- `DODGERBLUE` = `ManimColor('#1D90FF')`
- `DODGERBLUE` = `ManimColor('#3E82FC')`
- `DODGERBLUE1` = `ManimColor('#1E90FF')`
- `DODGERBLUE2` = `ManimColor('#1C86EE')`
- `DODGERBLUE3` = `ManimColor('#1874CD')`
- `DODGERBLUE4` = `ManimColor('#104E8B')`
- `DOVE_GREY` = `ManimColor('#909A92')`
- `DRAB` = `ManimColor('#828344')`
- `DRABGREEN` = `ManimColor('#749551')`
- `DRIEDBLOOD` = `ManimColor('#4B0101')`
- `DUCKEGGBLUE` = `ManimColor('#C3FBF4')`
- `DULLBLUE` = `ManimColor('#49759C')`
- `DULLBROWN` = `ManimColor('#876E4B')`
- `DULLGREEN` = `ManimColor('#74A662')`
- `DULLORANGE` = `ManimColor('#D8863B')`
- `DULLPINK` = `ManimColor('#D5869D')`
- `DULLPURPLE` = `ManimColor('#84597E')`
- `DULLRED` = `ManimColor('#BB3F3F')`
- `DULLTEAL` = `ManimColor('#5F9E8F')`
- `DULLYELLOW` = `ManimColor('#EEDC5B')`
- `DUSK` = `ManimColor('#4E5481')`
- `DUSKBLUE` = `ManimColor('#26538D')`
- `DUSKYBLUE` = `ManimColor('#475F94')`
- `DUSKYPINK` = `ManimColor('#CC7A8B')`
- `DUSKYPURPLE` = `ManimColor('#895B7B')`
- `DUSKYROSE` = `ManimColor('#BA6873')`
- `DUST` = `ManimColor('#B2996E')`
- `DUSTYBLUE` = `ManimColor('#5A86AD')`
- `DUSTYGREEN` = `ManimColor('#76A973')`
- `DUSTYLAVENDER` = `ManimColor('#AC86A8')`
- `DUSTYORANGE` = `ManimColor('#F0833A')`
- `DUSTYPINK` = `ManimColor('#D58A94')`
- `DUSTYPURPLE` = `ManimColor('#825F87')`
- `DUSTYRED` = `ManimColor('#B9484E')`
- `DUSTYROSE` = `ManimColor('#C0737A')`
- `DUSTYTEAL` = `ManimColor('#4C9085')`
- `EARTH` = `ManimColor('#A2653E')`
- `EASTERGREEN` = `ManimColor('#8CFD7E')`
- `EASTERPURPLE` = `ManimColor('#C071FE')`
- `EAU_DE_NIL` = `ManimColor('#BCD890')`
- `ECRU` = `ManimColor('#FEFFCA')`
- `EGGPLANT` = `ManimColor('#380835')`
- `EGGPLANTPURPLE` = `ManimColor('#430541')`
- `EGGSHELL` = `ManimColor('#FFFCC4')`
- `EGGSHELLBLUE` = `ManimColor('#C4FFF7')`
- `ELECTRICBLUE` = `ManimColor('#0652FF')`
- `ELECTRICGREEN` = `ManimColor('#21FC0D')`
- `ELECTRICLIME` = `ManimColor('#A8FF04')`
- `ELECTRICPINK` = `ManimColor('#FF0490')`
- `ELECTRICPURPLE` = `ManimColor('#AA23FF')`
- `EMERALD` = `ManimColor('#00A99D')`
- `EMERALD` = `ManimColor('#01A049')`
- `EMERALDGREEN` = `ManimColor('#028F1E')`
- `EMERALD_GREEN` = `ManimColor('#428B64')`
- `EVERGREEN` = `ManimColor('#05472A')`
- `EXTRA_DARK_SEA_GREY` = `ManimColor('#566164')`
- `FADEDBLUE` = `ManimColor('#658CBB')`
- `FADEDGREEN` = `ManimColor('#7BB274')`
- `FADEDORANGE` = `ManimColor('#F0944D')`
- `FADEDPINK` = `ManimColor('#DE9DAC')`
- `FADEDPURPLE` = `ManimColor('#916E99')`
- `FADEDRED` = `ManimColor('#D3494E')`
- `FADEDYELLOW` = `ManimColor('#FEFF7F')`
- `FAWN` = `ManimColor('#CFAF7B')`
- `FERN` = `ManimColor('#63A950')`
- `FERNGREEN` = `ManimColor('#548D44')`
- `FIESTA_BLUE` = `ManimColor('#78ADC2')`
- `FIREBRICK` = `ManimColor('#B12121')`
- `FIREBRICK` = `ManimColor('#B22222')`
- `FIREBRICK1` = `ManimColor('#FF3030')`
- `FIREBRICK2` = `ManimColor('#EE2C2C')`
- `FIREBRICK3` = `ManimColor('#CD2626')`
- `FIREBRICK4` = `ManimColor('#8B1A1A')`
- `FIREENGINERED` = `ManimColor('#FE0002')`
- `FLATBLUE` = `ManimColor('#3C73A8')`
- `FLATGREEN` = `ManimColor('#699D4C')`
- `FLORALWHITE` = `ManimColor('#FFF9EF')`
- `FLORALWHITE` = `ManimColor('#FFFAF0')`
- `FLUORESCENTGREEN` = `ManimColor('#08FF08')`
- `FLUROGREEN` = `ManimColor('#0AFF02')`
- `FOAMGREEN` = `ManimColor('#90FDA9')`
- `FOREST` = `ManimColor('#0B5509')`
- `FORESTGREEN` = `ManimColor('#009B55')`
- `FORESTGREEN` = `ManimColor('#218A21')`
- `FORESTGREEN` = `ManimColor('#228B22')`
- `FORESTGREEN` = `ManimColor('#06470C')`
- `FOREST_GREEN` = `ManimColor('#506B52')`
- `FORRESTGREEN` = `ManimColor('#154406')`
- `FRENCHBLUE` = `ManimColor('#436BAD')`
- `FRENCH_BLUE` = `ManimColor('#2458AF')`
- `FRENCH_GREY` = `ManimColor('#A5AD98')`
- `FRESHGREEN` = `ManimColor('#69D84F')`
- `FROGGREEN` = `ManimColor('#58BC08')`
- `FUCHSIA` = `ManimColor('#8C368C')`
- `FUCHSIA` = `ManimColor('#FF00FF')`
- `FUCHSIA` = `ManimColor('#ED0DD9')`
- `G11_BOTTLE_GREEN` = `ManimColor('#253A32')`
- `G12_HOLLY` = `ManimColor('#21432D')`
- `G13_EMERALD` = `ManimColor('#195F35')`
- `G14_MOSS_GREEN` = `ManimColor('#33572D')`
- `G15_RAINFOREST_GREEN` = `ManimColor('#3D492D')`
- `G16_TRAFFIC_GREEN` = `ManimColor('#305442')`
- `G17_MINT_GREEN` = `ManimColor('#006B45')`
- `G21_JADE` = `ManimColor('#127453')`
- `G22_SERPENTINE` = `ManimColor('#78A681')`
- `G23_SHAMROCK` = `ManimColor('#336634')`
- `G24_FERN_TREE` = `ManimColor('#477036')`
- `G25_OLIVE` = `ManimColor('#595B2A')`
- `G26_APPLE_GREEN` = `ManimColor('#4E9843')`
- `G27_HOMEBUSH_GREEN` = `ManimColor('#017F4D')`
- `G31_VERTIGRIS` = `ManimColor('#468A65')`
- `G32_OPALINE` = `ManimColor('#AFCBB8')`
- `G33_LETTUCE` = `ManimColor('#7B9954')`
- `G34_AVOCADO` = `ManimColor('#757C4C')`
- `G35_LIME_GREEN` = `ManimColor('#89922E')`
- `G36_KIKUYU` = `ManimColor('#95B43B')`
- `G37_BEANSTALK` = `ManimColor('#45A56A')`
- `G41_LAWN_GREEN` = `ManimColor('#0D875D')`
- `G42_GLACIER` = `ManimColor('#D5E1D2')`
- `G43_SURF_GREEN` = `ManimColor('#C8C8A7')`
- `G44_PALM_GREEN` = `ManimColor('#99B179')`
- `G45_CHARTREUSE` = `ManimColor('#C7C98D')`
- `G46_CITRONELLA` = `ManimColor('#BFC83E')`
- `G47_CRYSTAL_GREEN` = `ManimColor('#ADCCA8')`
- `G51_SPRUCE` = `ManimColor('#05674F')`
- `G52_EUCALYPTUS` = `ManimColor('#66755B')`
- `G53_BANKSIA` = `ManimColor('#929479')`
- `G54_MIST_GREEN` = `ManimColor('#7A836D')`
- `G55_LICHEN` = `ManimColor('#A7A98C')`
- `G56_SAGE_GREEN` = `ManimColor('#677249')`
- `G61_DARK_GREEN` = `ManimColor('#283533')`
- `G62_RIVERGUM` = `ManimColor('#617061')`
- `G63_DEEP_BRONZE_GREEN` = `ManimColor('#333334')`
- `G64_SLATE` = `ManimColor('#5E6153')`
- `G65_TI_TREE` = `ManimColor('#5D5F4E')`
- `G66_ENVIRONMENT_GREEN` = `ManimColor('#484C3F')`
- `G67_ZUCCHINI` = `ManimColor('#2E443A')`
- `GAINSBORO` = `ManimColor('#DCDCDC')`
- `GAINSBORO` = `ManimColor('#DCDCDC')`
- `GHOSTWHITE` = `ManimColor('#F7F7FF')`
- `GHOSTWHITE` = `ManimColor('#F8F8FF')`
- `GOLD` = `ManimColor('#F0AC5F')`
- `GOLD` = `ManimColor('#FFD700')`
- `GOLD` = `ManimColor('#DBB40C')`
- `GOLD` = `ManimColor('#F0AC5F')`
- `GOLD1` = `ManimColor('#FFD700')`
- `GOLD2` = `ManimColor('#EEC900')`
- `GOLD3` = `ManimColor('#CDAD00')`
- `GOLD4` = `ManimColor('#8B7500')`
- `GOLDEN` = `ManimColor('#F5BF03')`
- `GOLDENBROWN` = `ManimColor('#B27A01')`
- `GOLDENROD` = `ManimColor('#FFDF42')`
- `GOLDENROD` = `ManimColor('#DAA51F')`
- `GOLDENROD` = `ManimColor('#DAA520')`
- `GOLDENROD` = `ManimColor('#F9BC08')`
- `GOLDENROD1` = `ManimColor('#FFC125')`
- `GOLDENROD2` = `ManimColor('#EEB422')`
- `GOLDENROD3` = `ManimColor('#CD9B1D')`
- `GOLDENROD4` = `ManimColor('#8B6914')`
- `GOLDENYELLOW` = `ManimColor('#FEC615')`
- `GOLDEN_BROWN` = `ManimColor('#A86C29')`
- `GOLDEN_YELLOW` = `ManimColor('#FCC808')`
- `GOLD_A` = `ManimColor('#F7C797')`
- `GOLD_A` = `ManimColor('#F7C797')`
- `GOLD_B` = `ManimColor('#F9B775')`
- `GOLD_B` = `ManimColor('#F9B775')`
- `GOLD_C` = `ManimColor('#F0AC5F')`
- `GOLD_C` = `ManimColor('#F0AC5F')`
- `GOLD_D` = `ManimColor('#E1A158')`
- `GOLD_D` = `ManimColor('#E1A158')`
- `GOLD_E` = `ManimColor('#C78D46')`
- `GOLD_E` = `ManimColor('#C78D46')`
- `GRAPE` = `ManimColor('#6C3461')`
- `GRAPEFRUIT` = `ManimColor('#FEF96A')`
- `GRAPEFRUIT` = `ManimColor('#FD5956')`
- `GRAPEPURPLE` = `ManimColor('#5D1451')`
- `GRASS` = `ManimColor('#5CAC2D')`
- `GRASSGREEN` = `ManimColor('#3F9B0B')`
- `GRASSYGREEN` = `ManimColor('#419C03')`
- `GRASS_GREEN` = `ManimColor('#698B47')`
- `GRAY` = `ManimColor('#888888')`
- `GRAY` = `ManimColor('#949698')`
- `GRAY` = `ManimColor('#7F7F7F')`
- `GRAY` = `ManimColor('#BEBEBE')`
- `GRAY` = `ManimColor('#888888')`
- `GRAY1` = `ManimColor('#030303')`
- `GRAY10` = `ManimColor('#1A1A1A')`
- `GRAY11` = `ManimColor('#1C1C1C')`
- `GRAY12` = `ManimColor('#1F1F1F')`
- `GRAY13` = `ManimColor('#212121')`
- `GRAY14` = `ManimColor('#242424')`
- `GRAY15` = `ManimColor('#262626')`
- `GRAY16` = `ManimColor('#292929')`
- `GRAY17` = `ManimColor('#2B2B2B')`
- `GRAY18` = `ManimColor('#2E2E2E')`
- `GRAY19` = `ManimColor('#303030')`
- `GRAY2` = `ManimColor('#050505')`
- `GRAY20` = `ManimColor('#333333')`
- `GRAY21` = `ManimColor('#363636')`
- `GRAY22` = `ManimColor('#383838')`
- `GRAY23` = `ManimColor('#3B3B3B')`
- `GRAY24` = `ManimColor('#3D3D3D')`
- `GRAY25` = `ManimColor('#404040')`
- `GRAY26` = `ManimColor('#424242')`
- `GRAY27` = `ManimColor('#454545')`
- `GRAY28` = `ManimColor('#474747')`
- `GRAY29` = `ManimColor('#4A4A4A')`
- `GRAY3` = `ManimColor('#080808')`
- `GRAY30` = `ManimColor('#4D4D4D')`
- `GRAY31` = `ManimColor('#4F4F4F')`
- `GRAY32` = `ManimColor('#525252')`
- `GRAY33` = `ManimColor('#545454')`
- `GRAY34` = `ManimColor('#575757')`
- `GRAY35` = `ManimColor('#595959')`
- `GRAY36` = `ManimColor('#5C5C5C')`
- `GRAY37` = `ManimColor('#5E5E5E')`
- `GRAY38` = `ManimColor('#616161')`
- `GRAY39` = `ManimColor('#636363')`
- `GRAY4` = `ManimColor('#0A0A0A')`
- `GRAY40` = `ManimColor('#666666')`
- `GRAY41` = `ManimColor('#696969')`
- `GRAY42` = `ManimColor('#6B6B6B')`
- `GRAY43` = `ManimColor('#6E6E6E')`
- `GRAY44` = `ManimColor('#707070')`
- `GRAY45` = `ManimColor('#737373')`
- `GRAY46` = `ManimColor('#757575')`
- `GRAY47` = `ManimColor('#787878')`
- `GRAY48` = `ManimColor('#7A7A7A')`
- `GRAY49` = `ManimColor('#7D7D7D')`
- `GRAY5` = `ManimColor('#0D0D0D')`
- `GRAY50` = `ManimColor('#7F7F7F')`
- `GRAY51` = `ManimColor('#828282')`
- `GRAY52` = `ManimColor('#858585')`
- `GRAY53` = `ManimColor('#878787')`
- `GRAY54` = `ManimColor('#8A8A8A')`
- `GRAY55` = `ManimColor('#8C8C8C')`
- `GRAY56` = `ManimColor('#8F8F8F')`
- `GRAY57` = `ManimColor('#919191')`
- `GRAY58` = `ManimColor('#949494')`
- `GRAY59` = `ManimColor('#969696')`
- `GRAY6` = `ManimColor('#0F0F0F')`
- `GRAY60` = `ManimColor('#999999')`
- `GRAY61` = `ManimColor('#9C9C9C')`
- `GRAY62` = `ManimColor('#9E9E9E')`
- `GRAY63` = `ManimColor('#A1A1A1')`
- `GRAY64` = `ManimColor('#A3A3A3')`
- `GRAY65` = `ManimColor('#A6A6A6')`
- `GRAY66` = `ManimColor('#A8A8A8')`
- `GRAY67` = `ManimColor('#ABABAB')`
- `GRAY68` = `ManimColor('#ADADAD')`
- `GRAY69` = `ManimColor('#B0B0B0')`
- `GRAY7` = `ManimColor('#121212')`
- `GRAY70` = `ManimColor('#B3B3B3')`
- `GRAY71` = `ManimColor('#B5B5B5')`
- `GRAY72` = `ManimColor('#B8B8B8')`
- `GRAY73` = `ManimColor('#BABABA')`
- `GRAY74` = `ManimColor('#BDBDBD')`
- `GRAY75` = `ManimColor('#BFBFBF')`
- `GRAY76` = `ManimColor('#C2C2C2')`
- `GRAY77` = `ManimColor('#C4C4C4')`
- `GRAY78` = `ManimColor('#C7C7C7')`
- `GRAY79` = `ManimColor('#C9C9C9')`
- `GRAY8` = `ManimColor('#141414')`
- `GRAY80` = `ManimColor('#CCCCCC')`
- `GRAY81` = `ManimColor('#CFCFCF')`
- `GRAY82` = `ManimColor('#D1D1D1')`
- `GRAY83` = `ManimColor('#D4D4D4')`
- `GRAY84` = `ManimColor('#D6D6D6')`
- `GRAY85` = `ManimColor('#D9D9D9')`
- `GRAY86` = `ManimColor('#DBDBDB')`
- `GRAY87` = `ManimColor('#DEDEDE')`
- `GRAY88` = `ManimColor('#E0E0E0')`
- `GRAY89` = `ManimColor('#E3E3E3')`
- `GRAY9` = `ManimColor('#171717')`
- `GRAY90` = `ManimColor('#E5E5E5')`
- `GRAY91` = `ManimColor('#E8E8E8')`
- `GRAY92` = `ManimColor('#EBEBEB')`
- `GRAY93` = `ManimColor('#EDEDED')`
- `GRAY94` = `ManimColor('#F0F0F0')`
- `GRAY95` = `ManimColor('#F2F2F2')`
- `GRAY97` = `ManimColor('#F7F7F7')`
- `GRAY98` = `ManimColor('#FAFAFA')`
- `GRAY99` = `ManimColor('#FCFCFC')`
- `GRAY_A` = `ManimColor('#DDDDDD')`
- `GRAY_A` = `ManimColor('#DDDDDD')`
- `GRAY_B` = `ManimColor('#BBBBBB')`
- `GRAY_B` = `ManimColor('#BBBBBB')`
- `GRAY_BROWN` = `ManimColor('#736357')`
- `GRAY_BROWN` = `ManimColor('#736357')`
- `GRAY_C` = `ManimColor('#888888')`
- `GRAY_C` = `ManimColor('#888888')`
- `GRAY_D` = `ManimColor('#444444')`
- `GRAY_D` = `ManimColor('#444444')`
- `GRAY_E` = `ManimColor('#222222')`
- `GRAY_E` = `ManimColor('#222222')`
- `GREEN` = `ManimColor('#83C167')`
- `GREEN` = `ManimColor('#00A64F')`
- `GREEN` = `ManimColor('#007F00')`
- `GREEN` = `ManimColor('#15B01A')`
- `GREEN` = `ManimColor('#83C167')`
- `GREEN1` = `ManimColor('#00FF00')`
- `GREEN2` = `ManimColor('#00EE00')`
- `GREEN3` = `ManimColor('#00CD00')`
- `GREEN4` = `ManimColor('#008B00')`
- `GREENAPPLE` = `ManimColor('#5EDC1F')`
- `GREENBLUE` = `ManimColor('#01C08D')`
- `GREENBROWN` = `ManimColor('#544E03')`
- `GREENGREY` = `ManimColor('#77926F')`
- `GREENISH` = `ManimColor('#40A368')`
- `GREENISHBEIGE` = `ManimColor('#C9D179')`
- `GREENISHBLUE` = `ManimColor('#0B8B87')`
- `GREENISHBROWN` = `ManimColor('#696112')`
- `GREENISHCYAN` = `ManimColor('#2AFEB7')`
- `GREENISHGREY` = `ManimColor('#96AE8D')`
- `GREENISHTAN` = `ManimColor('#BCCB7A')`
- `GREENISHTEAL` = `ManimColor('#32BF84')`
- `GREENISHTURQUOISE` = `ManimColor('#00FBB0')`
- `GREENISHYELLOW` = `ManimColor('#CDFD02')`
- `GREENTEAL` = `ManimColor('#0CB577')`
- `GREENYBLUE` = `ManimColor('#42B395')`
- `GREENYBROWN` = `ManimColor('#696006')`
- `GREENYELLOW` = `ManimColor('#DFE674')`
- `GREENYELLOW` = `ManimColor('#ADFF2F')`
- `GREENYELLOW` = `ManimColor('#ADFF2F')`
- `GREENYELLOW` = `ManimColor('#B5CE08')`
- `GREENYGREY` = `ManimColor('#7EA07A')`
- `GREENYYELLOW` = `ManimColor('#C6F808')`
- `GREEN_A` = `ManimColor('#C9E2AE')`
- `GREEN_A` = `ManimColor('#C9E2AE')`
- `GREEN_B` = `ManimColor('#A6CF8C')`
- `GREEN_B` = `ManimColor('#A6CF8C')`
- `GREEN_C` = `ManimColor('#83C167')`
- `GREEN_C` = `ManimColor('#83C167')`
- `GREEN_D` = `ManimColor('#77B05D')`
- `GREEN_D` = `ManimColor('#77B05D')`
- `GREEN_E` = `ManimColor('#699C52')`
- `GREEN_E` = `ManimColor('#699C52')`
- `GREY` = `ManimColor('#888888')`
- `GREY` = `ManimColor('#7F7F7F')`
- `GREY` = `ManimColor('#929591')`
- `GREY` = `ManimColor('#888888')`
- `GREYBLUE` = `ManimColor('#647D8E')`
- `GREYBROWN` = `ManimColor('#7F7053')`
- `GREYGREEN` = `ManimColor('#86A17D')`
- `GREYISH` = `ManimColor('#A8A495')`
- `GREYISHBLUE` = `ManimColor('#5E819D')`
- `GREYISHBROWN` = `ManimColor('#7A6A4F')`
- `GREYISHGREEN` = `ManimColor('#82A67D')`
- `GREYISHPINK` = `ManimColor('#C88D94')`
- `GREYISHPURPLE` = `ManimColor('#887191')`
- `GREYISHTEAL` = `ManimColor('#719F91')`
- `GREYPINK` = `ManimColor('#C3909B')`
- `GREYPURPLE` = `ManimColor('#826D8C')`
- `GREYTEAL` = `ManimColor('#5E9B8A')`
- `GREY_A` = `ManimColor('#DDDDDD')`
- `GREY_A` = `ManimColor('#DDDDDD')`
- `GREY_B` = `ManimColor('#BBBBBB')`
- `GREY_B` = `ManimColor('#BBBBBB')`
- `GREY_BROWN` = `ManimColor('#736357')`
- `GREY_BROWN` = `ManimColor('#736357')`
- `GREY_C` = `ManimColor('#888888')`
- `GREY_C` = `ManimColor('#888888')`
- `GREY_D` = `ManimColor('#444444')`
- `GREY_D` = `ManimColor('#444444')`
- `GREY_E` = `ManimColor('#222222')`
- `GREY_E` = `ManimColor('#222222')`
- `GROSSGREEN` = `ManimColor('#A0BF16')`
- `GULF_RED` = `ManimColor('#793932')`
- `GUNMETAL` = `ManimColor('#536267')`
- `HAZEL` = `ManimColor('#8E7618')`
- `HEATHER` = `ManimColor('#A484AC')`
- `HELIOTROPE` = `ManimColor('#D94FF5')`
- `HIGHLIGHTERGREEN` = `ManimColor('#1BFC06')`
- `HONEYDEW` = `ManimColor('#EFFFEF')`
- `HONEYDEW1` = `ManimColor('#F0FFF0')`
- `HONEYDEW2` = `ManimColor('#E0EEE0')`
- `HONEYDEW3` = `ManimColor('#C1CDC1')`
- `HONEYDEW4` = `ManimColor('#838B83')`
- `HOSPITALGREEN` = `ManimColor('#9BE5AA')`
- `HOTGREEN` = `ManimColor('#25FF29')`
- `HOTMAGENTA` = `ManimColor('#F504C9')`
- `HOTPINK` = `ManimColor('#FF68B3')`
- `HOTPINK` = `ManimColor('#FF69B4')`
- `HOTPINK` = `ManimColor('#FF028D')`
- `HOTPINK1` = `ManimColor('#FF6EB4')`
- `HOTPINK2` = `ManimColor('#EE6AA7')`
- `HOTPINK3` = `ManimColor('#CD6090')`
- `HOTPINK4` = `ManimColor('#8B3A62')`
- `HOTPURPLE` = `ManimColor('#CB00F5')`
- `HUNTERGREEN` = `ManimColor('#0B4008')`
- `ICE` = `ManimColor('#D6FFFA')`
- `ICEBLUE` = `ManimColor('#D7FFFE')`
- `ICKYGREEN` = `ManimColor('#8FAE22')`
- `IMPERIAL_BROWN` = `ManimColor('#61361E')`
- `INDIANRED` = `ManimColor('#CD5B5B')`
- `INDIANRED` = `ManimColor('#CD5C5C')`
- `INDIANRED` = `ManimColor('#850E04')`
- `INDIANRED1` = `ManimColor('#FF6A6A')`
- `INDIANRED2` = `ManimColor('#EE6363')`
- `INDIANRED3` = `ManimColor('#CD5555')`
- `INDIANRED4` = `ManimColor('#8B3A3A')`
- `INDIGO` = `ManimColor('#4A0082')`
- `INDIGO` = `ManimColor('#380282')`
- `INDIGOBLUE` = `ManimColor('#3A18B1')`
- `INTERNATIONAL_ORANGE` = `ManimColor('#E45523')`
- `IRIS` = `ManimColor('#6258C4')`
- `IRISHGREEN` = `ManimColor('#019529')`
- `IVORY` = `ManimColor('#FFFFEF')`
- `IVORY` = `ManimColor('#FFFFCB')`
- `IVORY1` = `ManimColor('#FFFFF0')`
- `IVORY2` = `ManimColor('#EEEEE0')`
- `IVORY3` = `ManimColor('#CDCDC1')`
- `IVORY4` = `ManimColor('#8B8B83')`
- `JADE` = `ManimColor('#1FA774')`
- `JADEGREEN` = `ManimColor('#2BAF6A')`
- `JASMINE_YELLOW` = `ManimColor('#F3D163')`
- `JUNGLEGREEN` = `ManimColor('#00A99A')`
- `JUNGLEGREEN` = `ManimColor('#048243')`
- `KELLEYGREEN` = `ManimColor('#009337')`
- `KELLYGREEN` = `ManimColor('#02AB2E')`
- `KERMITGREEN` = `ManimColor('#5CB200')`
- `KEYLIME` = `ManimColor('#AEFF6E')`
- `KHAKI` = `ManimColor('#EFE58C')`
- `KHAKI` = `ManimColor('#F0E68C')`
- `KHAKI` = `ManimColor('#AAA662')`
- `KHAKI1` = `ManimColor('#FFF68F')`
- `KHAKI2` = `ManimColor('#EEE685')`
- `KHAKI3` = `ManimColor('#CDC673')`
- `KHAKI4` = `ManimColor('#8B864E')`
- `KHAKIGREEN` = `ManimColor('#728639')`
- `KIWI` = `ManimColor('#9CEF43')`
- `KIWIGREEN` = `ManimColor('#8EE53F')`
- `LAVENDER` = `ManimColor('#F49EC4')`
- `LAVENDER` = `ManimColor('#E5E5F9')`
- `LAVENDER` = `ManimColor('#E6E6FA')`
- `LAVENDER` = `ManimColor('#C79FEF')`
- `LAVENDERBLUE` = `ManimColor('#8B88F8')`
- `LAVENDERBLUSH` = `ManimColor('#FFEFF4')`
- `LAVENDERBLUSH1` = `ManimColor('#FFF0F5')`
- `LAVENDERBLUSH2` = `ManimColor('#EEE0E5')`
- `LAVENDERBLUSH3` = `ManimColor('#CDC1C5')`
- `LAVENDERBLUSH4` = `ManimColor('#8B8386')`
- `LAVENDERPINK` = `ManimColor('#DD85D7')`
- `LAWNGREEN` = `ManimColor('#7CFC00')`
- `LAWNGREEN` = `ManimColor('#7CFC00')`
- `LAWNGREEN` = `ManimColor('#4DA409')`
- `LEAD` = `ManimColor('#525B55')`
- `LEAF` = `ManimColor('#71AA34')`
- `LEAFGREEN` = `ManimColor('#5CA904')`
- `LEAFYGREEN` = `ManimColor('#51B73B')`
- `LEAF_BROWN` = `ManimColor('#8D5B41')`
- `LEATHER` = `ManimColor('#AC7434')`
- `LEMON` = `ManimColor('#FDD906')`
- `LEMON` = `ManimColor('#FDFF52')`
- `LEMONCHIFFON` = `ManimColor('#FFF9CD')`
- `LEMONCHIFFON1` = `ManimColor('#FFFACD')`
- `LEMONCHIFFON2` = `ManimColor('#EEE9BF')`
- `LEMONCHIFFON3` = `ManimColor('#CDC9A5')`
- `LEMONCHIFFON4` = `ManimColor('#8B8970')`
- `LEMONGREEN` = `ManimColor('#ADF802')`
- `LEMONLIME` = `ManimColor('#BFFE28')`
- `LEMONYELLOW` = `ManimColor('#FDFF38')`
- `LICHEN` = `ManimColor('#8FB67B')`
- `LIGHT` = `ManimColor('#EEDD82')`
- `LIGHTAQUA` = `ManimColor('#8CFFDB')`
- `LIGHTAQUAMARINE` = `ManimColor('#7BFDC7')`
- `LIGHTBEIGE` = `ManimColor('#FFFEB6')`
- `LIGHTBLUE` = `ManimColor('#ADD8E5')`
- `LIGHTBLUE` = `ManimColor('#ADD8E6')`
- `LIGHTBLUE` = `ManimColor('#7BC8F6')`
- `LIGHTBLUE1` = `ManimColor('#BFEFFF')`
- `LIGHTBLUE2` = `ManimColor('#B2DFEE')`
- `LIGHTBLUE3` = `ManimColor('#9AC0CD')`
- `LIGHTBLUE4` = `ManimColor('#68838B')`
- `LIGHTBLUEGREEN` = `ManimColor('#7EFBB3')`
- `LIGHTBLUEGREY` = `ManimColor('#B7C9E2')`
- `LIGHTBLUISHGREEN` = `ManimColor('#76FDA8')`
- `LIGHTBRIGHTGREEN` = `ManimColor('#53FE5C')`
- `LIGHTBROWN` = `ManimColor('#AD8150')`
- `LIGHTBURGUNDY` = `ManimColor('#A8415B')`
- `LIGHTCORAL` = `ManimColor('#EF7F7F')`
- `LIGHTCORAL` = `ManimColor('#F08080')`
- `LIGHTCYAN` = `ManimColor('#E0FFFF')`
- `LIGHTCYAN` = `ManimColor('#ACFFFC')`
- `LIGHTCYAN1` = `ManimColor('#E0FFFF')`
- `LIGHTCYAN2` = `ManimColor('#D1EEEE')`
- `LIGHTCYAN3` = `ManimColor('#B4CDCD')`
- `LIGHTCYAN4` = `ManimColor('#7A8B8B')`
- `LIGHTEGGPLANT` = `ManimColor('#894585')`
- `LIGHTERGREEN` = `ManimColor('#75FD63')`
- `LIGHTERPURPLE` = `ManimColor('#A55AF4')`
- `LIGHTER_GRAY` = `ManimColor('#DDDDDD')`
- `LIGHTER_GRAY` = `ManimColor('#DDDDDD')`
- `LIGHTER_GREY` = `ManimColor('#DDDDDD')`
- `LIGHTER_GREY` = `ManimColor('#DDDDDD')`
- `LIGHTFORESTGREEN` = `ManimColor('#4F9153')`
- `LIGHTGOLD` = `ManimColor('#FDDC5C')`
- `LIGHTGOLDENROD` = `ManimColor('#EDDD82')`
- `LIGHTGOLDENROD1` = `ManimColor('#FFEC8B')`
- `LIGHTGOLDENROD2` = `ManimColor('#EEDC82')`
- `LIGHTGOLDENROD3` = `ManimColor('#CDBE70')`
- `LIGHTGOLDENROD4` = `ManimColor('#8B814C')`
- `LIGHTGOLDENRODYELLOW` = `ManimColor('#F9F9D2')`
- `LIGHTGOLDENRODYELLOW` = `ManimColor('#FAFAD2')`
- `LIGHTGRASSGREEN` = `ManimColor('#9AF764')`
- `LIGHTGRAY` = `ManimColor('#D3D3D3')`
- `LIGHTGRAY` = `ManimColor('#D3D3D3')`
- `LIGHTGREEN` = `ManimColor('#90ED90')`
- `LIGHTGREEN` = `ManimColor('#76FF7B')`
- `LIGHTGREENBLUE` = `ManimColor('#56FCA2')`
- `LIGHTGREENISHBLUE` = `ManimColor('#63F7B4')`
- `LIGHTGREY` = `ManimColor('#D3D3D3')`
- `LIGHTGREY` = `ManimColor('#D8DCD6')`
- `LIGHTGREYBLUE` = `ManimColor('#9DBCD4')`
- `LIGHTGREYGREEN` = `ManimColor('#B7E1A1')`
- `LIGHTINDIGO` = `ManimColor('#6D5ACF')`
- `LIGHTISHBLUE` = `ManimColor('#3D7AFD')`
- `LIGHTISHGREEN` = `ManimColor('#61E160')`
- `LIGHTISHPURPLE` = `ManimColor('#A552E6')`
- `LIGHTISHRED` = `ManimColor('#FE2F4A')`
- `LIGHTKHAKI` = `ManimColor('#E6F2A2')`
- `LIGHTLAVENDAR` = `ManimColor('#EFC0FE')`
- `LIGHTLAVENDER` = `ManimColor('#DFC5FE')`
- `LIGHTLIGHTBLUE` = `ManimColor('#CAFFFB')`
- `LIGHTLIGHTGREEN` = `ManimColor('#C8FFB0')`
- `LIGHTLILAC` = `ManimColor('#EDC8FF')`
- `LIGHTLIME` = `ManimColor('#AEFD6C')`
- `LIGHTLIMEGREEN` = `ManimColor('#B9FF66')`
- `LIGHTMAGENTA` = `ManimColor('#FA5FF7')`
- `LIGHTMAROON` = `ManimColor('#A24857')`
- `LIGHTMAUVE` = `ManimColor('#C292A1')`
- `LIGHTMINT` = `ManimColor('#B6FFBB')`
- `LIGHTMINTGREEN` = `ManimColor('#A6FBB2')`
- `LIGHTMOSSGREEN` = `ManimColor('#A6C875')`
- `LIGHTMUSTARD` = `ManimColor('#F7D560')`
- `LIGHTNAVY` = `ManimColor('#155084')`
- `LIGHTNAVYBLUE` = `ManimColor('#2E5A88')`
- `LIGHTNEONGREEN` = `ManimColor('#4EFD54')`
- `LIGHTOLIVE` = `ManimColor('#ACBF69')`
- `LIGHTOLIVEGREEN` = `ManimColor('#A4BE5C')`
- `LIGHTORANGE` = `ManimColor('#FDAA48')`
- `LIGHTPASTELGREEN` = `ManimColor('#B2FBA5')`
- `LIGHTPEACH` = `ManimColor('#FFD8B1')`
- `LIGHTPEAGREEN` = `ManimColor('#C4FE82')`
- `LIGHTPERIWINKLE` = `ManimColor('#C1C6FC')`
- `LIGHTPINK` = `ManimColor('#FFB5C0')`
- `LIGHTPINK` = `ManimColor('#FFB6C1')`
- `LIGHTPINK` = `ManimColor('#FFD1DF')`
- `LIGHTPINK1` = `ManimColor('#FFAEB9')`
- `LIGHTPINK2` = `ManimColor('#EEA2AD')`
- `LIGHTPINK3` = `ManimColor('#CD8C95')`
- `LIGHTPINK4` = `ManimColor('#8B5F65')`
- `LIGHTPLUM` = `ManimColor('#9D5783')`
- `LIGHTPURPLE` = `ManimColor('#BF77F6')`
- `LIGHTRED` = `ManimColor('#FF474C')`
- `LIGHTROSE` = `ManimColor('#FFC5CB')`
- `LIGHTROYALBLUE` = `ManimColor('#3A2EFE')`
- `LIGHTSAGE` = `ManimColor('#BCECAC')`
- `LIGHTSALMON` = `ManimColor('#FFA07A')`
- `LIGHTSALMON` = `ManimColor('#FEA993')`
- `LIGHTSALMON1` = `ManimColor('#FFA07A')`
- `LIGHTSALMON2` = `ManimColor('#EE9572')`
- `LIGHTSALMON3` = `ManimColor('#CD8162')`
- `LIGHTSALMON4` = `ManimColor('#8B5742')`
- `LIGHTSEAFOAM` = `ManimColor('#A0FEBF')`
- `LIGHTSEAFOAMGREEN` = `ManimColor('#A7FFB5')`
- `LIGHTSEAGREEN` = `ManimColor('#1FB1AA')`
- `LIGHTSEAGREEN` = `ManimColor('#20B2AA')`
- `LIGHTSEAGREEN` = `ManimColor('#98F6B0')`
- `LIGHTSKYBLUE` = `ManimColor('#87CEF9')`
- `LIGHTSKYBLUE` = `ManimColor('#87CEFA')`
- `LIGHTSKYBLUE` = `ManimColor('#C6FCFF')`
- `LIGHTSKYBLUE1` = `ManimColor('#B0E2FF')`
- `LIGHTSKYBLUE2` = `ManimColor('#A4D3EE')`
- `LIGHTSKYBLUE3` = `ManimColor('#8DB6CD')`
- `LIGHTSKYBLUE4` = `ManimColor('#607B8B')`
- `LIGHTSLATEBLUE` = `ManimColor('#8470FF')`
- `LIGHTSLATEBLUE` = `ManimColor('#8470FF')`
- `LIGHTSLATEGRAY` = `ManimColor('#778799')`
- `LIGHTSLATEGRAY` = `ManimColor('#778899')`
- `LIGHTSLATEGREY` = `ManimColor('#778799')`
- `LIGHTSTEELBLUE` = `ManimColor('#AFC4DD')`
- `LIGHTSTEELBLUE` = `ManimColor('#B0C4DE')`
- `LIGHTSTEELBLUE1` = `ManimColor('#CAE1FF')`
- `LIGHTSTEELBLUE2` = `ManimColor('#BCD2EE')`
- `LIGHTSTEELBLUE3` = `ManimColor('#A2B5CD')`
- `LIGHTSTEELBLUE4` = `ManimColor('#6E7B8B')`
- `LIGHTTAN` = `ManimColor('#FBEEAC')`
- `LIGHTTEAL` = `ManimColor('#90E4C1')`
- `LIGHTTURQUOISE` = `ManimColor('#7EF4CC')`
- `LIGHTURPLE` = `ManimColor('#B36FF6')`
- `LIGHTVIOLET` = `ManimColor('#D6B4FC')`
- `LIGHTYELLOW` = `ManimColor('#FFFFE0')`
- `LIGHTYELLOW` = `ManimColor('#FFFE7A')`
- `LIGHTYELLOW1` = `ManimColor('#FFFFE0')`
- `LIGHTYELLOW2` = `ManimColor('#EEEED1')`
- `LIGHTYELLOW3` = `ManimColor('#CDCDB4')`
- `LIGHTYELLOW4` = `ManimColor('#8B8B7A')`
- `LIGHTYELLOWGREEN` = `ManimColor('#CCFD7F')`
- `LIGHTYELLOWISHGREEN` = `ManimColor('#C2FF89')`
- `LIGHT_ADMIRALTY_GREY` = `ManimColor('#B6D3CC')`
- `LIGHT_AIRCRAFT_GREY` = `ManimColor('#BEC0B8')`
- `LIGHT_BEIGE` = `ManimColor('#F5E7A1')`
- `LIGHT_BISCUIT` = `ManimColor('#E8C88F')`
- `LIGHT_BRONZE_GREEN` = `ManimColor('#6A7031')`
- `LIGHT_BROWN` = `ManimColor('#CD853F')`
- `LIGHT_BROWN` = `ManimColor('#9E7339')`
- `LIGHT_BROWN` = `ManimColor('#CD853F')`
- `LIGHT_BRUNSWICK_GREEN` = `ManimColor('#406A28')`
- `LIGHT_BUFF` = `ManimColor('#F6C870')`
- `LIGHT_FRENCH_BLUE` = `ManimColor('#4F81C5')`
- `LIGHT_GRAY` = `ManimColor('#BBBBBB')`
- `LIGHT_GRAY` = `ManimColor('#BBBBBB')`
- `LIGHT_GREY` = `ManimColor('#BBBBBB')`
- `LIGHT_GREY` = `ManimColor('#9AAA9F')`
- `LIGHT_GREY` = `ManimColor('#BBBBBB')`
- `LIGHT_OLIVE_GREEN` = `ManimColor('#87965A')`
- `LIGHT_ORANGE` = `ManimColor('#EF841E')`
- `LIGHT_PINK` = `ManimColor('#DC75CD')`
- `LIGHT_PINK` = `ManimColor('#DC75CD')`
- `LIGHT_PURPLE_BROWN` = `ManimColor('#693B3F')`
- `LIGHT_SLATE_GREY` = `ManimColor('#667563')`
- `LIGHT_STONE` = `ManimColor('#D4B97D')`
- `LIGHT_STRAW` = `ManimColor('#EEDFA5')`
- `LIGHT_VIOLET` = `ManimColor('#C9A8CE')`
- `LIGHT_WEATHERWORK_GREY` = `ManimColor('#A9B7B9')`
- `LILAC` = `ManimColor('#CEA2FD')`
- `LILIAC` = `ManimColor('#C48EFD')`
- `LIME` = `ManimColor('#00FF00')`
- `LIME` = `ManimColor('#AAFF32')`
- `LIMEGREEN` = `ManimColor('#8DC73E')`
- `LIMEGREEN` = `ManimColor('#31CD31')`
- `LIMEGREEN` = `ManimColor('#32CD32')`
- `LIMEGREEN` = `ManimColor('#89FE05')`
- `LIMEYELLOW` = `ManimColor('#D0FE1D')`
- `LINCON_GREEN` = `ManimColor('#2E4C1E')`
- `LINEN` = `ManimColor('#F9EFE5')`
- `LINEN` = `ManimColor('#FAF0E6')`
- `LIPSTICK` = `ManimColor('#D5174E')`
- `LIPSTICKRED` = `ManimColor('#C0022F')`
- `LOGO_BLACK` = `ManimColor('#343434')`
- `LOGO_BLACK` = `ManimColor('#343434')`
- `LOGO_BLUE` = `ManimColor('#525893')`
- `LOGO_BLUE` = `ManimColor('#525893')`
- `LOGO_GREEN` = `ManimColor('#87C2A5')`
- `LOGO_GREEN` = `ManimColor('#87C2A5')`
- `LOGO_RED` = `ManimColor('#E07A5F')`
- `LOGO_RED` = `ManimColor('#E07A5F')`
- `LOGO_WHITE` = `ManimColor('#ECE7E2')`
- `LOGO_WHITE` = `ManimColor('#ECE7E2')`
- `MACARONIANDCHEESE` = `ManimColor('#EFB435')`
- `MAGENTA` = `ManimColor('#EC008C')`
- `MAGENTA` = `ManimColor('#FF00FF')`
- `MAGENTA` = `ManimColor('#FF00FF')`
- `MAGENTA` = `ManimColor('#C20078')`
- `MAGENTA2` = `ManimColor('#EE00EE')`
- `MAGENTA3` = `ManimColor('#CD00CD')`
- `MAGENTA4` = `ManimColor('#8B008B')`
- `MAHOGANY` = `ManimColor('#A9341F')`
- `MAHOGANY` = `ManimColor('#4A0100')`
- `MAIZE` = `ManimColor('#F4D054')`
- `MANGO` = `ManimColor('#FFA62B')`
- `MANILLA` = `ManimColor('#FEF6BF')`
- `MANILLA` = `ManimColor('#FFFA86')`
- `MARIGOLD` = `ManimColor('#FCC006')`
- `MARINE` = `ManimColor('#042E60')`
- `MARINEBLUE` = `ManimColor('#01386A')`
- `MAROON` = `ManimColor('#C55F73')`
- `MAROON` = `ManimColor('#471B21')`
- `MAROON` = `ManimColor('#AF3235')`
- `MAROON` = `ManimColor('#7F0000')`
- `MAROON` = `ManimColor('#B03060')`
- `MAROON` = `ManimColor('#650021')`
- `MAROON` = `ManimColor('#C55F73')`
- `MAROON1` = `ManimColor('#FF34B3')`
- `MAROON2` = `ManimColor('#EE30A7')`
- `MAROON3` = `ManimColor('#CD2990')`
- `MAROON4` = `ManimColor('#8B1C62')`
- `MAROON_A` = `ManimColor('#ECABC1')`
- `MAROON_A` = `ManimColor('#ECABC1')`
- `MAROON_B` = `ManimColor('#EC92AB')`
- `MAROON_B` = `ManimColor('#EC92AB')`
- `MAROON_C` = `ManimColor('#C55F73')`
- `MAROON_C` = `ManimColor('#C55F73')`
- `MAROON_D` = `ManimColor('#A24D61')`
- `MAROON_D` = `ManimColor('#A24D61')`
- `MAROON_E` = `ManimColor('#94424F')`
- `MAROON_E` = `ManimColor('#94424F')`
- `MAUVE` = `ManimColor('#AE7181')`
- `MEDIUM` = `ManimColor('#66CDAA')`
- `MEDIUMAQUAMARINE` = `ManimColor('#66CDAA')`
- `MEDIUMAQUAMARINE` = `ManimColor('#66CDAA')`
- `MEDIUMBLUE` = `ManimColor('#0000CD')`
- `MEDIUMBLUE` = `ManimColor('#0000CD')`
- `MEDIUMBLUE` = `ManimColor('#2C6FBB')`
- `MEDIUMBROWN` = `ManimColor('#7F5112')`
- `MEDIUMGREEN` = `ManimColor('#39AD48')`
- `MEDIUMGREY` = `ManimColor('#7D7F7C')`
- `MEDIUMORCHID` = `ManimColor('#BA54D3')`
- `MEDIUMORCHID` = `ManimColor('#BA55D3')`
- `MEDIUMORCHID1` = `ManimColor('#E066FF')`
- `MEDIUMORCHID2` = `ManimColor('#D15FEE')`
- `MEDIUMORCHID3` = `ManimColor('#B452CD')`
- `MEDIUMORCHID4` = `ManimColor('#7A378B')`
- `MEDIUMPINK` = `ManimColor('#F36196')`
- `MEDIUMPURPLE` = `ManimColor('#9270DB')`
- `MEDIUMPURPLE` = `ManimColor('#9370DB')`
- `MEDIUMPURPLE` = `ManimColor('#9E43A2')`
- `MEDIUMPURPLE1` = `ManimColor('#AB82FF')`
- `MEDIUMPURPLE2` = `ManimColor('#9F79EE')`
- `MEDIUMPURPLE3` = `ManimColor('#8968CD')`
- `MEDIUMPURPLE4` = `ManimColor('#5D478B')`
- `MEDIUMSEAGREEN` = `ManimColor('#3BB271')`
- `MEDIUMSEAGREEN` = `ManimColor('#3CB371')`
- `MEDIUMSLATEBLUE` = `ManimColor('#7B68ED')`
- `MEDIUMSLATEBLUE` = `ManimColor('#7B68EE')`
- `MEDIUMSPRINGGREEN` = `ManimColor('#00F99A')`
- `MEDIUMSPRINGGREEN` = `ManimColor('#00FA9A')`
- `MEDIUMTURQUOISE` = `ManimColor('#48D1CC')`
- `MEDIUMTURQUOISE` = `ManimColor('#48D1CC')`
- `MEDIUMVIOLETRED` = `ManimColor('#C61584')`
- `MEDIUMVIOLETRED` = `ManimColor('#C71585')`
- `MEDIUM_SEA_GREY` = `ManimColor('#8E9B9C')`
- `MELON` = `ManimColor('#F89E7B')`
- `MELON` = `ManimColor('#FF7855')`
- `MERLOT` = `ManimColor('#730039')`
- `METALLICBLUE` = `ManimColor('#4F738E')`
- `MIDBLUE` = `ManimColor('#276AB3')`
- `MIDDLE_BLUE` = `ManimColor('#1C5680')`
- `MIDDLE_BRONZE_GREEN` = `ManimColor('#49523A')`
- `MIDDLE_BROWN` = `ManimColor('#74542F')`
- `MIDDLE_BUFF` = `ManimColor('#DBAC50')`
- `MIDDLE_GRAPHITE` = `ManimColor('#4E5355')`
- `MIDDLE_STONE` = `ManimColor('#AC7C42')`
- `MIDGREEN` = `ManimColor('#50A747')`
- `MIDNIGHT` = `ManimColor('#03012D')`
- `MIDNIGHTBLUE` = `ManimColor('#006795')`
- `MIDNIGHTBLUE` = `ManimColor('#181870')`
- `MIDNIGHTBLUE` = `ManimColor('#191970')`
- `MIDNIGHTBLUE` = `ManimColor('#020035')`
- `MIDNIGHTPURPLE` = `ManimColor('#280137')`
- `MID_BRUNSWICK_GREEN` = `ManimColor('#33533B')`
- `MILITARYGREEN` = `ManimColor('#667C3E')`
- `MILKCHOCOLATE` = `ManimColor('#7F4E1E')`
- `MINT` = `ManimColor('#9FFEB0')`
- `MINTCREAM` = `ManimColor('#F4FFF9')`
- `MINTCREAM` = `ManimColor('#F5FFFA')`
- `MINTGREEN` = `ManimColor('#8FFF9F')`
- `MINTYGREEN` = `ManimColor('#0BF77D')`
- `MISTYROSE` = `ManimColor('#FFE3E1')`
- `MISTYROSE1` = `ManimColor('#FFE4E1')`
- `MISTYROSE2` = `ManimColor('#EED5D2')`
- `MISTYROSE3` = `ManimColor('#CDB7B5')`
- `MISTYROSE4` = `ManimColor('#8B7D7B')`
- `MOCCASIN` = `ManimColor('#FFE3B5')`
- `MOCCASIN` = `ManimColor('#FFE4B5')`
- `MOCHA` = `ManimColor('#9D7651')`
- `MOSS` = `ManimColor('#769958')`
- `MOSSGREEN` = `ManimColor('#658B38')`
- `MOSSYGREEN` = `ManimColor('#638B27')`
- `MUD` = `ManimColor('#735C12')`
- `MUDBROWN` = `ManimColor('#60460F')`
- `MUDDYBROWN` = `ManimColor('#886806')`
- `MUDDYGREEN` = `ManimColor('#657432')`
- `MUDDYYELLOW` = `ManimColor('#BFAC05')`
- `MUDGREEN` = `ManimColor('#606602')`
- `MULBERRY` = `ManimColor('#A93C93')`
- `MULBERRY` = `ManimColor('#920A4E')`
- `MURKYGREEN` = `ManimColor('#6C7A0E')`
- `MUSHROOM` = `ManimColor('#BA9E88')`
- `MUSTARD` = `ManimColor('#CEB301')`
- `MUSTARDBROWN` = `ManimColor('#AC7E04')`
- `MUSTARDGREEN` = `ManimColor('#A8B504')`
- `MUSTARDYELLOW` = `ManimColor('#D2BD0A')`
- `MUTEDBLUE` = `ManimColor('#3B719F')`
- `MUTEDGREEN` = `ManimColor('#5FA052')`
- `MUTEDPINK` = `ManimColor('#D1768F')`
- `MUTEDPURPLE` = `ManimColor('#805B87')`
- `N11_PEARL_GREY` = `ManimColor('#D8D3C7')`
- `N12_PASTEL_GREY` = `ManimColor('#CCCCCC')`
- `N14_WHITE` = `ManimColor('#FFFFFF')`
- `N15_HOMEBUSH_GREY` = `ManimColor('#A29B93')`
- `N22_CLOUD_GREY` = `ManimColor('#C4C1B9')`
- `N23_NEUTRAL_GREY` = `ManimColor('#CCCCCC')`
- `N24_SILVER_GREY` = `ManimColor('#BDC7C5')`
- `N25_BIRCH_GREY` = `ManimColor('#ABA498')`
- `N32_GREEN_GREY` = `ManimColor('#8E9282')`
- `N33_LIGHTBOX_GREY` = `ManimColor('#ACADAD')`
- `N35_LIGHT_GREY` = `ManimColor('#A6A7A1')`
- `N41_OYSTER` = `ManimColor('#998F78')`
- `N42_STORM_GREY` = `ManimColor('#858F88')`
- `N43_PIPELINE_GREY` = `ManimColor('#999999')`
- `N44_BRIDGE_GREY` = `ManimColor('#767779')`
- `N45_KOALA_GREY` = `ManimColor('#928F88')`
- `N52_MID_GREY` = `ManimColor('#727A77')`
- `N53_BLUE_GREY` = `ManimColor('#7C8588')`
- `N54_BASALT` = `ManimColor('#585C63')`
- `N55_LEAD_GREY` = `ManimColor('#5E5C58')`
- `N61_BLACK` = `ManimColor('#2A2A2C')`
- `N63_PEWTER` = `ManimColor('#596064')`
- `N64_DARK_GREY` = `ManimColor('#4B5259')`
- `N65_GRAPHITE_GREY` = `ManimColor('#45474A')`
- `NASTYGREEN` = `ManimColor('#70B23F')`
- `NATO_GREEN` = `ManimColor('#5F5C4B')`
- `NAVAJOWHITE` = `ManimColor('#FFDDAD')`
- `NAVAJOWHITE1` = `ManimColor('#FFDEAD')`
- `NAVAJOWHITE2` = `ManimColor('#EECFA1')`
- `NAVAJOWHITE3` = `ManimColor('#CDB38B')`
- `NAVAJOWHITE4` = `ManimColor('#8B795E')`
- `NAVY` = `ManimColor('#00007F')`
- `NAVY` = `ManimColor('#01153E')`
- `NAVYBLUE` = `ManimColor('#006EB8')`
- `NAVYBLUE` = `ManimColor('#00007F')`
- `NAVYBLUE` = `ManimColor('#000080')`
- `NAVYBLUE` = `ManimColor('#001146')`
- `NAVYGREEN` = `ManimColor('#35530A')`
- `NEONBLUE` = `ManimColor('#04D9FF')`
- `NEONGREEN` = `ManimColor('#0CFF0C')`
- `NEONPINK` = `ManimColor('#FE019A')`
- `NEONPURPLE` = `ManimColor('#BC13FE')`
- `NEONRED` = `ManimColor('#FF073A')`
- `NEONYELLOW` = `ManimColor('#CFFF04')`
- `NICEBLUE` = `ManimColor('#107AB0')`
- `NIGHT` = `ManimColor('#282B2F')`
- `NIGHTBLUE` = `ManimColor('#040348')`
- `NUT_BROWN` = `ManimColor('#402D21')`
- `OCEAN` = `ManimColor('#017B92')`
- `OCEANBLUE` = `ManimColor('#03719C')`
- `OCEANGREEN` = `ManimColor('#3D9973')`
- `OCHER` = `ManimColor('#BF9B0C')`
- `OCHRE` = `ManimColor('#BF9005')`
- `OCRE` = `ManimColor('#C69C04')`
- `OFFBLUE` = `ManimColor('#5684AE')`
- `OFFGREEN` = `ManimColor('#6BA353')`
- `OFFWHITE` = `ManimColor('#FFFFE4')`
- `OFFYELLOW` = `ManimColor('#F1F33F')`
- `OLDLACE` = `ManimColor('#FCF4E5')`
- `OLDLACE` = `ManimColor('#FDF5E6')`
- `OLDPINK` = `ManimColor('#C77986')`
- `OLDROSE` = `ManimColor('#C87F89')`
- `OLIVE` = `ManimColor('#7F7F00')`
- `OLIVE` = `ManimColor('#6E750E')`
- `OLIVEBROWN` = `ManimColor('#645403')`
- `OLIVEDRAB` = `ManimColor('#6B8D22')`
- `OLIVEDRAB` = `ManimColor('#6B8E23')`
- `OLIVEDRAB` = `ManimColor('#6F7632')`
- `OLIVEDRAB1` = `ManimColor('#C0FF3E')`
- `OLIVEDRAB2` = `ManimColor('#B3EE3A')`
- `OLIVEDRAB4` = `ManimColor('#698B22')`
- `OLIVEGREEN` = `ManimColor('#3C8031')`
- `OLIVEGREEN` = `ManimColor('#677A04')`
- `OLIVEYELLOW` = `ManimColor('#C2B709')`
- `OLIVE_DRAB` = `ManimColor('#4F5138')`
- `OLIVE_GREEN` = `ManimColor('#4B5729')`
- `OPALINE_GREEN` = `ManimColor('#8FC693')`
- `ORANGE` = `ManimColor('#FF862F')`
- `ORANGE` = `ManimColor('#F58137')`
- `ORANGE` = `ManimColor('#FFA500')`
- `ORANGE` = `ManimColor('#F97306')`
- `ORANGE` = `ManimColor('#FF862F')`
- `ORANGE1` = `ManimColor('#FFA500')`
- `ORANGE2` = `ManimColor('#EE9A00')`
- `ORANGE3` = `ManimColor('#CD8500')`
- `ORANGE4` = `ManimColor('#8B5A00')`
- `ORANGEBROWN` = `ManimColor('#BE6400')`
- `ORANGEISH` = `ManimColor('#FD8D49')`
- `ORANGEPINK` = `ManimColor('#FF6F52')`
- `ORANGERED` = `ManimColor('#ED135A')`
- `ORANGERED` = `ManimColor('#FF4400')`
- `ORANGERED` = `ManimColor('#FE420F')`
- `ORANGERED1` = `ManimColor('#FF4500')`
- `ORANGERED2` = `ManimColor('#EE4000')`
- `ORANGERED3` = `ManimColor('#CD3700')`
- `ORANGERED4` = `ManimColor('#8B2500')`
- `ORANGEYBROWN` = `ManimColor('#B16002')`
- `ORANGEYELLOW` = `ManimColor('#FFAD01')`
- `ORANGEYRED` = `ManimColor('#FA4224')`
- `ORANGEYYELLOW` = `ManimColor('#FDB915')`
- `ORANGE_BROWN` = `ManimColor('#753B1E')`
- `ORANGISH` = `ManimColor('#FC824A')`
- `ORANGISHBROWN` = `ManimColor('#B25F03')`
- `ORANGISHRED` = `ManimColor('#F43605')`
- `ORCHID` = `ManimColor('#AF72B0')`
- `ORCHID` = `ManimColor('#DA70D6')`
- `ORCHID` = `ManimColor('#DA70D6')`
- `ORCHID` = `ManimColor('#C875C4')`
- `ORCHID1` = `ManimColor('#FF83FA')`
- `ORCHID2` = `ManimColor('#EE7AE9')`
- `ORCHID3` = `ManimColor('#CD69C9')`
- `ORCHID4` = `ManimColor('#8B4789')`
- `ORIENT_BLUE` = `ManimColor('#64A0AA')`
- `OXFORD_BLUE` = `ManimColor('#1F3057')`
- `P11_MAGENTA` = `ManimColor('#7B2B48')`
- `P12_PURPLE` = `ManimColor('#85467B')`
- `P13_VIOLET` = `ManimColor('#5D3A61')`
- `P14_BLUEBERRY` = `ManimColor('#4C4176')`
- `P21_SUNSET_PINK` = `ManimColor('#E3BBBD')`
- `P22_CYCLAMEN` = `ManimColor('#83597D')`
- `P23_LILAC` = `ManimColor('#A69FB1')`
- `P24_JACKARANDA` = `ManimColor('#795F91')`
- `P31_DUSTY_PINK` = `ManimColor('#DBBEBC')`
- `P33_RIBBON_PINK` = `ManimColor('#D1BCC9')`
- `P41_ERICA_PINK` = `ManimColor('#C55A83')`
- `P42_MULBERRY` = `ManimColor('#A06574')`
- `P43_WISTERIA` = `ManimColor('#756D91')`
- `P52_PLUM` = `ManimColor('#6E3D4B')`
- `PALE` = `ManimColor('#DB7093')`
- `PALE` = `ManimColor('#FFF9D0')`
- `PALEAQUA` = `ManimColor('#B8FFEB')`
- `PALEBLUE` = `ManimColor('#D0FEFE')`
- `PALEBROWN` = `ManimColor('#B1916E')`
- `PALECYAN` = `ManimColor('#B7FFFA')`
- `PALEGOLD` = `ManimColor('#FDDE6C')`
- `PALEGOLDENROD` = `ManimColor('#EDE8AA')`
- `PALEGOLDENROD` = `ManimColor('#EEE8AA')`
- `PALEGREEN` = `ManimColor('#97FB97')`
- `PALEGREEN` = `ManimColor('#98FB98')`
- `PALEGREEN` = `ManimColor('#C7FDB5')`
- `PALEGREEN1` = `ManimColor('#9AFF9A')`
- `PALEGREEN2` = `ManimColor('#90EE90')`
- `PALEGREEN3` = `ManimColor('#7CCD7C')`
- `PALEGREEN4` = `ManimColor('#548B54')`
- `PALEGREY` = `ManimColor('#FDFDFE')`
- `PALELAVENDER` = `ManimColor('#EECFFE')`
- `PALELIGHTGREEN` = `ManimColor('#B1FC99')`
- `PALELILAC` = `ManimColor('#E4CBFF')`
- `PALELIME` = `ManimColor('#BEFD73')`
- `PALELIMEGREEN` = `ManimColor('#B1FF65')`
- `PALEMAGENTA` = `ManimColor('#D767AD')`
- `PALEMAUVE` = `ManimColor('#FED0FC')`
- `PALEOLIVE` = `ManimColor('#B9CC81')`
- `PALEOLIVEGREEN` = `ManimColor('#B1D27B')`
- `PALEORANGE` = `ManimColor('#FFA756')`
- `PALEPEACH` = `ManimColor('#FFE5AD')`
- `PALEPINK` = `ManimColor('#FFCFDC')`
- `PALEPURPLE` = `ManimColor('#B790D4')`
- `PALERED` = `ManimColor('#D9544D')`
- `PALEROSE` = `ManimColor('#FDC1C5')`
- `PALESALMON` = `ManimColor('#FFB19A')`
- `PALESKYBLUE` = `ManimColor('#BDF6FE')`
- `PALETEAL` = `ManimColor('#82CBB2')`
- `PALETURQUOISE` = `ManimColor('#AFEDED')`
- `PALETURQUOISE` = `ManimColor('#AFEEEE')`
- `PALETURQUOISE` = `ManimColor('#A5FBD5')`
- `PALETURQUOISE1` = `ManimColor('#BBFFFF')`
- `PALETURQUOISE2` = `ManimColor('#AEEEEE')`
- `PALETURQUOISE3` = `ManimColor('#96CDCD')`
- `PALETURQUOISE4` = `ManimColor('#668B8B')`
- `PALEVIOLET` = `ManimColor('#CEAEFA')`
- `PALEVIOLETRED` = `ManimColor('#DB7092')`
- `PALEVIOLETRED` = `ManimColor('#DB7093')`
- `PALEVIOLETRED1` = `ManimColor('#FF82AB')`
- `PALEVIOLETRED2` = `ManimColor('#EE799F')`
- `PALEVIOLETRED3` = `ManimColor('#CD6889')`
- `PALEVIOLETRED4` = `ManimColor('#8B475D')`
- `PALEYELLOW` = `ManimColor('#FFFF84')`
- `PALE_BLUE` = `ManimColor('#8CC5BB')`
- `PALE_CREAM` = `ManimColor('#FCED96')`
- `PALE_ROUNDEL_BLUE` = `ManimColor('#A7C6EB')`
- `PALE_ROUNDEL_RED` = `ManimColor('#E8A1A2')`
- `PAPAYAWHIP` = `ManimColor('#FFEED4')`
- `PAPAYAWHIP` = `ManimColor('#FFEFD5')`
- `PARCHMENT` = `ManimColor('#FEFCAF')`
- `PASTELBLUE` = `ManimColor('#A2BFFE')`
- `PASTELGREEN` = `ManimColor('#B0FF9D')`
- `PASTELORANGE` = `ManimColor('#FF964F')`
- `PASTELPINK` = `ManimColor('#FFBACD')`
- `PASTELPURPLE` = `ManimColor('#CAA0FF')`
- `PASTELRED` = `ManimColor('#DB5856')`
- `PASTELYELLOW` = `ManimColor('#FFFE71')`
- `PEA` = `ManimColor('#A4BF20')`
- `PEACH` = `ManimColor('#F7965A')`
- `PEACH` = `ManimColor('#FFB07C')`
- `PEACHPUFF` = `ManimColor('#FFDAB8')`
- `PEACHPUFF1` = `ManimColor('#FFDAB9')`
- `PEACHPUFF2` = `ManimColor('#EECBAD')`
- `PEACHPUFF3` = `ManimColor('#CDAF95')`
- `PEACHPUFF4` = `ManimColor('#8B7765')`
- `PEACHYPINK` = `ManimColor('#FF9A8A')`
- `PEACOCKBLUE` = `ManimColor('#016795')`
- `PEACOCK_BLUE` = `ManimColor('#3B6879')`
- `PEAGREEN` = `ManimColor('#8EAB12')`
- `PEAR` = `ManimColor('#CBF85F')`
- `PEASOUP` = `ManimColor('#929901')`
- `PEASOUPGREEN` = `ManimColor('#94A617')`
- `PERIWINKLE` = `ManimColor('#7977B8')`
- `PERIWINKLE` = `ManimColor('#8E82FE')`
- `PERIWINKLEBLUE` = `ManimColor('#8F99FB')`
- `PERRYWINKLE` = `ManimColor('#8F8CE7')`
- `PERU` = `ManimColor('#CD843F')`
- `PETROL` = `ManimColor('#005F6A')`
- `PIGPINK` = `ManimColor('#E78EA5')`
- `PINE` = `ManimColor('#2B5D34')`
- `PINEGREEN` = `ManimColor('#008B72')`
- `PINEGREEN` = `ManimColor('#0A481E')`
- `PINK` = `ManimColor('#D147BD')`
- `PINK` = `ManimColor('#FFBFCA')`
- `PINK` = `ManimColor('#FFC0CB')`
- `PINK` = `ManimColor('#FF81C0')`
- `PINK` = `ManimColor('#D147BD')`
- `PINK1` = `ManimColor('#FFB5C5')`
- `PINK2` = `ManimColor('#EEA9B8')`
- `PINK3` = `ManimColor('#CD919E')`
- `PINK4` = `ManimColor('#8B636C')`
- `PINKISH` = `ManimColor('#D46A7E')`
- `PINKISHBROWN` = `ManimColor('#B17261')`
- `PINKISHGREY` = `ManimColor('#C8ACA9')`
- `PINKISHORANGE` = `ManimColor('#FF724C')`
- `PINKISHPURPLE` = `ManimColor('#D648D7')`
- `PINKISHRED` = `ManimColor('#F10C45')`
- `PINKISHTAN` = `ManimColor('#D99B82')`
- `PINKPURPLE` = `ManimColor('#EF1DE7')`
- `PINKRED` = `ManimColor('#F5054F')`
- `PINKY` = `ManimColor('#FC86AA')`
- `PINKYPURPLE` = `ManimColor('#C94CBE')`
- `PINKYRED` = `ManimColor('#FC2647')`
- `PISSYELLOW` = `ManimColor('#DDD618')`
- `PISTACHIO` = `ManimColor('#C0FA8B')`
- `PLUM` = `ManimColor('#92268F')`
- `PLUM` = `ManimColor('#DDA0DD')`
- `PLUM` = `ManimColor('#DDA0DD')`
- `PLUM` = `ManimColor('#580F41')`
- `PLUM1` = `ManimColor('#FFBBFF')`
- `PLUM2` = `ManimColor('#EEAEEE')`
- `PLUM3` = `ManimColor('#CD96CD')`
- `PLUM4` = `ManimColor('#8B668B')`
- `PLUMPURPLE` = `ManimColor('#4E0550')`
- `POISONGREEN` = `ManimColor('#40FD14')`
- `POO` = `ManimColor('#8F7303')`
- `POOBROWN` = `ManimColor('#885F01')`
- `POOP` = `ManimColor('#7F5E00')`
- `POOPBROWN` = `ManimColor('#7A5901')`
- `POOPGREEN` = `ManimColor('#6F7C00')`
- `POPPY` = `ManimColor('#BB3016')`
- `PORTLAND_STONE` = `ManimColor('#CEC093')`
- `POST_OFFICE_RED` = `ManimColor('#C41C22')`
- `POWDERBLUE` = `ManimColor('#AFE0E5')`
- `POWDERBLUE` = `ManimColor('#B0E0E6')`
- `POWDERBLUE` = `ManimColor('#B1D1FC')`
- `POWDERPINK` = `ManimColor('#FFB2D0')`
- `PRIMARYBLUE` = `ManimColor('#0804F9')`
- `PRIMROSE` = `ManimColor('#FEF963')`
- `PRIMROSE_2` = `ManimColor('#E9BB43')`
- `PROCESSBLUE` = `ManimColor('#00B0F0')`
- `PRUSSIANBLUE` = `ManimColor('#004577')`
- `PRU_BLUE` = `ManimColor('#5F7682')`
- `PUCE` = `ManimColor('#A57E52')`
- `PUKE` = `ManimColor('#A5A502')`
- `PUKEBROWN` = `ManimColor('#947706')`
- `PUKEGREEN` = `ManimColor('#9AAE07')`
- `PUKEYELLOW` = `ManimColor('#C2BE0E')`
- `PUMPKIN` = `ManimColor('#E17701')`
- `PUMPKINORANGE` = `ManimColor('#FB7D07')`
- `PUREBLUE` = `ManimColor('#0203E2')`
- `PURE_BLUE` = `ManimColor('#0000FF')`
- `PURE_BLUE` = `ManimColor('#0000FF')`
- `PURE_CYAN` = `ManimColor('#00FFFF')`
- `PURE_CYAN` = `ManimColor('#00FFFF')`
- `PURE_GREEN` = `ManimColor('#00FF00')`
- `PURE_GREEN` = `ManimColor('#00FF00')`
- `PURE_MAGENTA` = `ManimColor('#FF00FF')`
- `PURE_MAGENTA` = `ManimColor('#FF00FF')`
- `PURE_RED` = `ManimColor('#FF0000')`
- `PURE_RED` = `ManimColor('#FF0000')`
- `PURE_YELLOW` = `ManimColor('#FFFF00')`
- `PURE_YELLOW` = `ManimColor('#FFFF00')`
- `PURPLE` = `ManimColor('#9A72AC')`
- `PURPLE` = `ManimColor('#99479B')`
- `PURPLE` = `ManimColor('#7F007F')`
- `PURPLE` = `ManimColor('#A020F0')`
- `PURPLE` = `ManimColor('#7E1E9C')`
- `PURPLE` = `ManimColor('#9A72AC')`
- `PURPLE1` = `ManimColor('#9B30FF')`
- `PURPLE2` = `ManimColor('#912CEE')`
- `PURPLE3` = `ManimColor('#7D26CD')`
- `PURPLE4` = `ManimColor('#551A8B')`
- `PURPLEBLUE` = `ManimColor('#5D21D0')`
- `PURPLEBROWN` = `ManimColor('#673A3F')`
- `PURPLEGREY` = `ManimColor('#866F85')`
- `PURPLEISH` = `ManimColor('#98568D')`
- `PURPLEISHBLUE` = `ManimColor('#6140EF')`
- `PURPLEISHPINK` = `ManimColor('#DF4EC8')`
- `PURPLEPINK` = `ManimColor('#D725DE')`
- `PURPLERED` = `ManimColor('#990147')`
- `PURPLEY` = `ManimColor('#8756E4')`
- `PURPLEYBLUE` = `ManimColor('#5F34E7')`
- `PURPLEYGREY` = `ManimColor('#947E94')`
- `PURPLEYPINK` = `ManimColor('#C83CB9')`
- `PURPLE_A` = `ManimColor('#CAA3E8')`
- `PURPLE_A` = `ManimColor('#CAA3E8')`
- `PURPLE_B` = `ManimColor('#B189C6')`
- `PURPLE_B` = `ManimColor('#B189C6')`
- `PURPLE_C` = `ManimColor('#9A72AC')`
- `PURPLE_C` = `ManimColor('#9A72AC')`
- `PURPLE_D` = `ManimColor('#715582')`
- `PURPLE_D` = `ManimColor('#715582')`
- `PURPLE_E` = `ManimColor('#644172')`
- `PURPLE_E` = `ManimColor('#644172')`
- `PURPLISH` = `ManimColor('#94568C')`
- `PURPLISHBLUE` = `ManimColor('#601EF9')`
- `PURPLISHBROWN` = `ManimColor('#6B4247')`
- `PURPLISHGREY` = `ManimColor('#7A687F')`
- `PURPLISHPINK` = `ManimColor('#CE5DAE')`
- `PURPLISHRED` = `ManimColor('#B0054B')`
- `PURPLY` = `ManimColor('#983FB2')`
- `PURPLYBLUE` = `ManimColor('#661AEE')`
- `PURPLYPINK` = `ManimColor('#F075E6')`
- `PUTTY` = `ManimColor('#BEAE8A')`
- `R11_INTERNATIONAL_ORANGE` = `ManimColor('#CE482A')`
- `R12_SCARLET` = `ManimColor('#CD392A')`
- `R13_SIGNAL_RED` = `ManimColor('#BA312B')`
- `R14_WARATAH` = `ManimColor('#AA2429')`
- `R15_CRIMSON` = `ManimColor('#9E2429')`
- `R21_TANGERINE` = `ManimColor('#E96957')`
- `R22_HOMEBUSH_RED` = `ManimColor('#D83A2D')`
- `R23_LOLLIPOP` = `ManimColor('#CC5058')`
- `R24_STRAWBERRY` = `ManimColor('#B4292A')`
- `R25_ROSE_PINK` = `ManimColor('#E8919C')`
- `R32_APPLE_BLOSSOM` = `ManimColor('#F2E1D8')`
- `R33_GHOST_GUM` = `ManimColor('#E8DAD4')`
- `R34_MUSHROOM` = `ManimColor('#D7C0B6')`
- `R35_DEEP_ROSE` = `ManimColor('#CD6D71')`
- `R41_SHELL_PINK` = `ManimColor('#F9D9BB')`
- `R42_SALMON_PINK` = `ManimColor('#D99679')`
- `R43_RED_DUST` = `ManimColor('#D0674F')`
- `R44_POSSUM` = `ManimColor('#A18881')`
- `R45_RUBY` = `ManimColor('#8F3E5C')`
- `R51_BURNT_PINK` = `ManimColor('#E19B8E')`
- `R52_TERRACOTTA` = `ManimColor('#A04C36')`
- `R53_RED_GUM` = `ManimColor('#8D4338')`
- `R54_RASPBERRY` = `ManimColor('#852F31')`
- `R55_CLARET` = `ManimColor('#67292D')`
- `R62_VENETIAN_RED` = `ManimColor('#77372B')`
- `R63_RED_OXIDE` = `ManimColor('#663334')`
- `R64_DEEP_INDIAN_RED` = `ManimColor('#542E2B')`
- `R65_MAROON` = `ManimColor('#3F2B3C')`
- `RACINGGREEN` = `ManimColor('#014600')`
- `RADIOACTIVEGREEN` = `ManimColor('#2CFA1F')`
- `RAF_BLUE_GREY` = `ManimColor('#424C53')`
- `RAIL_BLUE` = `ManimColor('#1F4B61')`
- `RAIL_RED` = `ManimColor('#F24816')`
- `RASPBERRY` = `ManimColor('#B00149')`
- `RAWSIENNA` = `ManimColor('#974006')`
- `RAWSIENNA` = `ManimColor('#9A6200')`
- `RAWUMBER` = `ManimColor('#A75E09')`
- `REALLYLIGHTBLUE` = `ManimColor('#D4FFFF')`
- `RED` = `ManimColor('#FC6255')`
- `RED` = `ManimColor('#ED1B23')`
- `RED` = `ManimColor('#FF0000')`
- `RED` = `ManimColor('#E50000')`
- `RED` = `ManimColor('#FC6255')`
- `RED1` = `ManimColor('#FF0000')`
- `RED2` = `ManimColor('#EE0000')`
- `RED3` = `ManimColor('#CD0000')`
- `RED4` = `ManimColor('#8B0000')`
- `REDBROWN` = `ManimColor('#8B2E16')`
- `REDDISH` = `ManimColor('#C44240')`
- `REDDISHBROWN` = `ManimColor('#7F2B0A')`
- `REDDISHGREY` = `ManimColor('#997570')`
- `REDDISHORANGE` = `ManimColor('#F8481C')`
- `REDDISHPINK` = `ManimColor('#FE2C54')`
- `REDDISHPURPLE` = `ManimColor('#910951')`
- `REDDYBROWN` = `ManimColor('#6E1005')`
- `REDORANGE` = `ManimColor('#F26035')`
- `REDORANGE` = `ManimColor('#FD3C06')`
- `REDPINK` = `ManimColor('#FA2A55')`
- `REDPURPLE` = `ManimColor('#820747')`
- `REDVIOLET` = `ManimColor('#A1246B')`
- `REDVIOLET` = `ManimColor('#9E0168')`
- `REDWINE` = `ManimColor('#8C0034')`
- `RED_A` = `ManimColor('#F7A1A3')`
- `RED_A` = `ManimColor('#F7A1A3')`
- `RED_B` = `ManimColor('#FF8080')`
- `RED_B` = `ManimColor('#FF8080')`
- `RED_C` = `ManimColor('#FC6255')`
- `RED_C` = `ManimColor('#FC6255')`
- `RED_D` = `ManimColor('#E65A4C')`
- `RED_D` = `ManimColor('#E65A4C')`
- `RED_E` = `ManimColor('#CF5044')`
- `RED_E` = `ManimColor('#CF5044')`
- `RED_OXIDE` = `ManimColor('#774430')`
- `RHODAMINE` = `ManimColor('#EF559F')`
- `RICHBLUE` = `ManimColor('#021BF9')`
- `RICHPURPLE` = `ManimColor('#720058')`
- `ROBINEGGBLUE` = `ManimColor('#8AF1FE')`
- `ROBINSEGG` = `ManimColor('#6DEDFD')`
- `ROBINSEGGBLUE` = `ManimColor('#98EFF9')`
- `ROGUE` = `ManimColor('#AB1239')`
- `ROSA` = `ManimColor('#FE86A4')`
- `ROSE` = `ManimColor('#CF6275')`
- `ROSEPINK` = `ManimColor('#F7879A')`
- `ROSERED` = `ManimColor('#BE013C')`
- `ROSYBROWN` = `ManimColor('#BB8E8E')`
- `ROSYBROWN` = `ManimColor('#BC8F8F')`
- `ROSYBROWN1` = `ManimColor('#FFC1C1')`
- `ROSYBROWN2` = `ManimColor('#EEB4B4')`
- `ROSYBROWN3` = `ManimColor('#CD9B9B')`
- `ROSYBROWN4` = `ManimColor('#8B6969')`
- `ROSYPINK` = `ManimColor('#F6688E')`
- `ROUNDEL_BLUE` = `ManimColor('#2C3E75')`
- `ROYAL` = `ManimColor('#0C1793')`
- `ROYALBLUE` = `ManimColor('#0071BC')`
- `ROYALBLUE` = `ManimColor('#4168E1')`
- `ROYALBLUE` = `ManimColor('#4169E1')`
- `ROYALBLUE` = `ManimColor('#0504AA')`
- `ROYALBLUE1` = `ManimColor('#4876FF')`
- `ROYALBLUE2` = `ManimColor('#436EEE')`
- `ROYALBLUE3` = `ManimColor('#3A5FCD')`
- `ROYALBLUE4` = `ManimColor('#27408B')`
- `ROYALPURPLE` = `ManimColor('#613F99')`
- `ROYALPURPLE` = `ManimColor('#4B006E')`
- `ROYAL_BLUE` = `ManimColor('#2A283D')`
- `RUBINERED` = `ManimColor('#ED017D')`
- `RUBY` = `ManimColor('#982D57')`
- `RUBY` = `ManimColor('#CA0147')`
- `RUSSET` = `ManimColor('#A13905')`
- `RUST` = `ManimColor('#A83C09')`
- `RUSTBROWN` = `ManimColor('#8B3103')`
- `RUSTORANGE` = `ManimColor('#C45508')`
- `RUSTRED` = `ManimColor('#AA2704')`
- `RUSTYORANGE` = `ManimColor('#CD5909')`
- `RUSTYRED` = `ManimColor('#AF2F0D')`
- `SADDLEBROWN` = `ManimColor('#8A4413')`
- `SADDLEBROWN` = `ManimColor('#8B4513')`
- `SAFFRON` = `ManimColor('#FEB209')`
- `SAGE` = `ManimColor('#87AE73')`
- `SAGEGREEN` = `ManimColor('#88B378')`
- `SAGE_GREEN` = `ManimColor('#757639')`
- `SALMON` = `ManimColor('#C98A71')`
- `SALMON` = `ManimColor('#F69289')`
- `SALMON` = `ManimColor('#F97F72')`
- `SALMON` = `ManimColor('#FA8072')`
- `SALMON` = `ManimColor('#FF796C')`
- `SALMON1` = `ManimColor('#FF8C69')`
- `SALMON2` = `ManimColor('#EE8262')`
- `SALMON3` = `ManimColor('#CD7054')`
- `SALMON4` = `ManimColor('#8B4C39')`
- `SALMONPINK` = `ManimColor('#FE7B7C')`
- `SALMON_PINK` = `ManimColor('#F3B28B')`
- `SAND` = `ManimColor('#E2CA76')`
- `SANDBROWN` = `ManimColor('#CBA560')`
- `SANDSTONE` = `ManimColor('#C9AE74')`
- `SANDY` = `ManimColor('#F1DA7A')`
- `SANDYBROWN` = `ManimColor('#F3A45F')`
- `SANDYBROWN` = `ManimColor('#F4A460')`
- `SANDYBROWN` = `ManimColor('#C4A661')`
- `SANDYELLOW` = `ManimColor('#FCE166')`
- `SANDYYELLOW` = `ManimColor('#FDEE73')`
- `SAPGREEN` = `ManimColor('#5C8B15')`
- `SAPPHIRE` = `ManimColor('#2138AB')`
- `SCARLET` = `ManimColor('#BE0119')`
- `SEA` = `ManimColor('#3C9992')`
- `SEABLUE` = `ManimColor('#047495')`
- `SEAFOAM` = `ManimColor('#80F9AD')`
- `SEAFOAMBLUE` = `ManimColor('#78D1B6')`
- `SEAFOAMGREEN` = `ManimColor('#7AF9AB')`
- `SEAGREEN` = `ManimColor('#3FBC9D')`
- `SEAGREEN` = `ManimColor('#2D8A56')`
- `SEAGREEN` = `ManimColor('#53FCA1')`
- `SEAGREEN1` = `ManimColor('#54FF9F')`
- `SEAGREEN2` = `ManimColor('#4EEE94')`
- `SEAGREEN3` = `ManimColor('#43CD80')`
- `SEAGREEN4` = `ManimColor('#2E8B57')`
- `SEASHELL` = `ManimColor('#FFF4ED')`
- `SEASHELL1` = `ManimColor('#FFF5EE')`
- `SEASHELL2` = `ManimColor('#EEE5DE')`
- `SEASHELL3` = `ManimColor('#CDC5BF')`
- `SEASHELL4` = `ManimColor('#8B8682')`
- `SEAWEED` = `ManimColor('#18D17B')`
- `SEAWEEDGREEN` = `ManimColor('#35AD6B')`
- `SEA_GREEN` = `ManimColor('#96BF65')`
- `SEPIA` = `ManimColor('#671800')`
- `SEPIA` = `ManimColor('#985E2B')`
- `SERVICE_BROWN` = `ManimColor('#59493E')`
- `SHAMROCK` = `ManimColor('#01B44C')`
- `SHAMROCKGREEN` = `ManimColor('#02C14D')`
- `SHELL_PINK` = `ManimColor('#FBDED6')`
- `SHIT` = `ManimColor('#7F5F00')`
- `SHITBROWN` = `ManimColor('#7B5804')`
- `SHITGREEN` = `ManimColor('#758000')`
- `SHOCKINGPINK` = `ManimColor('#FE02A2')`
- `SICKGREEN` = `ManimColor('#9DB92C')`
- `SICKLYGREEN` = `ManimColor('#94B21C')`
- `SICKLYYELLOW` = `ManimColor('#D0E429')`
- `SIENNA` = `ManimColor('#A0512C')`
- `SIENNA` = `ManimColor('#A0522D')`
- `SIENNA` = `ManimColor('#A9561E')`
- `SIENNA1` = `ManimColor('#FF8247')`
- `SIENNA2` = `ManimColor('#EE7942')`
- `SIENNA3` = `ManimColor('#CD6839')`
- `SIENNA4` = `ManimColor('#8B4726')`
- `SIGNAL_RED` = `ManimColor('#DD3420')`
- `SILVER` = `ManimColor('#BFBFBF')`
- `SILVER` = `ManimColor('#C5C9C7')`
- `SILVER_GREY` = `ManimColor('#9D9D7E')`
- `SKY` = `ManimColor('#BBC9A5')`
- `SKY` = `ManimColor('#82CAFC')`
- `SKYBLUE` = `ManimColor('#46C5DD')`
- `SKYBLUE` = `ManimColor('#87CEEA')`
- `SKYBLUE` = `ManimColor('#87CEEB')`
- `SKYBLUE` = `ManimColor('#75BBFD')`
- `SKYBLUE1` = `ManimColor('#87CEFF')`
- `SKYBLUE2` = `ManimColor('#7EC0EE')`
- `SKYBLUE3` = `ManimColor('#6CA6CD')`
- `SKYBLUE4` = `ManimColor('#4A708B')`
- `SKY_BLUE` = `ManimColor('#94BFAC')`
- `SLATE` = `ManimColor('#6F7264')`
- `SLATE` = `ManimColor('#516572')`
- `SLATEBLUE` = `ManimColor('#6959CD')`
- `SLATEBLUE` = `ManimColor('#6A5ACD')`
- `SLATEBLUE` = `ManimColor('#5B7C99')`
- `SLATEBLUE1` = `ManimColor('#836FFF')`
- `SLATEBLUE2` = `ManimColor('#7A67EE')`
- `SLATEBLUE3` = `ManimColor('#6959CD')`
- `SLATEBLUE4` = `ManimColor('#473C8B')`
- `SLATEGRAY` = `ManimColor('#707F90')`
- `SLATEGRAY` = `ManimColor('#708090')`
- `SLATEGRAY1` = `ManimColor('#C6E2FF')`
- `SLATEGRAY2` = `ManimColor('#B9D3EE')`
- `SLATEGRAY3` = `ManimColor('#9FB6CD')`
- `SLATEGRAY4` = `ManimColor('#6C7B8B')`
- `SLATEGREEN` = `ManimColor('#658D6D')`
- `SLATEGREY` = `ManimColor('#707F90')`
- `SLATEGREY` = `ManimColor('#59656D')`
- `SLIMEGREEN` = `ManimColor('#99CC04')`
- `SMOKE_GREY` = `ManimColor('#7B93A3')`
- `SNOT` = `ManimColor('#ACBB0D')`
- `SNOTGREEN` = `ManimColor('#9DC100')`
- `SNOW` = `ManimColor('#FFF9F9')`
- `SNOW1` = `ManimColor('#FFFAFA')`
- `SNOW2` = `ManimColor('#EEE9E9')`
- `SNOW3` = `ManimColor('#CDC9C9')`
- `SNOW4` = `ManimColor('#8B8989')`
- `SOFTBLUE` = `ManimColor('#6488EA')`
- `SOFTGREEN` = `ManimColor('#6FC276')`
- `SOFTPINK` = `ManimColor('#FDB0C0')`
- `SOFTPURPLE` = `ManimColor('#A66FB5')`
- `SPEARMINT` = `ManimColor('#1EF876')`
- `SPRINGGREEN` = `ManimColor('#C6DC67')`
- `SPRINGGREEN` = `ManimColor('#00FF7E')`
- `SPRINGGREEN` = `ManimColor('#A9F971')`
- `SPRINGGREEN1` = `ManimColor('#00FF7F')`
- `SPRINGGREEN2` = `ManimColor('#00EE76')`
- `SPRINGGREEN3` = `ManimColor('#00CD66')`
- `SPRINGGREEN4` = `ManimColor('#008B45')`
- `SPRUCE` = `ManimColor('#0A5F38')`
- `SPRUCE_GREEN` = `ManimColor('#6B6F5A')`
- `SQUASH` = `ManimColor('#F2AB15')`
- `STEEL` = `ManimColor('#738595')`
- `STEELBLUE` = `ManimColor('#4682B3')`
- `STEELBLUE` = `ManimColor('#4682B4')`
- `STEELBLUE` = `ManimColor('#5A7D9A')`
- `STEELBLUE1` = `ManimColor('#63B8FF')`
- `STEELBLUE2` = `ManimColor('#5CACEE')`
- `STEELBLUE3` = `ManimColor('#4F94CD')`
- `STEELBLUE4` = `ManimColor('#36648B')`
- `STEELGREY` = `ManimColor('#6F828A')`
- `STEEL_FURNITURE_GREEN` = `ManimColor('#3B3629')`
- `STONE` = `ManimColor('#ADA587')`
- `STORMYBLUE` = `ManimColor('#507B9C')`
- `STRAW` = `ManimColor('#FCF679')`
- `STRAWBERRY` = `ManimColor('#FB2943')`
- `STRONGBLUE` = `ManimColor('#0C06F7')`
- `STRONGPINK` = `ManimColor('#FF0789')`
- `STRONG_BLUE` = `ManimColor('#3A73A9')`
- `SUNFLOWER` = `ManimColor('#FFC512')`
- `SUNFLOWERYELLOW` = `ManimColor('#FFDA03')`
- `SUNNYYELLOW` = `ManimColor('#FFF917')`
- `SUNRISE` = `ManimColor('#CFB48A')`
- `SUNSHINE` = `ManimColor('#CFB48A')`
- `SUNSHINEYELLOW` = `ManimColor('#FFFD37')`
- `SUNYELLOW` = `ManimColor('#FFDF22')`
- `SWAMP` = `ManimColor('#698339')`
- `SWAMPGREEN` = `ManimColor('#748500')`
- `T11_TROPICAL_BLUE` = `ManimColor('#006698')`
- `T12_DIAMANTIA` = `ManimColor('#006C74')`
- `T14_MALACHITE` = `ManimColor('#105154')`
- `T15_TURQUOISE` = `ManimColor('#098587')`
- `T22_ORIENTAL_BLUE` = `ManimColor('#358792')`
- `T24_BLUE_JADE` = `ManimColor('#427F7E')`
- `T32_HUON_GREEN` = `ManimColor('#72B3B1')`
- `T33_SMOKE_BLUE` = `ManimColor('#9EB6B2')`
- `T35_GREEN_ICE` = `ManimColor('#78AEA2')`
- `T44_BLUE_GUM` = `ManimColor('#6A8A88')`
- `T45_COOTAMUNDRA` = `ManimColor('#759E91')`
- `T51_MOUNTAIN_BLUE` = `ManimColor('#295668')`
- `T53_PEACOCK_BLUE` = `ManimColor('#245764')`
- `T63_TEAL` = `ManimColor('#183F4E')`
- `TAN` = `ManimColor('#DA9D76')`
- `TAN` = `ManimColor('#D2B38C')`
- `TAN` = `ManimColor('#D2B48C')`
- `TAN` = `ManimColor('#D1B26F')`
- `TAN1` = `ManimColor('#FFA54F')`
- `TAN2` = `ManimColor('#EE9A49')`
- `TAN3` = `ManimColor('#CD853F')`
- `TAN4` = `ManimColor('#8B5A2B')`
- `TANBROWN` = `ManimColor('#AB7E4C')`
- `TANGERINE` = `ManimColor('#FF9408')`
- `TANGREEN` = `ManimColor('#A9BE70')`
- `TAUPE` = `ManimColor('#B9A281')`
- `TEA` = `ManimColor('#65AB7C')`
- `TEAGREEN` = `ManimColor('#BDF8A3')`
- `TEAL` = `ManimColor('#5CD0B3')`
- `TEAL` = `ManimColor('#007F7F')`
- `TEAL` = `ManimColor('#029386')`
- `TEAL` = `ManimColor('#5CD0B3')`
- `TEALBLUE` = `ManimColor('#00AEB3')`
- `TEALBLUE` = `ManimColor('#01889F')`
- `TEALGREEN` = `ManimColor('#25A36F')`
- `TEALISH` = `ManimColor('#24BCA8')`
- `TEALISHGREEN` = `ManimColor('#0CDC73')`
- `TEAL_A` = `ManimColor('#ACEAD7')`
- `TEAL_A` = `ManimColor('#ACEAD7')`
- `TEAL_B` = `ManimColor('#76DDC0')`
- `TEAL_B` = `ManimColor('#76DDC0')`
- `TEAL_C` = `ManimColor('#5CD0B3')`
- `TEAL_C` = `ManimColor('#5CD0B3')`
- `TEAL_D` = `ManimColor('#55C1A7')`
- `TEAL_D` = `ManimColor('#55C1A7')`
- `TEAL_E` = `ManimColor('#49A88F')`
- `TEAL_E` = `ManimColor('#49A88F')`
- `TERRACOTA` = `ManimColor('#CB6843')`
- `TERRACOTTA` = `ManimColor('#A65341')`
- `TERRACOTTA` = `ManimColor('#C9643B')`
- `THISTLE` = `ManimColor('#D883B7')`
- `THISTLE` = `ManimColor('#D8BFD8')`
- `THISTLE` = `ManimColor('#D8BFD8')`
- `THISTLE1` = `ManimColor('#FFE1FF')`
- `THISTLE2` = `ManimColor('#EED2EE')`
- `THISTLE3` = `ManimColor('#CDB5CD')`
- `THISTLE4` = `ManimColor('#8B7B8B')`
- `TIFFANYBLUE` = `ManimColor('#7BF2DA')`
- `TOMATO` = `ManimColor('#FF6347')`
- `TOMATO` = `ManimColor('#EF4026')`
- `TOMATO1` = `ManimColor('#FF6347')`
- `TOMATO2` = `ManimColor('#EE5C42')`
- `TOMATO3` = `ManimColor('#CD4F39')`
- `TOMATO4` = `ManimColor('#8B3626')`
- `TOMATORED` = `ManimColor('#EC2D01')`
- `TOPAZ` = `ManimColor('#13BBAF')`
- `TOUPE` = `ManimColor('#C7AC7D')`
- `TOXICGREEN` = `ManimColor('#61DE2A')`
- `TRAFFIC_BLUE` = `ManimColor('#135B75')`
- `TRAFFIC_GREEN` = `ManimColor('#476A4C')`
- `TRAFFIC_RED` = `ManimColor('#A83C19')`
- `TRAFFIC_YELLOW` = `ManimColor('#DD7B00')`
- `TREEGREEN` = `ManimColor('#2A7E19')`
- `TRUEBLUE` = `ManimColor('#010FCC')`
- `TRUEGREEN` = `ManimColor('#089404')`
- `TURQUOISE` = `ManimColor('#00B4CE')`
- `TURQUOISE` = `ManimColor('#3FE0CF')`
- `TURQUOISE` = `ManimColor('#40E0D0')`
- `TURQUOISE` = `ManimColor('#06C2AC')`
- `TURQUOISE1` = `ManimColor('#00F5FF')`
- `TURQUOISE2` = `ManimColor('#00E5EE')`
- `TURQUOISE3` = `ManimColor('#00C5CD')`
- `TURQUOISE4` = `ManimColor('#00868B')`
- `TURQUOISEBLUE` = `ManimColor('#06B1C4')`
- `TURQUOISEGREEN` = `ManimColor('#04F489')`
- `TURQUOISE_BLUE` = `ManimColor('#5B9291')`
- `TURTLEGREEN` = `ManimColor('#75B84F')`
- `TWILIGHT` = `ManimColor('#4E518B')`
- `TWILIGHTBLUE` = `ManimColor('#0A437A')`
- `UGLYBLUE` = `ManimColor('#31668A')`
- `UGLYBROWN` = `ManimColor('#7D7103')`
- `UGLYGREEN` = `ManimColor('#7A9703')`
- `UGLYPINK` = `ManimColor('#CD7584')`
- `UGLYPURPLE` = `ManimColor('#A442A0')`
- `UGLYYELLOW` = `ManimColor('#D0C101')`
- `ULTRAMARINE` = `ManimColor('#2000B1')`
- `ULTRAMARINEBLUE` = `ManimColor('#1805DB')`
- `UMBER` = `ManimColor('#B26400')`
- `VELLUM` = `ManimColor('#F4F0BD')`
- `VELVET` = `ManimColor('#750851')`
- `VENETIAN_RED` = `ManimColor('#83422B')`
- `VERDIGRIS_GREEN` = `ManimColor('#68AB77')`
- `VERMILION` = `ManimColor('#F4320C')`
- `VERYDARKBLUE` = `ManimColor('#000133')`
- `VERYDARKBROWN` = `ManimColor('#1D0200')`
- `VERYDARKGREEN` = `ManimColor('#062E03')`
- `VERYDARKPURPLE` = `ManimColor('#2A0134')`
- `VERYLIGHTBLUE` = `ManimColor('#D5FFFF')`
- `VERYLIGHTBROWN` = `ManimColor('#D3B683')`
- `VERYLIGHTGREEN` = `ManimColor('#D1FFBD')`
- `VERYLIGHTPINK` = `ManimColor('#FFF4F2')`
- `VERYLIGHTPURPLE` = `ManimColor('#F6CEFC')`
- `VERYPALEBLUE` = `ManimColor('#D6FFFE')`
- `VERYPALEGREEN` = `ManimColor('#CFFDBC')`
- `VERY_DARK_DRAB` = `ManimColor('#4C4A3C')`
- `VIBRANTBLUE` = `ManimColor('#0339F8')`
- `VIBRANTGREEN` = `ManimColor('#0ADD08')`
- `VIBRANTPURPLE` = `ManimColor('#AD03DE')`
- `VIOLET` = `ManimColor('#58429B')`
- `VIOLET` = `ManimColor('#ED82ED')`
- `VIOLET` = `ManimColor('#EE82EE')`
- `VIOLET` = `ManimColor('#9A0EEA')`
- `VIOLETBLUE` = `ManimColor('#510AC9')`
- `VIOLETPINK` = `ManimColor('#FB5FFC')`
- `VIOLETRED` = `ManimColor('#EF58A0')`
- `VIOLETRED` = `ManimColor('#D01F90')`
- `VIOLETRED` = `ManimColor('#D02090')`
- `VIOLETRED` = `ManimColor('#A50055')`
- `VIOLETRED1` = `ManimColor('#FF3E96')`
- `VIOLETRED2` = `ManimColor('#EE3A8C')`
- `VIOLETRED3` = `ManimColor('#CD3278')`
- `VIOLETRED4` = `ManimColor('#8B2252')`
- `VIRIDIAN` = `ManimColor('#1E9167')`
- `VIVIDBLUE` = `ManimColor('#152EFF')`
- `VIVIDGREEN` = `ManimColor('#2FEF10')`
- `VIVIDPURPLE` = `ManimColor('#9900FA')`
- `VOMIT` = `ManimColor('#A2A415')`
- `VOMITGREEN` = `ManimColor('#89A203')`
- `VOMITYELLOW` = `ManimColor('#C7C10C')`
- `WARMBLUE` = `ManimColor('#4B57DB')`
- `WARMBROWN` = `ManimColor('#964E02')`
- `WARMGREY` = `ManimColor('#978A84')`
- `WARMPINK` = `ManimColor('#FB5581')`
- `WARMPURPLE` = `ManimColor('#952E8F')`
- `WASHEDOUTGREEN` = `ManimColor('#BCF5A6')`
- `WATERBLUE` = `ManimColor('#0E87CC')`
- `WATERMELON` = `ManimColor('#FD4659')`
- `WEIRDGREEN` = `ManimColor('#3AE57F')`
- `WHEAT` = `ManimColor('#F4DDB2')`
- `WHEAT` = `ManimColor('#F5DEB3')`
- `WHEAT` = `ManimColor('#FBDD7E')`
- `WHEAT1` = `ManimColor('#FFE7BA')`
- `WHEAT2` = `ManimColor('#EED8AE')`
- `WHEAT3` = `ManimColor('#CDBA96')`
- `WHEAT4` = `ManimColor('#8B7E66')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITE` = `ManimColor('#FFFFFF')`
- `WHITESMOKE` = `ManimColor('#F4F4F4')`
- `WHITESMOKE` = `ManimColor('#F5F5F5')`
- `WILDSTRAWBERRY` = `ManimColor('#EE2967')`
- `WINDOWSBLUE` = `ManimColor('#3778BF')`
- `WINE` = `ManimColor('#80013F')`
- `WINERED` = `ManimColor('#7B0323')`
- `WINTERGREEN` = `ManimColor('#20F986')`
- `WISTERIA` = `ManimColor('#A87DC2')`
- `X11_BUTTERSCOTCH` = `ManimColor('#D38F43')`
- `X12_PUMPKIN` = `ManimColor('#DD7E1A')`
- `X13_MARIGOLD` = `ManimColor('#ED7F15')`
- `X14_MANDARIN` = `ManimColor('#E45427')`
- `X15_ORANGE` = `ManimColor('#E36C2B')`
- `X21_PALE_OCHRE` = `ManimColor('#DAA45F')`
- `X22_SAFFRON` = `ManimColor('#F6AA51')`
- `X23_APRICOT` = `ManimColor('#FEB56D')`
- `X24_ROCKMELON` = `ManimColor('#F6894B')`
- `X31_RAFFIA` = `ManimColor('#EBC695')`
- `X32_MAGNOLIA` = `ManimColor('#F1DEBE')`
- `X33_WARM_WHITE` = `ManimColor('#F3E7D4')`
- `X34_DRIFTWOOD` = `ManimColor('#D5C4AE')`
- `X41_BUFF` = `ManimColor('#C28A44')`
- `X42_BISCUIT` = `ManimColor('#DEBA92')`
- `X43_BEIGE` = `ManimColor('#C9AA8C')`
- `X45_CINNAMON` = `ManimColor('#AC826D')`
- `X51_TAN` = `ManimColor('#8F5F32')`
- `X52_COFFEE` = `ManimColor('#AD7948')`
- `X53_GOLDEN_TAN` = `ManimColor('#925629')`
- `X54_BROWN` = `ManimColor('#68452C')`
- `X55_NUT_BROWN` = `ManimColor('#764832')`
- `X61_WOMBAT` = `ManimColor('#6E5D52')`
- `X62_DARK_EARTH` = `ManimColor('#6E5D52')`
- `X63_IRONBARK` = `ManimColor('#443B36')`
- `X64_CHOCOLATE` = `ManimColor('#4A3B31')`
- `X65_DARK_BROWN` = `ManimColor('#4F372D')`
- `Y11_CANARY` = `ManimColor('#E7BD11')`
- `Y12_WATTLE` = `ManimColor('#E8AF01')`
- `Y13_VIVID_YELLOW` = `ManimColor('#FCAE01')`
- `Y14_GOLDEN_YELLOW` = `ManimColor('#F5A601')`
- `Y15_SUNFLOWER` = `ManimColor('#FFA709')`
- `Y16_INCA_GOLD` = `ManimColor('#DF8C19')`
- `Y21_PRIMROSE` = `ManimColor('#F5CF5B')`
- `Y22_CUSTARD` = `ManimColor('#EFD25C')`
- `Y23_BUTTERCUP` = `ManimColor('#E0CD41')`
- `Y24_STRAW` = `ManimColor('#E3C882')`
- `Y25_DEEP_CREAM` = `ManimColor('#F3C968')`
- `Y26_HOMEBUSH_GOLD` = `ManimColor('#FCC51A')`
- `Y31_LILY_GREEN` = `ManimColor('#E3E3CD')`
- `Y32_FLUMMERY` = `ManimColor('#E6DF9E')`
- `Y33_PALE_PRIMROSE` = `ManimColor('#F5F3CE')`
- `Y34_CREAM` = `ManimColor('#EFE3BE')`
- `Y35_OFF_WHITE` = `ManimColor('#F1E9D5')`
- `Y41_OLIVE_YELLOW` = `ManimColor('#8E7426')`
- `Y42_MUSTARD` = `ManimColor('#C4A32E')`
- `Y43_PARCHMENT` = `ManimColor('#D4C9A3')`
- `Y44_SAND` = `ManimColor('#DCC18B')`
- `Y45_MANILLA` = `ManimColor('#E5D0A7')`
- `Y51_BRONZE_OLIVE` = `ManimColor('#695D3E')`
- `Y52_CHAMOIS` = `ManimColor('#BEA873')`
- `Y53_SANDSTONE` = `ManimColor('#D5BF8E')`
- `Y54_OATMEAL` = `ManimColor('#CAAE82')`
- `Y55_DEEP_STONE` = `ManimColor('#BC9969')`
- `Y56_MERINO` = `ManimColor('#C9B79E')`
- `Y61_BLACK_OLIVE` = `ManimColor('#47473B')`
- `Y62_SUGAR_CANE` = `ManimColor('#BCA55C')`
- `Y63_KHAKI` = `ManimColor('#826843')`
- `Y65_MUSHROOM` = `ManimColor('#A39281')`
- `Y66_MUDSTONE` = `ManimColor('#574E45')`
- `YELLOW` = `ManimColor('#F7D96F')`
- `YELLOW` = `ManimColor('#FFF200')`
- `YELLOW` = `ManimColor('#FFFF00')`
- `YELLOW` = `ManimColor('#FFFF14')`
- `YELLOW` = `ManimColor('#F7D96F')`
- `YELLOW1` = `ManimColor('#FFFF00')`
- `YELLOW2` = `ManimColor('#EEEE00')`
- `YELLOW3` = `ManimColor('#CDCD00')`
- `YELLOW4` = `ManimColor('#8B8B00')`
- `YELLOWBROWN` = `ManimColor('#B79400')`
- `YELLOWGREEN` = `ManimColor('#98CC70')`
- `YELLOWGREEN` = `ManimColor('#9ACD30')`
- `YELLOWGREEN` = `ManimColor('#9ACD32')`
- `YELLOWGREEN` = `ManimColor('#BBF90F')`
- `YELLOWISH` = `ManimColor('#FAEE66')`
- `YELLOWISHBROWN` = `ManimColor('#9B7A01')`
- `YELLOWISHGREEN` = `ManimColor('#B0DD16')`
- `YELLOWISHORANGE` = `ManimColor('#FFAB0F')`
- `YELLOWISHTAN` = `ManimColor('#FCFC81')`
- `YELLOWOCHRE` = `ManimColor('#CB9D06')`
- `YELLOWORANGE` = `ManimColor('#FAA21A')`
- `YELLOWORANGE` = `ManimColor('#FCB001')`
- `YELLOWTAN` = `ManimColor('#FFE36E')`
- `YELLOWYBROWN` = `ManimColor('#AE8B0C')`
- `YELLOWYGREEN` = `ManimColor('#BFF128')`
- `YELLOW_A` = `ManimColor('#FFF1B6')`
- `YELLOW_A` = `ManimColor('#FFF1B6')`
- `YELLOW_B` = `ManimColor('#FFEA94')`
- `YELLOW_B` = `ManimColor('#FFEA94')`
- `YELLOW_C` = `ManimColor('#F7D96F')`
- `YELLOW_C` = `ManimColor('#F7D96F')`
- `YELLOW_D` = `ManimColor('#F4D345')`
- `YELLOW_D` = `ManimColor('#F4D345')`
- `YELLOW_E` = `ManimColor('#E8C11C')`
- `YELLOW_E` = `ManimColor('#E8C11C')`
- **`average_color(*colors: 'ParsableManimColor') -> 'ManimColor'`** — Determine the average color between the given parameters.
- **`color_gradient(reference_colors: 'Iterable[ParsableManimColor]', length_of_output: 'int') -> 'list[ManimColor]'`** — Create a list of colors interpolated between the input array of colors with a
- **`color_to_int_rgb(color: 'ParsableManimColor') -> 'IntRGB'`** — Helper function for use in functional style programming. Refer to
- **`color_to_int_rgba(color: 'ParsableManimColor', alpha: 'float' = 1.0) -> 'IntRGBA'`** — Helper function for use in functional style programming. Refer to
- **`color_to_rgb(color: 'ParsableManimColor') -> 'FloatRGB'`** — Helper function for use in functional style programming.
- **`color_to_rgba(color: 'ParsableManimColor', alpha: 'float' = 1.0) -> 'FloatRGBA'`** — Helper function for use in functional style programming. Refer to
- **`get_shaded_rgb(rgb: 'FloatRGB', point: 'Point3D', unit_normal_vect: 'Vector3D', light_source: 'Point3D') -> 'FloatRGB'`** — Add light or shadow to the ``rgb`` color of some surface which is located at a
- **`hex_to_rgb(hex_code: 'str') -> 'FloatRGB'`** — Helper function for use in functional style programming. Refer to
- **`interpolate_color(color1: 'ManimColorT', color2: 'ManimColorT', alpha: 'float') -> 'ManimColorT'`** — Standalone function to interpolate two ManimColors and get the result. Refer to
- **`invert_color(color: 'ManimColorT') -> 'ManimColorT'`** — Helper function for use in functional style programming. Refer to
- **`random_bright_color() -> 'ManimColor'`** — Return a random bright color: a random color averaged with ``WHITE``.
- **`random_color() -> 'ManimColor'`** — Return a random :class:`ManimColor`.
- **`rgb_to_color(rgb: 'FloatRGBLike | IntRGBLike') -> 'ManimColor'`** — Helper function for use in functional style programming. Refer to
- **`rgb_to_hex(rgb: 'FloatRGBLike | IntRGBLike') -> 'str'`** — Helper function for use in functional style programming. Refer to
- **`rgba_to_color(rgba: 'FloatRGBALike | IntRGBALike') -> 'ManimColor'`** — Helper function for use in functional style programming. Refer to

## utils/other

### `Cell(c: 'Point2DLike', h: 'float', polygon: 'Polygon') -> 'None'`
> A square in a mesh covering the :class:`~.Polygon` passed as an argument.

<details><summary>métodos próprios (1) · herdados: 0</summary>

- `__init__(self, c: 'Point2DLike', h: 'float', polygon: 'Polygon') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Comparable(*args, **kwargs)` ← Protocol
> Base class for protocol classes.

<details><summary>métodos próprios (1) · herdados: 0</summary>

- `__init__(self, *args, **kwargs)`

</details>

### `DictAsObject(dictin: 'dict[str, Any]')`

<details><summary>métodos próprios (1) · herdados: 0</summary>

- `__init__(self, dictin: 'dict[str, Any]')` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `DummySceneFileWriter(renderer: 'CairoRenderer | OpenGLRenderer', scene_name: 'str', **kwargs: 'Any') -> 'None'` ← SceneFileWriter
> Delegate of SceneFileWriter used to test the frames.

<details><summary>métodos próprios (9) · herdados: 19</summary>

- `__init__(self, renderer: 'CairoRenderer | OpenGLRenderer', scene_name: 'str', **kwargs: 'Any') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `add_partial_movie_file(self, hash_animation: 'str | None') -> 'None'` — Adds a new partial movie file path to ``scene.partial_movie_files``
- `begin_animation(self, allow_write: 'bool' = True, file_path: 'StrPath | None' = None) -> 'Any'` — Used internally by manim to stream the animation to FFMPEG for
- `clean_cache(self) -> 'None'` — Will clean the cache by removing the oldest partial_movie_files.
- `combine_to_movie(self) -> 'None'` — Used internally by Manim to combine the separate
- `combine_to_section_videos(self) -> 'None'` — Concatenate partial movie files for each section.
- `end_animation(self, allow_write: 'bool' = False) -> 'None'` — Internally used by Manim to stop streaming to FFMPEG gracefully.
- `init_output_directories(self, scene_name: 'str') -> 'None'` — Initialise output directories.
- `write_frame(self, frame_or_renderer: 'PixelArray | OpenGLRenderer', num_frames: 'int' = 1) -> 'None'` — Used internally by Manim to write a frame to the FFMPEG input buffer.

</details>

### `EndSceneEarlyException()` ← Exception
> Common base class for all non-exit exceptions.

### `Facet(coordinates: 'PointND_Array', internal: 'PointND') -> 'None'`

<details><summary>métodos próprios (2) · herdados: 0</summary>

- `__init__(self, coordinates: 'PointND_Array', internal: 'PointND') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `compute_normal(self, internal: 'PointND') -> 'PointND'`

</details>

### `Horizon() -> 'None'`

<details><summary>métodos próprios (1) · herdados: 0</summary>

- `__init__(self) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `MultiAnimationOverrideException()` ← Exception
> Common base class for all non-exit exceptions.

### `Percent(axis: 'Vector3D') -> 'None'`

<details><summary>métodos próprios (1) · herdados: 0</summary>

- `__init__(self, axis: 'Vector3D') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `Polygon(rings: 'Sequence[Point2DLike_Array]') -> 'None'`
> Initializes the Polygon with the given rings.

<details><summary>métodos próprios (3) · herdados: 0</summary>

- `__init__(self, rings: 'Sequence[Point2DLike_Array]') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `compute_distance(self, point: 'Point2DLike') -> 'float'` — Compute the minimum distance from a point to the polygon.
- `inside(self, point: 'Point2DLike') -> 'bool'` — Check if a point is inside the polygon.

</details>

### `QuickHull(tolerance: 'float' = 1e-05) -> 'None'`
> QuickHull algorithm for constructing a convex hull from a set of points.

<details><summary>métodos próprios (5) · herdados: 0</summary>

- `__init__(self, tolerance: 'float' = 1e-05) -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.
- `build(self, points: 'PointND_Array') -> 'None'`
- `classify(self, facet: 'Facet') -> 'None'`
- `compute_horizon(self, eye: 'PointND', start_facet: 'Facet') -> 'Horizon'`
- `initialize(self, points: 'PointND_Array') -> 'None'`

</details>

### `QuickHullPoint(coordinates: 'PointND_Array') -> 'None'`

<details><summary>métodos próprios (1) · herdados: 0</summary>

- `__init__(self, coordinates: 'PointND_Array') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `RerunSceneException()` ← Exception
> Common base class for all non-exit exceptions.

### `SubFacet(coordinates: 'PointND_Array') -> 'None'`

<details><summary>métodos próprios (1) · herdados: 0</summary>

- `__init__(self, coordinates: 'PointND_Array') -> 'None'` — Initialize self.  See help(type(self)) for accurate signature.

</details>

### `VideoMetadata()` ← dict
> dict() -> new empty dictionary

- `ALIAS_DOCS_DICT` = `{}`
- `BLACK` = `ManimColor('#000000')`
- `CHOOSE_NUMBER_MESSAGE` = `'\nChoose number corresponding to desired scene/arguments.\n(Use comma separated list for multiple entries or use "*"...`
- `DATA_DICT` = `{}`
- `F` = `~F`
- `FRAME_ABSOLUTE_TOLERANCE` = `1.01`
- `FRAME_MISMATCH_RATIO_TOLERANCE` = `1e-05`
- `H` = `~H`
- `INVALID_NUMBER_MESSAGE` = `'Invalid scene numbers have been specified. Aborting.'`
- `KEYS_TO_FILTER_OUT` = `{'original_id', 'background', 'pixel_array', 'pixel_array_to_cairo_context'}`
- `MANIM_ROOT` = `PosixPath('<site-packages>/manim')`
- `NO_SCENE_MESSAGE` = `'\n   There are no scenes inside that module\n'`
- `OUT` = `array([0., 0., 1.])`
- `SCENE_NOT_FOUND_MESSAGE` = `'\n   {} is not in the script\n'`
- `STRAIGHT_PATH_THRESHOLD` = `0.01`
- `T` = `~T`
- `T` = `~T`
- `T` = `~T`
- `TYPEVAR_DICT` = `{}`
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
- `TYPST_COMPILATION_FONT_SIZE` = `10`
- `TYPST_TEMPLATE` = `'#set page(width: auto, height: auto, margin: 0pt, fill: none)\n#set text(size: {text_size}pt)\n{preamble}\n{body}\n'`
- `U` = `~U`
- **`add_extension_if_not_present(file_name: 'Path', extension: 'str') -> 'Path'`**
- **`add_import_statement(file: 'Path') -> 'None'`** — Prepends an import statement in a file
- **`add_version_before_extension(file_name: 'Path') -> 'Path'`**
- **`adjacent_n_tuples(objects: 'Sequence[T]', n: 'int') -> 'zip[tuple[T, ...]]'`** — Returns the Sequence objects cyclically split into n length tuples.
- **`adjacent_pairs(objects: 'Sequence[T]') -> 'zip[tuple[T, ...]]'`** — Alias for ``adjacent_n_tuples(objects, 2)``.
- **`all_elements_are_instances(iterable: 'Iterable[object]', Class: 'type[object]') -> 'bool'`** — Returns ``True`` if all elements of iterable are instances of Class.
- **`batch_by_property(items: 'Iterable[T]', property_func: 'Callable[[T], U]') -> 'list[tuple[list[T], U | None]]'`** — Takes in a Sequence, and returns a list of tuples, (batch, prop)
- **`binary_search(function: 'Callable[[float], float]', target: 'float', lower_bound: 'float', upper_bound: 'float', tolerance: 'float' = 0.0001) -> 'float | None'`** — Searches for a value in a range by repeatedly dividing the range in half.
- **`capture(command: 'str | list[str]', cwd: 'StrOrBytesPath | None' = None, command_input: 'str | None' = None) -> 'tuple[str, str, int]'`**
- **`change_to_rgba_array(image: 'RGBPixelArray', dtype: 'str' = 'uint8') -> 'RGBAPixelArray'`** — Converts an RGB array into RGBA with the alpha value opacity maxed.
- **`clip(a: 'ComparableT', min_a: 'ComparableT', max_a: 'ComparableT') -> 'ComparableT'`** — Clips ``a`` to the interval [``min_a``, ``max_a``].
- **`clockwise_path() -> 'PathFuncType'`** — This function transforms each point by moving clockwise around a half circle.
- **`concatenate_lists(*list_of_lists: 'Iterable[T]') -> 'list[T]'`** — Combines the Iterables provided as arguments into one list.
- **`copy_template_files(project_dir: 'Path' = PosixPath('.'), template_name: 'str' = 'Default') -> 'None'`** — Copies template files from templates dir to project_dir.
- **`counterclockwise_path() -> 'PathFuncType'`** — This function transforms each point by moving counterclockwise around a half circle.
- **`deprecated(func: 'Callable[..., T] | None' = None, since: 'str | None' = None, until: 'str | None' = None, replacement: 'str | None' = None, message: 'str | None' = '') -> 'Callable[..., T] | Callable[[Callable[..., T]], Callable[..., T]]'`** — Decorator to mark a callable as deprecated.
- **`deprecated_params(params: 'str | Iterable[str] | None' = None, since: 'str | None' = None, until: 'str | None' = None, message: 'str' = '', redirections: 'None | Iterable[tuple[str, str] | Callable[..., dict[str, Any]]]' = None) -> 'Callable[..., T]'`** — Decorator to mark parameters of a callable as deprecated.
- **`drag_pixels(frames: 'Sequence[PixelArray]') -> 'list[np.ndarray]'`**
- **`ensure_executable(path_to_exe: 'Path') -> 'bool'`**
- **`extract_mobject_family_members(mobjects: 'Iterable[Mobject]', use_z_index: 'bool' = False, only_those_with_points: 'bool' = False) -> 'list[Mobject]'`** — Returns a list of the types of mobjects and their family members present.
- **`extract_mobject_family_members(mobject_list: 'list[Mobject]', only_those_with_points: 'bool' = False) -> 'list[Mobject]'`**
- **`flatten_iterable_parameters(args: 'Iterable[T | Iterable[T] | GeneratorType]') -> 'list[T]'`** — Flattens an iterable of parameters into a list of parameters.
- **`get_dir_layout(dirpath: 'Path') -> 'Generator[str, None, None]'`** — Get list of paths relative to dirpath of all files in dir and subdirs recursively.
- **`get_full_raster_image_path(image_file_name: 'str | PurePath') -> 'Path'`**
- **`get_full_sound_file_path(sound_file_name: 'StrPath') -> 'Path'`**
- **`get_full_vector_image_path(image_file_name: 'str | PurePath') -> 'Path'`**
- **`get_hash_from_play_call(scene_object: 'Scene', camera_object: 'Camera | OpenGLCamera', animations_list: 'Iterable[Animation]', current_mobjects_list: 'Iterable[Mobject]') -> 'str'`** — Take the list of animations and a list of mobjects and output their hashes. This is meant to be used for `scene.play` function.
- **`get_json(obj: 'Any', *, include_pixel_array: 'bool' = False) -> 'str'`** — Recursively serialize `object` to JSON using the :class:`CustomEncoder` class.
- **`get_module(file_name: 'Path') -> 'types.ModuleType'`**
- **`get_scene_classes_from_module(module: 'types.ModuleType') -> 'list[type[Scene]]'`**
- **`get_scenes_to_render(scene_classes: 'list[type[Scene]]') -> 'list[type[Scene]]'`**
- **`get_template_names() -> 'list[str]'`** — Returns template names from the templates directory.
- **`get_template_path() -> 'Path'`** — Returns the Path of templates directory.
- **`get_video_metadata(path_to_video: 'str | os.PathLike') -> 'VideoMetadata'`**
- **`guarantee_empty_existence(path: 'Path') -> 'Path'`**
- **`guarantee_existence(path: 'Path') -> 'Path'`**
- **`handle_caching_play(func: 'Callable[..., None]') -> 'Callable[..., None]'`** — Decorator that returns a wrapped version of func that will compute
- **`hash_obj(obj: 'object') -> 'int'`** — Determines a hash, even of potentially mutable objects.
- **`index_labels(mobject: 'Mobject', label_height: 'float' = 0.15, background_stroke_width: 'float' = 5, background_stroke_color: 'ManimColor' = ManimColor('#000000'), **kwargs: 'Any') -> 'VGroup'`** — Returns a :class:`~.VGroup` of :class:`~.Integer` mobjects
- **`invert_image(image: 'PixelArray') -> 'Image'`**
- **`is_gif_format() -> 'bool'`** — Determines if output format is .gif
- **`is_mov_format() -> 'bool'`** — Determines if output format is .mov
- **`is_mp4_format() -> 'bool'`** — Determines if output format is .mp4
- **`is_png_format() -> 'bool'`** — Determines if output format is .png
- **`is_webm_format() -> 'bool'`** — Determines if output format is .webm
- **`list_difference_update(l1: 'Iterable[T]', l2: 'Iterable[T]') -> 'list[T]'`** — Returns a list containing all the elements of l1 not in l2.
- **`list_update(l1: 'Iterable[T]', l2: 'Iterable[T]') -> 'list[T]'`** — Used instead of ``set.update()`` to maintain order,
- **`listify(obj: 'str | Iterable[T] | T') -> 'list[str] | list[T]'`** — Converts obj to a list intelligently.
- **`make_even(iterable_1: 'Iterable[T]', iterable_2: 'Iterable[U]') -> 'tuple[list[T], list[U]]'`** — Extends the shorter of the two iterables with duplicate values until its
- **`make_even_by_cycling(iterable_1: 'Collection[T]', iterable_2: 'Collection[U]') -> 'tuple[list[T], list[U]]'`** — Extends the shorter of the two iterables with duplicate values until its
- **`matrix_to_shader_input(matrix: 'MatrixMN') -> 'FlattenedMatrix4x4'`**
- **`merge_dicts_recursively(*dicts: 'dict[Any, Any]') -> 'dict[Any, Any]'`** — Creates a dict whose keyset is the union of all the
- **`modify_atime(file_path: 'str') -> 'None'`** — Will manually change the accessed time (called `atime`) of the file, as on a lot of OS the accessed time refresh is disabled by default.
- **`open_file(file_path: 'Path', in_browser: 'bool' = False) -> 'None'`**
- **`open_media_file(file_writer: 'SceneFileWriter') -> 'None'`**
- **`orthographic_projection_matrix(width: 'float | None' = None, height: 'float | None' = None, near: 'float' = 1, far: 'float' = 21, format_: 'bool' = True) -> 'MatrixMN | FlattenedMatrix4x4'`**
- **`parse_module_attributes() -> 'tuple[AliasDocsDict, DataDict, TypeVarDict]'`** — Read all files, generate Abstract Syntax Trees from them, and
- **`path_along_arc(arc_angle: 'float', axis: 'Vector3DLike' = array([0., 0., 1.])) -> 'PathFuncType'`** — This function transforms each point by moving it along a circular arc.
- **`path_along_circles(arc_angle: 'float', circles_centers: 'Point3DLike_Array', axis: 'Vector3DLike' = array([0., 0., 1.])) -> 'PathFuncType'`** — This function transforms each point by moving it roughly along a circle, each with its own specified center.
- **`perspective_projection_matrix(width: 'float | None' = None, height: 'float | None' = None, near: 'float' = 2, far: 'float' = 50, format_: 'bool' = True) -> 'MatrixMN | FlattenedMatrix4x4'`**
- **`polylabel(rings: 'Sequence[Point3DLike_Array]', precision: 'float' = 0.01) -> 'Cell'`** — Finds the pole of inaccessibility (the point that is farthest from the edges of the polygon)
- **`print_family(mobject: 'Mobject', n_tabs: 'int' = 0) -> 'None'`** — For debugging purposes
- **`prompt_user_for_choice(scene_classes: 'list[type[Scene]]') -> 'list[type[Scene]]'`**
- **`remove_list_redundancies(lst: 'Reversible[H]') -> 'list[H]'`** — Used instead of ``list(set(l))`` to maintain order.
- **`remove_nones(sequence: 'Iterable[T | None]') -> 'list[T]'`** — Removes elements where bool(x) evaluates to False.
- **`resize_array(nparray: 'npt.NDArray[F]', length: 'int') -> 'npt.NDArray[F]'`** — Extends/truncates nparray so that ``len(result) == length``.
- **`resize_preserving_order(nparray: 'npt.NDArray[np.float64]', length: 'int') -> 'npt.NDArray[np.float64]'`** — Extends/truncates nparray so that ``len(result) == length``.
- **`resize_with_interpolation(nparray: 'npt.NDArray[F]', length: 'int') -> 'npt.NDArray[F]'`** — Extends/truncates nparray so that ``len(result) == length``.
- **`restructure_list_to_exclude_certain_family_members(mobject_list: 'list[Mobject]', to_remove: 'list[Mobject]') -> 'list[Mobject]'`** — Removes anything in to_remove from mobject_list, but in the event that one of
- **`rotate_in_place_matrix(initial_position: 'Point3D', x: 'float' = 0, y: 'float' = 0, z: 'float' = 0) -> 'MatrixMN'`**
- **`rotation_matrix(x: 'float' = 0, y: 'float' = 0, z: 'float' = 0) -> 'MatrixMN'`**
- **`scale_matrix(scale_factor: 'float' = 1) -> 'npt.NDArray'`**
- **`scene_classes_from_file(file_path: 'Path', require_single_scene: 'bool' = False, full_list: 'bool' = False) -> 'type[Scene] | list[type[Scene]]'`**
- **`seek_full_path_from_defaults(file_name: 'StrPath', default_dir: 'Path', extensions: 'list[str]') -> 'Path'`**
- **`show_diff_helper(frame_number: 'int', frame_data: 'PixelArray', expected_frame_data: 'PixelArray', control_data_filename: 'str') -> 'None'`** — Will visually display with matplotlib differences between frame generated and the one expected.
- **`sigmoid(x: 'float') -> 'float'`** — Returns the output of the logistic function.
- **`spiral_path(angle: 'float', axis: 'Vector3DLike' = array([0., 0., 1.])) -> 'PathFuncType'`** — This function transforms each point by moving along a spiral to its destination.
- **`straight_path() -> 'PathFuncType'`** — Simplest path function. Each point in a set goes in a straight path toward its destination.
- **`stretch_array_to_length(nparray: 'npt.NDArray[F]', length: 'int') -> 'npt.NDArray[F]'`**
- **`translation_matrix(x: 'float' = 0, y: 'float' = 0, z: 'float' = 0) -> 'MatrixMN'`**
- **`tuplify(obj: 'str | Iterable[T] | T') -> 'tuple[str] | tuple[T]'`** — Converts obj to a tuple intelligently.
- **`typst_to_svg_file(typst_code: 'str', preamble: 'str' = '', text_size: 'float' = 10, font_paths: 'list[str | Path] | None' = None) -> 'Path'`** — Compile a Typst string to SVG via the ``typst`` Python package.
- **`uniq_chain(*args: 'Iterable[T]') -> 'Generator[T, None, None]'`** — Returns a generator that yields all unique elements of the Iterables
- **`update_dict_recursively(current_dict: 'dict[Any, Any]', *others: 'dict[Any, Any]') -> 'None'`**
- **`view_matrix(translation: 'Point3D | None' = None, x_rotation: 'float' = 0, y_rotation: 'float' = 0, z_rotation: 'float' = 0) -> 'MatrixMN'`**
- **`write_to_movie() -> 'bool'`** — Determines from config if the output is a video format such as mp4 or gif, if the --format is set as 'png'
- **`x_rotation_matrix(x: 'float' = 0) -> 'MatrixMN'`**
- **`y_rotation_matrix(y: 'float' = 0) -> 'MatrixMN'`**
- **`z_rotation_matrix(z: 'float' = 0) -> 'MatrixMN'`**

## utils/rate_functions

### `RateFunction(*args, **kwargs)` ← Protocol
> Base class for protocol classes.

<details><summary>métodos próprios (2) · herdados: 0</summary>

- `__call__(self, t: 'float', *args: 'Any', **kwargs: 'Any') -> 'float'` — Call self as a function.
- `__init__(self, *args, **kwargs)`

</details>

- **`double_smooth(t: 'float') -> 'float'`**
- **`ease_in_back(t: 'float') -> 'float'`**
- **`ease_in_bounce(t: 'float') -> 'float'`**
- **`ease_in_circ(t: 'float') -> 'float'`**
- **`ease_in_cubic(t: 'float') -> 'float'`**
- **`ease_in_elastic(t: 'float') -> 'float'`**
- **`ease_in_expo(t: 'float') -> 'float'`**
- **`ease_in_out_back(t: 'float') -> 'float'`**
- **`ease_in_out_bounce(t: 'float') -> 'float'`**
- **`ease_in_out_circ(t: 'float') -> 'float'`**
- **`ease_in_out_cubic(t: 'float') -> 'float'`**
- **`ease_in_out_elastic(t: 'float') -> 'float'`**
- **`ease_in_out_expo(t: 'float') -> 'float'`**
- **`ease_in_out_quad(t: 'float') -> 'float'`**
- **`ease_in_out_quart(t: 'float') -> 'float'`**
- **`ease_in_out_quint(t: 'float') -> 'float'`**
- **`ease_in_out_sine(t: 'float') -> 'float'`**
- **`ease_in_quad(t: 'float') -> 'float'`**
- **`ease_in_quart(t: 'float') -> 'float'`**
- **`ease_in_quint(t: 'float') -> 'float'`**
- **`ease_in_sine(t: 'float') -> 'float'`**
- **`ease_out_back(t: 'float') -> 'float'`**
- **`ease_out_bounce(t: 'float') -> 'float'`**
- **`ease_out_circ(t: 'float') -> 'float'`**
- **`ease_out_cubic(t: 'float') -> 'float'`**
- **`ease_out_elastic(t: 'float') -> 'float'`**
- **`ease_out_expo(t: 'float') -> 'float'`**
- **`ease_out_quad(t: 'float') -> 'float'`**
- **`ease_out_quart(t: 'float') -> 'float'`**
- **`ease_out_quint(t: 'float') -> 'float'`**
- **`ease_out_sine(t: 'float') -> 'float'`**
- **`exponential_decay(t: 'float', half_life: 'float' = 0.1) -> 'float'`**
- **`linear(t: 'float') -> 'float'`**
- **`lingering(t: 'float') -> 'float'`**
- **`not_quite_there(func: 'RateFunction' = <function smooth at 0x713b879e5e40>, proportion: 'float' = 0.7) -> 'RateFunction'`**
- **`running_start(t: 'float', pull_factor: 'float' = -0.5) -> 'float'`**
- **`rush_from(t: 'float', inflection: 'float' = 10.0) -> 'float'`**
- **`rush_into(t: 'float', inflection: 'float' = 10.0) -> 'float'`**
- **`slow_into(t: 'float') -> 'float'`**
- **`smooth(t: 'float', inflection: 'float' = 10.0) -> 'float'`**
- **`smoothererstep(t: 'float') -> 'float'`** — Implementation of the 3rd order SmoothStep sigmoid function.
- **`smootherstep(t: 'float') -> 'float'`** — Implementation of the 2nd order SmoothStep sigmoid function.
- **`smoothstep(t: 'float') -> 'float'`** — Implementation of the 1st order SmoothStep sigmoid function.
- **`squish_rate_func(func: 'RateFunction', a: 'float' = 0.4, b: 'float' = 0.6) -> 'RateFunction'`**
- **`there_and_back(t: 'float', inflection: 'float' = 10.0) -> 'float'`**
- **`there_and_back_with_pause(t: 'float', pause_ratio: 'float' = 0.3333333333333333) -> 'float'`**
- **`unit_interval(function: 'RateFunction') -> 'RateFunction'`**
- **`wiggle(t: 'float', wiggles: 'float' = 2) -> 'float'`**
- **`zero(function: 'RateFunction') -> 'RateFunction'`**

## utils/space_ops

- `DOWN` = `array([ 0., -1.,  0.])`
- `OUT` = `array([0., 0., 1.])`
- `PI` = `3.141592653589793`
- `RIGHT` = `array([1., 0., 0.])`
- `TAU` = `6.283185307179586`
- `TYPE_CHECKING` = `False`
- `UP` = `array([0., 1., 0.])`
- **`R3_to_complex(point: 'Sequence[float]') -> 'np.ndarray'`**
- **`angle_axis_from_quaternion(quaternion: 'Sequence[float]') -> 'Sequence[float]'`** — Gets angle and axis from a quaternion.
- **`angle_between_vectors(v1: 'np.ndarray', v2: 'np.ndarray') -> 'float'`** — Returns the angle between two vectors.
- **`angle_of_vector(vector: 'Sequence[float] | np.ndarray') -> 'float'`** — Returns polar coordinate theta when vector is projected on xy plane.
- **`cartesian_to_spherical(vec: 'Vector3DLike') -> 'np.ndarray'`** — Returns an array of numbers corresponding to each
- **`center_of_mass(points: 'PointNDLike_Array') -> 'PointND'`** — Gets the center of mass of the points in space.
- **`compass_directions(n: 'int' = 4, start_vect: 'np.ndarray' = array([1., 0., 0.])) -> 'np.ndarray'`** — Finds the cardinal directions using tau.
- **`complex_func_to_R3_func(complex_func: 'Callable[[complex], complex]') -> 'Callable[[Point3DLike], Point3D]'`**
- **`complex_to_R3(complex_num: 'complex') -> 'np.ndarray'`**
- **`cross(v1: 'Vector3DLike', v2: 'Vector3DLike') -> 'Vector3D'`**
- **`cross2d(a: 'Vector2D | Vector2D_Array', b: 'Vector2D | Vector2D_Array') -> 'ManimFloat | npt.NDArray[ManimFloat]'`** — Compute the determinant(s) of the passed
- **`earclip_triangulation(verts: 'np.ndarray', ring_ends: 'list') -> 'list'`** — Returns a list of indices giving a triangulation
- **`find_intersection(p0s: 'Point3DLike_Array', v0s: 'Vector3DLike_Array', p1s: 'Point3DLike_Array', v1s: 'Vector3DLike_Array', threshold: 'float' = 1e-05) -> 'list[Point3D]'`** — Return the intersection of a line passing through p0 in direction v0
- **`get_unit_normal(v1: 'Vector3DLike', v2: 'Vector3DLike', tol: 'float' = 1e-06) -> 'Vector3D'`** — Gets the unit normal of the vectors.
- **`get_winding_number(points: 'Sequence[np.ndarray]') -> 'float'`** — Determine the number of times a polygon winds around the origin.
- **`line_intersection(line1: 'Sequence[np.ndarray]', line2: 'Sequence[np.ndarray]') -> 'np.ndarray'`** — Returns the intersection point of two lines, each defined by
- **`midpoint(point1: 'Sequence[float]', point2: 'Sequence[float]') -> 'float | np.ndarray'`** — Gets the midpoint of two points.
- **`norm_squared(v: 'float') -> 'float'`**
- **`normalize(vect: 'np.ndarray | tuple[float]', fall_back: 'np.ndarray | None' = None) -> 'np.ndarray'`**
- **`normalize_along_axis(array: 'np.ndarray', axis: 'np.ndarray') -> 'np.ndarray'`** — Normalizes an array with the provided axis.
- **`perpendicular_bisector(line: 'Sequence[np.ndarray]', norm_vector: 'Vector3D' = array([0., 0., 1.])) -> 'Sequence[np.ndarray]'`** — Returns a list of two points that correspond
- **`quaternion_conjugate(quaternion: 'Sequence[float]') -> 'np.ndarray'`** — Used for finding the conjugate of the quaternion
- **`quaternion_from_angle_axis(angle: 'float', axis: 'np.ndarray', axis_normalized: 'bool' = False) -> 'list[float]'`** — Gets a quaternion from an angle and an axis.
- **`quaternion_mult(*quats: 'Sequence[float]') -> 'np.ndarray | list[float | np.ndarray]'`** — Gets the Hamilton product of the quaternions provided.
- **`regular_vertices(n: 'int', *, radius: 'float' = 1, start_angle: 'float | None' = None) -> 'tuple[np.ndarray, float]'`** — Generates regularly spaced vertices around a circle centered at the origin.
- **`rotate_vector(vector: 'Vector3DLike', angle: 'float', axis: 'Vector3DLike' = array([0., 0., 1.])) -> 'Vector3D'`** — Function for rotating a vector.
- **`rotation_about_z(angle: 'float') -> 'np.ndarray'`** — Returns a rotation matrix for a given angle.
- **`rotation_matrix(angle: 'float', axis: 'Vector3DLike', homogeneous: 'bool' = False) -> 'np.ndarray'`** — Rotation in R^3 about a specified axis of rotation.
- **`rotation_matrix_from_quaternion(quat: 'np.ndarray') -> 'np.ndarray'`**
- **`rotation_matrix_transpose(angle: 'float', axis: 'Vector3DLike') -> 'np.ndarray'`**
- **`rotation_matrix_transpose_from_quaternion(quat: 'np.ndarray') -> 'list[np.ndarray]'`** — Converts the quaternion, quat, to an equivalent rotation matrix representation.
- **`shoelace(x_y: 'Point2D_Array') -> 'float'`** — 2D implementation of the shoelace formula.
- **`shoelace_direction(x_y: 'Point2D_Array') -> 'str'`** — Uses the area determined by the shoelace method to determine whether
- **`spherical_to_cartesian(spherical: 'Sequence[float]') -> 'np.ndarray'`** — Returns a numpy array ``[x, y, z]`` based on the spherical
- **`thick_diagonal(dim: 'int', thickness: 'int' = 2) -> 'MatrixMN'`**
- **`z_to_vector(vector: 'np.ndarray') -> 'np.ndarray'`** — Returns some matrix in SO(3) which takes the z-axis to the

## utils/tex

### `TexFontTemplates()`
> A collection of TeX templates for the fonts described at http://jf.burnol.free.fr/showcase.html

### `TexTemplate(tex_compiler: 'str | list[str]' = 'latex', description: 'str' = '', output_format: 'str' = '.dvi', documentclass: 'str' = '\\documentclass[preview]{standalone}', preamble: 'str' = '\\usepackage[english]{babel}\n\\usepackage{amsmath}\n\\usepackage{amssymb}', placeholder_text: 'str' = 'YourTextHere', post_doc_commands: 'str' = '') -> None`
> TeX templates are used to create ``Tex`` and ``MathTex`` objects.

<details><summary>métodos próprios (7) · herdados: 0</summary>

- `__init__(self, tex_compiler: 'str | list[str]' = 'latex', description: 'str' = '', output_format: 'str' = '.dvi', documentclass: 'str' = '\\documentclass[preview]{standalone}', preamble: 'str' = '\\usepackage[english]{babel}\n\\usepackage{amsmath}\n\\usepackage{amssymb}', placeholder_text: 'str' = 'YourTextHere', post_doc_commands: 'str' = '') -> None` — Initialize self.  See help(type(self)) for accurate signature.
- `add_to_document(self, txt: 'str') -> 'Self'` — Adds text to the TeX template just after \begin{document}, e.g. ``\boldmath``.
- `add_to_preamble(self, txt: 'str', prepend: 'bool' = False) -> 'Self'` — Adds text to the TeX template's preamble (e.g. definitions, packages). Text can be inserted at the beginning or at the end of the preamble.
- `copy(self) -> 'Self'` — Create a deep copy of the TeX template instance.
- `from_file(file: 'StrPath' = 'tex_template.tex', **kwargs: 'Any') -> 'Self'` — Create an instance by reading the content of a file.
- `get_texcode_for_expression(self, expression: 'str') -> 'str'` — Inserts expression verbatim into TeX template.
- `get_texcode_for_expression_in_env(self, expression: 'str', environment: 'str') -> 'str'` — Inserts expression into TeX template wrapped in ``\begin{environment}`` and ``\end{environment}``.

</details>

### `TexTemplateLibrary()`
> A collection of basic TeX template objects

- `LATEX_ERROR_INSIGHTS` = `[('inputenc Error: Unicode character (?:.*) \\(U\\+([0-9a-fA-F]+)\\)', <function insight_inputenc_error at 0x713b8440...`
- `TYPE_CHECKING` = `False`
- **`compile_tex(tex_file: 'Path', tex_compiler: 'str | list[str]', output_format: 'str') -> 'Path'`** — Compiles a tex_file into a .dvi or a .xdv or a .pdf
- **`convert_to_svg(dvi_file: 'Path', extension: 'str', page: 'int' = 1) -> 'Path'`** — Converts a .dvi, .xdv, or .pdf file into an svg using dvisvgm.
- **`delete_nonsvg_files(additional_endings: 'Iterable[str]' = ()) -> 'None'`** — Deletes every file that does not have a suffix in ``(".svg", ".tex", *additional_endings)``
- **`generate_tex_file(expression: 'str', environment: 'str | None' = None, tex_template: 'TexTemplate | None' = None) -> 'Path'`** — Takes a tex expression (and an optional tex environment),
- **`insight_inputenc_error(matching: 'Match[str]') -> 'Generator[str]'`**
- **`insight_package_not_found_error(matching: 'Match[str]') -> 'Generator[str]'`**
- **`make_tex_compilation_command(tex_compiler: 'str', output_format: 'str', tex_file: 'Path', tex_dir: 'Path') -> 'list[str]'`** — Prepares the TeX compilation command, i.e. the TeX compiler name
- **`print_all_tex_errors(log_file: 'Path', tex_compiler: 'str', tex_file: 'Path') -> 'None'`**
- **`print_tex_error(tex_compilation_log: 'Sequence[str]', error_start_index: 'int', tex_source: 'Sequence[str]') -> 'None'`**
- **`tex_hash(expression: 'Any') -> 'str'`**
- **`tex_to_svg_file(expression: 'str', environment: 'str | None' = None, tex_template: 'TexTemplate | None' = None) -> 'Path'`** — Takes a tex expression and returns the svg version of the compiled tex

