<%! from clld.web.util.helpers import JSNamespace %>

% if obj.newick:
    <svg id="${obj.eid}" style="width: 100%; margin-top: 20px; margin-left: 1em;"></svg>
    <script>
        $(window).load(function() {
                ${JSNamespace('CLLD_PHYLOGENY_PLUGIN').tree(obj.eid, obj.newick, obj.labelSpec, obj.options)|n};
        });
    </script>
% elif obj.parameters:
    <div class="alert alert-error">
        No leaf node in this phylogeny is related to a ${_('Language')} coded for
        any of the selected ${_('Parameters')}.
    </div>
% endif
