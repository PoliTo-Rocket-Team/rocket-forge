import tkinter
from typing import Optional, Union, Tuple
from customtkinter import CTkEntry
from customtkinter import CTkCanvas
from customtkinter.windows.widgets.theme               import ThemeManager
from customtkinter.windows.widgets.core_rendering      import DrawEngine
from customtkinter.windows.widgets.font                import CTkFont
from customtkinter.windows.widgets.theme               import ThemeManager
from customtkinter.windows.widgets.utility             import pop_from_dict_by_set, check_kwargs_empty


class CTkEntryUpdated(CTkEntry):
    def __init__(self,
                 master: any,
                 width: int = 140,
                 height: int = 28,
                 corner_radius: Optional[int] = None,
                 border_width: Optional[int] = None,
                 max_length: Optional[int] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 placeholder_text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 textvariable: Union[tkinter.Variable, None] = None,
                 placeholder_text: Union[str, None] = None,
                 font: Optional[Union[tuple, CTkFont]] = None,
                 state: str = tkinter.NORMAL,
                 **kwargs):
        # transfer basic functionality (bg_color, size, appearance_mode, scaling) to CTkBaseClass
        super().__init__(master=master, bg_color=bg_color, width=width, height=height)
        # configure grid system (1x1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # color
        self._fg_color = ThemeManager.theme["CTkEntry"]["fg_color"] if fg_color is None else self._check_color_type(fg_color, transparency=True)
        self._text_color = ThemeManager.theme["CTkEntry"]["text_color"] if text_color is None else self._check_color_type(text_color)
        self._placeholder_text_color = ThemeManager.theme["CTkEntry"]["placeholder_text_color"] if placeholder_text_color is None else self._check_color_type(placeholder_text_color)
        self._border_color = ThemeManager.theme["CTkEntry"]["border_color"] if border_color is None else self._check_color_type(border_color)
        # shape
        self._corner_radius = ThemeManager.theme["CTkEntry"]["corner_radius"] if corner_radius is None else corner_radius
        self._border_width = ThemeManager.theme["CTkEntry"]["border_width"] if border_width is None else border_width
        # text and state
        self._is_focused: bool = True
        self._placeholder_text = placeholder_text
        self._placeholder_text_active = False
        self._pre_placeholder_arguments = {}  # some set arguments of the entry will be changed for placeholder and then set back
        self._textvariable = textvariable
        self._state = state
        self._max_length = max_length
        self._textvariable_callback_name: str = ""

        # font
        self._font = CTkFont() if font is None else self._check_font_type(font)
        if isinstance(self._font, CTkFont):
            self._font.add_size_configure_callback(self._update_font)
        if not (self._textvariable is None or self._textvariable == ""):
            self._textvariable_callback_name = self._textvariable.trace_add("write", self._textvariable_callback)
        self._canvas = CTkCanvas(master=self,
                                 highlightthickness=0,
                                 width=self._apply_widget_scaling(self._current_width),
                                 height=self._apply_widget_scaling(self._current_height))
        self._draw_engine = DrawEngine(self._canvas)
        self._entry = tkinter.Entry(master=self,
                                    bd=0,
                                    width=1,
                                    highlightthickness=0,
                                    font=self._apply_font_scaling(self._font),
                                    state=self._state,
                                    textvariable=self._textvariable,
                                    **pop_from_dict_by_set(kwargs, self._valid_tk_entry_attributes))


        if self._max_length != None:
            self._entry.bind("<KeyPress>", self._enforce_max_length)

        check_kwargs_empty(kwargs, raise_error=True)

        self._create_grid()
        self._activate_placeholder()
        self._create_bindings()
        self._draw()
    
    def configure(self, require_redraw=False, **kwargs):
        if "state" in kwargs:
            self._state = kwargs.pop("state")
            self._entry.configure(state=self._state)

        if "max_length" in kwargs:
            self._max_length = kwargs.pop("max_length")

        if "fg_color" in kwargs:
            self._fg_color = self._check_color_type(kwargs.pop("fg_color"))
            require_redraw = True
        if "text_color" in kwargs:
            self._text_color = self._check_color_type(kwargs.pop("text_color"))
            require_redraw = True
        if "placeholder_text_color" in kwargs:
            self._placeholder_text_color = self._check_color_type(kwargs.pop("placeholder_text_color"))
            require_redraw = True
        if "border_color" in kwargs:
            self._border_color = self._check_color_type(kwargs.pop("border_color"))
            require_redraw = True
        if "border_width" in kwargs:
            self._border_width = kwargs.pop("border_width")
            self._create_grid()
            require_redraw = True
        if "corner_radius" in kwargs:
            self._corner_radius = kwargs.pop("corner_radius")
            self._create_grid()
            require_redraw = True
        if "placeholder_text" in kwargs:
            self._placeholder_text = kwargs.pop("placeholder_text")
            if self._placeholder_text_active:
                self._entry.delete(0, tkinter.END)
                self._entry.insert(0, self._placeholder_text)
            else:
                self._activate_placeholder()
        if "textvariable" in kwargs:
            self._textvariable = kwargs.pop("textvariable")
            self._entry.configure(textvariable=self._textvariable)
        if "font" in kwargs:
            if isinstance(self._font, CTkFont):
                self._font.remove_size_configure_callback(self._update_font)
            self._font = self._check_font_type(kwargs.pop("font"))
            if isinstance(self._font, CTkFont):
                self._font.add_size_configure_callback(self._update_font)
            self._update_font()
        if "show" in kwargs:
            if self._placeholder_text_active:
                self._pre_placeholder_arguments["show"] = kwargs.pop("show")  # remember show argument for when placeholder gets deactivated
            else:
                self._entry.configure(show=kwargs.pop("show"))
        self._entry.configure(**pop_from_dict_by_set(kwargs, self._valid_tk_entry_attributes))  # configure Tkinter.Entry
        super().configure(require_redraw=require_redraw, **kwargs)  # configure CTkBaseClass
    
    
    def _enforce_max_length(self, event=None):
        entry_text = self.get()
        if len(entry_text) >= self._max_length:
            entry_text = entry_text[:self._max_length]
            self.delete(0, "end")
            self.insert(0, entry_text)