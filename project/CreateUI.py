import tkinter
from tkinter.constants import FLAT, W, N, S, E, SINGLE

from ConfigParser import WindowConfig
from ButtonCommands import SetSelected, RemoveSelected, SelectAll, ClearAll, \
    Generate


class CreateWindow(object):

    def __init__(self):
        self.window_settings = WindowConfig().read_config()
        self.window = None

    def configure_window(self):
        """
        Sets up the initial window.
        :return:
        """
        self.window = tkinter.Tk()
        self.window.title(self.window_settings["window-title"])

        self.window.configure(
                background=self.window_settings["background-colour"])

        self.window.geometry("{}".format(self.window_settings["window-size"]))
        return self.window


class CreateUIElements(object):

    def __init__(self, window_frame):
        self.window_frame = window_frame
        self.element_settings = WindowConfig().read_config()

    def configure_elements(self):
        """
        Adds all of the elements to the window frame.
        Each element is stored as a separate function so they can be edited
        as needed.
        :return:
        """
        self._client_id_input()
        self._provider_select()
        self._plan_list()
        self._generate_button()

    def _client_id_input(self):
        """
        Sets up the Client ID textfield input.
        :return:
        """
        self.indigo_id_label = tkinter.Label(
                self.window_frame,
                text=self.element_settings["client-id-input"])

        self.indigo_id_label.configure(
                background=self.element_settings["background-colour"],
                fg=self.element_settings["text-colour"],
                font=self.element_settings["font"],
                padx=self.element_settings["x-padding"],
                pady=self.element_settings["y-padding"])

        self.indigo_id_input = tkinter.Entry(self.window_frame)
        self.indigo_id_input.configure(
                relief=FLAT,
                font=self.element_settings["font"])

        self.indigo_id_label.grid(row=1, column=0, sticky=W,
                                  padx=self.element_settings["x-padding"],
                                  pady=self.element_settings["y-padding"])
        self.indigo_id_input.grid(row=1, column=1, sticky=W,
                                  padx=self.element_settings["x-padding"],
                                  pady=self.element_settings["y-padding"])

    def _list_box_create_and_config(self, label_text):
        # LABEL
        self.section_label = tkinter.Label(self.window_frame, text=label_text)

        self.section_label.configure(
                background=self.element_settings["background-colour"],
                fg=self.element_settings["text-colour"],
                font=self.element_settings["font"])

        # SECTION LIST
        self.section_list = tkinter.Listbox(self.window_frame)
        self.section_list.configure(
                relief=FLAT, selectmode=SINGLE,
                font=self.element_settings["font"],
                selectbackground=self.element_settings["accent-colour"])

        # SCROLLBAR
        self.scrollbar = tkinter.Scrollbar(self.window_frame)
        self.scrollbar.configure(
                command=self.section_list.yview,
                bg=self.element_settings["secondary-colour"],
                activebackground=self.element_settings["accent-colour"],
                troughcolor=self.element_settings["secondary-colour"])

        # CURRENTLY SELECTED LIST
        self.selected_items = tkinter.Listbox(self.window_frame)
        self.selected_items.configure(
                relief=FLAT, selectmode=SINGLE, width=40,
                font=self.element_settings["font"],
                selectbackground=self.element_settings["accent-colour"])

        self.selected_scrollbar = tkinter.Scrollbar(self.window_frame)
        self.selected_scrollbar.configure(
                command=self.selected_items.yview,
                bg=self.element_settings["secondary-colour"],
                activebackground=self.element_settings["accent-colour"],
                troughcolor=self.element_settings["secondary-colour"]
        )

        # SELECT ALL BUTTON
        self.select_all_btn = tkinter.Button(
                self.window_frame,
                text=self.element_settings["select-all-button"])

        self.select_all_btn.configure(
                background=self.element_settings["accent-colour"],
                fg=self.element_settings["text-colour"],
                font=self.element_settings["font"],
                activebackground=self.element_settings["text-colour"],
                activeforeground=self.element_settings["accent-colour"],
                relief=FLAT, padx=self.element_settings["x-padding"],
                pady=self.element_settings["y-padding"])

        # MOVE TO SELECTED BUTTON
        self.move_to_selected = tkinter.Button(
                self.window_frame,
                text=self.element_settings["move-selection"])

        self.move_to_selected.configure(
                background=self.element_settings["accent-colour"],
                fg=self.element_settings["text-colour"],
                font=self.element_settings["font"],
                activebackground=self.element_settings["text-colour"],
                activeforeground=self.element_settings["accent-colour"],
                relief=FLAT, padx=self.element_settings["x-padding"],
                pady=self.element_settings["y-padding"])

        # REMOVE FROM SELECTED BUTTON
        self.remove_from_selected = tkinter.Button(
                self.window_frame,
                text=self.element_settings["remove-selection"])

        self.remove_from_selected.configure(
                background=self.element_settings["accent-colour"],
                fg=self.element_settings["text-colour"],
                font=self.element_settings["font"],
                activebackground=self.element_settings["text-colour"],
                activeforeground=self.element_settings["accent-colour"],
                relief=FLAT, padx=self.element_settings["x-padding"],
                pady=self.element_settings["y-padding"])

        # CLEAR BUTTON
        self.clear_selected_btn = tkinter.Button(
                self.window_frame,
                text=self.element_settings["clear-button"])

        self.clear_selected_btn.configure(
                background=self.element_settings["accent-colour"],
                fg=self.element_settings["text-colour"],
                font=self.element_settings["font"],
                activebackground=self.element_settings["text-colour"],
                activeforeground=self.element_settings["accent-colour"],
                relief=FLAT, padx=self.element_settings["x-padding"],
                pady=self.element_settings["y-padding"])

        # ADD SEARCH BAR
        # Text entry to search for provider
        self.search_bar = tkinter.Entry(self.window_frame)
        self.search_bar.configure(relief=FLAT,
                                  font=self.element_settings["font"])

        # ADD SEARCH BUTTON - Magnifying glass icon
        # Re-add items to list based on contents of search bar
        # If search bar text is empty or single space redisplay all

        return {"og_list": self.section_list,
                "new_list": self.selected_items,
                "move": self.move_to_selected,
                "remove": self.remove_from_selected,
                "clear": self.clear_selected_btn,
                "all": self.select_all_btn}

    def _arrange_list_box_grid(self, root_column, root_row):
        # LABEL
        self.section_label.grid(row=root_row, column=root_column, sticky=W,
                                padx=self.element_settings["x-padding"],
                                pady=self.element_settings["y-padding"])

        """
        Commented out until there is definite time for the search
        functionality to be implemented.
        # SEARCH BAR
        self.search_bar.grid(row=root_row, column=root_column + 1,
                             padx=self.element_settings["x-padding"],
                             pady=self.element_settings["y-padding"])
        """

        # BUTTONS DOWN THE MIDDLE
        btn_off = root_column + 3
        self.select_all_btn.grid(row=root_row + 1, column=btn_off,
                                 sticky=N+S+E+W,
                                 padx=self.element_settings["x-padding"],
                                 pady=self.element_settings["y-padding"])

        self.move_to_selected.grid(row=root_row + 2, column=btn_off,
                                   sticky=N+S+E+W,
                                   padx=self.element_settings["x-padding"],
                                   pady=self.element_settings["y-padding"])

        self.remove_from_selected.grid(row=root_row + 3, column=btn_off,
                                       sticky=N+S+E+W,
                                       padx=self.element_settings["x-padding"],
                                       pady=self.element_settings["y-padding"])

        self.clear_selected_btn.grid(row=root_row + 4, column=btn_off,
                                     sticky=N+S+E+W,
                                     padx=self.element_settings["x-padding"],
                                     pady=self.element_settings["y-padding"])

        # OPTIONS LIST BOX
        self.section_list.grid(row=root_row + 1, column=root_column,
                               columnspan=3, rowspan=4, sticky=N+S+E+W,
                               padx=self.element_settings["x-padding"],
                               pady=self.element_settings["y-padding"])

        self.scrollbar.grid(row=root_row + 1, column=root_column + 2,
                            rowspan=4, sticky=N+S,
                            padx=self.element_settings["x-padding"],
                            pady=self.element_settings["y-padding"])

        # CURRENTLY SELECTED LISTBOX
        self.selected_items.grid(row=root_row + 1, column=btn_off + 1,
                                 columnspan=4, rowspan=4, sticky=N+S+E+W,
                                 padx=self.element_settings["x-padding"],
                                 pady=self.element_settings["y-padding"])

        self.selected_scrollbar.grid(row=root_row + 1, column=btn_off + 4,
                                     rowspan=4, sticky=N+S+E+W,
                                     padx=self.element_settings["x-padding"],
                                     pady=self.element_settings["y-padding"])

    def _provider_select(self):
        """
        Create the provider select list and add the options from the config
        file.
        :return:
        """
        # CREATE ELEMENTS
        provider_el = self._list_box_create_and_config(
                label_text=self.element_settings["provider-list"])

        # DRAW ELEMENTS
        self._arrange_list_box_grid(root_column=0, root_row=2)

        # ADD ENTRIES TO PROVIDER LIST
        SelectAll(new_list=provider_el["og_list"]).add_providers_to_list()

        # SET MOVE TO SELECTED BOX COMMAND
        provider_el["move"].configure(
                command=lambda: SetSelected(
                        og_list=provider_el["og_list"],
                        new_list=provider_el["new_list"],
                        selected_items=provider_el["og_list"].get(
                                provider_el["og_list"].curselection())
                ).add_to_new_list())

        # SET REMOVE FROM SELECTED BOX COMMAND
        provider_el["remove"].configure(
                command=lambda: RemoveSelected(
                        og_list=provider_el["new_list"],
                        new_list=provider_el["og_list"],
                        selected_items=provider_el["new_list"].get(
                                provider_el["new_list"].curselection())
                ).add_to_new_list())

        # SET CLEAR BUTTON COMMAND
        provider_el["clear"].configure(
            command=lambda: ClearAll(
                    new_list=provider_el["new_list"],
                    og_list=provider_el["og_list"]).providers()
        )

        # SET SELECT ALL BUTTON COMMAND
        provider_el["all"].configure(
            command=lambda: SelectAll(new_list=provider_el["new_list"]
                                      ).add_providers_to_list()
        )
        self.selected_providers = provider_el["new_list"]

    def _plan_list(self):
        """
        Create the plan select list and add the options.
        :return:
        """
        # CREATE ELEMENTS
        plan_el = self._list_box_create_and_config(
                label_text=self.element_settings["plan-list"])

        # DRAW ELEMENTS
        self._arrange_list_box_grid(root_column=0, root_row=8)

        # ADD ENTRIES TO PLAN LIST
        SelectAll(new_list=plan_el["og_list"]).add_plans_to_list()

        # SET MOVE TO SELECTED BOX COMMAND
        plan_el["move"].configure(
                command=lambda: SetSelected(
                        og_list=plan_el["og_list"],
                        new_list=plan_el["new_list"],
                        selected_items=plan_el["og_list"].get(
                                plan_el["og_list"].curselection())
                ).add_to_new_list())

        # SET REMOVE FROM SELECTED BOX COMMAND
        plan_el["remove"].configure(
                command=lambda: SetSelected(
                        og_list=plan_el["new_list"],
                        new_list=plan_el["og_list"],
                        selected_items=plan_el["new_list"].get(
                                plan_el["new_list"].curselection())
                ).add_to_new_list())

        # SET CLEAR BUTTON COMMAND
        plan_el["clear"].configure(
            command=lambda: ClearAll(
                    new_list=plan_el["new_list"],
                    og_list=plan_el["og_list"]).plans()
        )

        # SET SELECT ALL BUTTON COMMAND
        plan_el["all"].configure(
            command=lambda: SelectAll(new_list=plan_el["new_list"]
                                      ).add_plans_to_list()
        )
        self.selected_plans = plan_el["new_list"]

    def _generate_button(self):
        self.generate_btn = tkinter.Button(
                self.window_frame,
                text=self.element_settings["generate-button"])

        self.generate_btn.configure(
                background=self.element_settings["accent-colour"],
                fg=self.element_settings["text-colour"],
                font=self.element_settings["font"],
                activebackground=self.element_settings["text-colour"],
                activeforeground=self.element_settings["accent-colour"],
                relief=FLAT,
                command=lambda: Generate(
                        client_id=self.indigo_id_input,
                        plan_list=self.selected_plans,
                        provider_list=self.selected_providers).create_csv())

        self.generate_btn.grid(column=7, row=13, sticky=N+S+E+W,
                               padx=self.element_settings["x-padding"],
                               pady=self.element_settings["y-padding"])


class DisplayApp(object):

    def __init__(self, app_window):
        self.app_window = app_window

    def show(self):
        self.app_window.mainloop()

if __name__ == "__main__":
    window = CreateWindow().configure_window()
    CreateUIElements(window).configure_elements()
    DisplayApp(window).show()
