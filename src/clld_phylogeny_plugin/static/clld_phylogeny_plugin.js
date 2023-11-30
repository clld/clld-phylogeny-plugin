CLLD_PHYLOGENY_PLUGIN = {};


CLLD_PHYLOGENY_PLUGIN.marker = function (container, spec, offset, marker_align_offset) {
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
    if(marker_align_offset > 0){
      marker.attr('transform', 'translate(' + marker_align_offset.toString() + ', 0)');
    }
    return marker;
};

CLLD_PHYLOGENY_PLUGIN.nodeStyler = function (labelSpec, options) {
    return function (element, data) {
        var text, current, sep;
        var init = false;
        if (d3.phylotree.isLeafNode(data)) {
            var marker_align_offset = 0;
            if (options['align-tips']) {
                var line = element.select("line");
                if (!options['hasBranchLengths']) {
                    line.attr("class", "branch");
                }
                marker_align_offset = parseFloat(line.attr("x2"));
            }
            text = element.select("text");
            text.attr("fill", "red");
            if (!data.data.org) {
                data.data.org = text.text();
                init = true;
            }
            current = data.data.org;
            if (labelSpec.hasOwnProperty(current)) {
                var values = [];
                sep = ' # ';
                for (i = 0; i < labelSpec[current].length; i++) {
                    var lblSpec = labelSpec[current][i];
                    if (element.select('#m-' + lblSpec.eid).size() === 0) {
                        CLLD_PHYLOGENY_PLUGIN.marker(element, lblSpec, i, marker_align_offset);
                    }
                    if (init) {
                        if (i == 0 && lblSpec.hasOwnProperty('tip_title')) {
                            text.text(lblSpec['tip_title']);
                            if (lblSpec.hasOwnProperty('tip_values_sep')) {
                                sep = lblSpec['tip_values_sep'];
                            }
                        }
                        if (lblSpec.hasOwnProperty('tip_values')) {
                            values.push(lblSpec['tip_values']);
                        }
                    }
                }
                if (init) {
                    data.data.name = text.text() + ' ' + values.join(sep);
                }
                text.attr('transform', null)
                    .attr('dx', function(d, i) {
                        return marker_align_offset + 4 + labelSpec[current].length * 12; }
                    );
            }
        }
    }
};

CLLD_PHYLOGENY_PLUGIN.tree = function (eid, newick, labelSpec, options) {
    var container_select_id = '#' + eid;
    var d3_container = d3.select(container_select_id);

    d3.phylotree = new phylotree.phylotree(newick);
    options['hasBranchLengths'] = d3.phylotree.hasBranchLengths();
    options['node-styler'] = CLLD_PHYLOGENY_PLUGIN.nodeStyler(labelSpec, options);
    options['container'] = container_select_id;

    // container should be a DIV - a possible custom legacy SVG container will be replaced by a DIV first
    if (d3_container.node().tagName.toLowerCase() === 'svg') {
        var p = d3_container.node().parentNode;
        var org_style = d3_container.attr('style');
        d3_container.remove();
        d3.select(p).append('div')
            .attr('id', eid)
            .attr('style', org_style)
            .attr('class', 'tree-widget');
    }

    d3_container.node()
        .appendChild(d3.phylotree.render(options).show());
    d3.phylotree.display.update();
};
