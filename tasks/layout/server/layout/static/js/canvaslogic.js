"use strict";
var text = new PointText(view.center);
text.content = top_text;
text.point.y = 35;
text.style = {
    fontFamily: 'Helvetica',
    fontWeight: 'bold',
    fontSize: 30,
    fillColor: 'Black',
    justification: 'center'
};

var desk_w = 60;
var desk_h = 50;
var desk_vd = 35;
var desk_hd_1 = 10;
var desk_hd_2 = 80;
var desk_r = 10;
var desks_group = new Group();
var desk_default_color = "burlywood";


for (var i = 0; i < 3; i++) {
    for (var j = 0; j < 5; j++) {
        var desk_a_rect = new Rectangle(new Point(i * (desk_w + desk_hd_1 + desk_w + desk_hd_2), j * (desk_h + desk_vd)),
            new Point(i * (desk_w + desk_hd_1 + desk_w + desk_hd_2) + desk_w, j * (desk_h + desk_vd) + desk_h));
        var radius = new Size(desk_r, desk_r);
        var desk_a_path = new Path.Rectangle(desk_a_rect, radius);
        desk_a_path.num = (j * 3 + i) * 2;
        desks_group.addChild(desk_a_path);

        var desk_b_rect = new Rectangle(new Point(i * (desk_w + desk_hd_1 + desk_w + desk_hd_2) + desk_w + desk_hd_1, j * (desk_h + desk_vd)),
            new Point(i * (desk_w + desk_hd_1 + desk_w + desk_hd_2) + desk_w + desk_hd_1 + desk_w, j * (desk_h + desk_vd) + desk_h));
        var desk_b_path = new Path.Rectangle(desk_b_rect, radius);
        desk_b_path.num = (j * 3 + i) * 2 + 1;
        desks_group.addChild(desk_b_path);
    }
}

desks_group.fillColor = desk_default_color;

// for(var i in desks_group.children) { // debug
//     desks_group.children[i].onClick = function(event) {
//         console.log(this.num, this.occupied.lastChild.content);
//     }
// }

desks_group.bounds.center = view.center;

var texts_group = new Group();
var text_vd = 40;
var text_hd = 40;
var text_row_count = 10;


for (var i = 0; i < student_count; i++) {
    var cur_text_group = new Group();
    var text_point = new Point(i % text_row_count * text_hd, Math.floor(i / text_row_count) * text_vd);
    var text = new PointText(text_point);
    text.content = String(i);
    text.style = {
        fontFamily: 'Helvetica',
        fontWeight: 'bold',
        fontSize: 15,
        fillColor: 'Black',
        justification: 'center'
    };
    var rect = new Rectangle(text_point - (new Point(15, 20)), new Size(30, 30));
    var rect_path = new Path.Rectangle(rect);
    rect_path.fillColor = "grey";
    cur_text_group.addChild(rect_path);
    cur_text_group.addChild(text);
    cur_text_group.num = i;
    cur_text_group.to = [];
    cur_text_group.onMouseEnter = function (event) {
        classroom.style.cursor = "grab";
    };
    cur_text_group.onMouseLeave = function (event) {
        classroom.style.cursor = "";
    };
    texts_group.addChild(cur_text_group);
}

texts_group.position = view.center;
texts_group.position += new Point(0, view.size.height/2 - 80);

var lines_group = new Group();

function getStrokeWidth(pnt_from, pnt_to) {
    return Math.min(Math.max((85 - pnt_from.getDistance(pnt_to)) * 3, 1), 50);
}

for (var i in hates) {
    var from = hates[i][0];
    var to = hates[i][1];
    var edge = new Path();
    var pnt_from = texts_group.children[from].position;
    var pnt_to = texts_group.children[to].position;
    edge.add(pnt_from, pnt_to);
    edge.strokeColor = "red";
    edge.strokeWidth = getStrokeWidth(pnt_from, pnt_to);
    texts_group.children[from].to.push([texts_group.children[to], edge]);
    texts_group.children[to].to.push([texts_group.children[from], edge]);
    lines_group.addChild(edge);
}

function recalc_edge(text, j) {
    var edge = text.to[j][1];
    var pnt_from = text.position;
    var pnt_to = text.to[j][0].position;
    edge.firstSegment.point = pnt_from;
    edge.lastSegment.point = pnt_to;
    edge.strokeWidth = getStrokeWidth(pnt_from, pnt_to);
}

function recalc_edges(text) {
    for (var j in text.to) {
        recalc_edge(text, j);
    }
}

function recalc_ok() {
    var bad = false;
    for (var j in texts_group.children) {
        texts_group.children[j].firstChild.fillColor = "grey";
        if (texts_group.children[j].closest === undefined) {
            bad = true;
        }
    }
    for (var j in hates) {
        var from = hates[j][0];
        var to = hates[j][1];
        var text_from = texts_group.children[from];
        var text_to = texts_group.children[to];
        if ((text_from.pos % 2 === 0 && text_to.pos === text_from.pos + 1) ||
            (text_from.pos % 2 === 1 && text_to.pos === text_from.pos - 1)) {
            text_from.firstChild.fillColor = "red";
            text_to.firstChild.fillColor = "red";
            bad = true;
        }
    }
    submit_group.visible = !bad;
}

var main_group = new Group();
main_group.addChild(desks_group);
main_group.addChild(lines_group);
main_group.addChild(texts_group);


for (var i = 0; i < student_count; i++) {
    texts_group.children[i].onMouseDown = function (event) {
        if (this.closest !== undefined) {
            this.closest.occupied = undefined;
            this.last_closest = this.closest;
        }
        this.ismoving = true;
    };
    texts_group.children[i].onMouseDrag = function (event) {
        this.position += event.delta;
        recalc_edges(this);
        if (this.closest !== undefined) {
            if (this.closest.occupied === undefined) {
                this.closest.fillColor = desk_default_color;
            } else {
                this.closest.fillColor = "silver";
            }
        }
        var closest_dist = Infinity;
        for (var j in desks_group.children) {
            var new_closest = desks_group.children[j];
            var new_dist = this.position.getDistance(new_closest.position);
            if (new_dist < closest_dist && (new_closest.occupied === undefined || this.last_closest !== undefined)) {
                closest_dist = new_dist;
                this.closest = new_closest;
                this.pos = new_closest.num;
            }
        }
        this.closest.fillColor = "saddlebrown";
    };
    texts_group.children[i].onMouseUp = function (event) {
        if (this.ismoving) {
            this.ismoving = false;
            this.position = this.closest.position;
            if (this.closest.occupied !== undefined) {
                var other_text = this.closest.occupied;
                other_text.position = this.last_closest.position;
                other_text.closest = this.last_closest;
                other_text.pos = this.last_closest.num;
                this.last_closest.occupied = other_text;
                this.last_closest.fillColor = "silver";
                recalc_edges(this.closest.occupied);
            }
            this.closest.occupied = this;
            recalc_edges(this);
            this.closest.fillColor = "silver";
            recalc_ok();
        }
    }
}

var submit_button = new Path.Rectangle(new Point(-70, -30), new Size(140, 40));
submit_button.fillColor = "dodgerblue";
var submit_text = new PointText(new Point());
submit_text.content = "submit";
submit_text.style = {
    fontFamily: 'Helvetica',
    fontWeight: 'bold',
    fontSize: 30,
    fillColor: 'white',
    justification: 'center'
};

var submit_group = new Group();
submit_group.addChild(submit_button);
submit_group.addChild(submit_text);
submit_group.position = view.center;
submit_group.position += new Point(0, view.size.height/2 - 80);
submit_group.visible = false;

submit_group.onClick = function () {
    var pairs = [];
    for (var i = 0; i < 30; i++) {
        if (i % 2 === 0) {
            pairs.push([]);
        };
        if(desks_group.children[i].occupied !== undefined) {
            pairs[pairs.length - 1].push(desks_group.children[i].occupied.lastChild.content - 0);
        }
    }
    submit(pairs).then(function () {
        window.location.reload();
    }, function (msg) {
        alert(msg);
    })
};