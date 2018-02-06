CLLD_PHYLOGENY_PLUGIN = {};


CLLD_PHYLOGENY_PLUGIN.marker = function (container, spec) {
    var marker, tt;
    if (spec.shape === 'c') {
        marker = container.append("circle")
            .attr("height", 12)
            .attr("width", 12)
            .attr("r", 5)
    } else if (spec.shape === 's') {
        marker = container.append("rect")
            .attr("height", 10)
            .attr("width", 10)
            .attr("x", 1)
            .attr("y", 1)
    } else {
        return
    }
    marker.style("fill", spec.color);
    if (spec.conflict) {
        marker.style("stroke", "#f00")
            .style("stroke-width", "2.5");

    } else {
        marker.style("stroke", "#222")
            .style("stroke-width", "0.5");
    }
    if (spec.tooltip !== undefined) {
        marker
            .on("click", function () {
                tt = $('#' + spec.eid);
                if (tt.length) {
                    tt.clickover('toggle');
                } else {
                    d3.select("body").append("div")
                        .attr("class", "clld-tree-tooltip")
                        .attr("id", spec.eid)
                        .html('')
                        .style("visibility", "hidden")
                        .style("left", (d3.event.pageX) + "px")
                        .style("top", (d3.event.pageY + 4) + "px");
                    tt = $('#' + spec.eid);
                    tt.clickover({
                        'html': true,
                        'placement': 'bottom',
                        'title': spec.tooltip_title || undefined,
                        'content': spec.tooltip});
                    tt.clickover('show');
                }
            });
    }
};


CLLD_PHYLOGENY_PLUGIN.nodeStyler = function (labelSpec) {
    return function (container, node) {
        var text, current;
        if (d3.layout.phylotree.is_leafnode(node)) {
            text = container.select("text");
            current = text.text();
            if (!text.text().endsWith(' ')) {
                text.text('   ' + text.text() + ' ');
                if (labelSpec.hasOwnProperty(current)) {
                    text.attr("fill", "red");
                    CLLD_PHYLOGENY_PLUGIN.marker(container, labelSpec[current]);
                }
            }
        }
    }
};

CLLD_PHYLOGENY_PLUGIN.tree = function (eid, newick, labelSpec, options) {
    var tree = d3.layout.phylotree().svg(d3.select("#" + eid))
        .options(options)
        .style_nodes(CLLD_PHYLOGENY_PLUGIN.nodeStyler(labelSpec));
    tree(newick).layout();
};
