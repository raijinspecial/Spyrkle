from . import utils

class Abstract_Page(object):
    """docstring for Page"""
    def __init__(self, notebook, name): # notebook here is BOOK, an object that represents the main page and is inputted as an argument when creating 'notes' object of type Notes
        super(Abstract_Page, self).__init__()
        self.notebook = notebook
        self.name = name
        self.static_urls = set()
        self.libs_urls = set()
        
        self.notebook.add_page(self) # run 'BOOK.add_page', a method in object BOOK, create a sub-page under notebook BOOK, putting in itself (object notes) as an argument.
        self.css_rules = {}
        # self.js_scripts = {}
        self.reset_css()

    def has_css(self) :
        return len(self.css_rules) > 0

    def register_static(self, url) :
        self.static_urls.add(url) 
    
    def register_lib(self, url) :
        self.lib_urls.add(url)

    def clear_css(self) :
        self.css_rules = {}

    def set_css_rule(self, name, lst) :
        self.css_rules[name] = lst

    def reset_css(self) :
        pass

    def get_css(self) :
        res = []
        for n, rules in self.css_rules.items() :
            str_rules = '; '.join(rules)
            res.append( "%s {%s} " % (n, str_rules) ) ;
        return '\n'.join(res)

    def get_html(self) :
        raise NotImplemented("Must be implemented in child")

class Notes(Abstract_Page): # creates an object "notes" of type Notes, notes = pages.Notes(BOOK, "Notes on life"), BOOK is the input for argument notebook
    """docstring for Notes"""
    def __init__(self, notebook, name):
        super(Notes, self).__init__(notebook, name) # the usage of BOOK object is shown in Abstract_Page
        self.notes_html = []

    def add_note_html(self, html, static_urls=[], lib_urls=[]) :
        self.notes_html.append(html)
        
        for e in static_urls :
            self.register_static(e)

        for e in static_libs :
            self.register_static(e)

    def add_note(self, title, body, img_src=None, code=None, add_line_reference=True) :

        if add_line_reference :
            import traceback
            try:
                raise TypeError("Oups!")
            except Exception as err:
                line_data = "<div class='uk-text-meta'>{filename}: {line}</div>".format(filename=traceback.extract_stack()[0].filename, line=traceback.extract_stack()[0].lineno)
        else :
            line_data = ""

        if img_src :    
            img = """
            <div class="uk-card-media-bottom">
                <img src="{img_src}" alt="">
            </div>
            """.format(img_src = img_src)
        else :
            img = ""

        if code :
            lines = code.splitlines()
            l0 = None
            for l in lines :
                if len(l) != 0 :
                    l0 = l 
                    break

            if not l0 :
                code=""
            else :
                indent = len(l0) - len(l0.strip()) 
                strip_lines = [ l[indent:] for l in lines ]
                code = "<pre class='uk-text-left'>%s</pre>" % '\n'.join(strip_lines)
        else :
            code = ""

        html = """
        <div class="uk-card uk-card-default">
            <div class="uk-card-body">
                <h3 class="uk-card-title">{title}</h3>
                {line}
                <p>{body}</p>
            </div>
            {code}
            {img}
        </div>
        """.format(line=line_data, title=title, body=body, code=code, img=img)
        self.notes_html.append(html)

    def add_bullet_points_note(self, title, points, img_src=None, add_line_reference=True) :
        
        if add_line_reference :
            import traceback
            try:
                raise TypeError("Oups!")
            except Exception as err:
                line_data = "<div class='uk-text-meta'>{filename}: {line}</div>".format(filename=traceback.extract_stack()[0].filename, line=traceback.extract_stack()[0].lineno)
        else :
            line_data = ""

        
        if img_src :    
            img = """
            <div class="uk-card-media-bottom">
                <img src="{img_src}" alt="">
            </div>
            """.format(img_src = img_src)
        else :
            img = ""
       
        lis = "<li>"+"</li><li>".join(points)+"</li>"

        html = """
        <div class="uk-card uk-card-default">
            <div class="uk-card-body">
                <h3 class="uk-card-title">{title}</h3>
                {line}
                <ul class="uk-list uk-list-bullet">{lis}</ul>
            </div>
            {img}
        </div>
        """.format(line=line_data, title=title, lis=lis, img=img)
        self.notes_html.append(html)

    def get_html(self) :
        html="""
        <div class="uk-grid uk-child-width-1-3@m uk-child-width-1-1@s uk-text-center" uk-grid >
        {notes}
        </div>
        """.format(notes = "\n".join(self.notes_html))
        return html

class Articles(Abstract_Page):
    """docstring for Notes"""
    def __init__(self, notebook, name):
        super(Articles, self).__init__(notebook, name)
        self.article_html = [] # article_html contains a list of html

    def add_article(self, title, abstract, body) :#, image) :
        im = Image(image)
        html = """
            <h1 class="uk-article-title"><a class="uk-link-reset" href="">{title}</a></h1>
            <p class="uk-text-lead">{abstract}</p>
            <p> {body} </p>
        """.format(title = title, abstract = abstract, body = body)#, src = im.get_src(self.notebook.static_folder))
        self.article_html.append(html) # each add_ functions append a new html into the _html list.

### Making page from txt file ###
    def add_from_doc(self, txtfile) :
        txt = utils.Text(txtfile)
        txt.set_content()
        html = """
            <h1 class="uk-article-title"><a class="uk-link-reset" href="">{title}</a></h1>
            <p class="uk-text-lead">{abstract}</p>
            <div> {body} </div>
        """.format(title = txt.get_title(), abstract = txt.get_abstract(), body = txt.get_body())
        self.article_html.append(html)

    def get_html(self) : # function called by 
        html="""
        <article class="uk-article">
        {notes}
        </article>
        """.format(notes = "\n".join(self.article_html))
        return html

class Figures(Abstract_Page):
    """docstring for Figures"""
    def __init__(self, notebook, name, save_folder = "temp_figs", final_folder = "figs"):
        import os
        super(Figures, self).__init__(notebook, name)
        #self.figure_path = os.path.join(".", notebook.name.replace(" ", "_").lower(), "figs")
        #self.html_path = os.path.join(".", "figs")
        self.figure_path = "/".join([".", notebook.name.replace(" ", "_").lower(), save_folder])
        self.html_path = "/".join([".", final_folder])

        self.files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(self.figure_path):
            for file in f:
                if '.png' in file:
                    self.files.append(file)
        self.files = [os.path.join(self.html_path, s) for s in self.files]

    def get_html(self) :
        fig_html = []
        for i in self.files:
            html="""
            <img src="{img}" alt="" uk-img>
            """.format(img = i)
            fig_html.append(html)
        html_final = """
        {img}
        """.format(img = "\n".join(fig_html))
        return(html_final)
