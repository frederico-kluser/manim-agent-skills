# ManimCE v0.21.0 × ManimGL v1.7.2

Mapa de compatibilidade gerado por reflexão dos dois pacotes instalados (`mx api-diff`) — não escrito à mão, não copiado de blog.

## Resumo

| | ManimCE | ManimGL |
|---|---:|---:|
| import | `from manim import *` | `from manimlib import *` |
| CLI | `manim` | `manimgl` |
| classes públicas | 337 | 270 |
| funções públicas | 281 | 216 |
| classes só nesta edição | 184 | 117 |
| classes com nome em comum | 153 | 153 |

> **Os dois não são compatíveis no nível de código-fonte.** Um script escrito para um não roda no outro sem tradução.

## Renomeações e mudanças de fluxo

Coluna de existência verificada contra os pacotes instalados: `✓` existe, `—` não existe.

| ManimGL (3b1b) | existe? | ManimCE | existe? | observação |
|---|:-:|---|:-:|---|
| `ShowCreation` | ✓ | `Create` | ✓ | renomeada na CE; `ShowCreation` não existe lá |
| `TexMobject` | — | `MathTex` | ✓ | LaTeX em modo matemático |
| `TextMobject` | — | `Tex` | ✓ | LaTeX em modo texto |
| `TexText` | ✓ | `Tex` | ✓ | nome do 3b1b para texto LaTeX |
| `GraphScene` | — | `Axes` | ✓ | `GraphScene` foi removida da CE; use `Axes` numa `Scene` |
| `get_graph` | — | `Axes.plot` | ✓ | virou método do `Axes` |
| `get_graph_label` | — | `Axes.get_graph_label` | ✓ | método do `Axes` |
| `CONFIG = {...}` | — | `argumentos de __init__` | — | a CE removeu os dicts `CONFIG` |
| `ApplyMethod(m.shift, UP)` | ✓ | `m.animate.shift(UP)` | — | sintaxe `.animate` |
| `self.play(m.shift, UP)` | — | `self.play(m.animate.shift(UP))` | — | GL aceita método cru |
| `interactive_embed()` | — | `--renderer=opengl` | — | fluxos interativos diferentes |
| `checkpoint_paste()` | — | `(sem equivalente)` | — | recurso do fluxo pessoal do 3b1b |
| `Group` | ✓ | `Group / VGroup` | ✓ | na CE, `VGroup` só aceita `VMobject` |
| `self.embed()` | — | `(sem equivalente)` | — | REPL embutido do ManimGL |
| `Mobject.set_color` | ✓ | `Mobject.set_color` | ✓ | existe nos dois; assinatura difere |

## Classes só no ManimCE (184)

```
AbstractImageMobject, Add, AddTextLetterByLetter, Angle, AnnotationDot, ArcBrace
ArcPolygon, ArcPolygonFromArcs, Arrow3D, ArrowCircleFilledTip, ArrowCircleTip, ArrowSquareFilledTip
ArrowSquareTip, ArrowTriangleFilledTip, ArrowTriangleTip, ArrowVectorField, BackgroundColoredVMobjectDisplayer, Blink
BraceBetweenPoints, CairoRenderer, CapStyleType, Cell, ChangeSpeed, Circumscribe
ClickArgs, ClockwiseTransform, Comparable, ConvertToOpenGL, ConvexHull, ConvexHull3D
CounterclockwiseTransform, Create, Cutout, DecimalTable, DefaultGroup, DefaultSectionType
DiGraph, DictAsObject, Dot3D, DoubleArrow, DummySceneFileWriter, EndSceneEarlyException
Facet, FullScreenQuad, GenericGraph, Graph, HSV, HealthCheckFunction
Horizon, Icosahedron, ImageMobjectFromCamera, IntegerTable, JSONFormatter, Label
LabeledArrow, LabeledDot, LabeledLine, LabeledPolygram, LayoutFunction, LineJointType
LinearBase, LinearTransformationScene, LogBase, ManimBanner, ManimColor, ManimConfig
ManimFrame, MappingCamera, MarkupUtils, MathTable, MathTex, MathTexPart
MathTypst, Mesh, MethodWithArgs, Mobject1D, Mobject2D, MobjectTable
MovingCamera, MovingCameraScene, MultiAnimationOverrideException, MultiCamera, Object3D, Octahedron
OldMultiCamera, OpenGLAnnularSector, OpenGLAnnulus, OpenGLArc, OpenGLArcBetweenPoints, OpenGLArrow
OpenGLArrowTip, OpenGLCamera, OpenGLCircle, OpenGLCubicBezier, OpenGLCurvedArrow, OpenGLCurvedDoubleArrow
OpenGLCurvesAsSubmobjects, OpenGLDashedLine, OpenGLDashedVMobject, OpenGLDot, OpenGLDoubleArrow, OpenGLElbow
OpenGLEllipse, OpenGLGroup, OpenGLImageMobject, OpenGLLine, OpenGLMobject, OpenGLPGroup
OpenGLPMPoint, OpenGLPMobject, OpenGLPoint, OpenGLPolygon, OpenGLRectangle, OpenGLRegularPolygon
OpenGLRenderer, OpenGLRoundedRectangle, OpenGLSector, OpenGLSquare, OpenGLSurface, OpenGLSurfaceGroup
OpenGLSurfaceMesh, OpenGLTangentLine, OpenGLTexturedSurface, OpenGLTipableVMobject, OpenGLTriangle, OpenGLVGroup
OpenGLVMobject, OpenGLVector, OpenGLVectorizedPoint, PangoUtils, Paragraph, ParametricFunction
Percent, PointCloudDot, PolarPlane, Polygram, Polyhedron, QualityDict
QuickHull, QuickHullPoint, RGBA, RandomColorGenerator, RateFunction, RegularPolygram
RemoveTextLetterByLetter, RendererType, RerunSceneException, RerunSceneHandler, RightAngle, SceneInteractContinue
SceneInteractRerun, Section, Shader, ShaderWrapper, ShowPassingFlashWithThinningStrokeWidth, SingleStringMathTex
SpecialThreeDScene, SpinInFromNothing, SpiralIn, SplitScreenCamera, Star, StealthTip
SubFacet, Table, TangentialArc, Tetrahedron, TexFontTemplates, TexTemplate
TexTemplateLibrary, TextSetting, ThreeDVMobject, TransformAnimations, TransformMatchingAbstractBase, TypeWithCursor
Typst, UntypeWithCursor, Unwrite, VDict, Variable, VectorScene
VideoMetadata, Wait, Wiggle, ZoomedScene
```

## Classes só no ManimGL (117)

```
AnimatedStreamLines, AnimationOnSurroundingRectangle, BlankScene, Bubble, Bundling, Button
CameraFrame, Checkbox, Checkmark, CheckpointManager, CircleIndicate, Clock
ClockPassesTime, ColorSliders, ControlMobject, ControlPanel, CountInFrom, Dartboard
DieFace, Disk3D, DoubleSpeechBubble, Drawing, EnableDisableButton, EndScene
EventDispatcher, EventListener, EventType, Exmark, ExponentialValueTracker, Fade
FadeInFromPoint, FadeOutToPoint, FlashAround, FlashUnder, FlashyFadeIn, FrameStream
FullScreenFadeRectangle, GlowDot, GlowDots, Gpu, InteractiveScene, InteractiveSceneEmbed
JuliaFractal, Keys, Laptop, LatexError, Lightbulb, LineBrace
LinearNumberSlider, MandelbrotFractal, Material, MetaNewtonFractal, Mods, ModuleLoader
MotionMobject, NewtonFractal, OldSpeechBubble, OldTex, OldTexText, OldThoughtBubble
ParametricCurve, ParametricSurface, Piano, Piano3D, PipelineState, PlaneFractal
Polyline, Prismify, RenderPass, Renderer, SceneState, SharedBuffer
ShowCreation, ShowCreationThenDestruction, ShowCreationThenDestructionAround, ShowCreationThenFadeAround, ShowCreationThenFadeOut, ShowPassingFlashAround
SingleStringTex, Slider, SmallDot, SpeechBubble, Speedometer, Square3D
StringMobject, StrokeArrow, StructuredArray, SurfaceDrawing, SurfaceMesh, TexMatrix
TexText, TexTextFromPresetString, Textbox, TexturedGeometry, TexturedSurface, ThoughtBubble
ThreeDModel, TimeVaryingVectorField, TracingTail, TransformMatchingParts, TransformMatchingStrings, TurnInsideOut
Uniforms, Updater, VCube, VDrawing, VFadeIn, VFadeInThenOut
VFadeOut, VGroup3D, VHighlight, VPrism, VShowPassingFlash, VectorizedEarth
VideoIcon, VideoSeries, WiggleOutThenIn
```

## Nome igual, assinatura diferente (153 de 153)

Esta é a armadilha silenciosa: o import funciona, o construtor aceita, e o resultado sai errado.

| classe | assinatura CE | assinatura GL |
|---|---|---|
| `AddTextWordByWord` | `(text_mobject: 'Text', run_time: 'float' = None, time_per_char: 'float' = 0.06, **kwargs) -> 'None'` | `(string_mobject: 'StringMobject', time_per_word: 'float' = 0.2, run_time: 'float' = -1.0, rate_func:` |
| `AnimatedBoundary` | `(vmobject: 'VMobject', colors: 'Sequence[ParsableManimColor]' = [ManimColor('#29ABCA'), ManimColor('` | `(vmobject: 'VMobject', colors: 'List[ManimColor]' = ['#29ABCA', '#9CDCEB', '#1C758A', '#736357'], ma` |
| `Animation` | `(mobject=None, *args, use_override=True, **kwargs) -> 'Self'` | `(mobject: 'Mobject', run_time: 'float' = 1.0, time_span: 'tuple[float, float] | None' = None, lag_ra` |
| `AnimationGroup` | `(*animations: 'Animation | Iterable[Animation]', group: 'Group | VGroup | OpenGLGroup | OpenGLVGroup` | `(*args: 'AnimationType | Iterable[AnimationType]', run_time: 'float' = -1, lag_ratio: 'float' = 0.0,` |
| `AnnularSector` | `(inner_radius: 'float' = 1, outer_radius: 'float' = 2, angle: 'float' = 1.5707963267948966, start_an` | `(angle: 'float' = 1.5707963267948966, start_angle: 'float' = 0.0, inner_radius: 'float' = 1.0, outer` |
| `Annulus` | `(inner_radius: 'float' = 1, outer_radius: 'float' = 2, fill_opacity: 'float' = 1, stroke_width: 'flo` | `(inner_radius: 'float' = 1.0, outer_radius: 'float' = 2.0, fill_opacity: 'float' = 1.0, stroke_width` |
| `ApplyComplexFunction` | `(function: 'types.MethodType', mobject: 'Mobject', **kwargs) -> 'None'` | `(function: 'Callable[[complex], complex]', mobject: 'Mobject', **kwargs)` |
| `ApplyFunction` | `(function: 'types.MethodType', mobject: 'Mobject', **kwargs) -> 'None'` | `(function: 'Callable[[Mobject], Mobject]', mobject: 'Mobject', **kwargs)` |
| `ApplyMatrix` | `(matrix: 'np.ndarray', mobject: 'Mobject', about_point: 'np.ndarray' = array([0., 0., 0.]), **kwargs` | `(matrix: 'npt.ArrayLike', mobject: 'Mobject', **kwargs)` |
| `ApplyMethod` | `(method: 'Callable', *args, **kwargs) -> 'None'` | `(method: 'Callable', *args, **kwargs)` |
| `ApplyPointwiseFunction` | `(function: 'types.MethodType', mobject: 'Mobject', run_time: 'float' = 3.0, **kwargs) -> 'None'` | `(function: 'Callable[[np.ndarray], np.ndarray]', mobject: 'Mobject', run_time: 'float' = 3.0, **kwar` |
| `ApplyPointwiseFunctionToCenter` | `(function: 'types.MethodType', mobject: 'Mobject', **kwargs) -> 'None'` | `(function: 'Callable[[np.ndarray], np.ndarray]', mobject: 'Mobject', **kwargs)` |
| `ApplyWave` | `(mobject: 'Mobject', direction: 'Vector3DLike' = array([0., 1., 0.]), amplitude: 'float' = 0.2, wave` | `(mobject: 'Mobject', direction: 'np.ndarray' = array([0., 1., 0.]), amplitude: 'float' = 0.2, run_ti` |
| `Arc` | `(radius: 'float | None' = 1.0, start_angle: 'float' = 0, angle: 'float' = 1.5707963267948966, num_co` | `(start_angle: 'float' = 0, angle: 'float' = 1.5707963267948966, radius: 'float' = 1.0, n_components:` |
| `ArcBetweenPoints` | `(start: 'Point3DLike', end: 'Point3DLike', angle: 'float' = 1.5707963267948966, radius: 'float | Non` | `(start: 'Vect3', end: 'Vect3', angle: 'float' = 1.5707963267948966, **kwargs)` |
| `Arrow` | `(*args: 'Any', stroke_width: 'float' = 6, buff: 'float' = 0.25, max_tip_length_to_length_ratio: 'flo` | `(start: 'Vect3 | Mobject' = array([-1.,  0.,  0.]), end: 'Vect3 | Mobject' = array([-1.,  0.,  0.]),` |
| `ArrowTip` | `(*args: 'Any', **kwargs: 'Any') -> 'None'` | `(angle: 'float' = 0, width: 'float' = 0.35, length: 'float' = 0.35, fill_opacity: 'float' = 1.0, fil` |
| `Axes` | `(x_range: 'Sequence[float] | None' = None, y_range: 'Sequence[float] | None' = None, x_length: 'floa` | `(x_range: 'RangeSpecifier' = (-8.0, 8.0, 1.0), y_range: 'RangeSpecifier' = (-4.0, 4.0, 1.0), axis_co` |
| `BackgroundRectangle` | `(*mobjects: 'Mobject', color: 'ParsableManimColor | None' = None, stroke_width: 'float' = 0, stroke_` | `(mobject: 'Mobject', color: 'ManimColor' = None, stroke_width: 'float' = 0, stroke_opacity: 'float' ` |
| `BarChart` | `(values: 'MutableSequence[float]', bar_names: 'Sequence[str] | None' = None, y_range: 'Sequence[floa` | `(values: 'Iterable[float]', height: 'float' = 4, width: 'float' = 6, n_ticks: 'int' = 4, include_x_t` |
| `Brace` | `(mobject: 'Mobject', direction: 'Vector3DLike' = array([ 0., -1.,  0.]), buff: 'float' = 0.2, sharpn` | `(mobject: 'Mobject', direction: 'Vect3' = array([ 0., -1.,  0.]), buff: 'float' = 0.2, tex_string: '` |
| `BraceLabel` | `(obj: 'Mobject', text: 'str', brace_direction: 'Vector3DLike' = array([ 0., -1.,  0.]), label_constr` | `(obj: 'VMobject | list[VMobject]', text: 'str | Iterable[str]', brace_direction: 'np.ndarray' = arra` |
| `BraceText` | `(obj: 'Mobject', text: 'str', label_constructor: 'type[SingleStringMathTex | Text]' = <class 'manim.` | `(obj: 'VMobject | list[VMobject]', text: 'str | Iterable[str]', brace_direction: 'np.ndarray' = arra` |
| `Broadcast` | `(mobject: 'Mobject', focal_point: 'Sequence[float]' = array([0., 0., 0.]), n_mobs: 'int' = 5, initia` | `(focal_point: 'np.ndarray', small_radius: 'float' = 0.0, big_radius: 'float' = 5.0, n_circles: 'int'` |
| `BulletedList` | `(*items: 'str', buff: 'float' = 0.5, dot_scale_factor: 'float' = 2, tex_environment: 'str | None' = ` | `(*items: 'str', buff: 'float' = 0.5, aligned_edge: 'Vect3' = array([-1.,  0.,  0.]), numbered: 'bool` |
| `Camera` | `(background_image: 'str | None' = None, frame_center: 'Point3D' = array([0., 0., 0.]), image_mode: '` | `(window: 'Optional[Window]' = None, frame_config: 'dict' = {}, resolution=(1920, 1080), fps: 'int' =` |
| `ChangeDecimalToValue` | `(decimal_mob: 'DecimalNumber', target_number: 'int', **kwargs: 'Any') -> 'None'` | `(decimal_mob: 'DecimalNumber', target_number: 'float | complex', **kwargs)` |
| `ChangingDecimal` | `(decimal_mob: 'DecimalNumber', number_update_func: 'Callable[[float], float]', suspend_mobject_updat` | `(decimal_mob: 'DecimalNumber', number_update_func: 'Callable[[float], float]', suspend_mobject_updat` |
| `Circle` | `(radius: 'float | None' = None, color: 'ParsableManimColor' = ManimColor('#FC6255'), **kwargs: 'Any'` | `(start_angle: 'float' = 0, stroke_color: 'ManimColor' = '#FC6255', **kwargs)` |
| `Code` | `(code_file: 'StrPath | None' = None, code_string: 'str | None' = None, language: 'str | None' = None` | `(code: 'str', font: 'str' = 'Consolas', font_size: 'int' = 24, lsh: 'float' = 1.0, fill_color: 'Mani` |
| `ComplexHomotopy` | `(complex_homotopy: 'Callable[[complex, float], float]', mobject: 'Mobject', **kwargs: 'Any')` | `(complex_homotopy: 'Callable[[complex, float], complex]', mobject: 'Mobject', **kwargs)` |
| `ComplexPlane` | `(**kwargs: 'Any')` | `(x_range: 'RangeSpecifier' = (-8.0, 8.0, 1.0), y_range: 'RangeSpecifier' = (-4.0, 4.0, 1.0), backgro` |
| `ComplexValueTracker` | `(value: 'float' = 0, **kwargs: 'Any') -> 'None'` | `(value: 'float | complex | np.ndarray' = 0, **kwargs)` |
| `Cone` | `(base_radius: 'float' = 1, height: 'float' = 1, direction: 'Vector3DLike' = array([0., 0., 1.]), sho` | `(u_range: 'Tuple[float, float]' = (0, 6.283185307179586), v_range: 'Tuple[float, float]' = (0, 1), *` |
| `CoordinateSystem` | `(x_range: 'Sequence[float] | None' = None, y_range: 'Sequence[float] | None' = None, x_length: 'floa` | `(x_range: 'RangeSpecifier' = (-8.0, 8.0, 1.0), y_range: 'RangeSpecifier' = (-4.0, 4.0, 1.0), num_sam` |
| `Cross` | `(mobject: 'Mobject | None' = None, stroke_color: 'ParsableManimColor' = ManimColor('#FC6255'), strok` | `(mobject: 'Mobject', stroke_color: 'ManimColor' = '#FC6255', stroke_width: 'float | Sequence[float]'` |
| `Cube` | `(side_length: 'float' = 2, fill_opacity: 'float' = 0.75, fill_color: 'ParsableManimColor' = ManimCol` | `(color: 'ManimColor' = '#58C4DD', opacity: 'float' = 1, shading: 'Tuple[float, float, float]' = (0.1` |
| `CubicBezier` | `(start_anchor: 'Point3DLike', start_handle: 'Point3DLike', end_handle: 'Point3DLike', end_anchor: 'P` | `(a0: 'Vect3', h0: 'Vect3', h1: 'Vect3', a1: 'Vect3', **kwargs)` |
| `CurvedArrow` | `(start_point: 'Point3DLike', end_point: 'Point3DLike', **kwargs: 'Any') -> 'None'` | `(start_point: 'Vect3', end_point: 'Vect3', **kwargs)` |
| `CurvedDoubleArrow` | `(start_point: 'Point3DLike', end_point: 'Point3DLike', **kwargs: 'Any') -> 'None'` | `(start_point: 'Vect3', end_point: 'Vect3', **kwargs)` |
| `CurvesAsSubmobjects` | `(vmobject: 'VMobject', **kwargs) -> 'None'` | `(vmobject: 'VMobject', **kwargs)` |
| `CyclicReplace` | `(*mobjects: 'Mobject', path_arc: 'float' = 1.5707963267948966, **kwargs) -> 'None'` | `(*mobjects: 'Mobject', path_arc=1.5707963267948966, **kwargs)` |
| `Cylinder` | `(radius: 'float' = 1, height: 'float' = 2, direction: 'Vector3DLike' = array([0., 0., 1.]), v_range:` | `(u_range: 'Tuple[float, float]' = (0, 6.283185307179586), v_range: 'Tuple[float, float]' = (-1, 1), ` |
| `DashedLine` | `(*args: 'Any', dash_length: 'float' = 0.05, dashed_ratio: 'float' = 0.5, **kwargs: 'Any') -> 'None'` | `(start: 'Vect3' = array([-1.,  0.,  0.]), end: 'Vect3' = array([1., 0., 0.]), dash_length: 'float' =` |
| `DashedVMobject` | `(vmobject: 'VMobject', num_dashes: 'int' = 15, dashed_ratio: 'float' = 0.5, dash_offset: 'float' = 0` | `(vmobject: 'VMobject', num_dashes: 'int' = 15, positive_space_ratio: 'float' = 0.5, **kwargs)` |
| `DecimalMatrix` | `(matrix: 'Iterable[Iterable[Any]]', element_to_mobject: 'type[VMobject] | Callable[..., VMobject]' =` | `(matrix: 'FloatMatrixType', num_decimal_places: 'int' = 2, decimal_config: 'dict' = {}, **config)` |
| `DecimalNumber` | `(number: 'float' = 0, num_decimal_places: 'int' = 2, mob_class: 'type[SingleStringMathTex]' = <class` | `(number: 'float | complex' = 0, color: 'ManimColor' = '#FFFFFF', stroke_width: 'float' = 0, fill_opa` |
| `Difference` | `(subject: 'VMobject', clip: 'VMobject', **kwargs: 'Any') -> 'None'` | `(subject: 'VMobject', clip: 'VMobject', **kwargs)` |
| `Dodecahedron` | `(edge_length: 'float' = 1, **kwargs: 'Any')` | `(fill_color: 'ManimColor' = '#1C758A', fill_opacity: 'float' = 1, stroke_color: 'ManimColor' = '#1C7` |
| `Dot` | `(point: 'Point3DLike' = array([0., 0., 0.]), radius: 'float' = 0.08, stroke_width: 'float' = 0, fill` | `(point: 'Vect3' = array([0., 0., 0.]), radius: 'float' = 0.08, stroke_color: 'ManimColor' = '#000000` |
| `DotCloud` | `(color: 'ParsableManimColor' = ManimColor('#FFFF00'), stroke_width: 'float' = 2.0, radius: 'float' =` | `(points: 'Vect3Array' = array([[0., 0., 0.]]), color: 'ManimColor' = '#888888', opacity: 'float' = 1` |
| `DrawBorderThenFill` | `(vmobject: 'VMobject | OpenGLVMobject', run_time: 'float' = 2, rate_func: 'Callable[[float], float]'` | `(vmobject: 'VMobject', run_time: 'float' = 2.0, rate_func: 'Callable[[float], float]' = <function do` |
| `Elbow` | `(width: 'float' = 0.2, angle: 'float' = 0, **kwargs: 'Any') -> 'None'` | `(width: 'float' = 0.2, angle: 'float' = 0, **kwargs)` |
| `Ellipse` | `(width: 'float' = 2, height: 'float' = 1, **kwargs: 'Any') -> 'None'` | `(width: 'float' = 2.0, height: 'float' = 1.0, **kwargs)` |
| `Exclusion` | `(subject: 'VMobject', clip: 'VMobject', **kwargs: 'Any') -> 'None'` | `(*vmobjects: 'VMobject', **kwargs)` |
| `FadeIn` | `(*mobjects: 'Mobject', **kwargs: 'Any') -> 'None'` | `(mobject: 'Mobject', shift: 'np.ndarray' = array([0., 0., 0.]), scale: 'float' = 1, **kwargs)` |
| `FadeOut` | `(*mobjects: 'Mobject', **kwargs: 'Any') -> 'None'` | `(mobject: 'Mobject', shift: 'Vect3' = array([0., 0., 0.]), remover: 'bool' = True, final_alpha_value` |
| `FadeToColor` | `(mobject: 'Mobject', color: 'str', **kwargs) -> 'None'` | `(mobject: 'Mobject', color: 'ManimColor', **kwargs)` |
| `FadeTransform` | `(mobject: 'Mobject', target_mobject: 'Mobject', stretch: 'bool' = True, dim_to_match: 'int' = 1, **k` | `(mobject: 'Mobject', target_mobject: 'Mobject', stretch: 'bool' = True, dim_to_match: 'int' = 1, **k` |
| `FadeTransformPieces` | `(mobject: 'Mobject', target_mobject: 'Mobject', stretch: 'bool' = True, dim_to_match: 'int' = 1, **k` | `(mobject: 'Mobject', target_mobject: 'Mobject', stretch: 'bool' = True, dim_to_match: 'int' = 1, **k` |
| `Flash` | `(point: 'Point3DLike | Mobject', line_length: 'float' = 0.2, num_lines: 'int' = 12, flash_radius: 'f` | `(point: 'np.ndarray | Mobject', color: 'ManimColor' = '#FFFF00', line_length: 'float' = 0.2, num_lin` |
| `FocusOn` | `(focus_point: 'Point3DLike | Mobject', opacity: 'float' = 0.2, color: 'ParsableManimColor' = ManimCo` | `(focus_point: 'np.ndarray | Mobject', opacity: 'float' = 0.2, color: 'ManimColor' = '#888888', run_t` |
| `FullScreenRectangle` | `(**kwargs: 'Any') -> 'None'` | `(height: 'float' = 8.0, fill_color: 'ManimColor' = '#222222', fill_opacity: 'float' = 1, stroke_widt` |
| `FunctionGraph` | `(function: 'Callable[[float], Any]', x_range: 'tuple[float, float] | tuple[float, float, float] | No` | `(function: 'Callable[[float], float]', x_range: 'Tuple[float, float, float]' = (-8, 8, 0.25), color:` |
| `Group` | `(*mobjects: 'Any', **kwargs: 'Any') -> 'None'` | `(*mobjects: 'SubmobjectType | Iterable[SubmobjectType]', **kwargs)` |
| `GrowArrow` | `(arrow: 'Arrow', point_color: 'ParsableManimColor | None' = None, **kwargs: 'Any')` | `(arrow: 'Arrow', **kwargs)` |
| `GrowFromCenter` | `(mobject: 'Mobject', point_color: 'ParsableManimColor | None' = None, **kwargs: 'Any')` | `(mobject: 'Mobject', **kwargs)` |
| `GrowFromEdge` | `(mobject: 'Mobject', edge: 'Vector3DLike', point_color: 'ParsableManimColor | None' = None, **kwargs` | `(mobject: 'Mobject', edge: 'np.ndarray', **kwargs)` |
| `GrowFromPoint` | `(mobject: 'Mobject', point: 'Point3DLike', point_color: 'ParsableManimColor | None' = None, **kwargs` | `(mobject: 'Mobject', point: 'np.ndarray', point_color: 'ManimColor' = None, **kwargs)` |
| `Homotopy` | `(homotopy: 'Callable[[float, float, float, float], tuple[float, float, float]]', mobject: 'Mobject',` | `(homotopy: 'Callable[[float, float, float, float], Sequence[float]]', mobject: 'Mobject', run_time: ` |
| `ImageMobject` | `(filename_or_array: 'StrPath | npt.NDArray', scale_to_resolution: 'int' = 1080, invert: 'bool' = Fal` | `(filename: 'str', height: 'float' = 4.0, **kwargs)` |
| `ImplicitFunction` | `(func: 'Callable[[float, float], float]', x_range: 'Sequence[float] | None' = None, y_range: 'Sequen` | `(func: 'Callable[[float, float], float]', x_range: 'Tuple[float, float]' = (-7.111111111111111, 7.11` |
| `Indicate` | `(mobject: 'Mobject', scale_factor: 'float' = 1.2, color: 'ParsableManimColor' = ManimColor('#FFFF00'` | `(mobject: 'Mobject', scale_factor: 'float' = 1.2, color: 'ManimColor' = '#FFFF00', rate_func: 'Calla` |
| `Integer` | `(number: 'float' = 0, num_decimal_places: 'int' = 0, **kwargs: 'Any') -> 'None'` | `(number: 'int' = 0, num_decimal_places: 'int' = 0, **kwargs)` |
| `IntegerMatrix` | `(matrix: 'Iterable[Iterable[Any]]', element_to_mobject: 'type[VMobject] | Callable[..., VMobject]' =` | `(matrix: 'FloatMatrixType', num_decimal_places: 'int' = 0, decimal_config: 'dict' = {}, **config)` |
| `Intersection` | `(*vmobjects: 'VMobject', **kwargs: 'Any') -> 'None'` | `(*vmobjects: 'VMobject', **kwargs)` |
| `LaggedStart` | `(*animations: 'Animation', lag_ratio: 'float' = 0.05, **kwargs: 'Any')` | `(*animations, lag_ratio: 'float' = 0.05, **kwargs)` |
| `LaggedStartMap` | `(animation_class: 'type[Animation]', mobject: 'Mobject', arg_creator: 'Callable[[Mobject], Iterable[` | `(anim_func: 'Callable[[Mobject], Animation]', group: 'Mobject', run_time: 'float' = 2.0, lag_ratio: ` |
| `Line` | `(start: 'Point3DLike | Mobject' = array([-1.,  0.,  0.]), end: 'Point3DLike | Mobject' = array([1., ` | `(start: 'Vect3 | Mobject' = array([-1.,  0.,  0.]), end: 'Vect3 | Mobject' = array([1., 0., 0.]), bu` |
| `Line3D` | `(start: 'Point3DLike' = array([-1.,  0.,  0.]), end: 'Point3DLike' = array([1., 0., 0.]), thickness:` | `(start: 'Vect3', end: 'Vect3', width: 'float' = 0.05, resolution: 'Tuple[int, int]' = (21, 25), **kw` |

_… e mais 73. Veja `api/*-index.tsv` para a lista completa._

