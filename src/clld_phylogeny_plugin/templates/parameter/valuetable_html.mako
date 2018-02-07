<%! from clld.db.meta import DBSession %>
<%! from clld.db.models.common import Value %>

% if ctx.description:
    <small>
        <i>
            ${ctx.description}
        </i>
    </small>
% endif

% if ctx.domain:
<table class="table table-condensed">
    % for de in ctx.domain:
        <tr>
            <td>${h.map_marker_img(req, de, height=12, width=12)}</td>
            <td>${de.number}</td>
            <td>${de}</td>
            <td class="right">${DBSession.query(Value).filter(Value.domainelement_pk == de.pk).count()}</td>
        </tr>
    % endfor
</table>
% endif