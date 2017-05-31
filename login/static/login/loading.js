function change(){
$("#maskDiv").css("display","block");

function ProgressBarWin8() {
  this.fixed = {left: 0, top: 0};
  this.position = {left: 0, top: 0};
  this.radius = 70;
  this.angle = 270;
  this.delay = 30;
  this.timer = null;
  this.dom = null;
  this.style = {
    position: "absolute",
    width: "10px",
    height: "10px",
    background: "#00FF00",
    "border-radius": "5px"
  };
}

ProgressBarWin8.prototype = {
  run: function() {
    if (this.timer) {
    clearTimeout(this.timer);
    }
    this.position.left = Math.cos(Math.PI * this.angle / 180) * this.radius + this.fixed.left;
    this.position.top = Math.sin(Math.PI * this.angle / 180) * this.radius + this.fixed.top;
    this.dom.style.left = this.position.left + "px";
    this.dom.style.top = this.position.top + "px";
    this.angle++;
    if (this.position.left < this.fixed.left) {
      this.delay += .5;
    } else {
      this.delay -= .5;
    }
    var scope = this;
    this.timer = setTimeout(function () {
      scope.run();
      }, this.delay);
  },

  defaultSetting: function () {
    this.dom = document.createElement("span");
    for (var property in this.style) {
      this.dom.style[property] = this.style[property];
    }
    this.fixed.left = window.innerWidth / 2;
    this.fixed.top = window.innerHeight / 2;
    this.position.left = Math.cos(Math.PI * this.angle / 180) * this.radius + this.fixed.left;
    this.position.top = Math.sin(Math.PI * this.angle / 180) * this.radius + this.fixed.top;
    this.dom.style.left = this.position.left + "px";
    this.dom.style.top = this.position.top + "px";
    document.body.appendChild(this.dom);
    return this;
  }
};

var progressArray = [],
tempArray = [],
timer = 200;

for (var i = 0; i < 5; ++i) {
  progressArray.push(new ProgressBarWin8().defaultSetting());
}

Array.prototype.each = function (fn) {
  for (var i = 0, len = this.length; i < len;) {
    fn.call(this[i++], arguments);
  }
};

window.onresize = function () {
  tempArray.each(function () {
    this.fixed.left = window.innerWidth / 2;
    this.fixed.top = window.innerHeight / 2;
  });
};

timer = setInterval(function () {
  if (progressArray.length <= 0) {
    clearInterval(timer);
  } else {
    var entity = progressArray.shift();
    tempArray.push(entity);
    entity.run();
  }
},timer);
}
