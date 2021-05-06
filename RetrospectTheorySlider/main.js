// When the page is fully loaded, the main function will be called
$(document).ready(main);


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
    return `<button id="ok" class="btn custom-button">Submit</button>`;
}

function generateImg(src) {
    return  `<img class="border rounded stim" src="${src}">`;
}

function generateQuestion(question) {
    return `<h5 class="justify-content-center">What was the average value of this symbol?</h5>`;
}
