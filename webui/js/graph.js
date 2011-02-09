// JavaScript inheritance helper -- see http://www.ruzee.com/blog/2008/12/javascript-inheritance-via-prototypes-and-closures
(function(){
  var isFn = function(fn) { return typeof fn == "function"; };
  PClass = function(){};
  PClass.create = function(proto) {
    var k = function(magic) { // call init only if there's no magic cookie
      if (magic != isFn && isFn(this.init)) this.init.apply(this, arguments);
    };
    k.prototype = new this(isFn); // use our private method as magic cookie
    for (key in proto) (function(fn, sfn){ // create a closure
      k.prototype[key] = !isFn(fn) || !isFn(sfn) ? fn : // add _super method
        function() { this._super = sfn; return fn.apply(this, arguments); };
    })(proto[key], k.prototype[key]);
    k.prototype.constructor = k;
    k.extend = this.extend || this.create;
    return k;
  };
})();

function simplePlot(f, a, b) {
    this.xmin = a; this.xmax = b;
    this.amin = a; this.amax = b;
    type = calc('type(' + f + ')');
    samples = 500;
    // samples = ((type.match('.*(Sin|Cos|Tan).*') == null) ? 5000 : 500);
    this.addRange(calc('evalbetween(' + f + ',' + a + ',' + b
        + ',' + samples + ')'));
    this.draw();
}

var Plot = PClass.create({
    init: function(id, samples, ranges, functions) {
        this.canvas = document.getElementById(id);
        this.canvas.width = this.canvas.width; // Reset canvas
        this.ctx = this.canvas.getContext('2d');
        this.samples = samples || 1000;
        this.ranges = ranges || [];
        this.functions = functions || [];
        this.border = 25;
        this.dot = 1;
        this.addFunction = function(f,c) {this.functions 
            = this.functions.concat(Array([f,c]))};
        this.addRange = function(data,c) {this.ranges
            = this.ranges.concat(Array([data,c]))};
    },
    draw: function() {
        this.drawDots(null, 1.5);
        for (var i in this.ranges)
            this.drawRange(this.ranges[i][0], this.ranges[i][1]);
        for (var i in this.functions)
            this.drawFunction(this.functions[i][0], this.functions[i][1]);
            
        this.drawAxes();
    },
    plot: function(f) {
        this.addFunction(f); this.draw();
    },
    addRange: function(data, c) {
        this.ranges = this.ranges.concat(Array([data, c]));
    },
    addFunction: function(f, c) {
        this.functions = this.functions.concat(Array([f, c]));
    },
});

var CartesianPlot = Plot.extend({
    init: function(id, xmin, xmax, ymin, ymax, samples, ranges, functions) {
        this._super(id, samples, ranges, functions);
        this.xmin = xmin || -10;
        this.xmax = xmax || 10;
        this.ymin = ymin || -10;
        this.ymax = ymax || 10;
    },
    xrange: function() { return this.xmax - this.xmin },
    xunit: function() { 
        return (this.canvas.width - 2*this.border) / this.xrange()
    },
    yrange: function() { return this.ymax - this.ymin },
    yunit: function() { 
        return (this.canvas.height - 2*this.border) / this.yrange()
    },
    step: function() { return this.xrange() / this.samples },
    xToPx: function(x) {
        return this.border + (x - this.xmin)*this.xunit()
    },
    yToPx: function(y) {
        return this.canvas.height - (y - this.ymin)*this.yunit()
            - this.border
    },
    drawFunction: function(f, colour, dotsize) {
        colour = colour || '#FF0000'; dotsize = dotsize || this.dot;
        for (var x = this.xmin; x <= this.xmax; x += this.step())
            this.plotPoint(x, f(x), colour, dotsize);
    },
    drawRange: function(data, colour, dotsize) {
        colour = colour || '#FF0000'; dotsize = dotsize || this.dot;
        for (var i in data)
            this.plotPoint(data[i][0], data[i][1], colour, dotsize);
    },
    plotPoint: function(x, y, colour, dotsize) {
        colour = colour || '#FF0000'; dotsize = dotsize || this.dot;
        if (this.xmin <= x && x <= this.xmax && this.ymin <= y 
            && y <= this.ymax) {
            this.ctx.fillStyle = colour;
            this.ctx.beginPath();
            this.ctx.arc(this.xToPx(x), this.yToPx(y), dotsize, 0, Math.PI*2,
                true);
            this.ctx.closePath();
            this.ctx.fill();
        }
    },
    drawAxes: function() {
        with (this) {
            // Properties of line
            ctx.beginPath();
            ctx.strokeStyle = '#000';
            ctx.lineWidth = 1;
            // x-axis
            ctx.moveTo(xToPx(xmin), yToPx(0));
            ctx.lineTo(xToPx(xmax), yToPx(0));
            // y-axis
            ctx.moveTo(xToPx(0), yToPx(ymin));
            ctx.lineTo(xToPx(0), yToPx(ymax));
            // Draw
            ctx.stroke();
            ctx.closePath();
            
            // Labels
            ctx.fillStyle = '#7f7f7f';
            ctx.textBaseline = 'middle';
            ctx.textAlign = 'center';
            ctx.font = '10pt sans-serif';
            // x-axis
            for (var x = xmin; x <= xmax; ++x)
                if (x != 0) ctx.fillText(x, xToPx(x), yToPx(0) + 10);
            ctx.fillText('X', xToPx(xmax), yToPx(0) - 10);
            // y-axis
            for (var y = ymin; y <= ymax; ++y)
                if (y != 0) ctx.fillText(y, xToPx(0) - 14, yToPx(y));
            ctx.fillText('Y', xToPx(0) + 10, yToPx(ymax));
            
            // Origin
            ctx.beginPath()
            ctx.strokeStyle = '#000';
            ctx.lineWidth = 0.5;
            ctx.arc(xToPx(0), yToPx(0), 6, 0, Math.PI*2, true);
            ctx.stroke();
            ctx.closePath();
        }
    },
    drawDots: function(colour, dotsize) {
        colour = colour || '#c3c3c3'; dotsize = dotsize || 2;
        for (var x = this.xmin; x <= this.xmax; ++x)
            for (var y = this.ymin; y <= this.ymax; ++y)
                if (y != 0 && x != 0)
                    this.plotPoint(x, y, colour, dotsize)
                else
                    this.plotPoint(x, y, '#000', dotsize);
    },
});

CartesianPlot.prototype.simplePlot = simplePlot;

// A polar plot of the equation r = f(a)
var PolarPlot = Plot.extend({
    init: function(id, amin, amax, rmax, samples, ranges, functions) {
        this._super(id, samples, ranges, functions);
        this.amin = amin || -Math.PI;
        this.amax = amax || Math.PI;
        this.rmax = rmax || 10;
    },
    xunit: function() { 
        return (this.canvas.width - 2*this.border) / (2*this.rmax)
    },
    yunit: function() { 
        return (this.canvas.height - 2*this.border) / (2*this.rmax)
    },
    step: function() { return (this.amax - this.amin) / this.samples },
    xToPx: function(x) {
        return this.border + (x + this.rmax)*this.xunit()
    },
    yToPx: function(y) {
        return this.canvas.height - (y + this.rmax)*this.yunit()
            - this.border
    },
    raToX: function(r, a) { return r * Math.cos(a) },
    raToXPx: function(r, a) { return this.xToPx(this.raToX(r, a)) },
    raToY: function(r, a) { return r * Math.sin(a) },
    raToYPx: function(r, a) { return this.yToPx(this.raToY(r, a)) },
    plotPoint: function(r, a, colour, dotsize) {
        colour = colour || '#FF0000'; dotsize = dotsize || this.dot;
        if (true) {
            this.ctx.fillStyle = colour;
            this.ctx.beginPath();
            this.ctx.arc(this.raToXPx(r, a), this.raToYPx(r, a), dotsize, 0,
                Math.PI*2, true);
            this.ctx.closePath();
            this.ctx.fill();
        }
    },
    drawFunction: function(f, colour, dotsize) {
        colour = colour || '#FF0000'; dotsize = dotsize || this.dot;
        for (var a = this.amin; a <= this.amax; a += this.step())
            this.plotPoint(f(a), a, colour, dotsize);
    },
    drawRange: function(data, colour, dotsize) {
        colour = colour || '#FF0000'; dotsize = dotsize || this.dot;
        for (var i in data)
            this.plotPoint(data[i][1], data[i][0], colour, dotsize);
    },
    drawAxes: function() {
        with (this) {
            // Properties of line
            ctx.beginPath();
            ctx.strokeStyle = '#000';
            ctx.lineWidth = 1;
            // x-axis
            ctx.moveTo(xToPx(-rmax), yToPx(0));
            ctx.lineTo(xToPx(rmax), yToPx(0));
            // y-axis
            ctx.moveTo(xToPx(0), yToPx(-rmax));
            ctx.lineTo(xToPx(0), yToPx(rmax));
            // Draw
            ctx.stroke();
            ctx.closePath();
            
            // Labels
            ctx.fillStyle = '#7f7f7f';
            ctx.textBaseline = 'middle';
            ctx.textAlign = 'center';
            ctx.font = '10pt sans-serif';
            // x-axis
            for (var x = -rmax; x <= rmax; ++x)
                if (x != 0) ctx.fillText(Math.abs(x), xToPx(x), yToPx(0) + 10);
            // ctx.fillText('r', xToPx(xmax), yToPx(0) - 10);
            // y-axis
            for (var y = -rmax; y <= rmax; ++y)
                if (y != 0) ctx.fillText(Math.abs(y), xToPx(0) - 14, yToPx(y));
            // ctx.fillText('Y', xToPx(0) + 10, yToPx(ymax));
            
            // Origin
            ctx.beginPath()
            ctx.strokeStyle = '#000';
            ctx.lineWidth = 0.5;
            ctx.arc(xToPx(0), yToPx(0), 6, 0, Math.PI*2, true);
            ctx.stroke();
            ctx.closePath();
        }
    },
    drawDots: function(colour, dotsize) {
        colour = colour || '#c3c3c3'; dotsize = dotsize || 2;
        for (var r = -this.rmax; r <= this.rmax; ++r) {
            this.plotPoint(r, 0, '#000', dotsize);
            this.plotPoint(r, Math.PI/2, '#000', dotsize);
        }
    },
});

PolarPlot.prototype.simplePlot = simplePlot;
