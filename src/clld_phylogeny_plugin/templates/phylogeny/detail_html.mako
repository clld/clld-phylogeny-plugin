<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "phylogenys" %>
<%block name="title">Phylogeny ${ctx.name}</%block>
<%! from clld_phylogeny_plugin.tree import Tree %>
<%! from clld_phylogeny_plugin.interfaces import ITree %>
<% tree = req.registry.queryUtility(ITree)(ctx, req) %>

<%block name="head">
    ${Tree.head(req)|n}
</%block>

<h2>${title()}</h2>

% if ctx.description:
    <div class="alert alert-info">${ctx.description}</div>
% endif

${tree.render()}
