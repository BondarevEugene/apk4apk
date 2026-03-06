def build_navigation(sm):

    from pages.page1 import Page1
    from pages.page2 import Page2

    sm.add_widget(Page1(name="page1"))
    sm.add_widget(Page2(name="page2"))