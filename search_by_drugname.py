__author__ = 'animeshk'
from gi.repository import Gtk, Pango
#side_effects_author_count_list = []
#drug_name = ""
alphabet = ["All", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

class SearchDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Search Side Effects by Drug Name", parent,
                            Gtk.DialogFlags.MODAL, buttons=(
                Gtk.STOCK_FIND, Gtk.ResponseType.OK,
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        box = self.get_content_area()

        label = Gtk.Label("Enter drug name you want to search for:")
        box.add(label)

        self.entry = Gtk.Entry()
        box.add(self.entry)

        self.show_all()


class TextViewWindow(Gtk.Window):
    def __init__(self, side_effects_author_count_list, drug_name):
        Gtk.Window.__init__(self, title=drug_name)

        self.set_default_size(900, 550)

        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.create_toolbar()

        #Creating the ListStore model
        self.software_liststore = Gtk.ListStore(str, int)
        for software_ref in side_effects_author_count_list:
            self.software_liststore.append(list(software_ref))
        self.current_filter_language = None

        #Creating the filter, feeding it with the liststore model
        self.language_filter = self.software_liststore.filter_new()
        #setting the filter function, note that we're not using the
        self.language_filter.set_visible_func(self.language_filter_func)

        #creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.language_filter)
        for i, column_title in enumerate(["Side-Effects ", "No. of users reported"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        #creating buttons to filter by programming language, and setting up their events
        self.buttons = list()
        for prog_language in alphabet:
            button = Gtk.Button(prog_language)
            self.buttons.append(button)
            button.connect("clicked", self.on_selection_button_clicked)

        #setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.scrollable_treelist.set_hexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 10, 27, 10)

       # self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)
        self.scrollable_treelist.add(self.treeview)
        self.show_all()

    def language_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if self.current_filter_language is None or self.current_filter_language == "All":
            return True
        else:
            return model[iter][0].upper().startswith(self.current_filter_language)

    def on_selection_button_clicked(self, widget):
        """Called on any of the button clicks"""
        #we set the current language filter to the button's label
        self.current_filter_language = widget.get_label()
        print("%s language selected!" % self.current_filter_language)
        #we update the filter, which updates in turn the view
        self.language_filter.refilter()

    def create_toolbar(self):
        toolbar = Gtk.Toolbar()
        self.grid.attach(toolbar, 0, 0, 1, 1)

        button_search = Gtk.ToolButton.new_from_stock(Gtk.STOCK_FIND)
        button_search.connect("clicked", self.on_search_clicked)
        toolbar.insert(button_search, 0)


    def on_search_clicked(self):
        print "haha"



# win = TextViewWindow()
# win.connect("delete-event", Gtk.main_quit)
# win.show_all()
# Gtk.main()
