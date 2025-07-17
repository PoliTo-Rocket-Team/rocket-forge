import tkinter
import sys
from typing import Union, Tuple, Optional
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
from customtkinter import CTkScrollableFrame
from customtkinter.windows.widgets.ctk_frame       import CTkFrame
from customtkinter.windows.widgets.ctk_scrollbar   import CTkScrollbar
from customtkinter.windows.widgets.appearance_mode import CTkAppearanceModeBaseClass
from customtkinter.windows.widgets.scaling         import CTkScalingBaseClass
from customtkinter.windows.widgets.ctk_label       import CTkLabel
from customtkinter.windows.widgets.font            import CTkFont
from customtkinter.windows.widgets.theme           import ThemeManager


class CTkScrollableFrameUpdated(CTkScrollableFrame):
    def __init__(self,
                 master: any,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: Optional[Union[int, str]] = None,
                 border_width: Optional[Union[int, str]] = None,
                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 scrollbar_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 scrollbar_button_color: Optional[Union[str, Tuple[str, str]]] = None,
                 scrollbar_button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 scrollbar_corner_radius: Optional[Union[int, str]] = None,
                 label_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 label_text_color: Optional[Union[str, Tuple[str, str]]] = None,

                 label_text: str = "",
                 label_font: Optional[Union[tuple, CTkFont]] = None,
                 label_anchor: str = "center",
                 orientation: Literal["vertical", "horizontal"] = "vertical",
                 scrollbar_cursor: str = "hand2"):
        self._orientation = orientation

        # dimensions independent of scaling
        self._desired_width = width  # _desired_width represent desired size set by width
        self._desired_height = height # _desired_height represent desired size set by height

        self._parent_frame = CTkFrame(master=master, width=0, height=0, corner_radius=corner_radius,
                                      border_width=border_width, bg_color=bg_color, fg_color=fg_color, border_color=border_color)
        self._parent_canvas = tkinter.Canvas(master=self._parent_frame, highlightthickness=0)
        self._set_scroll_increments()

        if self._orientation == "horizontal":
            self._scrollbar = CTkScrollbar(master=self._parent_frame, orientation="horizontal", command=self._parent_canvas.xview, width=self._desired_width, cursor=scrollbar_cursor,
                                           corner_radius=scrollbar_corner_radius, fg_color=scrollbar_fg_color, button_color=scrollbar_button_color, button_hover_color=scrollbar_button_hover_color)
            self._parent_canvas.configure(xscrollcommand=self._scrollbar.set)
        elif self._orientation == "vertical":
            self._scrollbar = CTkScrollbar(master=self._parent_frame, orientation="vertical", command=self._parent_canvas.yview, height=self._desired_height, cursor=scrollbar_cursor,
                                           corner_radius=scrollbar_corner_radius, fg_color=scrollbar_fg_color, button_color=scrollbar_button_color, button_hover_color=scrollbar_button_hover_color)
            self._parent_canvas.configure(yscrollcommand=self._scrollbar.set)

        self._label_text = label_text
        self._label = CTkLabel(self._parent_frame, text=label_text, anchor=label_anchor, font=label_font,
                               corner_radius=self._parent_frame.cget("corner_radius"), text_color=label_text_color,
                               fg_color=ThemeManager.theme["CTkScrollableFrame"]["label_fg_color"] if label_fg_color is None else label_fg_color)
        tkinter.Frame.__init__(self, master=self._parent_canvas, highlightthickness=0)
        CTkAppearanceModeBaseClass.__init__(self)
        CTkScalingBaseClass.__init__(self, scaling_type="widget")
        self._create_grid()
        self._parent_canvas.configure(width=self._apply_widget_scaling(self._desired_width),
                                      height=self._apply_widget_scaling(self._desired_height))
        self.bind("<Configure>", lambda e: self._parent_canvas.configure(scrollregion=self._parent_canvas.bbox("all")))
        self._parent_canvas.bind("<Configure>", self._fit_frame_dimensions_to_canvas)
        self.bind_all("<MouseWheel>", self._mouse_wheel_all, add="+")
        self.bind_all("<KeyPress-Shift_L>", self._keyboard_shift_press_all, add="+")
        self.bind_all("<KeyPress-Shift_R>", self._keyboard_shift_press_all, add="+")
        self.bind_all("<KeyRelease-Shift_L>", self._keyboard_shift_release_all, add="+")
        self.bind_all("<KeyRelease-Shift_R>", self._keyboard_shift_release_all, add="+")
        self._create_window_id = self._parent_canvas.create_window(0, 0, window=self, anchor="nw")
        if self._parent_frame.cget("fg_color") == "transparent":
            tkinter.Frame.configure(self, bg=self._apply_appearance_mode(self._parent_frame.cget("bg_color")))
            self._parent_canvas.configure(bg=self._apply_appearance_mode(self._parent_frame.cget("bg_color")))
        else:
            tkinter.Frame.configure(self, bg=self._apply_appearance_mode(self._parent_frame.cget("fg_color")))
            self._parent_canvas.configure(bg=self._apply_appearance_mode(self._parent_frame.cget("fg_color")))
        self._shift_pressed = False