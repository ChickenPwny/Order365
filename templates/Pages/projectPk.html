{% extends 'TemplateBase.html' %}
{% load bootstrap5 %}
{% load static %}

{% block content %}

<div class="table-responsive">
    <table class="table table-bordered table-striped" id="sortableTable{{ forloop.counter }}">
        {% if x.children and x.file %}
            <thead>
                <tr>
                    {% for key, value in x.children.0.dataDoct.0.items %}
                        {% if value  %}
                        <th class="sortable" onclick="sortTable({{ forloop.counter0 }}, 'sortableTable{{ forloop.counter }}', {{ forloop.counter0 }})">{{ key }}</th>
                        {% endif %}
                    {% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for Y in x.children %}
                    {% for Z in Y.dataDoct %}
                        {% if Z %}
                            <tr>
                                {% for key, value in Z.items %}
                                    {% if key and value != None  and value|length > 0 %}
                                        <td>{{ value }}</td>
                                    {% endif %}
                                {% endfor %}
                            </tr>
                        {% endif %}
                    {% endfor %}
                {% endfor %}
            </tbody>
        {% endif %}
    </table>
</div>
<script>
function sortTable(n, tableId, column) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById(tableId);
    if (table) {
        switching = true;
        dir = "asc"; 
        while (switching) {
            switching = false;
            rows = table.rows;
            for (i = 1; i < (rows.length - 1); i++) {
                shouldSwitch = false;
                x = rows[i].getElementsByTagName("TD")[column];
                y = rows[i + 1].getElementsByTagName("TD")[column];
                if (x && y) {
                    if (dir == "asc") {
                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    } else if (dir == "desc") {
                        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                }
            }
            if (shouldSwitch) {
                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                switching = true;
                switchcount ++;      
            } else {
                if (switchcount == 0 && dir == "asc") {
                    dir = "desc";
                    switching = true;
                }
            }
        }
    }
}
</script>
</div>
{% endblock %}