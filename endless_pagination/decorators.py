from endless_pagination.settings import PAGE_LABEL, TEMPLATE_VARNAME

def page_template(template, key=PAGE_LABEL):
    """
    Decorate a view that takes a *template* and *extra_context* keyword
    arguments (like generic views).
    The template is switched to *page_template* if request is ajax and
    if *querystring_key* variable passed by the request equals to *key*.
    This allows multiple ajax paginations in the same page.
    The name of the page template is given as *page_template* in the
    extra context.
    """
    def decorator(view):
        # decorator with arguments wrap      
        def decorated(request, *args, **kwargs):
            # trust the developer: he wrote context.update(extra_context) in his view
            extra_context = kwargs.setdefault("extra_context", {})
            extra_context['page_template'] = template
            # switch template on ajax requests
            querystring_key = request.REQUEST.get("querystring_key")
            if request.is_ajax() and querystring_key == key:
                kwargs[TEMPLATE_VARNAME] = template
            return view(request, *args, **kwargs)
        return decorated
    return decorator
    
def page_templates(mapping):
    """
    Like the *page_template* decorator but manage multiple paginations.
    You can map multiple templates to querystring_keys using the *mapping*
    dict, e.g.::
    
        @page_templates({"page_contents1.html": None, 
            "page_contents2.html": "go_to_page"})
        def myview(request):
            ...
    
    When the value of the dict is None then the default querystring_key
    (defined in settings) is used.
    You can use this decorator instead of chaining multiple *page_template*
    calls.
    """
    templates = dict((v or PAGE_LABEL, k) for k, v in mapping.items())
    def decorator(view):
        # decorator with arguments wrap      
        def decorated(request, *args, **kwargs):
            # trust the developer: he wrote context.update(extra_context) in his view
            extra_context = kwargs.setdefault("extra_context", {})
            querystring_key = request.REQUEST.get("querystring_key")
            template = templates.get(querystring_key)
            extra_context['page_template'] = template
            # switch template on ajax requests
            if request.is_ajax() and template:
                kwargs[TEMPLATE_VARNAME] = template
            return view(request, *args, **kwargs)
        return decorated
    return decorator
