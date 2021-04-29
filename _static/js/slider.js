
function main() {

    // params
    let min = -90;
    let max = 90;
    let step = .5;
    let question = 'What was the average value of this symbol?'

    let initValue = range(-60, 60, 1)[Math.floor(Math.random() * 10)];
    let clickEnabled = true;

    // generate html
    let sliderHTML = SliderManager.generateSlider({ text: question,
        min: min, max: max, step: step, initValue: initValue});

    let buttonHTML = generateSubmitButton();
    let imgHTML = generateImg('img/index.png')
    let questionHTML = generateQuestion(question);

    // insert in html
    appendElement('Stage', questionHTML);
    appendElement('Stage', imgHTML);
    appendElement('Stage', sliderHTML);
    appendElement('GameButton', buttonHTML);

    // listen on events
    SliderManager.listenOnSlider({}, function (event) {
        if (clickEnabled) {
            // they can click only once
            // clickEnabled = false;
            let choice = event.data.slider.val();
            SliderManager.clickEvent(choice);
        }
    });

    // allows to change value using left and right arrows
    SliderManager.listenOnArrowKeys();
}


class SliderManager {
    // class using static functions (i.e. each func can be extracted
    // from the class directly, there are no public members) to manage the slider

    static generateSlider({
                              min = 0, max = 100, step = 5,
                              initValue = 0,
                              classname = 'slider'
                          } = {}) {
        let slider = `<main style="flex-basis: 100%">
            <form id="form" class="${classname}">
            <div class="range">
            <input id="slider" name="range" type="range" value="${initValue}" min="${min}" max="${max}" step="${step}">
            <div class="range-output">
            <output id="output" class="output" name="output" for="range">
            ${initValue}
             </output>
             </div>
             </div>
            </form>
            </main>`;

        return slider;
    }
    static listenOnArrowKeys() {
        document.onkeydown = checkKey;

        function checkKey(e) {
            let sliderObj = $('#slider');

            let value = parseFloat(sliderObj.val());
            let step = parseFloat(sliderObj.attr('step'));

            e = e || window.event;

            if (e.keyCode == '37') {
                // left arrow
                sliderObj.val(value - step).change();
            }
            else if (e.keyCode == '39') {
                // right arrow
                sliderObj.val(value + step).change();
            }

        }
    }
    static listenOnSlider(clickArgs, clickFunc) {

        rangeInputRun();
        let slider = $('#slider');
        let output = document.getElementById('output');
        let form = document.getElementById('form');

        form.oninput = function () {
            output.value = slider.val();
        };

        clickArgs.slider = slider;

        let ok = $('#ok');
        ok.click(clickArgs, clickFunc);

        return slider
    }

    static clickEvent(choice) {
        alert(`Value is ${choice}`);
    }
}

// simple range function
function range(start, stop, step) {
    let a = [start], b = start;
    while (b < stop) {
        a.push(b += step || 1);
    }
    return a;
}

//append to div
function appendElement(divId, el) {
    $(`#${divId}`).append(el);
}

function generateSubmitButton(n) {
    return `<div align="center"><button type="button" id="ok" class="drawn-button">CONTRIBUTE</button></div>`;
}

function generateImg(src) {
    return  `<img class="border rounded stim" src="${src}">`;
}

function generateQuestion(question) {
    return `<h5 class="justify-content-center">What was the average value of this symbol?</h5>`;
}


function rangeInputRun() {

    const END = 'change';
    const START = 'ontouchstart' in document ? 'touchstart' : 'mousedown';
    const INPUT = 'input';
    const MAX_ROTATION = 1;
    const SOFTEN_FACTOR = 3;

    class RangeInput {

        constructor(el) {
            this.el = el;

            this._handleEnd = this._handleEnd.bind(this);
            this._handleStart = this._handleStart.bind(this);
            this._handleInput = this._handleInput.bind(this);

            //Call the plugin
            $(this.el.querySelector('input[type=range]')).rangeslider({
                polyfill: false, //Never use the native polyfill
                rangeClass: 'rangeslider',
                disabledClass: 'rangeslider-disabled',
                horizontalClass: 'rangeslider-horizontal',
                verticalClass: 'rangeslider-vertical',
                fillClass: 'rangeslider-fill-lower',
                handleClass: 'rangeslider-thumb',
                onInit: function () {
                    //No args are passed, so we can't change context of this
                    const pluginInstance = this;

                    //Move the range-output inside the handle so we can do all the stuff in css
                    $(pluginInstance.$element)
                        .parents('.range')
                        .find('.range-output')
                        .appendTo(pluginInstance.$handle);
                }
            });

            this.sliderThumbEl = el.querySelector('.rangeslider-thumb');
            this.outputEl = el.querySelector('.range-output');
            this.inputEl = el.querySelector('input[type=range]');
            this._lastOffsetLeft = 0;
            this._lastTimeStamp = 0;

            this.el.querySelector('.rangeslider').addEventListener(START, this._handleStart);
        }

        _handleStart(e) {
            this._lastTimeStamp = new Date().getTime();
            this._lastOffsetLeft = this.sliderThumbEl.offsetLeft;

            //Wrap in raf because offsetLeft is updated by the plugin after this fires
            requestAnimationFrame(_ => {
                //Bind through jquery because plugin doesn't fire native event
                $(this.inputEl).on(INPUT, this._handleInput);
                $(this.inputEl).on(END, this._handleEnd);
            });
        }

        _handleEnd(e) {
            //Unbind through jquery because plugin doesn't fire native event
            $(this.inputEl).off(INPUT, this._handleInput);
            $(this.inputEl).off(END, this._handleEnd);

            requestAnimationFrame(_ => this.outputEl.style.transform = 'rotate(0deg)')
        }

        _handleInput(e) {
            let now = new Date().getTime();
            let timeElapsed = now - this._lastTimeStamp || 1;
            let distance = this.sliderThumbEl.offsetLeft - this._lastOffsetLeft;
            let direction = distance < 0 ? -1 : 1;
            let velocity = Math.abs(distance) / timeElapsed; //pixels / millisecond
            let targetRotation = Math.min(Math.abs(distance * velocity) * SOFTEN_FACTOR, MAX_ROTATION);

            requestAnimationFrame(_ => this.outputEl.style.transform = 'rotate(' + targetRotation * -direction + 'deg)');

            this._lastTimeStamp = now;
            this._lastOffsetLeft = this.sliderThumbEl.offsetLeft;
        }

    }


    /*! rangeslider.js - v2.1.1 | (c) 2016 @andreruffert | MIT license | https://github.com/andreruffert/rangeslider.js */
    !function (a) {
        "use strict";
        "function" == typeof define && define.amd ? define(["jquery"], a) : "object" == typeof exports ? module.exports = a(require("jquery")) : a(jQuery)
    }(function (a) {
        "use strict";

        function b() {
            var a = document.createElement("input");
            return a.setAttribute("type", "range"), "text" !== a.type
        }

        function c(a, b) {
            var c = Array.prototype.slice.call(arguments, 2);
            return setTimeout(function () {
                return a.apply(null, c)
            }, b)
        }

        function d(a, b) {
            return b = b || 100, function () {
                if (!a.debouncing) {
                    var c = Array.prototype.slice.apply(arguments);
                    a.lastReturnVal = a.apply(window, c), a.debouncing = !0
                }
                return clearTimeout(a.debounceTimeout), a.debounceTimeout = setTimeout(function () {
                    a.debouncing = !1
                }, b), a.lastReturnVal
            }
        }

        function e(a) {
            return a && (0 === a.offsetWidth || 0 === a.offsetHeight || a.open === !1)
        }

        function f(a) {
            for (var b = [], c = a.parentNode; e(c);) b.push(c), c = c.parentNode;
            return b
        }

        function g(a, b) {
            function c(a) {
                "undefined" != typeof a.open && (a.open = a.open ? !1 : !0)
            }

            var d = f(a), e = d.length, g = [], h = a[b];
            if (e) {
                for (var i = 0; e > i; i++) g[i] = d[i].style.cssText, d[i].style.setProperty ? d[i].style.setProperty("display", "block", "important") : d[i].style.cssText += ";display: block !important", d[i].style.height = "0", d[i].style.overflow = "hidden", d[i].style.visibility = "hidden", c(d[i]);
                h = a[b];
                for (var j = 0; e > j; j++) d[j].style.cssText = g[j], c(d[j])
            }
            return h
        }

        function h(a, b) {
            var c = parseFloat(a);
            return Number.isNaN(c) ? b : c
        }

        function i(a) {
            return a.charAt(0).toUpperCase() + a.substr(1)
        }

        function j(b, e) {
            if (this.$window = a(window), this.$document = a(document), this.$element = a(b), this.options = a.extend({}, n, e), this.polyfill = this.options.polyfill, this.orientation = this.$element[0].getAttribute("data-orientation") || this.options.orientation, this.onInit = this.options.onInit, this.onSlide = this.options.onSlide, this.onSlideEnd = this.options.onSlideEnd, this.DIMENSION = o.orientation[this.orientation].dimension, this.DIRECTION = o.orientation[this.orientation].direction, this.DIRECTION_STYLE = o.orientation[this.orientation].directionStyle, this.COORDINATE = o.orientation[this.orientation].coordinate, this.polyfill && m) return !1;
            this.identifier = "js-" + k + "-" + l++, this.startEvent = this.options.startEvent.join("." + this.identifier + " ") + "." + this.identifier, this.moveEvent = this.options.moveEvent.join("." + this.identifier + " ") + "." + this.identifier, this.endEvent = this.options.endEvent.join("." + this.identifier + " ") + "." + this.identifier, this.toFixed = (this.step + "").replace(".", "").length - 1, this.$fill = a('<div class="' + this.options.fillClass + '" />'), this.$handle = a('<div class="' + this.options.handleClass + '" />'), this.$range = a('<div class="' + this.options.rangeClass + " " + this.options[this.orientation + "Class"] + '" id="' + this.identifier + '" />').insertAfter(this.$element).prepend(this.$fill, this.$handle), this.$element.css({
                position: "absolute",
                width: "1px",
                height: "1px",
                overflow: "hidden",
                opacity: "0"
            }), this.handleDown = a.proxy(this.handleDown, this), this.handleMove = a.proxy(this.handleMove, this), this.handleEnd = a.proxy(this.handleEnd, this), this.init();
            var f = this;
            this.$window.on("resize." + this.identifier, d(function () {
                c(function () {
                    f.update(!1, !1)
                }, 300)
            }, 20)), this.$document.on(this.startEvent, "#" + this.identifier + ":not(." + this.options.disabledClass + ")", this.handleDown), this.$element.on("change." + this.identifier, function (a, b) {
                if (!b || b.origin !== f.identifier) {
                    var c = a.target.value, d = f.getPositionFromValue(c);
                    f.setPosition(d)
                }
            })
        }

        Number.isNaN = Number.isNaN || function (a) {
            return "number" == typeof a && a !== a
        };
        var k = "rangeslider", l = 0, m = b(), n = {
            polyfill: !0,
            orientation: "horizontal",
            rangeClass: "rangeslider",
            disabledClass: "rangeslider--disabled",
            horizontalClass: "rangeslider--horizontal",
            verticalClass: "rangeslider--vertical",
            fillClass: "rangeslider__fill",
            handleClass: "rangeslider__handle",
            startEvent: ["mousedown", "touchstart", "pointerdown"],
            moveEvent: ["mousemove", "touchmove", "pointermove"],
            endEvent: ["mouseup", "touchend", "pointerup"]
        }, o = {
            orientation: {
                horizontal: {
                    dimension: "width",
                    direction: "left",
                    directionStyle: "left",
                    coordinate: "x"
                }, vertical: {dimension: "height", direction: "top", directionStyle: "bottom", coordinate: "y"}
            }
        };
        return j.prototype.init = function () {
            this.update(!0, !1), this.onInit && "function" == typeof this.onInit && this.onInit()
        }, j.prototype.update = function (a, b) {
            a = a || !1, a && (this.min = h(this.$element[0].getAttribute("min"), 0), this.max = h(this.$element[0].getAttribute("max"), 100), this.value = h(this.$element[0].value, Math.round(this.min + (this.max - this.min) / 2)), this.step = h(this.$element[0].getAttribute("step"), 1)), this.handleDimension = g(this.$handle[0], "offset" + i(this.DIMENSION)), this.rangeDimension = g(this.$range[0], "offset" + i(this.DIMENSION)), this.maxHandlePos = this.rangeDimension - this.handleDimension, this.grabPos = this.handleDimension / 2, this.position = this.getPositionFromValue(this.value), this.$element[0].disabled ? this.$range.addClass(this.options.disabledClass) : this.$range.removeClass(this.options.disabledClass), this.setPosition(this.position, b)
        }, j.prototype.handleDown = function (a) {
            if (this.$document.on(this.moveEvent, this.handleMove), this.$document.on(this.endEvent, this.handleEnd), !((" " + a.target.className + " ").replace(/[\n\t]/g, " ").indexOf(this.options.handleClass) > -1)) {
                var b = this.getRelativePosition(a), c = this.$range[0].getBoundingClientRect()[this.DIRECTION],
                    d = this.getPositionFromNode(this.$handle[0]) - c,
                    e = "vertical" === this.orientation ? this.maxHandlePos - (b - this.grabPos) : b - this.grabPos;
                this.setPosition(e), b >= d && b < d + this.handleDimension && (this.grabPos = b - d)
            }
        }, j.prototype.handleMove = function (a) {
            a.preventDefault();
            var b = this.getRelativePosition(a),
                c = "vertical" === this.orientation ? this.maxHandlePos - (b - this.grabPos) : b - this.grabPos;
            this.setPosition(c)
        }, j.prototype.handleEnd = function (a) {
            a.preventDefault(), this.$document.off(this.moveEvent, this.handleMove), this.$document.off(this.endEvent, this.handleEnd), this.$element.trigger("change", {origin: this.identifier}), this.onSlideEnd && "function" == typeof this.onSlideEnd && this.onSlideEnd(this.position, this.value)
        }, j.prototype.cap = function (a, b, c) {
            return b > a ? b : a > c ? c : a
        }, j.prototype.setPosition = function (a, b) {
            var c, d;
            void 0 === b && (b = !0), c = this.getValueFromPosition(this.cap(a, 0, this.maxHandlePos)), d = this.getPositionFromValue(c), this.$fill[0].style[this.DIMENSION] = d + this.grabPos + "px", this.$handle[0].style[this.DIRECTION_STYLE] = d + "px", this.setValue(c), this.position = d, this.value = c, b && this.onSlide && "function" == typeof this.onSlide && this.onSlide(d, c)
        }, j.prototype.getPositionFromNode = function (a) {
            for (var b = 0; null !== a;) b += a.offsetLeft, a = a.offsetParent;
            return b
        }, j.prototype.getRelativePosition = function (a) {
            var b = i(this.COORDINATE), c = this.$range[0].getBoundingClientRect()[this.DIRECTION], d = 0;
            return "undefined" != typeof a["page" + b] ? d = a["client" + b] : "undefined" != typeof a.originalEvent["client" + b] ? d = a.originalEvent["client" + b] : a.originalEvent.touches && a.originalEvent.touches[0] && "undefined" != typeof a.originalEvent.touches[0]["client" + b] ? d = a.originalEvent.touches[0]["client" + b] : a.currentPoint && "undefined" != typeof a.currentPoint[this.COORDINATE] && (d = a.currentPoint[this.COORDINATE]), d - c
        }, j.prototype.getPositionFromValue = function (a) {
            var b, c;
            return b = (a - this.min) / (this.max - this.min), c = Number.isNaN(b) ? 0 : b * this.maxHandlePos
        }, j.prototype.getValueFromPosition = function (a) {
            var b, c;
            return b = a / (this.maxHandlePos || 1), c = this.step * Math.round(b * (this.max - this.min) / this.step) + this.min, Number(c.toFixed(this.toFixed))
        }, j.prototype.setValue = function (a) {
            (a !== this.value || "" === this.$element[0].value) && this.$element.val(a).trigger("input", {origin: this.identifier})
        }, j.prototype.destroy = function () {
            this.$document.off("." + this.identifier), this.$window.off("." + this.identifier), this.$element.off("." + this.identifier).removeAttr("style").removeData("plugin_" + k), this.$range && this.$range.length && this.$range[0].parentNode.removeChild(this.$range[0])
        }, a.fn[k] = function (b) {
            var c = Array.prototype.slice.call(arguments, 1);
            return this.each(function () {
                var d = a(this), e = d.data("plugin_" + k);
                e || d.data("plugin_" + k, e = new j(this, b)), "string" == typeof b && e[b].apply(e, c)
            })
        }, "rangeslider.js is available in jQuery context e.g $(selector).rangeslider(options);"
    });


    new RangeInput(document.querySelector('.range'));
}