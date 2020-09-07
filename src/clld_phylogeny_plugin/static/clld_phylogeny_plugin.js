CLLD_PHYLOGENY_PLUGIN = {};


CLLD_PHYLOGENY_PLUGIN.marker = function (container, spec, offset) {
    var marker, tt, close;
    if (!spec) {
        return;
    }
    if (spec.shape === 'c') {
        marker = container.append("circle")
            .attr("cx", offset * 12 + 6)
            .attr("height", 12)
            .attr("width", 12)
            .attr("r", 5)
    } else if (spec.shape === 's') {
        marker = container.append("path")
            .attr("height", 12)
            .attr("width", 12)
            .attr("d", "M " + (offset * 12 + 1) + " 0 v -5 h 10 v 10 h -10 z")
    } else if (spec.shape === 'd') {
        marker = container.append("path")
            .attr("height", 12)
            .attr("width", 12)
            .attr("d", "M " + (offset * 12) + " 0 l 6 -6 l 6 6 l -6 6 z")
    } else if (spec.shape === 't') {
        marker = container.append("path")
            .attr("height", 12)
            .attr("width", 12)
            .attr("d", "M " + (offset * 12 + 1) + " 5 l 10 0 l -5 -10 z")
    } else if (spec.shape === 'f') {
        marker = container.append("path")
            .attr("height", 12)
            .attr("width", 12)
            .attr("d", "M " + (offset * 12 + 1) + " -5 l 10 0 l -5 10 z")
    } else {
        return
    }
    marker
        .style("fill", spec.color)
        .attr("id", 'm-' + spec.eid);
    if (spec.conflict) {
        marker.style("stroke", "#f00")
            .style("stroke-width", "2.5");

    } else if (!spec.tooltip) {
        marker.style("stroke", "#fff")
            .style("stroke-width", "0");
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
                        .style("left", (d3.event.pageX + 70) + "px")
                        .style("top", (d3.event.pageY) + "px")
                        .style("position", "absolute");
                    tt = $('#' + spec.eid);
                    tt.clickover({
                        'html': true,
                        'placement': 'right',
                        'title': spec.tooltip_title || undefined,
                        'content': spec.tooltip + close});
                    tt.clickover('show');
                }
            });
    }
    return marker;
};

CLLD_PHYLOGENY_PLUGIN.nodeStyler = function (labelSpec) {
    return function (container, node) {
        var text, current, sep;
        if (d3.layout.phylotree.is_leafnode(node)) {
            text = container.select("text");
            current = text.text();
            if (!current.endsWith(' ')) {
                var values = [];
                if (labelSpec.hasOwnProperty(current)) {
                    text.attr("fill", "red");
                    sep = ' # ';
                    for (i = 0; i < labelSpec[current].length; i++) {
                        CLLD_PHYLOGENY_PLUGIN.marker(container, labelSpec[current][i], i);
                        if (i == 0 && labelSpec[current][i].hasOwnProperty('tip_title')) {
                          text.text(labelSpec[current][i]['tip_title']);
                          if (labelSpec[current][i].hasOwnProperty('tip_values_sep')) {
                            sep = labelSpec[current][i]['tip_values_sep'];
                          }
                        }
                        if (labelSpec[current][i].hasOwnProperty('tip_values')) {
                          values.push(labelSpec[current][i]['tip_values']);
                        }
                    }
                    text.attr("transform", null).attr ("x", function (d, i) { return labelSpec[current].length * 12;});
                }
                text.text(text.text() + ' ' + values.join(sep) + ' ');
            }
        }
    }
};

CLLD_PHYLOGENY_PLUGIN.tree = function (eid, newick, labelSpec, options) {
    var tree = d3.layout.phylotree().svg(d3.select("#" + eid)).options(options);
    tree(newick);
    tree.style_nodes(CLLD_PHYLOGENY_PLUGIN.nodeStyler(labelSpec));
    tree.layout();
};
