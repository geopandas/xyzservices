"""
Utilities to support XYZservices
"""
import json
import uuid


class Bunch(dict):
    """A dict with attribute-access"""

    def __getattr__(self, key):
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError(key)

    def __dir__(self):
        return self.keys()

    def _repr_html_(self, inside=False):

        children = ""
        for key in self.keys():
            if isinstance(self[key], TileProvider):
                obj = "xyzservices.TileProvider"
            else:
                obj = "xyzservices.Bunch"
            uid = str(uuid.uuid4())
            children += f"""
            <li class="xyz-child">
                <label for="{uid}">{key} <span>{obj}</span></label>
                <input type="checkbox" id="{uid}" class="xyz-checkbox"/>
                <div style="xyz-inside">
                    {self[key]._repr_html_(inside=True)}
                </div>
            </li>
            """

        style = "" if inside else f"<style>{CSS_STYLE}</style>"
        html = f"""
        <div>
        {style}
            <div class="xyz-wrap">
                <div class="xyz-header">
                    <div class="xyz-obj">xyzservices.Bunch</div>
                    <div class="xyz-name">{len(self)} items</div>
                </div>
                <div class="xyz-details">
                    <ul class="xyz-collapsible">
                        {children}
                    </ul>
                </div>
            </div>
        </div>
        """

        return html


class TileProvider(Bunch):
    """
    A dict with attribute-access and that
    can be called to update keys
    """

    def __call__(self, **kwargs):
        new = TileProvider(self)  # takes a copy preserving the class
        new.update(kwargs)
        return new

    def _repr_html_(self, inside=False):
        provider_info = ""
        for key, val in self.items():
            if key != "name":
                provider_info += f"<dt><span>{key}</span></dt><dd>{val}</dd>"

        style = "" if inside else f"<style>{CSS_STYLE}</style>"
        html = f"""
        <div>
        {style}
            <div class="xyz-wrap">
                <div class="xyz-header">
                    <div class="xyz-obj">xyzservices.TileProvider</div>
                    <div class="xyz-name">{self.name}</div>
                </div>
                <div class="xyz-details">
                    <dl class="xyz-attrs">
                        {provider_info}
                    </dl>
                </div>
            </div>
        </div>
        """

        return html


def _load_json(f):

    data = json.loads(f)

    providers = Bunch()

    for provider_name in data.keys():
        provider = data[provider_name]

        if "url" in provider.keys():
            providers[provider_name] = TileProvider(provider)

        else:
            providers[provider_name] = Bunch(
                {i: TileProvider(provider[i]) for i in provider}
            )

    return providers


CSS_STYLE = """
/* CSS stylesheet for displaying xyzservices objects in Jupyter.*/
.xyz-header {
    padding-top: 6px;
    padding-bottom: 6px;
    margin-bottom: 4px;
    border-bottom: solid 1px #ddd;
}

.xyz-header>div {
    display: inline;
    margin-top: 0;
    margin-bottom: 0;
}

.xyz-obj,
.xyz-name {
    margin-left: 2px;
    margin-right: 10px;
}

.xyz-obj {
    color: #555;
}

.xyz-name {
    color: #000;
}

.xyz-attrs {
    grid-column: 1 / -1;
}

dl.xyz-attrs {
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: 125px auto;
}

.xyz-attrs dt,
dd {
    padding: 0;
    margin: 0;
    float: left;
    padding-right: 10px;
    width: auto;
}

.xyz-attrs dt {
    font-weight: normal;
    grid-column: 1;
}

.xyz-attrs dt:hover span {
    display: inline-block;
    background: #fff;
    padding-right: 10px;
}

.xyz-attrs dd {
    grid-column: 2;
    white-space: pre-wrap;
    word-break: break-all;
}

.xyz-details ul>li>label>span {
    color: #555;
    padding-left: 10px;
}

.xyz-collapsible li>input+* {
    display: none;
}

.xyz-collapsible li>input:checked+* {
    display: block;
}

.xyz-collapsible li>input {
    display: none;
}

.xyz-collapsible>li>label {
    cursor: pointer;
}

.xyz-collapsible>li>label:hover {
    color: #555;
}

ul.xyz-collapsible {
    list-style: none!important;
    padding-left: 20px!important;
}

li.xyz-child:before {
    content: '►';
    font-size: 11px;
}

input:checked+li.xyz-child:before {
    content: '▼';
}

.xyz-wrap {
    margin-bottom: 10px;
}
"""
