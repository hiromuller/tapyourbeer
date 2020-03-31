var $document = $(document);
var $graph_area = $('#graph_area');
var $xloc = $('#xloc');
var $yloc = $('#yloc');
var supportTouch = 'ontouchend' in document;
var graph_size_x = 600;
var graph_size_y = 600;
var form = document.forms.add_comment;

var EVENTNAME_TOUCHSTART = supportTouch ? 'touchstart' : 'mousedown';
var EVENTNAME_TOUCHMOVE = supportTouch ? 'touchmove' : 'mousemove';
var EVENTNAME_TOUCHEND = supportTouch ? 'touchend' : 'mouseup';

var updateXY = function(event) {
// jQueryのイベントはオリジナルのイベントをラップしたもの。
// changedTouchesが欲しいので、オリジナルのイベントオブジェクトを取得
  var original = event.originalEvent;
  var xloc_org, yloc_org, xloc_mod, yloc_mod;
  if(original.changedTouches) {
    bounds = original.changedTouches[0].target.getBoundingClientRect();
    xloc_org = original.changedTouches[0].clientX - bounds.left;
    yloc_org = original.changedTouches[0].clientY - bounds.top;
  } else {
    xloc_org = event.pageX;
    yloc_org = event.pageY;
  }

  xloc_mod = Math.round((xloc_org - (graph_size_x / 2)) / (graph_size_x / 2 / 100));
  yloc_mod = Math.round((yloc_org * (-1) + (graph_size_y / 2)) / (graph_size_y / 2 / 100));

  $xloc.text(xloc_mod);
  $yloc.text(yloc_mod);
  form.x.value = xloc_mod;
  form.y.value = yloc_mod;
  var w = $('#click').width();
  var h = $('#click').height();
  $(window).on('click', function(e) {
    var x_dot, y_dot;
    var x_dot = original.changedTouches[0].clientX;
    var y_dot = original.changedTouches[0].clientY;
    $('#click').css({
      top: y_dot,
      left: x_dot
    });
  });

};

var handleStart = function(event) {
  updateXY(event);
  bindMoveAndEnd();
};
var handleMove = function(event) {
  event.preventDefault(); // タッチによる画面スクロールを止める
  updateXY(event);
};
var handleEnd = function(event) {
  updateXY(event);
  unbindMoveAndEnd();
};
var bindMoveAndEnd = function() {
  $document.on('touchmove', handleMove);
  $document.on('touchend', handleEnd);
};
var unbindMoveAndEnd = function() {
  $document.off('touchmove', handleMove);
  $document.off('touchend', handleEnd);
};

$graph_area.on('touchstart', handleStart);
