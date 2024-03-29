// Add a result to the input box
function add_result(a, q) {
    q = q || document.getElementById('question').value;
    q = colour_brackets(q); // a = colour_brackets(a);
    document.getElementById('answers').style.display = '';
    var div = document.createElement('div');
    var answers = document.getElementById('answers');
    div.innerHTML = '<h4 class="question">' + q + '</h4>' + '<p>' + a + '</p>';
    answers.insertBefore(div, answers.firstChild);
    
    if (a.match('/.*canvas.*'))
        eval(a.match('<canvas.*onclick="([^"]*)".*>.*</canvas>')[1]);
}

function calc(x) {
    var y = '';
    $.ajax({
        type: 'GET',
        url: 'calculate',
        dataType: 'json',
        data: {question : x},
        success: function(data) {y = data.answer},
        async: false
    });
    y = y.replace(/(<([^>]+)>|&[a-z]+;)/ig,'');
    y = y.replace(/[^a-z0-9\(\)+\-\*\/\|\[\]\,\.\^\:\=]+/ig,'');
    y = y.slice(1).replace(/None/gi, 'null');
    y = y.replace(/None/gi, 'null');
    try {return eval(y)} catch(err) {return y};
}

// Return the result of a calculation
function calculate(x) {
    x = x || document.getElementById('question').innerHTML;
    x = x.replace(/(<([^>]+)>|&[a-z]+;)/ig,'');
    x = x.replace(/[^a-z0-9\(\) +\-\*\/\|\=\[\]\,\.\^\:\=]+/ig,'');
    $.getJSON('calculate', {question : x}, function(data) {
        add_result( data.answer, x );
    })
}

// List of possible bracket colours
var colours = ['#edd400', '#c4a000', '#8ae234', '#73d216', '#4e9a06', '#fcaf3e',
    '#f57900', '#ce5c00', '#729fcf', '#3465a4', '#204a87', '#ad7fa8', '#75507b',
    '#5c3566', '#e9b96e', '#c17d11', '#8f5902', '#cc0000', '#babdb6', '#888a85',
    '#555753', '#2e3436'];
// Randomize the order of the colours
colours.sort(function(){return Math.random() - 0.5});

// Highlight coresponding brakets in matching colours
function colour_brackets(s) {
    s = s.replace(/<[//]?(br|div|b)[^>]*>/gi,'');
    var i = 0;
    var result = '';
    for (var j in s) {
        if (s[j] == '(') {
            result += '<b style="color : ' + colours[i] + '">(</b>';
            i++;
        } else if (s[j] == ')') {
            i--;
            result += (i >= 0) 
                ? ('<b style="color : ' + colours[i] + '">)</b>')
                : ('<b style="background-color: #a40000; color: white">)</b>');
        } else {
            result += s[j]
        }
    }
    return result
}

// Highlight input and update page on keypresses
function keypress() {
    var sel = rangy.saveSelection();
    if (event.keyCode==13) { calculate(); }
    document.getElementById('question').innerHTML 
        = colour_brackets(document.getElementById('question').innerHTML);
    rangy.restoreSelection(sel);
}
