<%! from clld.web.util.helpers import JSNamespace %>

<svg id="${obj.eid}" style="width: 100%; margin-top: 20px; margin-left: 1em;"></svg>
<script>
    $(window).load(function() {
            ${JSNamespace('CLLD_PHYLOGENY_PLUGIN').tree(obj.eid, obj.newick, obj.labelSpec, obj.options)|n};
    });
</script>
