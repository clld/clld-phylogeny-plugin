CLLD_PHYLOGENY_PLUGIN = {};


CLLD_PHYLOGENY_PLUGIN.marker = function (container, spec, offset) {
    var marker, tt, close;
    if (!spec) {
        return;
    }
    if (spec.shape === 'c') {
        marker = container.append("circle")
            .attr("cx", offset * 12)
            .attr("height", 12)
            .attr("width", 12)
            .attr("r", 5)
    } else if (spec.shape === 's') {
        marker = container.append("rect")
            .attr("height", 10)
            .attr("width", 10)
            .attr("x", offset * 13 - 6)
            .attr("y", -5)
    } else {
        return
    }
    marker
        .style("fill", spec.color)
        .attr("id", 'm-' + spec.eid);
    if (spec.conflict) {
        marker.style("stroke", "#f00")
            .style("stroke-width", "2.5");

    } else {
        marker.style("stroke", "#222")
            .style("stroke-width", "0.5");
    }
    if (spec.tooltip) {
        close = '<button style="float: right;" onclick="$(\'#' + spec.eid + '\').clickover(\'toggle\');">Close</button>';
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
                        'content': spec.tooltip + close});
                    tt.clickover('show');
                }
            });
    }
};

CLLD_PHYLOGENY_PLUGIN.nodeStyler = function (labelSpec) {
    return function (container, node) {
        var text, current, offset = ' ';
        if (d3.layout.phylotree.is_leafnode(node)) {
            text = container.select("text");
            current = text.text();
            if (!current.endsWith(' ')) {
                if (labelSpec.hasOwnProperty(current)) {
                    text.attr("fill", "red");
                    for (i = 0; i < labelSpec[current].length; i++) {
                        CLLD_PHYLOGENY_PLUGIN.marker(container, labelSpec[current][i], i);
                        offset += '   ';
                    }
                }
                text.text(offset + current + ' ');
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
